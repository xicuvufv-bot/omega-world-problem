# ULTRA-ECDLP-LAB research/v4 — V4/V5 mission payload

Synthetic 70-bit interval ECDLP on secp256k1, engineered for **Kaggle T4x2
(sm_75)**. All secrets synthetic; every solve re-verified with `k·G == Q`.

## Files

| file | purpose |
| --- | --- |
| `kaggle_v5_run.py` | 28-phase gated pipeline: env → build → selftest gate → bench → prof → T4 single → T4 dual → batch → autotune → probes → 10 solves → stats → verdict → reproduction → scaling → leak test → speedups → report. |
| `kaggle_70bit_run.py` | earlier v2 pipeline (kept for reference; v5 supersedes it). |
| `detect_env.py` | real probe → `KAGGLE_ENVIRONMENT.json`. Never fabricates GPU data. |
| `challenge70.py` | deterministic synthetic generator + independent `verify_instance`. |
| `challenges.json` | sealed 10x70-bit instances (index/seed/k/Qx/Qy), synthetic. |
| `v4_cpu_engine.cpp` | CPU reference engine: `selftest`, `bench`, `scale`, `solve`. |
| `kangaroo_cuda.cu` | CUDA payload: `selftest`, `bench`, `scale`, `solve`, `prof`. |
| `.csv` artifacts | anti-fabrication audit trail from runs on real hardware. |

## CLI cheat-sheet

```bash
# CPU reference engine (built by `python ../../build.py cpu`):
./v4_cpu_engine selftest          # k-match + (n-1)G+G + 2G jDbl + distributivity + 32-bit solve + independent verify
./v4_cpu_engine bench 5 24        # field/point op timings
./v4_cpu_engine scale 16 40 3 16  # step-scaling curve (lo hi rep dpbits)
./v4_cpu_engine solve challenges.json <i> out.json <dpb> <nt> <nw> [gpus]

# CUDA payload (only builds where nvcc exists):
./kangaroo_cuda build             # self check on GPU host
./kangaroo_cuda selftest
./kangaroo_cuda bench 5 30 20 2
./kangaroo_cuda scale 16 40 3 16 2
./kangaroo_cuda solve challenges.json 0 out.json 20 22 22 2
./kangaroo_cuda prof 30 20 2      # h2d / kernel / d2h / merge timer split
```

`solve <nw>` is the **power-of-2 exponent** (nStart = 2^nw walkers per device).

## Kaggle T4x2 launch

1. Upload this repository (or `git clone` it inside a Kaggle notebook session).
2. Runtime: **GPU T4 x2**, Python 3.10+.
3. Terminal or first cell:
   ```bash
   cd ULTRA-ECDLP-LAB/research/v4
   python detect_env.py          # must show gpu.count == 2, names contain "T4"
   python kaggle_v5_run.py       # hard-gates before any GPU measurement
   ```
4. Success = `KAGGLE_V5_FINAL_REPORT.md` shows `solution_verified == true` for
   the 10 instances with `wall_time <= 1200 s` each, plus all companion CSVs.

If the environment lacks two T4s the pipeline says so and stages honestly —
it never invents numbers.

## Notes

- Step count means **walker jumps** (not point-ops). DP predicate is
  representation-independent; batching uses warp-wide Montgomery-trick
  inversion. Dual-GPU rounds are run with concurrent per-device worker
  threads so the second GPU is not idle.
- `walkKernelSimple` is dead code (pre-jump vs post-jump DP convention mismatch
  with the batch kernel); do not enable without auditing the DP convention.