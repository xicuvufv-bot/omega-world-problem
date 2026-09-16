# 03 — Method learning (TRY → MEASURE → LEARN → IMPROVE → RE-RANK)

The lab's core discipline. Every stage is logged in `benchmarks/` and this
report; every conclusion below is backed by a measured number, not a hunch.

## The learning log

### 1. Brute force is a floor, not a strategy
`v1` — one full scalar-mult per key — measured **~13.6k keys/s** on one CPU
core. That scaled naively would be hopeless at any *unsolved* size. It exists
as the honest baseline and as the toy-ladder's ground truth.

### 2. The cost of a key is dominated by two things you can attack separately
- **group arithmetic**: replace full scalar-mult with stride point-ADD (O(1)
  per step). v2 measured **43–45k keys/s** (≈3.3× v1), and the raw point-add
  stride loop hits **~125–140k adds/s**.
- **the match test**: with an address you must hash160 every key; with an
  *exposed pubkey* you can instead test `x` alone (`y` parity resolves sign).
  Prefiltering by `hash160(prefix bytes) & bitmask == target-bucket` lets a
  batch scan skip almost all full hashes (and is the standard trick that makes
  the big public R1 solvers fast at all).

**Lesson:** for R1, throughput ≫ math cleverness; the total work is irreducible
`2^(n-1)` hashes. For R2, the whole game changes — see 4.

### 3. Baby-step-giant-step is exact and that matters
`v3` — BSGS — gives the **same answer every time** (verified equal to brute
force at w=20, and internally self-consistent: recovering `k` then re-scans it
back identity). Cost `O(√W)` time **and** storage. At w=28: 0.8–3.3 s with
`m ≈ 11.6k` entries. Storage is the constraint that eventually hands R2 to
kangaroo.

### 4. Pollard kangaroo: the √W memory-free DLP — and its traps
`v4` — the interesting story (`07_KANGAROO_NOTES.md`). Key lessons:

- **Bucket function degeneracy.** V1 of v4 bucketed on `x & 0xF`. On
  secp256k1, field elements of the form `kP`’s x with the interval range are
  *not uniform* in the low bits — empirically the low nibble collapses to
  ~2 values for small intervals → 2 buckets → the walk becomes nearly
  deterministic → misses its meeting. **Fix:** bucket on high bits
  `(x >> 120) & 0xF`. Lesson: *distinguishability must be engineered against
  the actual group’s geometry, not assumed from "random-looking x".*
- **One fixed tame trail beats twin herds for reproducibility.** The classic
  2-kangaroo has a big **per-key variance**: an unlucky (key, tame-launch,
  d0) triple can run >12× the mean meeting time. We measured this hard on a
  24-bit interval. **Fix:** v4 solves "one tame trail from offset 0 + many
  wild passes, each with a fresh random bootstrap jump `d0`"; budget is checked
  between passes; every width 16–28 now solves **on its first pass**, and the
  historical "bad-key" pairs solve across seeds.
- **Off-by-one on interval bases.** The naive recovery formula double-added
  `lo`; the corrected form `k = tame_offset − wild_distance` (both absolute
  in the [0,W) frame) is what finally made 28-bit reliable.
- **`d0 == 0` is the infinity point** — the bootstrap must be changed, not
  just added.

### 5. The dataset is a map, not a to-do list
`puzzles_meta.csv` collapses the tracker into: bounds, regime (R1/R2), the
*type of work* (hashes vs group ops), estimated GPU-years, tier, and method.
The **R2/R1 distinction is the single most important structural fact**: 5
puzzles are attackable with √W interval DLP and the other 72 (unsolved) are
stuck with `W`-scale hashing.

### 6. Pattern analysis: honest "no".
83 solved keys → uniform relative position (mean 0.514, expected 0.5 over
deciles), uniform top/last nibbles, hamming weight ≈ n/2 (0.516). **No
shortcut exists in the data.** This kills any hope of a "position-aware"
reduction and keeps every estimate at full-interval search.

## Re-ranking consequence

The queue (`06_QUEUE.md`) is ordered by *estimated single-GPU years*, i.e.
**#140 (R2, ~7e3) → #71 (R1, ~1.5e4) → #72 → #145 → #73 → #74 → …**. R2
puzzles occupy the top of the order whenever their √W beats a neighboring R1's
W — the qualitative regime advantage, quantified.