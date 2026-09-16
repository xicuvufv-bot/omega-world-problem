"""Cluster wire protocol: sealed length-prefixed envelopes over TCP/TLS.

Every message is a JSON envelope signed with HMAC-SHA256(key=shared token):

    wire = <4B sig_len><sig><4B payload_len><payload>

Envelope shape:
    {"m": <type>, "t": <epoch ms>, "s": <seq>, "d": <dict>}

Connect-time authentication is challenge/response, so the raw 32-byte token
is never transmitted.  Replay is bounded per-connection by a monotonic seq
and the coordinator rejecting stale seqs for a given peer.
"""

import hashlib
import hmac
import json
import socket
import struct
import time

RESERVED_SEQ_LIMIT = 1 << 40

HEADER = struct.Struct(">II")  # sig_len, payload_len
MAX_FRAME = 16 * 1024 * 1024


class Msg:
    HELLO = "hello"
    CHALLENGE = "challenge"
    AUTH = "auth"
    ACCEPT = "accept"
    REJECT = "reject"
    REQ_WORK = "req_work"
    WORK = "work"
    NO_WORK = "no_work"
    HEARTBEAT = "heartbeat"
    HB_ACK = "hb_ack"
    DONE = "done"
    FOUND = "found"
    TELEM = "telem"
    PING = "ping"
    PONG = "pong"
    BYE = "bye"
    ERROR = "error"


class ProtocolError(Exception):
    pass


def _b64(data):
    import base64
    return base64.b64encode(data).decode("ascii")


def sign(token, payload):
    return hmac.new(token.encode("utf-8"), payload, hashlib.sha256).hexdigest()


def encode(token, mtype, data, seq):
    env = {"m": mtype, "t": int(time.time() * 1000), "s": seq, "d": data}
    canonical = json.dumps(env, sort_keys=True, separators=(",", ":"),
                           default=str).encode("utf-8")
    sig = sign(token, canonical).encode("ascii")
    return HEADER.pack(len(sig), len(canonical)) + sig + canonical


def decode(token, wire):
    if len(wire) < HEADER.size:
        raise ProtocolError("short frame")
    sig_len, payload_len = HEADER.unpack_from(wire[:HEADER.size])
    pos = HEADER.size
    if pos + sig_len + payload_len != len(wire):
        raise ProtocolError("frame length mismatch")
    sig = wire[pos:pos + sig_len]
    payload = wire[pos + sig_len:]
    if sig_len > 128 or payload_len > MAX_FRAME:
        raise ProtocolError("frame too large")
    expect = sign(token, payload)
    if not hmac.compare_digest(sig.decode("ascii"), expect):
        raise ProtocolError("bad signature")
    env = json.loads(payload.decode("utf-8"))
    if not isinstance(env, dict) or "m" not in env or "d" not in env:
        raise ProtocolError("malformed envelope")
    return env


class Conn:
    """Buffered, framing-safe connection.  Both sides speak this."""

    def __init__(self, sock, token, role, timeout=10.0):
        self.sock = sock
        self.token = token
        self.role = role
        self.timeout = timeout
        self._rfile = sock.makefile("rb")
        self._seq = 0

    def send(self, mtype, data):
        self._seq += 1
        self.sock.sendall(encode(self.token, mtype, data, self._seq))

    def recv(self, timeout=None):
        self.sock.settimeout(self.timeout if timeout is None else timeout)
        head = self._rfile.read(HEADER.size)
        if len(head) < HEADER.size:
            return None  # peer closed cleanly
        sig_len, payload_len = HEADER.unpack(head)
        if sig_len > 128 or payload_len > MAX_FRAME:
            raise ProtocolError("frame too large")
        body = self._rfile.read(sig_len + payload_len)
        if len(body) < sig_len + payload_len:
            raise ProtocolError("truncated frame")
        return decode(self.token, head + body)

    def close(self):
        try:
            self.sock.shutdown(socket.SHUT_RDWR)
        except OSError:
            pass
        try:
            self.sock.close()
        except OSError:
            pass


class PeerInfo:
    """Remote endpoint metadata refreshed by the coordinator from HELLO."""
    FIELDS = ("node_id", "name", "gpus", "engine_bin", "host", "hw")

    def __init__(self, node_id, name, gpus, engine_bin, host, hw):
        self.node_id = node_id
        self.name = name
        self.gpus = gpus
        self.engine_bin = engine_bin or {}
        self.host = host
        self.hw = hw or {}

    def to_dict(self):
        import copy
        d = copy.copy(vars(self))
        return {k: (v if not hasattr(v, "to_dict") else v.to_dict())
                for k, v in d.items()}


# ---------------------------------------------------------------------- helpers

def new_token(bits=256):
    import secrets
    return secrets.token_urlsafe(bits // 8)


def nonce():
    import secrets
    return secrets.token_hex(16)