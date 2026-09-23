#!/usr/bin/env python3
"""pn1_multitarget_rho.py — OPEN probe PN-1.

Test the Oorschot-Wiener shared-DP multi-target prediction: with K target instances
sharing the SAME base G, a single DP walker population with one shared DP table finds
ANY of the K keys in ~ sqrt(N/K) steps (first-hit distribution). If first-hit steps do
NOT shrink ~1/sqrt(K), the mechanism is REFUTED in this implementation.

Design (honest, synthetic-only, toy curve):
  - Fixed curve y^2=x^3+7, p=4294966177, l=4294835173 prime, base G verified.
  - K targets Q_i = k_i G, k_i uniform in [1,N), N=2^db, db in {16,18,20,22,24}.
  - 2W walkers: W tame (aG, dist a) and W wild (Q_i + uG, dist u) — wilds assigned round-
    robin across the K targets. One shared DP table (x, owner) records FIRST arrival;
    a tame/wild collision of DIFFERENT owners yields a solution for the wild's target.
  - Steps counted as group ops (walker steps), first-hit time recorded.
  - Gold check: every solved k re-verified via mul(k,G)==Q (the ok gate).
  - We measure E[first-hit steps] over reps for K=1,2,4,8,16 and fit log2(steps) vs
    log2(K) to see the slope (predicted ~ -0.5 if sqrt(N/K), 0 if no benefit).
"""
import io, os, sys, time, math, random, csv

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path[:0] = [HERE]
from gen import add, mul, TOY_P, TOY_L, TOY_G

def jac_from_aff(x, y, p): return (x % p, y % p, 1)
def jac_add_aff(a, bx, by, p):
    X, Y, Z = a
    Z1Z1 = Z*Z % p
    U2 = bx % p * Z1Z1 % p
    S2 = by % p * (Z1Z1*Z % p) % p
    H = (U2 - X) % p; R = (S2 - Y) % p
    HH = H*H % p; HHH = H*HH % p; V = X*HH % p
    return ((R*R - HHH - 2*V) % p, (R*(V - (R*R - HHH - 2*V) % p) - Y*HHH) % p, Z*H % p)
def jac_to_aff(a, p):
    X, Y, Z = a
    zi = pow(Z, -1, p)
    return (X*zi % p * zi % p, Y*zi % p * zi % p * zi % p)

def first_hit(db, K, W=8, b=8, Kt=16, wcc=6.0, seed=20260931, reps=1):
    """return (first_hit_steps, solved, verified) for one config."""
    N = 1 << db
    p, l, G = TOY_P, TOY_L, TOY_G
    rng = random.Random(seed)
    sl = math.isqrt(N)
    dpmask = (1 << b) - 1
    tab = {}
    # jump table
    jd = [1 + rng.randrange(max(1, 2*sl)) for _ in range(Kt)]
    jumps = [mul(d, G, p) for d in jd]
    # targets
    ks = [rng.randrange(1, N) for _ in range(K)]
    Qs = [mul(k, G, p) for k in ks]
    # walkers: index i -> (tame if i&1==0 else wild), wild carries target t = (i//2)%K
    walkers = []
    for i in range(2 * W):
        own = 0 if (i & 1) == 0 else 1
        t = None if own == 0 else (i // 2) % K
        if own == 0:
            a = rng.randrange(1, N); X = mul(a, G, p); d = a % l
        else:
            u = rng.randrange(1, N); X = add(Qs[t], mul(u, G, p), p); d = u % l
        walkers.append([jac_from_aff(*X, p), d, own, t, 0])
    steps = 0
    mi = 0
    budget = W * Kt * int(24 * sl) + 65536
    solved = None
    t0 = time.perf_counter()
    while steps < budget and solved is None:
        w = walkers[mi]; mi = (mi + 1) % len(walkers)
        X, d, own, t, cnt = w
        if cnt >= int(wcc * sl) + 64:
            if own == 0:
                a = rng.randrange(1, N); X = mul(a, G, p); d = a % l
            else:
                u = rng.randrange(1, N); X = add(Qs[t], mul(u, G, p), p); d = u % l
            w[0], w[1], w[4] = jac_from_aff(*X, p), d, 0
            continue
        sel = (X[0] >> 8) & (Kt - 1)
        bx, by = jumps[sel]
        X = jac_add_aff(X, bx, by, p)
        d = (d + jd[sel]) % l
        cnt += 1; steps += 1
        w[0], w[1], w[4] = X, d, cnt
        if (X[0] & dpmask) == 0:
            ax, ay = jac_to_aff(X, p)
            key = (ax, ay)
            ent = tab.get(key)
            if ent is None:
                tab[key] = (own, d, t)
                # restart after a DP? keep walking (standard: heavy walkers store, light continue)
                continue
            eo, ed, et = ent
            if eo != own:
                # collision between tame and wild
                if own == 0:
                    td, wd = d, ed; wt = et
                else:
                    td, wd = ed, d; wt = t
                cand = (td + l - wd) % l
                if cand < N and cand >= 1:
                    got = mul(cand, G, p)
                    if got == Qs[wt]:
                        solved = cand
                        break
    ms = (time.perf_counter() - t0) * 1e3
    ok = solved is not None
    return steps, ok, ms

def main():
    lab = os.path.join(HERE, "lab"); os.makedirs(lab, exist_ok=True)
    out = open(os.path.join(lab, "PN1_MULTITARGET_RHO.csv"), "w", newline="", encoding="utf-8")
    w = csv.writer(out)
    w.writerow(["db","K","rep","first_hit_steps","ok","ms_ms","verified","note"])
    dbs = [14, 16, 18]
    Ks = [1, 2, 4, 8, 16]
    reps = 4
    summary = {}
    for db in dbs:
        for K in Ks:
            hits = []
            for r in range(reps):
                steps, ok, ms = first_hit(db, K, seed=20260931 + 1000*r + db + K,
                                          W=16, b=4, Kt=16)
                w.writerow([db, K, r, steps, int(ok), "%.3f" % ms, int(ok),
                            "wallcap" if (steps >= 1 << 40) else ""])
                out.flush()
                if ok and steps > 0:
                    hits.append(steps)
                print("db=%2d K=%2d rep=%d first_hit=%-10d ok=%d" % (db, K, r, steps, ok), flush=True)
            g = math.exp(sum(math.log(h) for h in hits) / len(hits)) if hits else None
            summary[(db, K)] = (g, len(hits))
    out.close()
    # fit log2(E[first_hit]) vs log2(K) per db (slope ~ -0.5 predicted)
    print("\n== PN-1 summary: first-hit gmean vs K (slope vs log2 K) ==")
    for db in dbs:
        pts = [(K, summary[(db, K)][0]) for K in Ks if summary[(db, K)][1] >= 3]
        if len(pts) >= 4:
            x = [math.log2(K) for K, _ in pts]
            y = [math.log2(g) for _, g in pts]
            n = len(x)
            mx, my = sum(x)/n, sum(y)/n
            sxx = sum((xi-mx)**2 for xi in x); sxy = sum((xi-mx)*(yi-my) for xi, yi in zip(x, y))
            slope = sxy/sxx if sxx > 0 else None
            print("db=%d slope(log2K)=%s  (predicted -0.5 if sqrt(N/K))" % (db,
                  "%.3f" % slope if slope is not None else "NA"))
        else:
            print("db=%d: insufficient verified reps" % db)
    print("WROTE lab/PN1_MULTITARGET_RHO.csv")

if __name__ == "__main__":
    main()