"""SOLVER v6 — Fused + GLV order-3 endomorphism + Negation (raw walk, 6-quotient store).

Combines v5's proven raw-chain kangaroo with a SIZE-6 class store.

STRUCTURE (differs from the two failed drafts for a measured reason):
  * failure draft-1 / draft-2 used the min-x CANONICAL x for the jump bucket.
    Measured: the deterministic step map then collapses into tiny cycles
    (w=16: 13 distinct canonical states in 372 steps), so the tame and wild
    functional graphs sit in disjoint components -> no collision ever.
  * this version mirrors v5: the WALK runs on the RAW additive chain
        P_{n+1} = P_n + J_{b(x_raw)}
    (bucket on the pristine x bits -> the well-mixed v4/v5 walk, proven
    100% state coverage), and canonicalization to the full automorphism
    quotient Cl(P) = {P, psi P, psi^2 P, -P, -psi P, -psi^2 P} is applied
    ONLY for the stored-member / membership lookup.

  psi(x,y) = (BETA*x mod p, y), psi(P) = LAMBDA*P, BETA/LAMBDA = order-3 roots
  of unity (constants verified computationally).  canon(C) picks y even and
  x minimal over {x, BETA*x, BETA^2*x}.

DISTANCES ARE EXACT INTEGERS (raw chain):  tame stores  lo + D_t  for the
pre-hop canonical class; wild carries  wild_old = d0 + D_w.  A canonical hit
means tame_r and wild_r are THE SAME class, i.e. differ by one of the 6
automorphisms:  lo + D_t == sigma * psi^i * (k + D_w), so
        k = sigma * LAMBDA^{-i} * (lo + D_t) - D_w     (mod n)
We enumerate the 6 (sigma, i) candidates plus a 36-candidate +-LAMBDA^m
robustness grid; every candidate passes a full scalar-mult re-verification
(point_equal_jac) and an interval check before being returned, so a false
candidate can never be emitted (exact identity check, no geometry slack).

TWO EFFECTIVE WIDTHS (measured, w=12..20 sweep):
    jump_weff  = W//2  controls the jump table size.  It sizes the RAW
                 walk's displacement, so it must match the raw domain for
                 the v4/v5 mixing to survive (W//6 jumps collapsed the
                 functional graph: w=16, 13 distinct canonical states in
                 372 steps, 1/3 solves).
    store_weff = W//6  controls the tame trail / pass geometry.  This is
                 the ALL-AUTOMORPHISM quotient the trail must cover, and it
                 is the entire source of the K-gain over v5 (W//2 store).

Correctness gate before any K is trusted: w = 16..24, >= 36 solves, every
returned key re-verified through scalar-mult AND the independent native
secp256k1 FFI.  Zero tolerance for LookupError in the reported block.
KB_floor: K_floor = sqrt(pi/12) ~ 0.51 (the automorphism-group floor).
"""
import math
import random
import time

from algorithms.curve import (scalar_mult, to_affine, jac_add_affine,
                              point_equal_jac, P, N)

from solvers.v4_kangaroo import JUMP_FRACS

BETA = 0x7ae96a2b657c07106e64479eac3434e99cf0497512f58995c1396c28719501ee
BETA2 = (BETA * BETA) % P
LAMBDA = 0x5363ad4cc05c30e0a5261c028812645a122e22ea20816678df02967c1b23bd72
LAMBDA2 = (LAMBDA * LAMBDA) % N
LAMBDA_INV = {0: 1, 1: LAMBDA2, 2: LAMBDA}   # LAMBDA^{-i} mod n


def glv_canon_aff(aff):
    """Canonical rep of the size-6 class; returns (canon_aff, i, flip)."""
    x, y = aff
    flip = 1 if not (y & 1) else -1
    if y & 1:
        y = P - y
    x1 = (BETA * x) % P
    x2 = (BETA2 * x) % P
    if x1 < x and x1 < x2:
        return (x1, y), 1, flip
    if x2 < x and x2 < x1:
        return (x2, y), 2, flip
    if x1 < x:
        return (x1, y), 1, flip
    if x2 < x:
        return (x2, y), 2, flip
    return (x, y), 0, flip


