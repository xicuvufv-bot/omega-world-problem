"""Generate dataset/puzzles_meta.csv from dataset/raw_tracker.txt.

Adds per-puzzle derived fields: regime, exposed-pubkey flag, work estimates,
single-GPU-year estimates (4090-scale), an honest difficulty tier, a
recommended method, and an unsolved attack-order rank sorted ascending by
estimated single-GPU work for the puzzle's regime.
"""

import csv
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from algorithms.interval import parse_tracker, classify, bounds, RAW_TRACKER
from algorithms.metrics import (
    interval_work_hashes, interval_work_ops, years_for_work,
    GPU_HASH_PER_SEC, GPU_GROUP_PER_SEC, tier, format_ops,
)

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "puzzles_meta.csv")
COLUMNS = [
    "n", "lo", "hi", "lo_hex", "hi_hex", "address", "solved", "regime",
    "exposed_pubkey", "hashes_r1", "ops_r2", "years_r1", "years_r2", "tier",
    "method", "rank",
]

METHOD = {
    "SOLVED": "n/a - public key released",
    "R1": "hash scan (SHA256+RIPEMD160 compare)",
    "R2": "interval DLP: Pollard kangaroo / BSGS on exposed pubkey",
}


def main():
    rows = parse_tracker(RAW_TRACKER)
    stats = classify(rows)

    unsolved = []
    for r in rows:
        if r.regime == "SOLVED":
            years = 0.0
            yrs_r1, yrs_r2 = 0.0, 0.0
        elif r.regime == "R1":
            yrs_r1 = years_for_work(interval_work_hashes(r.n), GPU_HASH_PER_SEC)
            yrs_r2 = 0.0
            years = yrs_r1
        else:  # R2
            yrs_r1 = 0.0
            yrs_r2 = years_for_work(interval_work_ops(r.n), GPU_GROUP_PER_SEC)
            years = yrs_r2
        if r.regime != "SOLVED":
            unsolved.append((years, r))

    # ascending work => practical attack order; stable by n for ties
    unsolved.sort(key=lambda pair: (pair[0], pair[1].n))
    rank_of = {r.n: i + 1 for i, (_, r) in enumerate(unsolved)}

    with open(OUT, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(COLUMNS)
        for r in rows:
            if r.regime == "SOLVED":
                yrs_r1, yrs_r2 = 0.0, 0.0
                t = "SOLVED"
            elif r.regime == "R1":
                yrs_r1 = years_for_work(interval_work_hashes(r.n), GPU_HASH_PER_SEC)
                yrs_r2 = 0.0
                t = tier(yrs_r1)
            else:
                yrs_r1 = 0.0
                yrs_r2 = years_for_work(interval_work_ops(r.n), GPU_GROUP_PER_SEC)
                t = tier(yrs_r2)
            w.writerow([
                r.n,
                r.lo,
                r.hi,
                f"{r.lo:x}",
                f"{r.hi:x}",
                r.address,
                1 if r.solved else 0,
                r.regime,
                1 if r.exposed_pubkey else 0,
                format_ops(r.n - 1) if r.regime == "R1" else "",
                format_ops((r.n + 1) // 2 + 1) if r.regime == "R2" else "",
                f"{yrs_r1:.3g}" if r.regime == "R1" else "",
                f"{yrs_r2:.3g}" if r.regime == "R2" else "",
                t,
                METHOD[r.regime],
                "" if r.solved else rank_of[r.n],
            ])

    top = [(y, r.n, r.regime) for y, r in unsolved[:6]]
    print(f"wrote {OUT}")
    print(f"counts: {stats}")
    print("top attack-order (single-GPU estimator):")
    for y, n, regime in top:
        print(f"  puzzle #{n} ({regime})  {y:.3g} GPU-years")


if __name__ == "__main__":
    main()