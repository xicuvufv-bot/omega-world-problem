import random, time, math
import sys
sys.path.insert(0, ".")
from algorithms.curve import scalar_mult, to_affine, jac_add_affine, point_equal_jac, N
from SOLVER_LAB.candidate.v6_glv_negation import GlvFusedNegationSolver, glv_canon_aff, lam_pow

wb, seed = 10, 1
lo = 1 << (wb-1); hi = (1 << wb) - 1
rng = random.Random(seed*1000 + wb)
key = rng.randint(lo, hi)
target = scalar_mult(key)

s = GlvFusedNegationSolver(lo, hi, seed=seed)
W = s.W; Weff = s.Weff
theory = math.sqrt((Weff+1)*math.pi/2)
tame_steps = max(64, int(4*theory)+2)
pass_steps = max(64, int(6*theory)+2)
theory_w = math.sqrt((W+1)*math.pi/2)
print("W", W, "Weff", Weff, "tame_steps", tame_steps, "pass_steps", pass_steps, "theory_w", round(theory_w,1))

C_aff, i0t, flip0t = glv_canon_aff(to_affine(scalar_mult(lo)))
c_t = (lam_pow(i0t)*flip0t*lo) % N
tame_off = {C_aff: c_t}
for _ in range(tame_steps):
    C_next, i, flip, j = s._step(C_aff)
    c_t = (lam_pow(i)*flip*((c_t+j)%N)) % N
    C_aff = C_next
    tame_off[C_aff] = c_t
print("tame states:", len(tame_off), "key:", key)

hits = 0
for p in range(1, 8):
    rng = random.Random(seed*1000 + p)
    d0 = rng.randrange(0, int(2*theory_w)+1)
    if d0 == 0:
        C_aff, i0, flip0 = glv_canon_aff(to_affine(target)); sgn, rho = flip0, i0; off = 0
    else:
        raw = jac_add_affine(target, *to_affine(scalar_mult(d0)))
        C_aff, i0, flip0 = glv_canon_aff(to_affine(raw)); sgn, rho = flip0, i0
        off = (lam_pow(i0)*flip0*d0) % N
    for step in range(pass_steps):
        C_next, i, flip, j = s._step(C_aff)
        c_t = tame_off.get(C_aff)
        if c_t is not None:
            hits += 1
            good = False
            for k in s._candidates(c_t, sgn, rho, off):
                if 0 <= k - lo <= W and point_equal_jac(scalar_mult(k), target):
                    print(f"  VERIFIED k=%x" % k); good = True; break
            if p <= 2 and step < 120:
                print(f"pass {p} step {step} COLLISION: c_t={c_t} sgn={sgn} rho={rho} off={off} win={good}")
        sgn = sgn*flip; rho = (rho+i)%3
        off = (lam_pow(i)*flip*((off+j)%N)) % N
        C_aff = C_next
    if p <= 2:
        print(f"pass {p} done, hits so far {hits}, final state={C_aff}")
print("total canonical-state overlaps in 7 passes:", hits)
