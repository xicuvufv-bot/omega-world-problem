"""Interval math and tracker-parsing tests."""

from algorithms.interval import bounds, width, parse_tracker, classify, PuzzleRow


def test_bounds_66():
    lo, hi = bounds(66)
    assert lo == 1 << 65
    assert hi == (1 << 66) - 1
    assert lo == 0x20000000000000000
    assert hi == 0x3ffffffffffffffff


def test_width_66():
    assert width(66) == 1 << 65


def test_parse_tracker_count():
    rows = parse_tracker()
    assert len(rows) == 160


def test_parse_tracker_puzzle_66_range():
    rows = parse_tracker()
    row66 = [r for r in rows if r.n == 66][0]
    assert row66.lo == 0x20000000000000000
    assert row66.hi == 0x3ffffffffffffffff


def test_classify():
    rows = parse_tracker()
    c = classify(rows)
    assert c["total"] == 160
    assert c["solved"] == 83
    assert c["unsolved"] == 77
    assert c["r2"] == 5
    assert c["r1"] == 72


def test_exposed_r2_set():
    rows = parse_tracker()
    r2 = [r for r in rows if r.regime == "R2"]
    assert sorted([r.n for r in r2]) == [140, 145, 150, 155, 160]


def test_puzzle_row_regime():
    solved = PuzzleRow(1, 1, 1, "addr", "SOLVED", "pub", "priv")
    r1     = PuzzleRow(71, 0, 0, "addr", "UNSOLVED", "NOT SOLVED", "NOT SOLVED")
    r2     = PuzzleRow(140, 0, 0, "addr", "UNSOLVED", "03ab...", "NOT SOLVED")
    assert solved.regime == "SOLVED"
    assert r1.regime == "R1"
    assert r2.regime == "R2"
    assert r2.exposed_pubkey is True
