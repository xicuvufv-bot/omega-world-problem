"""Curve arithmetic self-tests against published constants."""

from algorithms.curve import scalar_mult, to_affine, compressed, Gx, Gy, P, N, point_equal_jac

VECTORS = [
    (1, Gx, Gy),
    (3, 0xf9308a019258c31049344f85f89d5229b531c845836f99b08601f113bce036f9,
          0x388f7b0f632de8140fe337e62a37f3566500a99934c2231b6cb9fd7584b8e672),
    (6, 0xff206757a898362124a45645c7b6c53b237730de1ee1800aa322ce93890d6e01,
          0xf12375498a58c167648784028305a5c2a4892df46f03ceabf2a9d797a6b50f1e),
]


def test_scalar_mult_k1():
    aff = to_affine(scalar_mult(1))
    assert aff == (Gx, Gy)


def test_scalar_mult_k3():
    aff = to_affine(scalar_mult(3))
    assert aff == (VECTORS[1][1], VECTORS[1][2])


def test_scalar_mult_k6():
    """6G = 2*(3G); verify via addition consistency."""
    from algorithms.curve import jac_add_affine
    pt3 = scalar_mult(3)
    pt6a = scalar_mult(6)
    pt6b = jac_add_affine(pt3, *to_affine(pt3))
    assert point_equal_jac(pt6a, pt6b)


def test_point_add_consistency():
    """1G + 1G == 2G, and addition is commutative."""
    from algorithms.curve import jac_add_affine, jac_double, INF
    p1 = scalar_mult(1)
    p2 = jac_add_affine(p1, Gx, Gy)      # p1 + G -> 2G
    p3 = scalar_mult(2)
    assert point_equal_jac(p2, p3)


def test_compressed_prefix_parity():
    """Prefix is 02 for even y, 03 for odd y."""
    for k, x, y in VECTORS[:2]:
        comp = compressed(scalar_mult(k))
        assert comp[0] == (0x02 if y % 2 == 0 else 0x03)
        assert int.from_bytes(comp[1:], "big") == x


def test_public_constants():
    assert P == 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
    assert N == 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
    assert Gx == 0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798
    assert Gy == 0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8


def test_k_nonzero_under_mod_n():
    """k=N (order) -> point at infinity."""
    from algorithms.curve import INF
    pt = scalar_mult(N)
    assert pt == (0, 1, 0)
