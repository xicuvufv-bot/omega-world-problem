# -*- coding: utf-8 -*-
"""probe_classify.py — find EVERY classify.py the verify_engine pickup could see and show
its line-136 bytes (repr, ASCII-safe) plus engine module resolution, verbatim from python.
Write-then-run (no heredoc, no shell quoting) to dodge PowerShell encoding issues."""
import io, os, sys
sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

HERE = os.path.dirname(os.path.abspath(__file__))
LAB = HERE
RESEARCH = os.path.dirname(HERE)
dbs = [LAB, RESEARCH, os.getcwd()]
for d in list(dbs):
    d = os.path.normpath(os.path.abspath(d))
    if d not in dbs:
        dbs.append(d)
    if d in dbs:
        pass

seen = {}
for d in dbs:
    if not os.path.isdir(d):
        continue
    for root, dirs, files in os.walk(d):
        for f in files:
            if f == "classify.py":
                p = os.path.join(root, f)
                if p in seen:
                    continue
                seen[p] = True
                L = io.open(p, encoding="utf-8").read().splitlines()
                n = len(L)
                one36 = repr(L[135]) if n >= 136 else "<n/a n=%d>" % n
                print("CLASSIFY:", p, "lines=%d" % n, "L136=", one36)

print("CWD:", os.getcwd())
print("PATHS:", dbs)
