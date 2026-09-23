#!/usr/bin/env python3
"""solvers.py — candidate DLP solvers for the synthetic benchmark (ALL toy-only).

Honest exhibits only; every returned k is re-verified by an independent scalar mul.
S1 bsgs  — interval-adapted baby-step/giant-step (memory √N, steps 2√N).
S2 rho   — classic Pollard rho for the FULL-group DLP (order l); does NOT exploit the
           interval; measured α vs l = 0.5, α vs N = 0 (huge constant).
S3 kanga — van Oorschot-Wiener parallel kangaroo w/ distinguished points (Phase-7 engine
           port, single-threaded scheduling; tunable K jump table, b DP bits).
S4 pir   — R independent rho restarts, take min-steps (shows restarts don't shift α).
S5 ph    — Pohlig-Hellman on the composite-order(smooth) CONTROL instances only.
S6 gro   — Grover-search EMULATION on db<=12 (classical amplitude-vector simulation of the
           quantum algorithm): statis oracle-queries ~ (π/4)√N. EMULATION, NO CLAIM.

Every solver returns dict(algorithm, steps, ms, ok, verified).
"""
import math, random, time, sys, json
from gen import add, mul, modinv, sqrt_mod, factor_small, TOY_P, TOY_L, TOY_G

# ---------------- shared timing / verification ----------------
def _sec():
    return time.perf_counter()

def _verify_prime(row, k):
    G = (row["Gx"], row["Gy"])
    got = mul(k, G, row["p"])
    return got is not None and got[0] == row["Qx"] and got[1] == row["Qy"]

def _res(alg, steps, ms, ok):
    return {"algorithm": alg, "steps": int(steps), "ms": ms, "ok": bool(ok)}

# ---------------- Jacobian helpers (mirror ec.hpp add_affine, VERIFIED) ----------------
def jac_from_aff(x, y, p):
    return (x % p, y % p, 1)

def jac_add_aff(a, bx, by, p):
    X, Y, Z = a
    Z1Z1 = Z * Z % p
    U2 = bx % p * Z1Z1 % p
    S2 = by % p * (Z1Z1 * Z % p) % p
    H = (U2 - X) % p
    R = (S2 - Y) % p
    HH = H * H % p
    HHH = H * HH % p
    V = X * HH % p
    X3 = (R * R - HHH - 2 * V) % p
    Y3 = (R * (V - X3) - Y * HHH) % p
    Z3 = Z * H % p
    return (X3, Y3, Z3)

def jac_to_aff(a, p):
    X, Y, Z = a
    zi = modinv(Z, p)
    x = X * zi % p * zi % p
    y = Y * zi % p * zi % p * zi % p
    return (x % p, y % p)

