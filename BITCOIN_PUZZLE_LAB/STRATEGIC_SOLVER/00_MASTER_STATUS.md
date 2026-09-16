# 00 — Master Status

**Date:** 2026-09-15
**Pipeline:** ACTIVE
**Session goal:** At least one major verified breakthrough on the most scientifically promising Bitcoin Puzzle target.

---

## What We Have

| Asset | Status |
|---|---|
| 83 published solved keys | Verified 83/83 end-to-end (privkey -> pubkey -> hash160 -> address) |
| 77 unsolved puzzles | 72 R1 (address-only) + 5 R2 (exposed pubkey) |
| 4 solver implementations | v1 naive, v2 stride, v3 BSGS, v4 kangaroo |
| Fused kangaroo | **2.0x speedup verified** (EX4, 36 cases) |
| Curve analysis | Cofactor 1, j=0, GLV exists but doesn't help walks, Θ(√W) floor confirmed |
| Structure search | **ALL NEGATIVE** — no PRNG, no low-bit, no hamming, no Benford, no relative-position bias |

## What We Found (Verified Results)

1. **Fused single-inversion kangaroo: 2.0x constant-factor improvement** — reduces per-hop modular inversions from 2 to 1. Measured on 36 synthetic test cases. Same key recovery, same walk identity, same memory.

2. **All 83 keys are uniform random draws** — no exploitable structure across 11 statistical metrics on train/test splits. No PRNG fingerprint across 6 strategies.

3. **secp256k1 has no asymptotic shortcut** — cofactor 1, prime order, GLV doesn't reduce walk-step cost. Θ(√W) floor is real.

## Current Target

**Puzzle #140** — smallest R2 (exposed pubkey), 140-bit interval DLP.
After fused kangaroo: ~1,998 GPU-years single-GPU (down from ~4,000).
With 400× RTX 4090 (RetiredCoder class): ~5 years wall-time.

## Key Risk

#140 at ~2,000 GPU-years after optimization is still OUT OF REACH for any single machine. This is a cluster-scale project. The honest breakthrough gate is at w≤28 on CPU (verified), or w≈33-34 as the CPU ceiling.

## This Phase (EXP-N1..N4)

- v5 (fused single-inversion + even-y W/2) confirmed as the best constant: K ~4.2-5.0 vs v4 ~5.99 (36/36 gate).
- **GLV order-3 × negation quotient (v6) REFUTED by measurement** — automorphism folding gives zero meeting-space reduction for bounded additive kangaroo (folded candidates fired 0/16; canonical min-x bucket walk collapses to 13 states in 372 hops); K-floor 0.51 unreachable. Full analysis: `SOLVER_LAB/candidate/v6_glv_negation.py` + `EXP-N2`.
- Multi-herd parallel: no wall gain on this box (serial trail ~23.7k steps dominates; host ceiling ~1.6×).
- Infeasibility quantified: #67 ≈ 173 CPU-days/core + hundreds of GB trail RAM (2^32.5 stored entries); #140 ≈ 4.1e10 core-years. Both remain compute- and memory-blocked.
- Every solve dual-verified (scalar-mult identity + native C engine); full suite 171/171 `pytest`.
- Log: `SOLVER_LAB/reports/experiment_log.md`, `exp_n2_results.json`, `exp_n3_results.json`.

## Safety Boundary

- No real-fund extraction
- No private key guessing on live addresses
- Synthetic toy keys only for testing
- Published keys are public-record data for verification
