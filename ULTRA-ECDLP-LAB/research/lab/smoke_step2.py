# -*- coding: utf-8 -*-
"""smoke_step2.py — build a real TOY row via gen.gen_prime_instances, print its
schema, then run REAL solvers (bsgs/rho/kanga) with their true signatures and
independently re-verify each recovered k by scalar multiplication (pipeline
honesty gate). No verify_engine dependency."""
import io, os, sys
sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")
RESEARCH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path[:0] = [RESEARCH]

import gen, solvers

rows = gen.gen_prime_instances([12, 16], seed=20260922, reps=2)
print("GEN produced %d rows" % len(rows))
r0 = rows[0]
print("ROW SCHEMA keys:", sorted(r0.keys()))
print("ROW SAMPLE: %s" % {k: (str(v)[:40]) for k, v in r0.items()})
print("GEN module file: %s" % getattr(gen, "__file__", "?"))

for r in rows:
    N = r["l"]
    p = r["p"]
    G = r["g"]
    for name, kw in (("bsgs", {}), ("rho", {}), ("kanga", {})):
        try:
            fn = getattr(solvers, name)
            if name == "bsgs":
                out = fn(r, N, seed=1)
            elif name == "rho":
                out = fn(r, N, seed=1)
            else:
                out = fn(r, N, seed=1)
        except TypeError as e:
            print("  %s db=%s SIGMISMATCH: %s" % (name, r["db"], e))
            continue
        except Exception as e:
            print("  %s db=%s RUNTIME_ERR %s: %s" % (name, r["db"], type(e).__name__, e))
            continue
        # independent re-verification
        k = out.get("k")
        ok = None
        ver = None
        if k is not None:
            # scalar mult the recovered k back to the public key
            try:
                H = r["H"]
                back = gen.mul(k, G, p)
                ok = (back == H)
            except Exception:
                ok = None
        print("  %s db=%s k=%r verified=%s (result keys: %s)" % (
            name, r["db"], k, ok, sorted(out.keys())))
print("SMOKE_STEP2_DONE")
