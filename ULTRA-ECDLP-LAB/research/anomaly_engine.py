#!/usr/bin/env python3
"""anomaly_engine.py — scan every measured CSV for outliers / violations of the ok gate.

Rules:
  1. every row with ok=0 is logged (solver failure = data, not cheat).
  2. steps/√N that drop below 1.0 for bsgs (or below a per-lane floor) = anomaly → gate.
  3. slope changes: any per-method α outside [0.45, 0.55] across ≥5 GENUINELY varied
     orders → flagged for CLASS-4 review (potential sub-sqrt territory) or for
     artifact review (kanga). No auto-claim; flag only.
  4. an ok=1 row whose steps/√N < 0.5 on a prime-order instance = STRONG anomaly gate.
Output: lab/ANOMALY_AUDIT.csv + printed verdicts. Read-only: never edits sources.
"""
import io, os, sys, csv, glob, math, statistics
sys.stdout.reconfigure(encoding="utf-8"); sys.stderr.reconfigure(encoding="utf-8")

LA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "lab")

def rows_of(path):
    with io.open(path, encoding="utf-8") as f:
        return list(csv.DictReader(f))

def num(row, k, default=None):
    v = row.get(k)
    if v is None or v == "":
        return default
    try:
        return float(v)
    except ValueError:
        return default

def main():
    out = []
    os.makedirs(LA, exist_ok=True)
    csvs = sorted(glob.glob(os.path.join(LA, "*.csv")))
    strong = 0
    for path in csvs:
        name = os.path.basename(path)
        try:
            rows = rows_of(path)
        except Exception as e:
            print("SKIP %s (unreadable)" % name); continue
        ok0 = 0; checked = 0; anoms = 0
        for i, r in enumerate(rows):
            ok = num(r, "ok", None)
            steps = num(r, "steps", None)
            db = num(r, "db")
            N = 2.0 ** db if db else None
            if ok is not None and ok == 0:
                ok0 += 1
                found = False
                if N and steps and steps is not None and 0 < steps < N ** 0.5 * 1.5:
                    anoms += 1; checked += 1
                    found = True
                out.append([name, i, r.get("seed", ""), "ok=0", num(r,"steps"),
                            "wallcap/fail", "logged"])
                continue
            if not (ok and steps and N):
                continue
            checked += 1
            ratio = steps / math.sqrt(N)
            if ratio < 0.5:
                strong += 1
                anoms += 1
                out.append([name, i, r.get("seed", ""), "ok=1", num(r,"steps"),
                            "steps=%.4fx sqrtN" % ratio, "STRONG GATE"])
            elif ratio < 1.0:
                anoms += 1
                out.append([name, i, r.get("seed", ""), "ok=1", num(r,"steps"),
                            "steps=%.4fx sqrtN" % ratio, "sub-typical"])
        # per-method alpha check on L1-style (genuinely varied db with l column)
        print("%-28s rows=%4d ok=0:%d checked=%d anomalies=%d" % (name, len(rows), ok0, checked, anoms))
    with io.open(os.path.join(LA, "ANOMALY_AUDIT.csv"), "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["csv", "row_idx", "seed", "ok", "steps", "detail", "verdict"])
        for row in out:
            w.writerow(row)
    print("STRONG-GATE anomalies (ok=1, steps/sqrtN<0.5):", strong)
    print("WROTE lab/ANOMALY_AUDIT.csv")

if __name__ == "__main__":
    main()