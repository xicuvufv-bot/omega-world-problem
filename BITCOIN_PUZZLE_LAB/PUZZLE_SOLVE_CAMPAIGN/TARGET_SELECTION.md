# TARGET_SELECTION.md — 8-Criterion Re-Rank (ALL unsolved)

Source data: `dataset/raw_tracker.txt` (160 rows), STRATEGIC_SOLVER/01, 09,
SOLVER_LAB evidence. All unsolved targets are **≥ 67-bit**; none is solvable
on a single workstation. The re-rank below therefore orders by *realistic
probability given cluster-grade resources*, then phases for what each solver
class can attack.

## Criteria weight (mission-specified)
1. Probability of solution   (weight 0.24)
2. Remaining search complexity (0.18)
3. Structural weaknesses      (0.14)   — all tapped: see STRUCTURAL_FINDINGS.md
4. Information from solved instances (0.12) — 83-key corpus, uniform (negative)
5. Available clues            (0.08)   — pubkey is the only R2 "clue"
6. Reward                     (0.08)   — N x 0.1 BTC per puzzle
7. Verification simplicity    (0.08)
8. Expected time-to-solution  (0.08)

## The universe (all 77 unsolved)
- **R1 (no public key):** #67-#74, #76-#84, #86-#89, #91-#94, #96-#99,
  #101-#104, #106-#109, #111-#114, #116-#119, #121-#124, #126-#129, #131-#134,
  #136-#139, #141-#144, #146-#149, #151-#154, #156-#159  → attack = hash160
  scan of [2^(N-1), 2^N - 1]. Cheapest first few: **#67 (2^66 avg)**, #68, #69.
- **R2 (public key published):** **#140, #145, #150, #155, #160**  → attack =
  Pollard kangaroo in the bit interval (our v5 solver applies).

## Re-Rank table

| Rank | Puzzle | Regime | Search cost (single RTX 4090) | Reward | Time-to-solve (400× GPU) | Feasibility score | Verdict |
|---|---|---|---|---|---|---|---|
| 1 | **#67** | R1 | ~**937** GPU-yr hashscan | 6.7 BTC | ~**2.3 yr** | 2 (cluster-only) | Already-solved pattern (#66 was 65-bit, solved by race) |
| 2 | **#68** | R1 | ~1,875 GPU-yr | 6.8 BTC | ~4.7 yr | 2 | 2x #67 |
| 3 | #140 | R2 | ~**1,400** GPU-yr (v5 kangaroo) | 14.0 BTC | ~**3.5-4 yr** | 2 | Smallest R2; only our solver's home regime |
| 4 | #69 | R1 | ~3,750 GPU-yr | 6.9 BTC | ~9.4 yr | 1 | |
| 5 | #70 | R1 | ~7,500 GPU-yr | 7.0 BTC | ~18.7 yr | 1 | |
| 6 | #145 | R2 | ~11,200 GPU-yr | 14.5 BTC | ~28 yr | 1 | 8x #140 |
| 7 | #150 | R2 | ~25,000 GPU-yr | 15.0 BTC | ~63 yr | 0 | |
| 8 | #155 | R2 | ~201,000 GPU-yr | 15.5 BTC | ~500 yr | 0 | |
| 9 | #160 | R2 | ~1,436,000 GPU-yr | 16.0 BTC | ~3,590 yr | 0 | Θ(√W) floor |

(R1 costs from repo benchmark basis #71≈15,000 GPU-yr; R2 from 09_BLOCKED_TARGETS
v5 figures; 400× GPU is RetiredCoder-class, justified by their #135 solve in ~2 months.)

## Selection
- **Primary attack track: #67 (R1).** Smallest search space in the entire
  unsolved corpus (≈2^66 hash evals). Follows the exact pattern of the 2024
  community solves of #66. Requires a hash160 bloom-scan pipeline (BitCrack /
  KeyHunt class) on multiple GPUs — none of our v5 kangaroo optimizations apply
  to R1 (no pubkey).
- **Secondary attack track: #140 (R2).** Our lab's *only* verified-advantage
  regime (v5 fused+negation = 2.5x). If a cluster is available for kangaroo,
  this is the target our own tooling is best positioned for.

## Why nothing below 67 bits exists
The tracker's highest one-off solve before the 2026 kangaroo run was #66
(65-bit, community brute-force race, 2024-09). Every interval < #67 is drained.

## Honest bottom line
Given THIS machine (single CPU, no kangaroo/hashscan GPU pipeline, v5 ceiling
w=34), probability of solving any unsolved puzzle = **0.00**. The re-rank above
quantifies what infrastructure would be required for a nonzero attack and
names the exact first target (#67) and the best solver-regime target (#140).