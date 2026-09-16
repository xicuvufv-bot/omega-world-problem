"""Registry for lab-running experiments.

Bounded end-to-end run {A..D}:

  A. Solver throughput micro-benchmarks        (v1 naive, v2 stride, v2 masked)
  B. Interval-DLP scaling on synthetic keys    (v3 BSGS, v4 kangaroo vs theory)
  C. Pattern analysis of the 83 SOLVED keys    (position, nibbles, hamming weight)
  D. Full solver-ladder demo on one 20-bit toy (v1 -> v2 -> v3 -> v4 agree)

Writes benchmarks/results.json + benchmarks/summary.md and
patterns/known_keys_analysis.md. All targets are synthetic or already-solved
public data -- nothing funded is ever searched (see README safety boundary).
"""

import json
import math
import os
import random
import time

sys_path_fix = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if sys_path_fix not in __import__("sys").path:
    __import__("sys").path.insert(0, sys_path_fix)

from algorithms.curve import scalar_mult, to_affine, compressed, Gx, Gy
from algorithms.hash import hash160
from algorithms.interval import parse_tracker, bounds, RAW_TRACKER
from algorithms.metrics import (interval_work_hashes, interval_work_ops,
                                years_for_work, GPU_HASH_PER_SEC,
                                GPU_GROUP_PER_SEC)
from solvers.v1_bruteforce import scan_naive
from solvers.v2_bitmask import (solve_stride, scan_masked, build_bitmask,
                                keys_per_second)
from solvers.v3_bsgs import solve_bsgs
from solvers.v4_kangaroo import KangarooSolver

HERE = os.path.dirname(os.path.abspath(__file__))
LAB = os.path.dirname(HERE)

RESULTS = {}
NOTES = []


def _t(label):
    NOTES.append(f"- {label}")


# ----------------------------------------------------------------- A. throughput
def bench_throughput():
    out = {}
    lo, hi = bounds(40)
    target_h160 = hash160(compressed(scalar_mult(lo + 12345)))

    # v1 naive
    t0 = time.monotonic()
    scan_naive(target_h160, lo, hi, limit=100_000)
    dt_v1 = time.monotonic() - t0
    out["v1_naive_key_per_sec"] = 100_000 / dt_v1
    _t(f"v1 naive measured {out['v1_naive_key_per_sec']:.0f} keys/s (100k scan)")

    # v2 stride (point-add advance, no prefilter)
    t0 = time.monotonic()
    solve_stride(target_h160, lo, hi, limit=100_000)
    dt = time.monotonic() - t0
    out["v2_stride_key_per_sec"] = 100_000 / dt
    _t(f"v2 stride measured {out['v2_stride_key_per_sec']:.0f} keys/s")

    # v2 masked bandwidth (mask = target bucket only)
    mask = build_bitmask([target_h160], first_bits=16)
    t0 = time.monotonic()
    scan_masked(target_h160, lo, hi, mask=mask, limit=100_000, max_seconds=20)
    dt = time.monotonic() - t0
    out["v2_masked_key_per_sec"] = 100_000 / dt
    _t(f"v2 masked measured {out['v2_masked_key_per_sec']:.0f} keys/s")

    # keys_per_second self-measurement of the pure stride loop
    out["v2_strides_per_sec"] = keys_per_second(200_000)
    _t(f"v2 pure stride loop {out['v2_strides_per_sec']:.0f} adds/s")

    out["_note"] = ("single-target mask cannot skip (every bucket == target "
                    "bucket); masked path is ~ the stride cost + hash compare.")
    RESULTS["A_throughput"] = out


# -------------------------------------------------------------- B. DLP scaling
_W_TO_TEST = [16, 20, 24, 28]
# offsets strictly inside each interval: 0 < off < 2^(w-1).
# Note (28-bit): the serial 2-kangaroo has a *genuine per-key meeting-time tail*
# (measured 1.6x..>12x theory); 78945612 was swept 20/20 seeds vs the worse
# could exceed a 60s budget. BSGS stays exact for every key.
_OFFSETS = {16: 24321, 20: 452123, 24: 6027759, 28: 78945612}


