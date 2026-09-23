#!/usr/bin/env python3
"""autotune.py — auto-tune kanga (W,b,K,wcc) across dbs on FIXED-l curve (L2 lane).

Goal: find parameter families that minimize med-steps/√N (a CONSTANT for the √N class).
An honest autotune must show: no parameter mapping turns the slope sub-sqrt; every
(cfg, db) stays ~c·√N with c≥1. Output: lab/AUTOTUNE_RESULTS.csv + fit summary.
"""
import io, os, sys, time, math, random, csv, statistics
sys.stdout.reconfigure(encoding="utf-8"); sys.stderr.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path[:0] = [HERE]
import gen, solvers

CFGS = [
    ("default",  dict(W=32, b=6,  K=32, wcc=6.0)),
    ("dp-shallow", dict(W=32, b=4,  K=32, wcc=6.0)),
    ("dp-lite",  dict(W=48, b=6,  K=32, wcc=5.0)),
    ("many-w",   dict(W=64, b=8,  K=64, wcc=6.0)),
    ("wide-jump",dict(W=32, b=6,  K=128, wcc=6.0)),
    ("shortcap", dict(W=32, b=8,  K=64, wcc=3.0)),
]

def main():
    lab = os.path.join(HERE, "lab"); os.makedirs(lab, exist_ok=True)
    p, l, G = gen.TOY_P, gen.TOY_L, gen.TOY_G
    rows = []
    dbs = [16, 18, 20, 22, 24]
    seeds = [20260922, 20260923, 20260924]
    t_all = time.perf_counter()
    with io.open(os.path.join(lab, "AUTOTUNE_RESULTS.csv"), "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["db","cfg","seed","kanga_steps","bsgs_steps","ratio_k_b","ok"])
        for db in dbs:
            N = 1 << db
            row = {"db": db, "p": p, "l": l, "Gx": G[0], "Gy": G[1]}
            for cfg_name, kw in CFGS:
                for s in seeds:
                    row = dict(row)
                    rnd = random.Random(s)
                    k = rnd.randrange(1, N)
                    Q = gen.mul(k, G, p)
                    row.update({"Qx": Q[0], "Qy": Q[1], "k": k})
                    rk = solvers.kanga(row, N, s, **kw)
                    rb = solvers.bsgs(row, N, s)
                    ratio = (rk["steps"]/rb["steps"]) if rb["steps"] else None
                    w.writerow([db, cfg_name, s, rk["steps"], rb["steps"], "%.3f" % ratio if ratio else "NA", int(rk["ok"])])
                    f.flush()
                    print("db=%2d %-10s seed=%d kanga=%8d ok=%d bsgs=%6d ratio=%.2f  (%.1fs)"
                          % (db, cfg_name, s, rk["steps"], int(rk["ok"]), rb["steps"],
                             ratio if ratio else 0, time.perf_counter()-t_all), flush=True)
    print("WROTE lab/AUTOTUNE_RESULTS.csv  total=%.1fs" % (time.perf_counter()-t_all))

if __name__ == "__main__":
    main()