"""EX2 (v2): PRNG artifact test — WITH null-expectation analysis.

v1 was flawed: it counted raw matches, but for small intervals W=2^(n-1)
the chance a random prediction equals the key is 1/W, which is huge for
puzzle #4 (W=8).  A "match" there proves nothing.  Classic false positive.

CORRECT DESIGN:
  For each (strategy, seed) we predict ALL 83 keys and score:
    - total exact matches
    - matches at LARGE intervals (n >= 40: W >= 2^39 — random match ~1e-12)
    - the longest consecutive run of correct predictions n=1,2,3,...
  We then compare total matches against the NULL EXPECTATION
  sum_n P(match at n = 1/W_n). If reality matches null within noise
  and no (strategy,seed) predicts ANY large key, the keys show NO
  weak-PRNG fingerprint.
"""

import os, sys, math, random, hashlib
LAB = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, LAB)
os.chdir(LAB)
from algorithms.interval import parse_tracker, RAW_TRACKER

rows = sorted([r for r in parse_tracker(RAW_TRACKER) if r.solved], key=lambda r: r.n)
print(f"=== EX2 (v2): PRNG artifact test, null-expectation design ===")
print(f"Solved keys: {len(rows)} (puzzle numbers 1..{max(r.n for r in rows)})\n")

# ------------------------------------------------------------------
# Generator strategies. Each returns a prediction for puzzle n.
# ------------------------------------------------------------------
def gen_getrandbits(seed, n, lo, hi):
    return random.Random(seed).getrandbits(n)

def gen_randint(seed, n, lo, hi):
    return random.Random(seed).randint(lo, hi)

def gen_randint_n(seed, n, lo, hi):
    return random.Random(n).randint(lo, hi)

def gen_xorshift(seed, n, lo, hi):
    x = seed & 0xFFFFFFFF
    x = x or 1
    for _ in range(n):
        x ^= (x << 13) & 0xFFFFFFFF
        x = (x ^ (x >> 17) ^ (x << 5)) & 0xFFFFFFFF
    return lo + (x % (hi - lo + 1))

def gen_lcg(seed, n, lo, hi):
    return lo + (seed * n) % (hi - lo + 1)

def gen_sha256(seed, n, lo, hi):
    h = hashlib.sha256(f"{seed}:{n}".encode()).digest()
    return lo + (int.from_bytes(h[:16], 'big') % (hi - lo + 1))

STRATEGIES = [
    ("getrandbits(seed)", gen_getrandbits),
    ("randint(seed)",      gen_randint),
    ("randint(seed=n)",    gen_randint_n),
    ("xorshift32(seed)",   gen_xorshift),
    ("LCG(seed*n)",        gen_lcg),
    ("sha256(seed,n)",     gen_sha256),
]

SEEDS = list(range(0, 300)) + [42, 160, 314, 271, 1024, 48879, 57005, 65536]

# Null expectation: for a random predictor, P(match at puzzle n) = 1/W_n.
# W_n = 2^(n-1). For randint/lcg/sha256 approach: 1/W. getrandbits bitlen n
# actually draws from 0..2^n-1 so P(match to an n-bit key) = 1/2^n.
null_total_randint = sum(1 / (r.hi - r.lo + 1) for r in rows)

print(f"Null expectation: a single random predictor matches "
      f"~{null_total_randint:.2f} of the {len(rows)} keys by chance "
      f"(sum of 1/W_n).\n")

print(f"{'strategy':<22} {'seeds':>5} {'total matches':>14} "
      f"{'null+3sd':>10} {'matches n>=40':>14} {'best run':>9}")
print("-" * 78)

results = {}
for sname, gen in STRATEGIES:
    total_matches = 0
    big_matches = 0
    best_run = 0
    best_run_seed = None
    for seed in SEEDS:
        matches_at = []
        consecutive = 0
        cur_max = 0
        for r in rows:
            n, lo, hi = r.n, r.lo, r.hi
            pred = gen(seed, n, lo, hi)
            walk_match = (pred == int(r.priv, 16))
            if walk_match:
                matches_at.append(n)
                consecutive += 1
                cur_max = max(cur_max, consecutive)
            else:
                consecutive = 0
        total_matches += len(matches_at)
        big = [n for n in matches_at if n >= 40]
        big_matches += len(big)
        if len(matches_at) == len(rows):
            print(f"  >>> {sname} seed={seed}: MATCHES ALL {len(rows)} KEYS")
        elif big:
            print(f"  >>> {sname} seed={seed}: matches large puzzles {big}")
        if cur_max > best_run:
            best_run = cur_max
            best_run_seed = seed
    results[sname] = dict(total=total_matches, big=big_matches,
                          best_run=best_run, best_seed=best_run_seed)
    # std of a single seed's matches ~ sqrt(sum W(1-W)/W^2) ~ sqrt(sum 1/W)
    sd1 = math.sqrt(null_total_randint)
    null3 = (null_total_randint + 3 * sd1) * len(SEEDS)  # over all seeds
    print(f"{sname:<22} {len(SEEDS):>5} {total_matches:>14} {null3:>10.1f} "
          f"{big_matches:>14} {best_run:>5} (seed {best_run_seed})")

print()
print("=" * 78)
print("VERDICT")
non_null = [s for s, d in results.items()
            if d["total"] > (null_total_randint + 3 * sd1) * len(SEEDS)]
if non_null:
    print(f"Strategies exceeding null+3sd: {non_null} — investigate further!")
else:
    print("No strategy exceeds the null expectation (chance) by 3 sigma.")
big_noise = [s for s, d in results.items() if d["big"] > 0]
if big_noise:
    print(f"WARNING: strategies with large-key matches: {big_noise}")
else:
    print("NO strategy predicts any key at puzzle >= 40 (W >= 2^39).")
    print("A true generator fingerprint would have to nail a large key")
    print("(probability <= 1e-12 per try) — nothing does.")
    print("=> The 83 recorded keys are CONSISTENT WITH high-entropy random")
    print("   draws. No weak-PRNG artifact found. (Honest negative.)")