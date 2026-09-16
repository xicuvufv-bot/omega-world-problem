"""FFI bridge to the native secp256k1 scan engine.

Exposes the fused ``s256_*`` API from ``bin/secp256k1.dll`` (Windows) or
``bin/libsecp256k1.so`` / ``.dylib`` (Linux/macOS).  The engine derives one
compressed public key per sequential private key entirely in C (window-4
scalar multiply for the batch start, then one mixed Jacobian+affine
``+G`` step per subsequent key, one Montgomery batch inversion, then fused
hash160) — so a whole key-range sweep costs a single cross the boundary,
never one round-trip per key.

Public surface (the names you actually want):

    privkey_to_pubkey(priv)          -> 33-byte compressed pubkey
    hash160_batch(pubkeys)           -> [20-byte hash160 digests]
    scan(start, n, targets=())       -> ScanResult
    scan_threaded(start, n, targets=(), n_threads=..., pin=True) -> ScanResult

``ScanResult`` carries .keys / .pubkeys / .hashes / .matches plus
.found_idx / .found_key / .found_hash (found_idx == -1 when nothing hit).

Thread-safety: the Lab pattern is ONE context per worker thread + affinity.
The C context is stateful (it keeps the current key/point across s256_run
calls), so sharing a single context across threads is NOT safe.  Use
``scan_threaded`` (spawns one context per thread and pins each to its own
core) or create per-thread contexts yourself via ``Context``.

Unlike the hash160 layer there is deliberately NO pure-Python fallback
for the fused scan: correctness of this native path is verified in
tests/test_secp256k1.py against the independent reference implementation
algorithms/curve.py + hashlib.
"""

import ctypes
import os
import sys
import time
import threading
from dataclasses import dataclass, field

_DIR = os.path.dirname(os.path.abspath(__file__))
_BIN = os.path.join(os.path.dirname(os.path.dirname(_DIR)), "bin")

_LIB = None
_LOCK = threading.Lock()


def _libpath():
    if sys.platform == "win32":
        return os.path.join(_BIN, "secp256k1.dll")
    if sys.platform == "darwin":
        return os.path.join(_BIN, "libsecp256k1.dylib")
    return os.path.join(_BIN, "libsecp256k1.so")


def _load():
    global _LIB
    if _LIB is not None:
        return _LIB
    path = _libpath()
    if not os.path.exists(path):
        return None
    try:
        lib = ctypes.CDLL(path)
    except OSError:
        return None

    lib.s256_selftest.restype = ctypes.c_int

    lib.s256_ctx_new.argtypes = [ctypes.c_int]
    lib.s256_ctx_new.restype = ctypes.c_void_p
    lib.s256_ctx_free.argtypes = [ctypes.c_void_p]
    lib.s256_ctx_free.restype = None

    lib.s256_set_targets.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_int]
    lib.s256_set_targets.restype = ctypes.c_int
    lib.s256_seek.argtypes = [ctypes.c_void_p, ctypes.c_char_p]
    lib.s256_seek.restype = ctypes.c_int
    lib.s256_get_key.argtypes = [ctypes.c_void_p, ctypes.c_void_p]
    lib.s256_get_key.restype = None
    lib.s256_run.argtypes = [ctypes.c_void_p, ctypes.c_int,
                             ctypes.c_void_p, ctypes.c_void_p,
                             ctypes.c_void_p, ctypes.c_void_p]
    lib.s256_run.restype = ctypes.c_int
    lib.s256_hash160_batch.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_void_p]
    lib.s256_hash160_batch.restype = None

    with _LOCK:
        _LIB = lib
    return lib


def native_available():
    return _load() is not None


def selftest():
    """Run the in-C self-test (1 = pass). Raises if the DLL is missing."""
    lib = _load()
    if lib is None:
        raise RuntimeError("secp256k1 native library not built; see README")
    return lib.s256_selftest()


def _check_key(key):
    if isinstance(key, int):
        if not 0 <= key < 2 ** 256:
            raise ValueError("key out of 256-bit range")
        key = key.to_bytes(32, "big")
    if isinstance(key, str):
        key = bytes.fromhex(key.zfill(64))
    key = bytes(key)
    if len(key) != 32:
        raise ValueError("key must be 32 bytes (or a hex string)")
    return key


