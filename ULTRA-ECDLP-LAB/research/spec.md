# Toy-ECDLP Synthetic Benchmark — Spec

Status: research scaffold. All instances SYNTHETIC. This suite measures the empirical
scaling exponent α of candidate ECDLP-solver designs on synthetic instances that share
the *structure* of the famous "Bitcoin Puzzle" challenges. It never targets a real
puzzle / real keys. See SAFETY.md.

## 1. Research question
Can any candidate approach to generic-group ECDLP scale **empirically better** than the
generic lower bound Θ(√N) (same group, same interval width N)?

Generic-group theorem (Nechaev/Shoup) says no single algorithm can do better than Ω(√N)
group operations *for an arbitrary input in the random-oracle model*. That is an *
algorithmic* constraint on a specific solver operating on a specific input, NOT a claim
that the *whole family* of solvers observed on many instances can't beat √N per instance
(a randomized restart that lands in a lucky orbit cuts steps; a quantum subroutines is a
different machine). We measure what actually happens.

Methodology:
- instances: prime-order group (order l), interval width N=2^db with 2^db << l.
- k (the secret) uniform in [1, N); target Q = k·G.
- measure wall-clock steps(ops) of each solver on the same k for each db.
- repeat R times with different k → geometric mean steps at fixed db (variance is huge in rho/kanga, so gmean, and report spread).
- fit log2(steps) vs log2(N) → empirical α = slope.
- classify: A α≈0.50, B 0.50<α<0.67, C 0.67≤α<0.95, D α≥0.95.

Predictions to falsify:
1. α_BSGS ≈ 0.50 (theorem-tight, memory √N).
2. α_rho ≈ 0.50 with huge constant.
3. Parallel VOW kangaroo with Σ walkers: steps ≈ 2√(N·Σ)/θ? Actually the *step count*
   consumed across all walkers obeys ~√(N·Σ), so total-ops α = 0.50 again, but the 
   *critical-path* wall α depends on Σ (that's the parallel (B)-class gain, not an A-class claim).
4. A "quantum-like" amplitude amplifier (Grover oracle staged on a function that detects
   a distinguished collision) would show α≈0.25 at small N *if* the oracle Q and its
   amplification were realizable; with the toy, we can build an amplitude-amplified
   collision DESK with exact scalar muls only — it still needs quantum hardware. So we
   implement a *classical emulation* of the Grover-amplified oracle only up to tiny db and
   clearly LABEL it emulation (no claim). We do NOT claim an A-class result from it.
5. Pohlig–Hellman on a NON-prime-order (smooth) group: α≈0 against √l (this is the
   canonical (C)-class "algorithmic shortcut" — it exists only for composite order, which
   the generator also emits as a control set).

Security-feature guarantee:
- Everything here runs on synthetic coordinates; N ≤ 2^71 but l is only ~2^32 in the
  C++ toy (Phase 1-9) or a PRIME-order field group sized for Python feasibility in
  research/. Nothing here is usable on secp256k1 (2^256). The generator is separate from
  solvers so that control instances are never real keys.

## 2. Instance format
JSON lines: {"db":24,"l":<order>,"Gx":...,"Gy":...,"Qx":...,"Qy":...,"k":<int>, "typ": "prime"}.
k is included ONLY for verification in local runs; benchmark runs that go toward a
public claim may strip k (the solver must verify by scalar-mult); SAFETY.md says when.

Curve: short Weierstrass y²=x³+b over field p. For the Python suite, l and p are sized
so that √(2^71) scalar ops are NOT feasible purely in Python; we only actually run db up
to ~40 locally (minutes-to-hours) and the Kaggle T4 runs 2^44-2^58.

## 3. Solvers (the oracle set)
- S1 BSGS  : baby/giant, memory √N; steps exactly 2√N.
- S2 rho   : Pollard rho w/ distinguished points, single walker stream (or walkers).
- S3 kanga : VOW parallel kangaroo, W walkers, DP pruning. This is the engine from
  Phase 7/9, ported and parameterized (b tuned per db by tuner_O2.exe rule).
- S4 pir   : "parallel independent restarts" — R random restarts of a small rho, keep
  min. Contrast to S3: shows restarts do NOT change the exponent.
- S5 ph    : Pohlig–Hellman on smooth-order control instances (typ="smooth").
- S6 gro   : Grover-style emulation ONLY up to db ≤ 12, no indexing for larger. Explicit
  "EMULATION, NO CLAIM".

Each solver returns: steps, wall_ms, ok, verified (independently scalar-multiplied).

## 4. Deliverables
research/
  spec.md            (this file)
  SAFETY.md
  gen.py             instance generator (deterministic seeds, hash-derived points)
  instances/           generated instances JSONL
  solvers.py         S1..S6
  bench.py           orchestration + csv + gmean + fit + classify
  fit.py             log-log regression
  kaggle_t4.ipynb    cupy port for the T4 (large db)
  results/            CSV + plots
  report.md          final A/B/C/D writeup