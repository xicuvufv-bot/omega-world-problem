# LIVE_PROGRESS.md — Campaign status log

## Entry 1 (opening)
- State: **NO SEARCH IN FLIGHT.** Single CPU only; all unsolved targets are
  ≥67 bits. v5's verified ceiling is w=34 (~60s solves). No GPU hash160/kangaroo
  pipeline exists in this environment.
- Targets decided: #67 (R1 primary — smallest interval), #140 (R2 secondary —
  only regime where our v5 advantage applies).
- Search completeness: **0.00% of #67** (0 of ~2^66 range evaluated).
- Reef/calibration: 0 candidates. 83 published keys remain the corpus.

## Milestones
| # | Milestone | Date | Result |
|---|---|---|---|
| 1 | Re-rank complete | today | #67 then #68 then #140 (see TARGET_SELECTION.md) |
| 2 | Compute basis re-verified | today | #66 pattern (65-bit race solve, 2024) => #67 next |
| 3 | — (blocked on compute) | — | — |

## Decisions gate (adaptive switching)
- Asked every milestone: "Has our probability of solving this target
  materially improved?"
- Today: **NO for every target** — no new structural result exists; the
  binding constraint is hardware, not knowledge.
- Therefore further target-switching is pointless until compute changes; no
  target is re-selected from computational data alone.

## Next update when: hardware / GPU pipeline status changes, a race is detected,
a candidate is produced, or a cluster becomes available.