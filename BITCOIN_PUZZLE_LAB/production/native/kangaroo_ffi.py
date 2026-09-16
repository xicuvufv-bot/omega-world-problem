"""FFI bridge to the native Pollard-Kangaroo engine.

Wraps ``kangaroo_engine.c`` (``bin/kangaroo.dll`` on Windows,
``libkangaroo.so`` / ``libkangaroo.dylib`` elsewhere).  The engine solves
interval discrete logs on secp256k1: for a public key Q known to have a
private key k in [A, B] it returns k.

The walk is the classic λ/Kangaroo: ``ntame`` tame kangaroos start at
random offsets inside the interval and hop with the *same* deterministic
jump table as ``nwild`` wild ones starting at Q; distinguished points
(low ``dpbits`` bits of affine x zero) are CAS-inserted into a shared DP
table, and an x-coordinate collision between opposite herds yields the
candidate k = T - U.  The whole herd walks in lockstep with one
Montgomery batch inversion per round, so thousands of kangaroos share a
single Fermat inversion -- the arithmetic cost per kangaroo-step is tiny.

Public surface (the names you actually want):

    selftest()                       -> 1 on pass
    solve(A, B, target, ...)         -> KangarooResult (one-shot, any threads)
    Context(A, B, target, ...)       -> checkpointable engine handle

``KangarooResult`` carries .found / .k (int) / .steps / .dps / .cross /
.elapsed_s.

Thread-safety: ONE engine context is shared by all worker threads (the DP
table is the shared memory; the walk is per-thread and collision-safe via
CAS).  ``solve`` spawns ``n_threads`` workers against a single context and
stops them on first hit.  Don't create two engines over the same DP buffer.

Checkpointing: pass ``checkpoint=path`` and the DP table is backed by a
mmapped file.  Re-opening the same path with the same A/B reuses the
accumulated DP table (kr_new validates magic/version/bounds), and a fresh
``seed`` re-seeds the herds without repeating old walks.
"""

import ctypes
import mmap
import os
import secrets
import sys
import threading
import time
from dataclasses import dataclass

_DIR = os.path.dirname(os.path.abspath(__file__))
_BIN = os.path.join(os.path.dirname(os.path.dirname(_DIR)), "bin")

KR_HDRSIZE = 160
KR_SLOT = 96
HDR_VERSION, HDR_FLAGS, HDR_CTRL = 8, 16, 24
HDR_SEED, HDR_STEPS, HDR_DPS, HDR_CROSS = 32, 40, 48, 56
HDR_KEY = 64

_LIB = None
_LOCK = threading.Lock()


def _libpath():
    if sys.platform == "win32":
        return os.path.join(_BIN, "kangaroo.dll")
    if sys.platform == "darwin":
        return os.path.join(_BIN, "libkangaroo.dylib")
    return os.path.join(_BIN, "libkangaroo.so")


def _load():
    global _LIB
    if _LIB is not None:
        return _LIB
    path = _libpath()
    if not os.path.exists(path):
        return None
    try:
        if sys.platform == "win32":
            lib = ctypes.WinDLL(path)
        else:
            lib = ctypes.CDLL(path)
    except OSError:
        return None

    lib.kr_selftest.restype = ctypes.c_int

    lib.kr_new.argtypes = [
        ctypes.c_char_p,                  # A32
        ctypes.c_char_p,                  # B32
        ctypes.c_void_p, ctypes.c_int,    # pub, publen
        ctypes.c_void_p, ctypes.c_uint64, # dpmem, dmem_size
        ctypes.c_int,                     # nthreads
        ctypes.c_int, ctypes.c_int,       # ntame, nwild
        ctypes.c_int,                     # dpbits
        ctypes.c_uint64,                  # seed
        ctypes.c_uint64,                  # budget
        ctypes.POINTER(ctypes.c_int),     # errcode
    ]
    lib.kr_new.restype = ctypes.c_void_p

    lib.kr_worker.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_int,
                              ctypes.c_void_p]
    lib.kr_worker.restype = ctypes.c_int
    lib.kr_reset.argtypes = [ctypes.c_void_p, ctypes.c_uint64, ctypes.c_uint64]
    lib.kr_reset.restype = ctypes.c_int
    lib.kr_stop.argtypes = [ctypes.c_void_p]
    lib.kr_stop.restype = None
    lib.kr_stats.argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p,
                             ctypes.c_void_p, ctypes.c_void_p]
    lib.kr_stats.restype = None
    lib.kr_free.argtypes = [ctypes.c_void_p]
    lib.kr_free.restype = None

    with _LOCK:
        _LIB = lib
    return lib


def native_available():
    return _load() is not None


