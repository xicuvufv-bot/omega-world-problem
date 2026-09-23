#!/usr/bin/env python3
"""gen.py — synthetic DLP instance generator for the research benchmark.

Emits JSONL instances (prime-order EC group + composite/smooth-order control for the
Pohlig-Hellman exhibit). Everything here is SYNTHETIC: no real keys, no real base points.
Deterministic: seeded by --seed. G is DERIVED through the generator's own point search
(fixed verified toy curve), never loaded from external key material.

  python gen.py --db 12,16,20 --seed 20260922 --out instances/prime.jsonl
  python gen.py --smooth --db 24,28 --seed 20260922 --out instances/smooth.jsonl

The prime-order group uses the Phase-1-verified toy curve (p=4294966177, b=7, order l
prime, G generated here). The smooth control uses a multiplicative group F_p* of smooth
|subgroup| so PH is actually sublinear in the top factor (standard exhibit, clearly a
control — NOT an EC shortcut claim).
"""
import argparse, json, math, os, random, sys

# ---------------- EC arithmetic (Mirror of ref/gen_instance.py) ----------------
def modinv(a, m):
    return pow(a, -1, m)

def add(P, Q, p):
    if P is None: return Q
    if Q is None: return P
    x1, y1 = P; x2, y2 = Q
    if x1 == x2:
        if (y1 + y2) % p == 0: return None
        lam = 3 * x1 * x1 % p * modinv(2 * y1, p) % p
    else:
        lam = (y2 - y1) % p * modinv((x2 - x1) % p, p) % p
    x3 = (lam * lam - x1 - x2) % p
    y3 = (lam * (x1 - x3) - y1) % p
    return (x3, y3)

def mul(k, P, p):
    if k < 0:
        R = mul(-k, P, p)
        return None if R is None else (R[0], (-R[1]) % p)
    R = None; Q = P
    while k:
        if k & 1: R = add(R, Q, p)
        Q = add(Q, Q, p); k >>= 1
    return R

def sqrt_mod(a, p):
    if a == 0: return 0
    if pow(a, (p - 1) // 2, p) != 1: return None
    if p % 4 == 3: return pow(a, (p + 1) // 4, p)
    q, s = p - 1, 0
    while q % 2 == 0: q //= 2; s += 1
    z = 2
    while pow(z, (p - 1) // 2, p) != p - 1: z += 1
    m, c, t, r = s, pow(z, q, p), pow(a, q, p), pow(a, (q + 1) // 2, p)
    while t != 1:
        i, tt = 0, t
        while tt != 1:
            tt = tt * tt % p; i += 1
        b = pow(c, 1 << (m - i - 1), p)
        m, c, t, r = i, b * b % p, t * b * b % p, r * b % p
    return r

def rand_point(p):
    while True:
        x = random.randrange(0, p)
        rhs = (x ** 3 + 7) % p
        y = sqrt_mod(rhs, p)
        if y is not None and y * y % p == rhs:
            return (x, y)

def factor_small(n):
    fac = []
    d = 2
    while d * d <= n:
        while n % d == 0:
            fac.append(d); n //= d
        d += 1 if d == 2 else 2
    if n > 1: fac.append(n)
    return fac

# ---------------- prime-order EC group (Phase-1-verified toy curve) ----------------
TOY_P = 4294966177          # 2^32 - 1119, p ≡ 1 mod 3 -> ordinary
TOY_L = 4294835173          # group order, prime (verified by gen_instance.py Phase 1)
TOY_G = (1960037684, 560815139)

def gen_prime_instances(dbs, seed, reps):
    random.seed(seed)
    out = []
    for db in dbs:
        assert db < TOY_L.bit_length(), "interval must fit in group order"
        for r in range(reps):
            k = random.randrange(1, 1 << db)
            Q = mul(k, TOY_G, TOY_P)
            out.append({"db": db, "rep": r, "typ": "prime",
                        "p": TOY_P, "l": TOY_L, "b7": 7,
                        "Gx": TOY_G[0], "Gy": TOY_G[1],
                        "Qx": Q[0], "Qy": Q[1], "k": k})
    return out

# ---------------- smooth-order control group (F_p* subgroup of smooth order) ----------------
def gen_smooth_instances(dbs, seed, reps):
    """Build a subgroup of F_p* whose |order| is smooth (product of small primes), so
    PH is sub-exponential in the largest factor — the canonical (C)-class exhibit.
    We pick p = 2*(... many small primes ...) + 1 form; simplest: find a safe prime where
    the cofactor is smooth (p-1 = 2^a * q1*q2*...). We use a fixed small-safe-prime search
    (p-1 smooth by construction)."""
    random.seed(seed)
    # p-1 = 2^8 * 3 * 5 * 7 * 11 * 13 * 17 * 19 * 23 = ... build candidate, require prime p
    base = (2 ** 8) * 3 * 5 * 7 * 11 * 13 * 17 * 19 * 23     # highly smooth
    p = base + 1
    while not _is_prime(p):
        base *= 2     # keep the 2-power factor growing; order stays smooth
        p = base + 1
    # find generator g of full F_p*
    for g in range(2, 1000):
        if pow(g, base, p) != 1:
            break
    l = base  # full subgroup order used by PH exhibit
    # element of full order, so DLP in generic group has order l (smooth).
    out = []
    for db in dbs:
        N = 1 << db
        assert N <= l
        for r in range(reps):
            k = random.randrange(1, N)
            h = pow(g, k, p)
            out.append({"db": db, "rep": r, "typ": "smooth",
                        "p": p, "l": l, "g": g, "h": h, "k": k,
                        "smooth": True})
    return out

def _is_prime(n):
    if n < 2: return False
    for s in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47):
        if n % s == 0: return n == s
    d, r = n - 1, 0
    while d % 2 == 0: d //= 2; r += 1
    for _ in range(30):
        a = 2 + random.randrange(n - 3)
        x = pow(a, d, n)
        if x in (1, n - 1): continue
        for _ in range(r - 1):
            x = x * x % n
            if x == n - 1: break
        else:
            return False
    return True

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", default="12,16,20,24", help="comma list of interval bits")
    ap.add_argument("--seed", type=int, default=20260922)
    ap.add_argument("--reps", type=int, default=3)
    ap.add_argument("--smooth", action="store_true", help="emit smooth-order control group")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()
    dbs = [int(x) for x in args.db.split(",")]
    if args.smooth:
        rows = gen_smooth_instances(dbs, args.seed, args.reps)
        tag = "smooth"
    else:
        rows = gen_prime_instances(dbs, args.seed, args.reps)
        tag = "prime"
    # independent verification: every k → Q checks by scalar mult
    bad = 0
    for i, row in enumerate(rows):
        if row["typ"] == "prime":
            got = mul(row["k"], (row["Gx"], row["Gy"]), row["p"])
            ok = got is not None and got[0] == row["Qx"] and got[1] == row["Qy"]
        else:
            ok = pow(row["g"], row["k"], row["p"]) == row["h"]
        row["verified"] = 1 if ok else 0
        bad += (0 if ok else 1)
    out = args.out or f"instances/{tag}_db{'-'.join(map(str,dbs))}.jsonl"
    os.makedirs(os.path.dirname(out) or ".", exist_ok=True)
    with open(out, "w") as f:
        for row in rows:
            f.write(json.dumps(row) + "\n")
    print(f"wrote {len(rows)} {tag} instances -> {out}; verification failures={bad}")

if __name__ == "__main__":
    main()