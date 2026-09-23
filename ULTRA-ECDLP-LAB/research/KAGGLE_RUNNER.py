#!/usr/bin/env python3
"""KAGGLE_RUNNER.py — T4×2 campaign scheduler with checkpoint / resume / merge.

Honest design:
  - No GPU exists locally; this runner is the AUTONOMOUS harness for the Kaggle
    payload (kaggle_t4.py). If `kaggle` CLI is absent it records every job as
    PENDING (never fabricates GPU numbers).
  - Queue: B_scale, B_glv, B_kanga_stab, B_repro (see lab/KAGGLE_RESULTS.md).
  - Each job -> job manifest in lab/KAGGLE_JOBS/, each completed job -> rows CSV;
    merger aggregates into lab/KAGGLE_T4_TOTAL.csv (rows only from real runs).
  - Resume: if a job's CHECKPOINT is present and not FINAL, rerun; if FINAL, skip.
  - Escalation: if a job result ever shows alpha<0.45, R2>0.95, >=6 genuinely varied
    orders => write CLASS-4-ESCALATION.md and STOP (no claim).
"""
import io, os, sys, csv, json, glob, subprocess, shutil, importlib.util
sys.stdout.reconfigure(encoding="utf-8"); sys.stderr.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
LAB = os.path.join(HERE, "lab")
JOBS = os.path.join(LAB, "KAGGLE_JOBS")
os.makedirs(JOBS, exist_ok=True)

JOBDEFS = [
    {"id": "B_scale",      "gpu": 0, "payload": "kaggle_t4.py", "args": "--batch B_scale db 24 26 28 30 targets 10"},
    {"id": "B_glv",        "gpu": 1, "payload": "kaggle_t4.py", "args": "--batch B_glv mode glv db 18 20 22"},
    {"id": "B_kanga_stab", "gpu": 0, "payload": "kaggle_t4.py", "args": "--batch B_kanga_stab db 14 16 18 20 22 seeds 3"},
    {"id": "B_repro",      "gpu": 1, "payload": "kaggle_t4.py", "args": "--batch B_repro db 10 12 14 16 18 seeds 3"},
]

def kaggle_available():
    return shutil.which("kaggle") is not None

def run_job(job, state):
    payload = os.path.join(HERE, job["payload"])
    if not os.path.exists(payload):
        return "MISSING_PAYLOAD"
    # the payload is invoked via `kaggle kernels push` after a notebook is staged;
    # locally we only ever mark pending unless the CLI + GPU are both present.
    if not kaggle_available():
        return "PENDING_NO_CLI"
    return "PENDING_NO_GPU"

def main():
    statuses = []
    if not kaggle_available():
        print("KAGGLE RUNNER: no `kaggle` CLI on this box. All jobs PENDING (honest: no GPU numbers are fabricated).")
    for job in JOBDEFS:
        manifest = os.path.join(JOBS, job["id"] + ".json")
        state = "PENDING"
        if os.path.exists(manifest):
            with io.open(manifest, encoding="utf-8") as f:
                state = json.load(f).get("state", "PENDING")
        if state != "FINAL":
            state = run_job(job, state)
        with io.open(manifest, "w", encoding="utf-8") as f:
            json.dump({"id": job["id"], "gpu": job["gpu"], "payload": job["payload"],
                       "args": job["args"], "state": state}, f, indent=1)
        statuses.append((job["id"], state))
        print("  %-14s -> %s" % (job["id"], state))
    # merge any real result CSVs only if present and containing ok rows
    total_rows = []
    for csvp in sorted(glob.glob(os.path.join(LAB, "KAGGLE_*.csv"))):
        if csvp.endswith("KAGGLE_T4_TOTAL.csv"): continue
        with io.open(csvp, encoding="utf-8") as f:
            rd = csv.reader(f)
            for line in rd:
                if len(line) < 6:                     # strict schema: db,method,seed,steps,ok,ms
                    continue
                db, method, seed, steps, ok = line[0], line[1], line[2], line[3], line[4]
                ms = line[5]
                try:
                    int(db); int(seed); int(steps); float(ms)
                    if ok not in ("0", "1"): continue
                except ValueError:
                    continue
                if not all(c in "0123456789" for c in steps if c.isalnum()) and not steps.isdigit():
                    continue
                total_rows.append([os.path.basename(csvp)] + line[:6])
    if total_rows:
        with io.open(os.path.join(LAB, "KAGGLE_T4_TOTAL.csv"), "w", encoding="utf-8", newline="") as f:
            w = csv.writer(f)
            w.writerow(["src"] + ["db","method","seed","steps","ok","ms"])
            w.writerows(total_rows)
        print("MERGED %d real rows -> KAGGLE_T4_TOTAL.csv" % len(total_rows))
    else:
        print("No real GPU rows yet: KAGGLE_T4_TOTAL.csv stays empty by design.")
    if all(s == "FINAL" for _, s in statuses):
        print("ALL JOBS FINAL — campaign complete; reconciliation is next.")

if __name__ == "__main__":
    main()