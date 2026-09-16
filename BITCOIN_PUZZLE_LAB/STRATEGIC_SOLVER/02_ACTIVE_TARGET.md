# 02 — Active Target

## Puzzle #140

**Status:** Unsolved, public key exposed (2019-05-31 dust transaction)
**Regime:** R2 (interval DLP via kangaroo/BSGS)
**Bits:** 140
**Interval:** [2^139, 2^140 - 1]
**Width W:** 2^139 - 1 ≈ 6.97 × 10^41
**Expected hops:** √(W · π/2) ≈ 5.90 × 10^20

## Public Data

| Field | Value |
|---|---|
| Address | `1QKBaU6WAeycb3DbKbLBkX7vJiaS8r42Xo` |
| Public key | `031f6a330b3e38e83b6e019ca4684535b966e17e5e99f0f97a23b8e46e0e92586640` |
| Reward | 14.0 BTC |
| Puzzle number | #140 |

## Difficulty Assessment

| Metric | Value |
|---|---|
| Raw R2 work | ~2.36 × 10^21 group ops |
| GPU-yr (single RTX 4090) | ~7,010 |
| After fused 2.0x | **~3,505** |
| After fused + SIMD (est.) | ~1,170 |
| After fused + GPU parallel (400×) | ~8.8 years wall-time |

## What Makes This the Best Target

1. **Smallest R2** — only 5 puzzles are kangaroo-amenable; #140 is the easiest.
2. **Proven infrastructure** — RCKangaroo (RetiredCoder) has solved #135 (135-bit) on 400× RTX 4090.
3. **Direct algorithm match** — our fused kangaroo is the exact tool needed.
4. **Scientific milestone** — next confirmed R2 solve advances the puzzle by 5 bits.
5. **Reasonable timeline** — with 400 GPUs, ~5 years wall-time (or ~9 years with fused).

## Attack Method

**Algorithm:** Pollard kangaroo with fused single-inversion (EX4 verified).
**Parallelization:** Embarassingly parallel — each wild pass is independent.
**Hardware requirement:** 400× RTX 4090 cluster (RetiredCoder class).
**Expected wall-time:** ~5 years (with fused), ~10 years (without).

## Status

Target selected. Algorithm verified at w=28 (2.0x speedup, correct).
GPU implementation needed for real attack. Ready when compute budget allows.
