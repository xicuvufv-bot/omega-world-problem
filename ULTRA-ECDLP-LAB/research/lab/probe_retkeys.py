# -*- coding: utf-8 -*-
"""probe_retkeys.py — for one real row, call bsgs/rho/kanga and print the FULL
return value with all keys + types, so we read the real recovered-k key."""
import io, os, sys, threading, time
sys.stdout.reconfigure(encoding="utf-8")
RESEARCH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path[:0] = [RESEARCH]
import gen, solvers

rows = gen.gen_prime_instances([16], seed=20260922, reps=1)
row = rows[0]
N = int(row["l"])

def capped(fn, row, N, seed, secs):
    box = {}
    def target():
        try:
            box["r"] = fn(row, N, seed=seed)
        except Exception as e:
            box["e"] = "%s: %s" % (type(e).__name__, e)
    t = threading.Thread(target=target, daemon=True)
    t0 = time.time()
    t.start(); t.join(secs)
    if t.is_alive():
        box["t"] = True
    return box

for name, fn in (("bsgs", solvers.bsgs), ("rho", solvers.rho), ("kanga", solvers.kanga)):
    box = capped(fn, row, N, 20260922, 40)
    if box.get("t"):
        print("%s: TIMEOUT>40s" % name, flush=True); continue
    if "e" in box:
        print("%s: ERR %s" % (name, box["e"]), flush=True); continue
    r = box["r"] if isinstance(box["r"], dict) else {"RET": box["r"]}
    print("%s RET keys: %s" % (name, sorted(r.keys())), flush=True)
    for kk, vv in r.items():
        print("   %s = %r" % (kk, (str(vv)[:120] if not isinstance(vv,(int,float,bool,type(None))) else vv)), flush=True)
print("PROBE_DONE", flush=True)
