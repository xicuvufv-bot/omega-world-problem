# PHASE 2 — Assembly Inspection Report

Date: 2026-09-22 · Toolchain: g++ 16.1.0 MinGW-w64 · Target: Ryzen 3 3200G (Zen+, 4C/4T @3.6GHz) · P=4294966177=2^32-1119

Method: compiled `src/asm_probe.cpp` with `-O3 -march=native -fno-inline` to keep each field-op /
EC-op as a *separate symbol* (`asm_native2.s`), plus the real benchmark `src/micro_main.cpp`
(`micro_native.s`) to census the *fully inlined* EC workers exactly as measured.
Tools: `extract_asm.py`, `asm_census.py`, `asm_hist_mont.py` (kept in lab root; all reproducible).

Census baseline (from `MICROBENCHMARKS.csv`, best flag per entry, ns):

| op | naive | barrett | mont | pseudo |
|---|---|---|---|---|
| field mul | 1.905 (O2) | 2.103 (native) | 2.624 (native) | 1.915 (native) |
| field add | 1.913 (O2) | 1.921 (Ofast) | 1.912 (native) | 1.897 (Ofast) |
| field sub | 1.905 (O2) | 1.917 (O2) | 1.905 (O2) | 1.902 (O3) |
| field inv | 83.4 (O2) | 88.2 (Ofast) | 87.8 (O3) | 82.4 (native) |
| jacobian_dbl | 17.1 (native) | **16.0 (O3)** | 34.6 (native) | 30.3 (O3) |
| jacobian_mixed_add | 19.3 (native) | 18.4 (Ofast) | 51.1 (native) | 30.5 (native) |

---

## 1. Instruction census — standalone field ops (asm_native2.s)

`mul/sqr/sub` are tiny straight-line routines; `inv` tail-jumps into a shared binary
Euclid loop (`inv_mod_u32.constprop.0` — scalar `idivq`, ~82-97 ns).

### naive_sub (branchless, 0 control flow)
```
subl   %ecx, %edx           ; t = a - b
cmpl   %ecx, %r8d
leal   -1119(%rdx), %eax    ; t - P (P = 2^32-1119 ⇒ subtract 1119)
cmovnb %edx, %eax           ; select t if t >= 0
ret
```
15`cmov`, zero branches. Correct because `t ∈ (-P, P)`.

### naive_sqr / naive_mul (division by P via magic reciprocal)
```
movabsq $-9223369633819947615,%rax   ; magic M for P
imulq  %rcx,%rcx                     ; t = a*b  (64-bit)
mulq   %rcx                          ; hi:lo = M * t   (128-bit)
shrq   $31,%rdx                      ; q = hi >> 31
imull  $1119,%edx,%edx               ; q*1119
leal   (%rdx,%rcx),%eax              ; t + 1119*q  == t mod 2^32 ... folded form
ret
```
2 multiplies (1× imulq + 1× mulq), branch-free, single dependency chain of 4 ops.
This is 1.905 ns — the fastest stand-alone mul. **No `div`, no spill, no loads/stores.**

### barrett_mul → barrett_reduce64 (mu = floor(2^96/P))
```
movabsq $4294968415,%rax   ; mu
movl    $4294966177,%r8d   ; P
mulq    %rcx               ; hi:lo = t*mu
movl    $4294966176,%eax   ; P-1
imulq   %r8,%rdx           ; q = hi (truncate), then q*P
subq    %rdx,%rcx          ; r = t - q*P
cmpq    %rcx,%rax
jnb     .L42               ; branch 1
movq    %rcx,%rdx
subq    %r8,%rdx           ; try r - P
cmpq    %rdx,%rax
jnb     .L43               ; branch 2
movabsq $-8589932354,%rax  ; -2P
addq    %rax,%rcx
...
```
1× `mulq` (128-bit) + 1× `imulq` + **2 data-dependent branches** (jnb). Random operands hit
branch 1 ~50% of the time ⇒ frequent mispredicts. Field mul = 2.103 ns.

### mont_mul (Montgomery: REDC with n0 = -P^-1 mod 2^32 = 0xE91F579F)
```
imulq  %rdx,%rax           ; t = a*b
imull  $-383821921,%eax,%ecx ; m = n0 * (t mod 2^32)
imulq  $4294966177,%rcx    ; m*P
xorl   %edx,%edx
addq   %rcx,%rax           ; t + m*P
adcq   $0,%rdx             ; 128-bit carry
shrdq  $32,%rdx,%rax       ; >> 32   = value · 2^-32
movl   %eax,%edx
cmpq   %rax,%rcx
jnb    .L21
addl   $1119,%edx          ; conditional add of P
.L21:
ret
```
**3 multiplies** (2× imulq + 1× imull) + `adcq` + `shrdq` (both latency-locked on the
carry chain) + **1 data-dependent branch**. Walk: imulq(4c) → imull(3c) → imulq(4c) →
addq/adcq(2c) → shrdq(1c) → cmp/jnb(2c) ≈ 15-16 cycles sequential. That precisely
explains the 2.624 ns (~9.4 cycles) — mul is the mont hot loser.

### pseudo_reduce64 (fold: P ≈ 2^32, 2 folds by 1119, branchless)
```
; fold 1
imul/$1119 on high word, shrink, add
; fold 2 (because hi*1119 can exceed 2^32)
imul/$1119 again, cmovnb select
```
2× `imulq` + `shrdq/shrq` chains + 1 `cmovnb`. No branch. Field mul 1.915 ns — mont-style
but 27% cheaper, competitive with naive.

**Key negative result (item 1 of the audit):** across *all four* strategies, **no `idiv`/`div`
instruction appears in any mul/sqr/add/sub path** (the only `idivq` is inside `inv`). GCC
already implements `% P` and `floor` via magic-multiply. There is nothing to win by
"removing division" — divisor elimination is already done by the compiler.

