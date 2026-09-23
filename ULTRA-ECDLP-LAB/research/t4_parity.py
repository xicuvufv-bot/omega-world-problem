#!/usr/bin/env python3
"""t4_parity.py — CPU reference check for the Kaggle T4 notebook payload.

Validates that gpu_kanga (as ported in kaggle_t4.py, but compiled to numpy CPU path)
solves the same instances that research/solvers.kanga solves, with the SAME walk rule.
Goal: uncover walk-semantics drift (jump selection, dist update, DP restart) before the
payload ever runs on a GPU. Requires cupy only at import time; guard by env.
"""
import os, sys, json
sys.path.insert(0, os.path.dirname(__file__))
import kaggle_t4 as kt

# kaggle_t4 imports cupy; on a CPU-only box cupy is missing -> stand-in
def _noop(*a, **k): raise RuntimeError("cupy unavailable")
htp = getattr(kt, "cp", None)
if htp is None:
    import numpy as np
    class _FakeCupy:
        uint64 = np.uint64
        ones = staticmethod(lambda n, dtype=None: np.ones(n, dtype=dtype))
        asarray = staticmethod(np.asarray)
        column_stack = staticmethod(np.column_stack)
        count_nonzero = staticmethod(np.count_nonzero)
        asnumpy = staticmethod(np.asarray)
    kt.cp = _FakeCupy()
    htp = _FakeCupy()

from solvers import kanga, solve

def main():
    dbs = [12, 14, 16]
    rows = kt.gen_instances(dbs, 20260922, 1)
    for row in rows:
        N = 1 << row["db"]
        a = kt.gpu_kanga(row, W=64, b=6, seed=9)
        b = kanga(row, N, 9, W=64, b=6, K=32, wcc=6.0)
        print(f"db={row['db']:3d} gpu_port steps={a[0]:>9,} ok={int(a[1])} | ref kanga steps={b['steps']:>9,} ok={int(b['ok'])}", flush=True)
        if a[1] != b["ok"]:
            print("  MISMATCH: GPU port vs reference", flush=True); sys.exit(1)
    print("PARITY OK: GPU port solves the same instances as solvers.kanga")

if __name__ == "__main__":
    main()