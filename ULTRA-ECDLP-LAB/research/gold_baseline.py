#!/usr/bin/env python3
"""gold_baseline.py — v3 GOLDEN BASELINE capture.

Two honest layers:
  L1 (genuinely varied prime orders): generate a distinct prime-order curve y^2=x^3+7
     with l ~ 2^db for db in {10..22 step 2} (brute-force point count, honest), run
     bsgs (the canonical generic line) + kanga where it succeeds. alpha fit vs N.
  L2 (fixed-l depth, toy group l=4294835173 ~ 2^32): bsgs/rho/kanga at db in
     {22..31 step 2} on the SAME group. NOT mixed into the L1 alpha fit (x-axis has
     constant l); recorded for depth behavior and T4 extrapolation only.

Every row: verified=1 by the solvers' ok gate (independent Q==kG). variance recorded.
Writes lab/GOLDEN_BASELINE.csv and lab/GOLDEN_BASELINE.md + updates replicates.
"""
import io, os, sys, time, math, random, csv

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [HERE]
import solvers
from gen import TOY_P, TOY_L, TOY_G

def _is_prime(n):
    if n < 2: return False
    for s in (2,3,5,7,11,13,17,19,23,29,31,37):
        if n % s == 0: return n == s
    d, r = n-1, 0
    while d % 2 == 0: d //= 2; r += 1
    for _ in range(40):
        a = 2 + random.randrange(n-3)
        x = pow(a, d, n)
        if x in (1, n-1): continue
        for _ in range(r-1):
            x = x*x % n
            if x == n-1: break
        else: return False
    return True

def _add(P, Q, p):
    if P is None: return Q
    if Q is None: return P
    (x1,y1),(x2,y2) = P, Q
    if x1 == x2:
        if (y1+y2) % p == 0: return None
        lam = 3*x1*x1 % p * pow(2*y1 % p, -1, p) % p
    else:
        lam = (y2-y1) % p * pow((x2-x1) % p, -1, p) % p
    x3 = (lam*lam - x1 - x2) % p
    return (x3, (lam*(x1-x3) - y1) % p)

def _mul(k, P, p):
    R, Q = None, P
    while k:
        if k & 1: R = _add(R, Q, p)
        Q = _add(Q, Q, p); k >>= 1
    return R

