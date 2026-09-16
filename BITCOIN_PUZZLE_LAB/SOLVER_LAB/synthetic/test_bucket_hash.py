"""Compare bucket functions: current (x>>120)&0xF vs spectral-mix XOR-fold.

Miller-Venkatesan (2002): bucket assignments with maximal spectral gap
(folding ALL 256 bits of the x-coordinate) mix better than taking only
the top bits. For truly uniform pseudo-random x there is no first-order
difference, but the theoretical result says the fold reduces the coupling
time / correlation between consecutive bucket draws.

Measure: K = total_ops / sqrt(W) for each bucket function on identical
widths and keys, many seeds, at w=24 (enough hops for the effect to show,
cheap enough for 15 trials).

Design uses the exact v4 KangarooSolver, overriding only the bucket
function via a subclass.
"""
import os, sys, math, random, time
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

LAB = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, LAB)
os.chdir(LAB)

from solvers.v4_kangaroo import KangarooSolver
from algorithms.curve import scalar_mult, to_affine, jac_add_affine

class TopBits(KangarooSolver):
    """Baseline: current v4 bucket function."""
    def _step(self, point_jac, d):
        aff = to_affine(point_jac)
        b = (aff[0] >> 120) & 0xF
        return jac_add_affine(point_jac, *self.jump_aff[b]), d + self.jumps[b]

class XorFold(KangarooSolver):
    """Spectral-mix: XOR all 32 8-bit chunks of x, mod 16.

    Folds every bit into the bucket choice: the deviation of the
    bucket-assignment function from the uniform distribution is
    concentrated at the top of the spectrum (Miller-Venkatesan).
    """
    def _step(self, point_jac, d):
        aff = to_affine(point_jac)
        x = aff[0]
        acc = 0
        for _ in range(32):
            acc ^= x & 0xFF
            x >>= 8
        b = acc & 0xF
        return jac_add_affine(point_jac, *self.jump_aff[b]), d + self.jumps[b]

def run_one(cls, lo, hi, key, seed, max_seconds=30):
    s = cls(lo, hi, max_seconds=max_seconds, seed=seed)
    try:
        k = s.solve(scalar_mult(key))
    except LookupError:
        return None, s.stats
    ok = (k == key)
    return ok, s.stats

W_BITS = 24
lo = 1 << (W_BITS - 1)
hi = (1 << W_BITS) - 1
W = hi - lo + 1
SEEDS = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]

print(f"=== Spectral-Mix Bucket vs Top-Bit Bucket (v4 kangaroo) ===")
print(f"Width: {W_BITS} bits, W = {W:,}, trials: {len(SEEDS)}")
print()

results = {"top": [], "fold": []}
fails = {"top": 0, "fold": 0}

for seed in SEEDS:
    rng = random.Random(seed * 1000 + W_BITS)
    key = rng.randint(lo, hi)
    for name, cls in (("top", TopBits), ("fold", XorFold)):
        ok, stats = run_one(cls, lo, hi, key, seed)
        if not ok:
            fails[name] += 1
            continue
        total_ops = stats.get("tame_trail", 0) + stats.get("hops", 0)
        K = total_ops / math.sqrt(W)
        results[name].append(K)

for name in ("top", "fold"):
    vals = results[name]
    if vals:
        print(f"{name:>6}: mean K = {sum(vals)/len(vals):.3f}  min={min(vals):.3f}  "
              f"max={max(vals):.3f}  solves={len(vals)}  fails={fails[name]}")
    else:
        print(f"{name:>6}: NO SOLVES  fails={fails[name]}")

if results["top"] and results["fold"]:
    ratio = (sum(results["fold"]) / len(results["fold"])) / \
            (sum(results["top"]) / len(results["top"]))
    print(f"\nK fold/top ratio: {ratio:.3f}  (>1 means spectral-mix made it WORSE)")