import random, time, math, sys
sys.path.insert(0, ".")
from algorithms.curve import scalar_mult, to_affine, jac_add_affine, point_equal_jac, N
from SOLVER_LAB.candidate.v6_glv_negation import GlvFusedNegationSolver, glv_canon_aff, lam_pow
from SOLVER_LAB.candidate.v5_fused_negation import FusedNegationSolver, canon_aff

def trail_stats(slv, cls):
    W = slv.W; Weff = slv.Weff
    theory = math.sqrt((Weff+1)*math.pi/2)
    tame_steps = max(64, int(4*theory)+2)
    C_aff, i0t, flip0t = cls(to_affine(scalar_mult(slv.lo)))
    seen = {C_aff}
    for _ in range(tame_steps):
        C_next = slv._step(C_aff)[0] if cls is glv_canon_aff else slv._step(C_aff)[0]
        # generic: _step returns (C_next, ...) or (new_pt, ...) ; canonicalize for counting
        if cls is glv_canon_aff:
            C_aff = C_next
        else:
            aff5 = cls(to_affine(C_next))
            C_aff = (C_next[0] % 1 if False else None) or C_next  # keep raw point chain
            # count canonical distinct
            seen.add(aff5)
        seen.add(C_aff)
    return len(seen), tame_steps

for wb in (10, 12, 14, 16, 20):
    lo = 1 << (wb-1); hi = (1 << wb)-1
    s6 = GlvFusedNegationSolver(lo, hi, seed=1)
    s5 = FusedNegationSolver(lo, hi, seed=1)
    # v6 distinct canonical states
    theory6 = math.sqrt((s6.Weff+1)*math.pi/2)
    ts6 = max(64, int(4*theory6)+2)
    C, i0, f0 = glv_canon_aff(to_affine(scalar_mult(lo)))
    seen6 = {C}
    for _ in range(ts6):
        Cnext, i, fl, j = s6._step(C); seen6.add(Cnext); C = Cnext
    # v5 distinct canonical states (even-y canon of raw-walk points)
    theory5 = math.sqrt((s5.Weff+1)*math.pi/2)
    ts5 = max(64, int(4*theory5)+2)
    pt = scalar_mult(lo); d = 0
    seen5 = set()
    for _ in range(ts5):
        pt, d, caff, old = s5._step(pt, d); seen5.add(caff)
    print(f"w={wb}: v6 trail {len(seen6)}/{ts6} distinct canon; v5 trail {len(seen5)}/{ts5} distinct canon")
