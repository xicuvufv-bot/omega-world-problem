# DEPENDENCY_REPORT — ULTRA-ECDLP-LAB

Every dependency below was **actually exercised** on the prep host (imports run,
binaries compiled) or is explicitly marked blocked. Nothing is invented.

## Python

| package | grade | where used | verified |
| --- | --- | --- | --- |
| (stdlib) | required | the whole `research/v4/` pipeline: `challenge70`, `detect_env`, `kaggle_v5_run`, `kaggle_70bit_run`, `tests/` | import + runtime (yes) |
| `numpy` | optional | `research/` scripts (`gen`, `bench`, `fit`, `kaggle_t4`, …) | import (yes, 2.4.6) |
| `cupy` | Kaggle-only, optional | `research/kaggle_t4.py` GPU path | import guarded (`try/except`); absent locally → GPU path not run |

`requirements.txt` lists only `numpy>=1.24`; cupy is documented, not forced
(Kaggle NVIDIA runtimes ship it, and the guard keeps CPU hosts importable).

## C / C++ (verified by clean-clone build)

| compiler | flags | target | status |
| --- | --- | --- | --- |
| `g++` (MinGW 16.1.0 here; any C++17 g++/clang) | `-O3 -march=native -std=c++17 -pthread` | `research/v4/v4_cpu_engine` | built in workspace + clean clone |
| `g++` | `-O2/-O3/-Ofast/-O3 -march=native`, `-std=c++17` | `micro_O2/O3/Ofast/native` | built (yes) |
| `gcc` | `-O2 -std=c11` | `tools/cpuid_probe` | built (yes) |

## CUDA (NOT locally verifiable)

| component | required | status on prep host |
| --- | --- | --- |
| `nvcc` (CUDA toolkit) | build `kangaroo_cuda`, sm_75 (`-arch=sm_75`) | **absent → GPU VALIDATION BLOCKED** |
| CUDA runtime / driver | run CUDA payload | absent |
| 2 x NVIDIA T4 | target hardware | absent |

The CUDA source is audited against the CPU engine (`V5_AUDIT.md`: identical
`jpInf`, point ops, DP convention; concurrent dual-device worker threads) but it
is **not compiled or run here** — the first successful `nvcc` build and selftest
must happen on a real CUDA host.

## OS / toolchain requirements

- **CPU path**: any OS with a C++17 compiler + Python 3.9+. No environment
  variables required.
- **GPU path**: Linux (or Windows with CUDA toolchain); NVIDIA driver + CUDA
  ≥ 11.x with sm_75 support. Kaggle Ubuntu T4x2 satisfies this.
- `make`, CMake, shell scripts, Jupyter: **not required**. `build.py` and the
  Python pipeline are the only build/test drivers.

## Environment variables

None required. Optional: `GXX` (override g++ path in `run_microbench.bat`).