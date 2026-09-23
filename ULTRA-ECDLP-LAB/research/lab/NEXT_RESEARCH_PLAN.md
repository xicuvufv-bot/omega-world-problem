# NEXT RESEARCH PLAN — what to do after today's sweep

## 1. Immediate (local CPU, cheap, high information)
- L1: Deepen the **near-max-trace slab** probe: enumerate the CM ring's unit group for
  t = p+1-l with D = -3·2419² (square-free part 3). The cubic endomorphism is exactly
  the cube root of unity; check whether a 2nd independent endomorphism (outside
  Z[ζ3]) exists at this trace — if it does, GLV-2D might apply in the full-range regime.
  This is the ONE open algebraic lead the data did not close.
- L2: Batch-BSGS constant curve (db=18..24, K=8..16, multi-seed) to pin the amortized
  constant precisely for the KAGGLE report.
- L3: Reproduce bsgs α=0.494 once more with a *second independent implementation*
  (different dictionary/loop structure) as a REPRODUCTIONS.csv entry.

## 2. Kaggle T4×2
- Run the 4 jobs in KAGGLE_RESULTS.csv (B_scale, B_glv, B_kanga_stab, B_repro).
- Any sub-0.45 α with R²>0.95 on ≥6 sizes → CLASS-4 path below.

## 3. CLASS-4 escalation path (only if triggered)
1. Independent re-implementation (new file, new author-style, new seeds).
2. Mathematical derivation of WHY α < 0.5 (the lattice/group why).
3. Counterexample search (biggest k, adversarial sizes).
4. 10+ genuinely varied prime orders with different bit structure.
5. Only then: report as CLASS-4, not "breakthrough".

## 4. Saturation guard
- Stop chasing kanga/rho parameter tuning (2 prior sweeps: no effect).
- Stop pretending GLV matters for the interval formulation (counterexample-backed).
- Any "AI-generated conjecture" that re-enters #1-#3 is fine; any that claims
  sub-sqrt without the CLASS-4 gate is rejected.

## 5. Deliverable cadence
- Update: SCALING_RESULTS.csv, REPRODUCTIONS.csv, ANOMALIES.csv, KAGGLE_RESULTS.csv,
  HYPOTHESES.json statuses, CLASSIFICATION_AUTONOMOUS.csv, and this plan.md.
- Highest priority next experiment: **L1 (unit-group / endomorphism-rank probe).**