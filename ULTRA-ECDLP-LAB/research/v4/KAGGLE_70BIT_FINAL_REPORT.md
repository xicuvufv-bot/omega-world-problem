# KAGGLE 70-BIT FINAL REPORT — ULTRA-ECDLP-LAB

Synthetic interval ECDLP: secp256k1, k in [2^69, 2^70), 10 independent instances. Target: solve all below 20 min wall.

## Verdict

**TARGET_20MIN = ** NOT_REACHED  
Every figure below is **NOT measured.** CUDA payload is STAGED ONLY (no nvcc on this box); local rows are CPU baseline. Nothing here claims GPU performance.

## Results

| index | solved | verified | steps | time (s) |
|---|---|---|---|---|
| 0 | -- | -- | -- | staged |
| 1 | -- | -- | -- | staged |
| 2 | -- | -- | -- | staged |
| 3 | -- | -- | -- | staged |
| 4 | -- | -- | -- | staged |
| 5 | -- | -- | -- | staged |
| 6 | -- | -- | -- | staged |
| 7 | -- | -- | -- | staged |
| 8 | -- | -- | -- | staged |
| 9 | -- | -- | -- | staged |

## Measured rate

No GPU measurement (no CUDA toolchain locally). Projected GPU steps/s are withheld rather than fabricated.

Local CPU reference (measured, v4_cpu_engine, dpb=12): 69600 steps/s derived from BASELINE_cpu.csv rows.

## Method

Parallel kangaroo with affine-x-driven walk and representation-independent DP predicate (fix for the v4 CPU bug class).  Per-step inversion warp-batched (Montgomery trick, 1 Fermat inverse per 32 lanes).  Recovered k is re-checked in the payload (k*G==Q) and independently in Python by this orchestrator before counting.

## Reproduce

Local CPU baseline: `v4_cpu_engine.exe` (validated selftest + scale).

GPU box:
```
nvcc -O3 -std=c++17 -arch=sm_75 -Xptxas -O3 -lineinfo \
  -maxrregcount=80 -o kangaroo_cuda kangaroo_cuda.cu
./kangaroo_cuda selftest      # gate: known-key, must match
python kaggle_70bit_run.py    # bench + 10 solves + verify
```
