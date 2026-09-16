# STRUCTURAL_FINDINGS.md — Everything the 83-key corpus and curve math actually say

Verdict up front: **no structural weakness has survived replication.** Every
avenue that would reduce the effective search space below its interval was
tested and failed. The 83 solved keys behave like uniform random draws from
their intervals.

## Corpus-level (83 solved keys, reconstructed in RECONSTRUCTED_CODE, verified 83/83)
| Finding | Test | Result |
|---|---|---|
| Low nibbles of x degenerate? | EX1, 5000 points | FALSE — uniform nibbles |
| Static PRNG pattern in keys? | EX2 v2, null-expectation design | HONEST NEGATIVE — no strategy beats null+3σ |
| Hamming bias directional? | EX3 dual-split | Negative — p<0.01 appears but in OPPOSITE train/test directions |
| Benford on key digits? | EX3 | Not replicable (train 40.3 / test 6.2) |
| Bit position correlations? | EX4-era + H6 (2^15 samples, 1600-pair FWER) | REFUTED — worst φ=0.0196, 0 survive correction |
| k-parity → x-parity? | H5 | DISPROVEN (16/28/19/20, not deterministic) |
| Randomness of 83 keys? | 83-key analysis | uniform random draws, consistent with the generator using a CSPRNG per key |

## Curve-level (secp256k1)
| Finding | Test | Result |
|---|---|---|
| Cofactor? GLV? | EX5 | cofactor 1; j=0 so 3x endomorphism EXISTS but doesn't cut hop cost (adds, not mults) |
| Θ(√W) floor | EX5 | CONFIRMED — no asymptotic kangaroo gain exists; K floor ~0.51 (with all automorphisms) |
| Low-bit x structure | EX1 | x≡9/13 mod 16 forced, but that is a curve artifact with zero reuse against intervals |
| Negation map gains | SOLVER_LAB test_negation | REAL (1.42x) — but a constant factor; already folded into v5 |

## External claims tested
| Claim | Verdict |
|---|---|
| Miller-Venkatesan spectral buckets | Neutral (0.991) on uniform EC x |
| Pollard 2025 spread=6 | Inconclusive/unadopted at toy width (1.195) |
| Parity-split 2x cut | Disproven |
| 16-fold root-of-unity reduction | Curve field facts rule it out: p≡15 (mod 16), n≡13 (mod 16); neither p-1 nor n-1 divisible by 16 |

## Conclusion for the campaign
The effective search space for R2 = the full interval (no reduction possible with
anything discovered). For R1 = the full interval under hash160. **Nothing learned
from 83 solved instances reduces #67 or #140 search work by even one bit.**

## Unresolved hypothesis worth one more cheap probe (if resources appear)
- Multi-seed CSPRNG protocol reconstruction: the earliest keys (#1-#15) were
  hand/coin based; keys #75+ show no pattern. A published generator analysis of
  the puzzle author's tooling (public BitcoinTalk post 2015-01-15) could in
  principle leak the RNG, but our EX2 null-expectation analysis bounds any such
  hope to ≤ null + 3σ — i.e., **nothing actionable**.