# -*- coding: utf-8 -*-
"""probe_classify_all.py — find every classify.py on the pickup candidate paths +
CWD, compile each, print per-path: resolve-order, line-136 byte-repr, compile status.
Ground truth for the stray-U+2026 fix, independent of read/glob display merging.
"""
import io, os, sys
sys.stdout.reconfigure(encoding="utf-8")

LAB = os.path.dirname(os.path.abspath(__file__))          # research\lab
RESEARCH = os.path.dirname(LAB)                            # research
HERE = LAB

cands = []
for d in (LAB, RESEARCH, os.getcwd()):
    d = os.path.normpath(os.path.abspath(d))
    if d not in cands:
        cands.append(d)

found = {}
for d in cands:
    for root, _dirs, files in os.walk(d):
        if "solvers" in root and "solvers.py" not in [f for f in files]:
            pass
        for f in files:
            if f == "classify.py":
                p = os.path.join(root, f)
                try:
                    src = io.open(p, encoding="utf-8").read()
                except Exception as e:
                    found.setdefault(p, "READERR: %s: %s" % (type(e).__name__, e))
                    continue
                lines = src.split("\n")
                l = lines[135] if len(lines) > 136 else "<no line 136: n=%d>" % len(lines)
                linfo = "L136=%r" % (l,)
                try:
                    compile(src, p, "exec")
                    st = "COMPILE-OK (%d lines)" % len(lines)
                except SyntaxError as e:
                    st = "SYNTAXERR: %s: %s (subline %s offset %s)" % (
                        type(e).__name__, e, e.lineno, e.offset)
                except Exception as e:
                    st = "ERR %s: %s" % (type(e).__name__, e)
                found.setdefault(p, "%s | %s" % (linfo, st))

# also record pickup candidates order so we know which path resolves first
print("CANDIDATE ORDER:", cands)
shown = 0
for p in sorted(found):
    shown += 1
    print(p)
    print("   ", found[p])
print("TOTAL classify.py reachable:", shown)

# and note which one the pickup would choose first
pick = None
for d in cands:
    p = os.path.join(d, "classify.py")
    if os.path.isfile(p):
        pick = p
        break
print("PICKUP-FIRST:", pick)
