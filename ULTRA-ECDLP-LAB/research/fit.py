#!/usr/bin/env python3
"""fit.py — log-log scaling fit and A/B/C/D classification for the benchmark CSV.

CSV columns: db,algorithm,steps,ms,ok,verified
Per (algorithm) we fit   log2(steps) ~ a + b*log2(N)   by least squares (N=2^db).
b = empirical exponent α. Given the *wide* per-instance variance of collision methods,
we fit on the geometric mean of steps per db (log-space midpoint) AND report the per-db
spread band (min-max in log2). Classification per spec:
  A: α in [0.45, 0.55] and close to the √N theoretical line (steps/√N ~ O(1) constant)
  B: α in (0.55, 0.67)   C: α in [0.67, 0.95)   D: α >= 0.95
'emulation'/'control' rows (grover_emu, ph) may be flagged instead of classified.
Also prints step-per-√N ratio at each db (how far above/below the generic line).
"""
import argparse, csv, math, sys
from collections import defaultdict

def load(path):
    rows = []
    with open(path) as f:
        rd = csv.DictReader(f)
        for r in rd:
            rows.append(r)
    return rows

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("csv", help="benchmark results csv")
    ap.add_argument("--dbmin", type=int, default=None)
    args = ap.parse_args()
    rows = load(args.csv)
    rows = [r for r in rows if r.get("verified") == "1" and r.get("ok") == "1"]

    by_alg = defaultdict(lambda: defaultdict(list))   # alg -> db -> steps
    for r in rows:
        db = int(r["db"]); alg = r["algorithm"]
        by_alg[alg][db].append(float(r["steps"]))

    print(f"analyzing {len(rows)} verified rows")
    for alg in sorted(by_alg):
        dbs = sorted(by_alg[alg])
        fit = []
        for db in dbs:
            vals = by_alg[alg][db]
            gm = math.exp(sum(math.log(v) for v in vals) / len(vals))
            fit.append((db, gm, min(vals), max(vals)))
        if len(fit) >= 2:
            dbs_p = [(db, gm) for db, gm, _, _ in fit]
            if args.dbmin is not None:
                dbs_p = [p for p in dbs_p if p[0] >= args.dbmin]
            x = [p[0] for p in dbs_p]; y = [math.log2(p[1]) for p in dbs_p]
            n = len(x)
            mx = sum(x) / n; my = sum(y) / n
            num = sum((x[i] - mx) * (y[i] - my) for i in range(n))
            den = sum((x[i] - mx) ** 2 for i in range(n))
            alpha = num / den
            b0 = my - alpha * mx
            # R^2
            ss_tot = sum((y[i] - my) ** 2 for i in range(n))
            ss_res = sum((y[i] - (alpha * x[i] + b0)) ** 2 for i in range(n))
            r2 = 1 - ss_res / ss_tot if ss_tot else 0
            # per-db ratio steps/sqrt(N) = steps / 2^(db/2)
            ratios = [("2^%d" % db, gm / (2 ** (db / 2))) for db, gm, _, _ in fit]
            # classify
            tag = ""
            if alg in ("grover_emu",): tag = "  [EMULATION NO CLAIM]"
            if alg in ("ph",): tag = "  [CONTROL: smooth-order]"
            cls = ""
            if not tag:
                if alpha >= 0.95: cls = "D"
                elif alpha >= 0.67: cls = "C"
                elif alpha > 0.55: cls = "B"
                else: cls = "A"
                if alpha < 0.30:
                    # essentially flat in N: solver is not exploiting the interval at all.
                    # This LOOKS like super-linear gains but is interval-blindness (rt() fixed
                    # at ~sqrt(l)); label X + flag in the summary.
                    cls = "X(flat)"
                if cls == "A":
                    for db, steps, _, _ in fit:
                        if steps / (2 ** (db / 2)) > 8:
                            cls = "B*"
                            break
            print(f"{alg:10s} α={alpha:.3f}  const 2^{b0:.2f}  R²={r2:.3f}  n={n}  class={cls or '--'}{tag}")
            for db, steps, mn, mx in fit:
                band = f" [min={mn/2**(db/2):.2f}√N, max={mx/2**(db/2):.2f}√N]" if len(by_alg[alg][db]) > 1 else ""
                print(f"   2^{db:2d}: gm={steps:>12,.0f} steps  {steps/2**(db/2):6.2f} √N{band}")
            if cls == "X(flat)":
                print(f"   X(flat): {alg} is interval-blind - working constant is the full-group order l; α=[0,0.3] only because N was varied, not ⟨l⟩.")

if __name__ == "__main__":
    main()