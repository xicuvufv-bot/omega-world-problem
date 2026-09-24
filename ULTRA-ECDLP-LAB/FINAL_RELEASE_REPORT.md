# FINAL_RELEASE_REPORT — ULTRA-ECDLP-LAB

Prepared at the completion of the release audit (clean-checkout verification
attached). Everything here is what actually happened on the prep host and in a
fresh clone — nothing invented.

## Release checklist (Phase 18)

| question | answer |
| --- | --- |
| Repository complete? | **YES** (169 tracked files; 0 untracked-non-ignored) |
| Clean clone builds? | **YES** — CPU engine, micro corpus, tools built from clone |
| Tests pass? | **YES** — `tests/run_all.py` 10/10 in workspace and in clean clone |
| Synthetic verification pass? | **YES** — `Q == kG` via independent verifier on all 10 sealed instances + CPU engine selftest |
| CUDA source consistent? | **YES by audit** (matches CPU engine semantics; `V5_AUDIT.md`) — **compile blocked here** |
| Kaggle runner present? | **YES** — `kaggle_onboard.sh` + `kaggle_v5_run.py` + gated docs |
| Hidden local dependencies? | **NO** — `probe_pc.py` & `run_microbench.bat` absolute paths fixed; imports all stdlib/numpy/guarded-cupy |
| Untracked required files? | **NO** — 0; runtime inputs (`challenges.json`, sources, tests) all tracked |
| Hard-coded local paths? | **NO** — post-fix sweep clean in code |
| Reproducible instructions? | **YES** — `ENVIRONMENT.md`, `BUILD.md`, `REPRODUCTION.md` |

## Clean-clone final standard (Phase 20) — evidence

Clone created with `git clone` into a fresh temp directory (no files copied):

```
git clone <repo> %TEMP%\ecdlp_cleanclone
cd ULTRA-ECDLP-LAB
python build.py cpu                          # -> compiles v4_cpu_engine in-clone   [OK]
python tests/run_all.py                       # 10/10                               [OK]
cd research/v4 && python kaggle_v5_run.py     # full pipeline, CPU path, honest      [OK]
  -> TARGET_NOT_REACHED, BASELINE_cpu.csv measured, SCALING_V5.csv (19 pts,
     alpha=0.0595 R2=0.99), KAGGLE_V5_FINAL_REPORT.md written
```

No JSON/source from the author's machine was consulted by any of it.

## GPU validation status (Phase 15 — not faked)

- Prep host: no `nvcc`, no `nvidia-smi`, no CUDA driver → CUDA cannot compile
  here.
- Statement: **GPU VALIDATION BLOCKED — HARDWARE UNAVAILABLE**.
- What this means precisely: `kangaroo_cuda.cu` (sm_75) remains to be compiled
  and selftested on a real T4 host; until that happens **no GPU performance
  number exists** in this release. `T4_SINGLE.csv` / `T4_DUAL.csv` carry
  `staged=1`; reports mark them as staged, not measured.
- The first GPU run is scripted and gated (`kaggle_onboard.sh` on Kaggle T4x2).

## Known limitations (documented, by design)

- `walkKernelSimple` in `kangaroo_cuda.cu` is dead code (pre/post-jump DP
  convention mismatch with the batch kernel); flagged in `V5_AUDIT.md`, do not
  enable without re-audit.
- `kaggle_70bit_run.py` is superseded by `kaggle_v5_run.py` but kept (reference).
- `kaggle_t4.ipynb` is historical v1 notebook (kept for provenance).

## Truth statement

This release contains exactly two kinds of numbers: **measured** (labelled with
the machine that measured them) and **staged/blocked** (labelled staged). No
projected GPU figure is presented as measured. All ECDLP is synthetic.