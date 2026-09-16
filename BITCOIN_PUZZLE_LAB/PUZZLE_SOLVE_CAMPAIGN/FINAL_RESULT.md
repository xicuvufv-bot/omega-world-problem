# FINAL_RESULT.md

## STATE: **NOT SOLVED**

## Mission status
No previously unsolved public puzzle has been solved. This is declared only
after the evidence below; per the campaign rules, "campaign complete" is NOT
claimed — it cannot be, until every realistically feasible target is exhausted
with evidence or one is actually solved. The feasibility analysis shows the
remaining targets are compute-bound, not knowledge-bound, and this environment
does not hold that compute.

## Current best target
- **Puzzle #67 (R1, 67-bit)** — smallest interval in the unsolved corpus
  (≈2^66 expected hash evals), address `1MVDYgVaSN6iKKEsbzRUAYFrYJadLYZvvZ`,
  reward 6.7 BTC. Follows the same brute-force-race pattern that solved #66
  (65-bit) in 2024-09.
- Secondary: **#140 (R2)** — 14.0 BTC; the only regime where our verified v5
  (fused+negation, 2.54x) advantage operates.

## Percentage / completeness of search
- #67: **0.00%** (0 of ≈2^66 keys). Nothing was scanned in this environment.
- All R2: 0.00%.
- The corpus-side search (structural hypotheses) is effectively complete: every
  membership/pattern/leakage hypothesis that could be posed and tested was
  answered (9/9 avenues, uniform-negative — FAILED_APPROACHES.md).

## Strongest evidence
- v5 kangaroo: **49/49 correct solves, w=20-34**, median 2.69x wall speedup —
  the strongest verified constant-factor solver in the repo (evidence runs in
  SOLVER_LAB/benchmarks + candidate/).
- 83/83 published keys verified end-to-end through the original address chain.
- The 83-key corpus is uniform: EX1/EX2/EX3/H5/H6 + spectral + spread all
  negative — there is NO discovered structure to exploit forward.

## Remaining search space
- ≈2^66 keys for #67; ≈2^139-2^140 for each R2; structurally irreducible at
  the Θ(√W)/uniform-DLP level confirmed by EX5.

## Strongest unresolved hypothesis
- A reconstructed generator/CSPRNG weakness in the puzzle author's tooling
  (public BitcoinTalk thread, 2015-01-15) COULD collapse an interval — but
  EX2's null-expectation analysis bounds any such predictor to "no better than
  null + 3σ," so this is not an actionable lead, only the least-dead hypothesis.

## Exact next computational step (honest)
1. Acquire GPU hash160-scan capability (BitCrack/KeyHunt class, ~2-6 Gkey/s
   per RTX 4090 published). (No v5 involvement — R1.)
2. Benchmark that exact configuration for 10 minutes; extrapolate measured
   keys/s into a chunk schedule — no claimed estimate without the benchmark.
3. Scan #67 in checkable 2^44-key chunks with resumable checkpoints.
4. On any pubkey-matching hash: verify per VERIFICATION.md (interval, kG
   recompute, address chain) and append to CANDIDATES.md.
- Expected on 400 GPUs ≈ 2.3 yr; on a community-scale 2000-GPU effort ≈ ~6
  months (the #66 pattern). On this single machine: ~2^33x beyond feasible.

## Why previous attempts failed (and nothing "changed")
- They did not fail computationally — they were never computed. Every attempt
  hit the same wall: unsolved puzzles are ≥67-bit, this environment is a single
  CPU with a w=34 kangaroo ceiling. The 2.5x solver gain is real but dwarfs
  against a ~2^33x compute gap on ANY single machine.
- No script, speedup, or re-ranking changes that gap. Only hardware changes it.

## Close-out condition
This campaign remains OPEN. It enters a waiting/blocked state that converts to
action the moment either (a) GPU hash-scan compute is available, or (b) a new
structural result emerges. No success will be declared on a "plausible
candidate," a "resembling pubkey," or a partial hash match.