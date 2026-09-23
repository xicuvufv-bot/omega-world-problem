# -*- coding: utf-8 -*-
# kaggle_t4.py — Kaggle notebook payload (T4 GPU, NVIDIA).
# Ports the research solver suite to cupy for the allowed GPU tier. Run cells 1-4 as a
# Kaggle notebook. Everything synthetic (safe), verified rows only.
#
# Cell 1: install + imports. Cell 2: build synthetic toy instances (prime-order EC).
# Cell 3: GPU VOW kangaroo (mirrors src/vow_engine.hpp + research/solvers.kanga).
# Cell 4: scale sweep db = 24..40 with the C++-rule b = clamp(best-of-{4,6}, db) -> CSV + fit.
import sys

# ---------------------------------------------------------------- cell 1
if "cell1" in sys.argv or True:
    import json, math, random, time, os
    import numpy as np
    try:
        import cupy as cp
        HAVE_GPU = True
    except Exception as e:
        HAVE_GPU = False
        print("NO GPU:", e)
        cp = None
    print("cupy:", cp.__version__ if HAVE_GPU else None,
          "gpu:", cp.cuda.runtime.getDeviceProperties(0)["name"].decode() if HAVE_GPU else None,
          flush=True)

# ---------------------------------------------------------------- cell 2 (same safe toy group as research/gen.py)
P  = 4294966177      # 2^32 - 1119, ordinary curve y^2 = x^3 + 7
L  = 4294835173      # prime order (verified)
GX, GY = 1960037684, 560815139

def modinv(a, m): return pow(a, -1, m)
def add(P, Q, p):
    if P is None: return Q
    if Q is None: return P
    x1, y1 = P; x2, y2 = Q
    if x1 == x2:
        if (y1 + y2) % p == 0: return None
        la = 3 * x1 * x1 % p * modinv(2 * y1, p) % p
    else:
        la = (y2 - y1) % p * modinv((x2 - x1) % p, p) % p
    x3 = (la * la - x1 - x2) % p; y3 = (la * (x1 - x3) - y1) % p
    return (x3, y3)
def smul(k, Pt, p):
    R = None; Q = Pt
    while k:
        if k & 1: R = add(R, Q, p)
        Q = add(Q, Q, p); k >>= 1
    return R

def gen_instances(dbs, seed, reps):
    rng = random.Random(seed)
    rows = []
    for db in dbs:
        for r in range(reps):
            k = rng.randrange(1, 1 << db)
            Q = smul(k, (GX, GY), P)
            rows.append(dict(db=db, rep=r, typ="prime", p=P, l=L,
                             Gx=GX, Gy=GY, Qx=Q[0], Qy=Q[1], k=k))
    return rows

