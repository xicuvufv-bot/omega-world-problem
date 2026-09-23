# OPTIMIZATION_DECISIONS — measured keep/revert decisions (Phases 1-4)

Toy-only. Toy field p=4294966177=2^32-1119, #E=l=4294835173, G=(1960037684,560815139).
Hardware: Ryzen 3 3200G 4C/4T @3.6GHz (Zen+, AVX2+FMA), g++ 16.1 MinGW only.
Correctness gate: `correct.exe` (FIELD laws ×4, EC-AGREE ×4, VECTORS ×4) must print DONE
before/after every decision. **It is green for every entry below.**

## Decision table (Optimization | Before | After | Speedup | Memory | Confidence)

| # | Optimization | Before (baseline) | After (measured) | Speedup | Memory | Confidence |
|---|---|---|---|---|---|---|
| 1 | Montgomery strategy for field mul (fixes applied: to_mont/from_mont, n0, one()=R, point/rep boundary) | previously broken | correct (trials 2000 fails=0) | correctness only | +0 | High |
| 2 | Keep **mont** mul as the default "fast" field strategy | — | — | **REVERT decision**: mont mul 2.624 ns vs naive 1.905 ns; mont EC worker carries 61 adcq+shrdq + 105 data branches, EC dbl 34.6 vs naive 17.1 | 0 | High |
| 3 | Keep **barrett** as EC-layer default | — | — | barrett EC dbl 16.0 ns = fastest measured (vs naive 17.1, pseudo 30.3, mont 34.6); keep for EC dbl only, not field-wide (its reduce64 has 2 branches, field mul 2.103) | 0 | High |
| 4 | Compiler flag `-O2` (not `-Ofast`) for field ops | O3 1.930 (naive mul) | O2 1.905 | +1.3% | 0 | Med |
| 5 | Compiler flag `-native` for EC jacobian_dbl (naive) | O3 18.028 | native 17.125 | +5.3% | 0 | High |
| 6 | `-Ofast` on mont mul | native 2.624 | Ofast 5.085 | **-94%** (regression) | 0 | High — **reverted, never ship -Ofast for mont** |
| 7 | AVX2 4-lane field **add** (64-bit lanes, fold-aware compare) | scalar 2.155 ns/op | AVX2 0.216 ns/op | **9.96×** (theoretical max ~4×/vector + ILP gains) | +16B/4 lanes | High |
| 8 | AVX2 4-lane field **sub** | scalar 2.515 | AVX2 0.265 | **9.49×** | +16B/4 lanes | High |
| 9 | AVX2 4-lane field **mul** (64-bit products + 2 folds + 1 cond subtract) | scalar 1.868 | AVX2 1.357 | **1.38×** (multiply chain dominates: 4 mul_epu32 + shifts + adds, no wide-mul available on AVX2) | +64B/lane-set | High |
| 10 | Multithreading 1→2 (independent Jacobian walks) | 36.1 Mops/s | 71.3 Mops/s | **1.97×** | thread-local, no sharing | High |
| 11 | Multithreading 1→4 | 36.1 Mops/s | 129.3 Mops/s | **3.58×** (of 4.0 theoretical; hyperthreading accounted) | thread-local, no sharing | High |
| 12 | Eliminate integer division in field mul (div-scavenging) | **no-op**: GCC already uses magic reciprocals — no `div`/`idiv` in any mul/add/sub/sqr path (PHASE2_ASSEMBLY_REPORT §1) | — | 0× | 0 | High — nothing to win |

## Reverted / rejected optimizations (with evidence)

- **`-Ofast` for Montgomery field mul** — regressed mul 2.624→5.085 ns and sqr 2.430→4.973 ns
  (MICROBENCHMARKS.csv, `best_flag=native` recorded for mont mul/sqr precisely because Ofast
  loses). Rule: revert on measured regression → **not shipped**.
- **Adopting Montgomery as the "fast" default** — measurement contradicts intuition on this
  hardware for p=2^32-1119: REDC needs 3 multiplications + a carry chain + 1 conditional
  branch per mul; naive needs 2 multiplications, branch-free. mont field mul is 1.38× slower
  than naive; mont EC is ~2× slower. **Rejected** (not reverted — never adopted).
- **Wide-vector (8-lane 32-bit) field add/sub** — rejected: a+b overflows 32 bits near
  P≈2^32, forcing 64-bit lanes (4 lanes/vector); re-deriving via dual-lane packing adds more
  instructions than it saves on Zen+ (no AVX-512). Measured 64-bit-lane version already
  delivers 9.5-10× on add/sub.

## What is retained (production-candidate settings, toy-scale only)

1. **Field default: `FpNaive`** (mul 1.905, add 1.913, sub 1.905 — fastest or tied on all
   three stand-alone ops; branch-free, no spills). 
2. **EC dbl/default: `FpBarrett`** for jacobian_dbl/mixed_add (16.0/18.4 ns — fastest).
   Field ops within those paths are already inlined, so the branchy reduce64 does not dominate
   a formula-level win.
