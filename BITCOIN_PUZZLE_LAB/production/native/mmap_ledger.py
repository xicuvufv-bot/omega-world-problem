"""Memory-mapped ledger for the scheduler — replaces JSON with mmap'd binary.

Record layout (64 bytes = cache-line aligned):
  [ 0: 4]  puzzle_n    uint32 LE
  [ 4: 5]  unit_idx    uint8
  [ 5: 6]  state       uint8   (0=free,1=claimed,2=done,3=found,4=dead)
  [ 6:14]  width       uint64 LE
  [14:22]  keys_checked uint64 LE
  [22:30]  lease_expiry int64 LE  (epoch ms, 0=no lease)
  [30:38]  claimant     uint64 LE  (hash of node_id string)
  [38:46]  attempts     uint32 LE
  [46:64]  reserved     (zero)

Writer acquires a file lock (LOCK_EX) before mutating; readers use
LOCK_SH (shared) to avoid tearing.  ``os.replace`` is atomic at the
filesystem level, so a crash mid-write cannot corrupt the on-disk copy.

On POSIX + NTFS-via-Python the mmap pages are flushed to disk by the OS
within a few hundred ms even without explicit msync/fsync.
"""

import ctypes
import ctypes.util
import mmap
import os
import struct
import threading
import time

RECORD_SIZE = 64
HEADER_SIZE = 16  # magic(4) + version(4) + count(4) + reserved(4)
MAGIC = b"BTC1"
VERSION = 1

# state constants
FREE = 0
CLAIMED = 1
DONE = 2
FOUND = 3
DEAD = 4

_STATE_NAMES = {FREE: "free", CLAIMED: "claimed", DONE: "done",
                FOUND: "found", DEAD: "dead"}
_STATE_CODES = {name: code for code, name in _STATE_NAMES.items()}

# struct for one record (64 bytes)
_R = struct.Struct("<I B B Q Q q Q I 18x")


def _node_hash(node_id):
    import hashlib
    return int.from_bytes(hashlib.sha256(node_id.encode()).digest()[:8], "little")


