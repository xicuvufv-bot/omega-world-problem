# TEST_REPORT — ULTRA-ECDLP-LAB

## The release battery (`tests/run_all.py`)

| # | check | workspace | clean clone |
| --- | --- | --- | --- |
| 1 | `python -m compileall` over the whole tree | ✅ | ✅ |
| 2 | import tests — 16 modules (missing/circular dep screen) | ✅ | ✅ |
| 3 | synthetic secp256k1 suite (vectors/edges/infinity/random/verifier) | ✅ | ✅ |
| 4 | CPU engine build | ✅ | ✅ (from source) |
| 5 | CPU engine selftest → `independent verify: 1` | ✅ | ✅ |
| 6 | CPU bench smoke (`bench 1 8`) | ✅ | ✅ |
| 7 | CLI failure handling (unknown command → exit≠0) | ✅ | ✅ |
| 8 | `detect_env.py` CLI (+ writes JSON) | ✅ | ✅ |
| 9 | `challenge70.py` generate + independent verify | ✅ | ✅ |
| 10 | v5 runner entry points importable | ✅ | ✅ |
| **total** | | **10/10** | **10/10** |

## Synthetic crypto coverage (synthetic-only, no real keys)

- Known-answer vectors: `G` on curve, `G*1 == G`, `G*0 == None`, `G*order == None`.
- Infinity / edge cases: `P+None`, `P+(-P)`, negation on curve, doubling-vs-add.
- Random vectors: 24 randomized scalars vs additive chains and on-curve checks.
- Interval generator bounds: `[2^(bits-1), 2^bits)` for bits 8/16/32/70.
- Independent verifier over the sealed `challenges.json` — all 10 instances pass
  (`k·G == Q`, `k` in interval).

The CPU engine selftest independently proves `kG == Q` on a solved 32-bit random
challenge (its own independent verifier), field distributivity, `2G` jacobian
doubling == affine scalar-mult, and `(n-1)G + G == infinity`.

## Entry-point testing (one target is hardware-gated)

| entry point | tested |
| --- | --- |
| `kaggle_v5_run.py` | full local pipeline run (workspace + clean clone): `TARGET_NOT_REACHED` on CPU, all 12 artifacts produced, honest `staged` rows |
| `detect_env.py` | CLI + JSON output |
| `challenge70.py` | generation + self-verify + CLI usage on missing args |
| `kaggle_70bit_run.py` | import + `main()` present |
| `v4_cpu_engine` | `selftest`, `bench`, unknown-command |
| `kangaroo_cuda` | ⛔ **BLOCKED — no CUDA host** (source-audited only) |
| `research/` modules (16) | import screen |

## What a CPU-only machine cannot test — stated, not hidden

- CUDA compile, CUDA selftest, T4 single/dual benchmarks, batch/autotune
  timings, 70-bit GPU solves, parallel efficiency. All are reported as blocked /
  staged on this host; none are claimed.

## Verdict

CPU-tested release surface: **PASS (10/10)**. GPU surface: **not testable here —
validated on a T4x2 host per `KAGGLE_READINESS.md`**.