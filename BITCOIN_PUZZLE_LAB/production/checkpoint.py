"""Checkpointing + resume ledger for the production pipeline.

State layout (all under production/state):

  ledger.json                the master JSON ledger of every share ever claimed
  scans/<puzzle>_<share>.kc  BitCrack --continue files (native, engine-owned)
  work/<puzzle>_<share>.work Kangaroo -w work files (native, engine-owned)
  logs/<puzzle>_<share>.log  stream capture
  found/<puzzle>.txt         verified keys (JSON lines)

Every process restart starts by reading ledger.json; shares marked finished
are never re-scanned; running shares are resumed from their native engine
checkpoint.
"""

import json
import os
import re
import time

STATE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "state")
LEDGER = os.path.join(STATE_DIR, "ledger.json")

SCAN_DIR = os.path.join(STATE_DIR, "scans")
WORK_DIR = os.path.join(STATE_DIR, "work")
LOG_DIR = os.path.join(STATE_DIR, "logs")
FOUND_DIR = os.path.join(STATE_DIR, "found")

for _d in (STATE_DIR, SCAN_DIR, WORK_DIR, LOG_DIR, FOUND_DIR):
    os.makedirs(_d, exist_ok=True)


class Checkpoint:
    def __init__(self, path=LEDGER):
        self.path = path
        self.data = self._load()

    def _load(self):
        if os.path.exists(self.path):
            with open(self.path, "r", encoding="utf-8") as fh:
                return json.load(fh)
        return {"version": 1, "shares": []}

    def _save(self):
        tmp = self.path + ".tmp"
        with open(tmp, "w", encoding="utf-8") as fh:
            json.dump(self.data, fh, indent=2)
        os.replace(tmp, self.path)

    # ---- record API ------------------------------------------------------

    def returns(self, key, n, share):
        key = "u:%s:%s:%s" % (key, n, share)
        for rec in self.data["shares"]:
            if rec.get("uid") == key:
                return rec
        return None

    def returns_all(self, n):
        return [r for r in self.data["shares"] if r.get("n") == n]

    def claim(self, n, share_idx, total_shares, start_hex, end_hex, engine,
              device=None):
        uid = "u:%s:%s:%s" % (engine, n, share_idx)
        rec = self.returns(engine, n, share_idx)
        if rec is not None:
            return rec
        rec = {
            "uid": uid,
            "engine": engine,
            "n": n,
            "share_idx": share_idx,
            "total_shares": total_shares,
            "start_hex": start_hex,
            "end_hex": end_hex,
            "device": device,
            "status": "claimed",
            "claimed_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "heartbeat": None,
            "engine_ckpt": None,
        }
        self.data["shares"].append(rec)
        self._save()
        return rec

    def touch(self, rec, status=None, engine_ckpt=None, note=None):
        for r in self.data["shares"]:
            if r.get("uid") == rec["uid"]:
                r["status"] = status or r.get("status")
                r["heartbeat"] = time.strftime(
                    "%Y-%m-%dT%H:%M:%SZ", time.gmtime())
                if engine_ckpt is not None:
                    r["engine_ckpt"] = engine_ckpt
                if note is not None:
                    r["note"] = note
                self._save()
                return r
        return rec

    def mark_found(self, rec, found_hex_path):
        r = self.touch(rec, status="found")
        r["found_file"] = found_hex_path
        self._save()

    # ---- scan state helpers ---------------------------------------------

    def running_shares(self):
        return [r for r in self.data["shares"]
                if r.get("status") in ("claimed", "running")]

    def unresolved(self):
        return [r for r in self.data["shares"]
                if r.get("status") not in ("found", "finished")]


# ---- native engine checkpoint parsing ------------------------------------

_HEX = re.compile(r"[0-9a-fA-F]{8,64}")

_STARTS = ("start", "start key", "range start", "0x")


def read_bitcrack_continue(path):
    """Parse a BitCrack --continue progress file (version-tolerant).

    Known format (semantics vary slightly across forks):
        Start key : 0x...
        End key   : 0x...
        Next key  : 0x...
        ... plus blocks/threads/points/compression as plain text ...
    Returns {} if the file cannot be understood (caller keeps scanning from
    the recorded start).
    """
    info = {}
    if not os.path.exists(path):
        return info
    with open(path, "r", encoding="utf-8", errors="replace") as fh:
        text = fh.read()
    lower = text.lower()
    for label, key in (("start", "start"), ("next", "next"), ("end", "end")):
        for line in lower.splitlines():
            if label + " key" in line or line.startswith(label):
                m = re.findall(r"0x[0-9a-fA-F]+", line)
                if m:
                    info[key] = m[0]
                else:
                    h = _HEX.search(line)
                    if h:
                        info[key] = h.group(0)
                break
    if "next" not in info and "start" in info:
        info["next"] = info["start"]
    return info


def read_kangaroo_work(path):
    """Read minimal metadata from a Kangaroo -w work file (binary-ish).

    We do not parse the binary DP table; we report size + mtime so the
    orchestrator knows the engine is alive and how much data it holds.
    """
    if not os.path.exists(path):
        return {}
    st = os.stat(path)
    return {"bytes": st.st_size,
            "mtime": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(st.st_mtime))}


# ---- progress rendering --------------------------------------------------

def render_progress(recs, puzzle_by_n):
    lines = []
    for r in sorted(recs, key=lambda r: (r.get("n"), r.get("share_idx"))):
        n = r.get("n")
        p = puzzle_by_n(n)
        lines.append(
            "#%-3d share %2d/%d  %-8s %s  engine=%s ckpt=%s"
            % (n, r.get("share_idx"), r.get("total_shares"),
               r.get("status"), r.get("device") or "-",
               r.get("engine"), r.get("engine_ckpt") or "-"))
    return "\n".join(lines)