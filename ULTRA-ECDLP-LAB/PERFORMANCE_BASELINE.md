# PERFORMANCE_BASELINE.md — Phase 1 microbenchmarks

Date: 2026-09-22. Machine: Ryzen 3 3200G 4C/4T @ 3.6 GHz (VM, hypervisor present), g++ 16.1.0 MinGW.
Curve: y^2 = x^3 + 7, p = 4294966177 (2^32 - 1119, p ≡ 1 mod 3), group order l = 4294835173 (prime),
G = (1960037684, 560815139). All timings are best-of-multiple calibrated runs of in-process steady_clock.

## Method (honesty rules)
- Field ops: 10M iterations over 256-entry operand buffers (L1-resident), xor-sinked so nothing folds out.
- EC ops: 3M-iteration dependent walks (true latency chain, no ILP across ops).
- Flag sets compared: -O2, -O3, -Ofast, -O3 -march=native. Best-of measured, not theoretical.
- Full data: MICROBENCHMARKS.csv (kind,strategy,op,O2,O3,Ofast,native,best,best_flag).

## Field arithmetic — ns/op (best across all flag sets)
| op    | naive | barrett | mont | pseudo |
|-------|-------|---------|------|--------|
| add   | 1.913 | 1.921   | 1.912| 1.897  |
| sub   | 1.905 | 1.917   | 1.905| 1.902  |
| mul   | 1.905 | 2.103   | 2.624| 1.915  |
| sqr   | 1.900 | 2.043   | 2.430| 1.936  |
| inv   | 83.4  | 88.2    | 87.8 | 82.4   |

Key baseline facts (surprises worth noting):
1. **naive `% P` is essentially free**: with P a compile-time constant GCC emits multiply-by-magic
   reciprocal division (~2 mul+shift+sub), so no division instruction runs. naive mul == pseudo mul.
2. **Montgomery is SLOWER here**, not faster (mul 2.62 vs 1.91 ns). The 128-bit REDC dependency chain
   (mulq + imul + add + shr64) costs more than the magic-multiply trick, and mont's `-Ofast` mul
   regressed to 5.08ns (unsafe FP contraction feeding the 128-bit path). Lesson for later phases:
   an optimization "known to be right" in general is not automatically right on this ISA/compiler.
3. Field inv (~82-96 ns, ~30-55x a mul) dominates affine arithmetic — this is why Jacobian/mixed
   coords rout affine on latency-bound walks.

## EC formulas — ns/op (best across all flag sets), dependent latency chain
| formula          | naive | barrett | mont | pseudo |
|------------------|-------|---------|------|--------|
| affine_add       | 102.9 | 101.4   |119.8 | 102.2  |
| affine_dbl       | 108.1 | 107.7   |129.3 | 112.1  |
| jacobian_dbl     | 17.1  | 16.0    | 34.6 | 30.3   |
| jacobian_mixed++ | 19.3  | 18.4    | 51.1 | 30.5   |
| jacobian_add     | 22.9  | 33.2    | 61.4 | 41.2   |

Key baseline facts:
1. Jacobian coords are ~5-7x faster than affine on latency chains (no inv in the loop).
2. **naive/barrett Jacobian dbl is ~17ns** — the fastest field*formula combination on this host.
3. mont jacobian_dbl (34.6ns) is 2x slower than naive (17.1ns): the mont mul penalty compounds
   across the 4-8 mul chain inside a dbl.
4. pseudo jacobian_dbl (30.3) loses to naive despite equal-field mul — because naive's magic-div
   has more ILP under `-march=native` scheduling inside the dependent dbl chain.

## Implication for algorithm phases
- Point multiplication target engine: naive or barrett field (not mont, not pseudo) on provably
  equal terms; jacobian + mixed coordinates; `-O3 -march=native` (or -Ofast for non-mont paths).
- One jacobian_dbl ≈ 17ns. A full 32-bit point mult (k has 32 bits, ~32 dbl + ~16 add) ≈
  32*17 + 16*20 ≈ 860ns single-threaded → ~1.16M point-mults/s/thread as the Phase-1 baseline.

## Caveats
- Cycle values are estimates; hypervisor present so rdtsc precision is reduced. We use monotonic
  wall time, best-of-N reps, which is unaffected by rdtsc.
- EC walk timings measure latency CHAINS (worst case for scheduling); pipelined scalar-mult
  variants (Phase 3/4) will measure throughput differently.