def selftest():
    """Run the in-C self-test (1 = pass). Raises if the DLL is missing."""
    lib = _load()
    if lib is None:
        raise RuntimeError("kangaroo native library not built; see README")
    return lib.kr_selftest()


def _check_bounds(A, B):
    A, B = int(A), int(B)
    if not (1 <= A < B):
        raise ValueError("bounds must satisfy 1 <= A < B")
    return A, B


def _check_target(target):
    if isinstance(target, str):
        target = target.strip()
        target = bytes.fromhex(target)
    target = bytes(target)
    if len(target) not in (33, 65):
        raise ValueError("target must be a 33-byte compressed or 65-byte uncompressed pubkey")
    if target[0] not in (0x02, 0x03, 0x04):
        raise ValueError("target must carry a SEC-1 prefix byte (02/03/04)")
    return target


def _default_dp_slots(dpbits):
    """DP table sized so insert-rate stays low: slots >= 2^(dpbits+4) keeps
    x-collisions rare for walks up to ~2^(dpbits+20) steps; cap at 2^26
    slots (4 GiB)."""
    lo = max(1 << (dpbits + 4), 1 << 10)
    hi = 1 << 26
    return lo, hi


@dataclass
class KangarooResult:
    found: bool = False
    k: int = None
    steps: int = 0
    dps: int = 0
    cross: int = 0
    elapsed_s: float = 0.0

    def __bool__(self):
        return self.found


class _DPBuffer:
    """Contiguous byte area handed to the engine as the DP table.

    ``addr`` and ``size`` are what kr_new consumes.  Anonymous buffers use a
    ctypes arena (guaranteed contiguous, addressable via addressof);
    checkpointed buffers are file-backed mmaps so the table survives.
    """

    def __init__(self, size, path=None):
        self.size = size
        self.path = os.path.abspath(path) if path else None
        if self.path:
            self._fd = os.open(self.path, os.O_RDWR | os.O_CREAT, 0o600)
            try:
                os.ftruncate(self._fd, size)
            except OSError:
                pass
            self.mm = mmap.mmap(self._fd, size)
            self._view = self.mm
            self.addr = _addr_of(self.mm)
        else:
            self.mm = None
            self._view = ctypes.create_string_buffer(size)
            self.addr = ctypes.addressof(self._view)
            self._fd = None

    def read_at(self, off, n):
        if self.path:
            self.mm.seek(off)
            return self.mm.read(n)
        return bytes(self._view[off:off + n])

    def flush(self):
        if self.mm is not None:
            self.mm.flush()

    def close(self):
        if getattr(self, "mm", None) is not None:
            self.mm.close()
            self.mm = None
        if getattr(self, "_fd", None) is not None:
            os.close(self._fd)
            self._fd = None


def _addr_of(mm):
    """Base address of a Python buffer object (mmap) as c_void_p."""
    one = ctypes.c_char.from_buffer(mm)
    return ctypes.c_void_p(ctypes.addressof(one))


class Context:
    """One engine instance over one DP buffer.

    ``n_threads`` is fixed at creation (the herd split lives in the engine);
    ``run()`` spawns that many worker threads against the shared engine.
    """

    def __init__(self, A, B, target, n_threads=1, ntame=8, nwild=8,
                 dpbits=14, seed=None, budget=1 << 40,
                 checkpoint=None, dp_slots=None):
        self._lib = _load()
        if self._lib is None:
            raise RuntimeError("kangaroo native library not built; see README")
        A, B = _check_bounds(A, B)
        self.A, self.B = A, B
        self.target = _check_target(target)
        self.n_threads = max(1, min(32, int(n_threads)))
        if ntame < 1 or nwild < 1:
            raise ValueError("need at least 1 tame and 1 wild kangaroo")
        self.ntame, self.nwild = int(ntame), int(nwild)
        self.dpbits = int(dpbits)
        if not (1 <= self.dpbits <= 31):
            raise ValueError("dpbits must be in [1, 31]")
        self.budget = int(budget) or (1 << 40)
        self.seed = int(secrets.randbits(64)) if seed is None else int(seed)

        lo, hi = _default_dp_slots(self.dpbits)
        if dp_slots is not None:
            slots = max(int(dp_slots), 1 << 2)
        else:
            slots = lo
        slots = min(slots, hi)
        self.nslots = slots
        self._dmem_size = KR_HDRSIZE + slots * KR_SLOT
        self._checkpoint = os.path.abspath(checkpoint) if checkpoint else None

        if self._checkpoint and os.path.exists(self._checkpoint):
            # resume: reuse the on-disk table; kr_new validates A/B header.
            pass
        self._buf = _DPBuffer(self._dmem_size, self._checkpoint)
        self._ptr = self._create_engine()

    def _create_engine(self):
        err = ctypes.c_int(0)
        a = int(self.A).to_bytes(32, "big")
        b = int(self.B).to_bytes(32, "big")
        ptr = self._lib.kr_new(a, b, self.target, len(self.target),
                               self._buf.addr, self._buf.size,
                               self.n_threads, self.ntame, self.nwild,
                               self.dpbits,
                               self.seed & 0xFFFFFFFFFFFFFFFF,
                               self.budget & 0xFFFFFFFFFFFFFFFF,
                               ctypes.byref(err))
        if not ptr:
            raise RuntimeError("kr_new failed (errcode=%d); "
                               "check A/B vs. existing checkpoint" % err.value)
        return ptr

    def stats(self):
        s = ctypes.c_uint64(0)
        d = ctypes.c_uint64(0)
        f = ctypes.c_uint64(0)
        c = ctypes.c_uint64(0)
        self._lib.kr_stats(self._ptr, ctypes.byref(s), ctypes.byref(d),
                           ctypes.byref(f), ctypes.byref(c))
        return s.value, d.value, f.value, c.value

    def stop(self):
        if self._ptr:
            self._lib.kr_stop(self._ptr)

    def key(self):
        """32-byte BE private key from the header (zeros until found)."""
        return self._buf.read_at(HDR_KEY, 32)

    def close(self):
        if getattr(self, "_ptr", None):
            self._lib.kr_free(self._ptr)
            self._ptr = None
        if getattr(self, "_buf", None):
            if self._buf.path:
                self._buf.flush()
            self._buf.close()
            self._buf = None

    def __del__(self):
        try:
            self.close()
        except Exception:
            pass

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        self.close()


