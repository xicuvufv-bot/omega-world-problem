# -*- coding: utf-8 -*-
"""probe_tree_classify.py — walk the ENTIRE project tree for every classify.py,
byte-probe it, and report path + has-U+2026 + compile status. This finds the
classify.py that verify_engine's pickup actually resolved (which lives somewhere
my earlier probes missed)."""
import io, os, sys
sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

RESEARCH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # research root
LAB = os.path.dirname(os.path.abspath(__file__))                         # lab

roots = set()
for r in (RESEARCH, LAB, os.getcwd()):
    r = os.path.normpath(os.path.abspath(r))
    roots.add(r)

# also walk upward from research to project root
proj = os.path.dirname(RESEARCH)
while proj and proj != os.path.dirname(proj):
    roots.add(os.path.normpath(proj))
    proj = os.path.dirname(proj)

found = {}
for root in sorted(roots):
    if not os.path.isdir(root):
        continue
    for dirpath, dirnames, filenames in os.walk(root):
        for fn in filenames:
            if fn == "classify.py":
                p = os.path.join(dirpath, fn)
                if p in found:
                    continue
                try:
                    with io.open(p, "rb") as fh:
                        raw = fh.read()
                except Exception as e:
                    found[p] = "<READERR %s>" % e
                    continue
                nlines = raw.count(b"\n") + 1
                # line-136 null check + U+2026 detection
                lxs = raw.split(b"\n")
                l136 = lxs[135] if len(lxs) >= 136 else b"<no line 136>"
                has2026 = b"\xe2\x80\xa6" in raw
                try:
                    src = raw.decode("utf-8")
                except Exception as e:
                    found[p] = "<DECODEERR %s>" % e
                    continue
                try:
                    compile(src, p, "exec")
                    comp = "COMPILE-OK"
                except SyntaxError as e:
                    comp = "SYNTAX:@%s %s" % (e.lineno, e.msg)
                found[p] = (
                    "lines=%d hasU2026=%s L136=%r\n    compile=%s"
                    % (nlines, has2026, l136.decode("utf-8", "replace"), comp)
                )

print("ROOTS searched:", sorted(roots))
for p in sorted(found):
    print("=" * 70)
    print(p)
    print(found[p])
print("TOTAL classify.py found:", len(found))
