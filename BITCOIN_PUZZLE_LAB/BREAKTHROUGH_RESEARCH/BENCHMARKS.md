# Benchmarks

## A. Key Enumeration Throughput

| Variant | Keys/sec | Improvement |
|---|---|---|
| v1 (naive bit-math) | 13,646 | baseline |
| v2 stride-only | 43,234 | 3.2x |
| v2 masked (low bits) | 44,763 | 3.3x |
| pure stride (no privkey) | 125,471 | 9.2x |

## B. DLP Solver Comparison (Published Numbers)

| Width | BSGS time | BSGS mem | Kangaroo time | Kangaroo mem | Kangaroo/GPU-yr |
|---|---|---|---|---|---|
| w=16 | 0.062s | 182 | 0.391s | 212 | 0.93 |
| w=20 | 0.297s | 725 | 1.812s | 1,762 | 1.94 |
| w=24 | 0.844s | 2,897 | 5.516s | 1,895 | 0.52 |
| w=28 | 3.312s | 11,586 | 31.328s | 28,845 | 1.99 |

## C. Statistical Structure (All Negatives)

| Test | Value | Significance |
|---|---|---|
| Relative position mean | 0.514 | p>0.01 (not biased) |
| Hamming weight mean | 0.516 | p<0.01 combined but **fails train/test replication** |
| Uniform nibble distribution | 16/16 | at all widths 8–28 |
| Decile concentration | 5–14 | consistent with uniform |

## D. EX4: Fused vs Baseline Kangaroo (Primary Result)

### Per-Width Breakdown

| Width | Baseline ms/hop | Fused ms/hop | Speedup | Cases |
|---|---|---|---|---|
| w=16 | 4.45 | 2.15 | 2.23x avg | 9 |
| w=20 | 17.83 | 8.45 | 1.92x avg | 9 |
| w=24 | 89.62 | 43.05 | 1.99x avg | 9 |
| w=28 | 8.97 | 4.96 | 1.84x avg | 9 |

### Full Summary

- **Average speedup:** 2.00x
- **Median speedup:** 1.98x
- **Min speedup:** 1.15x (w=16, small hop count)
- **Max speedup:** 4.00x (w=16, tiny startup amortized)
- **Key recovery:** 36/36 correct
- **Walk identity:** 4/4 bucket-sequence comparisons match
- **Hop delta:** ≤1 in all 36 cases (detection-timing endpoint shift)

### Correctness Verification

| Check | Result |
|---|---|
| All keys found (same key both variants) | ✓ 36/36 |
| Same bucket sequence (walk identity) | ✓ 4/4 sampled |
| Hop delta ≤ 1 (expected from endpoint shift) | ✓ 36/36 |
| j-invariant = 0 (EX5) | ✓ verified |
| Cofactor h = 1 (EX5) | ✓ verified |
