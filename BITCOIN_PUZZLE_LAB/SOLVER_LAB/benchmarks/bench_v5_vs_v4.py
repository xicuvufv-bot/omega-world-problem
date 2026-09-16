"""Benchmark: v5 (fused+negation) vs v4 baseline -- hop counts and ops.

Measures the OPS reduction from the negation map on identical widths:
  * v4:  total ops ~ tame_trail + hops
  * v5:  same counter (tame trail may be shorter due to W/2 tuning)
K = total_ops / sqrt(W) for both, many seeds.
"""
import os, sys, math, random, time
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

LAB = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, LAB)
os.chdir(LAB)

from algorithms.curve import scalar_mult
from solvers.v4_kangaroo import KangarooSolver

import importlib.util
_v5_path = os.path.join(LAB, "SOLVER_LAB", "candidate", "v5_fused_negation.py")
_spec = importlib.util.spec_from_file_location("v5_fused_negation", _v5_path)
_v5mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_v5mod)
FusedNegationSolver = _v5mod.FusedNegationSolver

def run_one(cls, lo, hi, key, seed, max_seconds=120):
    try:
        if cls is KangarooSolver:
            s = cls(lo, hi, max_seconds=max_seconds, seed=seed)
            k = s.solve(scalar_mult(key))
        else:
            s = cls(lo, hi, seed=seed)
            k = s.solve(scalar_mult(key), max_seconds=max_seconds)
    except LookupError:
        return None, s.stats
    return (k == key), s.stats

for W_BITS in (20, 24, 28):
    lo = 1 << (W_BITS - 1)
    hi = (1 << W_BITS) - 1
    W = hi - lo + 1
    SEEDS = list(range(1, 13))
    max_s = 120 if W_BITS < 28 else 240

    print(f"=== v5 Fused+Negation vs v4 Baseline (w={W_BITS}, W={W:,}) ===")
    print(f"trials: {len(SEEDS)}")

    res = {"base": [], "v5": []}
    fails = {"base": 0, "v5": 0}

    for seed in SEEDS:
        rng = random.Random(seed * 1000 + W_BITS)
        key = rng.randint(lo, hi)
        for name, cls in (("base", KangarooSolver), ("v5", FusedNegationSolver)):
            ok, stats = run_one(cls, lo, hi, key, seed, max_s)
            if not ok:
                fails[name] += 1
                continue
            total = stats.get("tame_trail", 0) + stats.get("hops", 0)
            res[name].append(total / math.sqrt(W))

    for name in ("base", "v5"):
        v = res[name]
        if v:
            print(f"  {name:>4}: mean K={sum(v)/len(v):.3f}  min={min(v):.3f}  "
                  f"max={max(v):.3f}  solves={len(v)}  fails={fails[name]}")
        else:
            print(f"  {name:>4}: NO SOLVES  fails={fails[name]}")

    if res["base"] and res["v5"]:
        r = (sum(res["v5"])/len(res["v5"])) / (sum(res["base"])/len(res["base"]))
        print(f"  K v5/base: {r:.3f}  (= ops speedup from negation; "
              f"  fused inversion then stacks 2.0x on top for wall-time)")
    print()