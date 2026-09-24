# BUILD_REPORT — ULTRA-ECDLP-LAB

## What was built, where, and with what

| target | builder | machine | result |
| --- | --- | --- | --- |
| `research/v4/v4_cpu_engine` | `python build.py cpu` | prep host (MinGW g++ 16.1.0) | ✅ compiled |
| `research/v4/v4_cpu_engine` | `python build.py cpu` | **fresh clean clone** (no files copied) | ✅ compiled |
| `micro_O2/O3/Ofast/native` | `python build.py micro` | prep host | ✅ compiled ×4 |
| `tools/cpuid_probe` | `python build.py tools` | prep host | ✅ compiled |
| `research/v4/kangaroo_cuda` | `python build.py cuda` | — | ⛔ **BLOCKED — nvcc not found** |

`build.py` refuses to report a C/C++ build as done unless the compiler exists,
and refuses the CUDA build entirely when `nvcc` is missing.

## Compiler warnings

- C++17 targets: none observed with these flags.
- `tools/cpuid_probe.c`: a stale `-std=c++17` leaked into the `gcc` invocation in
  an earlier revision (warning only) — fixed in `build.py` (`-std=c11` now used
  for the C tool); rebuilt warning-free.

## CUDA status (honest)

The prep host has **no `nvcc`, no `nvidia-smi`, no CUDA runtime**. Therefore:

> **GPU VALIDATION BLOCKED — HARDWARE UNAVAILABLE**

The CUDA source is audit-consistent with the validated CPU engine
(`research/v4/V5_AUDIT.md`: identical `jpInf`/point-op semantics, matched DP
convention, re-verified Montgomery-trick batch inversion, concurrent per-device
round workers). It still must be compiled and selftested **on a T4 (sm_75) host**
before any GPU number is claimed. The documented command:

```bash
nvcc -O3 -std=c++17 -arch=sm_75 -Xptxas -O3 -lineinfo -maxrregcount=80 \
     -Xcompiler -pthread -o kangaroo_cuda kangaroo_cuda.cu
```

If a linker error about missing pthread symbols appears on older glibc, the
`-Xcompiler -pthread` flag (already included) covers the `std::thread` host
workers; on glibc ≥ 2.34 it is unnecessary.

## Reproducibility

- Seeded challenge data reproduces exactly (`SHA256(seed)` → `k`, bit-forced
  interval; `challenges.json` sealed and committed).
- Flag sets, compiler expectations, and versions are in `BUILD.md` and
  `ENVIRONMENT.md`.
- Timing is inherently machine-dependent; step counts are the comparable metric.