"""EXP-N2: v6 (GLV x negation, quotient W/6)vs v5 vs v4 -- correctness gate + K.

Rules for the evidence to be reported as a REAL result:
  1. CORRECTNESS GATE first: w in {16,20,24}, 12 seeds each, ALL solvers must
     recover the exact key.  A solver's returned k is accepted ONLY if it
     is independently re-verified through TWO channels:
        (a) point_equal_jac(scalar_mult(k), target)   [linear-algebra identity]
        (b) native secp256k1 engine: privkey_to_pubkey(k) == target pubkey
            bytes (independent C implementation of the same curve math).
     Zero tolerance for LookupError in the reported block.
  2. Only after the gate passes do we report K statistics (ops/sqrt(W)).
  3. Every trial's full settings land in the JSON log:
        width(s), seeds, solvers, K per run, wall seconds, hops, passes,
        verdict, raw candidate counts.

Run:  python SOLVER_LAB/benchmarks/bench_v6.py
Out:  SOLVER_LAB/reports/exp_n2_results.json  (every trial, machine-readable)
      + stdout table (human).
"""
import importlib.util
import json
import math
import multiprocessing as mp
import os
import random
import sys
import time

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

LAB = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, LAB)
os.chdir(LAB)

from algorithms.curve import scalar_mult, compressed, point_equal_jac
from solvers.v4_kangaroo import KangarooSolver

# load v5, v6 by path (kept out of the importable tree on purpose)
def _load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

_V5 = _load(os.path.join(LAB, "SOLVER_LAB", "candidate", "v5_fused_negation.py"), "v5_fused_negation")
_V6 = _load(os.path.join(LAB, "SOLVER_LAB", "candidate", "v6_glv_negation.py"), "v6_glv_negation")

SOLVERS = {"v4": KangarooSolver, "v5": _V5.FusedNegationSolver, "v6": _V6.GlvFusedNegationSolver}

# native engine (independent C reference for key verification)
from production.native import secp256k1_ffi as _eng

REPORT = os.path.join(LAB, "SOLVER_LAB", "reports", "exp_n2_results.json")


def native_pubkey(k):
    return _eng.privkey_to_pubkey(k.to_bytes(32, "big"))


def verify_twice(k, target, target_compressed):
    """Both channels must confirm k == target."""
    if not (0 < k and point_equal_jac(scalar_mult(k), target)):
        return False
    return native_pubkey(k) == target_compressed


def run_one(width_bits, solver_name, seed, max_seconds):
    lo = 1 << (width_bits - 1)
    hi = (1 << width_bits) - 1
    rng = random.Random(seed * 1000 + width_bits)
    key = rng.randint(lo, hi)
    target = scalar_mult(key)
    target_compressed = compressed(target)
    t0 = time.perf_counter()
    try:
        if solver_name == "v4":
            s = SOLVERS[solver_name](lo, hi, max_seconds=max_seconds, seed=seed)
            k = s.solve(target)
        else:
            s = SOLVERS[solver_name](lo, hi, seed=seed)
            k = s.solve(target, max_seconds=max_seconds)
        wall = time.perf_counter() - t0
        ok = verify_twice(k, target, target_compressed) and k == key
    except LookupError:
        wall = time.perf_counter() - t0
        ok = False
        k = None
    stats = dict(s.stats) if hasattr(s, "stats") else {}
    return {
        "width_bits": width_bits, "solver": solver_name, "seed": seed,
        "key_hex": format(key, "x"), "recovered": None if k is None else format(k, "x"),
        "ok": ok, "wall_s": round(wall, 4), "timed_out": stats.get("timeout", False),
        "hops": stats.get("hops", 0), "passes": stats.get("passes", 0),
        "tame_trail": stats.get("tame_trail", 0), "edge": stats.get("edge", ""),
    }


def main():
    t_start = time.perf_counter()
    gate_widths = (16, 20, 24)
    k_widths = (20, 24, 28)
    seeds = list(range(1, 13))
    cap = {16: 120, 20: 120, 24: 240, 28: 300}
    pool = mp.Pool(processes=min(4, os.cpu_count() or 1))
    log = {"meta": {"experiment": "EXP-N2", "date": time.strftime("%Y-%m-%d %H:%M:%S"),
                    "solver_V6": "fused + GLV(3) x negation, quotient W/6",
                    "beta": hex(_V6.BETA), "lambda": hex(_V6.LAMBDA),
                    "verification": "scalar_mult identity + native secp256k1 FFI",
                    "processes": pool._processes}, "trials": []}

    def submit(w, solvers, seed):
        return pool.apply_async(run_one, (w, solvers, seed, cap[w]))

    # ---- GATE --------------------------------------------------------------
    print("=== GATE: correctness (all widths x 12 seeds, all solvers) ===")
    jobs = [submit(w, n, seed) for w in gate_widths
            for n in SOLVERS for seed in seeds]
    gate_rows = [j.get() for j in jobs]
    log["trials"] += gate_rows
    gate_fail = [r for r in gate_rows if not r["ok"]]
    for w in gate_widths:
        for n in SOLVERS:
            rs = [r for r in gate_rows if r["width_bits"] == w and r["solver"] == n]
            fails = [r for r in rs if not r["ok"]]
            print(f"  w={w} {n}: {len(rs)-len(fails)}/{len(rs)} ok")
    if gate_fail:
        print(f"GATE FAILED: {len(gate_fail)} bad trials -> NOT reporting K.")
        log["meta"]["gate"] = "FAILED"
    else:
        log["meta"]["gate"] = "PASSED"
        print("GATE PASSED: every recovered key verified via scalar-mult AND native FFI.")

    # ---- K statistics (only if gate passed) --------------------------------
    if log["meta"]["gate"] == "PASSED":
        print("\n=== K statistics (ops/sqrt(W); 12 seeds per block) ===")
        for w in k_widths:
            for n in SOLVERS:
                jobs = [submit(w, n, seed) for seed in seeds]
                rs = [j.get() for j in jobs]
                log["trials"] += rs
                okrs = [r for r in rs if r["ok"]]
                if not okrs:
                    print(f"  w={w} {n}: NO SOLVES")
                    continue
                Ks = [(r["tame_trail"] + r["hops"]) / math.sqrt(float(1 << (w-1)))
                      for r in okrs]
                mean, mn, mx = sum(Ks)/len(Ks), min(Ks), max(Ks)
                wall = [r["wall_s"] for r in okrs]
                print(f"  w={w} {n}: mean K={mean:.3f} min={mn:.3f} max={mx:.3f} "
                      f"solves={len(okrs)} wall_med={sorted(wall)[len(wall)//2]:.2f}s")

    pool.close()
    pool.join()
    log["meta"]["wall_total_s"] = round(time.perf_counter() - t_start, 2)
    with open(REPORT, "w", encoding="utf-8") as fh:
        json.dump(log, fh, indent=2)
    print(f"\nlog -> {REPORT}  (total {time.perf_counter()-t_start:.1f}s)")


if __name__ == "__main__":
    main()