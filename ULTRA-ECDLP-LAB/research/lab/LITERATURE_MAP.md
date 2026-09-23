# LITERATURE_MAP.md — what the literature says about ECDLP scaling (v3 mission)

Scope-note: everything here is *known theory*; it constrains what any synthetic toy can
show. Nothing below is original. Claims marked **[verified in-lab]** are the ones the
autonomous loop has reproduced on the toy family.

## 1. Generic lower bounds (the wall)

- **Shoup (1997), "Lower bounds for discrete logarithms and related problems"** — generic
  group model (black-box group ops): deterministic DLP needs Ω(√l), randomized needs
  Ω(√l) for prime-order groups. [baseline bsgs α=0.4974 R²=1.0 **verified in-lab**]
- **Nechaev (1994)** — same Ω(√p) bound for generic algorithms (earlier, weaker form).
- **de Castro, Shokrollahi, Sudan (2022)** — preprocessing DLP: with S bits of
  preprocessing and T queries the single-target work is Ω(min(N^(1/2), N/T)) etc.; the
  generic preprocessed bound keeps single-target at ~√N. Multi-target amortizes.
  [E2 bulk shared-G **verified in-lab** as constant gain only]
- Consequence for the mission: **any reproducible α<0.5 measured on prime-order toy
  instances is, a priori, either (a) an artifact of the metric/x-axis, or (b) a genuine
  non-generic structural shortcut — the latter would be extraordinary. The lab's default
  prior is (a), and CLASS-4 requires independent reproduction to override it.**

## 2. Non-generic algebraic attacks and why each fails on THIS family

| Attack | Condition needed | This family | In-lab status |
|---|---|---|---|
| Pohlig-Hellman | composite group order | l prime | REFUTED (prime order) |
| Smart / Semaev (anomalous) | #E = p exactly | #E=l, l≠p | REFUTED (non-anomalous) |
| MOV / Frey-Rück | small embedding degree k | k>1999 scan | REFUTED (verified) |
| XEDNI / decomposition | small-ish k, polynomial relation | k huge | REFUTED |
| Index calculus on E(F_p) | p smooth / extension structure | p~2^24..32 | known super-exp; not pursued |
| Weil/Teichmüller descent | special curves | j=0 but prime field | not applicable |
| GHS Weil descent | high-genus Jacobian rep | p prime, no small ext | not applicable |

## 3. Endomorphisms / fast arithmetic (constants only)

- **Gallant-Lambert-Vanstone GLV (2001)** — split k into k1+k2λ with |k1|,|k2|~√l/√2 using
  an endomorphism of norm-one; 2D-grid search gives ~constant √2 win. For interval DLP
  (k<2^db<<l) the reduction does NOT localize k (k2≡0 for tiny intervals) [E1 **verified**].
- **CM method / complex multiplication (Atkin-Morain)** — inverse direction (build curve
  from D); the toy has D=-3·2419² (conductor 2419 in Q(√-3)), rank-2 endom ring.
  [D=-3·2419² **verified in-lab**]
- **Extended-GLV / De Weger, GLV-with-more (Gaudry-Hess-Smart 2002)** — higher extension
  degrees give multi-dim decompositions; requires extension-field curves + pairing
  eigen-decomposition; inapplicable over F_p prime field with rank-2 ring.

## 4. Random-walk / collision methods (state of the art)

- **Pollard ρ (1978)**, **Pollard kangaroo (1978)** for intervals; **van Oorschot-Wiener
  (1999)** parallel collision search, DP tables — textbook √N with tunable memory.
- **Galbraith, Pollard, Ruprai (2010)** — kangaroo variants: 3-kangaroo, linear combos
  for small intervals; constants only.
- **Montgomery/Edwards models** — arithmetic speed (constants); open-source world uses
  them to multiply ops/sec, never exponent.
- Consequence: **tuning walk parameters (K/b/wcc, partitions, restart count) moves
  constants; measured in-lab: kanga α wanders 0.39-0.75, R² 0.68-0.82 → artifact,
  no stable slope.** [**verified in-lab**]

## 5. Multi-target / batching (the ONLY verified lever)

- Multi-target DLP (BBKT-style, Kuhn-Struik): K targets share base G; amortized cost can
  drop toward √(N/K) for the FIRST of K (Oorschot-Wiener) or keep per-target constant
  with a shared precomputed table (BSGS).
- **In-lab: E2 shared-G BSGS = 2.6–4.3× constant (CLASS-2); independent reproduction
  α_bulk=0.5539 amortized (still ≈generic).** This is an ENGINEERING constant, exactly what
  the literature predicts; sub-sqrt for a single target remains unverified.
- **Untested-but-predicted in-lab: shared-DP multi-target rho/kanga first-hit ~√(N/K)**
  (negative α vs K) — a NEW hypothesis (Q family, ID H investigated next).

## 6. Hadamard: what the field knows beats the wall

- **Attack class that ACTUALLY beats √l on real systems**: (1) small composites (PH),
  (2) anomalous (Smart), (3) low embedding (MOV), (4) x-largest-prime-factor smoothness.
  All require the group order / field to be special. On a *random prime-order* E(F_p) these
  conditions hold with negligible probability over the random-curve ensemble.
- The toy family y^2=x^3+7,p≈2^32,l prime is **generic in the sense of Shoup** (no attack
  class applies) — consistent with α≈0.5 measured everywhere.

## 7. Under-tested corners (open in the literature for THIS small range)

- Semaev summation-polynomial relation search **empirically** at db=12..20 (theory says
  super-exp; a concrete small-relation search is cheap and would falsify/confirm). Planned.
- Interplay of near-max-trace (t/2√p≈0.9995) with CM conductor structure: literature has
  no shortcut; the slab is where KL-direct methods get hard, not easy. Open: any hidden
  structure at t→2√p that HS/BSGS misses? No known result — cheap to probe (in lab next).
- Batch-preprocessed DLP at K=2,4,8 baby-Table reuse: theory bound is O(√N) per target
  after one √N build — in-lab E2 confirms the constant; asymptotic per-target for K→∞ is
  open at this toy scale (Q family).

## 8. Honest closure

The active literature contains **no class of attack that beats √N on a random prime-order
interval DLP**. This lab's job is to (a) re-validate, (b) hunt for a non-generic family
leak that theory missed, (c) **disprove or confirm** each new hypothesis with the ok-gate
and independent reproduction. No previous autonomous round found one; the baseline is
stable at α≈0.497.