# ---------------------------------------------------------------- cell 3: GPU VOW kangaroo (cupy)
def gpu_kanga(row, W, b, K=32, wcc=6.0, seed=7, budget_mult=24):
    """Same walk as solvers.kanga but data-parallel: one cupy array row per walker,
    batched Jacobian mixed-add, per-walker distance; DP detection on GPU; candidate
    extraction on host. Returns (steps, ok, ms)."""
    p, l = P, L
    Gx, Gy, Qx, Qy = row["Gx"], row["Gy"], row["Qx"], row["Qy"]
    N = 1 << row["db"]
    rng = np.random.default_rng(seed)
    sl = math.isqrt(N)
    jd = rng.integers(1, max(2, 2 * sl), size=K, dtype=np.uint64)
    JX = np.zeros((K, 2), dtype=np.uint64)
    for i in range(K):
        g_ = smul(int(jd[i]), (GX, GY), p)
        JX[i] = (g_[0], g_[1])
    JXc = cp.asarray(JX)
    off = rng.integers(1, N, size=W, dtype=np.uint64)
    # alternate tame (a*G) / wild (Q + u*G)
    tempt = np.empty((W, 2), dtype=np.uint64)
    for i in range(W):
        if i & 1:
            pu = smul(int(off[i]), (GX, GY), p)
            P2 = add((Qx, Qy), pu, p)
            tempt[i] = (P2[0], P2[1])
        else:
            pa = smul(int(off[i]), (GX, GY), p)
            tempt[i] = (pa[0], pa[1])
    X = cp.asarray(tempt)
    dist = cp.asarray((off % l).astype(np.uint64))
    owner = np.array([1 if i & 1 else 0 for i in range(W)], dtype=np.uint8)
    DPMASK = (1 << b) - 1
    MOD = cp.uint64(p)

    def step(X3, sel):
        # sel already computed from PRE-add x: jump JXc[sel], dist += jd[sel]
        B = JXc[sel]
        z = X3[:, 2]
        bx, by = B[:, 0], B[:, 1]
        Z1Z1 = (z * z) % MOD
        U2 = (bx * Z1Z1) % MOD
        S2 = (by * (Z1Z1 * z % MOD)) % MOD
        Xx, Yy = X3[:, 0], X3[:, 1]
        H = (U2 + MOD - Xx) % MOD
        R = (S2 + MOD - Yy) % MOD
        HH = (H * H) % MOD
        HHH = (H * HH) % MOD
        V = (Xx * HH) % MOD
        X3n = (R * R + MOD - HHH + MOD - 2 * V) % MOD
        Y3n = (R * (V + MOD - X3n) + MOD - Yy * HHH % MOD) % MOD
        Z3n = (z * H) % MOD
        return cp.column_stack((X3n, Y3n, Z3n % MOD))

    JDC = cp.asarray(jd)
    X3 = cp.column_stack((X[:, 0], X[:, 1], cp.ones(W, dtype=cp.uint64)))
    walkcap = int(wcc * sl) + 64
    budget = W * budget_mult * sl + 65536
    steps = 0
    tab = {}
    t0 = time.perf_counter()
    solved = None
    while steps < budget:
        sel = ((X3[:, 0] >> 8) & np.uint64(K - 1)).astype(np.int64)
        X3 = step(X3, sel)
        dist = (dist + JDC[sel]) % l
        steps += W
        dp = ((X3[:, 0] & np.uint64(DPMASK)) == 0)
        n_dp = int(cp.count_nonzero(dp))
        if n_dp:
            idx = np.nonzero(cp.asnumpy(dp))[0]
            for ix in idx:
                px, py = int(X3[ix, 0].item()), int(X3[ix, 1].item())
                # inverse to affine
                try:
                    zi = modinv(int(X3[ix, 2].item()), p)
                except ValueError:
                    continue
                ax = px * zi % p * zi % p
                ay = py * zi % p * zi % p * zi % p
                own = owner[ix]
                dd = int(dist[ix].item())
                key = (ax, ay)
                ent = tab.get(key)
                if ent is None:
                    tab[key] = (own, dd)
                elif ent[0] != own:
                    td = dd if own == 0 else ent[1]
                    wd = ent[1] if own == 0 else dd
                    cand = (td + l - wd) % l
                    got = smul(cand, (GX, GY), p)
                    if got == (Qx, Qy):
                        solved = cand
                        break
        if solved is not None:
            break
        # restart DP walkers (fresh offsets)
        if dp.any():
            r = rng.integers(1, N, size=W, dtype=np.uint64)
            for ix in (np.nonzero(cp.asnumpy(dp))[0]):
                if solved is not None: break
                if ix & 1:
                    pu = smul(int(r[ix]), (GX, GY), p)
                    Ru = add((Qx, Qy), pu, p)
                    X3[ix, 0], X3[ix, 1], X3[ix, 2] = Ru[0], Ru[1], 1
                else:
                    pa = smul(int(r[ix]), (GX, GY), p)
                    X3[ix, 0], X3[ix, 1], X3[ix, 2] = pa[0], pa[1], 1
                dist[ix] = r[ix] % l
    ms = (time.perf_counter() - t0) * 1e3
    return steps, solved is not None, ms

# ---------------------------------------------------------------- cell 4: sweep + csv
def main():
    import csv
    dbs = [24, 28, 32, 36, 40] if HAVE_GPU else [24, 28]
    rows = gen_instances(dbs, 20260922, 1)
    os.makedirs("results", exist_ok=True)
    with open("results/bench_t4.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["db", "rep", "algorithm", "steps", "ms", "ok", "verified", "note"])
        for row in rows:
            W, b = 1 << 10, 6      # GPU walker count; b from local tuner (b=6 mid-range ok here)
            if row["db"] >= 36: b = 8
            steps, ok, ms = gpu_kanga(row, W=W, b=b)
            print(f"db={row['db']:3d} gpu_kanga steps={steps:>14,} ok={int(ok)} {ms:8.1f} ms", flush=True)
            w.writerow([row["db"], row["rep"], "kanga", steps, f"{ms:.3f}", int(ok), int(ok), "T4 cupy"])
            f.flush()
    print("done")

if __name__ == "__main__":
    main()