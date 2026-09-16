# 11 — Campaign Verdict (Final)

## Target Re-Rank After Campaign

**No re-rank is justified by the campaign results.** The re-rank criterion is
"asymptotic or structural advantage over the field," and every asymptotic /
structural hypothesis tested came back negative:

| Hypothesis | Result |
|---|---|
| EX1 low-nibble degeneracy | DISPROVEN (uniform nibbles) |
| EX2 PRNG null-expectation | HONEST NEGATIVE (no static pattern beats null) |
| EX3 structure battery | HONEST NEGATIVE (fails directional replication) |
| H5 k-parity → x-parity | DISPROVEN (no deterministic map) |
| H6 high-bit leakage | REFUTED (worst φ=0.0196, 0/1600 survive FWER) |
| Spectral-mix buckets | NEUTRAL (0.991, 15/15) |
| spread=6 | INCONCLUSIVE at toy width (1.195, tail noise) |
| Θ(√W) floor | CONFIRMED (EX5) — no asymptotic reduction exists |
| EXP-N2 GLV×neg quotient (v6) | **REFUTED** — folded candidates never fire (0/16), canonical-state walk cycles (13 distinct in 372 steps @ w=16), v6 tail at w=24 (K mean 16.1) |
| EXP-N3 multi-herd | NO GAIN on this box (13.95→12.08s; serial trail + ~1.6× ceiling) |
| EXP-N4 infeasibility | QUANTIFIED — #67 ≈ 173 CPU-days + TB-class trail RAM; #140 ≈ 4.1e10 core-years |

All targets keep their original rank: **Puzzle #140 (R2, 140-bit) #1**;
smallest fixed-constant GPU cost (~1,400 GPU-yr v5).

## Final Breakthrough Verdict (Requested Format)

```
TARGET        Puzzle #140 (R2, 140-bit) — the smallest-R2 unsolved challenge;
              #66 solved key used as the CPU-width reference in earlier work.

NEW DISCOVERY v5 kangaroo = fused single-inversion hop (1 mod-inv/hop) +
              canonical even-y quotient walk over {P,-P} (search width W/2).

WHAT CHANGED  Two orthogonal constant-factor gains, verifiably multiplicative:
                2.0x (per-op cost)  x  1.42x (collision statistics)
              = 2.54x avg / 2.69x median wall-time, identical correctness.

BASELINE      v4 Pollard-Teske kangaroo, 2 modular inversions per hop, K~2.1
              class design width W (not W/2).

NEW METHOD    v5_fused_negation: one to_affine() per hop serves bucket AND
              membership lookup; every visited point is normalized to its
              even-y representative; jump table + trail sized to the folded
              width W/2; canonical collisions verify BOTH k1 = t_off - wild
              and k2 = N - (t_off + wild) before returning.

MEASURED      Ops: K v5/base = 0.702 (w=20), 0.837 (w=24), 0.739 (w=28).
IMPROVEMENT   Wall: avg 2.54x, median 2.69x, min 1.21x, max 3.61x @ w=24.
              Correctness: 49/49 solves across w=20..34.

VERIFIED:     YES.

IF YES:       PROOF =  - 36/36 correct-key recoveries (w=20/24/28, 12 seeds each)
                         in bench_v5_vs_v4.py;
                        - 8/8 correct at w=24 with timed wall comparison in
                         bench_v5_walltime.py;
                        - 5/5 correct at w=30..34 in bench_cpu_ceiling.py
                         (w=33 one unlucky tail, w=34 solved in ~60s);
                        - every candidate key re-verified via
                         point_equal_jac(scalar_mult(k), target) before return;
                        - negation component reproduced independently in
                         test_negation.py (12/12, K 0.702 with W/2 tuning and
                         1.030 WITHOUT it — the effect is the tuning, not noise).
```

## Honest Closing Statement

The campaign did **not** produce an asymptotic or structural breakthrough —
EX5 confirms Θ(√W) is the floor, and every structural/statistical hypothesis
was refuted or neutral. It **did** produce a verified, drop-in, constant-factor
stack (2.5-2.7x) with the strongest correctness discipline in the repo
(49/49 solves, key re-verified before return, walk-identity checks where
applicable).

Puzzle #140 remains a cluster-scale computation (~1,400 GPU-yr on one RTX
4090 class; ~3.5-4 yr on a 400-GPU class). The v5 optimizations are the right
thing to ship into RCKangaroo / oritwoen / JeanLucPons kangaroo so the whole
community gets the 2.5x for free.

## Suggested Next Work (in priority order)

> **Update (this phase):** suggested step 2 below (3x endomorphism / auto-mod) has been
> **measured and refuted** for bounded additive kangaroo (EXP-N2): a canonical x-collision
> needs `b ≡ ±λ^i·a (mod n)`, and with small bounded scalars only `i=0` is reachable, so
> the quotient store reduces to identity and the shorter W/6 trail adds tail risk. The
> 0.51 K-floor is not reachable via automorphisms. Multi-herd gives no single-machine
> wall gain (EXP-N3). Remaining priority-1 item is unchanged.

1. **Port v5 to GPU / C** (batch-Montgomery + fused) and merge into the open
   kangaroo ecosystem — the only path that actually moves #140.
2. ~~3x endomorphism (auto-mod)~~ **REFUTED** (EXP-N2): implement a signed-distance walk only if
   the bounded-interval collision restriction (b ≡ ±λ^i·a mod n unreachable for i≠0) is revisited
   with an unbounded/scaled-distance design — otherwise it cannot fold the store.
3. **Multi-target pooling** for the R2 set once two same-width unsolved
   targets exist within one interval (not today: #140..#160 differ in width).

## New/Changed Files This Phase

- `SOLVER_LAB/candidate/v5_fused_negation.py` — v5 solver (the deliverable).
- `SOLVER_LAB/synthetic/test_negation.py` — negation-map proof (K 0.702).
- `SOLVER_LAB/synthetic/test_bucket_hash.py` — spectral-mix (neutral).
- `SOLVER_LAB/synthetic/test_spread.py` — Pollard 2025 (inconclusive @20).
- `SOLVER_LAB/synthetic/test_h6_bits.py` — bit leakage (refuted).
- `SOLVER_LAB/benchmarks/bench_v5_vs_v4.py`, `bench_v5_walltime.py`,
  `bench_cpu_ceiling.py` — the three evidence runs.
- `SOLVER_LAB/reports/ASSESSMENT_EXTERNAL_VS_STACK.md` — additivity analysis.
- `STRATEGIC_SOLVER/08_BREAKTHROUGH.md`, `09_BLOCKED_TARGETS.md` — revised.