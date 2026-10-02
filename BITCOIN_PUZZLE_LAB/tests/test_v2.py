"""Solver v2 (stride + bitmask) tests."""

from algorithms.hash import compressed_pubkey_hash
from solvers.v2_bitmask import solve_stride, build_bitmask, scan_masked, keys_per_second


def test_find_7():
    target = compressed_pubkey_hash(7)
    assert solve_stride(target, 1, 15) == 7


def test_find_29():
    target = compressed_pubkey_hash(29)
    assert solve_stride(target, 1, 35) == 29


def test_bitmask_prefilter():
    t1 = compressed_pubkey_hash(7)
    mask = build_bitmask([t1], first_bits=16)
    assert scan_masked(t1, 1, 15, mask=mask, first_bits=16) == 7


def test_scan_masked_agrees_with_stride():
    """Batched-inversion scan_masked must find the same keys as the classical
    per-key solve_stride across a range of keys (equivalence of scan order)."""
    keys = [7, 29, 61, 257, 4097]
    for k in keys:
        target = compressed_pubkey_hash(k)
        hi = max(8192, 4 * k)
        assert solve_stride(target, 1, hi) == k
        assert scan_masked(target, 1, hi, mask=None, first_bits=16) == k


def test_scan_masked_no_false_hit():
    target = compressed_pubkey_hash(7)
    assert scan_masked(target, 100, 200, mask=None, first_bits=16) is None
    assert scan_masked(target, 1, 6, mask=None, first_bits=16) is None


def test_scan_masked_limit_respected():
    target = compressed_pubkey_hash(7)
    assert scan_masked(target, 1, 15, mask=None, first_bits=16, limit=2) is None


def test_kps_positive():
    kps = keys_per_second(800)
    assert kps > 50
