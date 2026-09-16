# 06 — Algorithms

## Solver Ladder (v1 → v4 + Fused)

### v1: Naive Brute-Force
- **Algorithm:** For each k in [lo, hi], compute scalar_mult(k) -> compressed -> hash160 -> compare.
- **Time:** O(W) group operations.
- **Memory:** O(1).
- **Measured:** 13,646 keys/s (single CPU core).
- **Use case:** Correctness baseline; small intervals.

### v2: Stride + Bitmask
- **Algorithm:** Advance via jac_add_affine (O(1) per key) + bitmask bucket prefilter.
- **Time:** O(W) group operations (but 3.2× faster constant).
- **Memory:** O(1).
- **Measured:** 43,234 keys/s (stride), 44,763 keys/s (masked), 125,471 adds/s (pure stride).
- **Use case:** Brute-force at 3× speed; bitmask useful for multi-target batches.

### v3: Baby-Step Giant-Step (BSGS)
- **Algorithm:** Build baby-step dict of size m=√W, then giant-step walk of m steps.
- **Time:** O(√W) group operations.
- **Memory:** O(√W) — the limiting factor.
- **Measured:** w=16: 0.062s, w=20: 0.297s, w=24: 0.844s, w=28: 3.312s.
- **Use case:** Exact oracle for verification-scale targets; BSGS at small W.

### v4: Pollard Kangaroo
- **Algorithm:** Fixed tame trail from offset 0, multiple wild passes with fresh d0.
- **Time:** O(√W) group operations.
- **Memory:** O(1) — key advantage over BSGS at scale.
- **Measured:** w=16: 0.391s (212 hops), w=20: 1.812s (1,762), w=24: 5.516s (1,895), w=28: 31.328s (28,845).
- **Use case:** Real-world interval DLP; trivially parallelizable.

### v4-Fused: Pollard Kangaroo with Single Inversion
- **Algorithm:** Same as v4 but _step returns affine alongside Jacobian point.
- **Time:** O(√W) group operations (same asymptotic).
- **Memory:** O(1) (same).
- **Speedup:** 2.0x average (EX4, 36 cases).
- **Mechanism:** 1 modular inversion/hop instead of 2 (reuse affine for bucket + lookup).
- **Use case:** Drop-in replacement for v4; any interval DLP.

## Comparison Table

| Algorithm | Time | Memory | Parallel? | Measured Speedup |
|---|---|---|---|---|
| v1 naive | O(W) | O(1) | No | 1x (baseline) |
| v2 stride | O(W) | O(1) | No | 3.2x |
| v3 BSGS | O(√W) | O(√W) | No | Exact oracle |
| v4 kangaroo | O(√W) | O(1) | Yes | Probabilistic |
| **v4-fused** | **O(√W)** | **O(1)** | **Yes** | **2.0x vs v4** |

## What's NOT Possible (Verified)

- ❌ No asymptotic shortcut (EX5: Θ(√W) floor confirmed)
- ❌ No Pohlig-Hellman (n is prime)
- ❌ No subgroup attack (cofactor=1)
- ❌ No GLV walk acceleration (walk steps are point additions)
- ❌ No low-bit bucket shortcut (EX1: uniform)
- ❌ No PRNG fingerprint (EX2: null-expectation passes)
- ❌ No statistical structure (EX3: no replicated p<0.01)

## Implementation Details

### Fused Inversion Design
```
Baseline _step(pt, d):
    aff = to_affine(pt)           # inversion #1 (bucket)
    b = jump_bucket(aff)
    return jac_add_affine(pt, jump_aff[b]), d + jumps[b]

Fused _step(pt, d):
    aff = to_affine(pt)           # inversion (bucket + lookup)
    b = jump_bucket(aff)
    old_d = d
    new_pt = jac_add_affine(pt, jump_aff[b])
    return new_pt, d + jumps[b], aff, old_d
```

Caller pairs `aff` with `old_d` for both bucket computation and dict lookup. One inversion serves both purposes.
