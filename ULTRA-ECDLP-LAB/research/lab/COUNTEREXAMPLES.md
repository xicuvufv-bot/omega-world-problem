# COUNTEREXAMPLES — concrete instances where a "promising" idea demonstrably does not work

## GLV decomposition is trivial on interval-DLP rows
Take the actual db=16 row (k = 457): lattice decomposition through λ gives
(k1, k2) = (-13024, 2419). The pair is NOT both small in √N = 256; it is sized √l ≈ 2^16.
Consequently a GLV 2D grid search of span √N cannot express the row's k; searching span √l
is strictly worse than plain BSGS (which needs √N). So "apply the validated endomorphism
to the interval DLP" is a concrete counterexample-backed NO.
Measured: db=16 GLV-grid required M=2^15-ish steps and STILL missed 457 (k2 became large);
plain BSGS found it in 457 steps. Evidence rows E1.GLV-decomp in RESULTS_STRUCTURAL.csv.

## Anomalous shortcut counterexample
Smart's attack needs #E = p. Here #E = l = p - 131004. Verified: random points satisfy
l·P = O, not p·P = O. A p-adic descent has nothing to act on. Counterexample family:
the lab's own near-max-trace primes.

## MOV counterexample
Scan k = 1..1999: no k with l | p^k - 1. Even 64-bit hint: no embedding ≤ 1999. A transfer
attack would need k small; the minimal k exceeds 1999. Counterexample: the actual (p, l)
pair of this lab.

## rho restarts counterexample
PIR with R=4 on db=16 took MORE total steps than R=1 (1.0M to 1.8M depending on mask);
min-of-restarts never beat a single walk's distribution tail. Counterexample rows
E3.rho-mb*-R* in RESULTS_STRUCTURAL.csv.