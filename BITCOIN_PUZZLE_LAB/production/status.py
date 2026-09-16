"""Puzzle-status verification.

Refresh pipeline:
  1) pull the canonical community tracker from GitHub
     (roadhero/Bitcoin-Puzzle-Info, file BTC-Solved-Unsolved.txt);
  2) diff every row against this lab's frozen registry so any *silent*
     status change (a puzzle that was unlocable yesterday and got solved
     overnight, or a tracker tamper) is surfaced instead of silently
     re-targeted;
  3) optionally cross-check the on-chain balance of the target address via
     mempool.space (public REST, no key) so we confirm the prize is still
     sitting there before spending GPU time;
  4) write state/status.json + state/status.md.

No write access to the tracker; this is read + diff only.
"""

import json
import os
import time
import urllib.request

from . import registry

TRACKER_URL = ("https://raw.githubusercontent.com/roadhero/"
               "Bitcoin-Puzzle-Info/master/BTC-Solved-Unsolved.txt")
MEMPOOL_API = "https://mempool.space/api/address/"

STATUS_JSON = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                           "state", "status.json")
STATUS_MD = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                         "state", "status.md")


def _fetch(url, timeout=20):
    req = urllib.request.Request(url, headers={"User-Agent": "puzzle-pipeline/1.0"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read().decode("utf-8", errors="replace")


def parse_tracker_text(text):
    """Reuse the lab parser semantics: | lo:hi | address | status | pub | priv |"""
    rows = []
    for line in text.splitlines():
        line = line.strip()
        if not line.startswith("|"):
            continue
        parts = [c.strip() for c in line.split("|")]
        if len(parts) < 6:
            continue
        lo_s, hi_s = parts[1].split(":")
        lo = int(lo_s, 16)
        n = lo.bit_length()
        rows.append({
            "n": n,
            "lo_hex": lo_s,
            "hi_hex": hi_s,
            "address": parts[2],
            "status": "SOLVED" if parts[3] == "SOLVED" else "UNSOLVED",
            "pub": parts[4],
        })
    return rows


def fetch_live_tracker():
    """Return list-of-dict rows from the live tracker; raise on failure."""
    return parse_tracker_text(_fetch(TRACKER_URL))


def diff(live_rows):
    """Compare live tracker vs frozen registry. Return list of diffs."""
    out = []
    live = {r["address"]: r for r in live_rows}
    for p in registry.all_rows():
        lr = live.get(p.address)
        if lr is None:
            out.append({"address": p.address, "n": p.n, "kind": "missing_live"})
            continue
        live_solved = lr["status"] == "SOLVED"
        if live_solved != p.solved:
            out.append({"address": p.address, "n": p.n, "kind": "changed",
                        "was_solved": p.solved, "now_solved": live_solved})
    return out


def balance_sats(address, timeout=15):
    """Best-effort on-chain balance via mempool.space. Raises on failure."""
    data = _fetch(MEMPOOL_API + address, timeout=timeout)
    j = json.loads(data)
    return (j["chain_stats"].get("funded_txo_sum", 0)
            - j["chain_stats"].get("spent_txo_sum", 0))


def refresh(chain_check=False, timeout=20):
    """Run the full verification. Returns a summary dict."""
    attempts = {}
    errors = []
    live = None
    try:
        live = fetch_live_tracker()
        attempts["tracker"] = "ok"
    except Exception as e:  # noqa: BLE001 - surfaced in report
        errors.append("tracker: %s" % e)
        attempts["tracker"] = "offline"

    diffs = diff(live) if live else []

    chain = {}
    if chain_check:
        # check the two cheapest realistic targets only (do not hammer API)
        for n in (71, 140):
            p = registry.get_by_number(n)
            try:
                chain[n] = {"address": p.address, "sats": balance_sats(p.address)}
                attempts["chain:%d" % n] = "ok"
            except Exception as e:  # noqa: BLE001
                errors.append("chain:%d: %s" % (n, e))
                attempts["chain:%d" % n] = "offline"

    report = {
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "attempts": attempts,
        "errors": errors,
        "registry": registry.summary(),
        "live": None if live is None else {
            "rows": len(live),
            "solved": sum(1 for r in live if r["status"] == "SOLVED"),
            "unsolved": sum(1 for r in live if r["status"] != "SOLVED"),
        },
        "diffs": diffs,
        "chain_spot": chain,
        "lowest_unsolved": {
            "n": 71, "address": registry.get_by_number(71).address,
            "still_unsolved": not registry.get_by_number(71).solved,
        },
    }

    with open(STATUS_JSON, "w", encoding="utf-8") as fh:
        json.dump(report, fh, indent=2)
    with open(STATUS_MD, "w", encoding="utf-8") as fh:
        fh.write(render_md(report))
    return report


def render_md(report):
    L = []
    L.append("# Puzzle status verification")
    L.append("")
    L.append("Cycle: %s" % report["generated_at"])
    L.append("")
    for k, v in report["attempts"].items():
        L.append("- %s: %s" % (k, v))
    L.append("")
    L.append("Registry: %(total)d total / %(solved)d solved / "
             "%(unsolved)d unsolved (R1=%(r1)d R2=%(r2)d)"
             % report["registry"])
    if report.get("live"):
        L.append("Live tracker: %(rows)d rows / %(solved)d solved / "
                 "%(unsolved)d unsolved" % report["live"])
    L.append("")
    if report["diffs"]:
        L.append("## Diffs vs frozen registry (ACTION BEFORE SCANNING)")
        for d in report["diffs"]:
            L.append("- %s" % json.dumps(d))
    else:
        L.append("No diffs vs frozen registry: status unchanged from the "
                 "published tracker.")
    L.append("")
    if report["chain_spot"]:
        L.append("## On-chain spot check (sats)")
        for n, c in sorted(report["chain_spot"].items()):
            L.append("- #%d %s : %d sat" % (n, c["address"], c["sats"]))
        L.append("")
    for e in report["errors"]:
        L.append("WARN: %s" % e)
    return "\n".join(L) + "\n"