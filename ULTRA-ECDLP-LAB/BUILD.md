# BUILD — ULTRA-ECDLP-LAB

One portable driver builds every C/C++/CUDA target:

```bash
python build.py cpu      # research/v4/v4_cpu_engine   (g++, C++17)
python build.py cuda     # research/v4/kangaroo_cuda   (nvcc, sm_75)  <- GPU host only
python build.py micro    # micro_O2/O3/Ofast/native    (g++, C++17)
python build.py tools    # tools/cpuid_probe           (gcc, C11)
python build.py all      # everything available
python build.py clean    # remove build products
```

Paths are resolved relative to `build.py`; it works from any directory and from
a fresh `git clone`. Output is a single native binary next to each source.

## Exact flags

| target | compiler | flags |
| --- | --- | --- |
| CPU engine | `g++` | `-O3 -march=native -std=c++17 -pthread` |
| CUDA payload | `nvcc` | `-O3 -std=c++17 -arch=sm_75 -Xptxas -O3 -lineinfo -maxrregcount=80 -Xcompiler -pthread` |
| micro (4 variants) | `g++` | `-O2` / `-O3` / `-Ofast` / `-O3 -march=native` (+ `-std=c++17`) |
| cpuid tool | `gcc` | `-O2 -std=c11` |

`-arch=sm_75` matches the Kaggle T4. `-Xcompiler -pthread` covers the
`std::thread` host workers used by the dual-GPU concurrent round loop on
toolchains where it is required (harmless where it is not).

## Version requirement

- **C++17** compiler (g++ 9+; tested with MinGW g++ 16.1.0; any Linux g++/clang
  works for the CPU path).
- **gcc** for `cpuid_probe.c`.
- **nvcc 11.x+** (sm_75) for the CUDA payload; only available on an NVIDIA host.
- **Python 3.9+** for every `.py`; nothing beyond the standard library is
  needed for the core, `numpy` optional for `research/` scripts.

## On Kaggle

`kaggle_v5_run.py` performs its own build (`phase2_build`) with these exact
flags, so `build.py` is optional there — it exists for standalone rebuilds and
for the release test suite.

See `BUILD_REPORT.md` for what was actually built where, and `REPRODUCTION.md`
for the from-scratch procedure.