# 00 — Master Status

_Last updated: 2026-09-15 · pipeline: **ACTIVE** · target: **#140 (R2)**_

## Mission

A disciplined, tool-supported study of the Bitcoin Puzzle series (#1 → #160):
every solver is a **verified, benchmarked, versioned** implementation, and every
conclusion is backed by a logged measurement. This is a *lab*, not a black box.

## Hard safety boundary

- No real-fund operations of any kind (no signatures, txns, network, wallets).
- Targets are always **synthetic keys** or **already-published solved keys**.
- The 5 **exposed-pubkey** puzzles (#140 … #160) are *analyzed* (structure,
  work, method) — never brute-forced, and their private keys are never
  approximated.
- All "SOLVED" entries are toy-scale synthetic solves or confirmations of
  published solves (see `01_SOLVED.md`).

## System state

| Component | Status | Evidence |
|---|---|---|
| secp256k1 arithmetic (stdlib `pow` field math) | ✅ | `tests/test_curve.py`, 83/83 address re-verification |
| hash160 (SHA256+RIPEMD160, stdlib) | ✅ | same re-verification |
| interval + tracker parsing | ✅ | `tests/test_interval.py`, `dataset/` |
| v1 brute-force (baseline) | ✅ measured | 13.6k keys/s (Benchmarks) |
| v2 stride + bitmask prefilter | ✅ measured | 43x keys/s (44.7k) |
| v3 BSGS (exact interval DLP) | ✅ all widths | w=16..28, m=√W |
| v4 Pollard kangaroo (tail-fixed) | ✅ all widths | w=16..28, ratio stable |
| dataset map (160 rows) | ✅ | `dataset/puzzles_meta.csv` |
| pattern analysis (83 solved keys) | ✅ | `patterns/known_keys_analysis.md` |

## Live cycle

TRY → MEASURE → LEARN → IMPROVE → RE-RANK (details in `03_METHOD_LEARNING.md`).
Currently: solvers v1–v4 verified → next pipeline action is documented in
`06_QUEUE.md`.

## Difficulty posture (honest)

- Every unsolved puzzle is → **LOCAL_INFEASIBLE** on a single desktop GPU
  (minimum ≈ 5 years of one 4090, best case #140 at ~7k GPU-years ≈
  7k years on a desktop … i.e. a real project, not a hobby run).
- Cheapest realistic next target by workload: **#140** (R2, ~7.0e3 GPU-years,
  interval DLP on the exposed pubkey) then **#71** (R1, ~1.5e4 GPU-years).
- Numbers are **estimates**; see `08_SOURCES.md` for the rate model and honest
  caveats. R2 puzzles enjoy a **qualitative** advantage: interval-DLP
  (√W thinking) applies, where R1 hash-scan (W thinking) does not.

## Report index

| Report | Contents |
|---|---|
| 01_SOLVED | 83 published solves, end-to-end re-verified |
| 02_UNSOLVED | 77 targets, workload estimates, tiers |
| 03_METHOD_LEARNING | the TRY→MEASURE→LEARN loop and its lessons |
| 04_ALGORITHMS | v1–v4 solver designs, correctness, big-O |
| 05_BENCHMARKS | all measured numbers |
| 06_QUEUE | ranked attack queue + method selection |
| 07_KANGAROO_NOTES | the v4 engineering journey (traps fixed) |
| 08_SOURCES | data provenance + estimate basis |