# AUTONOMOUS RESEARCH REPORT — ECDLP toy lab (prime-order, j=0 curve)

Date: 2026-09-23
Scope: synthetic only. NO real Puzzle #71, NO real keys. Every recovered k was re-verified
by independent scalar multiplication (the ok gate: `Q == k*G`).

---

## 1. WHAT WE KNOW (confirmed, reproducible)

- Instance family: `y^2 = x^3 + 7` over `F_p`, p = 4294966177 (2^32 - 1119).
- Group order of the base point **l = 4294835173 is PRIME and the full curve order is
  exactly #E = l** (cofactor = 1). Verified by random-point order test: `l * P == O` for
  multiple random curve points. Consequence: **Pollard-Pohlig-Hellman is inapplicable to
  these rows** — there is no composite subgroup tower to descend.
- Trace `t = p + 1 - l = 131005 ≈ 2·sqrt(p) = 131070`. The curve sits on the **max-trace
  boundary** (t/2√p ≈ 0.9995), i.e. the "near-anomalous" edge the generator named. This
  does NOT make the DLP easy: Smart's/Semaev's attacks need #E = p exactly (anomalous),
  which is false here.
- Endomorphism ring: `j=0` curve with `p ≡ 1 (mod 3)`, so there IS a cube-root-of-unity
  automorphism `(x,y) → (ωx, y)`. We computed `ω`, its image `φ(G)`, the GLV scalar
  `λ = 4021414523` (root of x²+x+1 mod l) and **validated `φ(G) = λ·G` exactly**, plus
  lattice decomposition `k = k1 + k2·λ mod l` on 500/500 random k.
- **MOV / XEDNI transfer is impossible here**: embedding degree `k` with `l | p^k - 1`
  exceeds 1999 (scanned k = 1..1999). Coupled with prime order, no index-calculus or
  pair-based transfer to a finite field is available.
- Baseline scale law (regression over db=10..18, output rows `l·G→O` verified):
  **bsgs α = 0.494, R² = 0.9997** — the classic √N bound, extremely tight.
  Single-seed reproduction today gave single-target bsgs α = 0.492, R² = 0.989.
- The three engine families (bsgs / rho / kanga) all land at α ≈ 0.5 vs the interval N.
  Nothing in the whole lab has shown α < 0.5 with high R² on genuinely varied orders.

## 2. WHAT WE DO NOT KNOW

- Whether ANY non-generic structure exists in this exact near-max-trace j=0 family that
  could beat √N. All structural probes below came back at or above 0.5, but the search
  space of "hidden" algebra (higher rank units, subring degenerations, GF(2) twists) is
  not exhausted to a mathematical proof — only to a strong negative data corpus.
- Whether a GPU/T4×2 campaign changes the *constant* (but not the exponent) for
  multi-target amortization scale-ups. Local CPU data supports a ~3x constant, which we
  attribute to shared-base amortization, not to sub-sqrt behavior.

## 3. EXPERIMENTS RUN TODAY (structural probes, all synthetic, all ok-gated)

| probe | meaning | α | R² | verdict |
|---|---|---|---|---|
| E1.bsgs | plain interval bsgs (fallback comparator) | 0.568* | 0.992 | √N (single seed, small db) |
| E1.GLV | GLV lattice decomposition of k | k2 ≡ 0 | — | **structural fact: GLV trivializes for interval DLP** |
| E2.bulk | shared-G multi-target BSGS (5 targets) | 0.462 | 0.914 | constant win ~3x, α stays ~0.5 |
| E4.kanga W16 | kangaroo W=16 | 0.448 | 0.811 | unstable, CLASS-0/1 |
| E4.kanga W32 | kangaroo W=32 | 0.395 | 0.817 | unstable, CLASS-0/1 |
| E4.kanga W64 | kangaroo W=64 | 0.752 | 0.686 | high-variance, CLASS-0 |
| E4.kanga W128 | kangaroo W=128 | 0.555 | 0.707 | high-variance, CLASS-0/1 |

\* E1 α>0.5 is a small-N artefact (tiny interval, single seed); the multi-seed mean is
α = 0.494 (R² = 0.9997) from the earlier genuinely-varied-order scaling run. The kanga
α values are dominated by the known (previously reported) jump-table defect — the walk
can hit Z ≡ 0 and crash 13/15 seeds; surviving parameter sets are not evidence of anything.

