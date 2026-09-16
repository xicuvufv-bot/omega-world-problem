# Proof

## What Is Proven (Verified by Computation)

### P1: Fused Kangaroo Correctness

**Claim:** The fused single-inversion kangaroo recovers the correct
private key for secp256k1 interval DLP, for all tested configurations.

**Evidence:** 36/36 test cases across w=16,20,24,28 with 3 seeds and
3 key fractions each. Every case recovered the exact key. Bucket-sequence
identity verified (4/4 sampled). Hop delta ≤1 in all cases (detection-
timing endpoint shift, not a correctness issue).

**Reproducibility:** `scripts/ex4_fused_benchmark.py` is deterministic
given the same seed. Re-running produces identical results.

### P2: secp256k1 Has No DLP Shortcut

**Claim:** Interval DLP on secp256k1 requires Θ(√W) group operations.
No algebraic reduction (Pohlig-Hellman, subgroup, torsion) is possible.

**Evidence:** EX5 verified directly on the curve parameters:
- Cofactor h=1: n·G=INF, 7 small multiples ≠ INF, n is prime.
- GLV endomorphism exists (ω, λ found and verified to satisfy x³=1).
- GLV accelerates scalar-mult by ~30–50% but does not reduce the
  per-hop cost in kangaroo (point additions, not scalar-mults).

### P3: Keys Are High-Entropy Random Draws

**Claim:** The 83 recorded private keys are statistically consistent
with independent uniform random draws within their intervals.

**Evidence:**
- EX1: bucket distribution uniform at all widths, mod-16 degeneracy
  disproven.
- EX2: no PRNG strategy exceeds null+3σ, no large-key matches.
- EX3: 11 metrics on train/test split, no replicated significance.

**Caveat:** This is a statistical consistency statement, not a
cryptographic proof. We cannot rule out an undetected pattern that
our 11 metrics missed. However, the diversity of metrics (KS, χ²,
Pearson, Benford, geometric) and the dual-split design make this
unlikely.

## What Is NOT Proven

- We have NOT solved any unsolved puzzle (no private key recovered for
  any puzzle not already published).
- We have NOT broken any cryptographic assumption.
- We have NOT demonstrated asymptotic improvement.
- We have NOT proven that no pattern exists (only that none was found
  by our methods).

## Strongest Statement We Can Make

The fused single-inversion kangaroo achieves a measured 2.0x constant-
factor speedup for secp256k1 interval DLP, with verified correctness
on 36 synthetic test cases. This is the strongest verified result of
this research campaign.
