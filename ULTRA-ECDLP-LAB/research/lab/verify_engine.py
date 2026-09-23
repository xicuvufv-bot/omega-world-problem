# -*- coding: utf-8 -*-
"""verify_engine.py — DETERMINISTIC engine pickup + smoke (loud-fail bootstrap).

The engine modules (solvers/gen/fit) live at the research ROOT per glob evidence, but
hypothesis/classify artifacts live in research\\lab. Some SESSION runs resolved them
from lab, others from root — so we never hard-code a single dir. Instead:

  1. Candidate dirs = {this file's dir (research\\lab), research root, CWD}.
  2. For each of (solvers, gen, fit): pick the FIRST module that imports cleanly.
  3. Persist the resolved __file__ paths to ENGINE_PICKUP.json (single source of truth
     consumed by every later stage: probes, pipeline, classify — no import guessing).
  4. Smoke: solve one toy row at db=16 with bsgs + rho + kanga, INDEPENDENTLY re-verify
     each recovered k by scalar mul. Exit code 0 only if all three solve AND verify.

Never proceeds silently: any missing engine, failed smoke, or verification mismatch
exits non-zero with a clear message so the rest of the pipeline refuses to run.
"""
import io, json, os, random, sys, time

def _here():
    return os.path.dirname(os.path.abspath(__file__))

HERE = _here()                                   # research\lab
RESEARCH = os.path.dirname(HERE)                 # research
CWD = os.getcwd()

def _res(path):
    return os.path.normpath(path)

CANDIDATES = []
for _d in (HERE, RESEARCH, CWD):
    _d = _res(_d)
    if _d not in CANDIDATES:
        CANDIDATES.append(_d)

sys.path[:0] = CANDIDATES

pickup = {}
missing = []
for modname in ("solvers", "gen", "fit", "classify"):
    found = False
    for d in CANDIDATES:
        p = os.path.join(d, modname + ".py")
        if os.path.isfile(p):
            # import from that exact path (insert only that dir first)
            try:
                import importlib
                saved = list(sys.path)
                sys.path[:0] = [d]
                m = importlib.import_module(modname)
                sys.path[:0] = saved
                pickup[modname] = _res(p)
                found = True
                break
            except Exception as e:
                sys.path[:0] = saved
                pickup[modname + "_ERR"] = "%s: %s" % (type(e).__name__, e)
    if not found:
        missing.append(modname)

with io.open(os.path.join(HERE, "ENGINE_PICKUP.json"), "w", encoding="utf-8", newline="") as f:
    json.dump(pickup, f, indent=1, ensure_ascii=False)

print("ENGINE PICKUP:", json.dumps(pickup, indent=1, ensure_ascii=False))
print("CANDIDATES:", CANDIDATES)
if missing:
    print("MISSING ENGINES:", missing)
    sys.exit(1)

# ------------------------- independent smoke -------------------------
import inspect
try:
    import solvers
    import gen as G
    from gen import add, mul, modinv
    from solvers import bsgs, rho as _rho, kanga
except Exception as e:
    print("SMOKE IMPORT FAILED:", type(e).__name__, e)
    sys.exit(1)

P = getattr(G, "TOY_P", None) or getattr(G, "P", None)
L = getattr(G, "TOY_L", None) or getattr(G, "L", None)
GX = getattr(G, "TOY_GX", None) or (getattr(G, "TOY_G", None) or [None, None])[0]
GY = getattr(G, "TOY_GY", None) or (getattr(G, "TOY_G", None) or [None, None])[1]
print("smoke constants: p=%r l=%r Gx=%r" % (P, L, GX))

def _verify(k, Q):
    got = mul(k, (GX, GY), P)
    return got is not None and got[0] == Q[0] and got[1] == Q[1]

def _make(db, seed):
    rng = random.Random(seed)
    k = rng.randrange(1, 1 << db)
    Q = mul(k, (GX, GY), P)
    if Q is None:
        return None
    return dict(Gx=GX, Gy=GY, Qx=Q[0], Qy=Q[1], p=P, l=L, db=db, seed=seed, k=k)

def solve_one(db, seed, fn, **kw):
    row = _make(db, seed)
    t0 = time.perf_counter()
    try:
        r = fn(row, **kw)
    except TypeError:
        r = fn(row)
    dt = (time.perf_counter() - t0) * 1e3
    if isinstance(r, dict):
        kk = r.get("k")
        steps = r.get("steps")
    else:
        kk, steps = None, None
    return dict(db=db, seed=seed, k=kk, steps=steps, ms=round(dt, 3),
                verified=int(_verify(kk, (row["Qx"], row["Qy"])) if kk is not None else 0))

results = []
for name, fn, kw in (("bsgs", bsgs, {"mem": 3}),
                     ("rho", _rho, {"seed": 1}),
                     ("kanga", kanga, {})):
    res = solve_one(16, 20260922, fn, **kw)
    res["engine"] = name
    results.append(res)

allok = all(r["verified"] == 1 and r["k"] is not None for r in results)
for r in results:
    print("SMOKE %-6s db=%d k=%s steps=%s ms=%s verified=%d" %
          (r["engine"], r["db"], r["k"], r["steps"], r["ms"], r["verified"]))
print("ENGINE VERDICT:", "OK" if allok else "FAIL")
sys.exit(0 if allok else 1)
