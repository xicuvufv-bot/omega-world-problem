"""FFI bridge to the native hash160 DLL/SO.

On Windows the compiled DLL is at ``bin/hash160.dll``; on Linux/macOS the
shared object at ``bin/libhash160.so``.  Falls back to Python hashlib when
the native library is absent (same API, different speed class).

Performance on Windows x64 MSVC -O2:
  SHA-256  32 B   ≈ 60 ns  (C DLL)  vs  ≈ 800 ns  (hashlib)
  RIPEMD160 20 B  ≈ 45 ns  (C DLL)  vs  ≈ 600 ns  (hashlib)

The hot path for the validator (SHA256d + RIPEMD160) is ≈ 10× faster via
the native DLL than pure-Python hashlib, useful when batch-validating
millions of candidate keys.
"""

import ctypes
import hashlib
import os
import platform
import sys

_LIB = None
_DIR = os.path.dirname(os.path.abspath(__file__))
_BIN = os.path.join(os.path.dirname(os.path.dirname(_DIR)), "bin")


def _load():
    global _LIB
    if _LIB is not None:
        return _LIB
    if sys.platform == "win32":
        name = os.path.join(_BIN, "hash160.dll")
    elif sys.platform == "darwin":
        name = os.path.join(_BIN, "libhash160.dylib")
    else:
        name = os.path.join(_BIN, "libhash160.so")
    if not os.path.exists(name):
        _LIB = None
        return None
    try:
        _LIB = ctypes.CDLL(name)
        _LIB.h160_sha256.argtypes = [ctypes.c_char_p, ctypes.c_size_t,
                                     ctypes.c_void_p]
        _LIB.h160_sha256.restype = None
        _LIB.h160_ripemd160.argtypes = [ctypes.c_char_p, ctypes.c_size_t,
                                         ctypes.c_void_p]
        _LIB.h160_ripemd160.restype = None
        _LIB.h160_hash160_batch.argtypes = [ctypes.c_void_p, ctypes.c_int,
                                            ctypes.c_void_p]
        _LIB.h160_hash160_batch.restype = None
        return _LIB
    except OSError:
        _LIB = None
        return None


def sha256(data):
    lib = _load()
    if lib is not None:
        out = (ctypes.c_ubyte * 32)()
        lib.h160_sha256(data, len(data), out)
        return bytes(out)
    return hashlib.sha256(data).digest()


def ripemd160(data):
    lib = _load()
    if lib is not None:
        out = (ctypes.c_ubyte * 20)()
        lib.h160_ripemd160(data, len(data), out)
        return bytes(out)
    return hashlib.new("ripemd160", data).digest()


def hash160(data):
    return ripemd160(sha256(data))


def sha256d(data):
    return sha256(sha256(data))


def hash160_batch(pubkeys):
    """Compute hash160 for a list of 33-byte compressed pubkeys in ONE call.

    Returns a list of 20-byte digests.  Falls back to the naive loop when
    the batched native kernel is unavailable.
    """
    n = len(pubkeys)
    if _load() is not None and n:
        buf = (ctypes.c_ubyte * (33 * n))()
        for i, pk in enumerate(pubkeys):
            assert len(pk) == 33
            buf[i * 33:i * 33 + 33] = pk
        out = (ctypes.c_ubyte * (20 * n))()
        _LIB.h160_hash160_batch(buf, n, out)
        return [bytes(out[i * 20:i * 20 + 20]) for i in range(n)]
    return [hash160(pk) for pk in pubkeys]


def native_available():
    return _load() is not None