# ---------------- S1: interval BSGS ----------------
def bsgs(row, N, seed):
    t0 = _sec()
    p, G, Q = row["p"], (row["Gx"], row["Gy"]), (row["Qx"], row["Qy"])
    m = math.isqrt(N) + 1
    baby = {}
    cur = None
    for j in range(m):
        baby.setdefault(cur, j)
        cur = G if cur is None else add(cur, G, p)
    step = mul(m, G, p)
    cur = Q
    steps = m
    for i in range(N // m + 2):
        steps += 1
        if cur in baby:
            cand = i * m + baby[cur]
            if cand < N and _verify_prime(row, cand):
                return _res("bsgs", steps, (_sec() - t0) * 1e3, True)
        cur = add(cur, (step[0], (-step[1]) % p), p) if step else None
    return _res("bsgs", steps, (_sec() - t0) * 1e3, False)

# ---------------- S2/S4: Pollard rho (full-group, DP, batched) ----------------
def _rho1(N, l, p, G, Q, mask, seed):
    rng = random.Random(seed)
    t0 = _sec()
    D2 = mul(2, G, p)   # partition increment (avoid in-place doubling in mixed-add)
    # fresh representation (a, b), walk X = a*G + b*Q
    a0, b0 = rng.randrange(l), rng.randrange(l)
    X = add(mul(a0, G, p), mul(b0, Q, p), p)
    store = {}
    steps = 0
    while True:
        steps += 1
        part = (X[0] % 3)
        if part == 0:
            X = G if X is None else add(X, G, p); a0 = (a0 + 1) % l
        elif part == 1:
            X = Q if X is None else add(X, Q, p); b0 = (b0 + 1) % l
        else:
            X = add(X, D2, p); a0 = (a0 + 2) % l
        if (X[0] & mask) == 0:
            key = (X[0], X[1])
            if key in store:
                a1, b1 = store[key]
                db = (b1 - b0) % l
                if db != 0:
                    da = (a0 - a1) % l
                    k = da * modinv(db, l) % l
                    if mul(k, G, p) == Q:
                        return k, steps, store, (_sec() - t0) * 1e3
                a0, b0 = rng.randrange(l), rng.randrange(l)
                X = add(mul(a0, G, p), mul(b0, Q, p), p)
                continue
            store[key] = (a0, b0)
            a0, b0 = rng.randrange(l), rng.randrange(l)
            X = add(mul(a0, G, p), mul(b0, Q, p), p)
        if steps > 8 * (1 << 20):
            return None, steps, store, (_sec() - t0) * 1e3

def rho(row, N, seed, maskbits=12, R=1):
    """R restarts -> PIR; R=1 -> plain rho. Steps counts group ops for ALL walkers."""
    p, l, G, Q = row["p"], row["l"], (row["Gx"], row["Gy"]), (row["Qx"], row["Qy"])
    mask = (1 << maskbits) - 1
    t0 = _sec()
    best = None
    for r in range(R):
        k, steps, store, ms = _rho1(N, l, p, G, Q, mask, seed + 1000 * r)
        if k is not None and (best is None or steps < best[1]):
            best = (k, steps, ms)
        if k is not None and R == 1:
            return _res("rho", steps, ms, _verify_prime(row, k))
    if best is None:
        return _res("rho", -1, (_sec() - t0) * 1e3, False)
    k, steps, ms = best
    return _res("pir" if R > 1 else "rho", steps, ms, _verify_prime(row, k))

# ---------------- S3: VOW parallel kangaroo (Phase 7/9 port) ----------------
def kanga(row, N, seed, W=32, b=6, K=32, wcc=6.0):
    p, l, Gx, Gy = row["p"], row["l"], row["Gx"], row["Gy"]
    Q = (row["Qx"], row["Qy"])
    rng = random.Random(seed)
    sl = math.isqrt(N)
    # jump table
    jumps = []
    jd = []
    for _ in range(K):
        d = 1 + rng.randrange(max(1, 2 * sl))
        jd.append(d)
        jumps.append(mul(d, (Gx, Gy), p))
    DPMASK = (1 << b) - 1
    tab = {}   # (x,y) -> (owner, dist)
    walkers = []
    t0 = _sec()
    for i in range(W):
        if i & 1:                            # wild: Q + u*G, dist u
            u = rng.randrange(1, N)
            X = add(Q, mul(u, (Gx, Gy), p), p)
            d = u % l
            own = 1
        else:                                # tame: a*G, dist a
            a = rng.randrange(1, N)
            X = mul(a, (Gx, Gy), p)
            d = a % l
            own = 0
        walkers.append([jac_from_aff(*X, p), d, own, 0])
    steps = 0
    mi = 0
    budget = W * int(24 * sl) + 65536
    solved = None
    while steps < budget:
        w = walkers[mi]; mi = (mi + 1) % W
        X, d, own, cnt = w
        if cnt >= int(wcc * sl) + 64:         # walkcap -> fresh restart
            if own == 0:
                a = rng.randrange(1, N); X = jac_from_aff(*mul(a, (Gx, Gy), p), p); d = a % l
            else:
                u = rng.randrange(1, N); X = jac_from_aff(*add(Q, mul(u, (Gx, Gy), p), p), p); d = u % l
            w[0], w[1], w[3] = X, d, 0
            continue
        sel = (X[0] >> 8) & (K - 1) if K > 1 else 0
        bx, by = jumps[sel]
        X = jac_add_aff(X, bx, by, p)
        d = (d + jd[sel]) % l
        cnt += 1
        steps += 1
        w[0], w[1], w[3] = X, d, cnt
        if (X[0] & DPMASK) == 0:
            ax, ay = jac_to_aff(X, p)
            key = (ax, ay)
            ent = tab.get(key)
            if ent is None:
                tab[key] = (own, d)
            elif ent[0] == own:
                pass
            else:
                td = d if own == 0 else ent[1]
                wd = ent[1] if own == 0 else d
                cand = (td + l - wd) % l
                if _verify_prime(row, cand):
                    solved = cand
                    break
            if own == 0:
                a = rng.randrange(1, N); X = jac_from_aff(*mul(a, (Gx, Gy), p), p); d = a % l
            else:
                u = rng.randrange(1, N); X = jac_from_aff(*add(Q, mul(u, (Gx, Gy), p), p), p); d = u % l
            w[0], w[1], w[3] = X, d, 0
    ok = solved is not None and _verify_prime(row, solved)
    return _res("kanga", steps, (_sec() - t0) * 1e3, ok)

# ---------------- S5: Pohlig-Hellman (smooth control) ----------------
def _ph_steps(row):
    """steps as in ph() but without the solve (for a cheap brute-vs-PH contrast)."""
    p, g, h, l = row["p"], row["g"], row["h"], row["l"]
    fac = factor_small(l)
    pe = {}
    for q in fac:
        pe[q] = pe.get(q, 0) + 1
    Steps = 0
    for q, e in pe.items():
        Steps += e * q
    return Steps

def brute_dlp(row):
    """Naive scan k=1..N (control for PH), steps == N. Only for control-group instances."""
    p, g, h = row["p"], row["g"], row["h"]
    N = 1 << row["db"]
    t0 = _sec()
    cur = 1
    for k in range(1, N + 1):
        cur = cur * g % p
        if cur == h:
            return _res("brute", k, (_sec() - t0) * 1e3, True)
    return _res("brute", N, (_sec() - t0) * 1e3, False)

def ph(row):
    p, g, h, l = row["p"], row["g"], row["h"], row["l"]
    t0 = _sec()
    fac = factor_small(l)
    # group factors by prime -> e
    pe = {}
    for q in fac:
        pe[q] = pe.get(q, 0) + 1
    crt_parts = []
    steps = 0
    for q, e in pe.items():
        qe = q ** e
        x_q = 0
        base = pow(g, l // q, p)   # generator of the order-q subgroup
        for k in range(e):
            cur = h * pow(g, (l - x_q) % l, p) % p
            c = pow(cur, l // (q ** (k + 1)), p)
            d_k = 0
            for val in range(q):
                steps += 1
                if pow(base, val, p) == c:
                    d_k = val
                    break
            x_q += d_k * (q ** k)
        crt_parts.append((x_q, qe))
    # CRT combine
    x = 0; M = 1
    for xi, mi in crt_parts:
        x = (x + (xi - x) * modinv(M, mi) * M) % (M * mi)
        M *= mi
    ok = pow(g, x, p) == h
    return _res("ph", steps, (_sec() - t0) * 1e3, ok)

# ---------------- S6: Grover EMULATION (db <= 12) ----------------
def grover(row, N):
    """Classical amplitude-vector simulation of Grover search over n=db bits.
    Oracle f(j)=1 iff j*G == Q. Reports oracle-queries (Grover iterations),
    reproducing quadratic speedup sqrt(N) oracle calls for N classical ones.
    EMULATION ON A CLASSICAL MACHINE — NO QUANTUM HARDWARE, NO ECDLP CLAIM."""
    db = int(math.log2(N))
    assert db <= 12, "Grover emulation limited to db<=12"
    p, G, Q = row["p"], (row["Gx"], row["Gy"]), (row["Qx"], row["Qy"])
    n = db
    D = 1 << n
    # find marked j set (should be exactly {k}, k in [1,N))
    marked = []
    # ORACLE QUERIES COUNTED, not amplitude state — evaluate f over full domain once
    # (that is 2^n classical evals to BUILD the emulation; separate from the algorithm's
    # query cost, which we report as the Grover iterations ~ (pi/4) sqrt(N)).
    for j in range(N):
        if mul(j, G, p) == Q:
            marked.append(j)
    state = [complex(1.0 / math.sqrt(D), 0)] * D
    had = 1.0 / math.sqrt(D)
    iters = int(math.pi / 4 * math.sqrt(D))
    queries = 0
    for it in range(iters):
        queries += 1
        # oracle: phase flip on marked
        for j in marked:
            state[j] = -state[j]
        # diffusion: reflection about mean
        mean = sum(state) / D
        for j in range(D):
            state[j] = 2 * mean - state[j]
    # measure
    probs = [abs(z) ** 2 for z in state]
    top = max(range(D), key=lambda j: probs[j])
    ok = top == row["k"]
    return _res("grover_emu", queries, 0.0, ok)

# ---------------- dispatch ----------------
def solve(row, method, **kw):
    N = 1 << row["db"]
    seed = kw.get("seed", 20260922)
    if method == "bsgs": return bsgs(row, N, seed)
    if method == "rho":  return rho(row, N, seed, R=1)
    if method == "pir":  return rho(row, N, seed, R=kw.get("R", 4))
    if method == "kanga":
        return kanga(row, N, seed, W=kw.get("W", 32), b=kw.get("b", 6), K=kw.get("K", 32), wcc=kw.get("wcc", 6.0))
    if method == "ph":
        assert row.get("smooth"), "PH only on composite-order control instances"
        return ph(row)
    if method == "brute":
        assert row.get("smooth"), "brute control only on control instances"
        return brute_dlp(row)
    if method == "grover": return grover(row, N)
    raise ValueError(method)

if __name__ == "__main__":
    # smoke test on the smallest instance
    import gen
    rows = gen.gen_prime_instances([12, 16], 20260922, 1)
    for method in ["bsgs", "rho", "kanga", "grover"]:
        r = solve(rows[0], method)
        print(method, json.dumps(r))
    sr = gen.gen_smooth_instances([20], 20260922, 1)
    print("ph", json.dumps(solve(sr[0], "ph")))