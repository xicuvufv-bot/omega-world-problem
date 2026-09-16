"""Minimal TLS-capable TCP transport for the cluster protocol.

Thread-per-connection accept loop with a callback dispatcher.  TLS is used
when cert/key paths are supplied; otherwise the connection is plain TCP on a
trusted LAN/VPN.  Authenticity is always HMAC-protected by the shared token
(the ``token`` argument), so the wire stays tamper-evident without TLS too.
"""

import logging
import os
import socket
import ssl
import threading

from . import protocol

log = logging.getLogger("cluster.transport")

DTLS = None


def server_tls_context(certfile, keyfile):
    ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    ctx.minimum_version = ssl.TLSVersion.TLSv1_2
    ctx.load_cert_chain(certfile, keyfile)
    return ctx


def client_tls_context():
    ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    ctx.minimum_version = ssl.TLSVersion.TLSv1_2
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE  # pinned token is the real auth layer
    return ctx


def _wrap(sock, ctx):
    return ctx.wrap_socket(sock, server_side=True) if ctx else sock


class CoordinatorServer:
    """Accepts cluster connections; the handler is a plain dict of
    ``message_type -> callable(peer, data) -> reply_dict``."""

    def __init__(self, token, host="0.0.0.0", port=25200,
                 certfile=None, keyfile=None, backlog=64):
        self.token = token
        self.host = host
        self.port = port
        self.certfile = certfile
        self.keyfile = keyfile
        self.backlog = backlog
        self.handlers = {}
        self._sock = None
        self._threads = []
        self._stop = threading.Event()
        self.peers = {}          # conn_id -> Conn
        self.peers_lock = threading.Lock()

    def on(self, mtype, fn):
        self.handlers[mtype] = fn
        return self

    def serve(self):
        ctx = (server_tls_context(self.certfile, self.keyfile)
               if self.certfile else None)
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._sock.bind((self.host, self.port))
        self._sock.listen(self.backlog)
        log.info("coordinator listening on %s:%d (tls=%s)",
                 self.host, self.port, bool(ctx))
        while not self._stop.is_set():
            try:
                raw, addr = self._sock.accept()
            except OSError:
                break
            raw.settimeout(15)
            conn = _wrap(raw, ctx)
            t = threading.Thread(target=self._serve_conn,
                                 args=(conn, addr), daemon=True)
            t.start()
            self._threads.append(t)
        for t in self._threads:
            t.join(timeout=2)

    def stop(self):
        self._stop.set()
        with self.peers_lock:
            for conn in list(self.peers.values()):
                try:
                    conn.close()
                except OSError:
                    pass
        if self._sock:
            try:
                self._sock.close()
            except OSError:
                pass

    def _serve_conn(self, raw, addr):
        conn = protocol.Conn(raw, self.token, "server")
        cid = id(conn)
        with self.peers_lock:
            self.peers[cid] = conn
        try:
            auth = self._authenticate(conn, addr)
            if not auth:
                return
            peer, node_id = auth
            self._run(conn, peer)
        except (OSError, protocol.ProtocolError, ValueError):
            log.debug("conn %s ended : %s", addr, _ex())
        finally:
            with self.peers_lock:
                self.peers.pop(cid, None)
            conn.close()

    def _authenticate(self, conn, addr):
        try:
            return self._do_authenticate(conn, addr)
        except (OSError, protocol.ProtocolError):
            return None

    def _do_authenticate(self, conn, addr):
        hello = conn.recv(10)
        if not hello or hello["m"] != protocol.Msg.HELLO:
            log.warning("no HELLO from %s", addr)
            return None
        n0 = protocol.nonce()
        conn.send(protocol.Msg.CHALLENGE, {"nonce": n0})
        auth = conn.recv(10)
        if not auth or auth["m"] != protocol.Msg.AUTH:
            return None
        d = auth["d"]
        mac = d.get("mac")
        if not mac or mac != protocol.sign(self.token, n0.encode("ascii")):
            log.warning("auth rejected for %s", addr)
            conn.send(protocol.Msg.REJECT, {"reason": "bad auth"})
            return None
        cfg = self.handlers.get("_cfg")
        cfg_lease = cfg(peer=None, data={}) if cfg else {}
        lease_ms = cfg_lease.get("lease_ms", 60_000)
        node_id = "node_" + protocol.nonce()[:8]
        peer = protocol.PeerInfo(node_id=node_id,
                                 name=d.get("name", "anon-%s" % addr[0]),
                                 gpus=d.get("gpus", []),
                                 engine_bin=d.get("engine_bin", {}),
                                 host=d.get("host", addr[0]),
                                 hw=d.get("hw") or {})
        conn.send(protocol.Msg.ACCEPT, {"node_id": node_id,
                                        "lease_ms": lease_ms,
                                        "hello_interval_ms": 10_000})
        return peer, node_id

    def _run(self, conn, peer):
        while not self._stop.is_set():
            try:
                msg = conn.recv()
            except (socket.timeout, TimeoutError, ConnectionResetError,
                    BrokenPipeError, OSError, protocol.ProtocolError):
                return  # peer gone / frame corrupt / shutdown
            if msg is None:
                return
            mtype = msg["m"]
            fn = self.handlers.get(mtype)
            if not fn:
                conn.send(protocol.Msg.ERROR, {"reason": "unhandled %s" % mtype})
                continue
            try:
                reply = fn(peer, msg["d"])
            except Exception as e:                      # noqa: BLE001
                log.exception("handler %s failed", mtype)
                conn.send(protocol.Msg.ERROR, {"reason": str(e)})
                continue
            if reply is not None:
                conn.send(_reply_type(mtype), reply)

def _ex():
    import traceback
    return traceback.format_exc().strip().splitlines()[-1] if __debug__ else ""


def _reply_type(mtype):
    mapping = {
        "req_work": protocol.Msg.WORK,
        "heartbeat": protocol.Msg.HB_ACK,
        "ping": protocol.Msg.PONG,
        "done": protocol.Msg.DONE,
        "found": protocol.Msg.FOUND,
    }
    return mapping.get(mtype, protocol.Msg.NO_WORK)


def connect(host, port, token, name="worker", gpus=None, engine_bin=None,
            tls=False, hw=None, timeout=10):
    raw = socket.create_connection((host, port), timeout=timeout)
    if tls:
        raw = client_tls_context().wrap_socket(raw, server_hostname=host)
    raw.settimeout(timeout)
    conn = protocol.Conn(raw, token, "node")
    conn.send(protocol.Msg.HELLO, {
        "name": name, "gpus": gpus or [],
        "engine_bin": dict(engine_bin or {}), "host": host, "hw": hw or {},
    })
    chall = conn.recv(timeout)
    if not chall or chall["m"] != protocol.Msg.CHALLENGE:
        raise protocol.ProtocolError("no challenge")
    d = chall["d"]
    conn.send(protocol.Msg.AUTH, {
        "nonce": d["nonce"],
        "mac": protocol.sign(token, d["nonce"].encode("ascii")),
    })
    acc = conn.recv(timeout)
    if not acc or acc["m"] != protocol.Msg.ACCEPT:
        if acc and acc["m"] == protocol.Msg.REJECT:
            raise protocol.ProtocolError("rejected: %s" % acc["d"])
        raise protocol.ProtocolError("auth failed")
    return conn, acc["d"]