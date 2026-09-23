# -*- coding: utf-8 -*-
"""probe_classify_all_tree.py — walk the ENTIRE ULTRA-ECDLP-LAB tree from its root,
find every classify.py, report path + byte-level line-136 probe + compile status."""
import io, os, sys
sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")
LAB = os.path.dirname(os.path.abspath(__file__))        # research\lab  (this file's home)
RESEARCH = os.path.dirname(LAB)                          # research
PROJECT = os.path.dirname(RESEARCH)                      # ULTRA-ECDLP-LAB
roots = [PROJECT]                                        # whole tree
found = {}
for r in roots:
    for root, dirs, files in os.walk(r):
        for f in files:
            if f == "classify.py":
                p = os.path.join(root, f)
                try:
                    raw = io.open(p, "rb").read()
                except Exception as e:
                    found[p] = "READERR %s" % e
                    continue
                lines = raw.split(b"\n")
                n = len(lines)
                l136 = lines[135] if n >= 136 else b"<no line136 n=%d>" % n
                l136s = repr(l136.decode("utf-8", "backslashreplace"))
                if 0x2026 in l136.decode("utf-8", "replace"):
                    flag = "HAS-U2026"
                else:
                    flag = "clean136"
                try:
                    compile(raw.decode("utf-8"), p, "exec")
                    st = "COMPILE-OK"
                except SyntaxError as e:
                    st = "SyntaxError line=%s col=%s: %s" % (e.lineno, e.offset, e.msg)
                found[p] = "n=%d flag=%s L136=%s | %s" % (n, flag, l136s, st)
print("TREE ROOT:", PROJECT)
for p in sorted(found):
    print(p)
    print("   ", found[p])
print("total classify.py in tree:", len(found))
