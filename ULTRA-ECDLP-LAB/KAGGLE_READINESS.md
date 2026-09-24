# KAGGLE_READINESS — ULTRA-ECDLP-LAB

## The clean-room claim

Everything the Kaggle session needs comes from **the git repository + documented
dependencies + synthetic data**. No local project directory, no hidden
credentials, no machine-specific config. The pipeline reads only:

- files next to itself (`research/v4/*`), resolved via `os.path.abspath(__file__)`;
- generated test files written into its own working directory.

## Launch path (T4 x2)

1. **Start a Kaggle Notebook** with runtime **GPU T4 x2**.
2. Get the repo into the session (Git clone or Upload; a Git clone is the
   clean-room form).
3. In a cell / terminal:

   ```bash
   cd <repo>/research/v4
   bash kaggle_onboard.sh        # = detect_env.py + kaggle_v5_run.py
   ```

   or step-by-step:

   ```bash
   python detect_env.py          # MUST show gpu.count==2, names "T4", nvcc present
   python kaggle_v5_run.py       # gated: build -> selftest -> all GPU phases -> report
   ```

4. Read `KAGGLE_V5_FINAL_REPORT.md` + all CSVs.

## Gates that prevent fakery

- `kaggle_v5_run.py` only enters GPU phases when `nvcc` exists **and** the
  `detect_env` GPU probe succeeds; a dual-claim requires `gpu.count==2` with
  `T4` in the device names.
- The selftest gate must pass before any measurement phase runs.
- Every claimed solve is re-verified (`k·G == Q`, independent) before it counts.
- On a non-CUDA host the same pipeline runs honestly: CPU phases measured, GPU
  phases `staged=1`, verdict `TARGET_NOT_REACHED`.

## What T4x2 enables (and is blocked otherwise)

`T4_SINGLE.csv`, `T4_DUAL.csv` (+ parallel efficiency), `prof` kernel timing,
`BATCH_RESULTS.csv`, `AUTOTUNE_V5.csv`, real scaling across bit sizes, and the
10×70-bit solves with `wall_time <= 1200 s` each. **None of these exist yet** —
no GPU was present during this release audit (explicitly: GPU VALIDATION
BLOCKED — HARDWARE UNAVAILABLE). The repository is *prepared*, not *proven on
GPU*.

## Expected runtime on T4x2

Based on the v5 design targets (dual concurrent devices, warp-batched
inversion, DP auto-tune, tiered starts), the pipeline allocates up to ~20 min
for the 10 solves after a ~4 min warm-up of benchmarks/autotune; exact numbers
are produced by the run itself and must not be pre-stated as results.

## Optional dependencies on Kaggle

`numpy` (installed by default) and `cupy` (preinstalled on NVIDIA runtimes,
guarded import) — neither is required by the v5 pipeline itself.