# V5_AUDIT — Pre-mission code audit of the T4x2 payload

Date: 2026-09-24 — Mission snapshot (v4 → v5). Review of `kangaroo_cuda.cu` (832 lines)
and `v4_cpu_engine.cpp` (466 lines) line-by-line against the mission honesty contract.

## 1. Correct (verified by reading + CPU cross-consistency)

| Item | Where | Note |
|---|---|---|
| Field ops | `.cu` L79–149 | fpAdd/fpSub/fpMul/fpSqr/fpPow/fpInv identical to CPU engine; same reduceMod (CP_=2^256−p). |
| nAdd/nSub | `.cu` L150–161 | mod-n distance arithmetic bit-identical to CPU. |
| Jacobian dbl/add | `.cu` L171–210 | jDbl/jAddAff are **copy-equivalent to CPU** (verified instruction-by-instruction). Infinity checks now `if(jpInf(P))`/`if(jpInf(J))` matching CPU after the earlier fix. |
| Affine-x walk | `.cu` L373–410 | Jump tap = `ax[0]&(W_-1)`, DP predicate on affine x — representation-independent fix for the CPU bug class. |
| Batch inversion | `.cu` L331–371 | Montgomery-trick warp invert: prefix scan `pre`, one Fermat `fpInv` on lane 31, suffix scan `s`, out = inv·prefix·suffix. **Math re-verified**: exclusive prefix of lane−1 × inv(product) × exclusive suffix = 1/den_i. Correct. |
| DP record convention | `.cu` L398–404 | Batch kernel records PRE-jump `(ax,d)` — all walkers consistent, so merge valid. |
| Collision key recovery | `.cu` L495–499 | `k = d_t − d_w mod n`, `kind==1` wild vs tame handled both directions. Re-verifies `kG==Q` on host before accepting. |
| Selftest gate | `.cu` L615–635 | Known 24-bit key `0x8A1B2C`, host compares recovered k. Abort-on-fail via rc. |
| Step counting | `.cu` L326/L409 | Per-walker actual `ran` written; host sums — **honest steps, not maxSteps·nStart**. |
| Full-warp guard | `.cu` L518 | `nStart%256` enforced. |
| Identical jump seed | `.cu` L552 | `0x0BADF00DCAFEBABE` on every device — cross-device merge valid. |
| Independent verifier | `kaggle_70bit_run.py` | Pure-Python `k*G==Q` + interval check; smoke-tested (10 True, negative False). |

## 2. Suspicious / needs on-device confirmation (why V5 war-room exists)

- `warpBatchInv` correctness rest on **full-warp lockstep**: `__shfl_sync(0xffffffff)`
  requires every convergence test to see all 32 lanes active. `nStart%256` guard is in
  `runSolve`/`runScale`/`runProf`/`bench` but **only asserted in `runSolve`** — bench/prof/
  scale check it implicitly via nStart=2^20/2^14. The stop-flag read is whole-warp
  (`if(*stopFlag)`) so no lane diverges. Confirmed on-device only by selftest passing.
- `walkKernelSimple` (**dead code**, `.cu` L295–327): kept as cross-check reference.
  It records **post-jump** `(ax,d)` — a DIFFERENT convention than the batch kernel.
  If ever wired into the merge it would still be self-consistent (all its own walkers),
  but must NOT be mixed with batch DPs. Flagged: do not enable without DP-convention audit.
- `fpNeg` (`.cu` L136–139): returns 0 for nonzero inputs (matches CPU's identical oddity);
  **unused** in the walk, so harmless, but marked fragile — do not start using it.
- jDbl's defensive `if(!isZeroN(P.Y)) return jpZero` (`.cu` L174): mirrors CPU exactly;
  for order-2 inputs returns infinity. secp256k1 cofactor=1, but defensive path is
  reachable only for degenerate walk points, which the walk can't produce (d in subgroup).
- `maxSteps` formula (`.cu` L530–532): `((1<<14)<<dpbits)/nStart` clamped to [1, 2^26].
  At dpb=24, nStart=2^19 → 2^19 steps/walker/round — on-device runtime per round to be
  measured (prof). Worst case per round could reject merge cadence tuning.

## 3. Slow (measured on CPU; GPU shares the arithmetic shape)

- `reduceMod` is the plain iterated right-shift reduction (up to 6 iterations of
  `hi*CP_ + lo` with carry propagation). Simpler than Montgomery/Barrett but multiplies
  the MUL cost by ~2–3×. This is the #1 single-variable field-arithmetic candidate for
  Phase "field impl benchmark"; keeping reduceMod as correctness baseline.
- `fpInv` is a full 256-squaring Fermat pow (fpPow, L140–149). Amortized to 1/32 lanes in
  the batch kernel, but still the dominant per-step cost (~380 muls-equivalent per warp/step).
- `mergeDps` (`.cu` L485–509) is host-side `std::unordered_map<std::string,…>` keyed by
  hex string — fine below ~2^16 DP/round, a real host bottleneck if round sizes grow
  toward 2^20. Phase "async execution / batching" will measure.
- Field ops are 32-bit-friendly (4×u64 with u128) — compiled sm_75 targets ~80 regs
  budgeted (`-maxrregcount=80`). Actual occupancy needs `cudaFuncSetAttribute` probe.

## 4. Untested (must run on the T4x2; nothing below is claimed yet)

- Everything GPU: compilation (nvcc 12.x, sm_75), selftest, bench, prof, solve, scale.
- Dual-GPU concurrency was **just restructured** (L557–594): previously the round loop
  walked device 0 fully (sync + readback) then device 1 → wall time ≈ 2× single-GPU, i.e.
  T4-DUAL would have measured ~1×, not 2×. Now each device walks in its own worker thread
  concurrently and DPs are merged after join. This is the exact defect that would have
  fooled Phase "dual T4" — the fix must be validated by `parallel_efficiency>=0.9`.
- `runProf` (new, L696–770) times host→device, kernel+sync, device→host, merge — the
  Phase "async/streams" inputs.
- Occupancy/registers/spills unmeasured (the only CUDA build here has no nvcc).

## 5. Must-remain unchanged (contract anchors)

- Interval convention `[2^(B-1), 2^B)`, B=70; k derived from seed; Q=kG; solvable only
  by walk replay. Sealed `challenges.json` (10 instances, base_seed 12648430).
- Field/point arithmetic bit-identical CPU↔GPU (selftest gate enforces).
- DP = affine-x predicate; jump table identical across devices.
- `solution_verified==true` requires `k*G==Q` byte-exact via independent Python verifier.
- `wall_time<=1200` per instance; 10/10 needed for TARGET. Honesty contract; graded
  result field `proven` is true only if measured+verified.
- Do NOT target real Bitcoin puzzles — hours of CPU time is the hard ceiling in the
  mission; the PTRACE-only deployment is as designed.

## 6. Immediate action items before T4x2 build (V5 pipeline does these)

1. Build command exactly: `nvcc -O3 -std=c++17 -arch=sm_75 -Xptxas -O3 -lineinfo -maxrregcount=80`.
2. Hard gate sequence: build → selftest → bench(3s) → prof(3s) → single-T4 solve probes
   (16/24/32/40-bit) → dual-T4 parallel-efficiency probe → contest solves.
3. `KAGGLE_ENVIRONMENT.json` must record `gpu_count==2`, model T4, VRAM before any 2-GPU claim.
4. No single-run winner without reps; every CSV row gets `src` column (measured/staged).