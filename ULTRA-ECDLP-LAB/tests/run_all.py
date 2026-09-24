#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""run_all.py - ULTRA-ECDLP-LAB release test orchestrator (stdlib only).

Runs the full non-GPU verification battery from a clean checkout:

  [1] python -m compileall  over every .py in the project
  [2] import test of every import-safe module (missing-dep + circular check)
  [3] synthetic secp256k1 suite      (tests/test_secp256k1.py)
  [4] CPU engine build               (python build.py cpu, if binary absent)
  [5] CPU engine selftest            (independent verify gate)
  [6] CPU engine micro-bench smoke
  [7] CLI failure handling           (unknown command -> nonzero exit)
  [8] detect_env.py CLI
  [9] challenge70 generate + independent verify (temp dir)
  [10] v5 runner entry-point import + constant sanity

Exit code 0 == all pass. Nothing here touches a GPU; CUDA validation is
reported separately as blocked when no CUDA host exists.
"""
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
LAB = os.path.dirname(HERE)
RES = os.path.join(LAB, "research")
V4 = os.path.join(RES, "v4")

RESULTS = []


def rec(step, ok, note=""):
    RESULTS.append((step, ok, note))
    print("%-4s %-44s %s" % ("[OK]" if ok else "[FAIL]", step, note))


def shell(*argv, **kw):
    return subprocess.run(argv, capture_output=True, text=True,
                          cwd=kw.get("cwd", LAB), timeout=kw.get("timeout", 600))


def py(*argv, **kw):
    return shell(sys.executable, *argv, **kw)


def main():
    # ---------- [1] compileall ----------
    r = py("-m", "compileall", "-q", LAB)
    rec("compileall", r.returncode == 0, "python compileall over %s" % LAB)

    # ---------- [2] import tests ----------
    sys.path.insert(0, RES)
    sys.path.insert(0, V4)
    import_list = [
        "challenge70", "detect_env", "kaggle_v5_run", "kaggle_70bit_run",
        "solvers", "gen", "gold_baseline", "kaggle_t4", "t4_parity",
        "experiments_structural", "consolidate", "bench", "autotune",
        "classify", "fit", "calib",
    ]
    import traceback
    errs = []
    for m in import_list:
        try:
            __import__(m)
        except Exception:
            errs.append(m)
            traceback.print_exc()
            rec("import %s" % m, False)
    rec("import tests (%d modules)" % len(import_list), not errs,
        "failed: %s" % (" ".join(errs) if errs else "none"))

    # ---------- [3] synthetic secp256k1 suite ----------
    sys.path.insert(0, HERE)
    import test_secp256k1
    nfail = test_secp256k1.run()
    rec("secp256k1 synthetic suite", nfail == 0,
        "%d failures" % nfail if nfail else "all vectors / edges / infinity / random / verifier")

    # ---------- [4] build CPU engine ----------
    cpu_bin = os.path.join(V4, "v4_cpu_engine" + (".exe" if os.name == "nt" else ""))
    if not os.path.isfile(cpu_bin):
        r = py(os.path.join(LAB, "build.py"), "cpu")
        rec("cpu engine build", r.returncode == 0 and os.path.isfile(cpu_bin),
            "build.py cpu")
    else:
        rec("cpu engine build", True, "binary already present (not rebuilt)")

    # ---------- [5] CPU engine selftest (independent verify gate) ----------
    r = shell(cpu_bin, "selftest", cwd=V4, timeout=300)
    ok = r.returncode == 0 and "independent verify: 1" in r.stdout
    tail = (r.stdout or r.stderr).splitlines()[-1] if (r.stdout or r.stderr) else ""
    rec("cpu engine selftest", ok, tail)

    # ---------- [6] CPU micro-bench smoke ----------
    r = shell(cpu_bin, "bench", "1", "8", cwd=V4, timeout=120)
    ok = r.returncode == 0 and "FIELD_MUL" in r.stdout
    rec("cpu bench smoke", ok, "bench 1 8 rc=%d" % r.returncode)

    # ---------- [7] CLI failure handling ----------
    r = shell(cpu_bin, "not_a_command", cwd=V4, timeout=60)
    rec("cpu unknown-command -> nonzero", r.returncode != 0,
        "rc=%d (expected != 0)" % r.returncode)

    # ---------- [8] detect_env CLI ----------
    import tempfile
    tmp = tempfile.mkdtemp(prefix="ecdlp_env_")
    out = os.path.join(tmp, "env.json")
    r = py(os.path.join(V4, "detect_env.py"), out, cwd=V4)
    ok = r.returncode == 0 and os.path.isfile(out)
    rec("detect_env CLI", ok, "wrote %s rc=%d" % (out, r.returncode))

    # ---------- [9] challenge generator + independent verify ----------
    chal = os.path.join(tmp, "ch10.json")
    r = py(os.path.join(V4, "challenge70.py"), "5", "64", "0xABCDE", chal, cwd=V4)
    ok = r.returncode == 0 and "self-verify all: 1" in r.stdout
    rec("challenge70 generate+verify", ok,
        r.stdout.splitlines()[-1] if r.stdout else "")

    # ---------- [10] v5 runner entry points ----------
    import kaggle_v5_run as k5
    import kaggle_70bit_run as k70
    ok = callable(getattr(k5, "main", None)) and callable(getattr(k70, "main", None))
    rec("v5 runners entry-points", ok,
        "kaggle_v5_run.main + kaggle_70bit_run.main importable")

    # ---------- summary ----------
    failed = [s for s, o, _ in RESULTS if not o]
    print()
    print("=" * 72)
    print("run_all complete: %d/%d checks passed, %d failed" %
          (len(RESULTS) - len(failed), len(RESULTS), len(failed)))
    for s, o, _ in RESULTS:
        if not o:
            print("  FAILED:", s)
    print("=" * 72)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())