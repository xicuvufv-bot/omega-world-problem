# KAGGLE V5 FINAL REPORT — ULTRA-ECDLP VM

Synthetic interval ECDLP on secp256k1: k in [2^69, 2^70), 10 independent instances, per-instance wall budget 1200 s.

## Verdict

**TARGET_20MIN = TARGET_NOT_REACHED**

**Not measured on GPU.** CUDA payload is staged-only on this host (no nvcc/nvidia-smi). The 70-bit target is therefore NOT reached here; everything below marked cpu_measured is real but is the CPU reference, and the GPU numbers are explicitly withheld to honor the no-fabrication contract.

## Results (70-bit challenge)

| index | solved | verified | counted | steps | time (s) |
|---|---|---|---|---|---|
| 0 | 0 | 0 | 0 | 0 | 0.0 |
| 1 | 0 | 0 | 0 | 0 | 0.0 |
| 2 | 0 | 0 | 0 | 0 | 0.0 |
| 3 | 0 | 0 | 0 | 0 | 0.0 |
| 4 | 0 | 0 | 0 | 0 | 0.0 |
| 5 | 0 | 0 | 0 | 0 | 0.0 |
| 6 | 0 | 0 | 0 | 0 | 0.0 |
| 7 | 0 | 0 | 0 | 0 | 0.0 |
| 8 | 0 | 0 | 0 | 0 | 0.0 |
| 9 | 0 | 0 | 0 | 0 | 0.0 |

Instances solved & verified: **0 / 10**


## Scaling

Measured scaling alpha = 0.0595, R2 = 0.990.  NOTE: this fits
log2(steps) = a*bits + b over the measured bit range; the
low-bit range is dominated by a fixed per-run setup floor
(start-point scalar mults), so alpha here is NOT the clean
O(sqrt(N)) exponent that asymptotically applies to the
engine's walk.  It is reported as measured, not as a theory
prediction, per the honesty contract.

## Method

Parallel kangaroo, affine-x driven walk, representation-independent DP predicate, warp-batched Montgomery-trick inversion (1 Fermat inverse per 32 lanes), concurrent dual-GPU rounds with host merge + kG==Q re-verification.

## Honesty statement

This report contains only what was measured at runtime (or explicitly marked staged / withheld). No projected GPU number is presented as measured. The benchmark definition is unchanged from the mission.

