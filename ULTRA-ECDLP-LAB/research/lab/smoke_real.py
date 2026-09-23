# -*- coding: utf-8 -*-
"""smoke_real.py — run real bsgs/rho/kanga using gen's true row schema
(Gx/Gy base, Qx/Qy target, l order, db bit-depth, k true scalar) and
re-verify each recovered k independently: k*Gmod == Q via gen.mul."""
import io, os, sys
sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")
RESEARCH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path[:0] = [RESEARCH]

import gen, solvers

rows = gen.gen_prime_instances([12, 16], seed=20260922, reps=2)
print("GEN rows:", len(rows))

def verify_k(r, k):
    if k is None:
        return None
    G = (int(r["Gx"]), int(r["Gy"]))
    Q = (int(r["Qx"]), int(r["Qy"]))
    back = gen.mul(k, G, int(r["p"]))
    return tuple(back) == tuple(Q)

allok = True
for r in rows:
    N = int(r["l"])
    db = r["db"]
    ktrue = int(r["k"])
    print("db=%s N=%d ktrue=%d" % (db, N, ktrue))
    for name in ("bsgs", "rho", "kanga"):
        try:
            if name == "bsgs":
                out = solvers.bsgs(r, N, seed=1)
            elif name == "rho":
                out = solvers.rho(r, N, seed=1)
            else:
                out = solvers.kanga(r, N, seed=1)
        except Exception as e:
            print("  %s RUN_ERR %s: %s" % (name, type(e).__name__, e))
            allok = False
            continue
        krec = out.get("k") if isinstance(out, dict) else out
        ok = verify_k(r, krec)
        if ok is not True:
            allok = False
        print("  %s -> k=%r verified=%s" % (name, krec, ok))
print("SMOKE_ALL_OK=%s" % allok)
sys.exit(0 if allok else 1)
