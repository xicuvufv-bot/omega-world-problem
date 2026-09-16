"""CPU ceiling validation: v5 solve time at w=32..34.

Theory says kangaroo needs ~ sqrt(pi*W/4) ops/side after the negation map,
so at w=34: sqrt(pi/4 * 2^34) ~= 130k hops. In pure CPython at ~7-9k
hops/s that is ~15-20 s per lucky solve but the stop tail means wall time
grows. This confirms the practical CPU ceiling (~32-34 bits) for a serial
Python kangaroo.
"""
import os, sys, math, random, time
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

LAB = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, LAB)
os.chdir(LAB)

from algorithms.curve import scalar_mult
import importlib.util
_spec = importlib.util.spec_from_file_location(
    "v5_fused_negation", os.path.join(LAB, "SOLVER_LAB", "candidate", "v5_fused_negation.py"))
_mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_mod)
FusedNegationSolver = _mod.FusedNegationSolver

print("=== CPU ceiling: v5 (fused+neg) at w=32..34 ===")
for W_BITS in (30, 31, 32, 33, 34):
    lo = 1 << (W_BITS - 1)
    hi = (1 << W_BITS) - 1
    key = lo + (hi - lo) // 2  # midpoint, not the most adversarial but informative
    max_s = 240
    t0 = time.monotonic()
    s = FusedNegationSolver(lo, hi, seed=1)
    try:
        k = s.solve(scalar_mult(key), max_seconds=max_s)
        ok = (k == key)
        dt = time.monotonic() - t0
        theory = math.sqrt((s.Weff + 1) * math.pi / 2)
        print(f"  w={W_BITS:2d} ok={ok}  hops={s.stats.get('hops',0):>8}  "
              f"passes={s.stats.get('passes',0):>4}  wall={dt:7.2f}s  "
              f"K={ (s.stats.get('tame_trail',0)+s.stats.get('hops',0))/math.sqrt(hi-lo+1):.2f}  "
              f"theory_ops~{theory:.0f}")
    except LookupError:
        dt = time.monotonic() - t0
        print(f"  w={W_BITS:2d} TIMEOUT after {dt:.1f}s  hops={s.stats.get('hops',0)}")