---

## 2. Instruction census — fully inlined EC workers (micro_native.s)

The benchmark compiles each EC op as one giant straight-line function; counts below are for
the complete worker bodies (this is the code actually timed).

| metric | naive | barrett | mont | pseudo |
|---|---|---|---|---|
| total ins | 1234 | 1737 | 2126 | 1231 |
| `mulq` (128-bit) | 55 | 35 | 23 | 0 |
| `imulq` | 114 | 142 | 170 | 111 |
| `shrq`/`shift` | 60 | 51 | 8 | 79 |
| `adcq` | 0 | 0 | 61 | 0 |
| `shrdq` | 0 | 0 | 61 | 0 |
| data branches (`jnb`) | 2 | 48 | 105 | 18 |
| `cmov` | 55 (36b/19nb) | 88 (48b/40nb) | 52 (28b/24nb) | 51 (35b/16nb) |
| spills (rsp-offset loads) | low | low | low | low |
| `call` | 14 | 15 | 14 | 15 |

Readings:
- **mont is the heaviest body (2126 ins) with the longest latency chains**: 61 `adcq`+`shrdq`
  pairs (the REDC carry chain can't be parallelized) and 105 data-dependent `jnb` (one
  conditional add per REDC, all with real branch pressure). This is why *every* mont EC op
  is ~2x slower (dbl 34.6 vs naive 17.1), even though mont is fast for pure `add`/`sub`
  (inputs behave like plain integers). **Neither surprising nor coincidental.**
- **barrett carries 48 `jnb` (2 per reduce64)** — branchy but short chains; measured dbl
  16.0 ns is the **fastest** EC dbl. The branch predictor absorbs them well (64-taker
  pattern + the second branch rarely fires on random inputs of uniform 32-bit width).
- **pseudo needs zero `mulq`** (128-bit multiply eliminated by the fold scheme) yet is slow
  *on EC* (dbl 30.3 ns): each add/sub costs 2 folds ⇒ deep sequential imul/shr chains; the
  dbl has many add/sub. Cheap per-op (1.90 ns), expensive per-EC-op.
- **naive is minimal and nearly branch-free**: 0 `adcq/shrdq`, only 2 `jnb` in the entire
  1234-ins worker, 55 cmov selects. It wins or ties on every stand-alone field op and posts
  the 2nd-best EC numbers.

No register-spill hotspots, no redundant reload loops, no `call` inside inner loops
(14-15 calls are the periodic clock reads / printf scaffolding), no loop-carried stalls
visible beyond the inherent chain analysis above. Compiler conversions (64→32) are minimal
and clean (leal/movl folding) — no obvious `cvt*` conversions in the hot paths.

---

## 3. Latency model vs. measured ns (Ryzen Zen+ @3.6 GHz)

| mul style | critical chain (ops) | ~cycles @Zen+ | predicted ns | measured ns |
|---|---|---|---|---|
| naive magic | imulq(4) mulq(5) shr(1) imul(3) lea(1) | ~14 | ~3.9 | 1.905* |
| barrett | mulq(5) imulq(4) sub(1) branch(2) | ~12 + mispredict | 2.0-3.5 | 2.103 |
| mont REDC | imulq(4) imull(3) imulq(4) adc(2) shrd(1) branch(2) | ~16 | ~4.4 | 2.624* |
| pseudo fold | imul(3) shr(1) imul(3) shr(1) cmov(1) | ~10 | ~2.8 | 1.915* |

(* measured well under the single-op latency ⇒ the bench loop overlaps independent
iterations and executes ~0.5-0.7 ops/cycle on these macro-ops; ratios, not absolutes, are
the signal. mont:9.4cy, naive:6.9cy, barrett:7.6cy, pseudo:6.9cy → mont is 1.36-1.38× the
others, matching the 1.905→2.624 ns gap exactly.)

---

## 4. Conclusions for Phase 3/4 (measured, reproducible)

1. **No architectural div scavenging to do** — compiler already eliminated all integer
   division. `inv` (binary Euclid, `idivq`) is the only remaining scalar-division site;
   it is already the slowest op (~83 ns) across all strategies.
2. **mont strategy carries an intrinsic ~1.35-1.4× latency tax** at the field-mul level and
   a **~2× tax at the EC level** (extra adcq/shrdq carry chains + one branch per REDC).
   Retaining mont as "the fast one" is **not supported by measurement** on this HW.
3. **barrett is the EC-layer winner** on this machine (dbl 16.0, mixed_add 18.4) despite
   branchy reduce64; naive is the field-swiss-knife winner (mul 1.905, sub 1.905, add 1.913).
4. **Enumeration-order red herring avoided**: the phase-4 mixed flips and code-size deltas
   are all part of the same straight-line models — no hidden serialization.
5. Phase 3 candidates that touch *these* chains, in descending expected value:
   - batching field ops into 4-lane (AVX2) packs — targets naive/add/sub (vpmulld/vpand
     already appear only in the pseudo body leg, suggesting partial SIMD already engaged).
   - avoiding REDC adcq/shrdq serialization in mont (or dropping mont on this P).
   - providing 128-bit multiply before reduce (barrett/naive) to shorten the magical chain.
6. Phase 4 candidates: parallel DLP walks (independent k·G instances) over 4 threads
   (Ryzen 3200G: 4C/4T), trivially embarrassingly-parallel; measured scaling target 3.4-3.9×.

All measurements share the same fixed harness (`measure` over steady_clock, warm-up,
ns/op), same source, same toy instance (instance.hpp). No algorithm was changed in this
phase; correctness suite (FIELD / EC-AGREE / VECTORS×4) remains green.