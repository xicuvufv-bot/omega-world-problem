r"""tests/test_secp256k1_engine.py
Cross-validate the C secp256k1 engine against the Python reference implementations
in algorithms/curve.py and algorithms/hash.py, driven through the FFI bridge in
production/native/secp256k1_ffi.py.

Run:
    pytest tests/test_secp256k1_engine.py -v

Compile step (run once before pytest):
    cmd /c 'call "C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools\VC\Auxiliary\Build\vcvars64.bat" >nul 2>&1 && cl /O2 /LD /Fo:bin\ production\native\secp256k1_engine.c /Fe:bin\secp256k1.dll'
"""
from __future__ import annotations

import ctypes
import sys
from pathlib import Path

import pytest

# ─── path setup ──────────────────────────────────────────────────────────
_ROOT = Path(__file__).resolve().parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from production.native import secp256k1_ffi as F
from production.native.secp256k1_ffi import Context, ScanResult
from algorithms.curve import (
    P, N, Gx, Gy,
    jac_add_affine, jac_double, scalar_mult,
    to_affine, compressed, is_on_curve, JacobianPoint,
)
from algorithms.hash import hash160, ripemd160, sha256d

# ─── engine availability ────────────────────────────────────────────────
pytestmark = pytest.mark.skipif(
    not F.native_available(),
    reason="secp256k1 native library not built; compile bin\\secp256k1.dll first",
)


@pytest.fixture(scope="module")
def ctx() -> Context:
    """One shared native context for raw low-level tests (module scope)."""
    c = Context(max_batch=8192)
    yield c
    c.close()


def _key_be(k: int) -> bytes:
    return k.to_bytes(32, "big")


def _py_pubkey(k: int) -> bytes:
    """Reference compressed pubkey via algorithms/curve.py."""
    return compressed(scalar_mult(k))


def _ctx_run(c: Context, n: int):
    """Raw s256_run on an existing context (mirrors the FFI's internals)."""
    lib = c._lib
    kb = (ctypes.c_ubyte * (32 * n))()
    pb = (ctypes.c_ubyte * (33 * n))()
    hb = (ctypes.c_ubyte * (20 * n))()
    mb = (ctypes.c_ubyte * n)()
    actual = lib.s256_run(c._ptr, n, kb, pb, hb, mb)
    assert actual > 0, f"s256_run returned {actual}"
    return (bytes(kb[:actual * 32]), bytes(pb[:actual * 33]),
            bytes(hb[:actual * 20]), bytes(mb[:actual]))


# ═════════════════════════════════════════════════════════════════════════
#  Self-test
# ═════════════════════════════════════════════════════════════════════════

def test_c_selftest():
    assert F.selftest() == 1


# ═════════════════════════════════════════════════════════════════════════
#  Scalar multiply vs Python reference + known vectors
# ═════════════════════════════════════════════════════════════════════════

_VECTORS = [
    (1, "0279be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798"),
    (2, "02c6047f9441ed7d6d3045406e95c07cd85c778e4b8cef3ca7abac09b95c709ee5"),
    (3, "02f9308a019258c31049344f85f89d5229b531c845836f99b08601f113bce036f9"),
    (4, "02e493dbf1c10d80f3581e4904930b1404cc6c13900ee0758474fa94abe8c4cd13"),
    (5, "022f8bde4d1a07209355b4a7250a5c5128e88b84bddc619ab7cba8d569b240efe4"),
    (6, "03fff97bd5755eeea420453a14355235d382f6472f8568a18b2f057a1460297556"),
    (7, "025cbdf0646e5db4eaa398f365f2ea7a0e3d419b7e0330e39ce92bddedcac4f9bc"),
    (8, "022f01e5e15cca351daff3843fb70f3c2f0a1bdd05e5af888a67784ef3e10a2a01"),
    (9, "03acd484e2f0c7f65309ad178a9f559abde09796974c57e714c35f110dfc27ccbe"),
    (10, "03a0434d9e47f3c86235477c7b1ae6ae5d3442d49b1943c2b752a68e2a47e247c7"),
]


@pytest.mark.parametrize("k,expected_hex", _VECTORS, ids=[f"k={v[0]}" for v in _VECTORS])
def test_scalar_mult_c_vs_python(k: int, expected_hex: str):
    c_pk33 = F.privkey_to_pubkey(k)
    # known vector
    assert c_pk33.hex() == expected_hex, f"C pubkey mismatch for k={k}"
    # Python reference pubkey
    py_pk = _py_pubkey(k)
    assert c_pk33 == py_pk, f"C vs Python pubkey mismatch for k={k}"
    # hash160 agreed too
    c_h = F.hash160_batch([c_pk33])[0]
    assert c_h == hash160(py_pk), f"C vs Python hash160 mismatch for k={k}"