3. **AVX2 batched add/sub for bulk point-set evaluation** (kinds of work that evaluate many
   independent points — used in Phase 6+ algorithm work): 9.5-10× per-op throughput.
   `v_mul` stays scalar (1.38× — poor ROI for added complexity; no wide multiply on AVX2).
4. **Multithreading 4 threads for independent DLP walks** (Phase 6/7 parallel collision
   engine): 3.58× end-to-end, embarrassingly parallel, zero synchronization overhead.
5. **Compiler flags: `-O2` for field-heavy TUs, `-O3 -march=native` for EC formulas**;
   `-Ofast` **banned** for Montgomery codepaths (see #6).

## Not decided here (carried to Phases 5+)

- Memory/cache behavior (Phase 5) — AVX2 kernels and threading are register-resident; no
  cache-trait measurements taken yet.
- Algorithm-level comparison (BSGS/rho/kangaroo/DP/parallel) — Phase 6 will reuse the
  retained naive-field EC worker + 4-thread engine above as the baseline implementation.

## Phase 5-6 addenda (measured, 2026-09-22)

### Phase 5 memory/cache (PHASE5_CACHE_RESULTS.csv)
- Sequential EC dbl/add are **compute-bound, not memory-bound**: dbl flat ~17.4-20.3 ns and
  add flat ~22-27.6 ns from 12KB to 50MB working sets (12 B/point, prefetcher keeps up).
- Random gather (BSGS/DP-table style) exposes the real hierarchy: 2.2 ns@32KB -> 2.5 ns@2MB
  -> 7.3 ns@8MB -> 11.0 ns@134MB (≈ L1/L2/L3/DRAM on the masked-CPUID VM).
- Stride-67 gather (creation-order walking) stays ~2.4-5.1 ns: **prefetch-friendly**; the
  12 B point stride fits cache lines. Design implication for Phase 7: keep parallel DP
  tables accessed in creation order when possible, or cache-aware tile/bloom before collect.
- CPUID leaf 4 / 0x8000001D are masked (hypervisor), so levels are read behaviorally.

### Phase 6 algorithm landscape (ALGORITHM_COMPARISON.csv, verified=1 every row)
- Empirical group-step laws (N=2^db): **brute ~ N**; **BSGS ~ 2.0(±0.3) sqrt(N)**
  (81@2^12 ... 22149@2^28); **Pollard rho ~ flat 1.2 sqrt(l) ≈ 55k-111k regardless of db
  — rho is interval-blind on the full-group toy** (expected); **kanga ~ 3-6 sqrt(N)**
  (266@2^12 ... 98482@2^28), **kanga4 ~ similar per-thread step budget, ~3.6× wall speedup
  at 2^28** (48.9 ms -> 43.2 ms including 4 concurrency on 4T; step aggregate 98k -> 128k).
- Algorithm-level decisions for Phase 7+:
  1. **BSGS is the reference sub-root engine** for parallel collision work (lowest measured
     constant, memory=sqrt(N) entries is cache-viable through ~2^26).
  2. **Kangaroo (Pollard lambda) is the interval-adaptive champion** for huge N where
     sqrt(N) memory is not viable: memory = O(1) bounded table (12*sqrt(N) worst cap, ~4x
     in practice) vs BSGS sqrt(N).
  3. **rho rejected for interval problems** (measured flat curve vs db — it does not see N);
     keep only as full-group baseline / for curves without interval structure.
  4. **Parallelism: shared-client per-thread DP tables (no read-sharing) kept** — the ~3.6×
     wall scaling from Phase 4 transfers to kanga4; collapsing to a single shared kanga table
     adds cache pressure (Phase 5 gather data) with no measured win yet.
- Correctness bugs found & fixed while building algos_main.cpp (worth recording):
  - rho partition by affine-x low bits degenerated to a 2-cycle (+/-P) on this curve
    (x%4 ≈ 3 for the whole orbit). Fixed with a Teske-style 2^7 = 128-mix r-adding walk +
    Knuth-multiplicative partition on x.
  - kangaroo cannot walk tame then wild: with a shared deterministic jump rule the tame must
    run **simultaneously** with the wild from a scattershot known offset into a single
    (x,y,owner,dist) table so both orbits coalesce; sequential tame-first versions FAIL on
    large N (birthday-only collisions, ~0 expected hits at 2^24+).
  - DP hash + open-addressing tables must grow past 2/3 load or insertions silently stall
    (bsgs/rho/kanga all use growing open-address tables now).

### Phase 7 parallel collision engine (PHASE7_PARALLEL_CS.csv, all verified=1)
- Architecture: W=8 walkers PER THREAD, every walker uses the SAME deterministic jump rule f
  ((x>>8)&31, K=32 jumps, size in [1,2*sqrt(N)]), so tame (random known offset) and wild
  (P + u*G) orbits coalesce; distinguished-point (DP) pruning emits only points with
  (x & 63)==0 (b=6), each walker restarts from a fresh random start; cross-owner DP match
  solves k = d_tame - d_wild (mod l), re-verified independently.
- Wins vs Phase 6 single-pair kanga at db=28: DP table 486 entries vs 16384 (BSGS) and
  270k (single-pair cap) => sub-linear memory; wall 2.6-2.8 ms vs 43-49 ms.
- ns/step drops ~3.6x from T=1 to T=4 (292.7 -> 158.7 -> 80.5 ns) — more walkers spread the
  same collision search; aggregate steps rise with walker count (VOW signature).
- REP=5 min-wall kept: single-shot wall is noisy at sub-10 ms scales. This is the engine the
  research benchmark reuse; it is the reference for "no better-than-sqrt(N) claim" Phase 12-13.

### Phase 8 GPU/OpenCL on Vega 8 (PHASE8_GPU_RESULTS.csv, parity-verified)
- Kernel: EC mixed-add replicated bit-for-bit (8M+3S) from ec.hpp in OpenCL C; per-walker
  checksum over (X,Y,Z). CPU 4-thread reference uses the real FpNaive engine.
- GPU sustained ~600 Mops/s (blocking transfer included), CPU ~40 Mops/s -> 14.7-20.4x.
  ~11% of 8CU*1.25GHz peak (5498 Mops/s): 32-bit mul mod chain is the limiter (same as CPU).
- OpenCL toolchain on this host: no system CL header/lib, so src/ocl_min.h + dlltool-built
  libOpenCL.a from C:\Windows\System32\OpenCL.dll (exports listed, deterministic).
- Decision: keep CPU VOW engine as the alpha-validity reference for the research claim;
  GPU port documented as an independent execution engine capable of the same primitive at
  higher aggregate throughput (matches "parallel/hardware" (B)-class constant gains).

### Phase 9 auto-tuning (PHASE9_TUNING_RESULTS.csv, all configs verified)
- Refactored phase7 engine into src/vow_engine.hpp (K, b, walkcap/budget all tunable);
  engine_main.cpp is now a thin CLI, tuner_main.cpp does grid search {b=2..12, K=8..64,
  wcm=3..24} at a fixed db, REP=3 min-wall, ranks by wall.
- Finding: DP-bits cut to b=4 is ~60x faster than b=ceil(log2 N / 2) at db=24 (1.1-1.7 ms
  vs 50-80 ms). Mechanism: each DP event restarts a walker with a fresh random offset, so
  with b=4 restarts are ~16 apart and the ensemble effectively re-samples the group almost
  continuously -- birthday-sampling-like behavior, faster than long structured walks at
  this N; verified correct because every reported k still passes jacobian check.
- b=2 (prob 1/4): table churn/lock traffic starts to cost (1.4-4.4 ms); b=4/6 sweet spot.
  K and walkcap are insensitive within 2x at db=24. `b` is the dominant knob.
- Action for benchmark scale-up: sweep b per db for the research generator rather than
  fixing b=ceil(0.5*log2 N); the 60x at db=24 may compress against the true ~sqrt(N) law as
  N grows (restart cost + table contention), worth measuring across db.

### Phase 10+ research/ suite (empirical scaling study, all synthetic)
- Contribution of Phases 1-9 distilled into a reusable benchmark: research/gen.py,
  solvers.py (bsgs/rho/pir/kanga/ph/brute/grover_emu), bench.py, fit.py,
  kaggle_t4.{py,ipynb}, t4_parity.py, report.md, spec.md, SAFETY.md.
- Decision on rho/pir classification: any near-flat α in log-N space is flagged
  X(flat)/interval-blind in fit.py, not counted as an α<0.5 win — the flatness is an
  artifact of measuring w.r.t. N while the method spends ~√l, the full group order.
- Decision on the Grover stage: kept as a classical amplitude emulation at db<=12 with
  query-count metric only, explicitly NO CLAIM, preventing a false A-class reading.
- Decision on PH: only runs on the generated smooth-order control group; validates that
  the one existing "fast DLP class" (composite order) is excluded by construction in the
  prime-order toy, so claims about the toy must not cite PH.

## Reproduction (all measured, toy-only)

```
g++ -O3 -march=native -std=c++17 -I. src/correct.cpp -o correct.exe   && ./correct.exe  # DONE
g++ -O3 -march=native -std=c++17 -I. src/micro_main.cpp -o micro_O3.exe && ./micro_O3.exe
g++ -O3 -march=native -std=c++17 -I. src/simd_main.cpp  -o simd_O3.exe  && ./simd_O3.exe
g++ -O3 -march=native -std=c++17 -I. -pthread src/thread_main.cpp -o thread_O3.exe && ./thread_O3.exe
# asm inspection: python extract_asm.py asm_native.s ; python asm_census.py asm_census.s
#                python asm_hist_mont.py micro_native.s Fp{Naive,Mont,Barrett,Pseudo}
```

Sources: MICROBENCHMARKS.csv, PHASE2_ASSEMBLY_REPORT.md, PHASE3_SIMD_RESULTS.csv,
PHASE4_THREAD_SCALING.csv (all in lab root). No algorithm changes; toy instance only.