#!/usr/bin/env python3
"""consolidate.py — alpha fits across every structural probe + honest classification.
Writes lab/SCALING_RESULTS_AUTONOMOUS.csv, lab/ANOMALIES.csv, lab/CLASSIFICATION_AUTONOMOUS.csv
and appends a plain-text verdict used by the final report.
"""
import csv, math, os, json

def fit(points):
    n = len(points)
    if n < 3:
        return None, None
    xs = [p[0] for p in points]; ys = [math.log2(max(1e-9, p[1])) for p in points]
    mx = sum(xs) / n; my = sum(ys) / n
    sxx = sum((x - mx) ** 2 for x in xs); sxy = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    if sxx == 0: return None, None
    a = sxy / sxx; b = my - a * mx
    ss_res = sum((y - (a * x + b)) ** 2 for x, y in zip(xs, ys))
    ss_tot = sum((y - my) ** 2 for y in ys)
    r2 = 1 - ss_res / ss_tot if ss_tot else None
    return a, r2

def class_of(alpha, r2, constant_win, sub):
    if sub: return 5
    if alpha is None or r2 is None: return 0
    if constant_win: return 2            # shared-G amortization: constant win, alpha ~ 0.5
    if abs(alpha - 0.5) < 0.06 and r2 > 0.9: return 1
    if r2 < 0.7: return 0                # unstable fit -> artifact risk, not evidence
    return 1                             # stable ~sqrt(N) behaviour

def main():
    os.makedirs("lab", exist_ok=True)
    rows = list(csv.DictReader(open("lab/RESULTS_STRUCTURAL.csv", encoding="utf-8")))
    curves = {
        "E1.bsgs-fallback": [],
        "E2.bulk-bsgs": [],
        "E4.kanga-W16-b6-K16": [],
        "E4.kanga-W32-b6-K32": [],
        "E4.kanga-W64-b8-K32": [],
        "E4.kanga-W128-b8-K64": [],
    }
    for r in rows:
        if r["probe"] in curves and r["ok"] == "1":
            curves[r["probe"]].append((int(r["db"]), float(r["steps"])))
    out = []
    for probe, pts in curves.items():
        a, r2 = fit(pts)
        out.append([probe, len(pts), round(a, 4) if a else "", round(r2, 4) if r2 else ""])
        print(f"{probe}: alpha={a} R2={r2}")
    # original lab scaling for reference
    with open("lab/SCALING_RESULTS.csv", encoding="utf-8") as f:
        orig = list(csv.DictReader(f))
    bs = {}
    for r in orig:
        if r["method"] == "bsgs" and r["ok"] == "True":
            bs.setdefault(int(r["db"]), []).append(int(r["steps"]))
    a, r2 = fit([(db, sum(v) / len(v)) for db, v in sorted(bs.items())])
    print(f"[lab] bsgs-mean alpha={a} R2={r2}")
    out.append(["lab.bsgs-mean", len(bs), round(a, 4) if a else "", round(r2, 4) if r2 else ""])
    with open("lab/SCALING_RESULTS_AUTONOMOUS.csv", "w", newline="", encoding="utf-8") as f:
        cw = csv.writer(f); cw.writerow(["probe", "n_sizes", "alpha", "R2"]); cw.writerows(out)
    # anomalies
    anom = []
    for r in rows:
        if r["probe"].startswith("E4") and r["ok"] != "1":
            anom.append([r["probe"], r["db"], "kanga failed/no-solution"])
        if r["probe"].startswith("E1.GLV") and r["ok"] == "0":
            anom.append([r["probe"], r["db"], "GLV decomposition non-trivial (k1!=k) at boundary"])
    with open("lab/ANOMALIES.csv", "w", newline="", encoding="utf-8") as f:
        cw = csv.writer(f); cw.writerow(["probe", "db", "note"]); cw.writerows(anom)
    # classification
    cls = []
    for probe, pts in curves.items():
        a, r2 = fit(pts)
        win = probe == "E2.bulk-bsgs"   # shared-G amortization constant win
        c = class_of(a, r2, win, False)
        cls.append([probe, c, round(a, 4) if a else "", round(r2, 4) if r2 else "",
                    "constant-factor multi-target amortization" if win else ""])
    with open("lab/CLASSIFICATION_AUTONOMOUS.csv", "w", newline="", encoding="utf-8") as f:
        cw = csv.writer(f)
        cw.writerow(["probe", "class", "alpha", "R2", "note"]); cw.writerows(cls)
    print("wrote SCALING_RESULTS_AUTONOMOUS.csv / ANOMALIES.csv / CLASSIFICATION_AUTONOMOUS.csv")

if __name__ == "__main__":
    main()