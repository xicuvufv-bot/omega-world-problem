# SAFETY.md — research suite guardrails (REQUIRED reading before any run)

## 1. Hard boundaries
- This project generates and solves **synthetic** elliptic-curve DLP instances ONLY.
  There are NO real keys, wallets, addresses, or funds anywhere in the dataset or code.
- "Synthetic" = every coordinate and scalar is produced by this repo's own generator
  (or the toy 2^32 instance in instance.hpp). The solver suite is never pointed at any
  externally supplied public key, puzzle coordinate, or transaction.
- The generator (gen.py / ref/gen_instance.py) chooses G by hashing a private seed and
  rejecting into the subgroup; it does NOT load any real base point.

## 2. Why the exponent study is safe
- The question being answered is purely about *algorithmic scaling*: does log(runtime)
  vs log(interval) have slope ≈0.5 (the generic lower bound) or better for some approach?
- A positive A-class result (α<0.50 measured) at these tiny sizes is a *measurement*, not
  a threat: the Nechaev/Shoup lower bound still holds for any concrete algorithm at
  real-world scale; if a candidate ever appeared to beat √N, SAFETY requires us to treat
  it as an artifact (variance, lucky orbit, incomplete DP, or wrong amortization) until
  replicated independently, not as a break.

## 3. What this suite is NOT
- NOT an ECDLP solver for any real curve. l in the python suite is chosen FAR below
  2^256 (order ~2^56..2^64 max) so that any method here is ∈ toy/benchmark scale even if
  "cuda-optimized". Do not raise l to cryptographic size; do not point solvers at a real
  curve's G or Q.
- NOT a "quantum algorithm" deliverable. The Grover emulation is a classical-
  arithmetic toy for db ≤ 12 ONLY; it demonstrates oracle COUNTING, not quantum speedup,
  and makes NO complexity claim. Label any such output "EMULATION, NO CLAIM".

## 4. Operational rules
- Do not add dependencies that import real-curve key material (no secp256k1 libs pointed
  at real base points). Using e.g. `ecdsa` to *verify* synthetic scalars cross-check is
  permitted but the generator never hands it a real key.
- If a run produces a k whose verification by scalar-mult fails, the row is INVALIDATED,
  never imputed.
- CSV rows always carry `verified=1/0`; only verified rows feed the fit.
- Report α with 90% CI and R²; classify A/B/C/D strictly per spec, and preface the whole
  final writeup with these boundaries.

## 5. If in doubt
Any change that could touch a real puzzle, real key space, or exceed the toy scale must be
stopped and flagged. Small toy/benchmark DLP research of this shape is standard and
benign; the danger is only in scope creep toward real instances. This repo is scoped to
synthetic instances from start to finish.