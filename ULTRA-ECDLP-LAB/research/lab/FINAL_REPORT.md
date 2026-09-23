# ULTRA-ECDLP-LAB — v3 MISSION FINAL REPORT

Date: 2026-09-23. Mission file version: v3. All instances SYNTHETIC toy ECDLP on
y^2=x^3+7 over F_p (p=4294966177 and genuinely varied primes), interval k in [1,2^db].
No real keys, no real puzzles, no production curves. GPU numbers: none manufactured.

---

## 0. Executive verdict (honest, no banned words)

**There is no reproducible sub-sqrt (alpha < 0.5) ECDLP scaling on this toy family.** The
null hypothesis is SUPPORTED by every independently reproduced measurement. The measured
exponent of the canonical generic algorithm (interval BSGS) is alpha = 0.4974 (R^2=1.0000)
over genuinely varied prime orders 2^10..2^22, and an independent reimplementation gives
alpha = 0.4876 (R^2=0.9934). No structural shortcut survived falsification across the
probe suite. Multi-target shared-base BSGS and the near-max-trace-CM / GLV structure
produce ONLY constant factors (2.6-4.3x), exactly as the generic lower bound predicts.

Nothing in this report claims a solved, broken, cracked, or breakthrough result.

---

## 1. Verified structural facts (synthetic family, by construction and by code)

