# Production pipeline — Bitcoin-Puzzle orchestration

A discipline wrapper around the two canonical open-source GPU engines:

| engine | repo | method | when |
|---|---|---|---|
| **BitCrack** (`cuBitCrack`) | `brichard19/BitCrack` | full-interval hash160 scan | R1 puzzles (address-only, no pubkey) |
| **Kangaroo** (`kangaroo`) | `JeanLucPons/Kangaroo` | Pollard interval-DLP (`√W`) | R2 puzzles (pubkey exposed) |

The pipeline exists to make one thing safe and repeatable: **coordinated,
checkpointed, multi-GPU work across the official puzzle ranges**. It does
**not** claim, broadcast, or build transactions — key extraction + offline
verification only.

## Scope boundary (hard)

- The attack surface is the **frozen official registry** (`registry_data.py`,
  generated from the canonical roadhero tracker). `registry.py` refuses any
  address that is not one of the 160 published puzzle addresses.
- A scan range must be a **sub-interval of the puzzle's own official range**
  `[2^(n-1), 2^n - 1]`. Anything else is rejected (`keyspace.validate_subrange`).
- Solved puzzles can never be selected as targets.
- This deliberately does not generalize into a "scan any wallet" tool.

## Layout

```
production/
  registry_data.py   frozen 160-row table (generated)
  registry.py        target resolution (registry-locked)
  keyspace.py        bounds, hex ranges, share splitting
  strategy.py        engine selection + honest feasibility model
  gpu.py             nvidia-smi read-only inventory
  checkpoint.py      ledger.json + native engine checkpoint handling
  validator.py       offline key -> address + WIF verification
  runner.py          native subprocess worker + on-found hook
  status.py          live tracker + chain spot-check + diff
  manager.py         CLI entry point
  build/             engine build scripts (Windows PS / Linux sh)
  native/            Beast Mode: hash160.c + DLL, mmap ledger, binproto, affinity
  state/             runtime: ledger, checkpoints, logs, found keys
  tests/             pytest suite
```

## Workflow

```bash
# 0. build engines (one-time)
powershell -ExecutionPolicy Bypass -File production\build\build_windows.ps1   # or
bash production/build/build_linux.sh

# 1. verify the puzzle state is unchanged BEFORE spending GPU time
python -m production.manager status --chain

# 2. feasibility rank (honest: every puzzle is a multi-thousand-GPU-year job)
python -m production.manager plan

# 3. dossier of one target
python -m production.manager audit --number 71
python -m production.manager audit --number 140

# 4. measure YOUR real keys/s on a small window (needed to trust the numbers)
python -m production.manager bench --number 71 --bits 26

# 5. plan the run without launching anything
python -m production.manager scan --number 71 --gpus 4 --dry-run
python -m production.manager scan --number 140 --engine kangaroo --gpus 4 --dry-run

# 6. launch for real (sub-range allowed, still must be inside the puzzle shell)
python -m production.manager scan --number 71 --gpus 4
python -m production.manager scan --number 140 --engine kangaroo --gpus 4 \
        --extra "-d 24 -ws -wi 120"

# 7. resume after a stop (native engine checkpoints keep positions)
python -m production.manager resume --number 71
python -m production.manager scan --number 71 --gpus 4

# 8. show a verified found key (privkey, WIF, both address forms)
python -m production.manager found
```

`--start` / `--end` (hex) restrict the scan to a sub-range; the splitter can
divide it across GPUs. `--extra` passes raw engine flags through (e.g. BitCrack
`-b/-t/-p`, Kangaroo `-d/-g`).

## On-found behavior

1. `runner.py` scans the engine stdout for the known privkey line shapes
   (`Key found privkey …`, `KEY FOUND! …`, `Key: 0x…`).
2. Every candidate is run through `validator.verify_candidate()` **before**
   anything is written: derive pubkey (compressed + uncompressed), hash160 →
   P2PKH address, compare with the target address.
3. On a match the artifacts (privkey hex, WIF compressed/uncompressed, both
   address forms) are written to `state/found/puzzle_N_<addr>.txt`, the
   checkpoint ledger is marked `found`, and a shared stop `Event` terminates
   every other running worker (no duplicate-claim race).
4. Broadcasting / claiming is intentionally **not** implemented. Move the key
   with standard wallet tooling only if you intend to claim the public prize,
   and be aware of front-running bots (puzzles #66/#69 were lost that way —
   the safest claim path is a private/off-chain method, none of which this
   project automates).

