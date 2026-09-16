# FAILED_APPROACHES.md — Every structural avenue tested against real keys

| # | Approach | Where | Outcome |
|---|---|---|---|
| 1 | Low-4-bit x degeneracy buckets | EX1, `ex1_x16_degeneracy.py` | DISPROVEN — uniform nibbles; was a curve artifact (x≡9/13 mod 16), not exploitable |
| 2 | Static PRNG pattern in solved keys | EX2 v2 `ex2_prng_test.py` | HONEST NEGATIVE — null-expectation design; no predictor beats null+3σ at n≥40 |
| 3 | Hamming / Benford structure | EX3 `ex3_structure_battery.py` | HONEST NEGATIVE — train/test opposite directions; not replicable |
| 4 | k-parity -> x-parity deterministic map (claims 2x) | H5 `test_parity.py` | DISPROVEN — 16/28/19/20 spread |
| 5 | High-bit leakage k vs X(kG) | H6 `test_h6_bits.py` | REFUTED — worst φ=0.0196, 0/1600 survive FWER |
| 6 | Spectral-mix bucket hash (Miller-Venkatesan) | `test_bucket_hash.py` | NEUTRAL — 0.991, 15/15 |
| 7 | Pollard 2025 spread=6 | `test_spread.py` | INCONCLUSIVE at w=20 (1.195); unadopted |
| 8 | 16-fold root-of-unity search reduction | theory check | RULED OUT — p≡15, n≡13 (mod 16); no 16th root of unity in either field |
| 9 | Asymptotic speedup (any) | EX5 `ex5_curve_floor.py` | CONFIRMED Θ(√W) floor; K floor 0.51 unreachable in serial design |

## What those failures prove together
The 83 solved keys are uniform independent draws; the curve yields no search-
space reduction; the only wins are constant factors (fused inversion 2.0x,
negation map 1.42x — both verified and now inside v5). No combination of shifts
this campaign's findings can cut #67 or #140 search work by even one bit of
the interval.