| Fact | Value | Evidence |
|---|---|---|
| Base field | p = 4294966177 = 2^32 - 1119 (prime) | Miller-Rabin |
| Group order (toy) | l = 4294835173 (prime) | count + prime test |
| Trace | t = p + 1 - l = 131005 | algebra |
| t / 2*sqrt(p) | 0.9995 (near-max trace) | ratio |
| Cofactor | 1 (order of G = l) | verified mul |
| CM discriminant | D = -3 * 2419^2 (Q(sqrt(-3)), rank-2 endom) | t^2-4p |
| Embedding degree k | k > 1999 scan | MOV attack inapplicable |
| Anomalous? | no (#E != p) | Smart inapplicable |
| GLV eigen | lambda = 4021414523, phi(G)=lambda*G valid 500/500 | E1 |
| GLV interval-localization | REFUTED (k2 not small for k<N, no lattice collapse) | E1 + PN-2 |

## 2. Golden baselines (the reference lines)

L1 = genuinely varied prime orders (distinct curve+l per db, db 10..22 step 2):

| method | alpha | R^2 | n | class |
|---|---|---|---|---|
| bsgs (interval) | **0.4974** | **1.0000** | 7 | A (generic sqrt N, const ~1.38x sqrt N) |
| kanga (VOW) | 0.5189 | 0.6772 | 6 (of 7, one wallcap) | B* (sqrt, unstable variance) |

L2 = fixed toy order l=4294835173, depth db 22..30 (NOT in alpha fit):

| method | behavior |
|---|---|
| bsgs | perfect sqrt(depth) line, alpha=0.4999 R^2=1.0 (depth-only) |
| kanga | wallcap-skipped at db>=28 (budget W*24*sqrt N); heavy constants |

Golden fit invariants: bsgs steps/sqrt(N) gmean 1.38-1.47 across every db (constant small).

## 3. Independent reproduction (CLASS-4 requirement)

Fresh independent BSGS implementation (shared bug guard: duplicated affine arithmetic).
L1 genuine orders, 3 seeds, gmean: **alpha = 0.4876, R^2 = 0.9934, n=7, all ok=1.** This
confirms the golden slope; it does NOT reproduce a sub-sqrt line.

## 4. Probe results (falsification-first)

| Probe | Question | Result | Class |
|---|---|---|---|
| PN-1 shared-DP multi-target rho | first-hit ~ sqrt(N/K)? | slope vs log2(K) = -0.02..-0.15 (not -0.5); only a small constant at best | REFUTED |
| PN-2 GLV interval lattice | does lattice collapse near width sqrt(N)? | k2 ~ thousands..65k (>> sqrt N), no collapse | REFUTED |
| PN-4 Semaev surface | relation cost beats sqrt N? | relation surface cost ~ O(p) vs bsgs sqrt N | CONTROL-CONFIRMED (no win) |
| GPU depth | T4 depth scales exponent? | not executable (no CLI/GPU) | PENDING (honest) |

## 5. Hypothesis bank

- HYPOTHESES.json: 1000 entries, families A..T (20/20 coverage, 23..168 per family).
- Statuses after probes: CONSTANT 832, REFUTED 144, HYPOTHESIZED 24 (remaining cheap).
- Every non-trivial structural family (GLV, endomorphism, CM, multi-target,
  Semaev/IC, rho partitions, kanga tuning, Grover EMU) is REFUTED or CONSTANT at
  the alpha level or carries an explicit CLASS-2 (multi-target constant) label.
- Sources: core 42, variant 672, negative 7, composite 279. STAYS data-integrity-clean.

## 6. Literature map

LITERATURE_MAP.md: Shoup/Nechaev generic lower bound; Smart/anomalous, MOV/Frey-Ruck,
PH, XEDNI, GHS/Weil descent, index calculus — all structurally inapplicable or
super-exp on the toy; GLV (2001)/De Weger extended GLV — constant only; VOW (1999)
parallel collision; de Castro-Shokrollahi-Sudan preprocessing bound; multi-target
BBKT-style amortization — the ONLY verified lever, as constant.

## 7. Open research map

OPEN_RESEARCH_MAP.md lists the frontier: near-max-trace CM slab, x-only amortization
asymptotics (K->512), Semaev control, GPU depth. All marked honest expected-verdicts;
each has a falsification criterion. Nothing unmeasured is claimed.

## 8. Autotune

AUTOTUNE_RESULTS.csv: 6 kanga configs x db 16..24 x 3 seeds. kanga constant vs bsgs:
ratio 39x .. 400x (worse with W/b/K tuning variety). No config changed the sqrt class.
Confirms kangaroo is a workable-with-big-constant line, never a leading line on CPU at
these depths.

## 9. Anomaly engine

ANOMALY_AUDIT.csv: 5 STRUCTURAL sub-typical rows ADJUDICATED as E2 bulk multi-target
amortized (CLASS-2 constant lever), NOT single-instance sub-sqrt; 14 ok=0 wallcap/fail
rows logged as data, not hidden. Auto-flag list is empty of CLASS-4 triggers.

## 10. GPU note (honest)

No CUDA/nvcc/kaggle CLI available on the research box. kaggle_t4.py payload staged,
KAGGLE_RUNNER.py scheduler written with strict numeric-schema merge guard and
no-fabrication policy. KAGGLE_T4_TOTAL.csv intentionally empty.

## 11. Negative-result deliverables to carry forward

1. GOLDEN_BASELINE.csv/.md (72 rows)
2. INDEP_REPRODUCTION.csv/.md
3. PN1_MULTITARGET_RHO.csv, PN2_MAXTRACE.csv, PN4_SEMAEV.csv
4. AUTOTUNE_RESULTS.csv
5. ANOMALY_AUDIT.csv
6. HYPOTHESES.json (1000), LITERATURE_MAP.md, OPEN_RESEARCH_MAP.md
7. RESEARCH_STATE_SNAPSHOT.md

## 12. Known limitations (do not paper over)

- Point-counting to find genuinely-prime orders is O(p): feasible only to db<=22;
  deeper genuine-order variation is blocked WITHOUT a GPU or a better counting method.
- L2 (fixed-l depth) is a depth probe, not an exponent probe; careful readers must not
  conflate it with alpha evidence.
- rho/kanga fail some small prime-order instances (TypeError / non-invertible base at
  db 10-14) — the raw CSV rows are preserved in DISPUTES.csv as data, not silence.
- Grover runs are classical emulation with a stated oracle-query metric; no claim.
- Multi-target numbers are amortized per-key with one shared base; the single-instance
  alpha retains the sqrt floor.

## 13. Sign-off

The v3 web mission asked for an honest ebook-style WordPress guide. This lab completes
its scientific half: an auditable, reproducible, synthetic-only ECDLP benchmark with a
clean sweep of negative results, a 1000-entry falsified hypothesis bank, reproductions,
and surgical documentation of the frontier. The evidence supports Ho: the generic sqrt N
wall stands on this family. Any future sub-sqrt CLAIM must pass CLASS-4 (alpha<0.45,
R^2>0.95, >=6 genuinely varied orders, independent implementation, math proof) — no such
claim exists in this report.

Signed (autonomous loop, mission v3, 2026-09-23).