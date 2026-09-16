# Experiments Log

## EX1: Mod-16 Degeneracy Test

**File:** `scripts/ex1_x16_degeneracy.py`
**Status:** Completed. Honest negative.

**Setup:** 5000 random secp256k1 affine points. Measured low 4 bits (hash &
  x-coordinate), low 8 bits, bits 120–123, walk points (w=8–28). Quadratic
  residues mod 16 computed analytically.

**Results:**
- QR(16) = {0, 1, 4, 9} — NOT {9, 13} as previously claimed.
- Candidate x where x³+7 ∈ QR16: {5, 9} — only 2 buckets, not the claimed
  "x≡9 or 13 mod 16" pattern.
- Empirical: 5000 points → low nibble uniform (expect ~312/bin, max dev 45).
- Walk points: low nibbles 16/16 distinct, bits 120–123 also 16/16.
- Audit across all widths w=8,12,16,20,24,28: all give 16/16 distinct.

**Conclusion:** The documented rationale for the bucket fix in v4 is
empirically false. The real fix for the old 20-bit timeout was the
trail/restart redesign, not bucket choice.

---

## EX2: PRNG Artifact Test (v2 with Null Expectation)

**File:** `scripts/ex2_prng_test.py`
**Status:** Completed. Honest negative.

**Setup:** 6 generator strategies × 308 seeds × 83 solved keys. Compared
total exact matches against null expectation (sum of 1/W_n ≈ 2.0 matches
per seed). Also measured matches at large intervals (n≥40: W≥2³⁹, random
match probability ≤ 1e-12).

**Results:**
| Strategy | Total matches | Null+3σ (1923) | Matches n≥40 | Best run |
|---|---|---|---|---|
| getrandbits(seed) | 296 | 1923 | 0 | 3 |
| randint(seed) | 606 | 1923 | 0 | 3 |
| randint(seed=n) | 308 | 1923 | 0 | 1 |
| xorshift32(seed) | 604 | 1923 | 0 | 5 |
| LCG(seed*n) | 585 | 1923 | 0 | 1 |
| sha256(seed,n) | 602 | 1923 | 0 | 4 |

**Conclusion:** No strategy exceeds null expectation by 3σ. No strategy
predicts any key at puzzle n≥40 (W≥2³⁹). The 83 keys are consistent
with high-entropy random draws.

---

## EX3: Structure Battery (Train/Test Split)

**File:** `scripts/ex3_structure_battery.py`
**Status:** Completed. Honest negative.

**Setup:** 83 solved keys. Train = odd-n (42 keys), test = even-n (41 keys).
11 statistical metrics: relative position, low-8/4 bits, hamming weight,
leading-ones, parity, mod-3, consecutive pair correlation, reward
correlation, depth, Benford. Anomaly threshold: p<0.01 in BOTH splits
AND same direction.

**Results:**
| Metric | Train (42) | Test (41) | Replicated? |
|---|---|---|---|
| Rel. position KS | 0.080 (p>0.01) | 0.093 (p>0.01) | No |
| Low-8 χ² | 250.6 (p>0.05) | 252.5 (p>0.05) | No |
| Low-4 χ² | 11.3 (p>0.05) | 19.5 (p>0.05) | No |
| Hamming KS | 0.339 (p<0.01) | 0.308 (p<0.01) | **Opposite direction** |
| Leading-ones χ² | 1.68 | 2.36 | No |
| Parity | 21/21 | 23/18 | No |
| Mod-3 | [12,19,11] | [15,16,10] | No |
| Consec pair r | 0.007 (p>0.05) | -0.169 (p>0.05) | No |
| Reward r | 0.011 (p>0.05) | 0.061 (p>0.05) | No |
| Depth KS | 0.080 (p>0.01) | 0.093 (p>0.01) | No |
| Benford χ² | 40.3 (p<0.01) | 6.2 (p>0.05) | No |

**Conclusion:** Hamming KS shows p<0.01 in both splits but train mean=0.539
(above 0.5) and test mean=0.493 (below 0.5) — opposite directions, so
the effect does NOT replicate. No metric passes the dual-split threshold.

---

## EX4: Fused Single-Inversion Kangaroo Benchmark

**File:** `scripts/ex4_fused_benchmark.py`
**Status:** Completed. VERIFIED constant-factor improvement.

**Setup:** Baseline (2 inversions/hop) vs Fused (1 inversion/hop, affine
returned from _step for reuse). 4 widths × 3 seeds × 3 key fractions
= 36 cases. Same key, same seed, same jump table. Walk identity verified
by bucket-sequence comparison. Correctness verified by key recovery.

**Results:**
| Width | Cases | Avg speedup | Median | Min | Max | Keys OK | Walk OK | Hop delta ≤1 |
|---|---|---|---|---|---|---|---|---|
| w=16 | 9 | 2.23x | 2.07x | 1.15x | 4.00x | ✓ | ✓ | ✓ |
| w=20 | 9 | 1.92x | 1.81x | 1.21x | 2.58x | ✓ | ✓ | ✓ |
| w=24 | 9 | 1.99x | 1.99x | 1.93x | 2.12x | ✓ | ✓ | ✓ |
| w=28 | 9 | 1.84x | 1.75x | 1.20x | 2.65x | ✓ | ✓ | ✓ |
| **ALL** | **36** | **2.00x** | **1.98x** | **1.15x** | **4.00x** | **✓** | **✓** | **✓** |

Per-hop ms (w=28): baseline 8.97 ms → fused 4.96 ms (1.81x).

**Conclusion:** The fused variant recovers the same key in all 36 cases,
produces identical walk paths (same bucket sequences), differs by at most
1 hop (endpoint detection-timing shift), and achieves a measured 2.0x
speedup. This is a genuine constant-factor improvement with zero
algorithmic change — same memory, same asymptotic complexity, same
correctness.

---

## EX5: Curve Floor (Cofactor, GLV, Asymptotic)

**File:** `scripts/ex5_curve_floor.py`
**Status:** Completed. Hard floor verified.

**Setup:** Computed directly on secp256k1 parameters. Verified cofactor
h=1 (n·G=INF, 7 small multiples ≠ INF). Found j-invariant = 0 (a=0,
b=7). Found cube root of unity ω in F_p (ω²+ω+1 ≡ 0 mod p). Found
GLV endomorphism parameter λ in F_n (λ²+λ+1 ≡ 0 mod n).

**Results:**
- Cofactor h = 1: E(F_p) ≅ Z_n (cyclic, prime order, no subgroups).
- j = 0: secp256k1 has CM by Z[ω], ω = e^(2πi/3).
- GLV decomposition exists: k = k1 + k2·λ (each ~128 bits).
- GLV speeds fixed-base scalar-mult by ~30–50% (used in Bitcoin Core).
- GLV does NOT reduce walk-step cost in kangaroo (point-add O(1)).
- No Pohlig-Hellman, no small-subgroup, no torsion-based reduction.

**Conclusion:** The asymptotic floor for interval DLP on secp256k1 is
Θ(√W) group operations. Any improvement must be a constant-factor win.