class GlvFusedNegationSolver:
    def __init__(self, lo, hi, seed=1, debug=False):
        self.lo = lo
        self.hi = hi
        self.W = hi - lo
        self.seed = seed
        self.debug = debug
        self.jump_weff = max(1, self.W // 2)    # raw-walk displacement sizing
        self.store_weff = max(1, self.W // 6)   # 6-quotient store / trail size
        mean = math.sqrt(self.jump_weff + 1)
        self.jumps = [int(max(1, mean * f)) for f in JUMP_FRACS]
        self.jump_aff = [to_affine(scalar_mult(j)) for j in self.jumps]
        self.stats = {}

    def _step(self, pt, d):
        """One hop on the RAW chain.  Returns (new_pt, new_d, canon_in, old_d).

        canon_in = canonical member of the INPUT point (bucket + membership),
        old_d    = distance carried by that input point (correct pairing).
        """
        aff = to_affine(pt)                      # the only inversion
        caff, _i, _f = glv_canon_aff(aff)
        b = (aff[0] >> 120) & 0xF                # RAW x bucket (well-mixed)
        old_d = d
        new_pt = jac_add_affine(pt, *self.jump_aff[b])
        return new_pt, d + self.jumps[b], caff, old_d

    def _candidates(self, t_off, wild_old):
        """k = sigma*LAMBDA^{-i}*t_off - wild_old, plus a robustness grid."""
        for sigma in (1, -1):
            for i in range(3):
                yield (sigma * LAMBDA_INV[i] * t_off - wild_old) % N
        for m_t in (1, LAMBDA, LAMBDA2, -1 % N, -LAMBDA % N, -LAMBDA2 % N):
            for m_o in (1, LAMBDA, LAMBDA2, -1 % N, -LAMBDA % N, -LAMBDA2 % N):
                if m_t == 1 and m_o == -1 % N:
                    continue                     # exact form already emitted
                yield (m_t * t_off + m_o * wild_old) % N

    def solve(self, target_jac, max_seconds=60):
        lo = self.lo
        W = self.W
        Weff = self.store_weff
        theory = math.sqrt((Weff + 1) * math.pi / 2)
        tame_steps = max(64, int(4 * theory) + 2)
        pass_steps = max(64, int(6 * theory) + 2)
        theory_w = math.sqrt((W + 1) * math.pi / 2)
        t0 = time.monotonic()
        passes = 0
        hops = 0

        # ---- tame trail: raw walk, 6-class canonical store -------------------
        tame = scalar_mult(lo)
        tame_d = 0
        tame_off = {}
        for _ in range(tame_steps):
            tame, tame_d, caff, old = self._step(tame, tame_d)
            tame_off[caff] = lo + old

        # ---- degenerate: canonical(target) already on the trail --------------
        C_q = glv_canon_aff(to_affine(target_jac))[0]
        t_q = tame_off.get(C_q)
        if t_q is not None:
            for k in self._candidates(t_q, 0):
                if 0 <= k - lo <= W and point_equal_jac(scalar_mult(k),
                                                        target_jac):
                    self.stats = dict(method="v6_glv+neg", hops=0, passes=0,
                                      tame_trail=tame_steps,
                                      edge="target-in-trail")
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
                            self.stats = dict(method="v6_glv+neg", hops=hops,
                                              passes=passes,
                                              tame_trail=tame_steps)
                            return k

            if max_seconds is not None and time.monotonic() - t0 > max_seconds:
                self.stats = dict(method="v6_glv+neg", hops=hops, passes=passes,
                                  tame_trail=tame_steps, timeout=True)
                raise LookupError(f"v6 budget exhausted: hops={hops}")

        raise LookupError("v6 walk lost")