#!/usr/bin/env python3
# ============================================================
# challenge70.py -- synthetic 70-bit ECDLP challenge generator
#
# Honesty contract: fully synthetic. k is seed-derived, never a
# real Bitcoin key. Independent verifier included (verify_instance).
#
# secp256k1: p = 2^256 - 2^32 - 977, n = order, G = generator.
# Interval DLP: k in [2^(B-1), 2^B) with B = 70, Q = k*G.
# Generates `count` independent instances (seed -> k -> Q),
# writes challenges.json for the payload + verifier.
# ============================================================
import json
import hashlib
import sys

P = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
N = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
GX = 0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798
GY = 0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8


def modinv(a, m):
    return pow(a, -1, m)


def point_add(p, q):
    if p is None:
        return q
    if q is None:
        return p
    x1, y1 = p
    x2, y2 = q
    if x1 == x2 and (y1 + y2) % P == 0:
        return None
    if p == q:
        lam = (3 * x1 * x1) * modinv(2 * y1, P) % P
    else:
        lam = (y2 - y1) * modinv(x2 - x1, P) % P
    x3 = (lam * lam - x1 - x2) % P
    y3 = (lam * (x1 - x3) - y1) % P
    return (x3, y3)


def scalar_mult(k, point=None):
    if point is None:
        point = (GX, GY)
    R = None
    base = point
    while k > 0:
        if k & 1:
            R = point_add(R, base)
        base = point_add(base, base)
        k >>= 1
    return R


def rand_in_interval(seed: int, bits: int) -> int:
    """Deterministic k in [2^(bits-1), 2^bits)."""
    h = hashlib.sha256(seed.to_bytes(8, "big")).digest()
    k = int.from_bytes(h, "big")
    mask = (1 << bits) - 1
    k &= mask
    k |= (1 << (bits - 1))
    return k


def generate(count: int, bits: int, base_seed: int, out_path: str):
    instances = []
    for i in range(count):
        seed = base_seed + i
        k = rand_in_interval(seed, bits)
        Q = scalar_mult(k)
        instances.append({
            "index": i,
            "seed": seed,
            "bits": bits,
            "k": hex(k),
            "Qx": hex(Q[0]),
            "Qy": hex(Q[1]),
        })
    payload = {
        "curve": "secp256k1",
        "bits": bits,
        "interval": "[2^%d, 2^%d)" % (bits - 1, bits),
        "count": count,
        "base_seed": base_seed,
        "instances": instances,
    }
    with open(out_path, "w") as f:
        json.dump(payload, f, indent=2)
    return payload


def verify_instance(inst: dict) -> bool:
    """Independent verification: k in interval, k*G == Q."""
    k = int(inst["k"], 16)
    bits = inst["bits"]
    if not ((1 << (bits - 1)) <= k < (1 << bits)):
        return False
    Q = scalar_mult(k)
    if Q[0] != int(inst["Qx"], 16) or Q[1] != int(inst["Qy"], 16):
        return False
    return True


def main():
    if len(sys.argv) < 4:
        print("usage: challenge70.py <count> <bits> <base_seed> [out_json]")
        print("  example: challenge70.py 10 70 0xC0FFEE challenges.json")
        return 1
    count = int(sys.argv[1])
    bits = int(sys.argv[2])
    base_seed = int(sys.argv[3], 0)
    out_path = sys.argv[4] if len(sys.argv) > 4 else "challenges.json"
    payload = generate(count, bits, base_seed, out_path)
    print("generated %d instances (bits=%d) -> %s" % (count, bits, out_path))
    ok = all(verify_instance(inst) for inst in payload["instances"])
    print("self-verify all: %d (expect 1)" % ok)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
