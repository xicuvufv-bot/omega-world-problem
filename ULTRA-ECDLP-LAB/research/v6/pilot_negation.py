#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""pilot_negation.py - V6 P1: measure K-factor classic vs negation-map kangaroo.

Paired, synthetic, CPU-side falsification of the K=2.08 -> K~1.15 claim
(RCKangaroo SOTA) using the lab's own toy group (research/gen.py) so the
mechanism -- not secp256k1 throughput -- is what's measured.

Design mirrors the lab payload: interval [2^(B-1), 2^B), tame=random point,
wild=random point + Q, x-driven jumps, PRE-jump DP records keyed on x,
k = Dt - Dw, independent kG==Q verify. The ONLY difference between modes is
y-canonicalization (negate point+distance when y > p//2).

K = group_ops / sqrt(interval_size). Classic expectation ~2.08.
A ratio negation/classic ~= 0.55 CONFIRMS the mechanism; ~= 1.0 REFUTES it.
"""
import hashlib
import json
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, os.pardir))
from gen import add, mul, TOY_P as P, TOY_L as L, TOY_G as G  # noqa: E402

W = 16


def build_jumps(B, seed):
    rng = int(hashlib.sha256(("jumps%d" % seed).encode()).hexdigest(), 16)
    jumps = []
    span = 1 << (B // 2)
    for i in range(W):
        rng = (rng * 6364136223846793005 + 1442695040888963407) & ((1 << 64) - 1)
        d = 1 + (rng % span)
        jumps.append((d, mul(d, G, P)))
    return jumps


def run_once(B, secret, jumps, dpbits, negate, cap_mult=25, debug=False):
    N = 1 << (B - 1)
    lo = 1 << (B - 1)
    Q = mul(secret, G, P)
    # tame: random offset in interval
    t0 = (secret * 6364136223846793005 + 0x9E3779B9) % N
    # wild: random offset in interval, shifted by Q
    w0 = (secret * 2862933555777941757 + 0x85EBCA6B) % N
    t_pt, w_pt = mul(lo + t0, G, P), add(mul(lo + w0, G, P), Q, P)
    t_d, w_d = (lo + t0) % L, (lo + w0) % L
    mask = (1 << dpbits) - 1
    tab = {}
    ops = 0
    cap = int(cap_mult * (N ** 0.5))
    half = P // 2

    def canon(pt, d):
        if negate and pt is not None and pt[1] > half:
            return ((pt[0], P - pt[1]), (L - d) % L)
        return pt, d

    t_pt, t_d = canon(t_pt, t_d)
    w_pt, w_d = canon(w_pt, w_d)
    # Loop escape (mandatory with negation maps: canonicalized walks fall
    # into tiny attractor cycles and spin forever; RCKangaroo/Mark1 ship
    # loop detection + restarts for exactly this reason).
    # CORRECT RULE for a deterministic walk: ANY revisit of a previously
    # visited x by the same walker means it entered a cycle -- exactly, no
    # probabilistic threshold. So the visited set must NEVER be cleared on
    # DP (clearing on DP wipes the evidence for DP-containing cycles and
    # the walker spins forever). Clear only on reseed. Memory is trivial
    # at pilot scale; production ports need bounded structures (RC RAM
    # management) -- recorded as a porting constraint in V6_STATE.
    import random as _rnd
    _rs = _rnd.Random(secret ^ 0x5EED)
    escapes = [0, 0]

    def reseed(kind):
        o = _rs.randrange(N)
        if kind == 0:
            pt, d = mul(lo + o, G, P), (lo + o) % L
        else:
            pt, d = add(mul(lo + o, G, P), Q, P), (lo + o) % L
        return canon(pt, d)

    visited = [set(), set()]
    visited[0].add(t_pt[0])
    visited[1].add(w_pt[0])
    while ops < cap:
        for pt, d, kind in ((t_pt, t_d, 0), (w_pt, w_d, 1)):
            idx = pt[0] & (W - 1)
            jd, jp = jumps[idx]
            npt = add(pt, jp, P)
            nd = (d + jd) % L
            npt, nd = canon(npt, nd)
            ops += 1
            if debug and ops % 20000 == 0:
                print("  ops=%d tab=%d escapes=%s" % (ops, len(tab), escapes),
                      flush=True)
            if npt[0] in visited[kind]:
                escapes[kind] += 1
                npt2, nd2 = reseed(kind)
                if kind == 0:
                    t_pt, t_d = npt2, nd2
                else:
                    w_pt, w_d = npt2, nd2
                visited[kind] = {npt2[0]}
                continue
            visited[kind].add(npt[0])
            if (npt[0] & mask) == 0:
                key = npt[0]
                if key in tab:
                    od, okind = tab[key]
                    if okind != kind:
                        # Negation flips the wild offset sign (X = D'G + sQ),
                        # so test both k = +(Dt-Dw) and k = -(Dt-Dw), exactly
                        # like RCKangaroo's Collision_SOTA candidate set.
                        # The kG==Q + interval check rejects the wrong one.
                        for kk in ((od - nd) % L, (nd - od) % L):
                            if lo <= kk < lo + N and mul(kk, G, P) == Q:
                                return {"solved": 1, "ops": ops, "k": kk,
                                        "escapes": escapes}
                else:
                    tab[key] = (nd, kind)
            if kind == 0:
                t_pt, t_d = npt, nd
            else:
                w_pt, w_d = npt, nd
    return {"solved": 0, "ops": ops, "k": None, "escapes": escapes}


def main():
    out = {"pairs": [], "summary": {}}
    for B in (24, 28, 32):
        N = 1 << (B - 1)
        for rep in range(12):
            seed = 1000 * B + rep
            h = hashlib.sha256(("secret%d" % seed).encode()).digest()
            secret = (1 << (B - 1)) | (int.from_bytes(h, "big") & ((1 << (B - 1)) - 1))
            jumps = build_jumps(B, seed)
            t0 = time.time()
            r0 = run_once(B, secret, jumps, 4, False)
            t1 = time.time()
            r1 = run_once(B, secret, jumps, 4, True)
            t2 = time.time()
            k0 = r0["ops"] / (N ** 0.5) if r0["solved"] else None
            k1 = r1["ops"] / (N ** 0.5) if r1["solved"] else None
            out["pairs"].append({"bits": B, "rep": rep, "secret": hex(secret),
                                 "classic": {**r0, "K": k0, "s": round(t1 - t0, 2)},
                                 "negation": {**r1, "K": k1, "s": round(t2 - t1, 2)}})
            print("B=%d rep=%d classic K=%s negation K=%s" %
                  (B, rep,
                   ("%.3f" % k0) if k0 else "FAIL",
                   ("%.3f" % k1) if k1 else "FAIL"), flush=True)
    for mode in ("classic", "negation"):
        ks = [p[mode]["K"] for p in out["pairs"] if p[mode]["K"] is not None]
        out["summary"][mode] = {"n": len(ks), "meanK": sum(ks) / len(ks) if ks else None,
                                "minK": min(ks) if ks else None,
                                "maxK": max(ks) if ks else None}
    sc, sn = out["summary"]["classic"], out["summary"]["negation"]
    ratio = (sn["meanK"] / sc["meanK"]) if (sc["meanK"] and sn["meanK"]) else None
    out["summary"]["ratio_neg_classic"] = ratio
    out["summary"]["verdict"] = ("CONFIRMED (~0.55)" if ratio and ratio < 0.75
                                 else ("REFUTED (~1.0)" if ratio and ratio > 0.9 else "INCONCLUSIVE"))
    op = os.path.join(HERE, "PILOT1_NEGATION.json")
    json.dump(out, open(op, "w"), indent=1)
    print("ratio negation/classic = %s -> %s" % (ratio, out["summary"]["verdict"]))
    print("wrote", op)


if __name__ == "__main__":
    main()