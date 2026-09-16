import random
import sys
import time

sys.path.insert(0, ".")
sys.path.insert(0, "SOLVER_LAB/candidate")

from algorithms.curve import scalar_mult, point_equal_jac
from v6_glv_negation import GlvFusedNegationSolver, glv_canon_aff

# sanity: canonicalization is idempotent and class-consistent
x = 0x5A
y = 2
(cx, cy), i1, f1 = glv_canon_aff((x, y))
(cx2, cy2), i2, f2 = glv_canon_aff((201487, 12345))
print("glv_canon_aff basics:", ((cx, cy), i1, f1), ((cx2, cy2), i2, f2), flush=True)

for wb in (10, 12, 14, 16):
    lo = 1 << (wb - 1)
    hi = (1 << wb) - 1
    t0 = time.perf_counter()
    for seed in range(1, 3):
        rng = random.Random(seed * 1000 + wb)
        key = rng.randint(lo, hi)
        target = scalar_mult(key)
        s = GlvFusedNegationSolver(lo, hi, seed=seed)
        try:
            k = s.solve(target, max_seconds=60)
        except LookupError:
            print(f"w={wb} seed={seed} TIMEOUT implements", flush=True)
            continue
        h = s.stats.get("hops")
        good = (k == key and point_equal_jac(scalar_mult(k), target))
        print(f"w={wb} seed={seed} k={k:x} good={good} hops={h} "
              f"passes={s.stats.get('passes')} dt={time.perf_counter()-t0:.2f}s",
              flush=True)
    print(f"w={wb} block done in {time.perf_counter()-t0:.2f}s", flush=True)