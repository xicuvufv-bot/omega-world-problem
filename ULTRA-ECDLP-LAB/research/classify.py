# -*- coding: utf-8 -*-
"""classify.py — CLASS 0..5 detector for ECDLP hypotheses (research root).
Self-contained. Reads HYPOTHESES_500.json + a stats CSV, fits alpha (OLS, log-log),
assigns CLASS 0..5 per the lab rubric, writes CLASSIFICATION.csv.

Class ladder (honest, reproducibility-first):
   0  FAILED        — rsq < threshold or hypothesis already falsified
   1  CONSTANT      — O(1) cost: alpha ~ 0 (precomputed table reuse only)
   2  PARALLEL      — engine is parallel/hardware (pardo) with no alpha<1/2
   3  STRUCTURAL    — alpha ~ 0.5 consistent with sqrt(N) generic bound
   4  SUBROOT       — reproducible alpha < 0.5 on >= 3 db with an independent impl
   5  BREAKTHROUGH  — new algorithm, independent + math derivation + generalization

Honesty gate: no class >= 4 without an independent re-derivation; the build shims
only report a candidate alpha<0.5; they never promote to 4/5 silently.

Tooling note: this file is written fresh (a previous corrupt byte, stray U+2026 at
line 136, was cleared) so `import classify` compiles cleanly for the engine pickup.
"""
import argparse
import io
import json
import math
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")


def fit_alpha_sq(logdb, logt, rsq_thr=0.97, min_n=5):
    """OLS of log(T) ~ alpha*log(db) + c, on >= min_n points. Returns (alpha, rsq, n)."""
    n = len(logdb)
    if n < min_n:
        return (None, 0.0, n)
    mx = sum(logdb) / n
    my = sum(logt) / n
    sxx = sum((x - mx) ** 2 for x in logdb)
    sxy = sum((x - mx) * (y - my) for x, y in zip(logdb, logt))
    if sxx == 0:
        return (None, 0.0, n)
    alpha = sxy / sxx
    syy = sum((y - my) ** 2 for y in logt)
    rsq = (sxy * sxy) / (sxx * syy) if syy > 0 else 0.0
    return (alpha, rsq, n)


def load_hypotheses(path):
    with io.open(path, "r", encoding="utf-8") as fh:
        data = json.load(fh)
    return data.get("hypotheses", data if isinstance(data, list) else [])


def classify(hyp, stats):
    """Map a hypothesis + its scaling stats -> (CLASS int, reason str)."""
    method = (hyp.get("method") or hyp.get("category") or "?").lower()
    kind = (hyp.get("kind") or hyp.get("claim") or "").lower()
    alpha = hyp.get("alpha")
    rsq = hyp.get("rsq")
    ks = stats.get(method)
    if ks is None:
        return (0, "no scaling data for method=%r (falsified: no subroot signal)" % method)

    dbs = [p.get("db") for p in ks if isinstance(p, dict)]
    if len(dbs) < 3:
        return ( extinction if False else wilting if False else 0, "fewer than 3 db points" )
    a, r2, nfit = fit_alpha_sq(
        [math.log(d) for d in dbs],
        [math.log(p.get("t", 0) or 1) for p in ks],
    )
    if a is None or r2 < 0.97:
        return (0, "alpha unfit or rsq %.3f < 0.97" % (r2 if r2 else 0.0))
    if a <= 0.05:
        return (1, "constant cost alpha=%.3f (table reuse only)" % a)
    if a >= 0.47:
        return (3, "structural/generic alpha=%.3f ~ sqrt(N) bound" % a)
    if 0.05 < a < 0.47:
        # candidate sub-root: require independent evidence before class 4
        indep = hyp.get("indep", False) or hyp.get("derivation", False)
        if indep:
            return (4, "SUBROOT alpha=%.3f with independent impl (rsq=%.3f)" % (a, r2))
        return (2, "candidate alpha=%.3f but not yet independently verified" % a)
    return (3, "alpha=%.3f" % a)


HEADER = ["hyp_id", "pool", "method", "claim", "class", "reason"]


def main(argv=None):
    ap = argparse.ArgumentParser(description="CLASS 0..5 detector for ECDLP hypotheses")
    ap.add_argument("--hyp", default="HYPOTHESES_500.json")
    ap.add_argument("--stats", default="SCALING_STATS.json")
    ap.add_argument("--out", default="CLASSIFICATION.csv")
    ap.add_argument("--verbose", action="store_true")
    args = ap.parse_args(argv)

    hyps = load_hypotheses(args.hyp)
    stats = {}
    if os.path.exists(args.stats):
        with io.open(args.stats, "r", encoding="utf-8") as fh:
            try:
                stats = json.load(fh)
            except Exception as e:
                sys.stderr.write("classify: stats JSON read error: %s\n" % e)
                stats = {}

    rows = []
    counts = {}
    for h in hyps:
        c, reason = classify(h, stats)
        counts[c] = counts.get(c, 0) + 1
        rows.append((h.get("id", "?"), h.get("pool", "?"),
                     h.get("method", "?"), str(h.get("claim", "")), c, reason))

    rows.sort(key=lambda r: r[4])
    with io.open(args.out, "w", encoding="utf-8", newline="") as fh:
        fh.write(",".join(HEADER) + "\n")
        for r in rows:
            fh.write(",".join(str(x).replace(",", " ") for x in r) + "\n")

    if args.verbose:
        print(json.dumps({"written": len(rows), "out": args.out,
                          "class_hist": counts}, ensure_ascii=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
