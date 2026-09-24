# STATE_SNAPSHOT — MISSION v4 (Kaggle T4x2 → synthetic 70-bit ECDLP)

Date: 2026-09-23. Pre-mission baseline (v3 portfolio state, intact).

## Environment reality (measured, no fiction)
| Check | Result |
|---|---|
| GPU / nvidia-smi | NOT PRESENT (command not found) |
| CUDA / nvcc | NOT PRESENT |
| kaggle CLI | NOT PRESENT |
| cupy / pycuda | NOT INSTALLED (import fails) |
| CPU | AMD Ryzen 3 3200G (4 cores / 4 threads, Zen+, 2019) |
| Integ. GPU | Radeon Vega 8 (shared) — not CUDA-capable |
| RAM | ~14.9 GB usable |
| Compiler | gcc.exe 16.1.0 (MinGW-Builds, x86_64-posix-seh) |
| Python | 3.11.9 |

**Consequence**: the mission's #2 rule ("if T4x2 is not available: don't lie, log actual
environment, stop 70-bit validation") applies **locally**. The TARGET_20MIN (1200 s)
cannot be demonstrated on this box. This snapshot records the actual environment and
the 70-bit validation is dispatched to a Kaggle T4x2 payload instead — leaving a
NO_FICTION stub locally.

## What is carried forward (verifised, do NOT rebuild)
- Verified structural facts (p, l=prime order, t, cofactor=1, D=-3*2419^2, k>1999,
  non-anomalous, GLV eigen lambda, l-1 factors) — v3 report.
- Golden baseline L1 (genuinely varied prime orders): bsgs alpha=0.4974 R^2=1.0;
  kanga unstable alpha=0.519 R^2=0.68. L2 depth lanes 2^22..2^30.
- Independent reproduction alpha=0.4876 R^2=0.993 (7 curves, separate solver).
- 1000-entry hypothesis bank (families A-T; 832 CONSTANT / 144 REFUTED / 24 HYPOTHESIZED).
- Falsified probes: PN-1 multi-target rho (slope vs log2 K = -0.02..-0.15), PN-2 GLV
  interval lattice (no collapse), PN-4 Semaev control (O(p) relation surface).
- Contract: solvers.solve(row, method, seed), ok-gate = independent verification.
- Kaggle runner with strict numeric merge guard (no-fabrication policy).

## What v4 adds (this mission)
1. A fresh **max-performance backend** engineered for real measurement on a T4x2:
   - C++17 (gcc) CPU reference engine, compiled and benchmarked LOCALLY (honest, real ops/sec).
   - CUDA (nvcc) kernels for the T4x2 payload: field/point-ops benchmark + kangaroo.
2. Zero-guess BASELINE (field/point/complete-step ops/sec measured on real hardware).
3. Scaling validation 2^16..2^70 (as resources allow) with alpha/R2.
4. Synthetic 70-bit challenge: interval [2^70,2^71), k hidden by seed, Q=kG,
   independent verifier, 10 instances, stats (mean/median/min/max/p90/p95).
5. Final honest verdict: TARGET_20MIN = ACHIEVED or NOT_REACHED — only from real runs.

## Staging plan (validated for real on Kaggle)
- Local: compile C++ engine with gcc, microbench (real numbers), scaling to what fits,
  write BASELINE.csv/BASELINE.json + AUTOTUNE.csv (CPU or stub, clearly labeled).
- Kaggle payload: detect GPUs → verify count/model/memory → verify CUDA → compile
  .cu → self-test → microbench → batched kangaroo → 10x70-bit challenge → stats →
  FINAL_PERFORMANCE.csv → KAGGLE_70BIT_FINAL_REPORT.md → TARGET_20MIN verdict.
- Any GPU number in local deliverables is tagged MEASURED_CPU / STUB_GPU / UNVALIDATED.