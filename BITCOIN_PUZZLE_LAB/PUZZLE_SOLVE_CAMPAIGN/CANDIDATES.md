# CANDIDATES.md — Found keys / candidate solutions

## Status
**NO CANDIDATES YET.** No search has been committed on any unsolved interval
(this machine cannot; see SEARCH_PLAN.md). Every entry below is a *verified
historical* solution (public record), kept here as the calibration set and as
the exact template for what a valid candidate must look like.

## Real candidates that WOULD count (the chain must close)
A valid solution for #67 requires a scalar k such that:
1. 2^66 ≤ k ≤ 2^67 - 1
2. pub = kG, hash160(pub) == hash160 of `1MVDYgVaSN6iKKEsbzRUAYFrYJadLYZvvZ`

## Verified published solutions used as calibration (from tracker)
| Puzzle | Key (hex) | Address verified |
|---|---|---|
| #66 | 000000000000000000000000000000000000000000000002832ed74f2b5e35ee | 13zb1hQbW... (yes) |
| #110 | 0000...35c0d7234df7deb0f20cf7062444 | 12JzYkkN... (yes) |
| #125 | 0000...1c533b6bb7f0804e09960225e44877ac | 1PXAyUB8... (yes) |
| #130 | 0000...033e7665705359f04f28b88cf897c603c9 | 1Fo65aKq... (yes) |
| #135 | 0000...6d9392a16883f90903d5f78da57af07eb2 | 16RGFo6h... (yes) |

(83/83 corpus re-verified end-to-end earlier; these rows spot-check the ledger.)

## Discipline
- No key is added to this file unless it survives VERIFICATION.md step-for-step.
- "Candidate looks plausible" and "partial hash match" are explicitly NOT
  success per the campaign rules.