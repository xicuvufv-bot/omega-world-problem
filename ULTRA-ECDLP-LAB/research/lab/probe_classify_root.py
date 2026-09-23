# -*- coding: utf-8 -*-
"""probe_classify_root.py — dump research-root classify.py bytes 133..139 safely
(ascii-escaped) + locate every U+2026 + compile status, so we can patch it right."""
import io, os, sys
sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")
LAB = os.path.dirname(os.path.abspath(__file__))     # research\lab
RESEARCH = os.path.dirname(LAB)                       # research
P = os.path.join(RESEARCH, "classify.py")
print("TARGET:", P, "exists=", os.path.isfile(P))
for alt in (os.path.join(LAB, "classify.py"), os.path.join(os.getcwd(), "classify.py")):
    print("  other:", alt, os.path.isfile(alt))
if not os.path.isfile(P):
    sys.exit(2)
raw = io.open(P, "rb").read()
lines = raw.split(b"\n")
print("N_LINES:", len(lines))
for i in range(133, 139):
    ln = lines[i] if i < len(lines) else b"<missing>"
    print("L%d ascii=%r" % (i + 1, ln.decode("utf-8", "backslashreplace")))
# find all U+2026
hits = []
for i, ln in enumerate(lines):
    if 0xE2 in ln:
        try:
            t = ln.decode("utf-8")
        except Exception:
            continue
        for j, ch in enumerate(t):
            if ch == "\u2026":
                hits.append((i + 1, j))
print("U+2026 COUNT:", len(hits), hits[:12])
try:
    compile(raw.decode("utf-8"), P, "exec")
    print("COMPILE: OK")
except SyntaxError as e:
    print("COMPILE: ERR line=%s col=%s msg=%s" % (e.lineno, e.offset, e.msg))
