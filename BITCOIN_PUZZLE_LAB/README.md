# Bitcoin Puzzle Lab

Universal solver lab for the Bitcoin Puzzle series (#1 → #160). One active
target at a time, a queued pipeline, and a continuous TRY → MEASURE → LEARN →
IMPROVE → RE-RANK loop. Built as a sequence of *verified, benchmarked* solver
versions — never as a black box.

## Hard safety boundary (applies to every module here)

- **No real-fund operations.** No ECDSA signatures, no transactions, no
  withdrawals, no network/full-node interactions.
- Solver targets are always one of:
  1. **synthetic keys** generated locally (toy intervals, `TOY` tier),
  2. **published solved puzzles** (reproduction + verification only),
- A solver never searches a funded, unsolved address's own key space
  automatically; such searches are non-goals. The 5 exposed-pubkey unsolved
  puzzles (#140..#160) are **analyzed** here (structure, work estimates,
  method selection) — not brute-forced.
- All "SOLVED" entries in `reports/01_SOLVED.md` are toy-scale synthetic solves
  or published-solve reproductions, explicitly labeled as such.

## Layout

```
dataset/        raw tracker + puzzles_meta.csv (160-row map: regime, work, tier)
algorithms/     curve arithmetic (self-contained secp256k1), intervals, metrics
solvers/        v1 brute-force · v2 stride+bitmask · v3 BSGS · v4 kangaroo
experiments/    benchmark + toy-chain runners (single command: run_all.py)
reproductions/  published-solve verification (83/83; verify_published.py)
patterns/       statistical analysis of published solved keys -> known_keys_analysis.md
benchmarks/     results.json + summary.md (all measured numbers)
reports/        00_MASTER_STATUS … 08_SOURCES
tests/          pytest suite (run from lab root: python -m pytest)
```

## Running everything

```
python experiments/run_all.py      # benchmarks + toy solves + pattern analysis
python reproductions/verify_published.py
python -m pytest -q                # unit + integration suite
python -m pytest production/tests -q   # production pipeline suite
```

Zero third-party dependencies required (stdlib `hashlib`, `pow` field math).

## Production module (`production/`)

`production/` is the **challenge-orchestration layer**: it wraps the two
canonical open-source puzzle engines (brichard19/BitCrack + JeanLucPons/
Kangaroo) behind one CLI (`python -m production.manager …`). It operates
under a *tighter*, registry-locked boundary than the analysis modules:

- Targets are resolved ONLY against the frozen official 160-address registry
  (`production/registry_data.py`, generated from the canonical tracker);
  arbitrary addresses and out-of-interval ranges are refused.
- Solved puzzles can never be selected.
- BitCrack = R1 (no pubkey) brute force; Kangaroo = R2 (exposed pubkey)
  interval DLP. See `production/README.md` for the full operating model,
  checkpointing, and honest feasibility tables.
- `production/cluster/` is the distributed extension: one coordinator
  (`serve`) + any number of worker nodes (`node` + `--slots`), lease-based
  work stealing, HMAC/TLS wire security, and a live text C2 dashboard
  (`dashboard`).

## Solver version log (why each version exists)

| Solver | Method | vN better than v(N-1) because… | Measured |
|---|---|---|---|
| v1 | naive scan, scalar-mult per key | baseline | see benchmarks |
| v2 | stride point-add + hash160 bitmask prefilter | O(1) point add per key (vs full mult) | see benchmarks |
| v3 | Baby-step Giant-step (BSGS) | O(√W) time **and** storage, exact interval DLP | see benchmarks |
| v4 | Pollard kangaroo (Teske jump table, edge guards) | O(√W) time, O(1) memory, trivially parallelizable | see benchmarks |

Full evidence in `benchmarks/summary.md` and `reports/04_ALGORITHMS.md`.