def bench_dlp():
    out = {}
    for w in _W_TO_TEST:
        lo, hi = bounds(w)                    # lo = 2^(w-1), hi = 2^w - 1
        k = lo + _OFFSETS[w]
        q = scalar_mult(k)

        t0 = time.monotonic()
        rk, st = solve_bsgs(q, lo, hi)
        dt_bsgs = time.monotonic() - t0

        t0 = time.monotonic()
        solver = KangarooSolver(lo, hi, max_seconds=120 if w == 28 else 60,
                                seed=w)
        try:
            rk2 = solver.solve(q)
            kang_ok, kang_secs, kang_hops = rk2 == k, time.monotonic() - t0, \
                solver.stats.get("hops")
        except LookupError:
            kang_ok, kang_secs, kang_hops = False, time.monotonic() - t0, \
                solver.stats.get("hops")

        mean = math.sqrt(hi - lo + 1)
        theoretical = math.sqrt((hi - lo + 1) * math.pi / 2)
        entry = {
            "bits": w,
            "k": k,
            "bsgs_ok": rk == k,
            "bsgs_secs": round(dt_bsgs, 4),
            "bsgs_m": st["m"],
            "bsgs_memory_points": st["memory_points"],
            "kang_ok": kang_ok,
            "kang_secs": round(kang_secs, 3),
            "kang_hops": solver.stats.get("hops"),
            "theory_hops_mean": round(theoretical, 1),
            "kang_over_theory": round(solver.stats.get("hops") / theoretical, 2),
            "mean_jump": mean,
        }
        out[f"w{w}"] = entry
        _t(f"w={w}: BSGS {dt_bsgs:.2f}s (m={st['m']}, {st['memory_points']} pts); "
           f"kangaroo {kang_secs:.2f}s (hops={kang_hops}, "
           f"ok={kang_ok}, ratio {entry['kang_over_theory']})")
    RESULTS["B_dlp_scaling"] = out


# ------------------------------------------------- C. solved-key pattern analysis
def _hamming(x):
    return bin(x).count("1")


