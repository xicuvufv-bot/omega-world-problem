"""Solver v1 — naive per-key scan.

For every k in [lo, hi] derives the full public key (one full scalar
multiplication per key) and compares hash160(pubkey) to the target. This is
the correctness baseline every faster version is measured against.
"""

from algorithms.curve import scalar_mult, compressed
from algorithms.hash import hash160


def scan_naive(target_h160: bytes, lo: int, hi: int, limit: int = None):
    """Return the first k in [lo, hi] with hash160(k) == target_h160, else None."""
    n = 0
    for k in range(lo, hi + 1):
        n += 1
        if limit is not None and n > limit:
            return None
        if hash160(compressed(scalar_mult(k))) == target_h160:
            return k
    return None