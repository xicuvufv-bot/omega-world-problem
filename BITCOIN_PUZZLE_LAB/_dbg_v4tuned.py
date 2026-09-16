import random, math, time, sys
sys.path.insert(0, "."); sys.path.insert(0, "SOLVER_LAB/candidate")
from algorithms.curve import scalar_mult, to_affine, jac_add_affine, point_equal_jac
from v5_fused_negation import FusedNegationSolver
from solvers.v4_kangaroo import KangarooSolver, JUMP_FRACS

class V4Tuned(KangarooSolver):
    def __init__(self, lo, hi, max_seconds=60.0, seed=1):
        self.lo, self.hi, self.W = lo, hi, hi-lo
        self.max_seconds, self.seed = max_seconds, seed
        self.rng = random.Random(seed)
        self.jump_weff = max(1, self.W//2)
        mean = math.sqrt(self.jump_weff+1)
        self.jumps = [int(max(1, mean*f)) for f in JUMP_FRACS]
        self.jump_aff = [to_affine(scalar_mult(j)) for j in self.jumps]
        self.stats = {}

def K_one(cls, wb, seed):
    lo = 1 << (wb-1); hi = (1<<wb)-1
    rng = random.Random(seed*1000+wb); key = rng.randint(lo,hi)
    target = scalar_mult(key); t0 = time.perf_counter()
    s = cls(lo, hi, seed=seed)
    k = s.solve(target)
    wd = time.perf_counter()-t0
    assert k == key and point_equal_jac(scalar_mult(k), target)
    K = (s.stats.get("tame_trail",0)+s.stats.get("hops",0))/math.sqrt(float(1<<(wb-1)))
    return K, s.stats.get("passes",0)

for wb in (20, 24):
    for name, cls in (("v4", KangarooSolver), ("v4tuned", V4Tuned)):
        Ks, ps = [], []
        for seed in range(1, 13):
            try:
                K, p = K_one(cls, wb, seed); Ks.append(K); ps.append(p)
            except LookupError:
                pass
        if Ks:
            print(f"w={wb} {name:>8}: meanK={sum(Ks)/len(Ks):6.3f} min={min(Ks):6.3f} max={max(Ks):6.3f} solves={len(Ks)}/12 meanpass={sum(ps)/len(ps):.2f}")