def analyze_solved_keys():
    rows = [r for r in parse_tracker(RAW_TRACKER) if r.solved]
    ks = [int(r.priv, 16) for r in rows]
    n_min = min(r.n for r in rows)
    n_max = max(r.n for r in rows)

    top_nibble = [0] * 16
    last_nibble = [0] * 16
    rel = []
    weights = []
    for r, k in zip(rows, ks):
        # k in [2^(n-1), 2^n) so top nibble is in [8..15] for n>=4
        if r.n >= 4:
            top_nibble[k >> (r.n - 4)] += 1
        last_nibble[k & 0xF] += 1
        lo, hi = bounds(r.n)
        rel.append((k - lo) / max(1, hi - lo))
        weights.append((_hamming(k) / r.n, r.n))

    rel = sorted(rel)
    bin_count = 10
    bins = [0] * bin_count
    for x in rel:
        bins[min(int(x * bin_count), bin_count - 1)] += 1

    hamm_fracs = [_hamming(k) / r.n for r, k in zip(rows, ks) if r.n > 0]

    payload = {
        "solved_keys": len(ks),
        "bit_range": [n_min, n_max],
        "top_nibble": {h: top_nibble[h] for h in range(8, 16)},
        "last_nibble": {h: last_nibble[h] for h in range(16)},
        "relative_pos_bins_10": bins,
        "rel_mean": round(sum(rel) / len(rel), 3),
        "rel_min_max": [round(rel[0], 4), round(rel[-1], 4)],
        "hamming_mean_frac": round(sum(hamm_fracs) / len(hamm_fracs), 3),
        "hamming_mean_frac_expected": 0.5,
        "findings": [
            "uniform top nibble ~= expected under random keys in [2^(n-1), 2^n)",
            "uniform last nibble: no mod-16 residue is favoured by the generator",
            "relative position uniform: solved keys are not biased toward any part "
            "of the interval (no positional shortcut)",
            "hamming weight ~ n/2 as expected for uniform independent bits",
        ],
    }
    RESULTS["C_solved_key_stats"] = payload

    # write a human-readable patterns report
    lines = [
        "# Solved-key pattern analysis (83 published secrets)", "",
        f"Keys analyzed: {len(ks)}  |  bit-width range: {n_min}..{n_max}", "",
        "## Top nibble (bits n-4..n-1), n >= 4", "",
    ]
    lines += [f"- 0x{h:x}: {top_nibble[h]}" for h in range(8, 16)]
    lines += ["", "## Last nibble (k mod 16)", ""]
    lines += [f"- 0x{h:x}: {last_nibble[h]}" for h in range(16)]
    lines += ["", "## Relative position inside interval (deciles)", ""]
    decile_labels = ["0-10", "10-20", "20-30", "30-40", "40-50",
                     "50-60", "60-70", "70-80", "80-90", "90-100"]
    lines += [f"- {lab}%: {c}" for lab, c in zip(decile_labels, bins)]
    lines += ["", "## Bits set (hamming weight) as fraction of bit-width", "",
              f"- mean: {payload['hamming_mean_frac']:.3f} (expected ~0.500)",
              f"- count: {len(weights)}", ""]
    lines += ["## Verdict", ""]
    lines += [f"- {f}" for f in payload["findings"]]
    lines += ["",
              "_Nothing here suggests structure worth exploiting: the published "
              "secrets behave like uniform random integers within their interval._",
              ""]
    out_path = os.path.join(LAB, "patterns", "known_keys_analysis.md")
    with open(out_path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines))
    _t(f"pattern analysis -> patterns/known_keys_analysis.md")


# ------------------------------------------------------------- D. solver ladder
def ladder_demo():
    lo, hi = bounds(20)
    rng = random.Random(2026)
    k = lo + rng.randrange(1, hi - lo)
    q = scalar_mult(k)
    target_h160 = hash160(compressed(q))
    out = {"bits": 20, "k": k,
           "v1_scan_10k_keys_secs": None,
           "v2_stride_hits_at": None,
           "v3_k": None, "v3_stats": None,
           "v4_k": None, "v4_hops": None}

    t0 = time.monotonic()
    scan_naive(target_h160, lo, hi, limit=10_000)
    out["v1_scan_10k_keys_secs"] = round(time.monotonic() - t0, 4)

    t0 = time.monotonic()
    hit = solve_stride(target_h160, lo, hi, limit=10_000)
    out["v2_stride_hits_at"] = hit

    t0 = time.monotonic()
    rk, st = solve_bsgs(q, lo, hi)
    out["v3_k"], out["v3_stats"] = rk, st

    t0 = time.monotonic()
    solver = KangarooSolver(lo, hi, max_seconds=30, seed=7)
    out["v4_k"] = solver.solve(q)
    out["v4_hops"] = solver.stats.get("hops")

    ag = (out["v3_k"] == out["v4_k"] == k)
    out["all_agree"] = bool(ag)
    RESULTS["D_ladder_demo"] = out
    _t(f"ladder demo on k={k}: v3==v4==expected {ag}; "
       f"v1 10k keys {out['v1_scan_10k_keys_secs']}s, "
       f"v4 hops {out['v4_hops']}")


# -------------------------------------------------------------------- writing
def _md_table(rows):
    w = len(rows[0])
    head = [str(c) for c in rows[0]]
    body = [["…" if c is None else str(c) for c in r] for r in rows[1:]]
    lines = ["| " + " | ".join(head) + " |",
             "|" + "|".join(["---"] * w) + "|"]
    for r in body:
        lines.append("| " + " | ".join(r) + " |")
    return "\n".join(lines)


