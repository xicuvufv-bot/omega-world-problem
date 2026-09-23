# FAILED HYPOTHESES — tried and (honestly) killed

Every entry: claim → experiment → why it failed. None of these is "proven impossible in
general"; each is disproven/neutered *for this synthetic interval-DLP family* with the
experiments listed.

## GLV endomorphism → sub-sqrt
- CLAIM: the validated order-3 endomorphism (x,y)→(ωx,y), λ=4021414523, lets us split
  k = k1 + k2·λ and search a 2D grid smaller than √N.
- EXPERIMENT: compute ω, λ, lattice-reduce, decompose k on 500/500 random k; attempt
  grid search on db=10..18 rows; ok-gate every candidate.
- WHY IT FAILED: for the bench's *interval* DLP (k < 2^db ≪ l) the decomposition is
  trivial: (k1 = k, k2 = 0). The 2D lattice degree of freedom only exists in the
  full-range (k ~ l) regime. Even there GLV gives ≤ √2 constant, CLASS-3 not CLASS-4/5.
- RESULT: REFUTED for interval rows. Documented in COUNTEREXAMPLES.md.

## Pohlig-Hellman on the prime rows
- CLAIM: factor l and descend subgroups.
- EXPERIMENT: random-point order test `l*P == O`; factor l.
- WHY IT FAILED: l is prime, cofactor = 1, #E = l. No subgroup tower exists.
- RESULT: REFUTED.

## MOV / XEDNI / index-calculus transfer
- CLAIM: embed the group into a multiplicative group / use summation polynomials.
- EXPERIMENT: scan k ≤ 1999 for `l | p^k - 1`.
- WHY IT FAILED: embedding degree > 1999 (none found) → no finite-field transfer, no
  index calculus leverage on prime-order EC over a prime field.
- RESULT: REFUTED.

## Anomalous / near-anomalous Smart-SEMAEV shortcut
- CLAIM: t ≈ 2√p (near-max trace) enables a p-adic log attack.
- EXPERIMENT: verify #E vs p.
- WHY IT FAILED: Smart/Semaev need #E = p exactly; here #E = l ≠ p. Verified again.
- RESULT: REFUTED.

## rho maskbits / PIR restarts
- CLAIM: richer partition or more restarts ≤ better α.
- EXPERIMENT: maskbits ∈ {8,12,14}, R ∈ {1,4}, db=16; steps logged.
- WHY IT FAILED: steps grow with maskbits (rarer DP); PIR does not move α. α stays 0.5.
- RESULT: CONSTANT (α=0.5), not sub-sqrt.

## kangaroo W/b/K tuning
- CLAIM: bigger W or richer jump table beats √N.
- EXPERIMENT: W∈{16,32,64,128}, b∈{6,8}, K∈{16,32,64}, db=12..16.
- WHY IT FAILED: fits are unstable (R² 0.68–0.82), α wanders 0.40–0.75 depending on the
  dial, and the walk crashes on Z≡0 for many seeds (previously 13/15). No dial produced
  a stable α < 0.5. Regarded as parameter artifacts, not structure.
- RESULT: CLASS-0/1 (artifact-prone), ceased.