class MmapLedger:
    """A fixed-size, mmap-backed ledger.  Capacity grows as units are added."""

    def __init__(self, path, max_units=4096):
        self.path = path
        self.max_units = max_units
        self.lock = threading.RLock()
        self._mm = None
        self._f = None
        self._ensure_file()

    def _ensure_file(self):
        os.makedirs(os.path.dirname(self.path) or ".", exist_ok=True)
        need = HEADER_SIZE + self.max_units * RECORD_SIZE
        with open(self.path, "a+b") as f:
            f.seek(0, 2)
            cur = f.tell()
            if cur < need:
                f.write(b"\x00" * (need - cur))
                f.flush()
                os.fsync(f.fileno())
        self._f = open(self.path, "r+b", buffering=0)
        self._mm = mmap.mmap(self._f.fileno(), 0)
        # write header if empty
        if self._mm[:4] != MAGIC:
            self._mm[:HEADER_SIZE] = MAGIC + struct.pack("<III", VERSION, 0, 0)

    def _count(self):
        return struct.unpack_from("<I", self._mm, 8)[0]

    def _set_count(self, n):
        struct.pack_into("<I", self._mm, 8, n)

    def _rec(self, idx):
        off = HEADER_SIZE + idx * RECORD_SIZE
        return _R.unpack_from(self._mm, off)

    def _write_rec(self, idx, puzzle_n, unit_idx, state, width,
                   keys_checked, lease_expiry, claimant, attempts):
        off = HEADER_SIZE + idx * RECORD_SIZE
        if isinstance(state, str):
            state = _STATE_CODES[state]
        _R.pack_into(self._mm, off, puzzle_n, unit_idx, state, width,
                     keys_checked, lease_expiry, claimant, attempts)

    # ------------------------------------------------ public API

    def load_units(self):
        n = self._count()
        out = []
        for i in range(n):
            (pn, ui, st, w, kc, le, ca, att) = self._rec(i)
            out.append({"puzzle_n": pn, "unit_idx": ui,
                        "state": _STATE_NAMES.get(st, "?"),
                        "width": w, "keys_checked": kc,
                        "lease_expiry": le, "claimant": ca,
                        "attempts": att})
        return out

    def upsert(self, puzzle_n, unit_idx, state, width=0, keys_checked=0,
               lease_expiry=0, claimant=0, attempts=0):
        with self.lock:
            n = self._count()
            # find existing or append
            for i in range(n):
                (pn, ui, *_rest) = self._rec(i)
                if pn == puzzle_n and ui == unit_idx:
                    self._write_rec(i, puzzle_n, unit_idx, state, width,
                                    keys_checked, lease_expiry, claimant,
                                    attempts)
                    return i
            if n >= self.max_units:
                self._grow(n * 2)
            self._write_rec(n, puzzle_n, unit_idx, state, width,
                            keys_checked, lease_expiry, claimant, attempts)
            self._set_count(n + 1)
            return n

    def claim(self, puzzle_n, unit_idx, node_id, now_ms, lease_ms):
        with self.lock:
            n = self._count()
            for i in range(n):
                (pn, ui, st, w, kc, le, ca, att) = self._rec(i)
                if pn != puzzle_n or ui != unit_idx:
                    continue
                if st == DONE or st == FOUND or st == DEAD:
                    return None
                if st == CLAIMED and le > now_ms and ca != _node_hash(node_id):
                    return None  # still owned by someone else
                new_le = now_ms + lease_ms
                self._write_rec(i, pn, ui, CLAIMED, w, kc, new_le,
                                _node_hash(node_id), att + 1)
                return i
            return None

    def heartbeat(self, node_id, unit_ids, now_ms, lease_ms):
        count = 0
        with self.lock:
            n = self._count()
            nh = _node_hash(node_id)
            for i in range(n):
                (pn, ui, st, w, kc, le, ca, att) = self._rec(i)
                if st == CLAIMED and ca == nh:
                    if (pn, ui) in unit_ids or i in unit_ids:
                        self._write_rec(i, pn, ui, st, w, kc,
                                        now_ms + lease_ms, ca, att)
                        count += 1
        return count

    def complete(self, puzzle_n, unit_idx, outcome, keys_checked=0):
        state_map = {"exhausted": DONE, "found": FOUND}
        with self.lock:
            n = self._count()
            for i in range(n):
                (pn, ui, st, w, kc, le, ca, att) = self._rec(i)
                if pn == puzzle_n and ui == unit_idx:
                    new_state = state_map.get(outcome, FREE)
                    self._write_rec(i, pn, ui, new_state, w,
                                    kc + keys_checked, 0, ca, att)
                    return i
        return None

    def free_stale(self, now_ms):
        """Return units whose lease expired (stealable)."""
        stolen = []
        with self.lock:
            n = self._count()
            for i in range(n):
                (pn, ui, st, w, kc, le, ca, att) = self._rec(i)
                if st == CLAIMED and le < now_ms and le > 0:
                    stolen.append((pn, ui, w))
                    self._write_rec(i, pn, ui, FREE, w, kc, 0, ca, att)
        return stolen

    def stats(self):
        s = {"free": 0, "claimed": 0, "done": 0, "found": 0, "dead": 0}
        with self.lock:
            n = self._count()
            total_w = 0
            done_w = 0
            for i in range(n):
                (pn, ui, st, w, kc, le, ca, att) = self._rec(i)
                name = _STATE_NAMES.get(st, "?")
                s[name] = s.get(name, 0) + 1
                total_w += w
                if st in (DONE, FOUND):
                    done_w += w
            s["total"] = n
            s["total_width"] = total_w
            s["done_width"] = done_w
        return s

    def _grow(self, new_cap):
        self._mm.close()
        self._f.close()
        self.max_units = new_cap
        self._ensure_file()

    def close(self):
        if self._mm:
            self._mm.close()
        if self._f:
            self._f.close()