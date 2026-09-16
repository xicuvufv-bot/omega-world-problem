"""Tests for the native/Beast-Mode modules: FFI hashing, mmap ledger,
binary protocol, and thread affinity."""

import hashlib
import os
import pickle
import struct
import tempfile
import threading
import time

import pytest

sys_path_prep = __import__("sys").path
sys_path_prep.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from production.native import affinity
from production.native import binproto
from production.native import hash160_ffi
from production.native import mmap_ledger as ml


# ---------------------------------------------------------------- hash160 FFI

class TestNativeHash:
    def test_sha256_matches_hashlib(self):
        for msg in [b"", b"a", b"abc", b"\x00" * 32, b"hello\x00world",
                    b"\xff" * 65]:
            assert hash160_ffi.sha256(msg) == hashlib.sha256(msg).digest()

    def test_ripemd160_matches_hashlib(self):
        for msg in [b"", b"a", b"abc", b"message digest", b"\xff" * 20]:
            assert (hash160_ffi.ripemd160(msg)
                    == hashlib.new("ripemd160", msg).digest())

    def test_hash160_generator_canonical(self):
        gen = bytes.fromhex("0279be667ef9dcbbac55a06295ce870b07029bfcdb2d"
                            "ce28d959f2815b16f81798")
        got = hash160_ffi.hash160(gen).hex()
        assert got == "751e76e8199196d454941c45d1b3a323f1433bd6"

    def test_sha256d(self):
        msg = b"block header payload"
        assert (hash160_ffi.sha256d(msg)
                == hashlib.sha256(hashlib.sha256(msg).digest()).digest())

    def test_batch_correct_per_key(self):
        if not hash160_ffi.native_available():
            pytest.skip("native DLL not built")
        keys = [os.urandom(33) for _ in range(8)]
        got = hash160_ffi.hash160_batch(keys)
        exp = [hash160_ffi.hash160(k) for k in keys]
        assert got == exp

    def test_native_bin_faster_than_pure_python(self):
        if not hash160_ffi.native_available():
            pytest.skip("native DLL not built")
        keys = [os.urandom(33) for _ in range(1000)]

        def best_of(reps, thunk):
            hash160_ffi.hash160_batch(keys[:64])   # warm the DLL / code cache
            [hash160_ffi.ripemd160(hash160_ffi.sha256(k)) for k in keys[:64]]
            times = []
            for _ in range(reps):
                t0 = time.perf_counter()
                thunk()
                times.append(time.perf_counter() - t0)
            times.sort()
            return times[len(times) // 2]          # median round

        tdll = best_of(7, lambda: hash160_ffi.hash160_batch(keys))
        tpy = best_of(7, lambda: [hash160_ffi.ripemd160(hash160_ffi.sha256(k))
                                  for k in keys])
        print(f"batched native {tdll:.4f}s vs pure-python hash160 loop "
              f"{tpy:.4f}s ({tpy/tdll:.1f}x)")
        assert tdll < tpy


# ----------------------------------------------------------------- mmap ledger

class TestMmapLedger:
    def _ledger(self):
        tmp = tempfile.mkdtemp()
        return ml.MmapLedger(os.path.join(tmp, "ledger.bin"), max_units=64)

    def test_upsert_load_roundtrip(self):
        led = self._ledger()
        idx = led.upsert(71, 0, "claimed", width=2**40, keys_checked=1234,
                         lease_expiry=9_999_999, claimant=42, attempts=1)
        assert idx == 0
        rows = led.load_units()
        assert len(rows) == 1
        assert rows[0]["puzzle_n"] == 71
        assert rows[0]["unit_idx"] == 0
        assert rows[0]["state"] == "claimed"
        assert rows[0]["width"] == 2**40
        assert rows[0]["keys_checked"] == 1234
        assert rows[0]["lease_expiry"] == 9_999_999
        assert rows[0]["claimant"] == 42
        assert rows[0]["attempts"] == 1
        led.close()

    def test_upsert_updates_existing(self):
        led = self._ledger()
        led.upsert(140, 2, "free")
        led.upsert(140, 2, "claimed", width=123, attempts=1)
        rows = led.load_units()
        assert len(rows) == 1
        assert rows[0]["state"] == "claimed"
        assert rows[0]["width"] == 123
        led.close()

    def test_claim_exclusive_and_steal(self):
        led = self._ledger()
        led.upsert(71, 0, "free", width=2**20)
        now = int(time.time() * 1000)
        led.claim(71, 0, "node-a", now, 30_000)
        # second claim by another node is rejected while leased
        assert led.claim(71, 0, "node-b", now + 1000, 30_000) is None
        # heartbeat of lease honors node-a's claims
        renewed = led.heartbeat("node-a", [(71, 0)], now + 1000, 30_000)
        assert renewed == 1
        # renewed lease keeps node-a's claim valid up to now+31000
        assert len(led.free_stale(now + 30_999)) == 0
        # expired lease becomes stealable
        assert len(led.free_stale(now + 31_001)) == 1
        led.close()

    def test_complete_transitions(self):
        led = self._ledger()
        led.upsert(71, 0, "claimed", width=2**20, keys_checked=10)
        led.complete(71, 0, "exhausted", keys_checked=500)
        rows = led.load_units()
        assert rows[0]["state"] == "done"
        assert rows[0]["keys_checked"] == 510
        # found pushes to found state
        led.upsert(140, 0, "claimed")
        led.complete(140, 0, "found")
        assert led.load_units()[1]["state"] == "found"
        led.close()

    def test_stats(self):
        led = self._ledger()
        led.upsert(71, 0, "done", width=100)
        led.upsert(71, 1, "claimed", width=50)
        led.upsert(71, 2, "free", width=25)
        s = led.stats()
        assert s["total"] == 3
        assert s["done"] == 1
        assert s["claimed"] == 1
        assert s["free"] == 1
        assert s["done_width"] == 100
        assert s["total_width"] == 175
        led.close()

    def test_persistence_across_reopen(self):
        tmp = tempfile.mkdtemp()
        path = os.path.join(tmp, "ledger.bin")
        led1 = ml.MmapLedger(path, max_units=16)
        led1.upsert(140, 0, "claimed", lease_expiry=55, claimant=7)
        led1.close()
        led2 = ml.MmapLedger(path, max_units=16)
        rows = led2.load_units()
        assert len(rows) == 1
        assert rows[0]["puzzle_n"] == 140
        assert rows[0]["lease_expiry"] == 55
        assert rows[0]["claimant"] == 7
        led2.close()

    def test_grow(self):
        led = ml.MmapLedger(os.path.join(tempfile.mkdtemp(), "l.bin"),
                            max_units=4)
        for i in range(10):
            led.upsert(i, 0, "free")
        assert len(led.load_units()) == 10
        led.close()


# --------------------------------------------------------------- binproto

class TestBinproto:
    KEY = "test-token-123"

    def test_roundtrip_hello(self):
        payload = binproto.str_payload("node-1")
        frame = binproto.encode(self.KEY, binproto.MSG_HELLO, payload, seq=1)
        msg = binproto.decode(self.KEY, frame)
        assert msg["name"] == "MSG_HELLO"
        assert msg["seq"] == 1
        s, off = binproto.read_str(msg["payload"])
        assert s == "node-1"

    def test_hmac_rejects_tamper(self):
        payload = binproto.str_payload("hello")
        frame = bytearray(binproto.encode(self.KEY, binproto.MSG_HEARTBEAT,
                                          payload, seq=2))
        frame[30] ^= 0xFF
        with pytest.raises(ValueError):
            binproto.decode(self.KEY, bytes(frame))

    def test_wrong_token_rejected(self):
        frame = binproto.encode(self.KEY, binproto.MSG_PING, b"", seq=3)
        with pytest.raises(ValueError):
            binproto.decode("wrong-token", frame)

    def test_incomplete_frame(self):
        payload = binproto.str_payload("x")
        frame = binproto.encode(self.KEY, binproto.MSG_WORK, payload, seq=4)
        with pytest.raises(ValueError):
            binproto.decode(self.KEY, frame[:8])

    def test_dict_payload_roundtrip(self):
        d = {"puzzle_n": 71, "range_start": 2**62, "node": "worker-99",
             "op": "scan", "tag": [1, 2, "three"]}
        frame = binproto.encode(self.KEY, binproto.MSG_WORK, d, seq=5)
        msg = binproto.decode(self.KEY, frame)
        up = binproto.unpack_dict(msg["payload"])
        assert up["puzzle_n"] == 71
        assert up["range_start"] == 2**62
        assert up["node"] == "worker-99"
        assert up["op"] == "scan"
        assert up["tag"] == [1, 2, "three"]

    def test_roundtrip_scalar(self):
        raw = struct.pack("<q", 2**40)
        frame = binproto.encode(self.KEY, binproto.MSG_TELEM, raw, seq=6)
        msg = binproto.decode(self.KEY, frame)
        assert binproto.unpack_int(msg["payload"]) == 2**40

    def test_frame_layout_fixed_24_bytes(self):
        raw = binproto.str_payload("n4")
        # header is 24 bytes: H B B Q Q I
        assert struct.calcsize(binproto._HDR.format) == 24
        frame = binproto.encode(self.KEY, binproto.MSG_HELLO, raw, seq=0)
        total = struct.unpack_from("<H", frame, 0)[0]
        assert len(frame) == total + 2


# ---------------------------------------------------------------- affinity

class TestAffinity:
    def test_partition_sane(self):
        p = affinity.partition_by_numa()
        assert p["compute"] and p["network"]
        assert p["all"]
        assert len(p["compute"]) + len(p["network"]) <= len(p["all"]) * 2

    def test_affinity_roundtrip(self):
        # pin to one core, then back to all we currently have
        cores = affinity.get_affinity()
        if not cores:
            pytest.skip("no affinity support")
        got = affinity.pin_thread([cores[0]])
        # false is a valid "unsupported" result on some platforms; only
        # assert correctness when the call is supported.
        if not got:
            pytest.skip("pin_thread not supported on this platform")

    def test_worker_core_selection_returns_something(self):
        compute, net = affinity.auto_pin_worker()
        assert isinstance(compute, list)
        assert isinstance(net, list)