"""Keyspace engineering: bounds, hex packaging, and interval splitting.

A scan may target the FULL official interval of a puzzle or a SUB-RANGE of it
(user must stay inside the puzzle's own interval — that is enforced against
the registry). For multi-GPU / multi-host work the interval is cut into M
equal shares (share index 0..M-1). BitCrack consumes ``START:END`` hex pairs
or ``M/N`` share fractions; Kangaroo consumes [start, end] hex lines.
"""

from .registry import RegistryError


def validate_subrange(puzzle, start_hex, end_hex):
    """Return (start, end) ints; refuse anything outside the puzzle interval."""
    lo, hi = puzzle.lo, puzzle.hi
    start = int(start_hex, 16) if start_hex else lo
    end = int(end_hex, 16) if end_hex else hi
    if start < lo or start > hi:
        raise RegistryError(
            "start 0x%x is outside puzzle #%d interval [0x%x, 0x%x]"
            % (start, puzzle.n, lo, hi))
    if end < lo or end > hi:
        raise RegistryError(
            "end 0x%x is outside puzzle #%d interval [0x%x, 0x%x]"
            % (end, puzzle.n, lo, hi))
    if start > end:
        raise RegistryError("start 0x%x > end 0x%x" % (start, end))
    return start, end


def default_hex_upper(v):
    return "%x" % v


def full_keyspace(puzzle):
    return "%x:%x" % (puzzle.lo, puzzle.hi)


def split_equal(puzzle, m):
    """Split puzzle interval into m contiguous shares.

    Returns list of (share_idx, start_hex, end_hex). Each share is
    exactly fitted to m; remainder is folded into the first share.
    """
    if m < 1:
        raise ValueError("m must be >= 1")
    lo, hi = puzzle.lo, puzzle.hi
    total = hi - lo + 1
    base = total // m
    rem = total % m
    out = []
    cur = lo
    for i in range(m):
        size = base + (1 if i < rem else 0)
        if size <= 0:
            continue
        end = cur + size - 1
        out.append((i, "%x" % cur, "%x" % end))
        cur = end + 1
    return out


def progress_fraction(start, end, puzzle):
    """0..1 fraction of the puzzle interval already covered by [start, end]."""
    width = puzzle.hi - puzzle.lo + 1
    return (min(end, puzzle.hi) - max(start, puzzle.lo) + 1) / float(width)


def eta_seconds(keys_remaining, keys_per_second):
    if keys_per_second <= 0:
        return float("inf")
    return keys_remaining / keys_per_second


def human_seconds(secs):
    secs = float(secs)
    if secs == float("inf"):
        return "infinite"
    for unit, div in (("y", 365 * 24 * 3600), ("d", 24 * 3600),
                      ("h", 3600), ("m", 60)):
        if secs >= div:
            return "%.2f %s" % (secs / div, unit)
    return "%.1f s" % secs


def fmt_hex_key(k):
    return "%064x" % k


def bitcheck_load(bits, keys_per_second):
    """Rough per-puzzle full-interval wall-clock (single engine)."""
    width = 1 << (bits - 1)
    return eta_seconds(width, keys_per_second)