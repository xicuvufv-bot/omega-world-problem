# ULTRA-ECDLP PERFORMANCE LAB — progress tracker

Toy-ECDLP performance lab. All work is local / generated / toy-only (see SAFETY.md).
Timestamp line 39: p=4294966177 (2^32-1119), p≡1 mod 3, #E=l=4294835173 prime,
G=(1960037684,560815139). DLP solved exactly at levels 2^16..2^32 (k clamped to [1,l)).

## Milestones
- [x] Phase 0 (audit): toolchain (g++ 16.1 only; clang/MSVC/cmake absent), CPU (Ryzen 3 3200G 4C/4T),
      SIMD (SSE2..AVX2+BMI/ADX; no AVX-512), memory, GPU (Vega 8 iGPU, OpenCL 2.1, no CUDA).
      -> HARDWARE_REPORT.md
- [x] Toy instance: prime-order curve instance.hpp + dlp_vectors.txt (generated & doubled-checked by ref/gen_instance.py).
- [x] Correctness suite (src/correct.cpp) green on all 4 field strategies:
      field laws, affine-vs-Jacobian agreement, independent DLP vectors. (2026-09-22)
- [x] Phase 1: microbenchmarks (field ops, EC formulas) -> MICROBENCHMARKS.csv, PERFORMANCE_BASELINE.md
- [x] Phase 2: asm inspection of hot paths -> PHASE2_ASSEMBLY_REPORT.md
      (2026-09-22: no idiv anywhere in mul/add/sub/sqr paths (GCC already uses magic
      reciprocals / folding); mont carries 61 adcq+shrdq carry chains + 105 data branches in
      the EC worker => its ~2x EC tax is intrinsic; barrett wins EC dbl 16.0ns; pseudo needs
      0 128-bit mulq but 2 folds/op cost it at EC layer.)
- [ ] Phase 3: SIMD-verified ops
- [ ] Phase 4: multithreading (1/2/4/N threads)
- [x] Phase 3: SIMD ops (AVX2 4-lane add/sub/mul, all validated vs scalar) ->
      PHASE3_SIMD_RESULTS.csv (add 9.96x, sub 9.49x, mul 1.38x @ -O3).
- [x] Phase 4: multithreading (independent Jacobian walks) -> PHASE4_THREAD_SCALING.csv
      (1.97x / 2.98x / 3.58x at 2/3/4 threads; embarrassingly parallel, no sharing).
- [x] OPTIMIZATION_DECISIONS.md: keep/revert table from measured data; correctness gate
      green before/after every decision (correct.exe DONE re-verified after Phases 3-4).
- [x] Phase 5: memory/cache behavior -> PHASE5_CACHE_RESULTS.csv (runs R0-R8; 12KB..50MB
      working sets; dbl/add flat ~17-28ns = compute-bound; random gather shows the real
      hierarchy: 2.2ns@32KB -> 7.3ns@8MB -> 11.0ns@134MB; stride-67 gather prefetch-friendly
      ~2.4-5.1ns. CPUID leaf4/0x8000001D masked (VM) => hierarchy read behaviorally.)
- [x] Phase 6: toy-ECDLP algorithm landscape (brute/BSGS/rho/kangaroo/1T+4T) ->
      ALGORITHM_COMPARISON.csv. All runs verified by independent scalar-mul (verified=1).
      Fits: brute ~k (2.6k@2^12 -> 858k@2^20); BSGS ~2*sqrt(N) (81@2^12 -> 22149@2^28);
      rho ~1.2*sqrt(l) flat 55k-111k regardless of db (interval-blind, as expected);
      kanga ~3-6*sqrt(N) (266@2^12 -> 98482@2^28); kanga4 similar step ratios, ~3.6x wall
      speedup at large db vs kanga. MEMO: first rho/kangaroo drafts failed -> fixed
      (DBG rho: low-3-bits partition folds onto 2-cycle +/-P; now Teske 128-auX r-adding
      walk + Knuth-mix partition; kangaroo must run tame+wild simultaneously under the
      SAME deterministic jump rule so orbits coalesce, single table, both stored).
