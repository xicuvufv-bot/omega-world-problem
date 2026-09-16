# TARGET_ANALYSIS.md — Puzzle #67 deep dive

## Identity
- Puzzle: **#67**. Interval [2^66, 2^67 - 1] (67 bits).
- Address: `1MVDYgVaSN6iKKEsbzRUAYFrYJadLYZvvZ` (public).
- Reward: **6.7 BTC** (puzzle N funds N x 0.1 BTC).
- Public key: **NOT published** (R1 regime).
- Verification: privkey -> pubkey -> (SHA256 -> RIPEMD160 -> base58check)
  == known address.

## Why this is the weakest target in the corpus
- Smallest interval of all 77 unsolved puzzles (2^66 vs ≥2^139 for R2).
- The same regime as the most recent community one-off solve: #66 (65-bit)
  was brute-forced by a race in 2024-09. #69+ double the work each step.

## Construction analysis (from the 83-key corpus)
- Early keys (#1-#15) are hand-picked / small integers (0x1, 0x3, 0x7...).
- Transition to pseudorandom keys around #15; all later keys pass uniform
  tests (EX1/EX2/EX3/H6 negative). No RNG weakness to exploit forward.
- Nothing about #67 distinguishes it from a uniform draw in [2^66, 2^67-1].

## Attack surface
- Only surface: exhaust the interval against the address's hash160.
- No BSGS / kangaroo possible (no pubkey; hash160 is one-way).
- No known clue structure beyond the interval.

## Compute math (honest, benchmarked basis)
- Expected ~7.4e19 evaluations (2^66).
- Our measured pure-CPU rate 125,471 keys/s => ~1.9e7 years (this machine: NO).
- Published GPU-rate class 2-6 Gkey/s/4090: 400-GPU cluster ~2.3 yr;
  2000-GPU community-class effort ~6 months (the #66 pattern).

## Decision record
- Chosen as PRIMARY because the mission criterion is "weakest realistically
  solvable," not "biggest prize." Realism is still zero on a single machine;
  the plan quantifies the smallest cluster that makes it nonzero.
- Secondary: #140 (the only target where our verified v5 advantage operates).

## Risk register
- Other communities may already run #67-style scans; a solve is a race.
- Reward 6.7 BTC is small relative to cluster cost — purely technical/scientific
  value unless the cluster is otherwise idle.