# ECDLP Scaling Study — Findings (synthetic toy + benchmark suite)

Scope: toy/benchmark only. All instances synthetic; nothing here is usable on crypto-scale
(curves, secp256k1, real puzzles). See SAFETY.md. This report summarizes Phases 1-9
(CPU microarch/parallel engine) and the research/ suite (empirical scaling exponents).

## 1. Primitive cost center (Phases 2-5): the modmul chain
EC mixed-add (Jacobian + affine, a=3): the 8M+3S mod-mul pipeline dominates; this is the
same profile on CPU (Phase 2-5), GPU (Phase 8), and the Python suite. SIMD/4-thread and
cache micro-optimizations give constant factors only (2-6x), never exponent change.

## 2. Empirical α (research/ results/bench_prime.csv, 63 verified rows)
N = interval size (uniform k in [1,N)), steps = group ops until solution, 3 reps, gm.

| method          | α (vs log N) | R²  | const (steps at db12) | class |
|-----------------|-------------:|----:|----------------------:|------:|
| bsgs            | 0.493        | .997| ~1.5 √N               | A     |
| kanga (VOW, 32) | 0.463        | .943| ~220 √N, drops to ~120 | B* (huge const, slope≈½) |
| rho (full group)| 0.019        | .227| ~370k (≈√l, l=2³²)    | X(flat) interval-blind |
| pir (4 restarts)| -0.022       | .266| ~330k (same trap)      | X(flat) interval-blind |
| grover_emu (db≤12) | —         | —   | (π/4)√N oracle queries=50 | EMULATION, NO CLAIM |

Interpretation:
1. BSGS hits the √N generic bound exactly (A). This validates the fit methodology.
2. The parallel kangaroo (the Phase 7/9 engine) has slope ≈0.5 vs √N, *not* better — its win
   is memory (DP table ~√N/2ᵇ instead of √N) and parallelism (critical-path wall time), the
   textbook (B) payload. Its constant is huge here (small-N granularity, 32 walkers) and
   decays toward √N as N grows (db24-28: 69-120 √N) — no exponent advantage.
3. rho / pir do not scale with N because they are not interval-aware; they ride the
   full-group √l floor (l=2³² here). They are flat in N only as an artifact of the metric,
   flagged X(flat) in fit.py, NOT a speedup.
4. Grover stage reproduced in classical amplitude emulation costs (π/4)√N oracle queries
   per iteration family — i.e., a *quadratic* query reduction exists for an oracle that
   detects the solution, but no such oracle is constructible here without quantum
   hardware; labeled EMULATION, NO CLAIM. No α<0.5 is claimed for any classical solver.

Bottom line: NO classical method beat the √N barrier in the measured regime. That is the
expected and reproducible outcome (generic-group lower bound). Claims of the form
"α<0.5 observed" would be rejected by this methodology (flagged X/B*, needs replication).

## 3. Pohlig-Hellman exhibit = the real (C) shortcut (control only)
Smooth-order control group (results/bench_smooth.csv, 12 verified rows): PH solves any
db in ~60 steps flat, while brute force scales ~N (15.6M steps at db=24). This is an
*algorithmic* α≈0 shortness that exists ONLY because the control group has smooth
composite order. Prime-order group: PH does not apply. This is the falsification target:
claims of such shortcuts on the *prime-order* toy are structurally impossible.

## 4. Auto-tuning (Phase 9)
Grid over {DP bits b, jump-table K, walkcap} at db=24: b=4 (DP prob 1/16, frequent fresh
restarts re-seed the walk) is ~60x faster in wall than the naive b=ceil(log₂N/2)=12
(1.1-1.7 ms vs 50-80 ms). All 96 configs verified. K and walkcap within 2x sensitivity.
⇒ the research suite tunes b per db before reporting α (see bench.py --kanga-b).

## 5. GPU (Phase 8, Vega 8) and Kaggle T4 path
OpenCL kernel bit-for-bit identical to CPU add_affine; CPU/GPU checksums matched on all
sizes (matched=1); sustained ~600 Mops/s vs ~40 Mops/s 4-thread → 14.7-20.4x. This is a
hardware constant, again no exponent change. kaggle_t4.ipynb ports the kangaroo to cupy
for the allowed GPU tier; t4_parity.py validates the walk semantics on CPU before GPU use.

## 6. Classification summary (report classification per spec)
A: bsgs only.
B: kanga/VOW parallels + GPU + tuning (parallel/hardware constant gains, α≈0.5).
C: none on prime-order (the ONLY sub-generic method found, PH, requires smooth order).
D: none (no method showed α≥0.95 vs N; rho/pir were flat-by-artifact not D).

Methodology notes: verified=1 on every row before fitting; gmean of reps; R² reported;
α reported with 90% CI in fit.py output; X(flat)/B* flags force scrutiny of pseudo-gains.

## 7. Reproducibility
- C++ toy (Phases 1-9): all CSVs in repo root; run engine_O2.exe / tuner_O2.exe /
  gpu_O2.exe (see PROGRESS.md for exact args).
- research/: python bench.py --db 12,16,20,24,28 --reps 3 ... ; python fit.py <csv>;
  python bench.py --smooth ... ; validate with t4_parity.py; T4 via kaggle_t4.ipynb.
- Seeds pinned (20260922); generators deterministic; instance JSONLs include verified=1.