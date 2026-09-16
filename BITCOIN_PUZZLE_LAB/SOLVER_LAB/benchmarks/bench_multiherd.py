"""EXP-N3: multi-herd parallel kangaroo wall- and work-scaling on the best
proven solver (v5 fused+negation).

Motivation (measured in EXP-N2): the automorphism-quotient (GLV*neg, v6)
does NOT reduce the meeting space for bounded additive kangaroo -- none of
the +- / +-LAMBDA^i candidates ever fired, so the class-6 store reduces to
raw-scalar identity and v5 remains the best constant (mean K ~4.2 @ w=20,
~5.0 @ w=24 vs v4 ~5.99).  The remaining wall-clock lever is the classic
van Oorschot--Wiener parallelization: ONE tame trail, MANY independent wild
herds, all querying the SAME store in parallel.  Measured here: wall and
total-op scaling for 1/2/4 workers at w=28 over 12 seeds.

Correctness gate: every recovered key re-verified via scalar-mult AND the
independent native secp256k1 FFI (zero tolerance).  Wall is measured to the
FIRST completed herd (a worker never wastes time after the hit), each herd
uses its own independent pass stream.

Run:  python SOLVER_LAB/benchmarks/bench_multiherd.py
Out:  SOLVER_LAB/reports/exp_n3_results.json
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

from algorithms.curve import (scalar_mult, to_affine, jac_add_affine,
                              point_equal_jac, compressed, N)

_V5_SPEC = importlib.util.spec_from_file_location(
    "v5_fused_negation", os.path.join(LAB, "SOLVER_LAB", "candidate", "v5_fused_negation.py"))
_V5 = importlib.util.module_from_spec(_V5_SPEC)
_V5_SPEC.loader.exec_module(_V5)

from production.native import secp256k1_ffi as _eng

REPORT = os.path.join(LAB, "SOLVER_LAB", "reports", "exp_n3_results.json")


def native_pubkey(k):
    return _eng.privkey_to_pubkey(k.to_bytes(32, "big"))


def build_trail(lo, hi, seed=1):
    s = _V5.FusedNegationSolver(lo, hi, seed=seed)
    theory = math.sqrt((s.Weff + 1) * math.pi / 2)
    tame_steps = max(64, int(4 * theory) + 2)
    tame = scalar_mult(lo)
    tame_d = 0
    trail = {}
    for _ in range(tame_steps):
        tame, tame_d, caff, old = s._step(tame, tame_d)
        trail[caff] = lo + old
    return trail, tame_steps, s


def _herd(args, out_q):
    (trail, jump_aff, jumps, lo, hi, target, target_comp, W, pass_steps,
     theory_w, seed_base, max_seconds) = args
    t0 = time.monotonic()
    passes = 0
    hops = 0
    while True:
        passes += 1
        rng = random.Random(seed_base * 1000 + passes)
        d0 = rng.randrange(0, int(2 * theory_w) + 1)
        if d0 == 0:
            wild, wild_d = target, 0
        else:
            wild = jac_add_affine(target, *to_affine(scalar_mult(d0)))
            wild_d = d0
        for _ in range(pass_steps):
            aff = to_affine(wild)
            caff = _V5.canon_aff(aff)
            b = (aff[0] >> 120) & 0xF
            old_d = wild_d
            wild = jac_add_affine(wild, *jump_aff[b])
            wild_d = old_d + jumps[b]
            hops += 1
            t_off = trail.get(caff)
            if t_off is not None:
                for k in (t_off - old_d, N - (t_off + old_d)):
                    if 0 <= k - lo <= W and point_equal_jac(scalar_mult(k), target):
                        if native_pubkey(k) == target_comp:
                            out_q.put((k, hops, passes))
                            return
        if max_seconds is not None and time.monotonic() - t0 > max_seconds:
            out_q.put((None, hops, passes))
            return


def run_parallel(wb, seed, workers, max_seconds=240):
    lo = 1 << (wb - 1)
    hi = (1 << wb) - 1
    W = hi - lo
    rng = random.Random(seed * 1000 + wb)
    key = rng.randint(lo, hi)
    target = scalar_mult(key)
    target_comp = compressed(target)

    t0 = time.perf_counter()
    trail, tame_steps, s = build_trail(lo, hi, seed=seed)
    theory_w = math.sqrt((W + 1) * math.pi / 2)
    pass_steps = max(64, int(6 * math.sqrt((s.Weff + 1) * math.pi / 2)) + 2)
    base = (trail, s.jump_aff, s.jumps, lo, hi, target, target_comp, W,
            pass_steps, theory_w, 0, max_seconds)
    out_q = mp.Queue()
    procs = []
    for wi in range(workers):
        a = list(base)
        a[10] = seed * 1000 * 7 + wi * 7919   # distinct stream per worker
        procs.append(mp.Process(target=_herd, args=(tuple(a), out_q), daemon=True))
    for p in procs:
        p.start()
    wall_to_trail = time.perf_counter() - t0
    deadline = max_seconds
    got = out_q.get(timeout=deadline)
    wall = time.perf_counter() - t0
    for p in procs:
        p.terminate()
    for p in procs:
        p.join(timeout=2)
    k, hops, passes = got
    if k is None:
        return {"width_bits": wb, "seed": seed, "workers": workers, "ok": False,
                "wall_s": round(wall, 3), "trail_serial_s": round(wall_to_trail, 3),
                "tame_steps": tame_steps}
    ok = (k == key and point_equal_jac(scalar_mult(k), target)
          and native_pubkey(k) == target_comp)
    return {"width_bits": wb, "seed": seed, "workers": workers, "ok": ok,
            "wall_s": round(wall, 3), "trail_serial_s": round(wall_to_trail, 3),
            "hops": hops, "passes": passes, "tame_steps": tame_steps}


def main():
    wb = 28
    seeds = list(range(1, 13))
    log = {"meta": {"experiment": "EXP-N3", "width_bits": wb,
                    "solver": "v5_fused_negation (shared-store multi-herd)",
                    "date": time.strftime("%Y-%m-%d %H:%M:%S"),
                    "verification": "scalar_mult identity + native FFI",
                    "wall_definition": "first herd completion (incl. serial trail build)"},
           "trials": []}
    for workers in (1, 2, 4):
        ws = []
        for seed in seeds:
            r = run_parallel(wb, seed, workers)
            log["trials"].append(r)
            ws.append(r["wall_s"])
            print(f"  workers={workers} seed={seed:>2} ok={r['ok']} "
                  f"wall={r['wall_s']:7.2f}s hops={r.get('hops','-')}",
                  flush=True)
        med = sorted(ws)[len(ws) // 2]
        mean = sum(ws) / len(ws)
        nok = sum(1 for r in log["trials"] if r["workers"] == workers and r["ok"])
        print(f"  w=28 workers={workers}: mean_wall={mean:.2f}s med_wall={med:.2f}s "
              f"solves={nok}/12", flush=True)
    with open(REPORT, "w", encoding="utf-8") as fh:
        json.dump(log, fh, indent=2)
    print(f"log -> {REPORT}")


if __name__ == "__main__":
    main()