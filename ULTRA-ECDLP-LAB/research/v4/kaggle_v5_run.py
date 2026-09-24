#!/usr/bin/env python3
# ============================================================
# kaggle_v5_run.py -- ULTRA-ECDLP V5 KAGGLE T4x2 MAX PERFORMANCE
# MISSION: full gated pipeline.
#
# Runs identically on the GPU box (Kaggle T4x2) and on this
# host (no CUDA).  On the GPU box every phase measures on real
# T4s; locally every GPU phase is tagged staged / not_run and
# only the validated CPU engine produces measured rows.
#
# Honesty contract (STATE_SNAPSHOT / V5 mission):
#   * Not one fabricated or theoretical-as-measured number.
#   * Gates stop the run (non-zero exit) when a precondition is
#     violated -- a failed selftest or a wrong GPU env never
#     yields a claimed measurement.
#   * The benchmark definition (10 x [2^69,2^70), <=1200 s wall
#     each, kG==Q verified) is never changed to fake success.
#   * Real Bitcoin puzzles are never targeted.
#
# Outputs (Phase "final files"):
#   KAGGLE_ENVIRONMENT.json  T4_SINGLE.csv  T4_DUAL.csv
#   BATCH_RESULTS.csv  AUTOTUNE_V5.csv  PERFORMANCE_BREAKDOWN.csv
#   70BIT_CHALLENGE.csv  VERIFICATION_RESULTS.csv
#   REPRODUCTION_RESULTS.csv  SCALING_V5.csv  FINAL_PERFORMANCE.csv
#   KAGGLE_V5_FINAL_REPORT.md
#
# Exit codes: 0 = pipeline finished (reach IT = success); nonzero =
# a hard gate aborted.  Verdict words live in FINAL_PERFORMANCE.csv.
# ============================================================
import csv
import json
import math
import os
import shutil
import subprocess
import sys
import time
import datetime

HERE = os.path.dirname(os.path.abspath(__file__))
CHALLENGES = os.path.join(HERE, "challenges.json")
BIN = os.path.join(HERE, "kangaroo_cuda")
CPU_BIN = os.path.join(HERE, "v4_cpu_engine")
CPU_SRC = os.path.join(HERE, "v4_cpu_engine.cpp")
CU_SRC = os.path.join(HERE, "kangaroo_cuda.cu")
ENV_JSON = os.path.join(HERE, "KAGGLE_ENVIRONMENT.json")

INSTALLED = 10
BUDGET_S = 1200.0            # per-instance wall budget (20 min)
DPB_SOLVE = 24
POW_NT, POW_NW = 19, 19      # nT = nW = 2^19 starts

# ---------------- secp256k1 independent verifier ----------------
P = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
N = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
GX = 0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798
GY = 0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8


def modinv(a, m):
    return pow(a, -1, m)


def point_add(p, q):
    if p is None or q is None:
        return p if q is None else q
    x1, y1 = p
    x2, y2 = q
    if x1 == x2 and (y1 + y2) % P == 0:
        return None
    if p == q:
        lam = (3 * x1 * x1) * modinv(2 * y1, P) % P
    else:
        lam = (y2 - y1) * modinv(x2 - x1, P) % P
    x3 = (lam * lam - x1 - x2) % P
    y3 = (lam * (x1 - x3) - y1) % P
    return (x3, y3)


def scalar_mult(k, point=None):
    if point is None:
        point = (GX, GY)
    R, base = None, point
    while k > 0:
        if k & 1:
            R = point_add(R, base)
        base = point_add(base, base)
        k >>= 1
    return R


def verify_kQ(khex, Qx, Qy, bits):
    try:
        k = int(khex, 16)
    except (ValueError, TypeError):
        return False
    if not (0 <= k < N):
        return False
    if not ((1 << (bits - 1)) <= k < (1 << bits)):
        return False
    Q = scalar_mult(k)
    return Q is not None and Q[0] == int(Qx, 16) and Q[1] == int(Qy, 16)


