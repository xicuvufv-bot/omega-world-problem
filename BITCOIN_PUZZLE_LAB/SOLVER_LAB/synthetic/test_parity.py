"""H5 Test: Parity Split Hypothesis.

Can we determine the parity of the private key from the public key,
and use this to eliminate half the search interval?

On secp256k1 (a=0, b=7):
  - Scalar mult: k*G = (x, y)
  - Doubling: 2*(x,y) = (3x²/4y², ...) — preserves y parity if y stays integer
  - Actually: the parity of k determines the parity of x-coordinate via
    the group law. If we can compute parity(x) from parity(k), we can
    split the interval.

For the 83 solved keys, we check:
  1. parity(k) vs parity(x(k*G))
  2. Is the mapping deterministic? (same parity(k) -> same parity(x))
  3. If yes: for any R2 puzzle, parity(x) from public key -> parity(k) -> eliminate half.
"""
import os, sys, random
LAB = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, LAB)
os.chdir(LAB)

from algorithms.curve import scalar_mult, to_affine, P, N, Gx, Gy
from algorithms.interval import parse_tracker, RAW_TRACKER

rows = sorted([r for r in parse_tracker(RAW_TRACKER) if r.solved], key=lambda r: r.n)
print(f"=== H5 Test: Parity Split ===\n")
print(f"Testing {len(rows)} solved keys...\n")

# Collect data
data = []
for r in rows:
    k = int(r.priv, 16)
    pt = to_affine(scalar_mult(k))
    x, y = pt
    k_parity = k & 1
    x_parity = x & 1
    data.append((r.n, k, k_parity, x_parity))

# Check mapping
k0_x0 = sum(1 for n, k, kp, xp in data if kp == 0 and xp == 0)
k0_x1 = sum(1 for n, k, kp, xp in data if kp == 0 and xp == 1)
k1_x0 = sum(1 for n, k, kp, xp in data if kp == 1 and xp == 0)
k1_x1 = sum(1 for n, k, kp, xp in data if kp == 1 and xp == 1)

print("Parity mapping (k_parity -> x_parity):")
print(f"  k_even -> x_even: {k0_x0}")
print(f"  k_even -> x_odd:  {k0_x1}")
print(f"  k_odd  -> x_even: {k1_x0}")
print(f"  k_odd  -> x_odd:  {k1_x1}")

# Check if mapping is deterministic
if k0_x1 == 0 and k1_x0 == 0:
    print("\n  Mapping: k_even -> x_even, k_odd -> x_odd (DETERMINISTIC)")
    print("  => Parity of x determines parity of k => 2x reduction!")
elif k0_x0 == 0 and k1_x1 == 0:
    print("\n  Mapping: k_even -> x_odd, k_odd -> x_even (DETERMINISTIC)")
    print("  => Parity of x determines parity of k => 2x reduction!")
else:
    print("\n  Mapping: NOT deterministic (mix of both)")
    print("  => Parity of x does NOT uniquely determine parity of k")
    print("  => No 2x reduction from parity alone")

# Also check: what fraction of keys are even vs odd?
even_k = sum(1 for n, k, kp, xp in data if kp == 0)
odd_k = sum(1 for n, k, kp, xp in data if kp == 1)
print(f"\nKey parity distribution: even={even_k}, odd={odd_k}")

# Check the actual mapping for each key
print("\nFirst 10 keys:")
for n, k, kp, xp in data[:10]:
    print(f"  #{n:3d}: k={k:#06x} parity={kp} -> x_parity={xp}")
