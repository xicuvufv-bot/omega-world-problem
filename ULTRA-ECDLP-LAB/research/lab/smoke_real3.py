# -*- coding: utf-8 -*-
"""smoke_real3.py — HONEST end-to-end with the TRUE row schema (gen rows carry
Gx/Gy/Qx/Qy/l/p/db; N = order l = TOY_L). Each solver is spawned in its own
thread with a hard wall-clock watchdog so a single pathological loop cannot
hang verification. Every recovered k is re-verified independently by scalar
multiplication Q == k*G using gen.mul."""
import io, os, sys, threading, time
sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")
RESEARCH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path[:0] = [RESEARCH]
import gen, solvers

rows = gen.gen_prime_instances([12, 16], seed=20260922, reps=1)
print("GEN rows=%d" % len(rows), flush=True)
row = rows[0]
N = int(row["l"])          # order (TOY_L)
p = int(row["p"])
G = (int(row["Gx"]), int(row["Gy"]))
Q = (int(row["Qx"]), int(row["Qy"]))

def verify_k(k):
    if k is None:
        return None
    try:
        back = gen.mul(int(k), G, p)
        ok = (back[0] == Q[0] and back[1] == Q[1])
        return bool(ok)
    except Exception as e:
        return "ERR %s" % e

def run_capped(fn, row, N, seed, timeout):
    box = {}
    def target():
        try:
            box["res"] = fn(row, N, seed=seed)
        except Exception as e:
            box["err"] = "%s: %s" % (type(e).__name__, e)
    t = threading.Thread(target=target, daemon=True)
    t0 = time.time(); t.start(); t.join(timeout)
    if t.is_alive():
        return {"_TIMEOUT": True, "timeout": timeout}
    return box

allok = True
for name, fn in (("bsgs", solvers.bsgs), ("rho", solvers.rho), ("kanga", solvers.kanga)):
    box = run_capped(fn, row, N, 20260922, 25)
    if "_TIMEOUT" in box:
        print("%s: TIMEOUT>%ss (possible pathological loop on order %d)" % (name, box["timeout"], N), flush=True)
        allok = False
        continue
    if "err" in box:
        print("%s: ERR %s" % (name, box["err"]), flush=True)
        allok = False
        continue
    r = box["res"]
    k = r.get("k") if isinstance(r, dict) else None
    v = verify_k(k)
    steps = r.get("steps") if isinstance(r, dict) else None
    print("%s: k=%r steps=%s VERIFIED=%s" % (name, k, steps, v), flush=True)
    if v is not True:
        allok = False
print("SMOKE_ALL_OK=%s" % allok, flush=True)
sys.exit(0 if allok else 1)