# ---------------------------------------------------------------------------
# high-level solve
# ---------------------------------------------------------------------------

def _worker_proc(engine, tid, n_threads, out_buf, error_box, result_box,
                 core=None):
    try:
        if core is not None:
            import production.native.affinity as aff
            aff.pin_thread([core])
        rc = engine._lib.kr_worker(engine._ptr, tid, n_threads, out_buf)
        result_box[0] = rc
    except Exception as exc:  # noqa: BLE001  -- report back
        error_box.append(exc)


def solve(A, B, target, n_threads=None, ntame=8, nwild=8, dpbits=14,
          seed=None, budget=1 << 40, checkpoint=None, dp_slots=None,
          pin=True):
    """Solve Q = k*G, k in [A, B], via the native kangaroo engine.

    Spawns ``n_threads`` pinned worker threads against one shared context
    and returns a KangarooResult when a worker reports the hit.
    """
    import production.native.affinity as affinity

    if n_threads is None:
        n_threads = affinity.get_cpu_count()
    n_threads = max(1, min(int(n_threads), 32))
    if pin is True:
        cores = list(range(affinity.get_cpu_count()))
    elif pin:
        cores = list(pin)
    else:
        cores = None

    rs = KangarooResult()
    t0 = time.perf_counter()
    with Context(A, B, target, n_threads=n_threads, ntame=ntame, nwild=nwild,
                 dpbits=dpbits, seed=seed, budget=budget,
                 checkpoint=checkpoint, dp_slots=dp_slots) as ctx:
        outs = [(ctypes.c_ubyte * 32)() for _ in range(n_threads)]
        eboxes = [[] for _ in range(n_threads)]
        rboxes = [[None] for _ in range(n_threads)]
        threads = []
        for t in range(n_threads):
            core = cores[t % len(cores)] if cores else None
            th = threading.Thread(
                target=_worker_proc,
                args=(ctx, t, n_threads, outs[t], eboxes[t], rboxes[t]),
                kwargs={"core": core},
                daemon=True)
            threads.append(th)
            th.start()

        found = False
        while any(th.is_alive() for th in threads):
            if all(rboxes[t][0] is not None for t in range(n_threads)):
                found = any(rboxes[t][0] == 1 for t in range(n_threads))
                break
            time.sleep(0.005)
        ctx.stop()
        for th in threads:
            th.join(5)

        errs = [e for box in eboxes for e in box]
        if errs:
            raise errs[0]

        steps, dps, flags, cross = ctx.stats()
        rs.found = bool(flags & 1)
        rs.steps = steps
        rs.dps = dps
        rs.cross = cross
        if rs.found:
            rs.k = int.from_bytes(ctx.key(), "big")
    rs.elapsed_s = time.perf_counter() - t0
    if rs.found:
        _verify_k(A, B, rs.k)
    return rs


def _verify_k(A, B, k):
    """Sanity gate: found private key must lie in [A, B].  (Full pubkey
    verification belongs to the runner/tests against algorithms/curve.py.)"""
    if not (A <= k <= B):
        raise RuntimeError("kangaroo engine reported k=%d outside [A,B]" % k)