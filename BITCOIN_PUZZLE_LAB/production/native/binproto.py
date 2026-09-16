"""Raw binary protocol for the cluster wire — struct-packed, zero-JSON.

Frame layout (no variable-length fields in the header):
  [ 0: 2]  total_len    uint16 LE   (excludes this 2-byte field)
  [ 2: 3]  msg_type     uint8       (see MSG_* constants)
  [ 3: 4]  flags        uint8       (bit 0=compressed, bit 1=urgent)
  [ 4:12]  seq          uint64 LE
  [12:20]  ts_ms        uint64 LE   (epoch ms)
  [20:24]  payload_len  uint32 LE
  [24:24+N]  payload    N bytes     (msgpack-free: raw struct per type)
  [24+N:24+N+32] HMAC   HMAC-SHA256 of [msg_type..payload]

Variable data (strings, lists) is length-prefixed inside the payload:
  [0:4] len then len bytes.

Fixed-size fields avoid parsing overhead entirely.  A single recv() of
``total_len + 2`` bytes gives the complete frame — no streaming parse
needed for messages under 64 KB.
"""

import hashlib
import hmac
import os
import struct
import time

# message types (fits in uint8)
MSG_HELLO      = 0x01
MSG_CHALLENGE  = 0x02
MSG_AUTH       = 0x03
MSG_ACCEPT     = 0x04
MSG_REJECT     = 0x05
MSG_REQ_WORK   = 0x10
MSG_WORK       = 0x11
MSG_NO_WORK    = 0x12
MSG_HEARTBEAT  = 0x20
MSG_HB_ACK     = 0x21
MSG_DONE       = 0x30
MSG_FOUND      = 0x31
MSG_TELEM      = 0x40
MSG_PING       = 0x50
MSG_PONG       = 0x51
MSG_BYE        = 0x60
MSG_ERROR      = 0xFF

_NAMES = {v: k for k, v in globals().items() if k.startswith("MSG_")}

# HMAC header
_HMAC_LEN = 32
# total_len(2) + type(1) + flags(1) + seq(8) + ts(8) + payload_len(4) = 24
_HDR = struct.Struct("<HBBQQI")
_HDR_FIELDS = "total", "type", "flags", "seq", "ts_ms", "payload_len"


def sign(token, data):
    return hmac.new(token.encode("utf-8") if isinstance(token, str) else token,
                    data, hashlib.sha256).digest()


def encode(token, msg_type, payload, seq, flags=0, ts_ms=None):
    ts_ms = ts_ms or int(time.time() * 1000)
    if isinstance(payload, (bytes, bytearray)):
        raw_payload = bytes(payload)
    elif isinstance(payload, dict):
        raw_payload = _pack_dict(payload)
    else:
        raw_payload = b""
    total = (_HDR.size - 2) + len(raw_payload) + _HMAC_LEN
    hdr = _HDR.pack(total, msg_type, flags, seq, ts_ms, len(raw_payload))
    body = hdr + raw_payload
    mac = sign(token, body)
    return body + mac


def decode(token, data):
    if len(data) < _HDR.size + _HMAC_LEN:
        raise ValueError("frame too short")
    total_len = struct.unpack_from("<H", data, 0)[0]
    if len(data) < total_len + 2:
        raise ValueError("incomplete frame")
    body = data[:total_len + 2 - _HMAC_LEN]
    mac = data[total_len + 2 - _HMAC_LEN: total_len + 2]
    expect = sign(token, body)
    if not hmac.compare_digest(mac, expect):
        raise ValueError("bad HMAC")
    msg_type, flags, seq, ts_ms, plen = struct.unpack_from("<BBQQI", data, 2)
    payload = data[_HDR.size: _HDR.size + plen]
    return {"type": msg_type, "flags": flags, "seq": seq, "ts_ms": ts_ms,
            "payload": payload, "name": _NAMES.get(msg_type, "0x%02x" % msg_type)}


# ──────────────────────────────────────────────── payload packers

_T_STR = 0
_T_INT = 1
_T_FLOAT = 2
_T_BYTES = 3
_T_LIST = 4


