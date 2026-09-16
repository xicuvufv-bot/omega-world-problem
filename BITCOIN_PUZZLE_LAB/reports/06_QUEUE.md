# 06 — Attack queue (ranked, with method)

Queue is **one active target at a time**, re-ranked after every measurement.
Order = estimated **single-GPU years** (ascending), from
`dataset/puzzles_meta.csv`.

## Verdict shape

Every entry is **LOCAL_INFEASIBLE** — this queue is the *method + awareness*
artifact, not a runnable schedule. Production-scale compute is out of scope.

| order | # | regime | est. GPU-yr | method |
|---|---|---|---|---|
| 1 | 140 | R2 | 7.0e3 | interval DLP (kangaroo) on exposed pubkey |
| 2 | 71 | R1 | 1.5e4 | hash scan (SHA256+RIPEMD160, batched GPU) |
| 3 | 72 | R1 | 3.0e4 | hash scan |
| 4 | 145 | R2 | 5.6e4 | interval DLP on exposed pubkey |
| 5 | 73 | R1 | 6.0e4 | hash scan |
| 6 | 74 | R1 | 1.2e5 | hash scan |
| 7 | 150 | R2 | 2.2e5 | interval DLP on exposed pubkey |
| 8 | 76 | R1 | 4.8e5 | hash scan |
| 9 | 77 | R1 | 9.6e5 | hash scan |
| 10 | 155 | R2 | 1.8e6 | interval DLP on exposed pubkey |
| 11 | 78 | R1 | 1.9e6 | hash scan |
| 12 | 79 | R1 | 3.8e6 | hash scan |
| … | … | … | … | … |
| 13 | 160 | R2 | 7.2e6 | interval DLP on exposed pubkey |

## Why #140 leads

- R2 (public key exposed) → √W interval DLP instead of W hash scanning.
- Smallest `n` of any R2 (#140..160 step 5) → smallest √W of the five
  exposed keys.
- Comparison: #140 ≈ **7.0e3** GPU-years ≈ 28× cheaper than the *cheapest*
  R1 (#71 ~1.5e4 … no: #71 is 2× #140) — the regime advantage made concrete.

## Non-negotiable rule: R2 keys are never approximated

For an R2 puzzle the public key is known, so:

- the "overlap/approximation trick" (guessing k modulo a public partial
  winning-range) is unnecessary and inexact — it also requires a *target
  pubkey* anyway, so it only applies *to* R2;
- we use the *exact* interval DLP; `k` is recovered from the collision, not
  estimated.

This is why R2 solvers (`v3`/`v4`) verify **k exactly**, and the ladder in
`05_BENCHMARKS.md` asserts agreement on the recovered key.

## Provider planning (conjecture only)

- R1 scan: packed SHA256+RIPEMD160, GPU, fed by stride point-add; the
  bitmask prefilter makes the actual hash rate the boundary (this is the
  architecture of public miners).
- R2: kangaroo is inherently parallel — partition the interval, each worker
  keeps its own tame/wild trail; BSGS stays the local oracle for
  verification-scale targets.