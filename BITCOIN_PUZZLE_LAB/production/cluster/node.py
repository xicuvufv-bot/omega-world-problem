"""Worker node daemon.  One authenticated connection per GPU *slot*, each
slot pulling units from the coordinator, executing them with a local executor
(the native engine wrapper), and reporting DONE/FOUND + telemetry.

Running a node never requires a registry decision on the node side: the
coordinator mints units from the frozen registry and the node just runs them.
"""

import logging
import os
import socket
import threading
import time

from .. import gpu as gpu_mod
from .. import registry
from .. import runner
from . import protocol, transport

log = logging.getLogger("cluster.node")

NO_WORK_POLL_S = 4.0
HEARTBEAT_S = 5.0


class EngineExecutor:
    """Local engine runner (per-slot).  Injects the node's NATIVE progress
    hook so keys/s stream into telemetry instead of waiting for completion."""

    def __init__(self, binary_kind="bitcrack", bin_dir=None, extra=None,
                 device=None, binary_path=None, on_progress=None):
        self.kind = binary_kind
        self.bin_dir = bin_dir
        self.extra = extra
        self.device = device
        self.binary_path = binary_path
        self.on_progress = on_progress

    def resolve_binary(self, puzzle):
        if self.binary_path:
            return self.binary_path
        name = "kangaroo" if puzzle.regime == "R2" else "cuBitCrack"
        env = "KANGAROO" if puzzle.regime == "R2" else "BITCRACK"
        env_path = os.environ.get(env)
        if env_path:
            return env_path
        import glob
        base = self.bin_dir or os.path.join(os.path.dirname(os.path.dirname(
            os.path.abspath(__file__))), "bin")
        found = glob.glob(os.path.join(base, name + ".*"))
        return found[0] if found else name

    def execute(self, unit, puzzle_lookup=None):
        """unit: scheduler.Unit dict; returns dict for the coordinator."""
        p = (puzzle_lookup or registry.resolve_target)(number=unit["puzzle_n"])
        binary = self.resolve_binary(p)
        engine = self.kind
        if engine == "auto":
            engine = "kangaroo" if p.regime == "R2" else "bitcrack"
        if engine == "kangaroo" and not p.pubkey:
            return {"outcome": "error", "reason": "no pubkey for R2"}

        share = {"share_idx": int(unit["uid"].split(":")[1]),
                 "total_shares": 0,
                 "start_hex": unit["start_hex"],
                 "end_hex": unit["end_hex"],
                 "start": int(unit["start_hex"], 16),
                 "end": int(unit["end_hex"], 16)}
        found_artifacts = {}

        def hook(artifacts):
            found_artifacts.update(artifacts)

        res = runner.run_worker(binary, p, engine, share,
                                device=self.device, extra=self.extra,
                                on_found_artifacts=hook,
                                on_progress=self.on_progress)
        if res == "found":
            return {"outcome": "found",
                    "keys_checked": int(unit["width"]),
                    "artifacts": found_artifacts}
        if res == "error":
            return {"outcome": "error"}
        return {"outcome": "exhausted", "keys_checked": int(unit["width"])}


class WorkerSlot:
    """One GPU slot == one connection == one active unit."""

    def __init__(self, node, gpu_idx, executor):
        self.node = node
        self.gpu_idx = gpu_idx
        self.executor = executor
        self.active = set()
        self._stop = threading.Event()

    def run(self):
        while not self._stop.is_set():
            try:
                conn, info = transport.connect(
                    self.node.host, self.node.port, self.node.token,
                    name=self.node.name, gpus=[{"id": self.gpu_idx}
                                               if self.gpu_idx is not None else None],
                    engine_bin={"kind": self.executor.kind},
                    tls=self.node.tls)
            except (OSError, protocol.ProtocolError) as e:
                log.warning("slot %s reconnect in %.0fs: %s",
                            self.gpu_idx, NO_WORK_POLL_S, e)
                if self._stop.wait(NO_WORK_POLL_S):
                    return
                continue
            try:
                self._session(conn, info)
            finally:
                conn.close()
        log.info("slot %s stopped", self.gpu_idx)

    def _session(self, conn, info):
        hb = threading.Thread(target=self._heartbeat, args=(conn, info),
                              daemon=True)
        hb.start()
        while not self._stop.is_set():
            try:
                with self.node.send_lock:
                    conn.send(protocol.Msg.REQ_WORK, {"want": 1})
            except OSError:
                return
            try:
                msg = conn.recv(30)
            except OSError:
                return  # peer went away (shutdown/reset) -> reconnect loop
            if msg is None:
                return
            if msg["m"] == protocol.Msg.NO_WORK:
                if self._stop.wait(NO_WORK_POLL_S):
                    return
                continue
            if msg["m"] != protocol.Msg.WORK:
                continue
            data = msg["d"]
            units = data.get("units", [])
            if not units:
                continue
            unit = units[0]
            self.active.add(unit["uid"])
            try:
                out = self.executor.execute(unit)
            except Exception as e:                        # noqa: BLE001
                log.exception("unit %s failed", unit["uid"])
                out = {"outcome": "error", "reason": str(e)}
            finally:
                self.active.discard(unit["uid"])
            try:
                with self.node.send_lock:
                    if out.get("outcome") == "found":
                        conn.send(protocol.Msg.FOUND, {
                            "unit": unit["uid"],
                            "artifacts": out.get("artifacts", {}),
                        })
                    else:
                        conn.send(protocol.Msg.DONE, {
                            "unit": unit["uid"],
                            "outcome": out.get("outcome", "exhausted"),
                            "keys_checked": out.get("keys_checked", 0),
                        })
            except OSError:
                return
        try:
            with self.node.send_lock:
                conn.send(protocol.Msg.BYE, {})
        except OSError:
            pass

    def _heartbeat(self, conn, info, every=HEARTBEAT_S):
        lease_ms = info.get("lease_ms", 60_000)
        while not self._stop.is_set():
            if self._stop.wait(every):
                return
            try:
                with self.node.send_lock:
                    conn.send(protocol.Msg.HEARTBEAT,
                              {"units": list(self.active)})
            except OSError:
                return


class WorkerNode:
    def __init__(self, host, port, token, name="worker", slots=1,
                 executor=None, tls=False, gpu_indices=None,
                 send_lock=None):
        self.host = host
        self.port = port
        self.token = token
        self.name = name
        self.slots = slots
        self.executor = executor
        self.tls = tls
        self._gpu_indices = gpu_indices
        self.send_lock = send_lock or threading.Lock()
        self._threads = []
        self._slots = []

    def run(self):
        devices = self._gpu_indices
        if devices is None:
            sm = gpu_mod.summary()
            devices = [d["id"] for d in sm["devices"]] if sm["present"] else []
        if not devices:
            devices = [None] * self.slots
        if self.executor is None:
            self.executor = EngineExecutor("auto")
        for i in range(max(1, len(devices))):
            slot = WorkerSlot(self, devices[i], self.executor)
            self._slots.append(slot)
            t = threading.Thread(target=slot.run, daemon=True,
                                 name="slot-%s" % i)
            t.start()
            self._threads.append(t)
        for t in self._threads:
            t.join()

    def stop(self):
        for slot in self._slots:
            slot._stop.set()