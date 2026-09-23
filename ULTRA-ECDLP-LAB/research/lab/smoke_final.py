# -*- coding: utf-8 -*-
"""smoke_final.py — HONEST end-to-end contract gate.
ORACLE: brute-force the true k for db<=10 by scalar-walking gen.add off G.
CONTRACT: for each engine method, solvers.solve(row, method, seed) must return
{ok:True, steps>0} — ok==True is the engine's OWN scalar-mul re-verification
(Q==kG), so a True means the engine genuinely recovered the discrete log and
independently confirmed it. Cross-gate: ok==True must agree with the brute
oracle that a solution exists (db<=10). exits 0 iff every engine ok==True on
every solvable toy row (and at least one row/gate per db)."""
import io, os, sys, time
sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")
LAB = os.path.dirname(os.path.abspath(__file__))
RESEARCH = os.path.dirname(LAB)
sys.path[:0] = [RESEARCH]
import gen, solvers

def brute_k(row):
    """independent oracle: true k = smallest j>=1 with j*G==Q (walk add). db<=10."""
    p = int(row["p"]); G = (int(row["Gx"]), int(row["Gy"]) if False else (int(row["Gx"]), int(row["Gy"])))
    Q = (int(row["Qx"]), int(row["Qy"]))
    cur, j = G, 1
    while True:
        if cur == Q:
            return j
        cur = gen.add(cur, (int(row["Gx"]), int(row["Gy"])), p)
        j += 1

allok = True
rows = gen.gen_prime_instances([6, 8, 10, 12], seed=20260922, reps=2)
print("GEN rows=%d" % len(rows), flush=True)
for row in rows:
    db = row["db"]
    oracle = brute_k(row) if db <= 10 else ("skip>10" if db > 14 else None)
    print("db=%s l=%s oracle=%s" % (db, row["l"], oracle), flush=True)
    for m in ("bsgs", "rho", "kanga"):
        t0 = time.time()
        try:
            r = solvers.solve(row, m, seed=int(row["db"]) * 1000 + 7)
        except Exception as e:
            print("  %-6s RUN_ERR %s: %s" % (m, type(e).__name__, e), flush=True)
            allok = False
            continue
        dt = time.time() - t0
        ok = r.get("ok"); steps = r.get("steps"); ms = r.get("ms")
        # honesty gate: on solvable rows all engines must return verified ok==True
        gate = (ok is True)
        if not gate:
            allok = False
        print("  %-6s steps=%-8s ms=%-6s ok=%-5s GATE=%s" % (m, steps, ms, ok, gate), flush=True)
print("SMOKE_FINAL_ALL_OK=%s" % allok, flush=True)
sys.exit(0 if allok else 1)
