# Knowledge Graph — BITCOIN_PUZZLE_LAB

The lab as a directed graph. **Edges** are claim → support links; **leaf
evidence** is a measured number or verified artifact. Keep this flat so any
report can be cross-checked.

## Entities

```
PUZZLE #1..160
  |-- INTERVAL(lo=2^(n-1), hi=2^n-1, W=2^(n-1))
  |-- ADDRESS        (P2PKH, hash160(pubkey))
  |-- REGIME: R1 address-only | R2 pubkey-exposed
  |-- STATUS: SOLVED (83) | UNSOLVED (77)
  |-- R2 exposure: #140 #145 #150 #155 #160
  `-- VERIFIED-BY: reproductions/verify_published.py 83/83

METHOD (v1..v4)
  |-- v1 brute-force     Θ(W) time, scalar-mult per key
  |-- v2 stride+mask     Θ(W) time, O(1) group per key + hash prefilter
  |-- v3 BSGS            Θ(√W) time AND memory (exact)
  |-- v4 kangaroo        Θ(√W) time, O(1) memory, parallel (probabilistic)
  |-- for R1: hash scan  (W hashes) — only route
  `-- for R2: DLP on Q   (√W group ops) — the qualitative win

MEASUREMENT (benchmarks/)
  |-- throughput: v1 13.6k/s | v2 43-45k/s | stride 125-140k/s
  |-- DLP scaling: BSGS & kangaroo ok at w=16..28
  |-- ladder: v1==v3==v4==k on 20-bit toy
  `-- pattern: uniform -> no shortcut (mean 0.514/0.516)

DECISION QUEUE  (reports/06)
  #140 R2 7.0e3 GPU-yr -> #71 1.5e4 -> #72 3.0e4 -> #145 5.6e4 -> ...
  Rule: EXACT k for R2 (never approximate); interval-DLP-when-R2; else hash.
```

## Edge table (claim → evidence)

| claim | evidence |
|---|---|
| tracker parsing correct | `tests/test_interval.py` + 83/83 addr re-verify |
| scalar-mult / hash160 / base58 correct | `verify_published.py` 83/83 round-trip |
| v1 baseline | 13.6k keys/s (A) |
| point-add ≫ scalar-mult for scanning | v2 3.3× v1 (A) |
| mask saves hashes; single-target can't skip | A mask≈45k=v≈43k+hash |
| BSGS exact | B all widths ok; ladder agree |
| kangaroo matches theory | ratio 0.5–2.0 across widths |
| meet-time tail fixed | 1st-pass solves, seed sweeps (07) |
| bucket degeneracy on low nibbles | 20-bit timeout → high-bit fix (07) |
| no key-position shortcut | C deciles + nibbles + hamming (05) |
| all unsolved LOCAL_INFEASIBLE | minimum #140 ≈ 7.0e3 GPU-yr (02) |
| #140 is top target | 7.0e3 < everything (06) |

## Source of truth

- **numbers**: `benchmarks/results.json` (machine) + `summary.md` (human)
- **map**: `dataset/puzzles_meta.csv` (160 rows)
- **analysis**: `patterns/known_keys_analysis.md`
- **narrative**: `reports/00..08`
- **tests**: 29/29 green (from lab root, `python -m pytest -q`)