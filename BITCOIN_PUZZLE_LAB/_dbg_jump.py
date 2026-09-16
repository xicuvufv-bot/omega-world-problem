import random, time, math, sys
sys.path.insert(0, ".")
sys.path.insert(0, "SOLVER_LAB/candidate")
from algorithms.curve import scalar_mult, to_affine, jac_add_affine, point_equal_jac, N
from v6_glv_negation import GlvFusedNegationSolver, glv_canon_aff, LAMBDA, LAMBDA2
from solvers.v4_kangaroo import JUMP_FRACS

class S(GlvFusedNegationSolver):
    def __init__(self, lo, hi, seed=1, jump_weff=None, **kw):
        super().__init__(lo, hi, seed=seed, **kw)
        if jump_weff is not None:
            mean = math.sqrt(jump_weff + 1)
            self.jumps = [int(max(1, mean*f)) for f in JUMP_FRACS]
            self.jump_aff = [to_affine(scalar_mult(j)) for j in self.jumps]

def solve_one(wb, seed, jw):
    lo = 1 << (wb-1); hi = (1<<wb)-1
    rng = random.Random(seed*1000+wb)
    key = rng.randint(lo,hi); target = scalar_mult(key)
    s = S(lo, hi, seed=seed, jump_weff=jw)
    t0 = time.perf_counter()
    try:
        k = s.solve(target, max_seconds=45)
        dt = time.perf_counter()-t0
        ok = (k==key and point_equal_jac(scalar_mult(k), target))
        return ok, dt, s.stats.get("hops",0), s.stats.get("passes",0)
    except LookupError:
        return False, time.perf_counter()-t0, -1, -1

for jw_label, jw in (("W", None), ("W/2", None), ("W/4", None)):
    # express explicitly: None means default W//6; compute W/2, W for this width
    pass

for wb, seeds in ((12,[1,2,3,4]),(16,[1,2,3]),(20,[1])):
    W = (1<<wb)-1 - (1<<(wb-1))
    for jw_label, jw in (("W/6", max(1,W//6)), ("W/4", max(1,W//4)), ("W/2", max(1,W//2)), ("W", W)):
        res = [solve_one(wb, sd, jw) for sd in seeds]
        oks = [r[0] for r in res]
        dts = [r[1] for r in res]
        hops = [r[2] for r in res]
        print(f"w={wb} jw={jw_label:>4} solves={sum(oks)}/{len(seeds)} dts={['%.2f'%d for d in dts]} hops={hops}")
