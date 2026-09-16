import random, math, sys
sys.path.insert(0, "."); sys.path.insert(0, "SOLVER_LAB/candidate")
from algorithms.curve import scalar_mult, to_affine, jac_add_affine, point_equal_jac, N
from v5_fused_negation import FusedNegationSolver, canon_aff

# instrument v5: report whether recovery used k1 (raw equality) or k2 (negation)
hits_k1 = hits_k2 = 0
for wb in (20, 24):
    lo = 1 << (wb-1); hi = (1<<wb)-1
    for seed in range(1, 9):
        rng = random.Random(seed*1000+wb)
        key = rng.randint(lo,hi); target = scalar_mult(key)
        s = FusedNegationSolver(lo, hi, seed=seed)
        theory = math.sqrt((s.Weff+1)*math.pi/2)
        tame_steps = max(64, int(4*theory)+2); pass_steps = max(64, int(6*theory)+2)
        theory_w = math.sqrt((s.W+1)*math.pi/2)
        tame = scalar_mult(lo); tame_d = 0; tame_off = {}
        for _ in range(tame_steps):
            tame, tame_d, caff, old = s._step(tame, tame_d); tame_off[caff] = lo+old
        found = None
        for p in range(1, 2000):
            rng = random.Random(seed*1000+p)
            d0 = rng.randrange(0, int(2*theory_w)+1)
            if d0 == 0: wild, wild_d = target, 0
            else: wild = jac_add_affine(target, *to_affine(scalar_mult(d0))); wild_d = d0
            for _ in range(pass_steps):
                wild, wild_d, caff, wild_old = s._step(wild, wild_d)
                t_off = tame_off.get(caff)
                if t_off is not None:
                    for cand_idx, k in enumerate(s._candidates(t_off, wild_old)):
                        if 0 <= k - lo <= s.W and point_equal_jac(scalar_mult(k), target):
                            found = (cand_idx, k); break
                    if found: break
            if found: break
        if found and found[1] == key:
            if found[0] == 0: hits_k1 += 1
            else: hits_k2 += 1
print(f"v5 recovery candidates used: k1(raw-equal)={hits_k1}, k2(negation)={hits_k2}")
