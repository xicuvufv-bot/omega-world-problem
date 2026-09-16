"""Tests for the production.cluster package.

Covers
  * protocol encode/decode, HMAC round-trip, tamper rejection
  * Scheduler claim / heartbeat / lease-expiry stealing / atomic ledger
  * Coordinator end-to-end: authenticated node connects, REQ_WORK, DONE/FOUND
  * Telemetry meter, snapshot, dashboard render
"""

import os
import socket
import sys
import threading
import time

import pytest

sys.path.insert(0, os.path.abspath(os.path.join(__file__, "..", "..", "..")))

from production.cluster import protocol, scheduler, transport, manager as cmanager
from production import telemetry, validator
from production.cluster import node as cluster_node


# ──────────────────────────────────────────────────────────── protocol

class TestProtocol:
    def test_roundtrip(self):
        tok = protocol.new_token()
        seq = 1
        enc = protocol.encode(tok, protocol.Msg.PING, {"x": 1}, seq)
        dec = protocol.decode(tok, enc)
        assert dec["m"] == protocol.Msg.PING
        assert dec["d"] == {"x": 1}
        assert dec["s"] == seq

    def test_bad_token_rejected(self):
        tok1, tok2 = protocol.new_token(), protocol.new_token()
        enc = protocol.encode(tok1, protocol.Msg.PING, {"x": 1}, 42)
        with pytest.raises(protocol.ProtocolError, match="bad signature"):
            protocol.decode(tok2, enc)

    def test_nonce_unique(self):
        assert protocol.nonce() != protocol.nonce()


# ──────────────────────────────────────────────────────────── scheduler

class TestScheduler:
    def _make_units(self, n=4, puzzle_n=71):
        units = []
        lo = 0x40000000000000000
        step = 0x1000000000000000
        for i in range(n):
            s = lo + i * step
            e = s + step - 1
            units.append(scheduler.Unit("%d:%d" % (puzzle_n, i), puzzle_n,
                                        "bitcrack", "%x" % s, "%x" % e, step))
        return units

    def test_claim_and_done(self):
        u = self._make_units(1)
        s = scheduler.Scheduler(u, lease_ms=100_000)
        got, _ = s.claim("nodeA", 1)
        assert len(got) == 1
        assert got[0].state == "claimed"
        assert got[0].claimant == "nodeA"
        s.complete(got[0].uid, "exhausted", keys_checked=got[0].width)
        st = s.stats()
        assert st["done"] == 1
        assert st["free"] == 0

    def test_steal_after_lease_expiry(self):
        u = self._make_units(1)
        s = scheduler.Scheduler(u, lease_ms=5000, now_fn=lambda: 1000)
        got, _ = s.claim("nodeA", 1)
        uid = got[0].uid
        assert got[0].claimant == "nodeA"
        # advance now past lease
        got2, stolen = s.claim("nodeB", 1, now=16000)
        assert len(got2) == 1
        assert got2[0].claimant == "nodeB"
        assert got2[0].uid == uid
        assert stolen > 0

    def test_heartbeat_extends_lease(self):
        u = self._make_units(1)
        s = scheduler.Scheduler(u, lease_ms=5000, now_fn=lambda: 1000)
        got, _ = s.claim("nodeA", 1)
        uid = got[0].uid
        leases = s.heartbeat("nodeA", [uid], now=3000)
        assert uid in leases
        assert leases[uid] == 5000
        # nodeB shouldn't be able to steal before expiry
        got2, _ = s.claim("nodeB", 1, now=5000)
        assert len(got2) == 0

    def test_persist_and_load(self, tmp_path):
        u = self._make_units(2)
        s = scheduler.Scheduler(u, lease_ms=10_000, now_fn=lambda: 1000)
        s.claim("nodeA", 1)
        s.save(str(tmp_path / "ledger.json"))
        loaded = scheduler.Scheduler.load(str(tmp_path / "ledger.json"),
                                          now_fn=lambda: 1000)
        assert loaded.stats()["claimed"] == 1
        assert loaded.stats()["total"] == 2

    def test_done_width_accounting(self):
        u = self._make_units(1)
        s = scheduler.Scheduler(u, lease_ms=100_000)
        got, _ = s.claim("nodeA", 1)
        s.complete(got[0].uid, "exhausted", keys_checked=got[0].width)
        st = s.stats()
        assert st["done_width"] == got[0].width
        assert st["total_width"] == st["done_width"]


# ──────────────────────────────────────────────────────────── telemetry

