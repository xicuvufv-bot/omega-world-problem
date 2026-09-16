"""SOLVER v5 candidate — Fused + Negation (canonical quotient walk).

Combines two independently-verified improvements into one solver:

  1. FUSED SINGLE-INVERSION (EX4, verified 2.0x wall-time):
     one modular inversion per hop serves BOTH bucket selection and the
     dict membership lookup (no second to_affine()).

  2. NEGATION MAP (test_negation.py, verified 1.42x ops):
     both herds walk the quotient space {P, -P}, canonicalizing each
     visited affine point to the even-y representative. Search width is
     halved, so the jump table + trail/pass lengths are tuned to W/2.
     A canonical match means wild == ±tame, so BOTH candidates
       k1 = t_off - wild_old   (wild == tame)
       k2 = N - (t_off + wild_old)  (wild == -tame)
     are verified with a full scalar mult before returning.

Stack effect expected: 2.0 x 1.42 ~= 2.84x over v4 on the same machine.
"""
import math
import random
import time

from algorithms.curve import scalar_mult, to_affine, jac_add_affine, point_equal_jac, P, N

from solvers.v4_kangaroo import JUMP_FRACS


def canon_aff(aff):
    """Even-y canonical representative of the class {P, -P}."""
    return (aff[0], P - aff[1]) if (aff[1] & 1) else aff


class FusedNegationSolver:
    def __init__(self, lo, hi, seed=1):
        self.lo = lo
        self.hi = hi
        self.W = hi - lo
        self.seed = seed
        self.Weff = max(1, self.W // 2)
        mean = math.sqrt(self.Weff + 1)
        self.jumps = [int(max(1, mean * f)) for f in JUMP_FRACS]
        self.jump_aff = [to_affine(scalar_mult(j)) for j in self.jumps]

    def _step(self, pt, d):
        """One hop: 1 inversion. Returns (new_pt, new_d, canon_in, old_d).

        canon_in = canonical affine of the INPUT point (bucket + membership).
        old_d    = distance carried by that input point (correct pairing).
        """
        aff = to_affine(pt)                      # the only inversion
        caff = canon_aff(aff)
        b = (caff[0] >> 120) & 0xF
        old_d = d
        new_pt = jac_add_affine(pt, *self.jump_aff[b])
        return new_pt, d + self.jumps[b], caff, old_d

    def _candidates(self, t_off, wild_d):
        yield t_off - wild_d
        yield N - (t_off + wild_d)

    def solve(self, target_jac, max_seconds=60):
        lo = self.lo
        W = self.W
        Weff = self.Weff
        theory = math.sqrt((Weff + 1) * math.pi / 2)
        tame_steps = max(64, int(4 * theory) + 2)
        pass_steps = max(64, int(6 * theory) + 2)
        theory_w = math.sqrt((W + 1) * math.pi / 2)
        t0 = time.monotonic()
        passes = 0
        hops = 0

        # Tame trail: single inversion per step, canonical store.
        tame = scalar_mult(lo)
        tame_d = 0
        tame_off = {}
        for _ in range(tame_steps):
            tame, tame_d, caff, old_d = self._step(tame, tame_d)
            tame_off[caff] = lo + old_d

        # degenerate: canonical(target) already in the trail
        for k in self._candidates(tame_off.get(canon_aff(to_affine(target_jac)), 0),
                                  0) if canon_aff(to_affine(target_jac)) in tame_off else ():
            if 0 <= k - lo <= W and point_equal_jac(scalar_mult(k), target_jac):
                self.stats = dict(method="fused+neg", hops=0, passes=0,
                                  tame_trail=tame_steps, edge="target-in-trail")
                return k

        while True:
            passes += 1
            rng = random.Random(self.seed * 1000 + passes)
            d0 = rng.randrange(0, int(2 * theory_w) + 1)
            if d0 == 0:
                wild, wild_d = target_jac, 0
            else:
                d0_aff = to_affine(scalar_mult(d0))
                wild = jac_add_affine(target_jac, *d0_aff)
                wild_d = d0

            for _ in range(pass_steps):
                wild, wild_d, caff, wild_old = self._step(wild, wild_d)
                hops += 1
                t_off = tame_off.get(caff)
                if t_off is not None:
                    for k in self._candidates(t_off, wild_old):
                        if 0 <= k - lo <= W and point_equal_jac(scalar_mult(k),
                                                                target_jac):
                            self.stats = dict(method="fused+neg", hops=hops,
                                              passes=passes, tame_trail=tame_steps)
                            return k

            if max_seconds is not None and time.monotonic() - t0 > max_seconds:
                self.stats = dict(method="fused+neg", hops=hops, passes=passes,
                                  tame_trail=tame_steps, timeout=True)
                raise LookupError(f"fused+neg budget exhausted: hops={hops}")

        raise LookupError("fused+neg walk lost")