def _check_targets(targets):
    out = []
    for t in targets or ():
        if isinstance(t, str):
            t = bytes.fromhex(t.zfill(40))
        t = bytes(t)
        if len(t) != 20:
            raise ValueError("each target must be a 20-byte hash160")
        out.append(t)
    return b"".join(out), len(out)


class Context:
    """One native scan context (owns its window table + batch buffers).

    A context is stateful (it remembers the current key between s256_run
    calls) and is therefore NOT thread-safe — use one context per worker
    thread.  ``max_batch`` is the largest s256_run chunk this context can
    serve; scanning a longer range is automatically chunked by `scan`.
    """

    MAX_BATCH = 65536

    def __init__(self, max_batch=4096, ptr=None):
        assert 1 <= max_batch <= self.MAX_BATCH, "max_batch out of range"
        self._lib = _load()
        if self._lib is None:
            raise RuntimeError("secp256k1 native library not built; see README")
        self.max_batch = max_batch
        self._ptr = ptr if ptr is not None else self._lib.s256_ctx_new(max_batch)
        if not self._ptr:
            raise MemoryError("s256_ctx_new returned NULL")

    def close(self):
        if getattr(self, "_ptr", None):
            self._lib.s256_ctx_free(self._ptr)
            self._ptr = None

    def __del__(self):
        try:
            self.close()
        except Exception:
            pass

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        self.close()

    # -- low-level pass-through --------------------------------------------------

    def seek(self, key):
        self._lib.s256_seek(self._ptr, _check_key(key))

    def set_targets(self, targets):
        raw, n = _check_targets(targets)
        if self._lib.s256_set_targets(self._ptr, raw, n) != 0:
            raise RuntimeError("s256_set_targets failed")

    def get_key(self):
        out = (ctypes.c_ubyte * 32)()
        self._lib.s256_get_key(self._ptr, out)
        return bytes(out)

    def hash160_batch(self, pubkeys):
        n = len(pubkeys)
        if not n:
            return []
        buf = (ctypes.c_ubyte * (33 * n))()
        for i, pk in enumerate(pubkeys):
            assert len(pk) == 33
            buf[i * 33:i * 33 + 33] = pk
        out = (ctypes.c_ubyte * (20 * n))()
        self._lib.s256_hash160_batch(buf, n, out)
        return [bytes(out[i * 20:i * 20 + 20]) for i in range(n)]


@dataclass
class ScanResult:
    keys: list = field(default_factory=list)
    pubkeys: list = field(default_factory=list)
    hashes: list = field(default_factory=list)
    matches: list = field(default_factory=list)
    found_idx: int = -1
    found_key: bytes = None
    found_hash: bytes = None

    def __bool__(self):
        return self.found_idx >= 0


def _run_buffers(ctx, start, n, targets):
    """Seek ctx to `start`, set targets, run n keys (chunked), return ScanResult."""
    ctx.seek(start)
    ctx.set_targets(targets)

    mb = ctx.max_batch
    keys_b = (ctypes.c_ubyte * (32 * mb))()
    pub_b = (ctypes.c_ubyte * (33 * mb))()
    hsh_b = (ctypes.c_ubyte * (20 * mb))()
    mch_b = (ctypes.c_ubyte * mb)()

    res = ScanResult()
    done = 0
    while done < n:
        take = min(mb, n - done)
        actual = ctx._lib.s256_run(ctx._ptr, take, keys_b, pub_b, hsh_b, mch_b)
        if actual <= 0:
            break
        off_idx = done
        for i in range(actual):
            res.keys.append(bytes(keys_b[i * 32:i * 32 + 32]))
            res.pubkeys.append(bytes(pub_b[i * 33:i * 33 + 33]))
            res.hashes.append(bytes(hsh_b[i * 20:i * 20 + 20]))
            hit = mch_b[i] == 1
            res.matches.append(bool(hit))
            if hit and res.found_idx < 0:
                res.found_idx = off_idx + i
                res.found_key = res.keys[-1]
                res.found_hash = res.hashes[-1]
        done += actual
        if actual < take:  # hit the internal boundary (key reached 0) -- stop
            break
    return res


def privkey_to_pubkey(priv):
    """Derive the compressed SEC-1 pubkey for one private key (C engine)."""
    with Context(max_batch=1) as ctx:
        ctx.seek(priv)
        res = _run_buffers(ctx, _check_key(priv), 1, ())
    return res.pubkeys[0]


