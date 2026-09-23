# -*- coding: utf-8 -*-
"""fix_classify_stats.py — bytes-level, deterministic repair of lab\\classify.py line 136.

Known corruption class (symbol gobble):  '_load_csv_stats(args.stats, statsyata<cRANGE…>)'
was written with a U+2026 swallowing the closing paren of the second argument token
'stats'. Intended line: '_load_csv_stats(args.stats, stats)'.

Replace every '<MANGLE-PREFIX>…' pattern of unknown length bounded by the parser:
we know the token must equal 'stats' (the in-scope dict accumulator) followed by ')'.
So: scan bytes for the literal 'statsyata' prefix + any run of non-ASCII (the U+2026),
and rewrite as 'stats'. Also assert the line then compiles.

No shell quoting involved: this runs as a plain file.
"""
import io

P = 'classify.py'

def _fix_bytes(b):
    # the corruption: b'statsyata' + U+2026 bytes (E2 80 A6) (+ possibly more gobble) then b')'
    key = 'statsyata'.encode('utf-8')
    out = bytearray()
    idx = 0
    hits = 0
    while True:
        i = b.find(key, idx)
        if i < 0:
            out += b[idx:]
            break
        j = i + len(key)
        # skip any run of bytes that decode as continuation characters (the gobbled tail)
        while j < len(b) and (b[j] & 0xC0) == 0x80:
            j += 1
        # also skip U+2026 E2 80 A6 if it leaked (already covered by continuation rule for A6,
        # but lead byte E2 isn't a continuation) - handle explicitly
        while j + 2 < len(b) and b[j:j+3] == '\u2026'.encode('utf-8'):
            j += 3
        out += b[idx:i]
        out += 'stats'.encode('utf-8')   # deterministic intended token
        hits += 1
        idx = j
    return bytes(out), hits

raw = io.open(P, 'rb').read()
fixed, hits = _fix_bytes(raw)
io.open(P, 'wb').write(fixed)
# any leftover stray non-ASCII in code positions will surface here:
compile(fixed.decode('utf-8'), P, 'exec')
print('fix_classify_stats: hits=%d bytes %d->%d compile=PASS' % (hits, len(raw), len(fixed)))