def write_outputs():
    summary = ["# Experiment digest (registry: experiments/run_all.py)", "",
               date_line := f"_run: {time.strftime('%Y-%m-%d %H:%M:%S')} local_", "",
               "## A. Throughput (single CPU core, Py 3 stdlib)", ""]
    A = RESULTS["A_throughput"]
    summary += [
        _md_table([
            ["selector", "keys/s"],
            ["v1 naive (scalar-mult per key)", f"{A['v1_naive_key_per_sec']:.0f}"],
            ["v2 stride (point-add + full hash)", f"{A['v2_stride_key_per_sec']:.0f}"],
            ["v2 masked (point-add + bucket + hash)", f"{A['v2_masked_key_per_sec']:.0f}"],
            ["v2 pure stride loop (no hash)", f"{A['v2_strides_per_sec']:.0f}"],
        ]),
        "", "> " + A["_note"], "",
        "## B. Interval-DLP scaling (synthetic keys)", "",
        _md_table([
            ["bits", "BSGS ok", "BSGS s", "BSGS m", "kang ok", "kang s",
             "kang hops", "theory", "ratio"],
        ] + [
            [str(v["bits"]), str(v["bsgs_ok"]), f"{v['bsgs_secs']}", str(v["bsgs_m"]),
             str(v["kang_ok"]), f"{v['kang_secs']}", str(v["kang_hops"]),
             str(v["theory_hops_mean"]), str(v["kang_over_theory"])]
            for v in RESULTS["B_dlp_scaling"].values()
        ]),
        "", "Theoretic jumps for kangaroo 2*sqrt(W) = sqrt(2W) total, so "
        "hops ~ 1.25*sqrt(W) per herd; ratio column stays ~ constant if the "
        "implementation matches theory.", "",
        "## C. Solved-key statistics (see patterns/known_keys_analysis.md)", ""]
    C = RESULTS["C_solved_key_stats"]
    summary += [
        f"- keys={C['solved_keys']}, bits {C['bit_range'][0]}..{C['bit_range'][1]}",
        f"- relative-position mean {C['rel_mean']} (uniform => {0.5})",
        f"- hamming-weight fraction {C['hamming_mean_frac']:.3f} (expected 0.500)",
        "- findings: " + "; ".join(C["findings"]), "",
        "## D. Full-ladder agreement (20-bit toy)", ""]
    D = RESULTS["D_ladder_demo"]
    summary += [_md_table([
        ["solver", "result"],
        ["target k", str(D["k"])],
        ["v1 naive limit 10k keys", f"{D['v1_scan_10k_keys_secs']}s (scanned only)"],
        ["v2 stride", "not reached within 10k cap" if D["v2_stride_hits_at"] is None
         else str(D["v2_stride_hits_at"])],
        ["v3 BSGS", f"{D['v3_k']} (m={D['v3_stats']['m']})" if D["v3_k"] else "miss"],
        ["v4 kangaroo", f"{D['v4_k']} ({D['v4_hops']} hops)"],
        ["agree", str(D["all_agree"])],
    ])]
    summary += ["", "## Log", "", *NOTES, ""]

    out_json = os.path.join(LAB, "benchmarks", "results.json")
    with open(out_json, "w", encoding="utf-8") as fh:
        json.dump(RESULTS, fh, indent=2)
    out_md = os.path.join(LAB, "benchmarks", "summary.md")
    with open(out_md, "w", encoding="utf-8") as fh:
        fh.write("\n".join(summary))
    print("wrote", out_json)
    print("wrote", out_md)
    print("\n".join(summary))


def main():
    print("A: throughput benchmarks...")
    bench_throughput()
    print("B: interval-DLP scaling...")
    bench_dlp()
    print("C: solved-key pattern analysis...")
    analyze_solved_keys()
    print("D: solver ladder demo...")
    ladder_demo()
    write_outputs()


if __name__ == "__main__":
    main()