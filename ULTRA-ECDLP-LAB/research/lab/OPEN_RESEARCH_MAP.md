# OPEN_RESEARCH_MAP.md — the frontier: where a sub-sqrt shortcut could (in principle) hide

Honest map of the *only* open doors worth probing, ranked by (strangeness × cheapness to
test). Each door below is either falsifiable this session or explicitly pushed to the
scheduler. Default prior = artifact; CLASS-4 gate = evidence.

## The contradiction to resolve

bsgs we trust: α=0.4974, R²=1.0, 7 genuinely-different orders, independent k, all ok.
Generic lower bound says you need a NON-GENERIC property of the family to beat it. The
family's verified properties (CM by Q(√-3), conductor 2419, near-max trace, l prime,
cofactor 1, k>1999) have NO literature shortcut. So the search universe is:
   (1) a property of the FAMILY that no attack class has exploited, OR
   (2) a metric/benchmark artifact (x-axis, seed, verification, table reuse).

## Open probes, numbered (PN = probe number)

### PN-1  [NEW, this session] Shared-DP multi-target rho/kanga: first-hit ~ √(N/K)?
- Claim (literature-consistent but NOT yet measured in-lab): Oorschot-Wiener shared DP
  table across K targets finds ANY of the K keys in ~√(N/K) group ops → α_vs_K < 0.
- Why it matters: confirms the ONLY known multi-target lever; measures K-scaling honestly.
- Falsification: if first-hit does NOT shrink as 1/√K, the shared-DP mechanism is broken
  in this implementation → REFUTED.
- Cost: cheap (db=16..24, K=1..16). Status: HYPOTHESIZED (family Q).

### PN-2  [NEW] Near-max-trace slab (t/2√p ≈ 0.9995): does the fundamental domain of the
       CM order degenerate?
- The CM discriminant D=-3·2419² has an unusually large square part 2419 when t≈2√p.
- Query: does the principal-cycle / ideal-class structure of the conductor-2419 order
  degenerate near the max-trace boundary in a way that leaks k through the φ-eigenpairs?
- Literature: unknown, no attack known. Probe: compute the order's fundamental domain and
  the φ-eigenpair alignment of small-k multiples at db=16..22; look for a lattice width
  collapse. Cost: cheap. Status: HYPOTHESIZED (family A/C).

### PN-3  [NEW] x-only shared hash amortization at K→∞ (baby-table reuse asymptotics)
- E2 showed constant 2.6-4.3×; asymptotic per-target behavior at K=64..512 is unmeasured.
- Probe: measure per-target amortized steps; check it does NOT dip below √N (which would
  violate de Castro et al. and be a CLASS-4 trigger). Status: HYPOTHESIZED (family Q/K).

### PN-4  [NEW] Semaev summation-polynomial relation search, degree 2-3, db=12..20
- Theory: super-exponential; the toy range is small enough to run a concrete relation
  search to CONFIRM the theory curve (negative control).
- Status: HYPOTHESIZED (family R), expected REFUTED-class (CONSTANT) — it's a control.

### PN-5  [deferred] GPU/T4 depth (kaggle_t4.py): wall-time constant on T4, not exponent.
- Needs a Kaggle T4 (not present locally). Payload ready; scheduler will queue it.
- Status: UNTESTABLE_YET (family B/T).

### PN-6  [deferred] Scheduler: KAGGLE_RUNNER with checkpoint/merge/resume.
- Implementation task, not a math probe. Builds the autonomous long-run loop.

## What is CLOSED (do not re-open without new evidence)

- GLV-as-sub-sqrt FOR THE INTERVAL: closed by E1 (k2 not localized; grid failed; theory).
- MOV/XEDNI, Smart/anomalous, PH: closed by verified algebraic properties.
- rho partition / maskbits / PIR restarts: closed by E3 (α unchanged).
- kanga W/K/b/wcc tuning: closed by E4 (α wobbles, R²<0.85; artifact).
- Grover as classical shortcut: closed (EMULATION, NO CLAIM).
- Cofactor-based subgroup tricks: closed (cofactor=1).

## Priority today

1. PN-1 (cheap, theory-aligned, family Q) — run now.
2. PN-4 (cheap negative control) — run after PN-1.
3. PN-2 (pure math, cheap) — run if budget allows.
4. PN-3 (asymptotic) — extend E2 if budget allows; else mark deferred.
5. PN-5/PN-6 — scheduler, no local GPU.

Every probe writes rows to lab/ GOLDEN_BASELINE-family CSVs with verified=1 and the ok
gate; any α<0.45 stable across ≥5 sizes goes to CLASS-4 review (independent reproduction
mandatory before any public claim).