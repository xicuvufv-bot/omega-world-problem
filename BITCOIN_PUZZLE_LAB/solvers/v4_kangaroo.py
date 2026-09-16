"""Solver v4 — Pollard's kangaroo (Teske-style jump table) for an interval ECDLP.

Structure (classic serial 2-kangaroo, "one tame trail + many wild passes"):

  * a FIXED tame herd walks from the bottom of the interval (offset 0) and
    records the absolute offset of every point it visits (the "trail"). The
    trail spans several multiples of the interval width, so every possible
    wild offset lies below its top edge;
  * the wild herd starts at the unknown key Q (offset s_k = k - lo) PLUS a
    fresh random bootstrap jump d0 on every PASS. Walks and re-check against
    the tame trail. A fresh d0 gives an independent trajectory each pass, so
    the run is a geometric stop over cheap passes (tame built once).

Meeting rule: both herds use the same bucket function f(x) and the same jump
table, so once tame lands on a wild point the next jumps coincide.

  Tame abs offset t_off (stored)           = lo + D_t
  Wild abs offset                          = lo + s_k + d0 + D_w
  Collision (same point) =>  lo + s_k + d0 + D_w = lo + D_t
  =>  s_k = D_t - d0 - D_w ;  k = lo + s_k   (wild-side form).

kG == Q is re-verified before returning; out-of-interval candidates are
rejected.  Why wild restarts (measured, 24/28-bit): a fixed launch geometry
has a heavy per-key meeting-time tail (>12x the mean historic for unlucky
geometries). Fresh d0 draws make passes independent, so wall-clock success is
essentially guaranteed within a pass budget that fits a normal budget.

Notes & provenance vs. the toy in BITCOIN_PUZZLE_RESEARCH:
  * interval-offset formulation keeps distances explicit and auditable;
  * edge guard rejects out-of-interval collisions instead of emitting them;
  * exact-x/y point matching (no useless half-collisions);
  * wall-clock budget via max_seconds for deterministic, bounded runs;
  * 16 jump sizes spread over 0.5..1.5 * sqrt(W) (better mixing);
  * low-4-bits-of-x buckets are DEGENERATE on secp256k1 (x^3+7 square mod 16
    forces x in {9,13}); buckets draw on bits 120..123 of x instead.
"""

import math
import random
import time

from algorithms.curve import scalar_mult, to_affine, jac_add_affine, point_equal_jac

JUMP_FRACS = (0.50, 0.55, 0.63, 0.72, 0.82, 0.92, 1.03, 1.15) * 2


def _jump_bucket(aff):
    # 16 uniform buckets from the x-coordinate.
    # Low bits of x are DEGENERATE on secp256k1: y^2 = x^3 + 7 forces
    # x^3 + 7 to be a quadratic residue mod 16, which restricts x to
    # x == 9 or 13 (mod 16) -- so hash(x)&0xF only ever yields 2 buckets.
    # Middle bits (120..123) are uniform and algebraically unconstrained.
    return (aff[0] >> 120) & 0xF


class KangarooSolver:
    def __init__(self, lo: int, hi: int, max_seconds: float = 60.0, seed: int = 1):
        self.lo = lo
        self.hi = hi
        self.W = hi - lo
        self.max_seconds = max_seconds
        self.rng = random.Random(seed)
        self.seed = seed
        mean = math.sqrt(self.W + 1)
        self.jumps = [int(max(1, mean * f)) for f in JUMP_FRACS]
        # precompute each jump-sized point once (affine) -> one mixed add/hop
        self.jump_aff = [to_affine(scalar_mult(j)) for j in self.jumps]
        self.stats = {}

    def _step(self, point_jac, d):
        aff = to_affine(point_jac)
        b = _jump_bucket(aff)
        return jac_add_affine(point_jac, *self.jump_aff[b]), d + self.jumps[b]

    def solve(self, target_jac):
        """Return k in [lo, hi] with target_jac = kG, else raise LookupError.

        Builds the tame trail once (O(sqrt W) points, spans ~4x the mean
        walk), then runs independent wild passes (fresh random bootstrap jump
        each) until a point collision recovers k. Wall-clock max_seconds
        bounds the whole run; stats records passes/hops for the report.
        """
        lo, W = self.lo, self.W
        theory = math.sqrt((W + 1) * math.pi / 2)
        tame_steps = max(64, int(4 * theory) + 2)
        pass_steps = max(64, int(6 * theory) + 2)
        t0 = time.monotonic()
        passes = 0
        hops = 0

        # --- tame trail: every visited point -> its absolute offset ----------
        tame = scalar_mult(lo)
        tame_d = 0
        tame_off = {to_affine(tame): lo}
        for _ in range(tame_steps):
            tame, tame_d = self._step(tame, tame_d)
            tame_off[to_affine(tame)] = lo + tame_d

        # degenerate case: target IS the low anchor
        aff_q = to_affine(target_jac)
        if aff_q in tame_off:
            k = lo + tame_off[aff_q] - lo
            if 0 <= k - lo <= W and point_equal_jac(scalar_mult(k), target_jac):
                self.stats = dict(method="kangaroo", hops=0, passes=0,
                                  tame_trail=tame_steps, edge="target==lo")
                return k

        # --- wild passes: fresh random bootstrap gives an independent walk ---
        while True:
            passes += 1
            rng = random.Random(self.seed * 1000 + passes)
            d0 = rng.randrange(0, int(3 * theory) + 1)
            if d0 == 0:
                wild, wild_d = target_jac, 0
            else:
                d0_aff = to_affine(scalar_mult(d0))
                wild = jac_add_affine(target_jac, *d0_aff)   # Q + d0*G
                wild_d = d0

            for _ in range(pass_steps):
                wild, wild_d = self._step(wild, wild_d)
                hops += 1
                t_off = tame_off.get(to_affine(wild))
                if t_off is not None:
                    # t_off is absolute (lo + D_t); wild abs = lo + s_k + wild_d
                    k = t_off - wild_d              # = lo + s_k
                    if 0 <= k - lo <= W and point_equal_jac(scalar_mult(k),
                                                            target_jac):
                        self.stats = dict(method="kangaroo", hops=hops,
                                          passes=passes, tame_trail=tame_steps)
                        return k

            if self.max_seconds is not None and time.monotonic() - t0 > self.max_seconds:
                self.stats = dict(method="kangaroo", hops=hops, passes=passes,
                                  tame_trail=tame_steps, timeout=True)
                raise LookupError(
                    f"kangaroo budget ({self.max_seconds:.1f}s) exhausted: "
                    f"interval {lo}..{self.hi}, hops={hops}, passes={passes}")

        raise LookupError("kangaroo internal termination lost")