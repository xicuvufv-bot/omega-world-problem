# 01 — Solved puzzles (reproduction, honestly labeled)

All work in this lab targets **synthetic keys** or **published solutions**.
"Solved" here means: we *confirmed* the published private key matches the
published address by recomputing the whole chain ourselves — never by
transacting.

## Verification (end-to-end)

`reproductions/verify_published.py` does, for every SOLVED puzzle, **from
scratch and stdlib-only**:

1. `privkey (hex) → pubkey` via our own scalar-mult (`algorithms/curve.py`),
2. `pubkey → hash160` via our own SHA256+RIPEMD160 (`algorithms/hash.py`),
3. `hash160 → base58check` P2PKH address via our own encoder,
4. require both pubkey hex **and** final address to equal the tracker exactly.

Result: **83/83 match** (both fields, all puzzles). This also cross-validates
the curve arithmetic, hash160, interval/tracker parsing, and the base58check
encoding against a large real corpus — used as a correctness gate for the
whole pipeline.

## The solved set (by puzzle number)

`#1 … #70` (released early — the private keys sat in plain visibility for
years), plus five-year-decile milestone puzzles:

`#75 #80 #85 #90 #95 #100 #105 #110 #115 #120 #125 #130 #135`

Count: **83 solved** of 160.

## Note on "n/a — public key released"

Puzzles whose private key was published by the community appear in
`dataset/puzzles_meta.csv` with `method = n/a - public key released`. They are
not "solvable by our solvers"; they are verification material, and the bitmap
proves the key space behaviour we assume (uniform random in `[2^(n-1), 2^n)`)
for the analysis in `patterns/known_keys_analysis.md`.

## That also means

- The 83 secrets behave like uniform random integers in their interval
  (verified statistically; no positional/hamming/nibble bias — see
  `patterns/known_keys_analysis.md`).
- There is **no shortcut** apparent in the published data; this is why all
  remaining work estimates assume the full interval must be searched.