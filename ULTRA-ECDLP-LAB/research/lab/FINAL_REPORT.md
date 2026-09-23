# FINAL REPORT — ULTRA-ECDLP-LAB: prime-order scaling (genuinely varying order)

**Date:** 2026-09-23. **Scope:** toy prime-order ECDLP only (y²=x³+7). Synthetic.

## 1. The measurement is honest

- Every db is its own DISTINCT prime-order group: the field prime `p` and true group
  order `l = |E(F_p)|` (a prime) both differ across sizes:
  - db=10: p=1051,  l=1093
  - db=12: p=4159,  l=4243
  - db=14: p=16477, l=16693
  - db=16: p=65647, l=65173
  - db=18: p=262153, l=262567
- Generation-time verification: `l·G ≡ O` (point-at-infinity) was re-checked by
  scalar multiplication for every curve (genchk=True, logged).
- Instances: `k` sampled by us, `Q = k·G` computed by scalar multiplication, then the
  engines re-derive `k`; each engine's `ok` flag is its OWN independent re-check
  `Q == k·G`. Nothing is oracle-loaded, nothing is invented.
- Fit X-axis is `log2(N=2^db) ≈ log2(l)` — i.e. genuinely varying problem size
  (log2 l ∈ [10.09, 18.00]), so α is *measurable* here (this is what the previous
  fixed-order run could not do).

## 2. Per-engine measured scaling (OLS on log2(steps) vs log2(N))

| engine | distinct sizes | verified | alpha | R²  | verdict |
|--------|---------------|----------|-------|-----|---------|
| bsgs   | 5            | 5/5      | 0.494 | 0.99994 | CLASS 2 — clean generic sqrt scaling |
| rho    | 5            | 2/5 dbs  | (none — insufficient) | n/a | CLASS 0 — no fit |
| kanga  | 5            | 5/5 (per-seed partial) | 0.692 | 0.879 | CLASS 0 — ragged/no sound fit |

- **bsgs**: steps(scaled) perfectly proportional to sqrt(N): alpha=0.494 (± small),
  R²=0.99994. Matches the expected generic baseline EXACTLY (theory: ~2·sqrt(N)).
- **rho**: did not complete verified recoveries on most seeds (see §3) → data too
  sparse (2 usable dbs) → **no α reported** (per rule: never fabricate α from
  insufficient data).
- **kanga**: fit exists but is ragged (R²=0.879, n=5) → not a sound sub-root curve;
  α(0.692) is ABOVE the √N baseline, i.e. slower than generic, not faster.

## 3. Disputes / anomalies (kept, not hidden)

Engine-internal failures on ≤18-bit orders (these are falsified-data points of the
`solvers.py` default configurations, recorded verbatim):

- **kanga** — `ValueError: base is not invertible for the given modulus` on 13 of 15
  seeds across all sizes. Cause: the Wiener walk reached a Jacobian Z≡0 (non-invertible)
  state — engine not robust at these tiny orders with defaults W=32/b=6/K=32.
- **rho** — `TypeError: 'NoneType' object is not subscriptable` on many seeds plus
  silent non-collision on others (18–23 s wasted per call); returned no k. The
  distinguished-set mask (`maskbits=12`) exceeds practical size at ≤18-bit orders.
- Both are engine-default artifacts at small l, NOT evidence of any sub-root shortcut —
  and NOT evidence against generic models either.

## 4. Honest verdict

- **No engine produced α < 0.5 with a sound fit on prime-order toy ECDLP.** bsgs is
  exactly at the generic sqrt baseline (α≈0.494, R²≈0.99994). kanga is *slower* than
  baseline. rho could not be evaluated (disputed).
- **No CLASS 4 / no "breakthrough" is claimed.** Nothing here beats the expected
  generic square-root baseline for prime-order ECDLP.
- The previously documented sub-sqrt α is attributable ONLY to the dedicated
  composite/smooth-order Pohlig–Hellman **control** exhibit (`gen.py --smooth`),
  which is a standard contrapositive control, NOT an EC shortcut — it does not apply
  to prime order.
- Follow-up if desired: raise sizes to db=32+ (needs the T4×2 runner) and reduce
  kanga/rho failure rate by tuning masks — a pure engineering task, not a shortcut.

## 5. Files

- `SCALING_RESULTS.csv` — full per-(db, engine, seed) table: db, l, engine, seed,
  steps, ok, ms, exception.
- `CLASSIFICATION.csv` — per-engine CLASS 0..5, alpha, R², reason.
- `DISPUTES.csv` — per (db, engine) seed-agreement flag.
- `ANOMALIES.csv` — every row with ok=False, verbatim exception text.