# 03 — Knowledge Transfer

## General Rules Extracted

### R1: The R2/R1 Divide Is the Most Important Structural Fact
- 5 puzzles (R2) are kangaroo-amenable with O(√W) work.
- 72 puzzles (R1) require O(W) hash scans — orders of magnitude harder.
- **Always check regime before choosing algorithm.**

### R2: BSGS Is Exact, Kangaroo Is Probabilistic
- BSGS: O(√W) time + O(√W) memory — deterministic, repeatable.
- Kangaroo: O(√W) time + O(1) memory — probabilistic, parallelizable.
- **BSGS wins at small W; kangaroo wins at large W** (memory constraint).

### R3: Bucket Function Choice Matters
- Low-bit buckets (x & 0xF) are degenerate on secp256k1 → only 2 effective buckets.
- High-bit buckets (x >> 120) & 0xF → 16 distinct buckets at all widths.
- **Always verify bucket distribution empirically before claiming uniformity.**

### R4: The Meet-Time Heavy Tail Is Real
- Twin-herd kangaroo can take 12×+ mean meeting time on unlucky launches.
- Mitigation: single tame trail + many fresh wild passes with independent seeds.
- **Never test on a single seed.** Use 3+ seeds minimum.

### R5: Bookkeeping Bugs Are the #1 Source of False Negatives
- Off-by-one in recovery formula (double-adding lo).
- d0=0 producing infinity point.
- Missing range check on recovered k.
- **Always re-verify kG == Q before returning.**

### R6: No Pattern Survives Train/Test Replication
- 83 published keys show no exploitable structure across 11 metrics.
- Hamming weight p<0.01 in combined data fails directional replication (train vs test).
- **Never claim a pattern without independent test-set verification.**

### R7: Constant-Factor Improvements Are Real and Measurable
- The fused kangaroo achieves 2.0x by eliminating one modular inversion per hop.
- This is not theoretical — it was measured on 36 test cases with verified correctness.
- **Don't dismiss constant-factor work.** It compounds with parallelism.

### R8: The Θ(√W) Floor Is Confirmed
- secp256k1 cofactor=1, prime order, no Pohlig-Hellman, GLV doesn't help walks.
- Any improvement must be constant-factor, not asymptotic.
- **Don't waste time searching for asymptotic shortcuts on secp256k1.**

## Useful Transformations

| Transformation | What It Does | When to Use |
|---|---|---|
| Fused inversion | Eliminate 1 modular inv/hop | Any kangaroo implementation |
| Stride point-add | O(1) per key instead of O(n) | Brute-force enumeration |
| Batch Jacobi-to-affine | Invert N points at once for 1/40 cost | Table building (BSGS) |
| Windowed scalar-mult | Precompute 2^w points, multiply in w-bit windows | Fixed-base multi-scalar |
| SIMD field arithmetic | Parallel modular add/mul | GPU/CPU vectorization |

## Failed Assumptions (Do Not Repeat)

1. ❌ "Low 4 bits are degenerate" → QR(16) analysis disproves this.
2. ❌ "Hamming weight is biased" → Fails train/test replication.
3. ❌ "Keys show PRNG artifact" → Null-expectation test passes.
4. ❌ "Benford's law applies to key first digits" → Fails on test set.
5. ❌ "Relative position biased toward 0.5" → KS p>0.01 in both splits.
6. ❌ "GLV reduces kangaroo walk cost" → Walk steps are point additions, not scalar-mults.
7. ❌ "Pohlig-Hellman applies" → secp256k1 group order is prime.

## Reusable Optimizations (Already Verified)

| Optimization | Source | Speedup | Verified? |
|---|---|---|---|
| Fused single-inversion | EX4 | 2.0x | Yes, 36 cases |
| Stride point-add | v2 | 3.2x | Yes, v2 benchmark |
| Jacobi projective | curve.py | ~2x vs affine | Yes, implicit in v4 |
| 16-bucket Teske table | v4 | Uniform distribution | Yes, EX1 |

## Current Limitations (Known Ceilings)

| Limit | Cause | Impact |
|---|---|---|
| CPU ceiling ~34 bits | Single-core Python speed | 2-4 hours max |
| GPU ceiling ~40-48 bits | RTX 4090 group rate ~8 Gop/s | Months at 400× |
| Python overhead | Interpreted, no SIMD | ~55,000× slower than C |
| No parallel solver | Single-threaded | Can't use multi-core |
