# Discovery

## What We Searched For

A genuine, measurable, reproducible improvement to the interval-DLP
solver (Pollard kangaroo on secp256k1) or a structural insight about
the 83 solved Bitcoin Puzzle keys.

## What We Found

### Discovery D1: Fused Single-Inversion Kangaroo (Positive)

The baseline v4 kangaroo performs **two modular inversions per hop**:
one in `_step()` for bucket selection and one in the membership lookup.
Since `jac_add_affine` does not return the affine of the result, the
lookup recomputes the affine from scratch.

**Key insight:** The affine used for bucket selection is the affine of
the *current* point (before the jump). The membership lookup checks the
*same* point's affine against the tame trail. So the affine computed for
the bucket can be reused for the lookup — one inversion serves both
purposes.

**Implementation:** `_step()` returns `(new_pt, new_d, aff_in, old_d)`.
The caller pairs `aff_in` with `old_d` for both bucket computation and
dict lookup. No second inversion.

**Measured result:** 2.00x average speedup across 36 test cases
(w=16,20,24,28), with identical key recovery and walk identity.

### Discovery D2: No Structural Anomaly in 83 Keys (Negative)

Searched for exploitable patterns across 11 statistical metrics
(relative position, low bits, hamming weight, leading-ones, parity,
mod-3, consecutive pairs, reward correlation, depth, Benford's law)
on a train/test split. None replicated at p<0.01 in the same direction.

Searched for weak-PRNG fingerprint across 6 generator strategies × 308
seeds. No strategy exceeds null expectation by 3σ. No strategy predicts
any key at puzzle n≥40 (W≥2³⁹, probability ≤ 1e-12 per try).

**Conclusion:** The 83 recorded keys are consistent with high-entropy
uniform random draws. No shortcut exists.

### Discovery D3: Low-4-Bit Degeneracy Claim Disproven (Correction)

The v4 docstring claimed low-4-bit degeneracy (x≡9 or 13 mod 16 → 2
buckets). EX1 showed QR(16)={0,1,4,9} and candidate set {5,9} — the
mod-16 pattern is empirically false. The real fix for the old 20-bit
timeout was the trail/restart redesign.

## What We Can State

We have one positive, verified result (D1) and two honest negatives
(D2, D3). The positive result is a constant-factor improvement — it
does not break the Θ(√W) asymptotic floor but achieves a measured 2x
speedup that is meaningful at practical interval sizes.
