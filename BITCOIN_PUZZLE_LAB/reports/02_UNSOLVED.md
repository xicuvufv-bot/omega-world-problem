# 02 — Unsolved targets

**77 unsolved** of 160 → split into two regimes that change the *method*:

- **72 × R1** — address-only (only `hash160(address)` is public). To find the
  key you must enumerate the interval and compare `hash160(pubkey)`. One full
  SHA256+RIPEMD160 per key. Work scales as **W = 2^(n-1)**.
- **5 × R2** — public key **exposed** (#140, #145, #150, #155, #160). An
  interval-DLP solver (Pollard kangaroo / BSGS) applies directly and needs
  only **√W** work on average. Strictly easier *in kind*, not in absolute size.

## Workload estimates

Rate model: **2.5e9 hash160/s** per modern GPU (conservative; see
`08_SOURCES.md`). R1 years ≈ `2^(n-1) / 2.5e9 / (3600·24·365)`.
R2 years ≈ `2^((n+1)/2) / 8e9 ops/s / (3600·24·365)` (kangaroo ≈ √W
group ops total, ×2 for the mean, ~8e9 ops/s ≈ a 4090-class group-op engine).

| # | regime | est. single-GPU years |
|---|---|---|
| 140 | R2 | 7.0e3 |
| 71 | R1 | 1.5e4 |
| 72 | R1 | 3.0e4 |
| 145 | R2 | 5.6e4 |
| 73 | R1 | 6.0e4 |
| 74 | R1 | 1.2e5 |
| 150 | R2 | 2.2e5 |
| 76 | R1 | 4.8e5 |
| 77 | R1 | 9.6e5 |
| 155 | R2 | 1.8e6 |
| 78 | R1 | 1.9e6 |
| 79 | R1 | 3.8e6 |
| … | … | … |
| 160 | R2 | 7.2e6 |

`dataset/puzzles_meta.csv` carries the full 160-row table (lo/hi, hex bounds,
hashes needed, ops per method, tier, method, rank).

## Tiers

| tier | meaning | examples |
|---|---|---|
| `TOY` | solvable on a laptop in seconds/minutes | synthetic w≤32 |
| `LOCAL_FEASIBLE` | solvable here within a benchmark budget | synthetic w≤28 today |
| `LOCAL_INFEASIBLE` | **every real unsolved puzzle** | #71 … #160 |

No unsolved puzzle is in `LOCAL_FEASIBLE`. This is the honest takeaway of the
whole lab: the value is the *toolchain*, measurement discipline, and method
selection — not a funded-address extraction (which is out of scope anyway).

## Structure caveat

`patterns/known_keys_analysis.md` finds **no statistical structure** in the 83
published secrets (uniform position in interval, uniform nibbles, hamming ≈
n/2). Work tables therefore assume full-interval search with no shortcut, and
`06_QUEUE.md` ranks purely by estimated workload.