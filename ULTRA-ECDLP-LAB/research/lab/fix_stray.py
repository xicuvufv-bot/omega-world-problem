# -*- coding: utf-8 -*-
"""fix_stray.py - move premature ')' inside strings:  c?")  ->  c?)"
The W-pool 3-tuples were written as ('...c?")  which closes the tuple after
element 1, orphaning 'amortized M'/'t'. Moving the ')' inside the string
(re-hiding the close of the '...2^db/2/c?' text) restores the 3-tuple.
Also sweeps the same pattern everywhere (covers line 27-style variants)."""
import io

P = 'hypothesis_gen.py'
s = io.open(P, encoding='utf-8', newline='').read()
cA = s.count('c?")')
s = s.replace('c?")', 'c?)"')
io.open(P, 'w', encoding='utf-8', newline='').write(s)
# compile-check the whole file
src = io.open(P, encoding='utf-8', newline='').read()
compile(src, P, 'exec')
print('OK compile; swept c?"->c?) occurrences:', cA)
