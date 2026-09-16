"""Coordinator-side scheduler: a lease-based pool of work units.

Model
   * R1 (BitCrack) puzzles are sliced into independent, stealable units.
   * R2 (Kangaroo) puzzles are a single unit per puzzle — the interval's
     Pollard DPs must be shared, so only one worker may own it; scale-out for
     R2 is the JLP client/server path, not slicing.
   * A unit is CLAIMED with (node_id, lease_expiry).  A node heartbeat
     extends the lease.  If the owner goes silent past the expiry, ANY node
     may claim it again: lease expiry IS the work-stealing trigger.
   * Every mutation (claim/steal/done/found) is appended to an atomic ledger
     (tmpfile + fsync + os.replace) so the pool can survive coordinator
     restart without re-dispatching completed ranges.
"""

import json
import os
import threading
import time

ONE_HOUR_MS = 3600_000


class Unit:
    __slots__ = ("uid", "puzzle_n", "engine", "start_hex", "end_hex",
                 "width", "state", "claimant", "lease_expiry", "attempts",
                 "keys_checked", "outcome")

    def __init__(self, uid, puzzle_n, engine, start_hex, end_hex, width):
        self.uid = uid
        self.puzzle_n = puzzle_n
        self.engine = engine
        self.start_hex = start_hex
        self.end_hex = end_hex
        self.width = width
        self.state = "free"        # free | claimed | done | found | dead
        self.claimant = None
        self.lease_expiry = None   # epoch ms
        self.attempts = 0
        self.keys_checked = 0
        self.outcome = None

    def to_dict(self):
        return {k: getattr(self, k) for k in self.__slots__}


class Scheduler:
    def __init__(self, units, lease_ms=60_000, now_fn=None):
        self.units = {u.uid: u for u in units}
        self.lease_ms = lease_ms
        self.now = now_fn or (lambda: int(time.time() * 1000))
        self.lock = threading.RLock()
        self._gen = 0   # bump on every mutation (for dashboard pushes)

    # ------------------------------------------------------------- sources
    def save(self, path):
        ledger = [u.to_dict() for u in self.units.values()]
        with self.lock:
            tmp = path + ".tmp"
            with open(tmp, "w", encoding="utf-8") as fh:
                json.dump(ledger, fh, sort_keys=True)
                fh.flush()
                os.fsync(fh.fileno())
            os.replace(tmp, path)   # atomic on POSIX + NTFS same volume
            self._gen += 1

    @classmethod
    def load(cls, path, now_fn=None):
        with open(path, "r", encoding="utf-8") as fh:
            rows = json.load(fh)
        units = []
        for r in rows:
            u = Unit(r["uid"], r["puzzle_n"], r["engine"],
                     r["start_hex"], r["end_hex"], r["width"])
            for slot in u.__slots__:
                setattr(u, slot, r[slot])
            units.append(u)
        sch = cls(units, lease_ms=60_000, now_fn=now_fn)
        # a stolen/claimed unit whose lease is stale comes back free
        t = sch.now()
        for u in sch.units.values():
            if u.state == "claimed" and u.lease_expiry and u.lease_expiry < t:
                u.state = "free"
                u.claimant = None
                u.lease_expiry = None
        return sch

    # ------------------------------------------------------------- queries
    def stats(self):
        with self.lock:
            s = {"free": 0, "claimed": 0, "done": 0, "found": 0, "dead": 0}
            for u in self.units.values():
                s[u.state] += 1
            s["total"] = len(self.units)
            s["done_width"] = sum(u.width for u in self.units.values()
                                  if u.state in ("done", "found"))
            s["total_width"] = sum(u.width for u in self.units.values())
            s["version"] = self._gen
            return s

    def progress(self):
        with self.lock:
            done = sum(1 for u in self.units.values() if u.state in ("done", "found"))
            return done, len(self.units)

    # ------------------------------------------------------------- mutation
    def claim(self, node_id, want, now=None, reaper_ms=None):
        """Give a node up to `want` free/stealable units.  Reaper returns
        `reaper_ms` for the *oldest stolen* unit (0 means nothing expired)."""
        now = now or self.now()
        reaper = 0
        with self.lock:
            out = []
            for u in self.units.values():
                if len(out) >= want:
                    break
                if u.state == "done" or u.state == "found":
                    continue
                if u.state == "claimed":
                    if u.lease_expiry and u.lease_expiry < now:
                        # --- work stealing by lease expiry ---
                        if u.claimant != node_id:
                            age = now - u.lease_expiry
                            reaper = max(reaper, age)
                        u.claimant = node_id
                        u.attempts += 1
                    else:
                        continue
                else:
                    if u.state == "dead":
                        continue
                    u.claimant = node_id
                    u.attempts += 1
                u.state = "claimed"
                u.lease_expiry = now + self.lease_ms
                out.append(u)
            if out:
                self._gen += 1
            return out, reaper

    def heartbeat(self, node_id, unit_ids, now=None):
        now = now or self.now()
        leases = {}
        with self.lock:
            for uid in unit_ids:
                u = self.units.get(uid)
                if u and u.state == "claimed" and u.claimant == node_id:
                    u.lease_expiry = now + self.lease_ms
                    leases[uid] = self.lease_ms
            self._gen += 1
            return leases

    def complete(self, uid, outcome, keys_checked=0):
        """outcome: exhausted | error | paused | found."""
        with self.lock:
            u = self.units.get(uid)
            if not u:
                return None
            u.keys_checked += int(keys_checked or 0)
            if outcome == "exhausted":
                u.state = "done"
                u.outcome = outcome
            elif outcome == "found":
                u.state = "found"
                u.outcome = outcome
            elif outcome == "error":
                u.attempts += 1
                if u.attempts >= 3:
                    u.state = "dead"
                    u.outcome = "error"
                else:
                    u.state = "free"
            else:  # paused / disconnected mid-run: back to free for stealing
                u.state = "free"
                u.claimant = None
                u.lease_expiry = None
            self._gen += 1
            return u


def build_units(puzzle, engine, slices):
    units = []
    for i, (lo_hex, hi_hex) in enumerate(slices):
        width = int(hi_hex, 16) - int(lo_hex, 16) + 1
        units.append(Unit("%d:%d" % (puzzle.n, i), puzzle.n, engine,
                          lo_hex, hi_hex, width))
    return units