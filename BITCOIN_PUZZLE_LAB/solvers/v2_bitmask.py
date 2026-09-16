"""Solver v2 — stride scan with a hash160 bitmask prefilter.

Improvement over v1: instead of one full scalar multiplication per key, the
running point is advanced by a *single mixed point addition* (P += G) per key.
The hash160 bitmask prefilter optionally skips buckets we know contain no
target before doing the full hash comparison — an efficiency trick copied from
historical GPU solvers that scanned many addresses at once.

For a single target the mask can't skip anything (every bucket equals the
target's bucket), which we *measure* in benchmarks/bitmask.json rather than
hand-waving about.
"""

import time

from algorithms.curve import scalar_mult, jac_add_affine, compressed, Gx, Gy
from algorithms.hash import hash160


def build_bitmask(target_hashes, first_bits: int = 16):
    """Set of (first_bits) hash160 prefixes that contain at least one target."""
    keys = set()
    shift = 160 - first_bits
    for h in target_hashes:
        keys.add(int.from_bytes(h, "big") >> shift)
    return keys


def solve_stride(target_h160: bytes, lo: int, hi: int, stride: int = 1,
                 limit: int = None):
    """Advance one point-add per key; return matching k or None. Uses stride 1."""
    if stride != 1:
        raise NotImplementedError("multi-key stride histogram planned in v2-next")
    P = scalar_mult(lo)
    n = 0
    for k in range(lo, hi + 1):
        n += 1
        if limit is not None and n > limit:
            return None
        if hash160(compressed(P)) == target_h160:
            return k
        P = jac_add_affine(P, Gx, Gy)
    return None


def scan_masked(target_h160: bytes, lo: int, hi: int, mask=None,
                first_bits: int = 16, limit: int = None,
                max_seconds: float = None):
    """Stride scan; every key is bitmask-tested before the full hash compare.
    ``mask`` is the set built by build_bitmask for the *same* first_bits."""
    P = scalar_mult(lo)
    t0 = time.monotonic()
    n = 0
    shift = 160 - first_bits
    target_bucket = int.from_bytes(target_h160, "big") >> shift
    hits = 0
    for k in range(lo, hi + 1):
        n += 1
        if limit is not None and n > limit:
            return None
        if mask is not None and target_bucket not in mask:
            # can never match: the whole bucket is empty of targets
            P = jac_add_affine(P, Gx, Gy)
            continue
        if int.from_bytes(hash160(compressed(P)), "big") >> shift == target_bucket:
            hits += 1
            if hash160(compressed(P)) == target_h160:
                return k
        if max_seconds is not None and time.monotonic() - t0 > max_seconds:
            return None
        P = jac_add_affine(P, Gx, Gy)
    return None


def keys_per_second(count: int, stride: int = 1) -> float:
    """Measure effective key throughput of the stride method (no hashing of
    results beyond the running update). Used for honest feasibility numbers."""
    P = scalar_mult(0)
    t0 = time.monotonic()
    step = jac_add_affine(P, Gx, Gy)
    for _ in range(count):
        step = jac_add_affine(step, Gx, Gy)
    dt = time.monotonic() - t0
    return count / dt if dt > 0 else float("inf")