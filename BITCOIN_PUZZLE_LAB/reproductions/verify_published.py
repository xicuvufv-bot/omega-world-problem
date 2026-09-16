"""Verify every published SOLVED puzzle end-to-end with zero dependencies.

For each puzzle the tracker marks SOLVED:
  1. we recompute the compressed pubkey for the published private key,
  2. hash160 it, then
  3. construct the base58check P2PKH address ourselves (stdlib only),
and require every field to match the tracker exactly. Any mismatch is a
signal to stop and investigate (data corruption, parsing bug, or wrong
key convention) before trusting downstream analysis.

Usage:  python reproductions/verify_published.py
"""

import hashlib
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from algorithms.curve import scalar_mult, compressed
from algorithms.hash import hash160
from algorithms.interval import parse_tracker, RAW_TRACKER

B58 = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"


def b58check(version_byte: int, h160: bytes) -> str:
    payload = bytes([version_byte]) + h160
    checksum = hashlib.sha256(hashlib.sha256(payload).digest()).digest()[:4]
    num = int.from_bytes(payload + checksum, "big")
    out = ""
    while num:
        num, rem = divmod(num, 58)
        out = B58[rem] + out
    # leading zero bytes -> leading '1's
    for b in payload + checksum:
        if b != 0:
            break
        out = "1" + out
    return out


def main():
    rows = [r for r in parse_tracker(RAW_TRACKER) if r.solved]
    ok = fails = 0
    for r in rows:
        k = int(r.priv, 16)
        pk = compressed(scalar_mult(k))
        h160 = hash160(pk)
        addr = b58check(0, h160)
        if addr == r.address and pk.hex() == r.pub:
            ok += 1
        else:
            fails += 1
            print(f"mismatch puzzle #{r.n}: addr {addr} vs {r.address}; "
                  f"pk {pk.hex()} vs {r.pub}")
    print(f"verified {ok}/{len(rows)} published solves end-to-end "
          f"(privkey -> pubkey -> hash160 -> base58check address)")
    return fails


if __name__ == "__main__":
    sys.exit(1 if main() else 0)