## Checkpointing (both engines)

- **BitCrack**: `--continue state/scans/<n>_<share>.kc` — the engine rewrites
  its own progress file (contains `Start key` / `End key` / `Next key`).
  Re-launching `scan` with the same share count resumes from that `Next key`
  automatically.
- **Kangaroo**: `-w state/work/<n>_<share>.work -wi <sec> -ws` — resume with
  `-i <workfile> -w <workfile>`. Merge across hosts with `kangaroo -wm`.
- `state/ledger.json` is the master record: every claimed share, its status,
  heartbeat, and engine checkpoint path. `resume` re-lists unfinished shares.

## Distributed / multi-host

- One worker per GPU per share; the orchestrator fans out over devices.
- Kangaroo has native client/server (`-s`, `-c <host>`) plus `-wm` merge —
  that is the supported multi-host path for R2 ranges.
- For R1 (BitCrack) multi-host, hand out disjoint `--keyspace START:END`
  slices (or `--share M/N`) and merge the `--continue` accounting in the
  shared ledger.

## Distributed cluster (`production/cluster/`)

The local scanner becomes a coordinated **task-execution cluster** when you
run the coordinator once and a node on every GPU host — same binaries, all
slices served from one lease-brokered pool.

```
┌───────────────────────────── coordinator (one) ─────────────────────────────┐
│  Scheduler  (unit pool, lease expiry = work stealing, atomic ledger)        │
│  Telemetry  (sliding-window keys/s, node table, live dashboard)             │
│  FOUND path (re-verifies every key offline before persisting)               │
└───┬──────────────┬──────────────┬──────────────┬────────────────────────────┘
    │ TLS │ TCP    │ TLS │ TCP    │              │
┌───▼───────┐  ┌───▼───────┐  ┌───▼───────┐  …   │  node N × GPU slots
│ node A    │  │ node B    │  │ node C    │      │  each slot = one conn,
│ slot0 GPU0│  │ slot0 GPU0│  │ slot0 GPU0│      │  one unit, one heartbeat
│ slot1 GPU1│  │ slot1 GPU1│  └───────────┘      │
└───────────┘  └───────────┘                     │
```

### How a cluster is minted

1. `serve --number N --token T` resolves the puzzle against the **frozen
   registry**, slic*s* it into stealable units (R1), or pins one unit (R2).
   The coordinator owns the ledger (`state/cluster_ledger.json`, written
   atomically: tmpfile + fsync + rename).
2. `node --host <coord> --token T` connects per GPU slot, authenticates
   (challenge/response — the token is never sent), and pulls one unit at a
   time.
3. A slot that finishes pulls the next unit; a slot that dies stops
   heartbeating; when its unit lease expires another node **steals** it —
   no second of hashing is stranded and no interval is double-funded.

### Commands

```bash
# on the coordinator host
python -m production.manager cluster-keygen --tls --cert-dir state  # token + TLS cert
export CLUSTER_TOKEN=<printed>
python -m production.manager serve --number 140 --token "$CLUSTER_TOKEN" \
        --engine kangaroo --port 25200
python -m production.manager serve --number 71  --token "$CLUSTER_TOKEN" \
        --engine bitcrack --units 32 --lease-ms 60000

# on every GPU host (as many slots as you give, now or grow later)
python -m production.manager node --host coord.example.com:25200 \
        --token "$CLUSTER_TOKEN" --name datacenter-gpu-1 --slots 2
python -m production.manager node --host coord.example.com:25200 \
        --token "$CLUSTER_TOKEN" --name 3090-rig --slots 1

# anywhere on the coordinator host
python -m production.manager dashboard          # live C2 text telemetry
python -m production.manager cluster-status     # one-shot snapshot
```

### Telemetry & C2

- Coordinator publishes `state/cluster_metrics.json` every ~2s.
- `dashboard` renders it as an updating ASCII panel: total keys/s, per-node
  rate table (`ONLINE`/`OFFLINE`), keys/s history bar chart, unit-pool
  progress. `RateMeter` is a 60 s sliding window, so a node that dies drops
  out of the total within one window — no phantom hashrate.

### Work stealing & fault tolerance (protocol level)

- Lease: a claimed unit carries an expiry. Heartbeat (`every 5 s`) extends it.
- Stealing: any node may claim a unit whose lease expired; the scheduler's
  counter is bumped so a stolen unit is never given to two live workers.
