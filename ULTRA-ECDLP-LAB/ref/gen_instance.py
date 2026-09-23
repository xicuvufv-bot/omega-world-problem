#!/usr/bin/env python3
"""gen_instance.py — find a prime p (~2^32, p=1 mod 3 for ordinary curve, convenient
2^32-c with small c for fast reduction) where #E(y^2=x^3+7) is prime (or has a very
large prime factor >= 2^32), then emit instance.hpp + DLP vectors.

Research toy instances only. NO real keys/wallets.
"""
import random, math

def modinv(a, m): return pow(a, -1, m)
def add(P, Q, p):
    if P is None: return Q
    if Q is None: return P
    x1,y1=P; x2,y2=Q
    if x1==x2:
        if (y1+y2)%p==0: return None
        l=3*x1*x1%p*modinv(2*y1,p)%p
    else:
        l=(y2-y1)%p*modinv((x2-x1)%p,p)%p
    x3=(l*l-x1-x2)%p; y3=(l*(x1-x3)-y1)%p
    return (x3,y3)
def mul(k,P,p):
    if k<0:
        R=mul(-k,P,p)
        if R is None: return None
        return (R[0],(-R[1])%p)
    R=None; Q=P
    while k:
        if k&1: R=add(R,Q,p)
        Q=add(Q,Q,p); k>>=1
    return R
