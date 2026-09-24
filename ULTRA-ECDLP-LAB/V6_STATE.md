# V6_STATE — ULTRA-ECDLP-LAB audit (V6 Phase 1)

Date: 2026-09-24. Purpose: exact starting point for the V6 research engine.
Nothing below is rebuilt if it is already correct.

## 1. Architecture

```
research/v4/                  PRIMARY STACK (V5 mission payload)
  kangaroo_cuda.cu            CUDA payload: dual-T4, concurrent per-device
                              worker threads, warp-batched Montgomery inversion
                              (1 Fermat inverse per 32 lanes), affine-x walk,
                              PRE-jump DP records, host merge + kG==Q re-verify.
                              cmds: selftest bench scale solve prof
  v4_cpu_engine.cpp           Validated CPU reference (selftest/bench/scale/solve)
  challenge70.py              Synthetic generator (SHA256(seed)->k, bit-forced
                              interval) + independent verify_instance
  challenges.json             Sealed 10x70-bit instances [2^69, 2^70)
  detect_env.py               Real env probe -> KAGGLE_ENVIRONMENT.json
  kaggle_v5_run.py            28-phase gated pipeline (env/build/selftest/
                              bench/prof/single/dual/batch/autotune/probes/
                              solves/stats/verdict/repro/scaling/leak/speedup)
  kaggle_70bit_run.py         Earlier runner (superseded, kept)
tests/                        run_all.py (10 checks) + test_secp256k1.py
build.py                      Portable driver (cpu/cuda/micro/tools/all/clean)
src/                          v1-v2 microbench corpus (fp/ec/perf kernels)
research/                     v3 corpus (solvers.py, gen.py, hypothesis lab)
```

## 2. Field arithmetic (4x u64 little-endian, verified CPU-side)

- add/sub plain with carry chains; mulRaw 4x4 schoolbook + reduceMod;
  Fermat pow/inv. CPU selftest proves distributivity + 2G-jDbl == scalarMult.
- GPU mirrors are line-identical in structure (V5_AUDIT.md).

## 3. Point arithmetic

- Jacobian double + add-affine; affine conversion via Fermat inverse (CPU)
  or warp-batched inverse (GPU). Infinity = Z==0 (`jpInf`), identical both sides.

## 4. Walk / collision design

- Jump table W_=64, IDENTICAL on all devices (fixed seed, wbits=bits/2).
- Starts: tame = random interval point, wild = random interval point + Q.
- Step rule: idx = ax[0] & 63, affine-x driven. DP predicate: low `dpbits`
  of ax == 0. Records are PRE-jump (x, d).
- Host merge on affine-x hex: tame/wild pair -> k = D_t - D_w -> verify kG==Q.
- `walkKernelSimple` is DEAD (post-jump convention) — do not enable.

## 5. Status of the GPU path (as of this writing)

- Compiles on nvcc 12.8 sm_75 (3 real fixes from first T4×2 contact:
  u32 typedef, atomicExch volatile cast, __constant__ mirrors).
- **OPEN DEFECT (under diagnosis): `selftest` spins 900 s with zero solves
  (rc=124), on a 24-bit known key that should fall in round 0.**
  Prime suspect: device-side constants wrong on the session host
  (hand-transcribed patch; merge-verify then fails silently forever).
  Fix in flight: derive constant limbs programmatically from challenge70.py.
- Per-step cost unmeasured (Fermat inverse per warp per step is the
  known expensive core; register pressure vs -maxrregcount=80 unknown).
- Dual/single efficiency unmeasured. T4×2 scaling unmeasured.

## 6. Measured CPU ground truth (local, reproduced from clean clone)

- fpMul 8.9e6/s, fpInv ~20k/s (50175 ns), point-madd ~7e5/s.
- CPU selftest: 32-bit solve found=1, independent verify=1.
- Scaling (bits 16-34): log2(steps)=0.0595*bits+b, R2=0.990 (setup-floor
  dominated; documented, not theory).
- tests/run_all.py 10/10 in workspace AND two fresh clones; pipeline
  artifacts byte-reproducible.

## 7. Failed hypotheses (do not retry without new evidence)

- F1 serial dual-GPU rounds (measured-by-design flaw) -> FIXED (workers).
- F2 `walkKernelSimple` post-jump records mixable with batch kernel -> DEAD.
- F3 `constexpr` host arrays visible to device code -> REFUTED (ODR-use by
  pointer needs a device symbol).
- F4 `__constant__` hidden under `#ifdef __CUDA_ARCH__` -> REFUTED (host
  stub must register the symbols; mirrors unconditional, redirects only).
- F5 "T4 numbers from a non-CUDA box" -> FORBIDDEN (honesty contract).

## 8. Surviving hypotheses (to be proven on T4×2)

- S1 concurrent dual-device rounds ~= single-device time.
- S2 warp-batched inversion amortizes to ~1/32 Fermat cost.
- S3 DP auto-tune + tiered starts reach 10x70-bit in <=1200 s each.
- S4 combinations from external components beat the current kernel.

## 9. What V6 must not redo

- Re-verifying CPU field/point ops, the merge math, the generator/verifier,
  the pipeline gates, the release hygiene (all DONE + committed).
- V6's job: EXTERNAL ideas -> adapted components -> measured deltas on T4×2,
  plus closing the open selftest defect.
