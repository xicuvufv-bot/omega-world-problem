# 05 — Experiments

## All Experiments in This Campaign

| ID | Name | Status | Result | Key Finding |
|---|---|---|---|---|
| EX1 | Mod-16 degeneracy | DONE | **NEGATIVE** | QR(16)={0,1,4,9}, candidates={5,9}, buckets uniform 16/16 |
| EX2 | PRNG artifact | DONE | **NEGATIVE** | No strategy exceeds null+3σ, no large-key matches |
| EX3 | Structure battery | DONE | **NEGATIVE** | Hamming KS fails directional replication |
| EX4 | Fused kangaroo | DONE | **POSITIVE** | 2.0x speedup, 36/36 correct, walks identical |
| EX5 | Curve floor | DONE | **CONFIRMED** | Cofactor 1, GLV doesn't help walks, Θ(√W) |
| EXP-N1 | v5 baseline | DONE | **CONFIRMED** | v5 K 4.2-5.0 vs v4 ~5.99 (ratio 0.70-0.84), 36/36 |
| EXP-N2 | GLV×neg quotient (v6) | DONE | **REFUTED** | folded candidates never fire; canonical walk cycles; K-floor 0.51 unreachable |
| EXP-N3 | multi-herd parallel | DONE | **NO GAIN** | serial trail + ~1.6× host ceiling; wall 13.95→12.08s |
| EXP-N4 | infeasibility | DONE | **QUANTIFIED** | #67 ≈ 173 CPU-days + TB RAM trail; #140 ≈ 4e10 core-yr |
| NEW1 | Parity split | PENDING | — | H5: can parity reduce W by 2×? |
| NEW2 | Bit correlation | PENDING | — | H6: high-bit correlation in scalar mult? |
| NEW3 | Multi-target | PENDING | — | H8: shared tame trail across R2 puzzles? |

## Experiment Log

### EX1: Mod-16 Degeneracy (DISPROVEN)

**Hypothesis:** Low 4 bits of secp256k1 points are degenerate (x ≡ 9 or 13 mod 16 → 2 buckets).
**Test:** 5000 random points, walk points at w=8-28, QR(16) analytical computation.
**Result:** QR(16) = {0,1,4,9}, candidate set {5,9}. All buckets give 16/16 distinct at all widths.
**Verdict:** The v4 docstring claim is empirically false. The real fix was the trail/restart redesign.

### EX2: PRNG Artifact (NEGATIVE)

**Hypothesis:** Published keys carry a weak-PRNG fingerprint.
**Test:** 6 strategies × 308 seeds × 83 keys. Compared against null expectation (sum of 1/W_n ≈ 2.0).
**Result:** No strategy exceeds null+3σ. No strategy predicts any key at puzzle n≥40 (W≥2^39, prob ≤ 1e-12).
**Verdict:** Keys are consistent with high-entropy random draws.

### EX3: Structure Battery (NEGATIVE)

**Hypothesis:** Published keys carry exploitable non-random structure.
**Test:** 11 metrics on train (odd-n, 42 keys) and test (even-n, 41 keys). Threshold: p<0.01 in BOTH splits, same direction.
**Result:** Hamming KS p<0.01 in both splits BUT train mean=0.539, test mean=0.493 (opposite directions). No metric replicates.
**Verdict:** Keys consistent with uniform random in their intervals.

### EX4: Fused Kangaroo (VERIFIED 2.0x)

**Hypothesis:** One modular inversion/hop instead of two → ~2x speedup at identical correctness.
**Test:** 4 widths × 3 seeds × 3 key fractions = 36 cases. Walk identity via bucket-sequence comparison.
**Result:** avg 2.00x, median 1.98x, min 1.15x, max 4.00x. 36/36 correct. 4/4 walks identical. Hop delta ≤ 1.
**Verdict:** Genuine constant-factor improvement. Same algorithm, same memory, half the wall time.

### EX5: Curve Floor (CONFIRMED)

