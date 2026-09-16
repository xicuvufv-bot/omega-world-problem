"""Minimal, self-contained secp256k1 arithmetic (Jacobian projective).

Implements exactly what the lab needs: scalar multiplication, point equality,
affine conversion and compression, using only Python integers. No third-party
dependencies. Formulas: additive/multiplicative inverses via Fermat's little
theorem; standard mixed-addition and a=0 doubling.

The implementation is deliberately small and auditable, and is cross-checked
against published Bitcoin Puzzle keys in tests/test_curve.py.
"""

P = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
N = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
A = 0
B = 7
Gx = 0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798
Gy = 0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8

INF = (0, 1, 0)  # Jacobian infinity (z == 0)


def JacobianPoint(x, y, z):
    return (x % P, y % P, z % P)


def is_affine_infinity(aff):
    return aff is None


def jac_double(pt):
    """Double a Jacobian point (curve parameter a = 0)."""
    x, y, z = pt
    if z == 0:
        return pt
    x2 = x * x % P
    y2 = y * y % P
    y4 = y2 * y2 % P
    s = ((x + y2) * (x + y2) - x2 - y4) % P
    d = 2 * s % P
    e = 3 * x2 % P
    xn = (e * e - 2 * d) % P
    yn = (e * (d - xn) - 8 * y4) % P
    zn = 2 * y * z % P
    return (xn, yn, zn)


def jac_add_affine(pt, ax, ay):
    """Add an affine point (ax, ay) to a Jacobian point (mixed addition)."""
    x, y, z = pt
    if z == 0:
        return (ax % P, ay % P, 1)
    z2 = z * z % P
    u = ax * z2 % P
    s = ay * z * z2 % P
    if u == x:
        if s != y:
            return INF
        return jac_double(pt)
    h = (u - x) % P
    h2 = h * h % P
    h3 = h * h2 % P
    r = (s - y) % P
    v = x * h2 % P
    xn = (r * r - 2 * v - h3) % P
    yn = (r * (v - xn) - y * h3) % P
    zn = (z * h) % P
    return (xn, yn, zn)


def _jac_to_affine(pt):
    x, y, z = pt
    if z == 0:
        return None
    zinv = pow(z, P - 2, P)
    zinv2 = zinv * zinv % P
    zinv3 = zinv2 * zinv % P
    return ((x * zinv2) % P, (y * zinv3) % P)


def to_affine(pt):
    return _jac_to_affine(pt)


def scalar_mult(k):
    """Return the Jacobian point k*G for 0 < k < N (k == 0 -> INF)."""
    if k == 0:
        return INF
    k = k % N
    if k == 0:
        return INF
    res = INF
    addend = INF
    # Build addend = G once: G is affine, we accumulate in Jacobian.
    for bit in bin(k)[2:]:
        res = jac_double(res)
        if bit == "1":
            res = jac_add_affine(res, Gx, Gy)
    return res


def point_equal_jac(p, q):
    """Equality in Jacobian without inversion (compare normalized coordinates)."""
    x1, y1, z1 = p
    x2, y2, z2 = q
    if z1 == 0 or z2 == 0:
        return z1 == 0 and z2 == 0
    a = x1 * z2 * z2 % P
    b = x2 * z1 * z1 % P
    if a != b:
        return False
    c = y1 * z2 * z2 * z2 % P
    d = y2 * z1 * z1 * z1 % P
    return c == d


def negative_affine(ax, ay):
    return (ax, (P - ay) % P)


def compressed(pt):
    """Compressed SEC-1 public key bytes for a Jacobian point."""
    aff = _jac_to_affine(pt)
    if aff is None:
        raise ValueError("cannot compress the point at infinity")
    x, y = aff
    prefix = 0x02 if (y % 2 == 0) else 0x03
    return bytes([prefix]) + x.to_bytes(32, "big")


def point_from_mult_affine(k):
    """Return (x, y) affine for k*G, or None for the identity."""
    return _jac_to_affine(scalar_mult(k))


def is_on_curve(x, y):
    return (y * y - (x * x * x + A * x + B)) % P == 0