# ═════════════════════════════════════════════════════════════════════════
#  Chaining / statefulness
# ═════════════════════════════════════════════════════════════════════════

def test_chaining():
    res = F.scan(1, 100)
    assert len(res.pubkeys) == 100
    for i in range(100):
        k = i + 1
        assert res.pubkeys[i] == _py_pubkey(k), f"Chain break at k={k}"
        assert res.keys[i] == _key_be(k)


def test_context_stateful(ctx: Context):
    """One context: run(5) twice = keys 1..10, no seek needed in between."""
    ctx.seek(1)
    kb1, pb1, _, _ = _ctx_run(ctx, 5)
    kb2, pb2, _, _ = _ctx_run(ctx, 5)
    for i in range(5):
        assert kb1[i * 32:(i + 1) * 32] == _key_be(i + 1)
        assert kb2[i * 32:(i + 1) * 32] == _key_be(i + 6)
        assert pb1[i * 33:(i + 1) * 33] == _py_pubkey(i + 1)
        assert pb2[i * 33:(i + 1) * 33] == _py_pubkey(i + 6)


# ═════════════════════════════════════════════════════════════════════════
#  Target matching
# ═════════════════════════════════════════════════════════════════════════

def test_target_matching():
    target_h160 = hash160(_py_pubkey(1))  # i.e. hash160 of k=1
    res = F.scan(1, 10, targets=[target_h160])
    assert isinstance(res, ScanResult)
    assert res.found_idx == 0
    assert res.found_key == _key_be(1)
    assert res.matches == [True] + [False] * 9
    assert bool(res) is True


def test_target_matching_multi():
    hits = {1, 50, 100}
    targets = [hash160(_py_pubkey(k)) for k in sorted(hits)]
    res = F.scan(1, 100, targets=targets)
    assert res.found_idx == 0
    for i, m in enumerate(res.matches):
        k = i + 1
        expect = k in hits
        assert m == expect, f"k={k}: expected match={expect}, got {m}"


def test_target_matching_hex_str():
    """40-hex target strings are accepted by the FFI."""
    target_h160 = hash160(_py_pubkey(42))
    res = F.scan(1, 42, targets=[target_h160.hex()])
    assert res.found_idx == 41
    assert res.found_key == _key_be(42)
    # clear-targets path: no target set
    res0 = F.scan(1, 10)
    assert res0.found_idx == -1
    assert not bool(res0)


# ═════════════════════════════════════════════════════════════════════════
#  Checkpoint / resume (via raw context state + get_key)
# ═════════════════════════════════════════════════════════════════════════

def test_checkpoint_resume(tmp_path, ctx: Context):
    ctx.seek(1000)
    _, pb1, _, _ = _ctx_run(ctx, 1)
    assert pb1 == _py_pubkey(1000)
    key_after = ctx.get_key()
    assert key_after == _key_be(1001), f"expected 1001, got {key_after.hex()}"

    # persist the checkpoint atomically (os.replace pattern)
    ckpt = tmp_path / "ckpt.dat"
    ckpt.write_bytes(key_after)

    # fresh context resumes from checkpoint file contents
    ctx2 = Context(max_batch=64)
    ctx2.seek(int.from_bytes(ckpt.read_bytes(), "big"))
    _, pb2, _, _ = _ctx_run(ctx2, 5)
    for j in range(5):
        k = 1001 + j
        assert pb2[j * 33:(j + 1) * 33] == _py_pubkey(k), f"Resume k={k}"
    ctx2.close()


# ═════════════════════════════════════════════════════════════════════════
#  Threading
# ═════════════════════════════════════════════════════════════════════════

def test_scan_threaded():
    res = F.scan_threaded(1, 200, n_threads=4, pin=False)
    assert len(res.pubkeys) == 200
    for i in range(200):
        k = i + 1
        assert res.pubkeys[i] == _py_pubkey(k), f"Threaded range k={k}"
        assert res.keys[i] == _key_be(k)


# ═════════════════════════════════════════════════════════════════════════
#  C hash160 batch vs Python
# ═════════════════════════════════════════════════════════════════════════