## 4. WHAT FAILED (honest)

- **GLV endomorphism → sub-sqrt.** Disproven *for this interval DLP*: decomposing the
  small scalar k (< 2^db ≪ l) through the λ-lattice returns (k1 = k, k2 = 0). The 2D
  lattice help only applies to full-range DLP, not to the bench's interval problem.
  Even in the full-range setting GLV gives only a √2 constant — CLASS-3 at best, and
  it does not even engage here. → HYPOTHESES H-REFUTED.
- **Pohlig-Hellman.** Inapplicable: cofactor = 1, l prime. → REFUTED for prime rows.
- **MOV/XEDNI/Index calculus.** Inapplicable: embedding degree > 1999. → REFUTED.
- **Anomalous/Smart family shortcut.** Inapplicable: #E = l ≠ p. → REFUTED.
- **rho maskbits (8,12,14) / PIR R∈{1,4}.** Steps grow with maskbits; restarts do not
  move α. → CONSTANT (α = 0.5), no sub-sqrt.
- **kangaroo parameter tuning (W,b,K).** Delivered instability and crashes, no α swing
  below 0.5 with stable fit. → CLASS-0 (artifact-prone), not an idea to keep.

## 5. WHAT SURVIVED (only one, and it is a constant, not a breakthrough)

- **E2 — shared-base multi-target BSGS.** Because every lab row reuses the SAME base
  point G and SAME curve, one baby table (size m ≈ √N) is built once and reused across
  K targets; each subsequent target needs only giant steps. Measured: bulk per-target
  ≈ 2.5-4x fewer steps than K independent BSGS runs, per-target α ≈ 0.5 (amortized
  constant win). Independent reproduction today (different seed, db=10..20, K=6)
  confirmed: bulk amortized α = 0.554, R² = 0.98 (includes the once-only build), every
  key ok-verified. → **CLASS-2 (engineering/amortization), NOT CLASS-4/5.**
  No claim of sub-square-root anywhere.

## 6. WHAT IS ONLY ENGINEERING

- Shared-G baby-table memoization (E2) — real, safe, useful for the lab's batch nature,
  constant factor only.
- rho DP mask / PIR restarts / kangaroo W-b-K tuning — engineering dials, α unchanged.
- The earlier bsgs α=0.494 measurement itself (fine, correct, generic √N).

## 7. WHAT IS MATHEMATICALLY INTERESTING (non-claims)

- The toy family sits at the **max-trace / near-anomalous boundary** (t ≈ 2√p). Such
  curves are j=0, triply covered, with a full CM endomorphism ring. It is worth keeping
  note that this boundary slab (t within ~70 of 2√p) is the SAME region where the
  endomorphism ring degenerates (trace = 2√p would be supersingular). We verified the
  curve is ordinary here, but this exact family occupies an unusual, thinly-studied band.
- GLV lattice structure is real and validated (500/500) — but provably useless for the
  bench's *interval* formulation. Documented as a counterexample to "any endomorphism
  helps".

## 8. BEST MEASURED ALPHA / BEST VERIFIED SPEEDUP

- Best measured α: **0.494 (bsgs, R²=0.9997)** — generic √N. No measurement anywhere
  in the lab gives a stable α < 0.5 on genuinely varied orders.
- Best verified speedup: **~3x (shared-base batch amortization)**, CLASS-2, constant.
- Strongest surviving hypothesis: **E2 shared-base amortization** (engineering), plus the
  open note that the near-max-trace family is under-explored (see NEXT_RESEARCH_PLAN.md).

## 9. FINAL HONEST POSITION

We did NOT find a sub-square-root algorithm. Every structural probe (GLV, cofactor,
MOV, anomalous, endomorphism, rho/kanga tuning) landed at α ≈ 0.5 or failed outright,
consistent with the generic-model lower bound. The only surviving win is a constant-factor
shared-base amortization (~3x), fully ok-verified, and it is CLASS-2 engineering, not a
mathematical breakthrough. Any claim that "Puzzle #71 / real keys are solvable faster"
would be FALSE and is explicitly NOT made here.