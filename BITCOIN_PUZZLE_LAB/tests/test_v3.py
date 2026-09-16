"""Solver v3 (BSGS) tests."""

from algorithms.curve import scalar_mult
from solvers.v3_bsgs import solve_bsgs


def test_find_45():
    k, stats = solve_bsgs(scalar_mult(45), 32, 63)
    assert k == 45
    assert stats["method"] == "bsgs"


def test_find_55():
    k, _ = solve_bsgs(scalar_mult(55), 32, 63)
    assert k == 55


def test_none_out_of_range():
    k, _ = solve_bsgs(scalar_mult(30), 32, 63)
    assert k is None


def test_wider_interval():
    lo, hi = 1 << 19, (1 << 20) - 1
    k, stats = solve_bsgs(scalar_mult(600000), lo, hi)
    assert k == 600000
    assert stats["m"] <= 1 << 10 + 1  # m ~ sqrt(2^19) ~ 724