def hash160_batch(pubkeys):
    """Native hash160 over a list of 33-byte compressed pubkeys."""
    with Context(max_batch=max(1, min(len(pubkeys), 4096))) as ctx:
        return ctx.hash160_batch(pubkeys)


def scan(start, n, targets=(), max_batch=4096):
    """Fused scan: derive n consecutive keys from `start`, hash160 each, and
    report every key whose digest exists in `targets` (20-byte digests or
    40-hex strings).  Returns a ScanResult.
    """
    if n < 1:
        return ScanResult()
    start = _check_key(start)
    if start == b"\x00" * 32 or int.from_bytes(start, "big") >= 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFE:
        raise ValueError("scan range must lie in [1, n-1]")
    with Context(max_batch=min(n, max_batch)) as ctx:
        return _run_buffers(ctx, start, n, targets)


def _worker(seg_start, seg_n, targets, max_batch, error_box, result_box,
            pin_spec, allow_pin_skip):
    try:
        import production.native.affinity as affinity
        if pin_spec is not None:
            pinned = affinity.pin_thread(pin_spec)
            if not pinned and not allow_pin_skip:
                raise RuntimeError("could not pin worker to %r" % (pin_spec,))
        res = scan(seg_start, seg_n, targets=targets, max_batch=max_batch)
        result_box[0] = res
    except Exception as exc:  # noqa: BLE001  -- report back to the main thread
        error_box.append(exc)


def scan_threaded(start, n, targets=(), n_threads=None, pin=True, max_batch=4096):
    """Parallel fused scan across disjoint key ranges.

    Each worker thread owns its own native context and is pinned to its own
    core (the Lab affinity pattern).  Returns one merged ScanResult for the
    range that starts at `start`.

    ``n_threads`` defaults to the CPU count.  ``pin`` may be True (pin to
    range(cpu_count)), a list of core ids, or False to skip pinning.
    """
    import production.native.affinity as affinity

    start = _check_key(start)
    if n_threads is None:
        n_threads = affinity.get_cpu_count()
    n_threads = max(1, min(n_threads, n))
    if pin is True:
        pin = list(range(affinity.get_cpu_count()))
    cores = pin or None

    seg, rem = divmod(n, n_threads)
    threads, results, errors, segments = [], [], [], []
    base = int.from_bytes(start, "big")
    pos = 0
    for t in range(n_threads):
        size = seg + (1 if t < rem else 0)
        if size <= 0:
            continue
        segments.append(((base + pos).to_bytes(32, "big"), size))
        pos += size

    for seg_start, size in segments:
        tgt = list(targets)
        rbox, ebox = [None], []
        th = threading.Thread(
            target=_worker,
            args=(seg_start, size, tgt, max_batch, ebox, rbox,
                  [cores[len(results) % len(cores)]] if cores else None,
                  pin is not None),
            daemon=True)
        threads.append(th)
        results.append(rbox)
        errors.append(ebox)
        th.start()
    for th in threads:
        th.join()

    if any(ebox for ebox in errors):
        raise errors[0][0]

    merged = ScanResult()
    for rbox in results:
        r = rbox[0]
        if r is None:
            continue
        base_len = len(merged.keys)
        merged.keys += r.keys
        merged.pubkeys += r.pubkeys
        merged.hashes += r.hashes
        merged.matches += r.matches
        if merged.found_idx < 0 and r.found_idx >= 0:
            merged.found_idx = base_len + r.found_idx
            merged.found_key = r.found_key
            merged.found_hash = r.found_hash
    if len(merged.keys) < n:  # defensive: never happens for in-range keys
        while len(merged.keys) < n:
            merged.keys.append(None)
            merged.pubkeys.append(None)
            merged.hashes.append(None)
            merged.matches.append(False)
    return merged


# ---------------------------------------------------------------------------
# Benchmark helpers
# ---------------------------------------------------------------------------

def scan_rate(start=1, n=65536):
    """Single-threaded keys/sec across `n` derivations."""
    import production.native.affinity as affinity
    t = time.perf_counter()
    res = scan(start, n)
    dt = time.perf_counter() - t
    return n / dt, res


def scan_rate_threaded(start=1, n=65536, n_threads=None):
    """N-thread keys/sec across `n` derivations, one pinned worker per core."""
    t = time.perf_counter()
    res = scan_threaded(start, n, n_threads=n_threads)
    dt = time.perf_counter() - t
    return n / dt, res