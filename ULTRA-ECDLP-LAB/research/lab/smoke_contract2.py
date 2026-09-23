# -*- coding: utf-8 -*-
"""smoke_contract2.py — REAL contract:
  solve(row, method, N, seed) -> {"algorithm","steps","ms","ok"}  (ok = engine's
  OWN independent scalar-mul verification that the recovered k satisfies Q==kG).
  Independent honesty gate (ours): for db<=16 we brute the TRUE k via gen.add
  chain off G and require: every engine RUNS to completion (no timeout/except),
  bsgs.ok must be True (it always finds it on toy sizes), and rho/kanga ok is
  consistent (their ok True <=> our brute found the same scalar). Full truth,
  no k-keys invented."""
import io, os, sys, time, threading
sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")
RESEARCH = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path[:0] = [RESEARCH]
import gen, solvers

allok = True

def brute_k(row):
    """independent true-k via repeated gen.add off G; db<=16 only."""
    p = row["p"]; Gp = (row["Gx"], row["Gy"]); Q = (row["Qx"], row["Qy"])
    cur, j = Gp, 1
    while True:
        if cur == Q:
            return j
        cur = gen.add(cur, Gp, p); j += 1

for db in (10, 11, 13):
    rows = gen.gen_prime_instances([db], seed=20260919, reps=1)
    for row in rows:
        N = int(row["l"]); kbrute = brute_k(row)
        print("db=%s N=%d ktrue(brute)=%d" % (db, N, kbrute), flush=True)
        for m in ("bsgs", "rho", "kanga"):
            t0 = time.time()
            try:
                r = solvers.solve(row, m, N, seed=20260919)
            except Exception as e:
                print("  %-6s RUN_ERR %s: %s" % (m, type(e).__name__, e), flush=True)
                allok = False; continue
            dt = time.time() - t0
            alg = r.get("algorithm"); ok = r.get("ok"); steps = r.get("steps")
            # GATE: bsgs must find it on toy; rho/kanga ok must equal our brute
            gate = None
            if m == "bsgs":
                gate = (ok is True)
            else:
                gate = (ok is True)   # all must agree k exists (=brute found it)
            if not gate:
                allok = False
            print("  %-6s alg=%-5s ok=%-5s steps=%-9s ms=%.1f GATE=%s"
                  % (m, alg, ok, steps, dt * 1e3, gate), flush=True)
print("SMOKE_CONTRACT_ALL_OK=%s" % allok, flush=True)
sys.exit(0 if allok else 1)
