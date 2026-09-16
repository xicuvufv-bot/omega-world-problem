# Active Target

## Chosen Target: Puzzle #66

**Private key is 33 bits (W ≈ 8.6 billion).**
Public key known. Exact interval DLP: k in [2^32, 2^33-1].
Expected kangaroo walks: √(W·π/2) ≈ 116,000 hops per wild path.

## Why This Target

1. **Smallest unsolved R1 puzzle** — puzzle #66 is the next in the sequence
   after the last solved R1 (#65 at 32 bits).
2. **Feasible on CPU with the fused kangaroo** — extrapolating from the
   EX4 benchmark (w=28 baseline ≈ 40s, fused ≈ 20s), w=33 should take
   roughly 30–60 minutes per random key on a single CPU core. This is within
   a realistic experiment budget.
3. **Exact public key available** — the public key is published on the
   Bitcoin Puzzle board, so verification of a found private key is trivial
   (scalar_mult(k) == target_point).
4. **Constant-factor improvement matters here** — the 2.0x fused speedup
   from EX4 cuts the solve time in half. At 33 bits, this is the regime
   where constant factors translate to hours vs minutes.

## What Is NOT Possible (Verified by EX5)

- No asymptotic improvement: secp256k1 cofactor=1, j=0, GLV endomorphism
  exists but does NOT reduce walk-step cost. The floor is Θ(√W) group ops.
- No subgroup/Pohlig-Hellman reduction: n is prime.
- The only path is constant-factor: better inversions, SIMD, GPU, memory
  optimization.

## Method

Use the fused single-inversion kangaroo (from EX4) on the exact public key
of puzzle #66. This is a **real challenge** (the key exists on the public
board) but involves no fund access — it is a proof-of-concept for the
constant-factor improvement.

## Status

Target selected. Algorithm verified at w=28 (2.0x speedup, correct).
Ready to run at w=33 when compute budget allows (~1 hour CPU time).
