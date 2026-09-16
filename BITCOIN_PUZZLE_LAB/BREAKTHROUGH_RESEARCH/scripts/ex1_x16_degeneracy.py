"""EX1: secp256k1 x-coordinate low-bit structure — empirical + exhaustive.

WHAT THIS TESTS
  v4's original bucket function bucketed on (x & 0xF). Prior notes claimed
  "x^3+7 square mod 16 forces x in {9,13} mod 16, so only 2 buckets".
  Two questions:
    Q1 (exhaustive): what residues x mod 16 admit a square root for x^3+7
       mod 16? (This is a NECESSARY condition only if the mod-16 reduction
       were valid for points reduced mod p, which it is NOT — we report it
       to show the claimed proof does not give {9,13}: it gives {5,9}.)
    Q2 (empirical, the real test): for actual secp256k1 points k*G, what is
       the empirical distribution of (x mod 16) and of ((x >> 120) & 0xF)?

CONCLUSION IS DRAWN FROM Q2 ONLY (measured, not assumed).
"""

import os, sys, random
LAB = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, LAB)

from algorithms.curve import P, N, scalar_mult, to_affine, jac_add_affine

def qr16(t):
    return any((s * s) % 16 == t for s in range(16))

print("=== EX1: secp256k1 x low-bit structure ===\n")

# ---- Q1: exhaustive candidate set (informational only) -------------------
QR16 = sorted(t for t in range(16) if qr16(t))
cand = sorted(x for x in range(16) if qr16((x * x * x + 7) % 16))
print(f"Q1. Quadratic residues mod 16: {QR16}")
print(f"    x in 0..15 with (x^3+7) in QR16: {cand}")
print(f"    NOTE: this is 2 residues, and it is NOT the claimed {9,13}. ")
print(f"    Moreover this mod-16 test is NOT a theorem for points reduced")
print(f"    mod p (a mod-p equality does not force a mod-16 equality).")
print(f"    The empirical distribution (Q2) is the authoritative answer.\n")

# ---- Q2a: low nibble of x for RANDOM secp256k1 points --------------------
random.seed(1)
hist = [0] * 16
samples = 5000
for _ in range(samples):
    k = random.randrange(1, N - 1)
    aff = to_affine(scalar_mult(k))
    hist[aff[0] & 0xF] += 1
print(f"Q2a. Low nibble (x mod 16) of {samples} random points k*G (k ~ random 256-bit):")
print(f"     {hist}")
expected = samples // 16
flat = max(abs(c - expected) for c in hist) < 0.4 * expected
print(f"     Expected {expected} per bin if uniform; max deviation "
      f"{max(abs(c - expected) for c in hist)}.")
print(f"     -> {'consistent with uniform' if flat else 'NOT uniform'}\n")

# ---- Q2b: low nibble vs bits 120..123 for WALK points in a small interval
print("Q2b. Walk points in interval [2^19, 2^20) (w=20):")
lo, hi = 1 << 19, (1 << 20) - 1
from solvers.v4_kangaroo import KangarooSolver
solver = KangarooSolver(lo, hi, max_seconds=1, seed=42)

def walk_hist(n_points):
    low = [0] * 16
    highb = [0] * 16
    pt = scalar_mult(lo + 500)
    d = 0
    for _ in range(n_points):
        aff = to_affine(pt)
        low[aff[0] & 0xF] += 1
        highb[(aff[0] >> 120) & 0xF] += 1
        b = (aff[0] >> 120) & 0xF
        pt = jac_add_affine(pt, *solver.jump_aff[b])
        d += solver.jumps[b]
    return low, highb

low_walk, high_walk = walk_hist(300)
print(f"     low nibble x mod 16:      {low_walk}")
print(f"     bits 120..123 of x:       {high_walk}")
ll = [x for x in low_walk if x]
lh = [x for x in high_walk if x]
print(f"     distinct low-nibble residues: {len(ll)}/16")
print(f"     distinct high-bit buckets:    {len(lh)}/16")
print()

# ---- Summary -------------------------------------------------------------
print("SUMMARY (measured):")
print(f"  random-point low nibbles: uniform-ish -> {max(hist)}/{samples}")
print(f"  walk low-nibble distinct residues: {len(ll)} vs high-bit buckets {len(lh)}")
if len(lh) > len(ll):
    print("  => bits 120..123 provide MORE distinct buckets than x mod 16.")
    print("  => the v4 bucket fix (high bits, not low bits) is MEASURED-justified.")
else:
    print("  => low nibbles do NOT collapse here; see full histograms.")
print(f"  Exhaustive candidate residues (informational): {cand}")