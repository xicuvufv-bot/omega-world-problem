import csv, sys
res = {}
for name in ["O2","O3","Ofast","native"]:
    for line in open(f"MICROBENCH_{name}.csv"):
        line = line.strip()
        if not line or line.startswith("#"): continue
        kind, strat, op, ns = line.split(",")
        res[(kind, strat, op)] = {**res.get((kind, strat, op), {}), name: float(ns)}

cols = ["O2","O3","Ofast","native"]
with open("MICROBENCHMARKS.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["kind","strategy","op"] + cols + ["best","best_flag"])
    for key in sorted(res):
        row = [key[0], key[1], key[2]]
        vals = [res[key].get(c) for c in cols]
        vals = ["" if v is None else f"{v:.3f}" for v in vals]
        num = [res[key][c] for c in cols if c in res[key]]
        best = min(num)
        bestf = min(cols, key=lambda c: res[key][c])
        w.writerow(row + vals + [f"{best:.3f}", bestf])

# per-strategy geometric-mean mul+jacobian speedup vs naive
import math
print("== strategy speedup over naive (geomean of mul + jacobian_dbl, native flags) ==")
strat = {}
for key, v in res.items():
    if key[1] not in strat: strat[key[1]] = []
    if key[2] in ("mul","jacobian_dbl"):
        strat[key[1]].append(v["native"])
naive_mul = strat["naive"][0]
naive_jac = strat["naive"][1]
print(f"{'strategy':9s} {'mul%':>8s} {'dbl%':>8s}")
for s, v in strat.items():
    print(f"{s:9s} {v[0]/naive_mul*100-100:8.1f} {v[1]/naive_jac*100-100:8.1f}")
print("MICROBENCHMARKS.csv written")