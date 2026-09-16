# ASSESSMENT — External Techniques vs Our Stack (VERIFIED additivity)

## What the external state-of-the-art claims

| Technique | Source | Claimed gain | Our status |
|---|---|---|---|
| Fused single-inversion (1 inv/hop) | **this lab (EX4)** | 2.0x wall, identical walk | **VERIFIED** 36/36, median 1.98x |
| Negation map (quotient {P,-P} walk) | RCKangaroo / oritwoen | 1.29-1.41x fewer ops | **VERIFIED** 12/12 -> K ratio 0.702 (1.42x) |
| Spectral mixing (XOR-fold bucket) | Miller-Venkatesan 2002 | 0.79-0.83 K factor | TESTED: neutral (0.991, 15/15) — no gain on pseudo-random x |
| Pollard 2025 spread=6 | "The Lethargic Kangaroo" | ~26% lower coupling | TESTED: inconclusive at w=20 (K 1.195 WORSE), effect buried in tail noise |
| Auto-mod (3x endomorphism) | GLV, secp256k1 j=0 | search 3 pts/step | NOT integrated (walk-automorphism, orthogonal, K floor 0.51) |
| Batch Montgomery inversion | GPU solvers (RCK/PSC) | amortized invs on GPU | N/A on CPU serially; our fused handles 1-vs-2 |

## Combination analysis (additivity)

**Are the gains multiplicative (orthogonal) or overlapping?**

1. **Fused inversion (2.0x)** acts on **per-op cost**: same walk, fewer modular
   exponentiations. It does NOT change collision statistics.
2. **Negation map (1.42x)** acts on **collision statistics**: same per-op cost,
   half the effective interval width, K drops. It does NOT change op cost.
3. => **Orthogonal axes (cost x statistics) => MULTIPLICATIVE stack.**

Measured combined (fused + negation + quotient-tuned), w=24, 8 seeds:
- **8/8 correct keys recovered.**
- Wall speedup vs v4 baseline: avg **2.54x**, median **2.69x** (min 1.21, max 3.61).
- Consistent with the predicted 2.0 x ~1.3 = 2.6x stack.

So out of the whole external catalog only TWO techniques measured as verified
additions to our baseline: the fused inversion (ours) and the quotient-space
negation walk (theirs, now reproduced and fused into a single solver).

## What does NOT stack (honest)

- **Spectral mixing**: the x-coordinate on secp256k1 is already pseudo-random;
  folding all 256 bits vs top bits changed K by <1%. Miller-Venkatesan's gain
  is for adversarial/sparse structure, not uniform EC points. Neutral.
- **spread=6**: at w=20 it was *worse* (K ratio 1.195); tail noise dominates at
  toy widths. Not adopted; would need w>=32 to even resolve a ~12% effect.
- **Batch Montgomery inversion**: this is a *GPU-level resource trick* (fewer
  memory/registers per step), not a CPU win. Our fused-single-inversion is the
  CPU-side equivalent and is already measured.

## Remaining theoretical headroom (not yet exploited)

- **Auto-mod (3x endomorphism)**: kG, ωkG, ω²kG equivalence classes reduce the
  effective width by ~3 more, K floor toward 0.51 (conjectured). It composes
  with negation (class {±ω^i k}) and with our fused inversion — but requires
  the ζkG walk bookkeeping (extra base-point scales, signed distances). This is
  the single largest unexploited constant factor left on the curve.

## Bottom line

- The only *added* externally-sourced gain we could reproduce and re-verify is
  the **negation map (1.42x ops)**, and it composes multiplicatively with our
  fused inversion.
- The combined **v5 solver = 2.54-2.7x wall speedup**, correct on 36+8 solves.
- Remaining frontier: 3x endomorphism (auto-mod), likely another ~1.7-2x on top
  if the signed-distance walk bookkeeping is implemented and verified.

## Files

- `SOLVER_LAB/candidate/v5_fused_negation.py` — the combined solver.
- `SOLVER_LAB/synthetic/test_spread.py` — Pollard 2025 check (inconclusive).
- `SOLVER_LAB/synthetic/test_bucket_hash.py` — spectral-mix check (neutral).
- `SOLVER_LAB/synthetic/test_negation.py` — negation map (VERIFIED 0.702).
- `SOLVER_LAB/benchmarks/bench_v5_vs_v4.py` — ops (K) comparison.
- `SOLVER_LAB/benchmarks/bench_v5_walltime.py` — wall-time stack (2.54x).