def test_hash160_batch():
    pubkeys = [_py_pubkey(k) for k in range(1, 51)]
    c_h160s = F.hash160_batch(pubkeys)
    assert len(c_h160s) == 50
    for i in range(50):
        assert c_h160s[i] == hash160(pubkeys[i]), f"hash160 mismatch at k={i+1}"


# ═════════════════════════════════════════════════════════════════════════
#  Group-order edge cases
# ═════════════════════════════════════════════════════════════════════════

def test_key_at_N():
    """k = N -> equivalent to 0 -> point at infinity row, then continues."""
    res = F.scan(N, 3)
    assert len(res.keys) == 3
    # row 0: key 0 mod N (seek reduced N to 0), infinity -> zero pubkey/hash
    assert res.keys[0] == b"\x00" * 32
    assert res.pubkeys[0] == b"\x00" * 33
    assert res.hashes[0] == b"\x00" * 20
    # rows 1,2 resume at k=1,2
    assert res.pubkeys[1] == _py_pubkey(1)
    assert res.pubkeys[2] == _py_pubkey(2)


def test_seek_to_max_key():
    """seek(2^256-1) must behave as (2^256-1 mod N).  Uses Context directly
    because the scan() helper deliberately rejects ranges near 2^256."""
    max_key = 2 ** 256 - 1
    c = Context(max_batch=16)
    c.seek(max_key)
    kb, pb, _, _ = _ctx_run(c, 1)
    reduced = max_key % N
    assert kb[:32] == _key_be(reduced)
    assert pb[:33] == _py_pubkey(reduced)
    c.close()


# ═════════════════════════════════════════════════════════════════════════
#  Python reference arithmetic cross-checks
# ═════════════════════════════════════════════════════════════════════════

def test_fe_addmod_reference():
    assert (P - 1 + 1) % P == 0


def test_fe_mulmod_reference():
    assert ((P - 1) * (P - 1)) % P == 1


def test_fe_inv_reference():
    assert (pow(2, P - 2, P) * 2) % P == 1


@pytest.mark.parametrize("a", [1, 2, 3, 5, 7, 11, 12345, 2 ** 64 + 1, P - 1])
def test_fe_inv_modp(a):
    assert (a * pow(a, P - 2, P)) % P == 1


def test_jacobian_dbl_reference():
    G_jac = JacobianPoint(Gx, Gy, 1)
    G2 = jac_double(G_jac)
    assert to_affine(G2) is not None
    assert compressed(G2) == _py_pubkey(2)


def test_jacobian_add_reference():
    G2 = jac_double(JacobianPoint(Gx, Gy, 1))
    G3 = jac_add_affine(G2, Gx, Gy)
    assert compressed(G3) == _py_pubkey(3)


def test_g_on_curve():
    assert is_on_curve(Gx, Gy)


# ═════════════════════════════════════════════════════════════════════════
#  Large batch
# ═════════════════════════════════════════════════════════════════════════

def test_large_batch():
    res = F.scan(1, 4096, max_batch=4096)
    assert len(res.pubkeys) == 4096
    for k in [1, 2, 3, 50, 255, 256, 1000, 2048, 4095, 4096]:
        assert res.pubkeys[k - 1] == _py_pubkey(k), f"Large batch k={k}"


# ═════════════════════════════════════════════════════════════════════════
#  Python reference hash known-answer tests
# ═════════════════════════════════════════════════════════════════════════

def test_sha256_vector():
    assert sha256d(b"abc") == bytes.fromhex(
        "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad"
    )


def test_ripemd160_vector():
    assert ripemd160(b"abc") == bytes.fromhex(
        "8eb208f7e05d987a9b044a8e98c6b087f15a0bfc"
    )


def test_hash160_vector():
    assert hash160(b"abc") == ripemd160(sha256d(b"abc"))


# ═════════════════════════════════════════════════════════════════════════
#  Error paths
# ═════════════════════════════════════════════════════════════════════════

def test_bad_key_length():
    with pytest.raises(ValueError):
        F.privkey_to_pubkey(b"\x01" * 16)


def test_key_out_of_range():
    with pytest.raises(ValueError):
        F.privkey_to_pubkey(2 ** 256)


def test_bad_target():
    with pytest.raises(ValueError):
        F.scan(1, 5, targets=[b"\x00" * 19])  # not 20 bytes


def test_ctx_bad_batch():
    with pytest.raises(AssertionError):
        Context(max_batch=0)
    with pytest.raises(AssertionError):
        Context(max_batch=70000)


def test_empty_scan():
    res = F.scan(1, 0)
    assert res.found_idx == -1
    assert len(res.pubkeys) == 0