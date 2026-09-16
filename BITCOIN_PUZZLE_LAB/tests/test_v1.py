"""Solver v1 (naive scan) tests."""

from algorithms.hash import compressed_pubkey_hash
from solvers.v1_bruteforce import scan_naive


def test_find_7():
    target = compressed_pubkey_hash(7)
    assert scan_naive(target, 1, 15) == 7


def test_returns_none_out_of_range():
    target = compressed_pubkey_hash(100)
    assert scan_naive(target, 1, 50) is None


def test_limit_hits():
    target = compressed_pubkey_hash(20)
    assert scan_naive(target, 1, 30, limit=10) is None
