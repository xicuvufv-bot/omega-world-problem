# 04 — Algorithms

All solvers share the same self-contained secp256k1 core
(`algorithms/curve.py`, field math via stdlib `pow`) and Stdlib-only hash160
(`algorithms/hash.py`). No third-party crypto.

Common problem: find `k` in `[lo, hi]` (interval width `W = hi − lo + 1`)
such that `S + Q = k·G` for target point `Q`. In the puzzle setting:

- **R1 (address-only):** we only have `h = hash160(pubkey)`, so `Q` is
  unknown — must hash every candidate.
- **R2 (exposed pubkey):** `Q` is known → interval DLP applies directly.

## v1 — brute force (baseline)

- For `k` from `lo` to `hi`: `scalar_mult(k)`, `compressed()`, `hash160`,
  compare.
- Time `Θ(W)` group ops (`Θ(n)` per scalar-mult) — the naive floor.
- Measured: **~13.6k keys/s** (single CPU core).
- Used as ground truth for toy ladder (`tests/test_v1.py`, D-section).

## v2 — stride point-add + bitmask prefilter

- Walk the interval with **point-ADD each step**: `P_{k+1} = P_k + G`.
  O(1) group op per key instead of O(n).
- For R1-style matching, first hash a *single* probe candidate, derive a
  **bitmask bucket** from the target hash’s low bytes, and skip any key whose
  own `hash160(prefix)` doesn’t share the bucket. Skip-rate ≈
  `1 − 2^{popcount(mask)}/2^{bits}`; every skipped key avoids a full hash.
  Single-target runs can’t skip (the probe equals the target bucket), which is
  why the masked path ≈ stride + hash-complete.
- Measured: **~44k keys/s** masked (3.3× v1); pure stride loop
  **~125–140k adds/s**.
- Realism: this is the shape the major public R1 miners use (GPU, batched
  hash160 with bitmask); scaling 30–50× from CPU to GPU is the expected
  multiplier, not a count of keys.

## v3 — Baby-step Giant-step (BSGS), exact

- With `m = ⌈√W⌉`: precompute baby table `{j·G → j : j < m}` (`Θ(m)` storage),
  then walk `Q − i·m·G` for `i` until the table hits — recover
  `k = lo + i·m − j`.
- Time `O(√W)`, storage `O(√W)`. Deterministic; used as the heavyweight oracle
  in the ladder.
- Verified equal to brute force on toy widths and self-consistent
  (re-scan confirms identity): w=16..28 all `ok=True`.
- Limits: memory (≈ 32·√W bytes for point+bucket at a minimum) and random
  access; at real R2 sizes this is why kangaroo wins despite the same √W time.

## v4 — Pollard kangaroo (Teske jumps, huge dP, fixed trail)

- Two pseudorandom walks in `[0, W)`: **tame** from offset 0, **wild** from
  `Q − lo·G` (interval-relative). Jumps use a Teske apportioned-by-`x` table
  so a `dP` collision lands on a matching jump index → solve the linear
  equation.
- Time `O(√W)`, **memory O(1)**, trivially embarrassingly parallel.
- Correctness engineering (detailed in `07_KANGAROO_NOTES.md`):
  - **bucket = `(x >> 120) & 0xF`** — never low nibbles (degenerate on
    secp256k1 small-interval x’s).
  - **one tame trail + many wild passes**, each wild pass with a fresh random
    bootstrap `d0`; meet-time tail eliminated (measured, see notes).
  - recovery `k = tame_offset − wild_distance` (absolute offsets; no 2nd `lo`).
  - `d0 == 0` → infinity point guard.
  - exact `y`-match on collision (not just `x`), two hesitance index alignment.
- Measured at w=28: ~28.8k hops in ~31 s, ≤2.0× theory across all widths
  (fine for a twin-trail variant).

## Choosing between v3/v4 for R2

| | v3 BSGS | v4 kangaroo |
|---|---|---|
| work | ~√W | ~1.25√W/hops? per herd |
| storage | Θ(√W) | O(1) |
| determinism | exact | probabilistic (trail/pass design converges in practice) |
| parallel | moderate | trivial |
| real 1e10+√W sizes | memory-bound | the pick |

`06_QUEUE.md` records **kangaroo** as the R2 method for real targets, with BSGS
as the check oracle at verification scale.