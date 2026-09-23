#!/usr/bin/env python3
"""bench.py — orchestrate the synthetic benchmark and write results CSV.

Usage:
  python bench.py --db 12,16,20,24 --reps 3 --methods bsgs,rho,kanga,pir --out results/bench.csv
Control sets (smooth instances): --smooth --methods ph
Grover emulation is auto-limited to db<=12 by solvers.grover.

Row: db,rep,algorithm,steps,ms,ok,verified,note
"""
import argparse, csv, glob, json, os, sys
from gen import gen_prime_instances, gen_smooth_instances
from solvers import solve

METHODS = ["bsgs", "rho", "pir", "kanga", "grover"]

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", default="12,16,20,24")
    ap.add_argument("--reps", type=int, default=3)
    ap.add_argument("--seed", type=int, default=20260922)
    ap.add_argument("--methods", default=None, help=f"comma list, default all for type")
    ap.add_argument("--smooth", action="store_true")
    ap.add_argument("--kanga-w", type=int, default=32)
    ap.add_argument("--kanga-b", type=int, default=6)
    ap.add_argument("--pir-r", type=int, default=4)
    ap.add_argument("--out", default=None)
    args = ap.parse_args()
    dbs = [int(x) for x in args.db.split(",")]

    if args.smooth:
        rows = gen_smooth_instances(dbs, args.seed, args.reps)
        methods = args.methods.split(",") if args.methods else ["ph"]
        note = "smooth-order control"
    else:
        rows = gen_prime_instances(dbs, args.seed, args.reps)
        default = METHODS if args.methods is None else None
        methods = (args.methods or ",".join(default)).split(",")
        note = "prime-order synthetic"

    os.makedirs("results", exist_ok=True)
    out = args.out or f"results/bench_{'smooth' if args.smooth else 'prime'}.csv"
    with open(out, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["db", "rep", "algorithm", "steps", "ms", "ok", "verified", "note"])
        okc = 0
        for row in rows:
            for method in methods:
                if method == "grover" and row["db"] > 12:
                    continue    # solver asserts; skip
                kwargs = {"seed": args.seed + row["rep"]}
                if method == "kanga":
                    kwargs.update(W=args.kanga_w, b=args.kanga_b)
                if method == "pir":
                    kwargs.update(R=args.pir_r)
                res = solve(row, method, **kwargs)
                verified = 1 if res["ok"] else 0
                okc += verified
                w.writerow([row["db"], row["rep"], method, res["steps"], f"{res['ms']:.3f}",
                            int(res["ok"]), verified, note])
                print(f"db={row['db']:3d} {method:8s} steps={res['steps']:>12,} ok={int(res['ok'])} "
                      f"({res['ms']:.1f} ms)")
                f.flush()
    print(f"wrote {out}: {len(rows)*len(methods)} rows, verified={okc}")

if __name__ == "__main__":
    main()