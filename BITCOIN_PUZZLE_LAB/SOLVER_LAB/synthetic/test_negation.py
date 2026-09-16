"""Test the negation map (Y-parity directed walk) on v4 kangaroo.

External claim (RCKangaroo / oritwoen): walking on the equivalence class
{P, -P} halves the effective search width, worth ~1.29-1.41x fewer ops.

Construction:
  * Both herds normalize each visited point to the canonical representative
    with EVEN y (negate if the affine y is odd).
  * A stored tame canonical point equals a wild canonical point iff the
    underlying points match up to sign, so candidates are:
        k1 = t_off - wild_d          (wild == tame)
        k2 = N - (t_off + wild_d)    (wild == -tame)
    Both are verified with a full scalar mult before returning.
  * Jump table is symmetric on the class (deterministic from canonical x).

Measure: K = total_ops / sqrt(W) for baseline v4 vs negation-map v4,
the same width and keys.
"""
import os, sys, math, random, time
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

LAB = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, LAB)
os.chdir(LAB)

from solvers.v4_kangaroo import KangarooSolver
from algorithms.curve import scalar_mult, to_affine, jac_add_affine, point_equal_jac, P, N

class Baseline(KangarooSolver):
    pass

class NegationMap(KangarooSolver):
    """v4 + canonical (even-y) walks, sized to the quotient space W/2.

    Bucket from canonical x; the jump table and trail lengths are tuned to
    the folded interval (effective width W/2), which is the correct
    construction for the equivalence-class walk (Wiener-Zuccherato 1998).
    """
    def _step(self, point_jac, d):
        aff = to_affine(point_jac)
        if aff[1] & 1:
            aff = (aff[0], P - aff[1])
        b = (aff[0] >> 120) & 0xF
        return jac_add_affine(point_jac, *self.jump_aff[b]), d + self.jumps[b]

    def _canon(self, point_jac, d):
        aff = to_affine(point_jac)
        if aff[1] & 1:
            aff = (aff[0], P - aff[1])
        return aff, d

    def solve(self, target_jac):
        lo, W = self.lo, self.W
        Weff = max(1, W // 2)
        # retune the jump table for the quotient space
        mean = math.sqrt(Weff + 1)
        n = len(self.jumps)
        for i in range(n):
            self.jumps[i] = int(max(1, mean * (0.5 + 0.1 * i)))
        self.jump_aff = []
        from algorithms.curve import to_affine as _ta
        from solvers.v4_kangaroo import JUMP_FRACS
        mean = math.sqrt(Weff + 1)
        self.jumps = [int(max(1, mean * f)) for f in JUMP_FRACS]
        self.jump_aff = [_ta(scalar_mult(j)) for j in self.jumps]

        theory = math.sqrt((Weff + 1) * math.pi / 2)
        tame_steps = max(64, int(4 * theory) + 2)
        pass_steps = max(64, int(6 * theory) + 2)
        theory_w = math.sqrt((W + 1) * math.pi / 2)
        t0 = time.monotonic()
        passes = 0
        hops = 0

        tame = scalar_mult(lo)
        tame_d = 0
        tame_off = {}
        for _ in range(tame_steps):
            tame, tame_d = self._step(tame, tame_d)
            aff, tame_d = self._canon(tame, tame_d)
            tame_off[aff] = lo + tame_d

        aff_q, _ = self._canon(target_jac, 0)
        if aff_q in tame_off:
            for k in (lo + tame_off[aff_q] - 0, N - (tame_off[aff_q] + 0)):
                if 0 <= k - lo <= W and point_equal_jac(scalar_mult(k), target_jac):
                    self.stats = dict(method="negation", hops=0, passes=0,
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
                wild, wild_d = self._step(wild, wild_d)
                hops += 1
                cant, wild_d = self._canon(wild, wild_d)
                t_off = tame_off.get(cant)
                if t_off is not None:
                    k1 = t_off - wild_d
                    k2 = N - (t_off + wild_d)
                    for k in (k1, k2):
                        if 0 <= k - lo <= W and point_equal_jac(scalar_mult(k),
                                                                target_jac):
                            self.stats = dict(method="negation", hops=hops,
                                              passes=passes, tame_trail=tame_steps)
                            return k

            if self.max_seconds is not None and time.monotonic() - t0 > self.max_seconds:
                self.stats = dict(method="negation", hops=hops, passes=passes,
                                  tame_trail=tame_steps, timeout=True)
                raise LookupError(f"negation budget exhausted: hops={hops}")

        raise LookupError("negation walk lost")

def run_one(cls, lo, hi, key, seed, max_seconds=60):
    s = cls(lo, hi, max_seconds=max_seconds, seed=seed)
    try:
        k = s.solve(scalar_mult(key))
    except LookupError:
        return None, s.stats
    return (k == key), s.stats

W_BITS = 20
lo = 1 << (W_BITS - 1)
hi = (1 << W_BITS) - 1
W = hi - lo + 1
SEEDS = list(range(1, 13))

print(f"=== Negation Map vs Baseline (v4 kangaroo) ===")
print(f"Width: {W_BITS} bits, W = {W:,}, trials: {len(SEEDS)}")
print()

res = {"base": [], "neg": []}
fails = {"base": 0, "neg": 0}

for seed in SEEDS:
    rng = random.Random(seed * 1000 + W_BITS)
    key = rng.randint(lo, hi)
    for name, cls in (("base", Baseline), ("neg", NegationMap)):
        ok, stats = run_one(cls, lo, hi, key, seed)
        if not ok:
            fails[name] += 1
            continue
        total = stats.get("tame_trail", 0) + stats.get("hops", 0)
        res[name].append(total / math.sqrt(W))

for name in ("base", "neg"):
    v = res[name]
    if v:
        print(f"{name:>4}: mean K={sum(v)/len(v):.3f}  min={min(v):.3f}  "
              f"max={max(v):.3f}  solves={len(v)}  fails={fails[name]}")
    else:
        print(f"{name:>4}: NO SOLVES  fails={fails[name]}")

if res["base"] and res["neg"]:
    r = (sum(res["neg"])/len(res["neg"])) / (sum(res["base"])/len(res["base"]))
    print(f"\nK neg/base: {r:.3f}  (>1 = negation made it WORSE, <1 = speedup)")
    print(f"Expected if claim holds: ~0.70-0.78 (1.29-1.41x fewer ops)")