- [x] Phase 7: parallel collision engine (van Oorschot-Wiener distributed kangaroo) ->
      PHASE7_PARALLEL_CS.csv (T=1/2/4, W=8 walkers/thread, DP b=6, REP=5 min-wall).
      All rows verified=1. Walking leads: refuses BSGS's sqrt(N) table in favor of a
      distinguished-point output stream: at db=28 table = 486 entries vs BSGS 16384,
      wall 7.2ms(T=1) -> 2.6ms(T=2) -> 2.8ms(T=4) at fixed N; ns/step drops ~3.6x
      (const 292 -> 80.5). Aggregate steps grow with walker count (more concurrent
      walkers, same primitive), which is the expected VOW signature: wall time falls
      while total work rises. Note: min-wall runs are shown; tiny-db rows dominated by
      fixed setup, honest but noisy.)
- [x] Phase 8: GPU/OpenCL (AMD Vega 8 iGPU, gfx902, 8CU@1250MHz) — EC mixed-add kernel
      bit-for-bit vs src/ec.hpp add_affine; CPU 4-thread reference matches GPU checksum
      (matched=1 all runs) but GPU sustains ~600 Mops/s vs CPU ~40 Mops/s =>
      14.7-20.4x (PHASE8_GPU_RESULTS.csv). Transfer included (blocking read). Notes:
      local GPU slower than Vega12-critical iGPU: Verifies kernel portability but the
      CPU VOW engine (Phase 7) stays the reference alpha-scaling vehicle.
- [x] Phase 9: auto-tuner (src/tuner_main.cpp, tuner_O2.exe, PHASE9_TUNING_RESULTS.csv) --
      grid over {b,K,walkcap-mult} at db=24, T=4, W=8/T, REP=3. All 96 configs verified.
      Default b=ceil(log2(N)/2)=12 was badly suboptimal: b=4 (DP prob 1/16) solves in
      ~1.1-1.7 ms vs 50-80 ms for b=10-12 (~60x). Low b => frequent DP restarts ~ cheap
      fresh random starts; walk effectively samples more of the orbit space per wall tick.
      Small-K (8) matches big-K (64): jump-table size insensitive at this scale.
- [x] Phase 10+: research/ suite (spec.md, SAFETY.md, gen.py, solvers.py, bench.py,
      fit.py, kaggle_t4.py + kaggle_t4.ipynb, t4_parity.py, report.md)
      Synthetic puzzle-#71-structure benchmark, all verified rows:
      bsgs α=0.493 (A, exact √N); kanga α≈0.5 huge const - no exponent win (B*);
      rho/pir interval-blind (X flat); grover ≡ EMULATION NO CLAIM; PH on smooth-order
      control = the genuine sub-linear (C) shortcut (flat ~60 steps vs brute ~N).
      NO classical method beats √N on prime order in measured regime.
- [ ] Phase 10: optimized-engine profiling loop
- [ ] Phase 11: correctness (extended)
- [ ] Phase 12: scaling studies d=16..32 -> SCALING_RESULTS.csv
- [ ] Phase 13: alpha extraction
- [ ] Phase 14: final reports (PERFORMANCE/OPTIMIZATIONS/PROFILING/FAILED/FINAL) + answers to 8 questions

## Design notes / findings log
- [x] FIXED (2026-09-22): Montgomery + Affine::point(): `point()` calls from_raw (a Montgomery
      to_mont), double-converting internally-computed coords -> broke EC for mont only.
      Added Affine::rep() (assumes already-represented) used by add/dbl/to_affine; point() used
      only at raw boundary (from_affine for jacobian too). naive/barrett/pseudo unaffected
      (from_raw is identity) -> matched vectors though.
- [x] FIXED: Montgomery one() must be R (=2^32 mod P), not R2; from_mont = mul(x,1); reduce64 is
      division-free Barrett (true mod), not REDC; n0 via Newton-Hensel mod 2^32.
- [x] FIXED: Jacobian::mul used a stale affine recoding table while `b` doubles -> full Jacobian
      add() instead; add_affine kept for walks.
- [x] FIXED: ref layer: BSGS trace sign (B-(b*m+a)); point negation only y; Tonelli-Shanks
      requires QR check (pow(a,(p-1)//2,p)==1) else None.