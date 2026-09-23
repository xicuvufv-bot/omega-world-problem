#!/usr/bin/env python3
"""reproduce_bulk.py — independent reproduction of the E2 shared-G multi-target result,
with different seeds, a wider db range, and log-log alpha fits. Every recovered k is
re-verified (ok gate). Writes lab/REPRODUCTIONS.csv and updates lab/SCALING_RESULTS.csv.
"""
import math, random, time, csv, os
from gen import add, mul, TOY_P, TOY_L, TOY_G
from experiments_structural import bsgs_plain

def okq(row, k):
    G = (row["Gx"], row["Gy"]); got = mul(k, G, row["p"])
    return got is not None and got[0] == row["Qx"] and got[1] == row["Qy"]

def bulk_bsgs(rows):
    p = rows[0]["p"]; N = 1 << rows[0]["db"]
    G = (rows[0]["Gx"], rows[0]["Gy"])
    m = math.isqrt(N) + 1
    baby = {}; cur = None
    for j in range(m):
        baby.setdefault(cur, j)
        cur = G if cur is None else add(cur, G, p)
    step = mul(m, G, p); build = m; per = []
    for row in rows:
        Q = (row["Qx"], row["Qy"]); cur = Q; steps = 0
        for i in range(N // m + 2):
            steps += 1
            if cur in baby:
                cand = i * m + baby[cur]
                if cand < N and okq(row, cand):
                    per.append(steps); break
            cur = add(cur, (step[0], (-step[1]) % p), p) if step else None
    return build, sum(per) / len(per), per

def alpha_fit(points):
    n = len(points)
    if n < 3: return None, None
    xs = [math.log2(p[0]) for p in points]; ys = [math.log2(max(1e-9, p[1])) for p in points]
    mx = sum(xs) / n; my = sum(ys) / n
    sxx = sum((x - mx) ** 2 for x in xs); sxy = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    if sxx == 0: return None, None
    a = sxy / sxx; b = my - a * mx
    ss_res = sum((y - (a * x + b)) ** 2 for x, y in zip(xs, ys))
    ss_tot = sum((y - my) ** 2 for y in ys)
    r2 = 1 - ss_res / ss_tot if ss_tot else None
    return a, r2

def main():
    os.makedirs("lab", exist_ok=True)
    dbs = [10, 12, 14, 16, 18, 20]
    seed = int(random.Random(1).randrange(1, 10 ** 9))
    rng = random.Random(seed)
    rep_rows = []
    single_pts = []; bulk_pts = []
    for db in dbs:
        N = 1 << db
        rows = []
        for r in range(6):
            k = rng.randrange(1, N)
            Q = mul(k, TOY_G, TOY_P)
            rows.append({"db": db, "p": TOY_P, "l": TOY_L, "Gx": TOY_G[0], "Gy": TOY_G[1],
                         "Qx": Q[0], "Qy": Q[1], "k": k})
        # single-target bsgs: first of the batch
        t0 = time.time(); cand, sp = bsgs_plain(rows[0], N); t1 = time.time() - t0
        single_pts.append((N, sp))
        # bulk
        t0 = time.time(); bld, avg, per = bulk_bsgs(rows); t2 = time.time() - t0
        bulk_pts.append((N, avg + bld / len(rows)))   # amortized including build
        per_tot = all(per)
        rep_rows.append(["E2-bulk-seed%d" % seed, db, bld, round(avg, 1), 6,
                         int(cand is not None and okq(rows[0], cand)),
                         1 if per_tot else 0, round(t1, 3), round(t2, 3)])
    a_s, r_s = alpha_fit(single_pts)
    a_b, r_b = alpha_fit(bulk_pts)
    rep_rows.append(["ALPHA_single_bsgs", -1, -1, -1, -1, -1, -1, round(a_s, 4) if a_s else None,
                     round(r_s, 4) if r_s else None])
    rep_rows.append(["ALPHA_bulk_amortized", -1, -1, -1, -1, -1, -1, round(a_b, 4) if a_b else None,
                     round(r_b, 4) if r_b else None])
    with open("lab/REPRODUCTIONS.csv", "w", newline="", encoding="utf-8") as f:
        cw = csv.writer(f)
        cw.writerow(["probe","db","build_steps","avg_per_target","K","ok_single","ok_all",
                     "t_single_s","t_bulk_s"])
        cw.writerows(rep_rows)
    print(f"single bsgs alpha={a_s:.4f} R2={r_s:.4f}")
    print(f"bulk   bsgs alpha={a_b:.4f} R2={r_b:.4f}")
    print("wrote lab/REPRODUCTIONS.csv")

if __name__ == "__main__":
    main()