- `DONE` with `keys_checked` feeds the accounting + telemetry.
- `error` units return to the pool, re-dispatchable up to 3 attempts (then
  `dead`); `exhausted`/`found` never re-dispatch.
- Node outage = lease expires = unit re-offered. Local engine checkpoints
  (`*.kc` / `*.work`) remain in place, so even re-execution resumes from the
  native progress file instead of the slice start.

### Honesty about the wire

- Every frame is HMAC-SHA256-signed with the shared token; a bad signature
  terminates that connection. TLS (server-side cert) can be layered on for
  WAN links; on a trusted LAN/VPN the HMAC layer alone is tamper-evident.
- The coordinator **re-verifies** every `FOUND` (derives the address from the
  private key locally) before writing `state/found/` — a misbehaving node
  cannot inject a fabricated finding.
- The registry lock never loosens: units only ever come from the frozen
  puzzle table; no arbitrary address can enter the pool or the wire.

## Beast Mode (native layer `production/native/`)

Four raw-speed modules that strip Python overhead from the hot paths. All
stdlib-ctypes, zero pip deps.

| module | what it is | where it helps |
|---|---|---|
| `hash160.c` → `bin/hash160.dll` | self-contained SHA-256 + RIPEMD-160 + Base58Check in C (no OpenSSL) | address derivation, checksum validation |
| `hash160_ffi.py` | ctypes bridge + **batched** kernel `h160_hash160_batch` (N×33-byte pubkeys → N 20-byte digests in one call) | validator throughput; amortized ctypes cost |
| `mmap_ledger.py` | memory-mapped fixed-record ledger, 64-byte cache-line records, atomic header, lease/steal semantics | replaces JSON ledger writes for the scheduler |
| `binproto.py` | struct-packed binary wire format (24-byte header + HMAC-SHA256), typed dict encoding | replaces JSON envelopes between coordinator and nodes |
| `affinity.py` | NUMA partition + `SetThreadAffinityMask`/`sched_setaffinity` pinning | bind compute threads to cores, network threads elsewhere |

Build the native DLL once (MSVC):

```powershell
cmd /c "call `"C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools\VC\Auxiliary\Build\vcvarsall.bat`" x64 && cl /O2 /LD production\native\hash160.c /Febin\hash160.dll"
```

Linux/macOS: `gcc -O3 -shared -fPIC -o bin/libhash160.so production/native/hash160.c` (the FFI loader picks the platform binary automatically).

Verification anchors: the DLL matches every official RIPEMD-160 spec vector and
the canonical Bitcoin constant `hash160(SECP256k1 compressed G)` =
`751e76e8199196d454941c45d1b3a323f1433bd6`, and every digest + batched batch
cross-checks `hashlib`.

Honest note on speed: per-*call* ctypes overhead cancels the native gain, so
the native path only wins with the batched kernel (`hash160_batch`, same order
of magnitude as the pure-Python loop but monotonic in batch size). Use the
batch API in the validator, not single-key calls.

## secp256k1 Engine (CPU-native fused scan — `secp256k1_engine.c`)

The missing link for "Beast Mode" CPU scans: a single C module that performs
the entire key→scan pipeline in one process boundary, eliminating per-key
Python overhead entirely.

### What it does

For a given starting private key `start` and a range of `n` keys (incrementing
by +1 each step), the engine in a single C call:

1. **scalar_mult_window** the start key onto the curve (window-4 MSB scan;
   ~130-200 group operations for a 256-bit key)
2. **jac_madd** +1 for each subsequent key in the range (one Jacobian+affine
   mixed addition per key — a small fraction of the ~13µs per-key budget)
3. **Montgomery batch inversion** to affine-convert all `n` Jacobian points
   at once (~5× faster than `n` individual inversions)
4. **Fused hash160** (SHA-256 + RIPEMD-160) per pubkey
5. **Target scan** against a caller-supplied list of 20-byte digests, returning
   the first match

A `scan(start, n, targets)` call crosses the Python→C boundary **once** and
stays there for the entire range.

### Architecture

```
┌───────────────────────────────────────────────────────────┐  Python
│  secp256k1_ffi.py  Context(max_batch=4096)                │
│    scan(start, n, targets) → ScanResult                   │
│    scan_threaded(start, n, targets, n_threads=4) → merged│
└───────────────────────────┬───────────────────────────────┘
                            │ ctypes.c_void_p (opaque context)
