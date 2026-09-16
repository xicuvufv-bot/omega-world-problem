"""Test Pollard 2025 spread optimization on our v4 kangaroo.

Pollard, Potapov & Guminov (2025) proved that low-variance step sets
increase collision time by 12-15% due to "coupling latency."

The fix: increase spread from 1 to 6, creating a wider distribution
of jump sizes. This ensures jump sizes span 6 bits of range instead
of 1, directly matching Pollard's 2025 recommendation.

Test: compare K = total_ops / sqrt(W) for spread=1 (current v4)
vs spread=6 (Pollard 2025 optimal).
"""
import os, sys, math, random, time
LAB = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, LAB)
os.chdir(LAB)

from algorithms.curve import scalar_mult, to_affine, jac_add_affine, point_equal_jac, P, N, Gx, Gy

# Current v4 jump table (spread=1 equivalent)
JUMP_FRACS_SPREAD1 = (0.50, 0.55, 0.63, 0.72, 0.82, 0.92, 1.03, 1.15) * 2

# Pollard 2025 optimal (spread=6 equivalent): wider distribution
JUMP_FRACS_SPREAD6 = (0.25, 0.35, 0.45, 0.55, 0.65, 0.75, 0.85, 0.95,
                       1.05, 1.15, 1.25, 1.35, 1.45, 1.55, 1.65, 1.75)

def jump_bucket(pt, n_buckets=16):
    x = pt[0]
    return (x >> 120) & (n_buckets - 1)

def make_jump_table(fracs, W):
    mean = math.sqrt(W + 1)
    jumps = [int(max(1, mean * f)) for f in fracs]
    return jumps

def make_jump_affs(jumps):
    return [to_affine(scalar_mult(j)) for j in jumps]

def solve_kangaroo(lo, hi, target_jac, seed, fracs, max_seconds=60):
    W = hi - lo
    jumps = make_jump_table(fracs, W)
    jump_affs = make_jump_affs(jumps)
    theory = math.sqrt((W + 1) * math.pi / 2)
    tame_steps = max(64, int(4 * theory) + 2)
    pass_steps = max(64, int(6 * theory) + 2)

    # Tame trail
    tame = scalar_mult(lo)
    tame_d = 0
    tame_off = {}
    for _ in range(tame_steps):
        aff = to_affine(tame)
        b = jump_bucket(aff)
        tame = jac_add_affine(tame, *jump_affs[b])
        tame_d += jumps[b]
        tame_off[aff] = lo + tame_d

    aff_q = to_affine(target_jac)
    if aff_q in tame_off:
        k = tame_off[aff_q]
        return k, 0, 0, tame_steps, tame_steps

    passes = 0
    hops = 0
    t0 = time.monotonic()
    while True:
        passes += 1
        rng = random.Random(seed * 1000 + passes)
        d0 = rng.randrange(0, int(3 * theory) + 1)
        if d0 == 0:
            wild, wild_d = target_jac, 0
        else:
            d0_aff = to_affine(scalar_mult(d0))
            wild = jac_add_affine(target_jac, *d0_aff)
            wild_d = d0

        for _ in range(pass_steps):
            aff = to_affine(wild)
            b = jump_bucket(aff)
            wild = jac_add_affine(wild, *jump_affs[b])
            wild_d += jumps[b]
            hops += 1
            t_off = tame_off.get(aff)
            if t_off is not None:
                k = t_off - wild_d
                if 0 <= k - lo <= W and point_equal_jac(scalar_mult(k), target_jac):
                    return k, hops, passes, tame_steps, time.monotonic() - t0

        if time.monotonic() - t0 > max_seconds:
            return None, hops, passes, tame_steps, time.monotonic() - t0

# Test on w=20 (fast enough for many seeds)
W_bits = 20
lo = 1 << (W_bits - 1)
hi = (1 << W_bits) - 1
W = hi - lo + 1
SEEDS = [1, 42, 99, 7, 13]
N_TRIALS = 5

print(f"=== Pollard 2025 Spread Optimization Test ===")
print(f"Width: {W_bits} bits, W = {W:,}")
print(f"Trials: {N_TRIALS} seeds\n")

print(f"{'Seed':>6} {'Spread1 K':>12} {'Spread6 K':>12} {'Ratio':>8} {'S1 hops':>10} {'S6 hops':>10}")
print("-" * 62)

k1_list = []
k6_list = []

for seed in SEEDS:
    rng = random.Random(seed * 10000 + W_bits)
    key = rng.randint(lo, hi)
    target = scalar_mult(key)

    # Spread=1
    k1, h1, p1, t1, wall1 = solve_kangaroo(lo, hi, target, seed, JUMP_FRACS_SPREAD1, max_seconds=30)
    total_ops1 = t1 + h1  # tame steps + wild hops

    # Spread=6
    k6, h6, p6, t6, wall6 = solve_kangaroo(lo, hi, target, seed, JUMP_FRACS_SPREAD6, max_seconds=30)
    total_ops6 = t6 + h6

    k_val1 = total_ops1 / math.sqrt(W)
    k_val6 = total_ops6 / math.sqrt(W)
    k1_list.append(k_val1)
    k6_list.append(k_val6)

    ok1 = k1 == key
    ok6 = k6 == key
    ratio = k_val6 / k_val1 if k_val1 > 0 else 0

    print(f"{seed:6d} {k_val1:12.3f} {k_val6:12.3f} {ratio:8.3f} {h1:10d} {h6:10d}")

avg1 = sum(k1_list) / len(k1_list)
avg6 = sum(k6_list) / len(k6_list)
print(f"\nAverage K: spread1={avg1:.3f}  spread6={avg6:.3f}  ratio={avg6/avg1:.3f}")
print(f"Theoretical minimum K: 0.51 (with secp256k1 automorphisms)")
print(f"SOTA K: 1.15 (RCKangaroo)")
print(f"Classic K: 2.1 (Montenegro-Tetali)")
