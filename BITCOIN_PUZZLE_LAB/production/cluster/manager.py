"""Coordinator: the brain of the cluster.

Owns
   * the Scheduler (unit pool + lease stealing),
   * the TelemetryStore (aggregate hashrate + node table),
   * the global cluster ledger (atomic),
   * found-key verification (re-derives the address offline before trusting
     any node's claim).

Security posture
   * token-bound HMAC on every frame + challenge/response auth,
   * optional TLS wrap for WAN links,
   * every node sends full unit context back on DONE; the coordinator RE-VERIFIES
     the key against the registry address before persisting a found record,
   * the Scheduler only ever issues units built from the frozen registry —
     an arbitrary address never enters the wire protocol.
"""

import json
import logging
import os
import threading
import time

from .. import checkpoint as ckpt
from .. import validator
from . import protocol, transport

log = logging.getLogger("cluster.coordinator")

DEFAULT_PORT = 25200


class Coordinator:
    def __init__(self, token, scheduler, telemetry, ledger_path=None,
                 state_dir=None, lease_ms=60_000):
        self.token = token
        self.scheduler = scheduler
        self.telemetry = telemetry
        self.lease_ms = lease_ms
        self.state_dir = state_dir or ckpt.STATE_DIR
        self.ledger_path = ledger_path or os.path.join(self.state_dir,
                                                       "cluster_ledger.json")
        self._lock = threading.RLock()
        self._stop = threading.Event()
        self.server = None
        self._found_hook = None    # callable(artifacts, node_id) if set

    # ----------------------------------------------------------- lifecycle
    def on_found(self, hook):
        self._found_hook = hook
        return self

    def serve(self, host="0.0.0.0", port=DEFAULT_PORT,
              certfile=None, keyfile=None):
        srv = transport.CoordinatorServer(self.token, host, port,
                                          certfile=certfile, keyfile=keyfile)
        srv.on("_cfg", lambda peer, data: {"lease_ms": self.lease_ms})
        srv.on(protocol.Msg.REQ_WORK, self._on_req_work)
        srv.on(protocol.Msg.HEARTBEAT, self._on_heartbeat)
        srv.on(protocol.Msg.DONE, self._on_done)
        srv.on(protocol.Msg.FOUND, self._on_found)
        srv.on(protocol.Msg.TELEM, self._on_telem)
        srv.on(protocol.Msg.PING, lambda peer, data: {"echo": "pong"})
        srv.on("subscribe", self._on_subscribe)
        self.server = srv

        tick = threading.Thread(target=self._publish_loop, daemon=True)
        tick.start()
        try:
            srv.serve()
        finally:
            self._stop.set()
            self.scheduler.save(self.ledger_path)

    def stop(self):
        self._stop.set()
        if self.server:
            self.server.stop()

    # ------------------------------------------------------------- handlers
    def _on_req_work(self, peer, data):
        want = max(1, min(int(data.get("want", 1)), 64))
        units, stolen = self.scheduler.claim(peer.node_id, want)
        self._persist()
        return {"units": [u.to_dict() for u in units],
                "reap_ms": stolen}

    def _on_heartbeat(self, peer, data):
        leases = self.scheduler.heartbeat(peer.node_id, data.get("units", []))
        self.telemetry.heartbeat(peer.node_id)
        return {"leases": leases}

    def _on_done(self, peer, data):
        uid = data.get("unit")
        outcome = data.get("outcome", "exhausted")
        keys = int(data.get("keys_checked") or 0)
        u = self.scheduler.complete(uid, outcome, keys)
        self.telemetry.finish(peer.node_id, u, keys,
                              os.getenv("CLUSTER_NODE_RATE_SCALE", "1"))
        self._persist()
        return {"ok": True, "state": u.state if u else None}

    def _on_found(self, peer, data):
        """Node-claimed hit path: re-verify offline before accepting it."""
        artifacts = data.get("artifacts")
        if not artifacts:
            return {"ok": False, "reason": "missing artifacts"}
        addr = artifacts.get("compressed_address")
        target = artifacts.get("target")
        try:
            if target:
                # defense: target must be a registry address, re-derive locally
                from .. import registry as reg
                p = reg.resolve_target(address=target)
                check = validator.verify_candidate(
                    artifacts["privkey_hex"], p.address)
            else:
                check = validator.verify_candidate(
                    artifacts["privkey_hex"], addr)
        except (validator.ValidationError, KeyError, reg.RegistryError) as e:
            log.warning("FOUND rejected from %s: %s", peer.node_id, e)
            return {"ok": False, "reason": str(e)}
        path = self._persist_found(check, peer.node_id)
        self.scheduler.complete(data.get("unit"), "found")
        self.telemetry.found(peer.node_id)
        self._persist()
        if self._found_hook:
            try:
                self._found_hook(check, peer.node_id, path)
            except Exception:                            # noqa: BLE001
                log.exception("found hook failed")
        return {"ok": True, "path": path, "key": check["privkey_hex"]}

    def _on_telem(self, peer, data):
        self.telemetry.rate(peer.node_id, float(data.get("kps") or 0),
                            data.get("gpu_id"))
        return None

    def _on_subscribe(self, peer, data):
        return {"metrics": self.telemetry.snapshot()}

    # -------------------------------------------------------------- helpers
    def _persist(self):
        try:
            self.scheduler.save(self.ledger_path)
        except OSError as e:
            log.warning("ledger persist failed: %s", e)

    def _persist_found(self, artifacts, node_id):
        os.makedirs(ckpt.FOUND_DIR, exist_ok=True)
        addr = artifacts["compressed_address"]
        path = os.path.join(ckpt.FOUND_DIR,
                            "cluster_%s_puzzle_%s_%s.txt"
                            % (node_id.split("_")[-1][:6], addr[:8], addr))
        with open(path, "w", encoding="utf-8") as fh:
            fh.write("# cluster FOUND reported by %s\n" % node_id)
            fh.write("privkey_hex=%s\n" % artifacts["privkey_hex"])
            fh.write("compressed_address=%s\n" % artifacts["compressed_address"])
            fh.write("uncompressed_address=%s\n" % artifacts["uncompressed_address"])
            fh.write("wif_compressed=%s\n" % artifacts["wif_compressed"])
            fh.write("wif_uncompressed=%s\n" % artifacts["wif_uncompressed"])
            fh.write("matched_form=%s\n" % artifacts["matched_form"])
        log.info("FOUND confirmed for %s via %s (→ %s)",
                 artifacts["compressed_address"], node_id, path)
        return path

    def _publish_loop(self, interval=2.0):
        while not self._stop.is_set():
            time.sleep(interval)
            snap = self.telemetry.snapshot()
            try:
                with open(os.path.join(self.state_dir, "cluster_metrics.json"),
                          "w", encoding="utf-8") as fh:
                    json.dump(snap, fh, indent=1, sort_keys=True)
            except OSError:
                pass