┌───────────────────────────▼───────────────────────────────┐  C
│  secp256k1_engine.c  (917 lines, single-TU DLL)           │
│                                                           │
│  s256_ctx_new(batch) ─► precompute Wx[15]/Wy[15] table   │
│  s256_seek(key)      ─► scalar_mult window-4 onto curve   │
│  s256_run(count,...)  ─► jac_madd ×count + Montgomery     │
│                         batch inversion + fuse hash160     │
│  s256_set_targets()  ─► set match digests                  │
│                                                           │
│  Also self-contained: SHA-256, RIPEMD-160                 │
└───────────────────────────────────────────────────────────┘
```

### Build

Same MSVC one-liner (existing `bin/` path):

```powershell
cmd /c "call `"C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools\VC\Auxiliary\Build\vcvarsall.bat`" x64 && cl /O2 /LD production\native\secp256k1_engine.c /Febin\secp256k1.dll"
```

Linux: `gcc -O3 -shared -fPIC -o bin/libsecp256k1.so production/native/secp256k1_engine.c`

### Python surface (`secp256k1_ffi.py`)

```python
from production.native import secp256k1_ffi as eng

# single key
pub33 = eng.privkey_to_pubkey(1)

# fused scan (one ctypes call for the whole range)
res = eng.scan(start=33, n=10_000, targets=[target_digest])
assert res.found_idx == 777          # relative to start
assert res.found_key == (33+777).to_bytes(32, "big")

# multi-threaded: one pinned native context per core, merged result
res = eng.scan_threaded(33, n=50_000, targets=[d1, d2], n_threads=4, pin=True)

# benchmark
rate, _ = eng.scan_rate(start=1, n=262_144)
```

### Verified correctness (test suite: `test_secp256k1.py` — 41 tests)

All results cross-checked against the independent pure-Python reference
(`algorithms/curve.py` — secp256k1 scalar_mult + compressed + to_affine) and
hashlib, never against themselves.

| gate | what |
|---|---|
| `s256_selftest` | in-C self-test (SHA-256, RIPEMD-160, EC formulas) — embedded |
| canonical `1G`, `2G` | hardcoded hex against published SECP-256k1 vectors |
| 25 random keys | `privkey_to_pubkey(k)` == `compressed(scalar_mult(k))` |
| 3×300 batch scan | every derived pubkey equals the per-key Python reference |
| hash160 consistency | every `hash160s20[i]` == `hashlib.sha256(ripemd160(pubkey_i))` |
| buried target scan | match found at the exact expected delta index |
| first-of-many | earliest hit selected |
| chunked (max_batch < n) | chunk boundary produces identical results to unchunked |
| threaded == single | `scan_threaded` merged result matches single-threaded scan |
| key=0 rejected | `scan(0, …)` → `ValueError` (secp256k1 private key must be ≥ 1) |

### Throughput (Ryzen 3 3200G, measured)

| mode | keys/sec |
|---|---|
| single-thread | ~76,000 |
| 4-thread pinned | ~105,000 |

Per-key cost: ~13µs (single-thread, purely in C — no Python in the hot loop).

### Honest assessment

The fused scan closes the gap between "one key per Python call" and "GPU":
at 76k-105k keys/sec, a 34-bit sweep (~17 billion keys) takes ~5 years on
this CPU (vs ~36,000 GPU-years for the same range with BitCrack). For 34+ bit
ranges the engine is practically useful as a **parallel complement** to the
GPU scan — or as the entire pipeline on machines with no GPU. It is not a
replacement for GPU engines at 40+ bit ranges; it closes the gap for
mid-range puzzles where every bit matters and CPU cores can contribute while
the GPU is busy.

## Honest expectations

Every remaining puzzle is in the `EXTREME` tier:

| puzzle | method | single-GPU estimate (default rates) |
|---|---|---|
| #140 (R2) | kangaroo | ≈ 9,700 GPU-years |
| #71 (R1)  | BitCrack | ≈ 62,000 GPU-years |
| #72 (R1)  | BitCrack | ≈ 124,000 GPU-years |
| #150 (R2) | kangaroo | ≈ 310,000 GPU-years |
| … | … | … |

These are **lower bounds at 6e8 (R1) / 6e9 (R2) keys-or-ops per second**; feed
in real numbers from `bench` to correct the plan. No statistical shortcut is
known (the 83 published keys show uniform interval position — see
`../patterns/known_keys_analysis.md`). The correct use of this pipeline is as
a *coordination frame* for a pool or fleet, not as a solo nights-and-weekends
hobby run.