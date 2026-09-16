# Known Patterns from 83 Solved Puzzles

## Pattern Status Summary

| # | Pattern | Status | Evidence |
|---|---------|--------|----------|
| 1 | Low-4-bit degeneracy (x≡9 or 13 mod 16) | DISPROVEN | EX1: QR(16)={0,1,4,9}, candidates={5,9}, all buckets 16/16 |
| 2 | Low-nibble distribution non-uniformity | DISPROVEN | EX1: measured ~312/bin for 5000 points, max dev 45 |
| 3 | Bits 120–123 degenerate under kangaroo | DISPROVEN | EX1: all widths 8–28 give 16/16 distinct |
| 4 | Hamming weight biased (mean 0.516, p<0.01) | DISPROVEN (directional) | EX3: train mean=0.539, test mean=0.493 (opposite) |
| 5 | Keys carry weak-PRNG artifact | DISPROVEN | EX2: null+3σ exceeded, no large-key matches |
| 6 | Benford's law on first digit of (k-lo) | DISPROVEN (non-replicated) | EX3: train p<0.01, test p>0.05 |
| 7 | Relative position biased toward 0.5 | DISPROVEN | EX3: KS p>0.01 in both splits |
| 8 | Reward correlation (higher puzzle → more biased) | DISPROVEN | EX3: r=0.01 (train), r=0.06 (test), both p>0.05 |
| 9 | Parity or mod-3 structure | DISPROVEN | EX3: even/odd split ~50/50, mod-3 uniform |

## Key Fact: ALL 83 recorded private keys are consistent with high-entropy uniform random draws within their respective intervals.

No exploitable structure was found across any of the 11 statistical metrics,
tested on both a train split (odd-n puzzles) and an independent test split
(even-n puzzles), using p<0.01 replication criteria.

## Correction to v4 Docstring

The `solvers/v4_kangaroo.py` docstring claims the low-4-bit degeneracy is
the reason for a previous 20-bit timeout. This claim is now **empirically
disproven** by EX1. The real fix for the old timeout was the trail/restart
redesign (different algorithmic approach), not bucket selection.
