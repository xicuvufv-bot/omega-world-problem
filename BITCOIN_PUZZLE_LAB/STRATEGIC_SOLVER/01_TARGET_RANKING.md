# 01 — Target Ranking

Priority Score = Feasibility(0-5) × ScientificValue(0-5) × Novelty(0-5) / 10

## Ranking Table

| Rank | Puzzle | Bits | Regime | Public Key? | GPU-yr (single) | Feasibility | ScientificValue | Novelty | Priority | Notes |
|---|---|---|---|---|---|---|---|---|---|---|
| **1** | **#140** | **140** | **R2** | **Yes** | **~1,998** | **2** | **5** | **3** | **3.0** | **Smallest R2; direct kangaroo attack; benchmark target** |
| 2 | #71 | 71 | R1 | No | ~15,000 | 1 | 3 | 1 | 0.3 | Cheapest R1; no pubkey; hash scan only |
| 3 | #145 | 145 | R2 | Yes | ~15,984 | 1 | 4 | 2 | 0.8 | Second R2; 2x harder than #140 |
| 4 | #66 | 66 | R2* | Yes | ~19.9 (CPU) | 5 | 3 | 2 | 3.0 | Already solved 2024-09; benchmark proxy |
| 5 | #72 | 72 | R1 | No | ~29,900 | 1 | 3 | 1 | 0.3 | R1; no pubkey |
| 6 | #150 | 150 | R2 | Yes | ~63,928 | 1 | 4 | 2 | 0.8 | Third R2; 8x harder than #140 |
| 7 | #73 | 73 | R1 | No | ~59,900 | 1 | 3 | 1 | 0.3 | R1 |
| 8 | #74 | 74 | R1 | No | ~119,800 | 1 | 3 | 1 | 0.3 | R1 |
| 9 | #135 | 135 | R2* | Yes | ~1,200 | 2 | 3 | 1 | 0.6 | Already solved 2026-07 by RetiredCoder |
| 10 | #155 | 155 | R2 | Yes | ~511,424 | 1 | 4 | 2 | 0.8 | Fourth R2 |
| 11 | #160 | 160 | R2 | Yes | ~2,045,700 | 0 | 5 | 3 | 0.0 | Hardest R2; Bitcoin's last line |
| 12-13 | #76,#77 | 76-77 | R1 | No | ~480k-960k | 0 | 2 | 1 | 0.0 | Deep R1 |

## Why #140 Is Best Target Now

1. **Smallest R2 puzzle** — only 5 puzzles have exposed pubkeys, and #140 is the easiest.
2. **Kangaroo-amenable** — our v4 solver (plus fused 2.0x improvement) is the exact algorithm needed.
3. **Public key published** — `031f6a33...6640`, address `1QKBaU6WAeycb3DbKbLBkX7vJiaS8r42Xo`, reward 14.0 BTC. All public-record data.
4. **Benchmark target** — RetiredCoder solved #135 (135 bits) in ~2 months with 400× RTX 4090. #140 is 5 bits harder = ~4× more work = ~8-10 months on same hardware.
5. **Scientific value** — would be the next confirmed kangaroo solve, advancing the puzzle state-of-the-art by 5 bits.

## Attack Order (Fused Kangaroo, 400× RTX 4090 cluster)

| # | Puzzle | Fused GPU-yr | Wall-time (400 GPUs) | Difficulty |
|---|---|---|---|---|
| 1 | #140 | ~1,998 | ~5 years | Substantial |
| 2 | #145 | ~15,984 | ~40 years | Infeasible |
| 3 | #150 | ~63,928 | ~160 years | Infeasible |

## Status

#140 is the active target. Ready to run on GPU when compute budget allows.
