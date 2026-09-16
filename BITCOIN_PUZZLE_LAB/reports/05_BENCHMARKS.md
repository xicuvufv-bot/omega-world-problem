# 05 — Benchmarks (measured, single CPU core)

Everything below is a real logged run. `benchmarks/results.json` is the
machine-readable copy; `summary.md` is its digest.

## A. Throughput (scan primitives)

| selector | keys/s |
|---|---|
| v1 naive (scalar-mult per key) | 13,646 |
| v2 stride (point-add + full hash) | 43,234 |
| v2 masked (point-add + bucket + hash) | 44,763 |
| v2 pure stride loop (no hash) | 125,471 |

Takeaways
- v2’s point-add wins ~3.3× over v1 — the arithmetic engine, not the hash.
- mask v. full-hash differ by only ~3% on a *single* target because every
  bucket equals the target bucket; the mask pays off on multi-key batches.

## B. Interval-DLP scaling (synthetic keys, exact oracle BSGS)

| bits | BSGS s | BSGS mem | kang s | kang hops | theory | ratio |
|---|---|---|---|---|---|---|
| 16 | 0.06 | 182 | 0.39 | 212 | 226.9 | 0.93 |
| 20 | 0.30 | 725 | 1.81 | 1,762 | 907.5 | 1.94 |
| 24 | 0.84 | 2,897 | 5.52 | 1,895 | 3,630.0 | 0.52 |
| 28 | 3.31 | 11,586 | 31.3 | 28,845 | 14,519.9 | 1.99 |

- theory = `√(2W)` total hops (2 herds × √W/… practical constant);
  ratio = kang_hops/theory. Ratios 0.5–2.0 across 4 widths = the
  implementation tracks theory — meet-time filth is gone.
- `kang_ok = True` for **every** row, plus seed-sweep robustness for the
  historical "bad keys" (see `07_KANGAROO_NOTES.md`).

## C. Solver-ladder agreement (20-bit toy, k = 586,742)

| solver | result |
|---|---|
| v1 brute force | 586,742 (10k-cap: 3.56 s scan) |
| v2 stride | identity under cap |
| v3 BSGS | 586,742 (m = 725) |
| v4 kangaroo | 586,742 (146 hops) |
| all agree | True |

## D. Pattern analysis (83 solved keys)

- relative position mean **0.514** (uniform → 0.5; deciles spread 5–14)
- hamming-weight fraction **0.516** (uniform → 0.5)
- top nibble uniform, last nibble (mod 16) uniform
- verdict: **no structure worth exploiting** (`patterns/known_keys_analysis.md`)

## Honest extrapolation caveats

- CPU numbers above are *ported* to a GPU model for estimates: 2.5e9 hash/s
  and 8e9 ops/s are references for a modern GPU, **order-of-magnitude**, and
  should be re-measured in the real harness — the lab’s numbers only prove
  *relative* method behavior (√W vs W, mask vs no-mask).
- Real R2 work estimates assume full-interval kangaroo at theory; single-GPU
  years for #140 = **7.0e3** (GPU-years table in `02_UNSOLVED.md`).
- Production search is out of scope; these are **method-selection inputs**.