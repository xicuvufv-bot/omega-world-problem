# -*- coding: utf-8 -*-
"""fix27.py — surgical fix for hypothesis_gen.py line 27/28 orphan + W-pool imbalance.
Deterministic single-target replacements + syntax check. Safe to re-run."""
import io, sys

P = 'hypothesis_gen.py'
src = io.open(P, encoding='utf-8', newline='').read()

# 1) TOY dict: line carrying facts ends with '"]),' but is inside a dict( that continues
#    with group=/sec= on the next line -> the unexpected ')' closes dict prematurely.
old1 = '"curve is ordinary (t=100004, t\\u22600 mod l)"]),'
new1 = '"curve is ordinary (t=100004, t\\u22600 mod l)"],'
c1 = src.count(old1)
src = src.replace(old1, new1)

# 2) the whole dict must still close: the next line is
#    '          group="toy-prime", sec={"method": "kangs-BSGS", "alpha": 0.5, "const": 2.0})'
#    after removal of its own stray ')' the dict( remaining open gets closed by that line's
#    terminal ')'.  Nothing else to change for TOY.

# 3) W pool line: '("make tame table once for {G,db}, solve M Q's online (expected per-Q = 2^db/2/c?"),'
#    The closing `('` of dict(...) analogy: this is a stray ')' after the string closing query '?'.
#    It sits INSIDE a 3-tuple ('...?', 'amortized M', 't').  Removing the stray paren.
old3 = '(expected per-Q = 2^db/2/c?")), "amortized M", "t"),'
new3 = '(expected per-Q = 2^db/2/c?)" ), "amortized M", "t"),'
c3 = src.count(old3)
src = src.replace(old3, new3)

io.open(P, 'w', encoding='utf-8', newline='').write(src)
compile(io.open(P, encoding='utf-8').read(), P, 'exec')
print('OK: replaced1=%d replaced3=%d ; compile PASS' % (c1, c3))
