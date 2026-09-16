"""Solver v3 — Baby-step Giant-step (BSGS) for an interval ECDLP.

Variants: given the public key Q = kG with k in [lo, lo+W], set m = ceil(sqrt W).
Baby steps: store the m points (lo + j)G for j in [0, m).
Giant steps: for i in [0, m) check Q - i*m*G against the baby table;
on a match, k = lo + j + i*m.

Takes O(m) time *and* memory and is always exact (verified by re-deriving
kG == Q before returning).
"""

import math

from algorithms.curve import (scalar_mult, to_affine, jac_add_affine,
                              negative_affine, point_equal_jac, Gx, Gy)


def solve_bsgs(target_jac, lo: int, hi: int, m: int = None):
    """Return (k, stats) for Q = kG, k in [lo, hi]; (None, stats) if not found."""

    W = hi - lo + 1
    if m is None:
        m = math.isqrt(W) + 1
    m = max(1, m)

    # --- baby steps: table {(x, y): j} for (lo + j)*G -------------------
    baby = {}
    P = scalar_mult(lo)
    for j in range(m):
        aff = to_affine(P)
        key = (aff[0], aff[1])
        if key not in baby:  # first visit wins (deterministic structure)
            baby[key] = j
        P = jac_add_affine(P, Gx, Gy)
    baby_size = len(baby)

    # --- giant steps: R_i = Q - i*m*G -----------------------------------
    step_aff = to_affine(scalar_mult(m))
    neg = negative_affine(*step_aff)
    R = target_jac
    giant = 0
    for i in range(m):
        affR = to_affine(R)
        if affR is not None:
            giant += 1
            j = baby.get((affR[0], affR[1]))
            if j is not None:
                k = lo + j + i * m
                if lo <= k <= hi and point_equal_jac(scalar_mult(k), target_jac):
                    stats = dict(m=m, baby_size=baby_size, giant_steps=giant,
                                 memory_points=baby_size, method="bsgs")
                    return k, stats
        R = jac_add_affine(R, *neg)
    stats = dict(m=m, baby_size=baby_size, giant_steps=giant,
                 memory_points=baby_size, method="bsgs")
    return None, stats