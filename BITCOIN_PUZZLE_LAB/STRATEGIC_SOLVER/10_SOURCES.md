# 10 — Sources

## Data Sources

| Source | URL/Location | Content |
|---|---|---|
| Bitcoin Puzzle tracker | `dataset/raw_tracker.txt` | 160-row pipe-delimited tracker |
| privatekeys.pw | privatekeys.pw | Puzzle status, balances, addresses |
| btcpuzzle.info | btcpuzzle.info | Community puzzle information |
| BitcoinTalk | bitcointalk.org | Original puzzle announcement (2015-01-15) |
| Hacker News | news.ycombinator.com/item/41547395 | Puzzle discussion thread |

## Algorithm References

| Reference | What It Covers | Relevance |
|---|---|---|
| Pollard (1978) | Kangaroo method | Foundation of v4 solver |
| van Oorschot & Wiener (1999) | Parallel collision search | RCKangaroo basis |
| Teske (2006) | Jump distributions | 16-bucket table design |
| Shanks (1971) | Baby-step Giant-step | v3 BSGS solver |
| Washington (2008) | Elliptic Curves | secp256k1 properties |

## Existing Tools (Referenced, Not Used)

| Tool | Author | Algorithm | Hardware |
|---|---|---|---|
| BitCrack | brichard19 | R1 brute-force | GPU (CUDA) |
| JeanLucPons/Kangaroo | JeanLucPons | R2 kangaroo | GPU (CUDA) |
| Keyhunt | miguelamartino | R2 kangaroo/BSGS | GPU (CUDA) |
| RCKangaroo | RetiredCoder | R2 kangaroo | ~400× RTX 4090 |

## Code Repositories

| Repo | Path | Content |
|---|---|---|
| BITCOIN_PUZZLE_LAB | `.` | Main research lab (this project) |
| BITCOIN_PUZZLE_RESEARCH | `../BITCOIN_PUZZLE_RESEARCH/` | Reconstructed pipeline (44 tests) |
| RECONSTRUCTED_CODE | `../BITCOIN_PUZZLE_RESEARCH/RECONSTRUCTED_CODE/` | Canonical build |

## Published Solve Data

| Puzzle | Date | Solver | Method | Key |
|---|---|---|---|---|
| #1-#50 | 2015 | Community | Brute-force | Published |
| #64 | 2022-09-09 | — | Last no-pubkey solve | Published |
| #65 | 2022-09 | — | Kangaroo (65-bit) | Published |
| #66 | 2024-09-12 | 1Jvv4y... | Brute-force race | `0x2832ed74f2b5e35ee` |
| #125 | 2026-07 | RetiredCoder | RCKangaroo | Published |
| #130 | 2026-07 | RetiredCoder | RCKangaroo (~400 GPU) | Published |
| #135 | 2026-07-28 | RetiredCoder | RCKangaroo | `0x6d9392...` |

## Safety Contract

- **PRIVATE-KEY BOUNDARY:** No private key for unsolved puzzles is in this repository.
- **SYNTHETIC_ONLY:** All testing uses toy keys, not real puzzle keys.
- **NO FUND EXTRACTION:** No transactions, no wallet access, no node RPC.
- **PUBLIC RECORD ONLY:** Published keys are public data for verification.
