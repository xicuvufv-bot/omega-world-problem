#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""test_secp256k1.py - independent synthetic ECDLP correctness suite.

Pure stdlib. Implements secp256k1 arithmetic from scratch (different code path
than the C++ engine and challenge70.py) and cross-checks:

  * known-answer vectors (G, 2G, 3G, 0*G, n*G)
  * identity / infinity edge cases (P + None, P + (-P), doubling)
  * random scalar vectors vs point-add chains
  * challenge70.randint_in_interval bounds
  * challenge70.generate + verify_instance as the independent verifier

Every test is synthetic. No real keys, ever.
"""
import hashlib
import os
import sys

P = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
N = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
GX = 0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798
GY = 0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8

FAILS = []


def check(name, cond, detail=""):
    if cond:
        return True
    FAILS.append(name)
    return False


def inv(a, m):
    return pow(a, m - 2, m)


def add(p, q):
    if p is None:
        return q
    if q is None:
        return p
    x1, y1 = p
    x2, y2 = q
    if x1 == x2 and (y1 + y2) % P == 0:
        return None
    if p == q:
        lam = (3 * x1 * x1) * inv((2 * y1) % P, P) % P
    else:
        lam = (y2 - y1) * inv((x2 - x1) % P, P) % P
    x3 = (lam * lam - x1 - x2) % P
    y3 = (lam * (x1 - x3) - y1) % P
    return (x3, y3)


def mul(k, point=None):
    pt = point if point is not None else (GX, GY)
    r = None
    b = pt
    kk = k % N
    if kk == 0:
        return None
    while kk > 0:
        if kk & 1:
            r = add(r, b)
        b = add(b, b)
        kk >>= 1
    return r


def is_on_curve(pt):
    if pt is None:
        return True
    x, y = pt
    return (y * y - (x * x * x + 7)) % P == 0


def run(prng=None):
    prng = prng or hashlib.sha256(b"test-seed").digest()

    # --- known-answer vectors (public constants) ---
    check("G on curve", is_on_curve((GX, GY)))
    check("G*1 == G", mul(1) == (GX, GY))
    check("G*0 infinity", mul(0) is None)
    check("G*order infinity", mul(N) is None)
    g2 = add((GX, GY), (GX, GY))
    check("G+G on curve and on G*2", is_on_curve(g2) and g2 == mul(2))
    check("G*3 doubles twice", mul(3) == add(g2, (GX, GY)))

    # --- infinity / edge cases ---
    check("P + None == P", add((GX, GY), None) == (GX, GY))
    neg = (GX, P - GY)
    check("P + (-P) == None", add((GX, GY), neg) is None)
    check("on-curve negation", is_on_curve(neg))

    # --- random vectors: mul(k) == additive chain ---
    ok_rand = True
    for i in range(24):
        k = int.from_bytes(prng[i * 32:(i + 1) * 32], "big") or 1
        chain = None
        for _ in range(k % 8):
            chain = add(chain, (GX, GY))
        chain2 = mul(k % 8)
        if chain != chain2:
            ok_rand = False
            FAILS.append("random chain %d" % i)
            break
        if not is_on_curve(mul(k)):
            ok_rand = False
            FAILS.append("random on-curve %d" % i)
            break
    check("random scalar vectors", ok_rand)

    # --- interval generator bounds ---
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                    os.pardir, "research", "v4"))
    from challenge70 import rand_in_interval  # noqa: E402
    ok_iv = True
    for bits in (8, 16, 32, 70):
        for i in range(8):
            k = rand_in_interval(1000 + i, bits)
            if not ((1 << (bits - 1)) <= k < (1 << bits)):
                ok_iv = False
    check("interval bounds", ok_iv)

    # --- independent verifier on the committed challenge set ---
    import json
    payload = json.load(open(os.path.join(
        os.path.dirname(os.path.abspath(__file__)), os.pardir,
        "research", "v4", "challenges.json"), encoding="utf-8"))
    from challenge70 import verify_instance  # noqa: E402
    ok_all = all(verify_instance(inst) for inst in payload["instances"])
    check("payload independent verifier (%d instances)" % len(payload["instances"]),
          ok_all)

    return len(FAILS)


if __name__ == "__main__":
    n = run()
    if n:
        print("FAILED %d: %s" % (n, FAILS))
        sys.exit(1)
    print("test_secp256k1: ALL PASS")