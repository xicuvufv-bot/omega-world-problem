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


def test_kps_positive():
    kps = keys_per_second(800)
    assert kps > 50
