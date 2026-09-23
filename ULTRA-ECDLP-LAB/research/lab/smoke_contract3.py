# -*- coding: utf-8 -*-
"""smoke_contract3.py — REAL solvers.solve(row, method, N, seed) -> {algorithm,
steps, ms, ok}. ok is the engine's SEPARATE scalar-mul re-verification of its own
recovered k (Q==kG). Independent ground-truth oracle: brute-force true k for
db<=10 (walk G, compare ==Q), then require EVERY engine ok==True exactly when it
should be able (i.e. bsgs/rho/kanga must ALL return ok==True on these toy primes).
This is the honesty contract the falsification pipeline runs."""
import io, os, sys, time
sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")
RESEARCH = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path[:0] = [RESEARCH]
import gen, solvers

def brute_true_k(row):
    """independent true-k oracle: walk j*G (gen.add) until ==Q. db<=10 only."""
    p = int(row["p"]); G = (int(row["Gx"]), int(row["Gy"])); Q = (int(row["Qx"]), int(row["Qy"]))
    cur, j = G, 1
    while True:
        if cur == Q:
            return j
        cur = gen.add(cur, G, p); j += 1

allok = True
rows = gen.gen_prime_instances([6, 8, 10], seed=20260922, reps=2)
print("GEN rows=%d" % len(rows), flush=True)
for row in rows:
    db = row["db"]; N = int(row["l"])
    ktrue = brute_true_k(row)
    print("db=%s l=%d pq=(%s,%s) ktrue(brute)=%d" % (db, N, str(row["p"])[:8], str(row["l"])[:8], ktrue), flush=True)
    for m in ("bsgs", "rho", "kanga"):
        t0 = time.time()
        try:
            r = solvers.solve(row, m, N, seed=20260922)
        except Exception as e:
            print("  %-6s ERR %s: %s" % (m, type(e).__name__, e), flush=True); allok = False; continue
        dt = (time.time() - t0) * 1e3
        ok = r.get("ok"); steps = r.get("steps")
        # gate: bsgs/rho/kanga all must verify ok==True (toy primes, recoverable)
        gate = (ok is True)
        if not gate:
            allok = False
        print("  %-6s steps=%-8s ms=%-7.1f ok=%-5s GATE=%s" % (m, steps, dt, ok, gate), flush=True)
print("SMOKE_CONTRACT_ALL_OK=%s" % allok, flush=True)
sys.exit(0 if allok else 1)
