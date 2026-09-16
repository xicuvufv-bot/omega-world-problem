# 07 — Benchmarks

## Complete Benchmark Data

### A. Key Enumeration Throughput (CPU, single core)

| Variant | Keys/sec | Speedup vs v1 |
|---|---|---|
| v1 naive (scalar_mult per key) | 13,646 | 1.00x |
| v2 stride (jac_add_affine) | 43,234 | 3.17x |
| v2 masked (stride + bucket prefilter) | 44,763 | 3.28x |
| v2 pure stride (no hash) | 125,471 adds/s | 9.19x |

### B. Interval DLP Scaling (CPU, single core)

| Width | BSGS time | BSGS mem | Kangaroo time | Kangaroo hops | Theory hops | Ratio |
|---|---|---|---|---|---|---|
| w=16 | 0.062s | 182 | 0.391s | 212 | 226.9 | 0.93 |
| w=20 | 0.297s | 725 | 1.812s | 1,762 | 907.5 | 1.94 |
| w=24 | 0.844s | 2,897 | 5.516s | 1,895 | 3,630.0 | 0.52 |
| w=28 | 3.312s | 11,586 | 31.328s | 28,845 | 14,519.9 | 1.99 |

### C. Fused Kangaroo (EX4, 36 cases)

| Width | Baseline ms/hop | Fused ms/hop | Speedup | Cases | Keys OK | Walk OK |
|---|---|---|---|---|---|---|
| w=16 | 4.45 | 2.15 | 2.23x | 9 | 36/36 | 4/4 |
| w=20 | 17.83 | 8.45 | 1.92x | 9 | 36/36 | 4/4 |
| w=24 | 89.62 | 43.05 | 1.99x | 9 | 36/36 | 4/4 |
| w=28 | 8.97 | 4.96 | 1.84x | 9 | 36/36 | 4/4 |
| **ALL** | **30.22** | **14.65** | **2.00x** | **36** | **36/36** | **4/4** |

### D. Solved Key Statistics (83 keys)

| Metric | Value | Expected (uniform) |
|---|---|---|
| Relative position mean | 0.514 | 0.500 |
| Hamming weight fraction mean | 0.516 | 0.500 |
| Top nibble distribution | 16/16 distinct | 16/16 |
| Last nibble distribution | 16/16 distinct | 16/16 |
| Parity (odd/even) | 39/44 | ~41.5/41.5 |

### E. Curve Properties (EX5)

| Property | Value | Implication |
|---|---|---|
| Cofactor h | 1 | No subgroup attack |
| j-invariant | 0 | CM by Z[ω], ω = cube root |
| GLV λ | Verified (λ³=1 mod n) | Speeds scalar-mult, not walks |
| Group order n | Prime | No Pohlig-Hellman |
| Asymptotic floor | Θ(√W) | No asymptotic shortcut |

## GPU Extrapolation (RTX 4090)

| Puzzle | Bits | Raw GPU-yr | Fused GPU-yr | Wall-time (400 GPUs) |
|---|---|---|---|---|
| #140 | 140 | 7,010 | 3,505 | ~8.8 years |
| #145 | 145 | 56,100 | 28,050 | ~70 years |
| #150 | 150 | 224,000 | 112,000 | ~280 years |
| #155 | 155 | 1,800,000 | 900,000 | ~2,250 years |
| #160 | 160 | 7,180,000 | 3,590,000 | ~8,975 years |

**GPU model:** RTX 4090 at 8×10^9 group ops/s.
**Fused factor:** 2.0x (EX4 verified).
