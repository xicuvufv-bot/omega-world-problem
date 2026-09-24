# GIT_COMPLETENESS_REPORT — ULTRA-ECDLP-LAB

## Commands executed (release snapshot)

```
git status            # clean for ULTRA-ECDLP-LAB except staged release work
git ls-files          # 169 tracked files (see REPOSITORY_AUDIT.md)
git check-ignore -v   # verified: __pycache__, *.exe, native binaries, _t*, logs
git submodule status  # none
```

## Results

| check | outcome |
| --- | --- |
| untracked, non-ignored files | **0** |
| ignored-but-required files | **0** |
| generated files required at runtime | **0** (all generated artifacts are outputs, never inputs; the only input files are tracked) |
| local-only user assets | **1 removed** — `probe_pc.py` absolute path fixed; `run_microbench.bat` MinGW path fixed |
| absolute paths in code (`C:\Users`, `/home/`, `D:\`) | **0 in code** (only in `KAGGLE_ENVIRONMENT.json`, which is a *generated record*, not a code dependency) |
| Windows-only paths | removed (`run_microbench.bat`, `probe_pc.py`) |
| Linux-only assumptions | none in Python/CPU path; Kaggle path documented in `KAGGLE_READINESS.md` |
| missing imports | 0/16 import-tested modules fail |
| missing system packages | none for CPU path (numpy optional) |
| submodules | none |
| committed binaries buildable from source | yes — all 16 `.exe` untracked; `src/*.cpp`, `research/v4/v4_cpu_engine.cpp`, `tools/cpuid_probe.c`, `.cu` provide recipes (`build.py`) |

## Commit hygiene changes (this release)

- `git rm --cached`: 16 Windows executables + `__pycache__/hypothesis_gen.cpython-311.pyc`.
- `.gitignore` expanded (no longer just `__pycache__/`).
- Working tree has no ignored-but-needed file: the sole native dependency of the
  CPU path (`v4_cpu_engine`) is produced by `python build.py cpu` from tracked
  source.

## Clean-checkout proof

A fresh `git clone` of the repository (no copied files) was built and tested:

- `python build.py cpu` → compiles `v4_cpu_engine` from source **in the clone**.
- `python tests/run_all.py` → **10/10 pass** in the clone.
- `python research/v4/kaggle_v5_run.py` → full pipeline end-to-end in the clone
  (CPU path, honest `TARGET_NOT_REACHED`, all artifacts produced).

Conclusion: **the git repository itself is complete** for the CPU-tested
release; GPU runtime requires the documented CUDA host only.