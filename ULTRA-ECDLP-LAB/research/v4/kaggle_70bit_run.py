#!/usr/bin/env python3
# ============================================================
# kaggle_70bit_run.py -- orchestrator for the 70-bit interval
# ECDLP payload (ULTRA-ECDLP-LAB / research/v4).
#
# Pipeline on the GPU box (Kaggle T4 or T4x2, CUDA 12.x):
#   1. detect nvcc; BUILD kangaroo_cuda (sm_75 / sm_86)
#   2. GATE: run `selftest` (known 24-bit key, on-device, k must
#      match).  ABORT on failure -- nothing measured counts.
#   3. bench throughput -> AUTOTUNE rows + rate for projections
#   4. solve all 10 instances from challenges.json with a hook
#      watchdog (per-instance wall budget, default 1200 s),
#      parse out.json, and INDEPENDENTLY verify k*G == Q in pure
#      Python before a row counts as solved.
#   5. write AUTOTUNE.csv / 70BIT_CHALLENGE.csv /
#      FINAL_PERFORMANCE.csv + KAGGLE_70BIT_FINAL_REPORT.md
#
# NO-CUDA fallback (must NOT fake anything): rows marked staged,
# measured rows come only from the validated local CPU engine
# (v4_cpu_engine.exe, BASELINE_cpu.csv).  Local verdict:
#   TARGET_20MIN = NOT_REACHED.
#
# Honesty contract (STATE_SNAPSHOT.md): every GPU figure is
# measured at runtime on the actual hardware; independence
# verification gates each solve; the report never equates
# projection with measurement.
# ============================================================
import csv
import json
import os
import shutil
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
CHALLENGES = os.path.join(HERE, "challenges.json")
BIN = os.path.join(HERE, "kangaroo_cuda")
SELFTEST_JSON = os.path.join(HERE, "_selftest_challenge.json")
TARGET_20MIN_S = 1200.0   # per-instance wall budget
INSTALLED = 10
CLOCK_HZ = 2.0e9          # projected scalar-mult cost floor (see report)

# ---------------- secp256k1 independent verifier ----------------
P = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
N = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
GX = 0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798
GY = 0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8


def modinv(a, m):
    return pow(a, -1, m)


def point_add(p, q):
    if p is None:
        return q
    if q is None:
        return p
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
    R = None
    base = point
    while k > 0:
        if k & 1:
            R = point_add(R, base)
        base = point_add(base, base)
        k >>= 1
    return R


def verify_kQ(khex, Qx, Qy, bits):
    """Independent: k in interval AND k*G solves Q."""
    try:
        k = int(khex, 16)
    except (ValueError, TypeError):
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


# ---------------- toolchain / build ----------------
def have_nvcc():
    return shutil.which("nvcc") is not None


def build():
    nvcc = shutil.which("nvcc")
    src = os.path.join(HERE, "kangaroo_cuda.cu")
    arch = "sm_86"   # A100/V100-class safest on Kaggle; T4=sm_75 fallback below
    cmd = [nvcc, "-O3", "-std=c++17", "-arch=sm_75", "-Xptxas", "-O3",
           "-lineinfo", "-maxrregcount=80", "-o", BIN, src]
    subprocess.run(cmd, cwd=HERE, check=True)
    return BIN


def run(args, timeout, cwd=HERE):
    """Run the payload, return (rc, elapsed_s, stdout)."""
    t0 = time.time()
    try:
        p = subprocess.run(args, cwd=cwd, capture_output=True, text=True,
                           timeout=timeout)
        return p.returncode, time.time() - t0, p.stdout, p.stderr
    except subprocess.TimeoutExpired as e:
        return 124, time.time() - t0, (e.stdout or ""), "timeout-expired"


def parse_out(out_json, bits):
    """Return (solved, khex, steps, time_ms) from payload out.json."""
    try:
        with open(out_json) as f:
            o = json.load(f)
        return (bool(o.get("solved")), o.get("k", ""), int(o.get("steps", 0)),
                float(o.get("time_ms", 0.0)))
    except (OSError, ValueError):
        return False, "", 0, 0.0


