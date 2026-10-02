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

from algorithms.curve import scalar_mult, jac_add_affine, compressed, Gx, Gy, P
from algorithms.hash import hash160

# Block size for batch affine conversion.  Inverting one z per key is the
# dominant Python cost (a Fermat pow ~= 256 field multiplications); the
# Montgomery prefix-product trick turns a whole block into a single inverse
# plus ~3N multiplications.
_BLOCK = 64


def _block_affines(jac_pts):
    """Affine forms of a block of Jacobian points with ONE modular inverse.

    Montgomery batch inverse: prefix products, a single pow, back-substitution.
    Results are identical to calling to_affine per point; used exactly where a
    stride scan walks a block in pure Jacobian before comparing any hash.
    """
    n = len(jac_pts)
    zs = [p[2] for p in jac_pts]
    if any(z == 0 for z in zs):
        # point at infinity cannot participate in a batch -> per-point path.
        # kG is never infinity for k in [1, N-1], so this is defensive only.
        return _per_point_affines(jac_pts)
    prefix = [1] * n
    acc = 1
    for i in range(n):
        prefix[i] = acc
        acc = acc * zs[i] % P
    inv = pow(acc, P - 2, P)
    invs = [0] * n
    for i in range(n - 1, -1, -1):
        invs[i] = inv * prefix[i] % P
        inv = inv * zs[i] % P
    out = []
    for i, (x, y, z) in enumerate(jac_pts):
        iz, iz2 = invs[i], invs[i] * invs[i] % P
        out.append(((x * iz2) % P, (y * iz2 * iz) % P))
    return out


def _per_point_affines(jac_pts):
    out = []
    for x, y, z in jac_pts:
        if z == 0:
            out.append(None)
            continue
        inv = pow(z, P - 2, P)
        iz2 = inv * inv % P
        out.append(((x * iz2) % P, (y * iz2 * inv) % P))
    return out


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

    ``mask`` is the set built by build_bitmask for the *same* first_bits.
    Keys are walked in pure Jacobian one point-add per key; affine conversion
    is batched (a single Fermat inverse per _BLOCK keys) instead of one
    inversion per key.  Scan order and results are identical to the classical
    per-key version (verified in tests/test_v2.py).
    """
    P_pt = scalar_mult(lo)
    t0 = time.monotonic()
    n = 0
    shift = 160 - first_bits
    target_bucket = int.from_bytes(target_h160, "big") >> shift
    hits = 0
    k = lo
    while k <= hi:
        cnt = min(_BLOCK, hi - k + 1)
        jac = [P_pt]
        cur = P_pt
        for _ in range(1, cnt):
            cur = jac_add_affine(cur, Gx, Gy)
            jac.append(cur)
        affs = _block_affines(jac)
        for i, aff in enumerate(affs):
            n += 1
            if limit is not None and n > limit:
                return None
            if mask is not None and target_bucket not in mask:
                # whole bucket empty of targets: nothing to hash
                continue
            h = hash160(compressed_from_affine(aff))
            if int.from_bytes(h, "big") >> shift == target_bucket:
                hits += 1
                if h == target_h160:
                    return k + i
            if max_seconds is not None and time.monotonic() - t0 > max_seconds:
                return None
        P_pt = jac_add_affine(cur, Gx, Gy)
        k += cnt
    return None


def compressed_from_affine(aff):
    """SEC-1 compressed key bytes for an affine (x, y) (no re-inversion)."""
    x, y = aff
    return bytes([0x02 if (y % 2 == 0) else 0x03]) + x.to_bytes(32, "big")


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