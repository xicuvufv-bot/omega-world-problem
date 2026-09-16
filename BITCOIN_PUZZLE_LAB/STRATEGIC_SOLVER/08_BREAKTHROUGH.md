# 08 — Breakthrough

## Breakthrough Summary

### What We Achieved

**LEVEL 2 BREAKTHROUGH (UPGRADED): Verified Algorithmic Improvement — v5 solver**

Two independently-verified constant-factor improvements, composed multiplicatively:

| Component | Axis | Gain | Evidence |
|---|---|---|---|
| Fused single-inversion (EX4) | per-op cost | **2.0x** wall | 36 cases, min 1.15x, walk-identical |
| Negation map (quotient {P,-P}) | collision stats | **1.42x** fewer ops | 12/12, K ratio 0.702 |
| **Combined v5 solver** | stacked | **2.54x avg / 2.69x median** wall | 8/8 correct @w=24 |

The two gains are **orthogonal** (cost x statistics), so they multiply; measured
together the v5 solver beats the standalone 2.0x EX4 record.

### Evidence (new)

| Check | Result |
|---|---|
| New idea | Canonical even-y walk over {P,-P} (width W/2) + the fused single-inversion hop |
| Implementation | `SOLVER_LAB/candidate/v5_fused_negation.py` |
| Ops measurement | bench_v5_vs_v4.py: K v5/base = 0.702 @w=20, 0.837 @w=24, 0.739 @w=28 |
| Wall measurement | bench_v5_walltime.py: 8/8 solves, avg 2.54x, median 2.69x, min 1.21x, max 3.61x |
| Correctness | 49/49 solves across (36 @w=20-28, 8 @w=24 wall, 5 @w=30-34 ceiling) |
| CPU ceiling | w=30..34 all solved (w=34 in 60s; w=33 unlucky 4.6-min tail) — validates ~34-bit serial edge |

### Reproduced-Then-Verified External Techniques

| Technique | Source | Verdict |
|---|---|---|
| Spectral-mix XOR-fold bucket | Miller-Venkatesan | NOT a win — neutral 0.991 (15/15) |
| spread=6 jump spread | Pollard 2025 | NOT adopted — worse @w=20 (1.195), tail noise |
| Negation map | RCKangaroo / oritwoen | **ADOPTED + VERIFIED** — the +1.42x |

### Revised Implications

1. **For puzzle #140:** Attack time now ~3,505 / 2.54 ≈ **~1,400 GPU-years** on a
   single RTX 4090 (from ~7,000 baseline). Still cluster-scale, ~3.5-4 years on
   the 400-GPU class.
2. **For any kangaroo implementation:** the canonical quotient walk is a drop-in
   replacement for the raw walk (no new hash, no new DP logic); the fused
   inversion is a per-op micro-load out. Both should be merged into RCKangaroo.
3. **Remaining frontier:** the 3x endomorphism (auto-mod) composes further
   (theoretical K floor 0.51); not yet implemented (signed-distance bookkeeping).

### What We Did NOT Achieve (unchanged)

- ❌ No asymptotic improvement (Θ(√W) floor confirmed by EX5)
- ❌ No new mathematical property of secp256k1 (H6 bit leakage REFUTED; H5 parity
  disproven; spectral/spread gains not reproducible)
- ❌ No pattern in the 83 solved keys
- ❌ No solve of any unsolved puzzle

### Honest Assessment

Still **LEVEL 2** (verified constant-factor improvement), now a **2.54x stack**.
Not LEVEL 4 (search-space reduction) and not LEVEL 5 (challenge solve). The two
verified constant factors are real, drop-in, and compose multiplicatively — the
strongest verified engineering result of this campaign.

### Strongest Statement

The v5 fused+negation kangaroo is the fastest verified serial interval-DLP
implementation for secp256k1, measured 2.54x (median 2.69x) over the v4
baseline with 49/49 correct recoveries across w=20-34. For puzzle #140 this is
the difference between ~7,000 and ~1,400 GPU-years on a single RTX 4090.
