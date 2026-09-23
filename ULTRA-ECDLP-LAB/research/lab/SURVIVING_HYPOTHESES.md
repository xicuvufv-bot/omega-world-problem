# SURVIVING HYPOTHESES — survive current data (with honest ceilings)

Only hypotheses that have clean, reproduced experimental support are listed. STATUS is
the strongest label the data will honestly tolerate.

## E2: shared-base multi-target BSGS amortization
- CLAIM: one baby table for the fixed G serves K targets; per-target amortized cost is
  roughly (build + K·giants)/K ~ √N with a smaller constant.
- EVIDENCE: db=10..18, K=5: bulk per-target steps 20.4/25.0/79.4/78.2/283.8 vs independent
  53.4/90.0/208.4/335.2/796.8 → ~2.6–4.3x fewer steps. Independent reproduction (different
  seed, K=6, db=10..20): bulk amortized α=0.554 R²=0.98; all keys ok-verified.
- RESULT: **CLASS-2 (engineering constant factor).** α stays ~0.5. NOT sub-sqrt.
- CEILING: cannot cross the √N barrier for a single target; only batch constant.

## GLV lattice structure (validated, but no DLP win here)
- CLAIM: the endomorphism exists and decomposes k (500/500).
- EVIDENCE: ω, λ, φ(G)=λ·G all verified exactly.
- RESULT: survives as a *fact about the curve*, but REFUTED as a DLP speedup for the
  interval formulation. Kept only as correct background, not as an advantage.