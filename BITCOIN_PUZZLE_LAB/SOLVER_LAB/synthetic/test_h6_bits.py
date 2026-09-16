"""H6: high-bit correlation k vs X(kG) -- vectorized with big-int bit vectors.

Represent each bit slice as one Python big int; correlation = popcounts of
AND/OR arithmetic (C-speed). Grid: 40 k-bits x 40 x-bits = 1600 pairs on
the HIGH half of both. With 2^15 samples this is a principled leakage scan
without the 16384-pair CPython-loop blow-up of the first draft.
"""
import os, sys, math, random
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

LAB = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, LAB)
os.chdir(LAB)

from algorithms.curve import scalar_mult

N = 1 << 15
N_BITS = 40

rng = random.Random(0xC0FFEE)
keys = [rng.getrandbits(160) for _ in range(N)]
xs = [scalar_mult(k)[0] for k in keys]

def bitvec(bits, shift):
    v = 0
    for i, b in enumerate(bits):
        v |= ((b >> shift) & 1) << i
    return v

kV = [bitvec(keys, s) for s in range(120, 120 + N_BITS)]
xV = [bitvec(xs, s) for s in range(120, 120 + N_BITS)]

def corr(a, b, n=N):
    both = (a & b).bit_count()
    na = a.bit_count()
    nb = b.bit_count()
    return phi_equiv(both, na, nb, n)

def phi_equiv(both, na, nb, n):
    # phi = (both - na*nb/n) / sqrt( na*nb*(n-na)*(n-nb) / n^4 )  [same as Pearson]
    if na == 0 or nb == 0 or na == n or nb == n:
        return 0.0
    exp = na * nb / n
    obs_diff = both - exp
    den = math.sqrt((na / n) * (1 - na / n) * (nb / n) * (1 - nb / n)) * n
    return obs_diff / den if den else 0.0

worst = (0.0, None)
signif = []
for i, a in enumerate(kV):
    for j, b in enumerate(xV):
        r = phi_equiv((a & b).bit_count(), a.bit_count(), b.bit_count(), N)
        if abs(r) > abs(worst[0]):
            worst = (r, (120 + i, 120 + j))
        if abs(r) > 0.01:   # ~ |z| > 1.8 at n=32768; pre-filter for cheap z
            z = r * math.sqrt(N - 2) / math.sqrt(max(1 - r * r, 1e-12))
            signif.append((120 + i, 120 + j, r, z))

z_bonf = 4.4   # 1600 tests FWER
strong = [(i, j, r, z) for (i, j, r, z) in signif if abs(z) > z_bonf]

print("=== H6: k-bit vs X(kG)-bit correlation (n=2^15, 40x40 high-bit grid) ===")
print(f"worst |phi| over 1600 pairs: {abs(worst[0]):.6f} at {worst[1]}")
print(f"pairs with |phi|>0.01: {len(signif)}")
print(f"surviving |z|>{z_bonf} (1600-test FWER): {len(strong)}")
for i, j, r, z in strong[:10]:
    print(f"  k bit {i} <-> X bit {j}: phi={r:+.4f} z={z:.1f}")
print("\nVERDICT:", "H6 EFFICIENT-LEAK PRESENT" if strong
      else "no high-bit leakage (H6 REFUTED)")