class TestTelemetry:
    def test_rate_meter_sliding(self):
        m = telemetry.RateMeter(window_s=5.0)
        t0 = time.time()
        m.feed(t0, 1000)
        m.feed(t0 + 0.5, 1000)
        m.feed(t0 + 1.0, 1000)
        assert m.kps(t0 + 1.0) > 1500

    def test_telemetry_store_snapshot(self):
        s = telemetry.TelemetryStore()
        p = protocol.PeerInfo("n1", "test", [{"id": 0, "mem": 8}],
                              {}, "127.0.0.1", {})
        s.register(p)
        s.heartbeat("n1")
        snap = s.snapshot()
        assert len(snap["nodes"]) == 1
        assert snap["nodes"][0]["name"] == "test"

    def test_render_dashboard_smoke(self):
        snap = {"ts": 1.0, "total_kps": 12345.0, "nodes": [
            {"node_id": "n1", "name": "gpu-a", "kps": 12345.0,
             "units_done": 10, "found": 0, "last_seen_ms": 1000,
             "online": True}],
                "scheduler": {"free": 2, "claimed": 0, "done": 4,
                              "total": 6},
                "history": [(0, 0), (1, 12345)]}
        out = telemetry.render_dashboard(snap)
        assert "n1" in out
        assert "gpu-a" in out
        assert "C2 CLUSTER DASHBOARD" in out


# ──────────────────────────────────────────────────────────── coordinator

class _FakeUnitExecutor:
    """Simulates completing an R1 unit instantly (no engine binary needed)."""
    kind = "bitcrack"

    def __init__(self, found=None):
        self.found = found

    def execute(self, unit, puzzle_lookup=None):
        if self.found:
            return {"outcome": "found", "keys_checked": int(unit["width"]),
                    "artifacts": self.found}
        return {"outcome": "exhausted", "keys_checked": int(unit["width"])}


class TestCoordinatorIntegration:
    def _start_coordinator(self, executor, lease_ms=100_000):
        u0 = scheduler.Unit("71:0", 71, "bitcrack",
                            "400000000000000000", "4fffffffffffffffff",
                            0x1000000000000000)
        sch = scheduler.Scheduler([u0], lease_ms=lease_ms)
        tele = telemetry.TelemetryStore()
        tok = protocol.new_token()
        coord = cmanager.Coordinator(tok, sch, tele, lease_ms=lease_ms)
        srv = transport.CoordinatorServer(tok, "127.0.0.1", 0)
        srv.on("_cfg", lambda peer, data: {"lease_ms": lease_ms})
        srv.on(protocol.Msg.REQ_WORK, coord._on_req_work)
        srv.on(protocol.Msg.HEARTBEAT, coord._on_heartbeat)
        srv.on(protocol.Msg.DONE, coord._on_done)
        srv.on(protocol.Msg.FOUND, coord._on_found)
        srv.on(protocol.Msg.TELEM, coord._on_telem)
        t = threading.Thread(target=srv.serve, daemon=True)
        t.start()
        time.sleep(0.1)
        port = srv._sock.getsockname()[1]
        return tok, port, srv, sch

    def test_node_lifecycle(self):
        tok, port, srv, sch = self._start_coordinator(_FakeUnitExecutor())
        try:
            conn, info = transport.connect("127.0.0.1", port, tok,
                                           name="test", gpus=[{"id": 0}])
            conn.send(protocol.Msg.REQ_WORK, {"want": 1})
            msg = conn.recv(10)
            assert msg and msg["m"] == protocol.Msg.WORK
            units = msg["d"]["units"]
            assert len(units) == 1
            unit = units[0]
            assert unit["puzzle_n"] == 71
            conn.send(protocol.Msg.DONE, {"unit": unit["uid"],
                                          "outcome": "exhausted",
                                          "keys_checked": unit["width"]})
            ack = conn.recv(5)
            assert ack and ack["m"] == protocol.Msg.DONE
            assert ack["d"]["ok"] is True
            st = sch.stats()
            assert st["done"] == 1
            conn.close()
        finally:
            srv.stop()

    def test_heartbeat_keeps_lease(self):
        tok, port, srv, sch = self._start_coordinator(_FakeUnitExecutor(),
                                                       lease_ms=5000)
        try:
            conn, info = transport.connect("127.0.0.1", port, tok, name="hb")
            conn.send(protocol.Msg.REQ_WORK, {"want": 1})
            msg = conn.recv(10)
            uid = msg["d"]["units"][0]["uid"]
            now = time.time() * 1000
            # send heartbeat before expiry
            conn.send(protocol.Msg.HEARTBEAT, {"units": [uid]})
            hb = conn.recv(10)
            assert hb["m"] == "hb_ack"
            assert uid in hb["d"]["leases"]
            conn.close()
        finally:
            srv.stop()

    def test_found_reverified_offline(self):
        found = {"n": 1, "privkey_hex": "1",
                 "compressed_address": "1BgGZ9tcN4rm9KBzDn7KprQz87SZ26SAMH",
                 "uncompressed_address": "1BgGZ9tcN4rm9KBzDn7KprQz87SZ26SAMH",
                 "wif_compressed": "5HpHagv65nkxPCmqsbKhpnrv2QHMRDUmXAJp8zHcQL1eMhr4mf7Z",
                 "wif_uncompressed": "5HpHagv65nkxPCmqsbKhpnrv2QHMRDUmXAJp8zHcQL1eMhr4mf7Z",
                 "matched_form": "compressed"}
        tok, port, srv, sch = self._start_coordinator(_FakeUnitExecutor(),
                                                       lease_ms=100_000)
        try:
            conn, _ = transport.connect("127.0.0.1", port, tok, name="fnd")
            conn.send(protocol.Msg.REQ_WORK, {"want": 1})
            msg = conn.recv(10)
            uid = msg["d"]["units"][0]["uid"]
            conn.send(protocol.Msg.FOUND, {"unit": uid, "artifacts": found})
            ack = conn.recv(10)
            assert ack["m"] == protocol.Msg.FOUND
            assert ack["d"]["ok"] is True
            st = sch.stats()
            assert st["found"] == 1
            conn.close()
        finally:
            srv.stop()