# ---------------- productive path (GPU box) ----------------
def gpu_run():
    print("== CUDA toolchain found: productive path ==")
    build()
    print("built: %s" % BIN)

    # GATE: selftest must solve a KNOWN 24-bit key on-device.
    rc, el, out, err = run([BIN, "selftest"], 600)
    print(out, err or "")
    if rc != 0:
        print("GATE FAILED (selftest rc=%d): abort, nothing counted." % rc)
        sys.exit(1)
    print("GATE PASSED (selftest k-match on-device): bench+solve enabled.")

    # bench -> aggregate steps/s (dpbits=24 default)
    rc, el, out, err = run([BIN, "bench", "5", "24"], 120)
    print(out, err or "")
    if rc != 0:
        print("bench failed rc=%d" % rc)
        sys.exit(1)
    # parse "bench: X s, N steps, R steps/s aggregate"
    rate = 0.0
    for line in out.splitlines():
        if line.startswith("bench:"):
            parts = line.split(",")
            try:
                rate = float(parts[2].split("steps/s")[0].strip())
            except (ValueError, IndexError):
                pass
    gpu_rate = rate

    autotune = [("bits", "dpbits", "nstart", "rate_steps_per_s", "src")]
    autotune.append((40, 24, 1 << 20, gpu_rate, "gpu_bench"))
    for line in out.splitlines():
        print("  " + line)

    solved_rows = []
    instances = load_instances()
    # per-instance watchdog: hard budget plus a grace mask
    for inst in instances:
        idx, bits = inst["index"], inst["bits"]
        outj = os.path.join(HERE, "_solve_%d.json" % idx)
        budget = TARGET_20MIN_S
        rc, el, out, err = run(
            [BIN, "solve", CHALLENGES, str(idx), outj, "24", "19", "19"],
            budget + 30.0)
        solved, khex, steps, tms = parse_out(outj, bits)
        shipped = solved and bool(khex)
        v_ok = shipped and verify_kQ(khex, inst["Qx"], inst["Qy"], bits)
        counted = bool(v_ok) and el <= budget
        solved_rows.append({
            "index": idx, "bits": bits, "seed": inst["seed"],
            "k": inst["k"], "solved_native": int(solved),
            "verify": int(bool(v_ok)), "counted": int(counted),
            "steps": steps, "time_s": round(el, 3),
            "rc": rc, "note": "", "rate": (steps / el) if el > 0 else 0.0,
        })
        print("instance %d: solved=%d verify=%d counted=%d time=%.1fs" %
              (idx, int(solved), int(bool(v_ok)), int(counted), el))
        if not counted:
            solved_rows[-1]["note"] = "unverified_or_timeout"

    write_outputs(solved_rows, autotune, gpu_rate, proven=True)
    print("GPU run complete.")


# ---------------- honest no-CUDA fallback ----------------
def local_only():
    print("== no nvcc: LOCAL-ONLY honest path ==")
    print("  CUDA payload is STAGED ONLY; no GPU figure is claimed.")
    # measured CPU baseline: parse BASELINE_cpu.csv if present
    csv_path = os.path.join(HERE, "BASELINE_cpu.csv")
    cpu_rows = []
    if os.path.exists(csv_path):
        with open(csv_path) as f:
            for r in csv.DictReader(f):
                cpu_rows.append(r)
    # projected GPU figures are NOT measured: carry rate=0 and flag staged.
    write_outputs([], [], 0.0, proven=False, cpu_rows=cpu_rows)
    print("Wrote honest CSV/report with TARGET_20MIN = NOT_REACHED.")