**Hypothesis:** secp256k1 has no asymptotic DLP shortcut.
**Test:** Direct computation on curve parameters. Cofactor check (n·G=INF), j-invariant (a=0→j=0), GLV (ω, λ cube roots).
**Result:** Cofactor=1 confirmed. GLV exists but doesn't reduce walk-step cost. Θ(√W) floor stands.
**Verdict:** Any improvement must be constant-factor, not asymptotic.

### EXP-N1: v5 baseline reproduction (CONFIRMED)

**Hypothesis:** v5 (fused single-inversion + even-y W/2 store) reproduces its recorded K advantage over v4.
**Test:** `bench_v6.py` gate, w∈{16,20,24} × 12 seeds; K = (tame_trail+hops)/√W; dual verification.
**Result:** 36/36 correct both solvers. K v4→v5: w20 5.99→4.20, w24 5.94→4.97, w28 5.99→4.43 (ratio 0.70-0.84).
**Verdict:** v5 is the steady best constant (~K 4.2-5.0).

### EXP-N2: GLV order-3 × negation quotient store (REFUTED)

**Hypothesis:** Walk the size-6 automorphism quotient {P,ψP,ψ²P,-P,-ψP,-ψ²P}, store W/6, approach K-floor √(π/12)≈0.51 (11_VERDICT next-step #2).
**Test:** Full candidate (`SOLVER_LAB/candidate/v6_glv_negation.py`): raw walk + 6-class canonical store + exact integer distances + 6/36 candidate grid. GLV constants re-verified computationally. Gate 36/36, then K at w=20/24/28 × 12 seeds.
**Result:** Folded candidates never fire — canonical x-collision requires b ≡ ±λ^i·a (mod n); for small a,b only i=0 (raw equality) is reachable. Instrumented v5: negation candidate fired 0/16 solves. Draft-2 canonical-state (min-x bucket) walk collapses: 13 distinct canonical states in 372 steps at w=16 (disjoint tame/wild components). v6 K: w20 3.84 (vs v5 4.20), w24 16.10 with heavy tail (vs 4.97), w28 4.11 (vs 4.43).
**Verdict:** **REFUTED.** The automorphism quotient gives zero meeting-space reduction for bounded additive kangaroo; K-floor 0.51 is unreachable via this route. v5's 1.42× vs v4 is jump/trail density (v5 ~1.77 trail points/√W vs v4 ~1.25), not negation folding.

### EXP-N3: multi-herd wall scaling (NO GAIN on this box)

**Hypothesis:** One tame trail + N independent wild herds querying the same store scales wall ~1/N.
**Test:** `bench_multiherd.py`, w=28, 12 seeds, workers∈{1,2,4}, first-herd wall, per-worker independent streams, FFI re-verification.
**Result:** mean wall 13.95s (1) / 12.05s (2) / 12.08s (4). Serial trail build (~23.7k steps) dominates the hop phase (~8k), and the host's measured parallel ceiling is only ~1.6× (scan_threaded 239,289 vs 150,495 keys/s).
**Verdict:** No single-machine parallel gain; requires GPU/cluster distinguished-point infra.

### EXP-N4: infeasibility bounds for live targets (QUANTIFIED)

**Test:** v5 constants (K≈4.5, 2,600 steps/s/core, trail ≈ 3.54·2^((w-1)/2) entries) applied to #67 (w=67) and #140 (w=140).
**Result:**
- #67: ~3.9e10 steps ≈ 173 CPU-days/core; trail ~1.7e10 entries (hundreds of GB - 1 TB RAM); brute scan 2^66/239k ≈ 10M years.
- #140: ~3.3e21 steps ≈ 4.1e10 core-years; trail 2.2e21 entries (impossible).
**Verdict:** Both targets remain compute- AND memory-blocked on this hardware.

## Pending Experiments

| ID | Hypothesis | Priority | Expected Outcome |
|---|---|---|---|
| NEW1 | Parity split reduces W by 2× | HIGH | Cheap to test; 2× reduction = significant |
| NEW2 | High-bit correlation | MEDIUM | Low probability but cheap |
| NEW3 | Multi-target tame sharing | LOW | Probably marginal |