# ──────────────────────────────────────────────────────────── node executor

class TestEngineExecutor:
    def test_missing_pubkey_r2_returns_error(self):
        exc = cluster_node.EngineExecutor("kangaroo")
        unit = {"puzzle_n": 1, "start_hex": "1", "end_hex": "2",
                "width": 2, "uid": "1:0"}
        class FakePuzzle:
            n = 1
            regime = "R2"
            pubkey = None
            address = ""
            lo_hex = "1"
            hi_hex = "2"
        result = exc.execute(unit, puzzle_lookup=lambda **kw: FakePuzzle())
        assert result["outcome"] == "error"
        assert "pubkey" in result["reason"]


# ──────────────────────────────────────────────────────────── full node stack

class TestEndToEndWorkerNode:
    """Real Coordinator.serve() + WorkerNode.run() over localhost TCP."""

    def _free_port(self):
        s = socket.socket()
        s.bind(("127.0.0.1", 0))
        p = s.getsockname()[1]
        s.close()
        return p

    def test_coordinator_drives_node_to_completion(self):
        tok = protocol.new_token()
        u0 = scheduler.Unit("71:0", 71, "bitcrack",
                            "400000000000000000", "4fffffffffffffffff",
                            0x1000000000000000)
        sch = scheduler.Scheduler([u0], lease_ms=120_000)
        tele = telemetry.TelemetryStore()
        coord = cmanager.Coordinator(tok, sch, tele, lease_ms=120_000)
        port = self._free_port()
        t = threading.Thread(target=lambda: coord.serve("127.0.0.1", port),
                             daemon=True)
        t.start()
        time.sleep(0.2)

        node = cluster_node.WorkerNode("127.0.0.1", port, tok, name="e2e",
                                       slots=1, executor=_FakeUnitExecutor())
        tn = threading.Thread(target=node.run, daemon=True)
        tn.start()

        deadline = time.time() + 10
        while time.time() < deadline:
            if sch.stats()["done"] >= 1:
                break
            time.sleep(0.2)
        assert sch.stats()["done"] == 1
        assert sch.stats()["free"] == 0
        snap = tele.snapshot()
        assert len(snap["nodes"]) >= 1
        assert snap["nodes"][0]["units_done"] >= 1
        node.stop()
        coord.stop()


# ──────────────────────────────────────────────────────────── edges

class TestSchedulerEdge:
    def test_found_prevents_stealing(self):
        u = [scheduler.Unit("71:0", 71, "bitcrack", "a", "b", 10)]
        s = scheduler.Scheduler(u, lease_ms=5000, now_fn=lambda: 1000)
        got, _ = s.claim("nA", 1)
        s.complete(got[0].uid, "found")
        got2, _ = s.claim("nB", 1, now=999999)
        assert len(got2) == 0

    def test_dead_not_stealable(self):
        u = [scheduler.Unit("71:0", 71, "bitcrack", "a", "b", 10)]
        s = scheduler.Scheduler(u, lease_ms=5000, now_fn=lambda: 1000)
        got, _ = s.claim("nA", 1)
        s.complete(got[0].uid, "error")
        s.complete(got[0].uid, "error")
        u0 = s.units["71:0"]
        u0.attempts = 3
        u0.state = "dead"
        got2, _ = s.claim("nB", 1, now=999999)
        assert len(got2) == 0