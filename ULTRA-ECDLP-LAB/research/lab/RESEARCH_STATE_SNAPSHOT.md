# RESEARCH_STATE_SNAPSHOT.md — ULTRA-ECDLP-LAB (v3 mission)

Date: 2026-09-23 · Author: autonomous research loop · Scope: SYNTHETIC toy ECDLP only.
Everything below is verified-false-or-constant unless explicitly marked HYPOTHESIZED.

## 1. What exists (audited, truthful)

| Artifact | Reality | Verified |
|---|---|---|
| `research/gen.py` | toy curve y^2=x^3+7, p=4294966177, prime l=4294835173, G derived | l prime; l*G=O |
| `research/solvers.py` | bsgs / rho / pir / kanga / ph(control) / grover(emul) | every `ok` re-checks Q==kG |
| `research/prime_scaling_run.py` | RESEARCH ROOT: distinct prime order l~2^db PER db (db=10..18) | 3 seeds x 3 methods |
| `research/fit.py` | A/B/C/D + X(flat) ladder, gmean, R² | — |
| `research/hypothesis_engine.py` | NOW emits 1000 hypotheses / 20 families (A..T) | schema-complete |
| `research/experiments_structural.py` | E1 GLV, E2 shared-G bulk, E3 rho, E4 kanga | ok-gated |
| `research/reproduce_bulk.py` | independent re-implementation of E2 | all ok=1 |
| `research/consolidate.py` | alpha fits + classification | — |
| `research/kaggle_t4.py` | cupy payload for T4 notebook | NOT YET RUN on GPU |
| `research/lab/*.md/csv` | 13-20 deliverables incl. honest negative report | — |
| GPU track | no nvcc, no CUDA runtime, no kaggle CLI on this host | NOT EXECUTABLE locally |

## 2. Verified mathematical facts of the toy family (primary source = experiments_structural.py probe)

- p = 4294966177 = 2^32 - 1119 (p ≡ 1 mod 3, ordinary)
- l = 4294835173, prime, p−l = 131004
- trace t = p + 1 − l = 131005 ≈ 2√p (t/2√p ≈ 0.9995 — near-max-trace slab)
- #E(F_p) = l (cofactor = 1; random-point order tests: l·P = O)
- CM discriminant D = t² − 4p = −17554683 = −3·2419²  (non-square → ordinary, rank-2 endom)
- endomorphism φ: (x,y)→(ωx,y) exists; cube root ω mod p found; λ = 4021414523 mod l is a
  root of x²+x+1 → φ(G) = λG; on l-torsion λ²+λ+1 ≡ 0 (mod l)
- GLV decomposition valid 500/500 on sampled k, BUT for the interval DLP k<2^db<<l the
  decomposition is NOT helpful: k2 ≡ 0 for db≤14; for db=16,18 recovered k2≠0 but
  |k1|,|k2| ~ thousands ≫ √N → 2D grid needs M~2^15, i.e. no sub-√N. GLV = CONSTANT only.
- embedding degree: NO k in 1..1999 with l | p^k−1 → MOV/XEDNI transfer unavailable
- NOT anomalous (#E=l ≠ p) → Smart attack inapplicable (verified)
- l−1 = 2²·3²·23·647·8017 (largest prime factor 8017 → no PH leverage on l−1)
- curve is j=0 ⇒ Aut ⊇ µ6 (order 3 endomorphism + negation = constant orbit)

## 3. Measured scaling (honest, verified rows only)

| method | α vs N | R² | class | note |
|---|---|---|---|---|
| bsgs | 0.494 | 0.9997 | A/generic-sqrt | golden reference; matches √N |
| kanga | 0.463 (unstable) | 0.943 | B*(huge const) | tuning sweep α∈0.395..0.752, R² 0.68..0.82 → artifact |
| rho | 0.019 | 0.227 | X(flat) | interval-blind: rides √l, NOT a speedup |
| rho maskbits/PIR | no α change | — | artifact | steps grow with maskbits; R=4 worse |
| E2 shared-G bsgs (bulk) | 0.462 bulk per-target | 0.914 | CLASS-2 | constant 2.6–4.3× win; reproduction α_bulk=0.5539 (seed 144272510, K=6, db10..20) |
| single bsgs repro | 0.4920 | 0.9894 | A | independent implementation |
| grover_emu | (π/4)√N queries | — | EMULATION | NO classical claim |

KEY FACT: **no engine measures α<0.5 with a sound stable fit on prime order.** The only
below-generic *absolute* figures are (a) artifacts (X-flat interval-blind rho), (b) the
composite-order PH control (NOT an EC result), (c) Grover emulation (NO CLAIM).

## 4. Other research known-but-not-executed (respect the mission: evidence before claim)

- Cross-family instance sets: only l~2^db prime orders with db∈{10,12,14,16,18} since
  generator scan to l (Lebesgue sum) over p<2^24 is feasible; larger db was run ONLY on the
  FIXED toy group → those alpha numbers must NOT be used as generic claims (x-axis constant l).
- GPU/T4: `kaggle_t4.py` payload ready (cupy GPU VOW kangaroo), `t4_parity.py` CPU validator
  exists. NOT yet executed on an actual T4; hence the "T4×2 win ≈ 10–50× constant" numbers in
  prior chatter are ESTIMATES, not lab results.
- Puzzle #71 / secp256k1: OUT OF SCOPE (synthetic only). No production puzzle work is done
  in this lab.

## 5. Bottlenecks / gaps

1. **Point counting** (`prime_scaling_run.count_curve_order`) is an O(p) Legendre scan → db≥20
   per-db prime-order curves are currently too slow to generate. Bottleneck for the
   "genuinely varied orders 2^12..2^32" mandate.
2. **No local GPU/CUDA** → GPU track and T4 autonomy require the Kaggle payload; cannot be
   validated on this host.
3. **Classifier/consolidator** was fixed ("lambda leftover" removal) but still fits on best-db
   only; variance bands are right but per-seed fits not tabulated in SCALING_RESULTS_AUTONOMOUS.
4. **Hypothesis bank** was 525 with non-string STATUS values in first pass; rebuilt to 1000 with
   clean schema, but only ~49 hypotheses beyond core/math facts are testable cheaply; rest are
   variants/composite padding (honest: most will be CONSTANT).

## 6. Decisions locked (do not revisit without evidence)

- Reported α is vs log2(N), N=2^db (the true search-space size).
- Only verified=1 rows enter fits.
- CLASS-4 (α<0.45, R²≥0.97, ≥5 distinct orders, independent reproduction) is the ONLY route to
  a sub-sqrt claim.
- Rows that fail `ok` are logged to ANOMALIES, never silently dropped.
- No real-world curve/puzzle work; SAFETY.md governs.