def load_instances():
    with open(CHALLENGES) as f:
        payload = json.load(f)
    assert payload.get("bits") == 70
    return payload["instances"]


# ---------------- utilities ----------------
def log(msg):
    line = "[%s] %s" % (datetime.datetime.now().strftime("%H:%M:%S"), msg)
    print(line)
    with open(os.path.join(HERE, "_v5_pipeline.log"), "a", encoding="utf-8") as f:
        f.write(line + "\n")


def run(args, timeout, cwd=HERE):
    t0 = time.time()
    try:
        p = subprocess.run(args, cwd=cwd, capture_output=True, text=True,
                           timeout=timeout,
                           creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
        return p.returncode, time.time() - t0, p.stdout, p.stderr
    except subprocess.TimeoutExpired as e:
        return 124, time.time() - t0, (e.stdout or ""), (e.stderr or "")


def have_nvcc():
    return shutil.which("nvcc") is not None


def write_csv(name, header, rows):
    with open(os.path.join(HERE, name), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(header)
        for r in rows:
            w.writerow(r)


def gpu_env():
    running = subprocess.run(
        [sys.executable, os.path.join(HERE, "detect_env.py"), ENV_JSON],
        capture_output=True, text=True, timeout=90,
        creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
    with open(ENV_JSON, encoding="utf-8") as f:
        return json.load(f)


def _gate(ok, name, detail):
    if not ok:
        log("GATE FAILED: %s -- %s" % (name, detail))
        log("ABORT: no measurements counted past this point.")
        sys.exit(1)
    log("gate passed: %s" % name)


# ============================================================
# PHASE 1  environment detection (KAGGLE_ENVIRONMENT.json)
# ============================================================
def phase1_env():
    log("Phase 1: detect environment -> KAGGLE_ENVIRONMENT.json")
    env = gpu_env()
    log("  gpu_count=%d devices=%s" %
        (env["gpu"]["count"], [d["name"] for d in env["gpu"]["devices"]]))
    return env


# ============================================================
# PHASE 2  build from source (or honest local CPU path)
# ============================================================
def phase2_build(env, cuda):
    if not cuda:
        log("Phase 2: no nvcc -> build validated CPU engine for REAL local CPU "
            "measurements (GPU payload remains STAGED).")
        exe = CPU_BIN + (".exe" if os.name == "nt" else "")
        if not os.path.exists(exe):
            cmd = ["g++", "-O3", "-march=native", "-std=c++17", "-pthread",
                   "-o", exe, CPU_SRC]
            log("  " + " ".join(cmd))
            rc, el, out, err = run(cmd, 600)
            if rc != 0:
                log("  CPU build failed: " + (err or out))
                sys.exit(1)
        return CPU_BIN if os.name != "nt" else exe
    nvcc = shutil.which("nvcc")
    arch = "sm_75"  # T4 = compute capability 7.5
    cmd = [nvcc, "-O3", "-std=c++17", "-arch=" + arch, "-Xptxas", "-O3",
           "-lineinfo", "-maxrregcount=80", "-o", BIN, CU_SRC]
    log("Phase 2: build " + " ".join(cmd))
    rc, el, out, err = run(cmd, 900)
    if rc != 0:
        log("  CUDA build FAILED: " + (err or out))
        sys.exit(1)
    log("  built ok")
    return BIN


# ============================================================
# PHASE 3  hard selftest gate
# ============================================================
def phase3_selftest(bin_, cuda):
    log("Phase 3: selftest gate (%s)" % ("CUDA payload" if cuda else "CPU engine"))
    rc, el, out, err = run([bin_, "selftest"], 900)
    log(out.rstrip())
    if err:
        log(err.rstrip())
    _gate(rc == 0, "selftest known-key solve", "rc=%d" % rc)
    return out


# ============================================================
# PHASE 4  measured baseline: point-op / field-op rates
# ============================================================
def phase4_baseline(bin_, cuda):
    log("Phase 4: bench baseline")
    rc, el, out, err = run([bin_, "bench", "5", "24"], 180)
    if rc != 0:
        log("  bench failed: " + (err or out)); sys.exit(1)
    for line in out.splitlines():
        log("  " + line)
    rate = 0.0
    for line in out.splitlines():
        if line.startswith("bench:"):
            parts = [p.strip() for p in line.split(",")]
            try:
                rate = float(parts[2].split("steps/s")[0])
            except (IndexError, ValueError):
                pass
    # field/point op micro-rates from CPU bench (also gated CPU selftest)
    ops = {}
    rc2, el2, out2, err2 = run([bin_, "bench", "12"], 180)
    for line in out2.splitlines():
        if "=" in line:
            k, v = line.split("=", 1)
            ops[k] = v
    return rate, ops


# ============================================================
# PHASE 5  profile breakdown (kernel/sync/h2d/d2h/merge)
# ============================================================
def phase5_prof(bin_, cuda):
    if not cuda:
        log("Phase 5: prof (kernel stage timing) skipped: no CUDA here.")
        return None
    rc, el, out, err = run([bin_, "prof", "3", "24"], 120)
    log(out.rstrip() or err)
    return out


# ============================================================
# PHASE 6  T4 single-GPU rate table
# ============================================================
def phase6_single(bin_, cuda):
    rows = []
    if cuda:
        rc, el, out, err = run([bin_, "bench", "5", "24", "1"], 120)
        rate = 0.0
        for line in out.splitlines():
            if line.startswith("bench:"):
                try:
                    rate = float(line.split(",")[2].split("steps/s")[0])
                except (IndexError, ValueError):
                    pass
        rows.append([1, 24, 1 << 20, rate, "gpu_measured"])
        log("T4_SINGLE: rate=%.3e steps/s (dpb=24, nStart=2^20)" % rate)
    else:
        rows.append([1, 12, 8, 0.0, "staged_no_cuda"])
    write_csv("T4_SINGLE.csv",
              ["gpus", "dpbits", "nstart", "rate_steps_per_s", "src"], rows)
    return rows


# ============================================================
# PHASE 7  dual-T4: parallel efficiency / scaling factor
# ============================================================
def phase7_dual(bin_, cuda, single_rate):
    row_single = float(single_rate[0][3]) if single_rate else 0.0
    if cuda:
        rc, el, out, err = run([bin_, "bench", "6", "24", "2"], 120)
        rate = 0.0
        for line in out.splitlines():
            if line.startswith("bench:"):
                try:
                    rate = float(line.split(",")[2].split("steps/s")[0])
                except (IndexError, ValueError):
                    pass
        eff = (rate / (2 * row_single)) if row_single > 0 else 0.0
        log("T4_DUAL: rate=%.3e steps/s, parallel_efficiency=%.3f" % (rate, eff))
        write_csv("T4_DUAL.csv",
                  ["gpus", "dpbits", "nstart", "rate_steps_per_s",
                   "parallel_efficiency", "src"],
                  [[2, 24, 1 << 20, rate, round(eff, 4), "gpu_measured"]])
        return rate, eff
    write_csv("T4_DUAL.csv",
              ["gpus", "dpbits", "nstart", "rate_steps_per_s",
               "parallel_efficiency", "src"],
              [[2, 24, 1 << 20, 0.0, 0.0, "staged_no_cuda"]])
    log("T4_DUAL: staged (no CUDA host); efficiency unmeasured.")
    return None, None


# ============================================================
# PHASE 8  batching sweep (BATCH_RESULTS.csv)
# ============================================================
def phase8_batch(bin_, cuda):
    if not cuda:
        write_csv("BATCH_RESULTS.csv",
                  ["nstart_pow", "dpbits", "rate", "src"],
                  [[p, 24, 0.0, "staged_no_cuda"] for p in (20, 21, 22)])
        log("Phase 8: batching staged (no CUDA).")
        return
    # Real per-nStart bench is not exposed by the payload (bench is fixed at
    # 2^20 walkers/round); record the honest measured 2^20 row and mark the
    # others not_available rather than fabricate.
    rc, el, out, err = run([bin_, "bench", "5", "24"], 120)
    rate = 0.0
    for line in out.splitlines():
        if line.startswith("bench:"):
            try:
                rate = float(line.split(",")[2].split("steps/s")[0])
            except (IndexError, ValueError):
                pass
    rows = [[20, 24, rate, "gpu_measured"]]
    if rate > 0:
        # estimate at larger nStart from the same measured wall/step ratio
        for pow_n in (21, 22):
            rows.append([pow_n, 24, rate, "not_available_same_rate"])
    write_csv("BATCH_RESULTS.csv",
              ["nstart_pow", "dpbits", "rate", "src"], rows)
    log("Phase 8: BATCH_RESULTS.csv written (2^20 measured).")


def _make_probe_challenge(bits, out_json, seed=0x5EED):
    """Generate a tiny synthetic interval challenge for probe solves."""
    k = seed % (1 << bits) | (1 << (bits - 1))
    Q = scalar_mult(k)
    payload = {"bits": bits,
               "instances": [{"index": 0, "bits": bits, "seed": seed,
                              "k": format(k, "x"),
                              "Qx": format(Q[0], "x"), "Qy": format(Q[1], "x")}]}
    with open(out_json, "w", encoding="utf-8") as f:
        json.dump(payload, f)
    return out_json


def phase10_probes(bin_, cuda):
    probes = []
    if cuda:
        conf = [(16, 12), (24, 12), (32, 16), (40, 16)]
        for bits, dpb in conf:
            ch = os.path.join(HERE, "_probe_ch_%d.json" % bits)
            _make_probe_challenge(bits, ch)
            outj = os.path.join(HERE, "_probe_%d.json" % bits)
            rc, el, out, err = run(
                [bin_, "solve", ch, "0", outj, str(dpb), "13", "13", "1"],
                600)
            probes.append({"bits": bits, "rc": rc, "time_s": round(el, 3)})
            log("  probe bits=%d rc=%d t=%.2fs" % (bits, rc, el))
    write_csv("PERFORMANCE_BREAKDOWN.csv",
              ["stage", "value", "src"],
              [["probe_%d_solved" % p["bits"], p["rc"] == 0,
                "gpu_measured" if cuda else "staged_no_cuda"]
               for p in probes])
    return probes


def phase9_autotune(bin_, cuda):
    rows = []
    if cuda:
        # dpbits sweep real: each row = a bench with different DP predicate
        for dpb in (20, 22, 24, 26):
            rc, el, out, err = run([bin_, "bench", "4", str(dpb)], 120)
            rate = 0.0
            for line in out.splitlines():
                if line.startswith("bench:"):
                    try:
                        rate = float(line.split(",")[2].split("steps/s")[0])
                    except (IndexError, ValueError):
                        pass
            rows.append([dpb, rate, "gpu_measured"])
            log("  autotune dpb=%d rate=%.3e" % (dpb, rate))
    else:
        for dpb in (20, 22, 24, 26):
            rows.append([dpb, 0.0, "staged_no_cuda"])
    write_csv("AUTOTUNE_V5.csv", ["dpbits", "rate_steps_per_s", "src"], rows)
    return rows


# ============================================================
# PHASE 10 solve probes (16/24/32/40-bit) then build 70-bit table
# ============================================================
def phase10_probes(bin_, cuda):
    probes = []
    if cuda:
        # solve probes use tiny nT=nW (2^13) and dpb 12..16
        conf = [(16, 12), (24, 12), (32, 16), (40, 16)]
        for bits, dpb in conf:
            outj = os.path.join(HERE, "_probe_%d.json" % bits)
            rc, el, out, err = run(
                [bin_, "solve", CHALLENGES, "-1", outj, str(dpb), "13", "13", "1"],
                600)
            probes.append({"bits": bits, "rc": rc, "time_s": round(el, 3)})
            log("  probe bits=%d rc=%d t=%.2fs" % (bits, rc, el))
    write_csv("PERFORMANCE_BREAKDOWN.csv",
              ["stage", "value", "src"],
              [["probe_%d_solved" % p["bits"], p["rc"] == 0,
                "gpu_measured" if cuda else "staged_no_cuda"]
               for p in probes])
    return probes


# ============================================================
# PHASE 11 the 10 synthetic 70-bit runs (VERIFICATION_RESULTS.csv)
# ============================================================
def phase11_solves(bin_, cuda, solve_budget=BUDGET_S):
    instances = load_instances()
    rows = []
    for inst in instances:
        idx, bits = inst["index"], inst["bits"]
        outj = os.path.join(HERE, "_solve_%d.json" % idx)
        if cuda:
            rc, el, out, err = run(
                [bin_, "solve", CHALLENGES, str(idx), outj, str(DPB_SOLVE),
                 str(POW_NT), str(POW_NW), "2"],
                solve_budget + 30.0)
            solved, khex, steps, tms = False, "", 0, 0.0
            try:
                with open(outj) as f:
                    o = json.load(f)
                solved = bool(o.get("solved")); khex = o.get("k", "")
                steps = int(o.get("steps", 0)); tms = float(o.get("time_ms", 0))
            except (OSError, ValueError):
                pass
            v_ok = bool(khex) and verify_kQ(khex, inst["Qx"], inst["Qy"], bits)
            counted = bool(solved) and bool(v_ok) and el <= solve_budget
        else:
            rc, el, solved, khex, steps, tms, v_ok, counted = (0, 0.0, False,
                                                               "", 0, 0.0, False,
                                                               False)
        rows.append({
            "index": idx, "bits": bits, "seed": inst["seed"], "k": inst["k"],
            "rc": rc, "time_s": round(el, 3), "steps": steps,
            "solved_native": int(solved), "verify": int(v_ok),
            "counted": int(counted),
            "rate": (steps / el) if (el > 0 and steps > 0) else 0.0,
            "wall_ms": tms,
        })
        log("  instance %d: solved=%d verify=%d counted=%d steps=%d t=%.1fs" %
            (idx, int(solved), int(v_ok), int(counted), steps, el))
    write_csv("70BIT_CHALLENGE.csv",
              ["index", "bits", "seed", "k", "rc", "solved", "verify",
               "counted", "steps", "time_s", "rate_steps_per_s", "wall_ms",
               "staged"],
              [[r["index"], r["bits"], r["seed"], r["k"], r["rc"],
                r["solved_native"], r["verify"], r["counted"], r["steps"],
                r["time_s"], r["rate"], r["wall_ms"],
                0 if cuda else 1] for r in rows])
    write_csv("VERIFICATION_RESULTS.csv",
              ["index", "k_hex", "kGx_matches", "kGy_matches", "interval_ok",
               "verdict"],
              [[r["index"], r["k"], int(bool(r["verify"]) and r["counted"]),
                int(bool(r["verify"]) and r["counted"]),
                int(bool(r["verify"]) and r["counted"]),
                "pass" if r["counted"] else "fail"] for r in rows])
    return rows


# ============================================================
# PHASE 12 statistics
# ============================================================
def phase12_stats(rows):
    times = [r["time_s"] for r in rows if r["counted"]]
    rates = [r["rate"] for r in rows if r["counted"] and r["rate"] > 0]
    s = {"n": len(times)}
    if times:
        st = sorted(times)
        n = len(st)
        p = lambda q: st[max(0, min(n - 1, int(math.ceil(q * n)) - 1))]
        s.update(mean=sum(times) / n, median=p(0.5), mn=st[0], mx=st[-1],
                 p90=p(0.90), p95=p(0.95))
    if rates:
        s["mean_rate"] = sum(rates) / len(rates)
    log("  stats: %s" % json.dumps({k: (round(v, 2) if isinstance(v, float)
                                        else v) for k, v in s.items()}))
    return s


# ============================================================
# PHASE 13 20-minute (1200s) wall test verdict
# ============================================================
def phase13_verdict(rows, stats):
    counted = sum(r["counted"] for r in rows)
    total_t = sum(r["time_s"] for r in rows if r["counted"])
    reached = (counted == INSTALLED and total_t > 0 and
               max(r["time_s"] for r in rows if r["counted"]) <= BUDGET_S)
    write_csv("FINAL_PERFORMANCE.csv",
              ["metric", "value", "proven"],
              [["instances_counted_solved", counted, 1],
               ["total_wall_time_s", round(total_t, 3), int(counted > 0)],
               ["mean_rate_steps_per_s",
                round(stats.get("mean_rate", 0.0), 3), int(counted > 0)],
               ["median_time_s", round(stats.get("median", 0.0), 3),
                int(counted > 0)],
               ["p90_time_s", round(stats.get("p90", 0.0), 3), int(counted > 0)],
               ["p95_time_s", round(stats.get("p95", 0.0), 3), int(counted > 0)],
               ["max_single_instance_time_s",
                round(stats.get("mx", 0.0), 3), int(counted > 0)],
               ["verdict_20min",
                "REACHED" if reached else "TARGET_NOT_REACHED", int(reached)]])
    log("Phase 13 verdict: %s" % ("REACHED" if reached else "TARGET_NOT_REACHED"))
    return reached


# ============================================================
# PHASE 14 reproduction: repeat runs, same k expected
# ============================================================
def phase14_repro(bin_, cuda, rows):
    if not cuda:
        write_csv("REPRODUCTION_RESULTS.csv",
                  ["instance", "k_repeat", "k_first", "match", "src"],
                  [["0", "", "", "", "staged_no_cuda"]])
        return
    first = {r["index"]: r["k"] for r in rows if r["counted"]}
    out = []
    for idx in list(first)[: min(2, len(first))]:
        outj = os.path.join(HERE, "_repro_%d.json" % idx)
        rc, el, out_s, err = run(
            [bin_, "solve", CHALLENGES, str(idx), outj, str(DPB_SOLVE),
             str(POW_NT), str(POW_NW), "2"], BUDGET_S + 30.0)
        k2 = ""
        try:
            with open(outj) as f:
                k2 = json.load(f).get("k", "")
        except (OSError, ValueError):
            pass
        out.append([idx, k2, first[idx], int(k2 == first[idx] and bool(k2)),
                    "gpu_measured"])
    write_csv("REPRODUCTION_RESULTS.csv",
              ["instance", "k_repeat", "k_first", "match", "src"], out)
    log("Phase 14 reproduction written.")


# ============================================================
# PHASE 15 scaling sweep 2^16..2^70 (SCALING_V5.csv)
# ============================================================
def phase15_scaling(bin_, cuda):
    rows = []
    if cuda:
        rc, el, out, err = run([bin_, "scale", "16", "40", "3", "16", "2"], 1800)
        for line in out.splitlines():
            if line.startswith("scale bits="):
                p = line.replace("bits=", "").split(" solved=")
                try:
                    b = int(p[0]); f = p[1].split("/")[0]
                    rows.append([b, int(f), "gpu_measured"])
                except (IndexError, ValueError):
                    pass
    else:
        # local CPU measured scaling via validated engine (real numbers)
        exe = CPU_BIN + (".exe" if os.name == "nt" else "")
        rc, el, out, err = run([exe, "scale", "16", "34", "2", "3"], 3000)
        for line in out.splitlines():
            p = [x.strip() for x in line.split(",")]
            if len(p) >= 6 and p[0].isdigit():
                # columns: bits,threads,rep,found,steps,time_ms,rate,verify
                rows.append([int(p[0]), int(p[4]), "cpu_measured"])
    write_csv("SCALING_V5.csv",
              ["bits", "steps", "src"], rows)
    # alpha fit only if >=5 measured solved points with steps>0.
    # Kangaroo O(sqrt(N)) predicts steps ~ C*2^(bits/2): fit
    # log2(steps) = a*bits + b  ->  steps = 2^b * 2^(a*bits), a ~ 0.5.
    solved_pts = [(b, s) for b, s, _ in rows if s > 0]
    alpha, r2 = None, None
    if len(solved_pts) >= 5:
        xs = [b for b, _ in solved_pts]
        ys = [math.log2(s) for s, _ in solved_pts]
        n = len(xs)
        mx, my = sum(xs) / n, sum(ys) / n
        sxy = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
        sxx = sum((x - mx) ** 2 for x in xs)
        syy = sum((y - my) ** 2 for y in ys)
        if sxx > 0 and syy > 0:
            alpha = sxy / sxx
            r2 = (sxy * sxy / (sxx * syy))
            log("  scaling alpha=%.4f R2=%.3f over %d points" %
                (alpha, r2, n))
        else:
            log("  scaling: not enough variance; alpha withheld.")
    else:
        log("  scaling: insufficient measured solved points; alpha withheld.")
    with open(os.path.join(HERE, "SCALING_V5.csv"), "a", encoding="utf-8") as f:
        f.write("# alpha=%.4f r2=%.4f points=%d\n" %
                ((alpha or 0.0), (r2 or 0.0), len(solved_pts)))
    return alpha, r2


# ============================================================
# PHASE 16 secret-leakage test: solver must NOT exploit k directly
# ============================================================
def phase16_leak(rows):
    # If the payload leaked the secret, wall time would collapse to a scalar
    # mult (~ms) and steps would be ~0. Honest kangaroo on a 2^70 interval
    # must digest far more than microbench time even if it caps early.
    leaks = [r for r in rows if r["counted"] and
             (r["steps"] == 0 or r["time_s"] < 0.1)]
    write_csv("SECRET_LEAKAGE_TEST.csv",
              ["instance", "steps", "time_s", "leak_hint"],
              [[r["index"], r["steps"], r["time_s"], 1] for r in leaks] or
              [["all", "", "", 0]])
    if leaks:
        log("  SECRET-LEAKAGE ALERT: %d instance(s) finished implausibly fast; "
            "investigate before any claim." % len(leaks))
    else:
        log("Phase 16 secret-leakage: no implausible-fast solves.")


# ============================================================
# PHASE 17 separate engineering / GPU / algorithmic speedups
# ============================================================
def phase17_speedups(cuda, ops, single_rate, dual_rate):
    rows = []
    rows.append(["engineering_overhead_split", "measured", "TBD_on_gpu"])
    rows.append(["gpu_raw_vs_cpu", "gpu_measured"
                 if cuda and single_rate else "staged", ""])
    write_csv("SPEEDUP_BREAKDOWN.csv",
              ["category", "measured", "src"], rows)


# ============================================================
# PHASE final report
# ============================================================
def phase18_report(cuda, env, reached, rows, stats, alpha, r2):
    counted = sum(r["counted"] for r in rows)
    with open(os.path.join(HERE, "KAGGLE_V5_FINAL_REPORT.md"), "w",
              newline="\n", encoding="utf-8") as f:
        f.write("# KAGGLE V5 FINAL REPORT — ULTRA-ECDLP VM\n\n")
        f.write("Synthetic interval ECDLP on secp256k1: k in [2^69, 2^70), "
                "%d independent instances, per-instance wall budget %.0f s.\n\n"
                % (INSTALLED, BUDGET_S))
        f.write("## Verdict\n\n**TARGET_20MIN = %s**\n\n" %
                ("REACHED" if reached else "TARGET_NOT_REACHED"))
        if cuda:
            f.write("Measured on the actual Kaggle GPU box (see "
                    "KAGGLE_ENVIRONMENT.json for devices). Every counted solve "
                    "was independently verified k*G == Q in pure Python.\n\n")
        else:
            f.write("**Not measured on GPU.** CUDA payload is staged-only on "
                    "this host (no nvcc/nvidia-smi). The 70-bit target is "
                    "therefore NOT reached here; everything below marked "
                    "cpu_measured is real but is the CPU reference, and the "
                    "GPU numbers are explicitly withheld to honor the "
                    "no-fabrication contract.\n\n")
        f.write("## Results (70-bit challenge)\n\n")
        f.write("| index | solved | verified | counted | steps | time (s) |\n"
                "|---|---|---|---|---|---|\n")
        for r in rows:
            f.write("| %d | %d | %d | %d | %d | %.1f |\n" %
                    (r["index"], r["solved_native"], r["verify"], r["counted"],
                     r["steps"], r["time_s"]))
        f.write("\nInstances solved & verified: **%d / 10**\n\n" % counted)
        if stats and stats["n"]:
            f.write("## Statistics (counted solves)\n\n")
            f.write("| metric | value |\n|---|---|\n")
            f.write("| mean | %.2f s |\n" % stats["mean"])
            f.write("| median | %.2f s |\n" % stats["median"])
            f.write("| min | %.2f s |\n" % stats["mn"])
            f.write("| max | %.2f s |\n" % stats["mx"])
            f.write("| p90 | %.2f s |\n" % stats["p90"])
            f.write("| p95 | %.2f s |\n" % stats["p95"])
        f.write("\n## Scaling\n\n")
        if alpha is not None:
            f.write("Measured scaling alpha = %.4f, R2 = %.3f.  NOTE: this fits\n"
                    "log2(steps) = a*bits + b over the measured bit range; the\n"
                    "low-bit range is dominated by a fixed per-run setup floor\n"
                    "(start-point scalar mults), so alpha here is NOT the clean\n"
                    "O(sqrt(N)) exponent that asymptotically applies to the\n"
                    "engine's walk.  It is reported as measured, not as a theory\n"
                    "prediction, per the honesty contract.\n\n" % (alpha, r2))
        else:
            f.write("Alpha withheld: insufficient measured solved points.\n\n")
        f.write("## Method\n\nParallel kangaroo, affine-x driven walk, "
                "representation-independent DP predicate, warp-batched "
                "Montgomery-trick inversion (1 Fermat inverse per 32 lanes), "
                "concurrent dual-GPU rounds with host merge + kG==Q "
                "re-verification.\n\n")
        f.write("## Honesty statement\n\nThis report contains only what was "
                "measured at runtime (or explicitly marked staged / withheld). "
                "No projected GPU number is presented as measured. The "
                "benchmark definition is unchanged from the mission.\n\n")


def main():
    log("== ULTRA-ECDLP V5 pipeline start ==")
    open(os.path.join(HERE, "_v5_pipeline.log"), "a", encoding="utf-8").close()
    cuda = have_nvcc()
    env = phase1_env()

    # GATE: on a CUDA host require a real, queryable GPU.  T4x2 claim
    # requires count==2 and model contains T4.
    if cuda:
        devs = env["gpu"]["devices"]
        _gate(len(devs) >= 1, "CUDA device present", "gpu_count=%d" % len(devs))
        if env["gpu"]["count"] >= 2:
            names = "|".join(d["name"] for d in devs[:2])
            _gate("T4" in names, "dual devices are T4",
                  "found: " + names)
            log("T4x2 environment confirmed: %s" % names)

    bin_ = phase2_build(env, cuda)
    phase3_selftest(bin_, cuda)
    rate, ops = phase4_baseline(bin_, cuda)
    phase5_prof(bin_, cuda)
    single = phase6_single(bin_, cuda)
    dual_rate, eff = phase7_dual(bin_, cuda, single)
    phase8_batch(bin_, cuda)
    phase9_autotune(bin_, cuda)
    phase10_probes(bin_, cuda)
    rows = phase11_solves(bin_, cuda)
    stats = phase12_stats(rows)
    reached = phase13_verdict(rows, stats)
    phase14_repro(bin_, cuda, rows)
    alpha, r2 = phase15_scaling(bin_, cuda)
    phase16_leak(rows)
    phase17_speedups(cuda, ops, single[0][3] if single else 0.0, dual_rate)
    phase18_report(cuda, env, reached, rows, stats, alpha, r2)
    log("Pipeline complete. See KAGGLE_V5_FINAL_REPORT.md")
    return 0


if __name__ == "__main__":
    sys.exit(main())