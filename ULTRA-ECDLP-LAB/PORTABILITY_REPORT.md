# PORTABILITY_REPORT — ULTRA-ECDLP-LAB

Rule applied: a clean clone on an unrelated machine must build, test, and run
with nothing from the author's machine.

## Hard-coded / machine-specific items discovered

| item | what was wrong | fix | status |
| --- | --- | --- | --- |
| `research/probe_pc.py:3` | `exec(open(r"C:\Users\Administrator\Documents\Default Project\ULTRA-ECDLP-LAB\research\prime_scaling_run.py" ...))` — absolute path + machine username | `__file__`-relative resolution | fixed, committed |
| `run_microbench.bat` | `set L=c:\ProgramData\mingw64\mingw64\bin` then `"%L%\g++.exe"` — machine-specific MinGW path | `g++` from PATH with optional `GXX` override | fixed, committed |
| 16 tracked `.exe` | Windows binaries committed to git | untracked; rebuildable via `build.py` (recipes in `BUILD.md`) | fixed, committed |
| `research/lab/__pycache__/*.pyc` | committed bytecode | untracked + ignored | fixed, committed |
| `KAGGLE_ENVIRONMENT.json` | records absolute `python_path`, `cwd`, host | **kept as-is**: it is a *generated audit record* (`detect_env.py`), not a code dependency; it is honest by design and regenerated per host | documented |
| `calib.py` | top-level solve-loop executed on `import` (side effect) | moved under `if __name__ == "__main__":` | fixed, committed |

## Post-fix sweep

```
grep (case-insensitive) for  C:\Users | /home/ | D:\ | C:/Users  in
*.py *.cu *.cpp *.hpp *.c *.h *.bat *.md *.json  ->  0 hits in code.
```

The only remaining occurrence is inside `KAGGLE_ENVIRONMENT.json` (data record —
see above) and `research/v4/KAGGLE_ENVIRONMENT.json` (same artifact).

## Windows ⇄ Linux / Kaggle

- All Python paths are `os.path.abspath(__file__)`-relative (`HERE` pattern) in
  `kaggle_v5_run.py` / `kaggle_70bit_run.py`; binary suffix selected by
  `os.name` (`v4_cpu_engine` vs `v4_cpu_engine.exe`).
- `build.py` picks `.exe` by `os.name`; compiler discovery via `shutil.which`.
- `challenge70.py`, `detect_env.py`, `tests/` are pure stdlib and platform-blind.
- The CUDA payload is Linux/Kaggle-targeted (sm_75, `std::thread` host workers,
  no Windows-only calls).

## Verified from an unrelated location

A fresh `git clone` placed under `%TEMP%\opencode` (a different directory tree,
no copied files) built the CPU engine and passed the whole battery — 10/10 —
plus a full pipeline run. See `TEST_REPORT.md`.