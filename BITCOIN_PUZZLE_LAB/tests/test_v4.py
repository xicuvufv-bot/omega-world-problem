"""Solver v4 (kangaroo) tests — deterministic seeds, generous budgets."""

from algorithms.curve import scalar_mult
from solvers.v4_kangaroo import KangarooSolver

TEN_POW_19 = 1 << 19
TEN_POW_20 = (1 << 20) - 1
TEN_POW_23 = 1 << 23
TEN_POW_24 = (1 << 24) - 1


def test_20bit_seed1():
    k = 700000
    solver = KangarooSolver(TEN_POW_19, TEN_POW_20, max_seconds=60, seed=1)
    assert solver.solve(scalar_mult(k)) == k


def test_20bit_seed2():
    k = 900123
    solver = KangarooSolver(TEN_POW_19, TEN_POW_20, max_seconds=60, seed=2)
    assert solver.solve(scalar_mult(k)) == k


def test_24bit_seed1():
    k = 12345678
    solver = KangarooSolver(TEN_POW_23, TEN_POW_24, max_seconds=60, seed=1)
    assert solver.solve(scalar_mult(k)) == k


def test_24bit_seed2():
    k = 9876543
    solver = KangarooSolver(TEN_POW_23, TEN_POW_24, max_seconds=60, seed=2)
    assert solver.solve(scalar_mult(k)) == k