# ---------------- outputs ----------------
def write_outputs(solved_rows, autotune, rate, proven, cpu_rows=None):
    # ---- AUTOTUNE.csv ----
    with open(os.path.join(HERE, "AUTOTUNE.csv"), "w", newline="",
              encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["bits", "dpbits", "nstart", "rate_steps_per_s", "src"])
        for r in autotune:
            w.writerow(r)
        if cpu_rows:
            for r in cpu_rows:
                w.writerow([r["bits"], 12, r["threads"],
                            r["rate_steps_per_s"], "cpu_measured"])

    # ---- 70BIT_CHALLENGE.csv ----
    with open(os.path.join(HERE, "70BIT_CHALLENGE.csv"), "w", newline="",
              encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["index", "bits", "seed", "k", "solved", "verify",
                    "counted", "steps", "time_s", "rate_steps_per_s",
                    "rc", "note", "staged"])
        for r in solved_rows:
            w.writerow([r["index"], r["bits"], r["seed"], r["k"],
                        r["solved_native"], r["verify"], r["counted"],
                        r["steps"], r["time_s"], r["rate"], r["rc"],
                        r["note"], 0])
        for inst in load_instances():
            if not any(r["index"] == inst["index"] for r in solved_rows):
                w.writerow([inst["index"], inst["bits"], inst["seed"],
                            inst["k"], "", "", "", "", "", "", "", "staged", 1])

    # ---- FINAL_PERFORMANCE.csv ----
    nonzero = [r for r in solved_rows if r["rate"] > 0]
    mean_rate = (sum(r["rate"] for r in nonzero) / len(nonzero)) if nonzero else rate
    counted = sum(r["counted"] for r in solved_rows)
    total_steps = sum(r["steps"] for r in solved_rows)
    total_time = sum(r["time_s"] for r in solved_rows)
    with open(os.path.join(HERE, "FINAL_PERFORMANCE.csv"), "w", newline="",
              encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["metric", "value", "proven"])
        w.writerow(["target", "T4x2? 10x[2^69,2^70) <=20min", proven])
        w.writerow(["instances_counted_solved", counted, proven])
        w.writerow(["measured_rate_steps_per_s", mean_rate if proven else 0, proven])
        w.writerow(["total_steps", total_steps, proven])
        w.writerow(["total_time_s", round(total_time, 3), proven])
        w.writerow(["verdict_20min", "REACHED" if (proven and counted == 10
                    and total_time <= TARGET_20MIN_S * INSTALLED) else
                    "NOT_REACHED", proven])

    # ---- Markdown report ----
    with open(os.path.join(HERE, "KAGGLE_70BIT_FINAL_REPORT.md"), "w",
              newline="\n", encoding="utf-8") as f:
        f.write("# KAGGLE 70-BIT FINAL REPORT — ULTRA-ECDLP-LAB\n\n")
        f.write("Synthetic interval ECDLP: secp256k1, k in [2^69, 2^70), "
                "%d independent instances. Target: solve all below 20 min wall.\n\n"
                % INSTALLED)
        f.write("## Verdict\n\n")
        f.write("**TARGET_20MIN = ** " +
                ("REACHED" if (proven and counted == 10
                               and total_time <= TARGET_20MIN_S * INSTALLED)
                 else "NOT_REACHED") +
                "  \n")
        f.write("Every figure below is ")
        if proven:
            f.write("**measured at runtime on the GPU box** and every counted "
                    "solve was independently verified k*G == Q in Python.\n\n")
        else:
            f.write("**NOT measured.** CUDA payload is STAGED ONLY (no nvcc "
                    "on this box); local rows are CPU baseline. Nothing here "
                    "claims GPU performance.\n\n")
        f.write("## Results\n\n")
        f.write("| index | solved | verified | steps | time (s) |\n")
        f.write("|---|---|---|---|---|\n")
        written = set()
        for r in solved_rows:
            written.add(r["index"])
            f.write("| %d | %d | %d | %d | %.1f |\n" %
                    (r["index"], r["solved_native"], r["verify"],
                     r["steps"], r["time_s"]))
        for inst in load_instances():
            if inst["index"] not in written:
                f.write("| %d | -- | -- | -- | staged |\n" % inst["index"])
        f.write("\n## Measured rate\n\n")
        if proven:
            f.write("Aggregate steps/s (measured): %.3e\n\n" % rate)
        else:
            f.write("No GPU measurement (no CUDA toolchain locally). "
                    "Projected GPU steps/s are withheld rather than "
                    "fabricated.\n\n")
        if cpu_rows:
            f.write("Local CPU reference (measured, v4_cpu_engine, dpb=12): "
                    "%.0f steps/s derived from BASELINE_cpu.csv rows.\n\n"
                    % float(cpu_rows[-1]["rate_steps_per_s"]))
        f.write("## Method\n\n"
                "Parallel kangaroo with affine-x-driven walk and "
                "representation-independent DP predicate (fix for the v4 CPU "
                "bug class).  Per-step inversion warp-batched (Montgomery "
                "trick, 1 Fermat inverse per 32 lanes).  Recovered k is "
                "re-checked in the payload (k*G==Q) and independently in "
                "Python by this orchestrator before counting.\n\n")
        f.write("## Reproduce\n\n")
        if os.path.exists(os.path.join(HERE, "v4_cpu_engine.exe")):
            f.write("Local CPU baseline: `v4_cpu_engine.exe` "
                    "(validated selftest + scale).\n\n")
        f.write("GPU box:\n```\n"
                "nvcc -O3 -std=c++17 -arch=sm_75 -Xptxas -O3 -lineinfo \\\n"
                "  -maxrregcount=80 -o kangaroo_cuda kangaroo_cuda.cu\n"
                "./kangaroo_cuda selftest      # gate: known-key, must match\n"
                "python kaggle_70bit_run.py    # bench + 10 solves + verify\n"
                "```\n")
    print("wrote AUTOTUNE.csv / 70BIT_CHALLENGE.csv / FINAL_PERFORMANCE.csv / "
          "KAGGLE_70BIT_FINAL_REPORT.md")


def main():
    if have_nvcc():
        gpu_run()
    else:
        local_only()
    return 0


if __name__ == "__main__":
    sys.exit(main())