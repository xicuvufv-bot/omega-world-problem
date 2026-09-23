# RESEARCH_AUDIT — ground-truth audit of ULTRA-ECDLP-LAB
# Generated 2026-09-22 by the autonomous research controller (README: all synthetic, toy-only).

## 0. Purpose
This audit classifies what the existing lab PROVES, what is portable to new experiments,
and what must be re-derived before any "breakthrough" claim. It is the correctness +
reproducibility backbone that new hypotheses must be measured against.

## 1. Verified baseline inventory

| Asset | Role | Verified? | Portability |
|-------|------|-----------|-------------|
| instance.hpp (toy p=4294966177=2^32-1119, p≡1 mod 3, l=4294835173 prime, G=(x,y)) | canonical toy group | correct.cpp independent vectors, Phase 4-9 reruns | Primary synthetic group |
| src/fp.hpp (naive/barrett/montgomery/pseudo Fp) | field arithmetic | green correctness suite | mount point for representation experiments |
| src/ec.hpp add_affine/dbl/mul | EC ops | matched Python gen equivalent | must mirror exactly in any new walk |
| src/vow_engine.hpp + engine_O2.exe | VOW kangaroo engine (T threads, DP b, K jumps) | all rows verified=1 | refactored into header (tunable) |
| src/tuner_main.cpp | auto-tuner grid | PHASE9 all verified | b sensitivity proven (b=4 best at db=24, 60x wall) |
| src/gpu_main.cpp + ocl_min.h + libOpenCL.a | OpenCL kernel parity vs CPU | matched=1 all sizes | PRIVATE to Vega8; do NOT port to T4 (no OpenCL); T4 route = cupy |
| research/gen.py | synthetic instance generator (prime + smooth control) | verified field | keep; extend for anomalous/supersingular controls |
| research/solvers.py | S1 bsgs S2 rho S3 kanga S4 pir S5 ph S6 grover_emu | all ok=1 self-checked | baseline oracle set |
| research/bench.py / fit.py | orchestration + log-log α fit + A/B/C/D | reproducible | reuse for CLASS detection |
| research/kaggle_t4.py | cupy VOW port (payload + notebook) | CPU-parity checked locally (t4_parity.py) | T4 route; EXTEND to 2-GPU |

## 2. Measured laws (do not rediscover)
- BSGS: steps ≈ 2√N, α=0.493 R²=0.997 (A). This is the √N reference line.
- rho: interval-blind, steps ≈ 1.2√l (l=2^32) flat across db (α≈0 vs N by artifact).
- kanga/VOW: α≈0.46-0.5 vs N, constant huge at small N (~220√N@2^12) decaying (~120√N@2^28).
  No exponent win; wins are memory (DP table) + parallelism + tuning.
- PH on smooth-order control: ~60 steps flat across db — the ONE true sub-linear class,
  structural (composite order), impossible on prime order.
- Grover emulation: (π/4)√N oracle queries; EMULATION ONLY.
- T groups: EVEN advance noisy at tiny db; REP=min-wall; geometric-mean fits.
- Const rates: ~600 Mops/s Vega8 GPU vs ~40 Mops/s (4T CPU) = 15-20x hardware only.

## 3. Correctness gates that MUST be preserved for every new claim
1. Every returned k re-verified by independent scalar-mul (verified=1) before being scored.
2. Generator verifies all rows at generation time (`verified` field == 1).
3. CPU/GPU parity via checksum gate (Phase 8 matched=1). Any new GPU kernel:
   run identical CPU reference + checksum compare.
4. t4_parity.py gate: cupy port must solve same instances as solvers.kanga before GPU runs.
5. Fit on geometric mean over ≥3 seeds; report R²; per-db spread min/max.
6. Never impute a failed row; never drop failing seeds unless logged.

## 4. What this new phase must NOT assume
- The prior "NO classical method beats √N" conclusion is ENGINEERING-true for the tested
  oracle set, not a theorem about our group. It is the null hypothesis to FALSIFY, not a ceiling.
- Phase 9 tuning found b-sensitivity on one db (24). It does NOT generalize across all db/curves.
- The toy curve is ordinary y²=x³+7 prime-order — rich in structure candidates:
  p≡1 mod 3 => 3-isogeny / endomorphism λ (GLV) available — UNTESTED so far.
  This is the highest-value untested surface (endomorphism/automorphism family E/D).

## 5. Method priority for new work (cost/benefit)
1. p≡1 mod 3 endomorphism (GLV) decomposition experiments — cheap to build on toy, may
   change the walk geometry; must show α change, not constant, to matter.
2. Anomalous-trace curve control (#E=p) — Smart attack gives α≈0 class on a DIFFERENT
   curve family (like PH controls). Build the control, confirm sub-linear, then falsify
   "does it apply to ordinary toy?" (answer no ⇒ supports generic √N binding).
3. Batch/multi-target amortization — real effect (W) but constant over M, not α.
4. Walk mixing audit — rare but cheap; guards against accidental bias in any new walk
   (detects the *negative* failures of earlier drafts: 2-cycle fold, low-b partition).
5. Information-theoretic/density candidates are NOT implementable on prime order at toy
   sizes with the current oracle set; keep as HYPOTHESIS-only (no resources).

## 6. Portability decisions (final)
- Alpha-scaling vehicle stays: research/solvers.py + Python bench (reproducible, seedable,
  portable to T4). C++ engine only for large-db constant tuning.
- T4×2 route: cupy; never OpenCL. GPU0/GPU1 = independent seed/hypothesis split, not
  shared-memory; each job writes CSV+JSON+checkpoint.
- All new experimental code goes under research/lab/<experiment>/ with its own test.py
  entry (self-checking) + a results/ CSV. No experiment code in the verified core.

## 7. Threats to each conclusion
- finite-size/cache artifacts: guard by multiple db + REP and min/geomean reporting
- generator bias: verify distribution of k (uniform) periodically
- cherry-picking: detector uses ALL rows, statuses written by pipeline, never hand-picked
- hidden preprocessing advantage: any precomputed value saved across runs logged as cost
- overfitting: any hypothesis whose "reason to win" is a single db or single seed is CUT.