def sqrt_mod(a, p):
    if a==0: return 0
    if pow(a,(p-1)//2,p)!=1: return None     # non-residue
    if p%4==3: return pow(a,(p+1)//4,p)
    # Tonelli-Shanks
    q,s=p-1,0
    while q%2==0: q//=2; s+=1
    z=2
    while pow(z,(p-1)//2,p)!=p-1: z+=1
    m,c,t,r=s,pow(z,q,p),pow(a,q,p),pow(a,(q+1)//2,p)
    while t!=1:
        i,tt=0,t
        while tt!=1: tt=tt*tt%p; i+=1
        b=pow(c,1<<(m-i-1),p)
        m,c,t,r=i,b*b%p,t*b*b%p,r*b%p
    return r
def is_prime(n):
    if n<2: return False
    for s in (2,3,5,7,11,13,17,19,23,29,31,37,41,43,47):
        if n%s==0: return n==s
    d,r=n-1,0
    while d%2==0: d//=2; r+=1
    for _ in range(30):
        a=2+random.randrange(n-3); x=pow(a,d,n)
        if x in (1,n-1): continue
        for _ in range(r-1):
            x=x*x%n
            if x==n-1: break
        else: return False
    return True

def next_prime(n):
    while not is_prime(n): n+=1
    return n

def group_order(p):
    # BSGS over Hasse trace; returns #E
    B=math.isqrt(4*p)+1
    while True:
        x=random.randrange(0,p); rhs=(x**3+7)%p
        y=sqrt_mod(rhs,p)
        if y is None: continue
        P=(x,y)
        Q=mul(p+1,P,p)
        m=math.isqrt(2*B)+1
        baby={}; cur=None
        for a in range(m):
            baby.setdefault(cur,a)
            cur=P if cur is None else add(cur,P,p)
        step=mul(m,P,p); mB=mul(B,P,p)
        if mB is None: continue
        gbase=(mB[0],(-mB[1])%p)
        giant=add(Q,gbase,p)
        cands=[]
        for b in range(m+1):
            if giant in baby:
                t=B-(b*m-baby[giant])
                N=p+1-t
                if 0 < N < 2*p: cands.append(N)
            giant=add(giant,step,p)
        # verify each candidate against fresh points
        for N in cands:
            ok=True
            for _ in range(2):
                x2=random.randrange(0,p); rhs2=(x2**3+7)%p; y2=sqrt_mod(rhs2,p)
                if y2 is None: ok=False; break
                if mul(N,(x2,y2),p) is not None: ok=False; break
            if ok: return N
        # no candidate passed -> try a new point (may have low order)

def factor_small(n):
    """Trial-divide to sqrt(n) (n~2^32 -> sqrt~2^16, fast). Returns sorted prime factors with multiplicity."""
    fac=[]
    d=2
    while d*d<=n:
        while n%d==0: fac.append(d); n//=d
        d+=1 if d==2 else 2
    if n>1: fac.append(n)
    return fac

def rand_point(p):
    while True:
        x=random.randrange(0,p); rhs=(x**3+7)%p; y=sqrt_mod(rhs,p)
        if y is not None and y*y%p==rhs: return (x,y)

def main():
    random.seed(20260922)
    # search primes p = 2^32 - c with c ≡ 0 mod 3 (so p = 1 mod 3 -> ordinary), small c,
    # and #E prime (or largest prime factor >= 2^32, which essentially requires #E prime).
    base = 1 << 32
    found = None
    c = 3
    tries = 0
    while c < 4000 and found is None:
        p = base - c
        if is_prime(p) and p % 3 == 1:
            tries += 1
            N = group_order(p)
            if is_prime(N):
                found = (p, c, N, 'prime')
                break
            # else check largest prime factor of N
            fac = factor_small(N)
            l = fac[-1]
            if l >= (1 << 32):
                found = (p, c, N, f'largest_factor_{l}')
                break
            # else record but keep searching for better (prime) — but accept large factor >= 2^31 as fallback
        c += 3
    if found is None:
        # fallback: accept largest prime factor >= 2^31
        c = 3
        best = None
        while c < 4000:
            p = base - c
            if is_prime(p) and p % 3 == 1:
                N = group_order(p)
                fac = factor_small(N)
                l = fac[-1]
                if best is None or l > best[3]:
                    best = (p, c, N, l)
                if l >= (1 << 31):
                    break
            c += 3
        found = best
        if found is None:
            print("FAILED to find acceptable curve"); return
        p, c, N, l = found
        kind = f'largest_factor_{l}'
    else:
        p, c, N, kind = found
        l = N if kind == 'prime' else int(kind.split('_')[-1])

    print(f"CHOSEN p = {p} (2^32 - {c}), p%3={p%3}")
    print(f"  #E = {N} (prime={is_prime(N)}), largest prime factor l = {l}")

    # find generator of order l
    for _ in range(5000):
        P = rand_point(p)
        G = mul(N // l, P, p)
        if G is not None and mul(l, G, p) is None:
            break
    else:
        print("no generator"); return
    print(f"  generator G = {G}, order l = {l}")

    # DLP test vectors for k up to 2^d, d <= log2(l)
    lines_hpp = ["// instance.hpp — generated by ref/gen_instance.py (deterministic). NO REAL KEYS.", "#pragma once",
                 "#include <cstdint>"]
    lines_vec = []
    lbits = l.bit_length()
    print(f"  l has {lbits} bits -> can scale problems up to 2^{lbits-1} (interval width)")
    for iv in (16, 20, 24, 28, 32):
        if iv >= lbits:  # need k < l and interval 2^iv fits
            ks = random.randrange(1, l)
            Q = mul(ks, G, p)
            print(f"  DLP lvl{iv} (clamped): k={ks} Q={Q}")
            lines_vec.append(f"{iv} {ks} {Q[0]} {Q[1]}")
            continue
        ks = random.randrange(1, 1 << iv)
        Q = mul(ks, G, p)
        print(f"  DLP lvl{iv}: k={ks} Q={Q}")
        lines_vec.append(f"{iv} {ks} {Q[0]} {Q[1]}")

    lines_hpp.append(f"constexpr uint32_t TOY_P = {p}u;")
    lines_hpp.append(f"constexpr uint32_t TOY_Gx = {G[0]}u;")
    lines_hpp.append(f"constexpr uint32_t TOY_Gy = {G[1]}u;")
    lines_hpp.append(f"constexpr uint64_t TOY_L  = {l}ull;")
    with open("instance.hpp","w") as f: f.write("\n".join(lines_hpp)+"\n")
    with open("dlp_vectors.txt","w") as f: f.write("\n".join(lines_vec)+"\n")
    print("wrote instance.hpp + dlp_vectors.txt")

if __name__=="__main__":
    main()