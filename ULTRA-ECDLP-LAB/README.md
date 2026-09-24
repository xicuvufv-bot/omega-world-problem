# ULTRA-ECDLP-LAB

Synthetic ECDLP (Elliptic Curve Discrete Logarithm) research and an interval
kangaroo solver, engineered for NVIDIA T4 GPUs on Kaggle. **Everything in this
repository is synthetic-only**: generated secrets, generated challenges, no real
Bitcoin keys, no real puzzles.

## Honesty contract

- Every measurement artifact in this repo is either **measured at runtime** on
  the machine that produced it or **explicitly staged** (e.g. the no-GPU host's
  `T4_*` rows carry `staged=1`).
- GPU numbers are only ever produced on a real CUDA host. This repository makes
  **no GPU claims** from a machine without one.
- All ECDLP tests are synthetic. The independent verifier checks `Q == k·G`
  with `k` inside the documented interval for every instance.

## Layout

```
ULTRA-ECDLP-LAB/
  src/                v1-v2 native microbench corpus (fp/ec/perf kernels, C++17)
  research/           v3 research corpus (solvers, hypothesis lab, reports)
  research/v4/        V4/V5 mission payload  <-- PRIMARY RELEASE ENTRY POINT
    kaggle_v5_run.py      28-phase gated pipeline (env -> build -> test -> reports)
    detect_env.py         real environment probe -> KAGGLE_ENVIRONMENT.json
    challenge70.py        synthetic 70-bit challenge generator + independent verifier
    challenges.json       sealed synthetic instances (10x 70-bit interval)
    v4_cpu_engine.cpp     validated CPU reference engine (selftest/bench/scale/solve)
    kangaroo_cuda.cu      CUDA payload (dual-T4, sm_75, concurrent device workers)
  tests/              synthetic correctness + entry-point suite (stdlib only)
  build.py            portable build driver (cpu / cuda / micro / tools / all / clean)
  requirements.txt    Python deps (numpy; core pipeline is pure stdlib)
  REPOSITORY_AUDIT.md      release audit
  GIT_COMPLETENESS_REPORT.md
  DEPENDENCY_REPORT.md
  PORTABILITY_REPORT.md
  BUILD_REPORT.md
  TEST_REPORT.md
  KAGGLE_READINESS.md
  ENVIRONMENT.md     BUILD.md     REPRODUCTION.md
  FINAL_RELEASE_REPORT.md
```

## Quick start (CPU / any machine)

```
python research/v4/detect_env.py            # record this host's real environment
python build.py cpu                          # g++ build of the reference engine
python tests/run_all.py                      # 10/10 synthetic + entry-point checks
```

## Quick start (Kaggle, NVIDIA T4x2)

```
# clone the repo, then in a terminal / Jupyter cell:
cd ULTRA-ECDLP-LAB/research/v4
python detect_env.py                          # confirms T4x2 before anything else
python kaggle_v5_run.py                       # gates, builds, selftests, measures, reports
```

`kaggle_v5_run.py` refuses to claim T4x2 unless `nvidia-smi` actually lists two
T4 devices; on a CUDA host it hard-gates on the CPU selftest before any GPU
phase. See `KAGGLE_READINESS.md` and `research/v4/README.md`.

## GPU validation status

GPU validation is currently **BLOCKED — hardware unavailable** on the machines
where this release was prepared (no `nvcc`, no `nvidia-smi`). The CUDA payload
is consistent with the validated CPU engine (shared semantics: `jpInf`,
`jDbl`/`jAddAff`, DP convention, merged concurrent dual-device rounds), but it
has not been compiled or run here. See `BUILD_REPORT.md`.