def _pack_dict(d):
    parts = []
    for k, v in d.items():
        key_b = k.encode("utf-8")
        if isinstance(v, str):
            val_b = v.encode("utf-8")
            parts.append(struct.pack("<HHB", len(key_b), len(val_b), _T_STR) +
                         key_b + val_b)
        elif isinstance(v, bool):
            val_b = b"\x01" if v else b"\x00"
            parts.append(struct.pack("<HHB", len(key_b), 1, _T_INT) +
                         key_b + val_b)
        elif isinstance(v, int):
            val_b = struct.pack("<q", v)
            parts.append(struct.pack("<HHB", len(key_b), len(val_b), _T_INT) +
                         key_b + val_b)
        elif isinstance(v, float):
            val_b = struct.pack("<d", v)
            parts.append(struct.pack("<HHB", len(key_b), len(val_b), _T_FLOAT) +
                         key_b + val_b)
        elif isinstance(v, (list, tuple)):
            val_b = _pack_list(v)
            parts.append(struct.pack("<HHB", len(key_b), len(val_b), _T_LIST) +
                         key_b + val_b)
        elif isinstance(v, bytes):
            parts.append(struct.pack("<HHB", len(key_b), len(v), _T_BYTES) +
                         key_b + v)
        else:
            val_b = str(v).encode("utf-8")
            parts.append(struct.pack("<HHB", len(key_b), len(val_b), _T_STR) +
                         key_b + val_b)
    return b"".join(parts)


def _pack_list(lst):
    parts = [struct.pack("<I", len(lst))]
    for item in lst:
        if isinstance(item, dict):
            raw = _pack_dict(item)
            parts.append(struct.pack("<IB", len(raw), _T_LIST) + raw)
        elif isinstance(item, str):
            b = item.encode("utf-8")
            parts.append(struct.pack("<IB", len(b), _T_STR) + b)
        elif isinstance(item, bool):
            parts.append(struct.pack("<IB", 1, _T_INT) +
                         (b"\x01" if item else b"\x00"))
        elif isinstance(item, int):
            parts.append(struct.pack("<IB", 8, _T_INT) + struct.pack("<q", item))
        elif isinstance(item, float):
            parts.append(struct.pack("<IB", 8, _T_FLOAT) + struct.pack("<d", item))
        else:
            b = str(item).encode("utf-8")
            parts.append(struct.pack("<IB", len(b), _T_STR) + b)
    return b"".join(parts)


def unpack_dict(data):
    """Decode a dict payload into typed Python values."""
    out = {}
    off = 0
    while off + 5 <= len(data):
        klen, vlen, typ = struct.unpack_from("<HHB", data, off)
        off += 5
        if off + klen + vlen > len(data):
            break
        key = data[off:off + klen].decode("utf-8", errors="replace")
        val_raw = data[off + klen:off + klen + vlen]
        off += klen + vlen
        if typ == _T_STR:
            out[key] = val_raw.decode("utf-8", errors="replace")
        elif typ == _T_INT and vlen == 8:
            out[key] = struct.unpack("<q", val_raw)[0]
        elif typ == _T_INT:
            out[key] = int.from_bytes(val_raw, "little")
        elif typ == _T_FLOAT:
            out[key] = struct.unpack("<d", val_raw)[0]
        elif typ == _T_BYTES:
            out[key] = val_raw
        elif typ == _T_LIST:
            out[key] = _unpack_list(val_raw)
    return out


def _unpack_list(raw):
    if len(raw) < 4:
        return []
    (n,) = struct.unpack_from("<I", raw, 0)
    off = 4
    out = []
    for _ in range(n):
        if off + 5 > len(raw):
            break
        (vlen,) = struct.unpack_from("<I", raw, off)
        typ = raw[off + 4]
        val = raw[off + 5:off + 5 + vlen]
        off += 5 + vlen
        if typ == _T_STR:
            out.append(val.decode("utf-8", errors="replace"))
        elif typ == _T_INT and vlen == 8:
            out.append(struct.unpack("<q", val)[0])
        elif typ == _T_INT:
            out.append(int.from_bytes(val, "little"))
        elif typ == _T_FLOAT:
            out.append(struct.unpack("<d", val)[0])
        elif typ == _T_LIST:
            out.append(_unpack_list(val))
        else:
            out.append(val)
    return out


def unpack_str(raw):
    return raw.decode("utf-8", errors="replace") if raw else ""


def unpack_int(raw):
    if len(raw) == 8:
        return struct.unpack("<q", raw)[0]
    elif len(raw) == 4:
        return struct.unpack("<I", raw)[0]
    return 0


# ──────────────────────────────────── helpers

def str_payload(s):
    b = s.encode("utf-8")
    return struct.pack("<I", len(b)) + b


def read_str(raw, off=0):
    if off + 4 > len(raw):
        return "", off
    n = struct.unpack_from("<I", raw, off)[0]
    off += 4
    if off + n > len(raw):
        return "", off
    return raw[off:off + n].decode("utf-8", errors="replace"), off + n