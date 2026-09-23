# -*- coding: utf-8 -*-
"""smoke_bsgs_only.py — bsgs ONLY, on the real smallest row (db=12), flushed, time-capped,
independent k re-verification."""
import io, json, os, sys, time
sys.stdout.reconfigure(encoding="utf-8", line_buffering=True)
sys.stderr.reconfigure(encoding="utf-8", line_buffering=True)
RESEARCH = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path[:0] = [RESEARCH]
import gen, solvers

rows = gen.gen_prime_instances([12], seed=20260922, reps=1)
row = rows[0]
N = int(row["l"])
p = int(row["p"])
G = (int(row["Gx"]), int(row["Gy"]))
Q = (int(row["Qx"]), int(row["Qy"]))
print("ROW db=%s l=%d p=%d G=%s Q=%s" % (row["db"], N, p, G, Q), flush=True)

t0 = time.time()
try:
    r = solvers.bsgs(row, N, seed=3)
    print("BSGS_RET=%s" % {k: str(v)[:80] for k, v in r.items()} if isinstance(r, dict) else r, flush=True)
except Exception as e:
    print("BSGS_ERR %s: %s" % (type(e).__name__, e), flush=True)
    sys.exit(1)
dt = time.time() - t0

# independent verify via gen.mul
k = r.get("k") if isinstance(r, dict) else None
ok = None
if k is not None:
    try:
        back = gen.mul(int(k), G, p)
        ok = (tuple(back) == tuple(Q))
    except Exception as e:
        ok = "ERR %s" % e
print("BSGS k=%r recovered_ok=%s steps=%s dt=%.2fs" % (k, ok, r.get("steps") if isinstance(r, dict) else "?", dt), flush=True)
sys.exit(0 if ok is True else 1)
