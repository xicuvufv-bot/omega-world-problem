"""Independent correctness gate for the native secp256k1 engine.

Cross-checks the C fused pipeline (secp256k1_engine.c / bin/secp256k1.dll)
against the lab's pure-Python reference implementation (algorithms/curve.py)
and hashlib.  The whole point of this suite: the native layer is fast, but
only as good as its arithmetic -- every rule below compares the C output to
the independent Python EC math, not to itself.

The native engine is optional (skip if bin/secp256k1.dll is absent).
"""

import hashlib
import os
import secrets
import sys
import time

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from algorithms.curve import P, scalar_mult, compressed, to_affine
from production.native import secp256k1_ffi as eng

pytestmark = pytest.mark.skipif(
    not eng.native_available(), reason="secp256k1 native lib not built")


def _pub_ref(k):
    """Reference compressed pubkey for int key k (independent Python EC)."""
    return compressed(scalar_mult(k))


def _h160(pk_bytes):
    h = hashlib.sha256(pk_bytes).digest()
    h = hashlib.new("ripemd160", h).digest()
    return h


def _k(offset_bytes=1):
    return int.from_bytes(offset_bytes, "big")


# ---- canonical constants -----------------------------------------------------

def test_selftest_passes():
    assert eng.selftest() == 1


def test_canonical_g_pubkey():
    assert eng.privkey_to_pubkey((1).to_bytes(32, "big")).hex() == (
        "0279be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798")
    assert eng.privkey_to_pubkey((2).to_bytes(32, "big")).hex() == (
        "02c6047f9441ed7d6d3045406e95c07cd85c778e4b8cef3ca7abac09b95c709ee5")


def test_known_multiples():
    for k in [1, 2, 3, 15, 16, 17, 255, 256, 65536, 2 ** 40]:
        got = eng.privkey_to_pubkey(k.to_bytes(32, "big"))
        assert got == _pub_ref(k), "mismatch at k=%d" % k


# ---- randomized cross-check against the Python reference ---------------------

@pytest.mark.parametrize("trial", range(25))
def test_random_keys_match_reference(trial):
    k = secrets.randbelow(P - 1) + 1
    assert eng.privkey_to_pubkey(k.to_bytes(32, "big")) == _pub_ref(k)


def test_random_batch_matches_reference():
    starts = [secrets.randbelow(2 ** 56) + 1 for _ in range(3)]
    per = 300
    for base in starts:
        res = eng.scan(base, per)
        assert len(res.pubkeys) == per
        for i in range(per):
            assert res.pubkeys[i] == _pub_ref(base + i), (
                "batch mismatch at %d+%d" % (base, i))


# ---- fused scan semantics ----------------------------------------------------

def test_scan_hashes_match_reference():
    base = 123456789
    res = eng.scan(base, 500)
    for i, pk in enumerate(res.pubkeys):
        assert res.hashes[i] == _h160(pk)


def test_scan_finds_buried_target():
    base = 0x10_0000
    delta = 733
    target = _h160(_pub_ref(base + delta))
    res = eng.scan(base, 2048, targets=[target])
    assert res.found_idx == delta
    assert res.found_key == (base + delta).to_bytes(32, "big")
    assert res.found_hash == target


def test_scan_finds_first_of_many_targets():
    base = 9000
    targets = [_h160(_pub_ref(base + d)) for d in (500, 7, 3000)]
    res = eng.scan(base, 4000, targets=targets)
    assert res.found_idx == 7                      # earliest hit wins


def test_scan_no_match():
    res = eng.scan(5555, 512, targets=[bytes(20)])
    assert res.found_idx == -1
    assert not any(res.matches)


def test_scan_empty_targets():
    res = eng.scan(1, 16)
    assert res.found_idx == -1
    assert len(res.pubkeys) == 16


def test_scan_rejects_key_zero():
    with pytest.raises(ValueError):
        eng.scan(0, 16)


def test_scan_key_sequence_is_consecutive():
    res = eng.scan(777, 4)
    got = [int.from_bytes(k, "big") for k in res.keys]
    assert got == [777, 778, 779, 780]


# ---- chunking (context max_batch < range) ------------------------------------

def test_scan_chunked_large_range_matches_single():
    base = 42_000
    n = 7000
    res = eng.scan(base, n, max_batch=4096)          # forces a 2nd chunk
    assert len(res.keys) == n
    for i in range(0, n, 100):
        assert res.pubkeys[i] == _pub_ref(base + i)


# ---- threading + affinity -----------------------------------------------------

def test_scan_threaded_equals_single():
    base = 2_500_000
    n = 4000
    single = eng.scan(base, n)
    multi = eng.scan_threaded(base, n, n_threads=2, pin=False)
    assert len(multi.pubkeys) == n
    assert [int.from_bytes(k, "big") for k in multi.keys] == list(
        range(base, base + n))
    for i in range(0, n, 17):
        assert multi.pubkeys[i] == single.pubkeys[i]
    assert multi.found_idx == -1 == single.found_idx


def test_threaded_match_reports_global_index():
    base = 1000
    target = _h160(_pub_ref(base + 1234))
    res = eng.scan_threaded(base, 5000, targets=[target], n_threads=4, pin=False)
    assert res.found_idx == 1234
    assert res.found_key == (base + 1234).to_bytes(32, "big")


# ---- performance sanity (logged, floor is machine-independent-ish) -----------

def test_scan_rate_sane():
    rate, _ = eng.scan_rate(start=1, n=65536)
    print("\n[single-thread] %.0f keys/sec" % rate)
    assert rate > 2_000, "engine degraded: %.0f keys/sec" % rate


def test_scan_rate_threaded_sane():
    rate, _ = eng.scan_rate_threaded(start=1, n=65536, n_threads=4)
    print("\n[4-thread pin]  %.0f keys/sec" % rate)
    assert rate > 5_000, "engine degraded: %.0f keys/sec" % rate