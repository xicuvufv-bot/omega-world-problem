# ENVIRONMENT — ULTRA-ECDLP-LAB

Recorded automatically by `research/v4/detect_env.py` into
`KAGGLE_ENVIRONMENT.json` on every run. This file documents the exact toolchain
and the machines involved.

## Reference toolchain (this repository's preparation host)

| component | value | role |
| --- | --- | --- |
| OS | Windows (win32) | dev host |
| Python | 3.11.9 | runs all `.py` (pipeline is stdlib-only; numpy optional) |
| gcc / g++ | 16.1.0 (MinGW-w64) | builds `v4_cpu_engine`, microbench corpus, `tools/cpuid_probe` |
| make | absent | not required; `build.py` drives all builds |
| git | present | version control |
| numpy | 2.4.6 | optional research dependency (not needed by the v4 pipeline) |
| ffmpeg | present | media only (unrelated) |

## GPU / CUDA availability

| component | status on prep host | required for |
| --- | --- | --- |
| nvidia-smi | **absent** | any GPU measurement |
| nvcc | **absent** | building `kangaroo_cuda` |
| CUDA runtime / driver | **absent** | running CUDA payload |
| cupy | **absent** | `research/kaggle_t4.py` GPU path (guarded import) |

⇒ **GPU VALIDATION BLOCKED — HARDWARE UNAVAILABLE** on the prep host. No GPU
number in this repository was produced here; `T4_*` rows are `staged=1`.

## Target environment (Kaggle NVIDIA T4x2)

| component | expectation | `detect_env.py` gate |
| --- | --- | --- |
| OS | Ubuntu 22.04+ (glibc ≥ 2.34) | — |
| GPU | 2 x NVIDIA Tesla T4 (sm_75) | `gpu.count==2` and names contain `T4` |
| nvcc | CUDA toolkit (sm_75) | `gpu.nvcc_path` non-null |
| python | 3.10+ | `python` field |
| cupy | preinstalled on Kaggle NVIDIA runtimes | import-guarded, never required |

## Environment variables used

None are required. `build.py` consults no variables. `run_microbench.bat`
honours an optional `GXX` override (default: `g++` from PATH).