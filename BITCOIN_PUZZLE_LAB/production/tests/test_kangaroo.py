"""Tests for the native Pollard's Kangaroo interval-DLP solver."""

import os
import tempfile

import pytest

sys_path_prep = __import__("sys").path
sys_path_prep.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from production.native import kangaroo_ffi as kr
from algorithms.curve import point_from_mult_affine

pytestmark = pytest.mark.skipif(
    not kr.native_available(),
    reason="kangaroo.dll not built")


# ─── helper: tiny interval + known answer ────────────────────────────────

_A, _B, _K = 4096, 8191, 6000
_px, _py = point_from_mult_affine(_K)
_PUB_COMPRESSED = ("%02x" % (2 | (_py & 1))) + "%064x" % _px
_PUB_UNCOMPRESSED = "04" + "%064x" % _px + "%064x" % _py


def _solve(*a, **kw):
    return kr.solve(_A, _B, bytes.fromhex(_PUB_COMPRESSED), *a, **kw)


# ─── selftest ────────────────────────────────────────────────────────────

class TestSelftest:
    def test_passes(self):
        assert kr.selftest()


# ─── single-shot solve ───────────────────────────────────────────────────

class TestSolve:
    def test_compressed_single_thread(self):
        r = _solve(n_threads=1, seed=42, budget=1 << 30)
        assert r.found
        assert r.k == _K

    def test_compressed_multi_thread(self):
        r = _solve(n_threads=2, seed=42, budget=1 << 30)
        assert r.found
        assert r.k == _K

    def test_uncompressed(self):
        r = kr.solve(_A, _B, bytes.fromhex(_PUB_UNCOMPRESSED),
                     n_threads=1, seed=42, budget=1 << 30)
        assert r.found
        assert r.k == _K

    def test_deterministic_same_seed(self):
        r1 = _solve(n_threads=2, seed=12345, budget=1 << 30)
        r2 = _solve(n_threads=2, seed=12345, budget=1 << 30)
        assert r1.found and r2.found
        assert r1.k == r2.k

    def test_budget_too_small_returns_not_found(self):
        r = _solve(n_threads=1, seed=42, budget=100)
        assert not r.found

    def test_checkpoint_resume(self):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".bin") as f:
            path = f.name
        try:
            r1 = kr.solve(_A, _B, bytes.fromhex(_PUB_COMPRESSED),
                          n_threads=1, seed=11111, budget=1 << 30,
                          checkpoint=path)
            assert r1.found
            assert r1.k == _K
            # Re-running with same checkpoint reuses DPs
            r2 = kr.solve(_A, _B, bytes.fromhex(_PUB_COMPRESSED),
                          n_threads=1, seed=22222, budget=1 << 30,
                          checkpoint=path)
            assert r2.found
        finally:
            try: os.unlink(path)
            except OSError: pass


# ─── edge cases / bad inputs ─────────────────────────────────────────────

class TestEdgeCases:
    def test_invalid_range_rejected(self):
        """A >= B must fail."""
        with pytest.raises(ValueError):
            kr.solve(8191, 4096, bytes.fromhex(_PUB_COMPRESSED),
                     n_threads=1, seed=42, budget=1 << 20)

    def test_256bit_range_runs(self):
        """A real R2 interval (puzzle 140) should start without error."""
        r = kr.solve(2**139, 2**140 - 1,
                     bytes.fromhex(_PUB_COMPRESSED),
                     n_threads=1, ntame=4, nwild=4,
                     dpbits=16, seed=42, budget=10000)
        # budget far too small — just verifying no crash
        assert isinstance(r.found, bool)
