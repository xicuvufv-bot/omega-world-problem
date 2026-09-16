"""Real-time telemetry store + ASCII dashboard.

Aggregates keys/s per node from completed-unit widths (sliding window), keeps
a short history for the text chart, and renders a human-readable C2 status
table with ETA per active puzzle.
"""

import json
import os
import threading
import time
from collections import deque

WINDOW_S = 60.0
HISTORY = 48


class RateMeter:
    """Sliding-window keys/s from (timestamp, keys) point events."""

    def __init__(self, window_s=WINDOW_S):
        self.window_s = window_s
        self.events = deque()

    def feed(self, ts, keys):
        if keys <= 0:
            return
        self.events.append((ts, float(keys)))
        while self.events and self.events[0][0] < ts - self.window_s:
            self.events.popleft()

    def kps(self, now=None):
        if not self.events:
            return 0.0
        now = now or time.time()
        while self.events and self.events[0][0] < now - self.window_s:
            self.events.popleft()
        if len(self.events) < 1:
            return 0.0
        oldest = self.events[0][0]
        span = max(now - oldest, 1e-3)
        total = sum(k for _, k in self.events)
        return total / span


class NodeView:
    def __init__(self, node_id, name, gpus=None):
        self.node_id = node_id
        self.name = name
        self.gpus = gpus or []
        self.meter = RateMeter()
        self.units_done = 0
        self.found = 0
        self.last_seen_ms = time.time() * 1000
        self.online = True
        self.puzzle = {}
        self.kps = 0.0

    def touch(self):
        self.last_seen_ms = time.time() * 1000

    def to_dict(self):
        return {"node_id": self.node_id, "name": self.name,
                "gpus": self.gpus, "kps": round(self.kps, 1),
                "units_done": self.units_done, "found": self.found,
                "last_seen_ms": int(self.last_seen_ms), "online": self.online}


class TelemetryStore:
    def __init__(self, history=HISTORY):
        self.nodes = {}
        self.history = deque(maxlen=history)
        self.lock = threading.RLock()
        self.scheduler_stats = {}

    def register(self, peer):
        with self.lock:
            if peer.node_id not in self.nodes:
                self.nodes[peer.node_id] = NodeView(peer.node_id,
                                                    peer.name, peer.gpus)

    def rate(self, node_id, kps, gpu_id=None):
        with self.lock:
            n = self._upsert(node_id)
            n.touch()
            n.kps = float(kps)
            if gpu_id:
                n.puzzle["gpu"] = gpu_id

    def heartbeat(self, node_id):
        with self.lock:
            n = self._upsert(node_id)
            n.touch()

    def finish(self, node_id, unit, keys, scale="1"):
        with self.lock:
            n = self._upsert(node_id)
            n.touch()
            n.units_done += 1
            if unit:
                ms = time.time() * 1000
                n.meter.feed(ms / 1000.0, keys or 0)
                n.puzzle["unit"] = unit.uid
                n.puzzle["puzzle_n"] = unit.puzzle_n

    def found(self, node_id):
        with self.lock:
            n = self._upsert(node_id)
            n.found += 1

    def _upsert(self, node_id, name=None):
        n = self.nodes.get(node_id)
        if n is None:
            n = NodeView(node_id, name or node_id)
            self.nodes[node_id] = n
        return n

    def prune(self, stale_ms=15_000):
        now = time.time() * 1000
        with self.lock:
            for nid in list(self.nodes):
                if now - self.nodes[nid].last_seen_ms > stale_ms:
                    self.nodes[nid].online = False

    def total_kps(self):
        with self.lock:
            return sum(n.meter.kps() for n in self.nodes.values())

    def snapshot(self):
        self.prune()
        with self.lock:
            for n in self.nodes.values():
                n.kps = n.meter.kps()
            total = sum(n.kps for n in self.nodes.values())
            self.history.append((time.time(), total))
            nodes = [n.to_dict() for n in
                     sorted(self.nodes.values(), key=lambda n: -n.kps)]
            return {"ts": time.time(), "total_kps": total,
                    "nodes": nodes,
                    "scheduler": dict(self.scheduler_stats or {}),
                    "history": list(self.history)}


def meter_bar(v, width=34, maxv=None):
    w = 1 if v > 0 else 0
    if maxv and maxv > 0:
        w = max(w, int(width * v / maxv))
    bar = "#" * min(w, width) + "-" * max(0, width - w)
    return bar


def render_dashboard(snap, rates_label="Mkey/s"):
    out = []
    total = snap.get("total_kps", 0.0)
    units = max(1, abs(total) / 1e6) if total else 1
    out.append("=" * 78)
    out.append("C2 CLUSTER DASHBOARD  total=%.2f %s (%d nodes)"
               % (total, rates_label, len(snap.get("nodes", []))))
    out.append("=" * 78)

    hist = snap.get("history", [])
    maxv = max((v for _, v in hist), default=0.0) or 0.0
    for _, v in hist[-14:]:
        out.append(" %s %8.2f %s" % (meter_bar(v, 30, maxv), v, "kps"))

    out.append("-" * 78)
    out.append("%-12s %-20s %-8s %-10s %-7s %s"
               % ("NODE", "NAME", "KPS", "DONE", "FOUND", "STATE"))
    for n in snap.get("nodes", []):
        out.append("%-12s %-20s %-8.1f %-10d %-7d %s"
                   % (n["node_id"], n["name"][:20], n["kps"],
                      n["units_done"], n["found"],
                      "ONLINE" if n["online"] else "OFFLINE"))
    sc = snap.get("scheduler", {})
    if sc:
        done, total = sc.get("done", 0), sc.get("total", 0)
        pct = 100.0 * done / total if total else 0.0
        out.append("\npool: %d/%d units done (%.2f%%)" % (done, total, pct))
    return "\n".join(out)


def write_metrics(state_dir, snap):
    os.makedirs(state_dir, exist_ok=True)
    with open(os.path.join(state_dir, "cluster_metrics.json"), "w",
              encoding="utf-8") as fh:
        json.dump(snap, fh, indent=1, sort_keys=True)