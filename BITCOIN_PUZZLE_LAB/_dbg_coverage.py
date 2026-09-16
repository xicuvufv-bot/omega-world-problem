import random, math, sys
sys.path.insert(0, "."); sys.path.insert(0, "SOLVER_LAB/candidate")
from algorithms.curve import scalar_mult, to_affine, jac_add_affine, N
from v6_glv_negation import GlvFusedNegationSolver, glv_canon_aff

wb, seed = 24, 5
lo = 1 << (wb-1); hi = (1<<wb)-1
rng = random.Random(seed*1000+wb)
key = rng.randint(lo,hi); target = scalar_mult(key)
s = GlvFusedNegationSolver(lo, hi, seed=seed)
theory = math.sqrt((s.store_weff+1)*math.pi/2)
tame_steps = max(64, int(4*theory)+2)
pass_steps = max(64, int(6*theory)+2)
print("W", s.W, "W/6", s.store_weff, "jump_weff", s.jump_weff, "trail", tame_steps, "passsteps", pass_steps, "key", key)

tame = scalar_mult(lo); tame_d = 0
tame_off = {}; hits_self = 0
for _ in range(tame_steps):
    tame, tame_d, caff, old = s._step(tame, tame_d)
    if caff in tame_off: hits_self += 1
    tame_off[caff] = lo + old
print("distinct trail classes:", len(tame_off), "of", tame_steps, "steps; self-repeats:", hits_self)

# wild passes
for p in range(1, 4):
    rng = random.Random(seed*1000+p)
    d0 = rng.randrange(0, int(2*math.sqrt((s.W+1)*math.pi/2))+1)
    if d0 == 0: wild, wild_d = target, 0
    else: wild = jac_add_affine(target, *to_affine(scalar_mult(d0))); wild_d = d0
    seen = {}; trail_hits = 0; distinct = 0
    for _ in range(pass_steps):
        wild, wild_d, caff, old = s._step(wild, wild_d)
        if caff not in seen:
            seen[caff] = 1; distinct += 1
        if caff in tame_off:
            trail_hits += 1
    print(f"pass {p}: distinct classes visited {distinct}/{pass_steps}, trail class hits {trail_hits}")
