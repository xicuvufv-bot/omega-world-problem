"""Wall-time: v5 (fused+negation) vs v4, same keys/seeds, w=24.

Claims to substantiate:
  * negation map: ~1.3x fewer ops (bench_v5_vs_v4.py)
  * fused inversion: ~2.0x per-op wall-time (EX4)
  * stack verdict measured directly here: wall_v4 / wall_v5
"""
import os, sys, math, random, time
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

LAB = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, LAB)
os.chdir(LAB)

from algorithms.curve import scalar_mult
from solvers.v4_kangaroo import KangarooSolver
import importlib.util
_spec = importlib.util.spec_from_file_location(
    "v5_fused_negation", os.path.join(LAB, "SOLVER_LAB", "candidate", "v5_fused_negation.py"))
_mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_mod)
FusedNegationSolver = _mod.FusedNegationSolver

W_BITS = 24
lo = 1 << (W_BITS - 1)
hi = (1 << W_BITS) - 1
W = hi - lo + 1
SEEDS = list(range(1, 9))
max_s = 180

def timed(cls, lo, hi, key, seed):
    t0 = time.monotonic()
    s = cls(lo, hi, max_seconds=max_s, seed=seed) if cls is KangarooSolver \
        else cls(lo, hi, seed=seed)
    try:
        k = s.solve(scalar_mult(key)) if cls is KangarooSolver \
            else s.solve(scalar_mult(key), max_seconds=max_s)
    except LookupError:
        return None, None, time.monotonic() - t0, s.stats
    return (k == key), s.stats.get("hops", 0), time.monotonic() - t0, s.stats

print(f"=== Wall-time stack: v4 vs v5 (w={W_BITS}, W={W:,}, trials={len(SEEDS)}) ===")
rows = []
for seed in SEEDS:
    rng = random.Random(seed * 1000 + W_BITS)
    key = rng.randint(lo, hi)
    okb, hb, wb, sb = timed(KangarooSolver, lo, hi, key, seed)
    okv, hv, wv, sv = timed(FusedNegationSolver, lo, hi, key, seed)
    speedup = wb / wv if (okb and okv and wv > 0) else float("nan")
    rows.append((okb and okv, hb, hv, wb, wv, speedup))
    print(f"  seed={seed:2d} ok={okb and okv}  v4 {wb:7.3f}s/{hb:6d}h  "
          f"v5 {wv:7.3f}s/{hv:6d}h  speedup={speedup:.2f}x")

oks = [r for r in rows if r[0] and r[5] == r[5]]
sp = [r[5] for r in oks]
if sp:
    print(f"\nAll solved: {len(oks)}/{len(rows)}")
    print(f"Wall speedup v4/v5: avg={sum(sp)/len(sp):.2f}x  "
          f"med={sorted(sp)[len(sp)//2]:.2f}x  min={min(sp):.2f}x  max={max(sp):.2f}x")
    hops_base = sum(r[1] or 0 for r in oks)
    hops_v5 = sum(r[2] or 0 for r in oks)
    print(f"Total ops: v4={hops_base}  v5={hops_v5}  ratio={hops_v5/hops_base:.3f}")
    print("(wall speedup = ops reduction x per-op fused inversion saving)")