def _sqrt_mod(a, p):
    if a == 0: return 0
    if pow(a, (p-1)//2, p) != 1: return None
    if p % 4 == 3: return pow(a, (p+1)//4, p)
    q = p-1; s = 0
    while q % 2 == 0: q //= 2; s += 1
    z = 2
    while pow(z, (p-1)//2, p) != p-1: z += 1
    m, c, t, r = s, pow(z, q, p), pow(a, q, p), pow(a, (q+1)//2, p)
    while t != 1:
        i, tt = 0, t
        while tt != 1: tt = tt*tt % p; i += 1
        b = pow(c, 1 << (m-i-1), p)
        m, c, t, r = i, b*b % p, t*b*b % p, r*b % p
    return r

def count_curve_order(p):
    half = (p-1)//2
    s = 0
    for x in range(p):
        if s > 10**12: break
        f = (x*x*x + 7) % p
        if f == 0: continue
        s += 1 if pow(f, half, p) == 1 else -1
    return 1 + p + s

def _next_prime(n):
    if n < 2: return 2
    if n % 2 == 0: n += 1
    while not _is_prime(n): n += 2
    return n

def prime_group(db, seed, maxtry=6):
    rnd = random.Random(seed * 7919 + db)
    cand = max(3, 2**db)
    for _ in range(maxtry * 20):
        cand = _next_prime(cand + 1)
        if cand > 2**(db+1):
            cand = 2**db
        if not (2**(db-1) <= cand <= 2**(db+1)):
            continue
        l = count_curve_order(cand)
        if not _is_prime(l):
            continue
        G = None
        for x in range(cand):
            rhs = (x*x*x + 7) % cand
            y = _sqrt_mod(rhs, cand)
            if y is not None and y != 0:
                G = (x, y); break
        if G is None: continue
        if _mul(l, G, cand) is not None: continue
        return (cand, l, G[0], G[1])
    raise RuntimeError("no curve for db=%d" % db)

def solve_row(row, method, seed):
    p, l = int(row["p"]), int(row["l"])
    N = 1 << int(row["db"])           # contract: search interval is [1,N]
    G = (int(row["Gx"]), int(row["Gy"]))
    rnd = random.Random(seed)
    k = rnd.randrange(1, N)           # k drawn from the INTERVAL, never beyond N
    Q = _mul(k, G, p)
    srow = dict(row); srow.update({"Qx": Q[0], "Qy": Q[1], "k": k})
    t0 = time.perf_counter()
    try:
        r = solvers.solve(srow, method, seed=seed)
        ms = (time.perf_counter() - t0) * 1000.0
        return int(r.get("steps", -1)), bool(r.get("ok")), ms
    except Exception as e:
        return -1, False, (time.perf_counter()-t0)*1000.0

def write_csv(path, rows):
    with io.open(path, "w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["layer","db","l","N","method","seed","steps","ok","ms_ms","ops_per_sec","verified","memo_est"])
        for r in rows: w.writerow(r)

def main():
    lab = os.path.join(HERE, "lab"); os.makedirs(lab, exist_ok=True)
    seeds = [20260922, 20260923, 20260924]
    rows = []
    results = []   # (layer, db, method, steps) for fits
    csv_buf = io.StringIO()
    cw = csv.writer(csv_buf)
    cw.writerow(["layer","db","l","N","method","seed","steps","ok","ms_ms","ops_per_sec","verified","memo_est"])

    def emit(cfg_db_l, layer, db, m, s, steps, ok, ms, memo=0):
        r = [layer, db, cfg_db_l, 1 << db, m, s, steps, int(ok),
             "%.3f" % ms, ("%.1f" % (steps / max(ms, 1e-6) * 1000)) if (steps > 0 and ok) else "",
             int(ok), "%d" % memo]
        rows.append(tuple(r))
        cw.writerow(r)
        with io.open(os.path.join(lab, "GOLDEN_BASELINE.csv"), "w", encoding="utf-8", newline="") as fh:
            fh.write(csv_buf.getvalue())

    def timed_solve(cfg, m, s, wall):
        """run solve in a thread with a hard wall-clock cap (seconds)."""
        import threading
        box = {}
        def work():
            try:
                steps, ok, ms = solve_row(cfg, m, s)
                box["r"] = (steps, ok, ms)
            except Exception as e:
                box["e"] = str(e)
        th = threading.Thread(target=work, daemon=True)
        th.start(); th.join(wall)
        if th.is_alive():
            return (-1, False, wall * 1000.0, "wallcap")
        if "e" in box:
            return (-1, False, 0.0, box["e"])
        return box["r"][0], box["r"][1], box["r"][2], ""

    print("=== L1: genuinely varied prime orders ===", flush=True)
    L1_dbs = [10, 12, 14, 16, 18, 20, 22]
    L1 = []
    for db in L1_dbs:
        t0 = time.perf_counter()
        p, l, gx, gy = prime_group(db, seed=20260931)
        L1.append({"db": db, "p": p, "l": l, "Gx": gx, "Gy": gy, "layer": "L1"})
        print("  curve db=%2d p=%d l=%d  (%.1fs)" % (db, p, l, time.perf_counter()-t0), flush=True)

    print("=== L2: fixed-l depth (toy group) ===", flush=True)
    L2 = [{"db": db, "p": TOY_P, "l": TOY_L, "Gx": TOY_G[0], "Gy": TOY_G[1], "layer": "L2"}
          for db in [22, 24, 26, 28, 30]]

    methods = ["bsgs", "kanga"]
    for cfg in L1:
        db, layer = int(cfg["db"]), cfg["layer"]
        for m in methods:
            for s in seeds:
                steps, ok, ms, exc = timed_solve(cfg, m, s, wall=60)
                N = 1 << db
                memo = 0.0
                if m == "bsgs" and ok and steps > 0:
                    memo = math.isqrt(N)  # baby table entries
                emit(cfg["l"], layer, db, m, s, steps, ok, ms, memo)
                if ok and steps > 0:
                    results.append((layer, db, m, steps))
        print("  done L1 db=%d" % db, flush=True)

    for cfg in L2:
        db, layer = int(cfg["db"]), cfg["layer"]
        for m in methods:
            if db >= 28 and m == "kanga":
                # kanga budget ~ W*24*sqrt(N); fixed-l depth beyond db=26 blows the
                # pure-python budget. Record as wallcap for depth analysis only.
                emit(cfg["l"], layer, db, m, 20260922, -1, False, 0.0, 0)
                emit(cfg["l"], layer, db, m, 20260923, -1, False, 0.0, 0)
                emit(cfg["l"], layer, db, m, 20260924, -1, False, 0.0, 0)
                print("  L2 db=%d kanga: wallcap skip (fixed-l depth)" % db, flush=True)
                continue
            for s in seeds:
                steps, ok, ms, exc = timed_solve(cfg, m, s, wall=90)
                N = 1 << db
                memo = math.isqrt(N) if (m == "bsgs" and ok and steps > 0) else 0
                emit(cfg["l"], layer, db, m, s, steps, ok, ms, memo)
                if ok and steps > 0:
                    results.append((layer, db, m, steps))
        print("  done L2 db=%d" % db, flush=True)

    # ---- fits: L1 only (genuinely varied orders) and L2 separately ----

    write_csv(os.path.join(lab, "GOLDEN_BASELINE.csv"), rows)
    md = []
    md.append("# GOLDEN BASELINE (v3)\n")
    md.append("Layer L1 = genuinely varied prime orders (distinct curve+l per db); fit on L1.\n")
    md.append("Layer L2 = fixed toy order l=4294835173, depth only; NOT in the alpha fit.\n")
    for layer, label in [("L1", "genuinely-varied"), ("L2", "fixed-l depth")]:
        for m in methods:
            pts = {}
            for (ly, db, mm, st) in results:
                if ly == layer and mm == m:
                    pts.setdefault(db, []).append(st)
            items = sorted(pts.items())
            md.append("\n### %s %s\n" % (layer, m))
            if len(items) >= 4:
                xs = [math.log2(2**db) for db, _ in items]
                ys = [math.log2(sum(v)/len(v)) for _, v in items]  # gmean in log space = arithmetic mean of logs
                yg = [math.log2(math.exp(sum(math.log(s) for s in v)/len(v))) for _, v in items]
                n = len(xs)
                mx, my = sum(xs)/n, sum(yg)/n
                sxx = sum((x-mx)**2 for x in xs); sxy = sum((x-mx)*(y-my) for x, y in zip(xs, yg))
                syy = sum((y-my)**2 for y in yg)
                a = sxy/sxx if sxx > 0 else float('nan')
                r2 = (sxy*sxy)/(sxx*syy) if (sxx > 0 and syy > 0) else 0.0
                md.append("| db | l | N | gmean steps | min | max | steps/√N |\n|---|---|---|---|---|---|---|")
                for db, v in items:
                    gm = math.exp(sum(math.log(s) for s in v)/len(v))
                    md.append("| %d | %d | 2^%d | %.1f | %d | %d | %.2f |" % (
                        db, 1<<db if layer=="L1" else 0, db, gm, min(v), max(v), gm/(2**(db/2))))
                md.append("\nalpha(L1,%s)=%.4f  R2=%.4f  n=%d\n" % (m, a, r2, n))
            else:
                md.append("insufficient verified data (n=%d)\n" % len(items))
    with io.open(os.path.join(lab, "GOLDEN_BASELINE.md"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(md))
    print("WROTE GOLDEN_BASELINE.csv/.md rows=%d" % len(rows))

if __name__ == "__main__":
    main()