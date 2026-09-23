# -*- coding: utf-8 -*-
"""patch_line27.py: fix the runaway ')' that closes dict( prematurely on line 27 of
hypothesis_gen.py. The facts list should close with ']' then comma to continue onto
group=/sec=. Uses only stdlib, UTF-8, deterministic. Safe to run any number of times."""
import io, sys
p = 'hypothesis_gen.py'
s = io.open(p, encoding='utf-8').read()
target = 'mod l)"]),'
repl   = 'mod l)"],'
n = s.count(target)
s = s.replace(target, repl)
io.open(p, 'w', encoding='utf-8', newline='').write(s)
compile(io.open(p, encoding='utf-8').read(), p, 'exec')
print(f'PATCHED occurrences={n} :: hypothesis_gen.py now compiles')
