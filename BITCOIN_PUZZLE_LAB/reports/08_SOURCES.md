# 08 — Sources

## Data provenance

- **Tracker** (`dataset/raw_tracker.txt`): community-maintained Bitcoin Puzzle
  sheet — 160 rows, each: puzzle #, lo = 2^(n-1), hi = 2^n − 1, address,
  solved flag, published private key (hex) where released, compressed pubkey
  where relevant. **Verified** here: all 83 solved rows re-derived
  end-to-end (privkey → pubkey → hash160 → base58check) with a match.
- **`dataset/puzzles_meta.csv`**: *derived* map (lo/hi, work-hashes,
  ops-per-method, GPU-year estimates, tier, method, rank). Estimations, see
  below.

## The puzzle convention

Puzzle #n: private key is an integer in **[2^(n−1), 2^n − 1]** — interval
width 2^(n−1). Addresses are P2PKH. 83 keys were solved over the years; 77
remain, of which exactly 5 have **exposed public keys** (#140, #145, #150,
#155, #160).

## Rate & work model (all estimates are model inputs, not measurements)

- **R1 (address-only):** must hash160 every key: `2^(n-1)` hashes.
  GPU rate assumption: **2.5e9 hash160/s** (a modern GPU doing packed
  SHA256+RIPEMD160; reference-class, but *CPU-to-GPU* multiplier is the real
  uncertainty — our single-core measured 4.5e4/s; the 2.5e9 number implies
  ~5.5e4×).
- **R2 (pubkey exposed):** interval DLP; Pollard kangaroo ≈
  `√(2W)` total group ops mean ≈ `2^((n+1)/2)`. Ops-rate assumption:
  **8e9 group ops/s** (4090-class scalar engine).  GPU-year =
  work / rate / (year seconds), plus a 2× reality factor for kangaroo hopping
  ÷ 2 for only-average search.

## Confidence tiers for estimates

| tier | what | use |
|---|---|---|
| measured | times in `benchmarks/` | method comparisons, ladder checks |
| model | GPU rate assumptions above | queue ordering far apart (orders of magnitude) |
| rule | √W vs W, kangaroo vs BSGS limits | method selection |

Real production numbers would need a GPU harness — explicitly not built here.

## Method references (summary-level; standard results)

- Pollard's kangaroo: Pollard, "Kangaroos, Monopoly and Discrete Logarithms" (1978).
- Distinguished points + parallelization: van Oorschot & Wiener (1999).
- Jump-table partitioning by x: Teske-type apportioned jumps (exponent
  dP table), the `(x >> 120) & 0xF` choice is group-aware (low bits of x are
  degenerate on secp256k1 small intervals — see `07_KANGAROO_NOTES.md`).
- BSGS: Shanks, 1971.

## Honesty statement

No source here is a wallet or node. No private key for any unsolved puzzle
exists in this repository, and none is searched. The lab's outputs are
analysis, not extraction.