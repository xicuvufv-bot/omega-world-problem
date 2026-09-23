# -*- coding: utf-8 -*-
"""smoke_real2.py — HONEST end-to-end: take ACTUAL rows from gen.gen_prime_instances,
run the REAL bsgs/rho/kanga with their real (row, N=order_l, seed) signatures,
then INDEPENDENTLY re-verify every recovered k by scalar mul (k*G == Q)."""
import io, os, sys
sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")
RESEARCH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path[:0] = [RESEARCH]

import gen, solvers

rows = gen.gen_prime_instances([12, 16], seed=20260922, reps=2)
print("GEN rows:", len(rows))
print("SCHEMA:", sorted(rows[0].keys()))
print("SAMPLE:", {k: str(v)[:22] for k, v in rows[0].items()})

def mul_verify(row, k):
    if k is None:
        return None
    try:
        Q = gen.mul(int(k), (int(row["Gx"]), int(row["Gy"])), int(row["p"]))
        return Q == (int(row["Qx"]), int(row["Qy"]))
    except Exception as e:
        return "ERR %s" % e

allok = True
for row in rows:
    N = int(row["l"])
    db = row["db"]
    p = int(row["p"])
    print("-- db=%s l=%d k_true=%s" % (db, N, row["k"]))
    for name in ("bsgs", "rho", "kanga"):
        fn = getattr(solvers, name)
        try:
            res = fn(row, N, seed=1)
        except Exception as e:
            print("   %-6s ERR %s: %s" % (name, type(e).__name__, e))
            allok = False
            continue
        if not isinstance(res, dict):
            print("   %-6s WRONG-RETURN: %r" % (name, res)[:120])
            allok = False
            continue
        k = res.get("k")
        verified = mul_verify(row, k)
        print("   %-6s k=%s steps=%s ok=%s verified=%s" % (
            name, k, res.get("steps"), res.get("ok"), verified))
        if verified is not True:
            allok = False
print("SMOKE_ALL_OK=%s" % allok)
sys.exit(0 if allok else 1)
