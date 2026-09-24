# REPRODUCTION — ULTRA-ECDLP-LAB

Goal: from a **clean `git clone`** on a machine that has only a C++17 compiler
(+ an NVIDIA/CUDA host for the GPU phases), reproduce the toolchain, the tests,
the synthetic benchmark, and the report set — with zero files from the author's
machine.

## 1. Clone

```bash
git clone <repository> && cd ULTRA-ECDLP-LAB
```

Requirements at this point: `python3`, `g++` (or `nvcc` for GPU). Nothing else.

## 2. Record the environment

```bash
python research/v4/detect_env.py
```

Writes `KAGGLE_ENVIRONMENT.json` on **this** host. If it reports no GPU, the
pipeline treats GPU phases as blocked and says so.

## 3. Build the reference CPU engine

```bash
python build.py cpu
# or, on an NVIDIA host:  python build.py cuda
```

## 4. Run the release test battery

```bash
python tests/run_all.py
```

Expected: `run_all complete: N/N checks passed, 0 failed` — compileall, import
tests, synthetic secp256k1 crypto suite, CPU selftest, bench smoke, CLI failure
handling, env probe, challenge generator + independent verify, runner entry
points.

## 5. Run the full v5 pipeline (CPU path)

```bash
cd research/v4
python kaggle_v5_run.py
```

On a no-GPU host this is the honest path: CPU phases measure for real, GPU
phases are staged, and the verdict is `TARGET_NOT_REACHED`. It still writes all
artifacts (`BASELINE_cpu.csv`, `SCALING_V5.csv`, `KAGGLE_V5_FINAL_REPORT.md`,
…), which is how a CPU-only machine reproduces the *format* of every deliverable
without fabricating GPU numbers.

## 6. Reproduce the T4x2 result (the real target)

On a **Kaggle GPU T4 x2** session (or any dual-T4 Linux box) running the same
commands:

```bash
cd research/v4
python kaggle_v5_run.py
```

The pipeline gates on `nvidia-smi` naming two T4s and on the CUDA selftest
before it measures anything, then produces the real `T4_SINGLE.csv`,
`T4_DUAL.csv`, `BATCH_RESULTS.csv`, `AUTOTUNE_V5.csv`, `VERIFICATION_RESULTS.csv`
and a `KAGGLE_V5_FINAL_REPORT.md` with verified solves.

## Reproducibility notes

- **Seeded**: `challenge70.py` maps `seed = base_seed + i` → `k`; the sealed
  `challenges.json` reproduces identically. Hash function: SHA-256.
- **Deterministic walk seeds**: engine jump seeds derive from a fixed constant
  scaled per instance, so walk behavior is deterministic per challenge.
- **Timing is machine-dependent** by nature; steps are the comparable quantity.
- Percent-sign and byte-order are consistent on Windows/Linux (little-endian
  x86-64 / vs builds).