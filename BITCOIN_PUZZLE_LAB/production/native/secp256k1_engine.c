/*
 * secp256k1_engine.c -- Fused secp256k1 key-scan + hash160 engine
 *
 * Pipeline:  scalar generation  -->  compressed pubkey (Jacobian)
 *          -->  RIPEMD160(SHA256(pubkey))  -->  optional target match
 *
 * Design choices
 *   Portable 256-bit arithmetic on native u64 limbs (no __int128 on MSVC
 *   x64 required, though __uint128_t is used on GCC/Clang for speed).
 *   One Fermat inversion per BATCH via Montgomery's prefix-product trick,
 *   replacing one inversion per key.  The hot loop (incremental +G
 *   mixed-add, hash160, compare) performs zero heap allocation and touches
 *   no global state, so it is fully thread-safe when each thread owns its
 *   own context.
 *
 * Build
 *   MSVC  x64:  call vcvars64.bat first, then
 *               cl /O2 /LD /Febin\secp256k1_engine.dll secp256k1_engine.c
 *   GCC / Clang: gcc -O3 -shared -fPIC -o bin/secp256k1_engine.so secp256k1_engine.c
 */

/* ──────────────────────────── portability ──────────────────────────── */

#ifdef _MSC_VER
#  pragma comment(lib, "advapi32.lib")
#  include <intrin.h>
#  define MUL64(a,b,hi,lo) do { (lo) = _umul128((a),(b),&(hi)); } while(0)
#  define EXPORT __declspec(dllexport)
#  define ALIGN64(n) __declspec(align(n))
#else
   typedef unsigned __int128 u128;
#  define MUL64(a,b,hi,lo) do { u128 _p=(u128)(a)*(u128)(b); \
      (hi)=(uint64_t)(_p>>64); (lo)=(uint64_t)(_p); } while(0)
#  define EXPORT __attribute__((visibility("default")))
#  define ALIGN64(n) __attribute__((aligned(n)))
#endif

#include <string.h>
#include <stdint.h>
#include <stdlib.h>
#include <stdio.h>

typedef uint8_t  u8;
typedef uint32_t u32;
typedef uint64_t u64;

/* ─────────────────────────── field constants ───────────────────────── */

#define C 0x00000001000003D1ULL          /* 2^256 - p                     */

typedef struct { u64 w[4]; } fe;          /* 256-bit field element, LE     */

static const fe FIELD_P  = {{ 0xFFFFFFFEFFFFFC2FULL, 0xFFFFFFFFFFFFFFFFULL,
                              0xFFFFFFFFFFFFFFFFULL, 0xFFFFFFFFFFFFFFFFULL }};
static const fe FIELD_P2 = {{ 0xFFFFFFFEFFFFFC2DULL, 0xFFFFFFFFFFFFFFFFULL,
                              0xFFFFFFFFFFFFFFFFULL, 0xFFFFFFFFFFFFFFFFULL }};/* p-2 */
static const fe GROUP_N  = {{ 0xBFD25E8CD0364141ULL, 0xBAAEDCE6AF48A03BULL,
                              0xFFFFFFFFFFFFFFFEULL, 0xFFFFFFFFFFFFFFFFULL }};
static const fe FE_ONE   = {{ 1ULL, 0, 0, 0 }};
static const fe FE_ZERO  = {{ 0, 0, 0, 0 }};

/* generator coordinates as 4-limb LE arrays (not fe -- same layout)     */
static const u64 GX_W[4] = { 0x59F2815B16F81798ULL, 0x029BFCDB2DCE28D9ULL,
                              0x55A06295CE870B07ULL, 0x79BE667EF9DCBBACULL };
static const u64 GY_W[4] = { 0x9C47D08FFB10D4B8ULL, 0xFD17B448A6855419ULL,
                              0x5DA4FBFC0E1108A8ULL, 0x483ADA7726A3C465ULL };

static const u64 C_LIMB[4] = { C, 0, 0, 0 };  /* constant C as a 4-limb value */

/* ───────────────────────── byte I/O (big-endian) ──────────────────── */

static u64 read_be64(const u8 *p) {
    return ((u64)p[0]<<56)|((u64)p[1]<<48)|((u64)p[2]<<40)|((u64)p[3]<<32)|
           ((u64)p[4]<<24)|((u64)p[5]<<16)|((u64)p[6]<<8) | (u64)p[7];
}
static void write_be64(u8 *p, u64 v) {
    p[0]=(u8)(v>>56); p[1]=(u8)(v>>48); p[2]=(u8)(v>>40); p[3]=(u8)(v>>32);
    p[4]=(u8)(v>>24); p[5]=(u8)(v>>16); p[6]=(u8)(v>>8);  p[7]=(u8)(v);
}
static void be32_to_fe(fe *o, const u8 *b) {
    o->w[3]=read_be64(b);    o->w[2]=read_be64(b+8);
    o->w[1]=read_be64(b+16); o->w[0]=read_be64(b+24);
}
static void fe_to_be32(u8 *b, const fe *a) {
    write_be64(b,     a->w[3]); write_be64(b+8,  a->w[2]);
    write_be64(b+16,  a->w[1]); write_be64(b+24, a->w[0]);
}

/* ────────────── limb-level add / subtract / compare ────────────────── */

/* r = a + b;  *carry = 0 or 1.  a,b,r may alias. */
static void add_limbs(u64 r[4], const u64 a[4], const u64 b[4], u64 *carry) {
    int i; u64 c = 0;
    for (i = 0; i < 4; i++) {
        u64 t = a[i] + c;  c = (t < a[i]);
        u64 s = t + b[i];  c += (s < t);
        r[i] = s;
    }
    *carry = c;
}

/* r = a - b;  *borrow = 0 or 1.  a,b,r may alias. */
static void sub_limbs(u64 r[4], const u64 a[4], const u64 b[4], u64 *borrow) {
    int i; u64 br = 0;
    for (i = 0; i < 4; i++) {
        u64 t = a[i] - br;  br = (a[i] < br);
        u64 s = t - b[i];   br += (t < b[i]);
        r[i] = s;
    }
    *borrow = br;
}

/* returns -1/0/+1  (a vs b) */
static int cmp_fe(const fe *a, const fe *b) {
    int i;
    for (i = 3; i >= 0; i--) {
        if (a->w[i] > b->w[i]) return  1;
        if (a->w[i] < b->w[i]) return -1;
    }
    return 0;
}

static int fe_is_zero(const fe *a) {
    return (a->w[0] | a->w[1] | a->w[2] | a->w[3]) == 0;
}

/* ──────────────────── modular arithmetic mod p ─────────────────────── */

static void addmod(fe *r, const fe *a, const fe *b) {
    u64 carry, c2;
    add_limbs(r->w, a->w, b->w, &carry);
    /* fold 2^256 ≡ C */
    while (carry) { add_limbs(r->w, r->w, C_LIMB, &c2); carry = c2; }
    if (cmp_fe(r, &FIELD_P) >= 0) { u64 br; sub_limbs(r->w, r->w, FIELD_P.w, &br); }
}

static void submod(fe *r, const fe *a, const fe *b) {
    if (cmp_fe(a, b) >= 0) {
        u64 br; sub_limbs(r->w, a->w, b->w, &br);
    } else {
        fe pmb; u64 br, carry;
        sub_limbs(pmb.w, FIELD_P.w, b->w, &br);
        add_limbs(r->w, a->w, pmb.w, &carry);
    }
}

/* ──────────────── 512-bit multiply  +  C-fold  ─────────────────────── */

/* Schoolbook: r[0..7] = a[0..3] * b[0..3]  (both < 2^256).              *
 * Uses per-column 128-bit accumulation via overflow counting.             */
static void mul_full(u64 r[8], const u64 a[4], const u64 b[4]) {
    u64 hiP[16], loP[16];
    int i, j, k;
    u64 carry;

    for (i = 0; i < 4; i++)
        for (j = 0; j < 4; j++)
            MUL64(a[j], b[i], hiP[j*4+i], loP[j*4+i]);

    carry = 0;
    for (k = 0; k < 8; k++) {
        u64 lo = 0, hi = 0, s, c2;
        /* lo-contributions: products with  index j + bi == k */
        for (j = 0; j < 4; j++) { int bi=k-j;
            if (bi>=0 && bi<4) { u64 v=loP[j*4+bi]; lo+=v; hi+=(lo<v); } }
        /* hi-contributions: products with index j + bi == k-1 */
        for (j = 0; j < 4; j++) { int bi=k-1-j;
            if (bi>=0 && bi<4) { u64 v=hiP[j*4+bi]; lo+=v; hi+=(lo<v); } }
        s  = lo + carry; c2 = (s < lo);
        r[k] = s;
        carry = hi + c2;
    }
}

/* r[0..4] = a[0..3] * C   (C < 2^33, result < 5 limbs).                */
static void mul_C5(u64 r[5], const u64 a[4]) {
    int i; u64 carry = 0;
    for (i = 0; i < 4; i++) {
        u64 hi, lo, s, c2;
        MUL64(a[i], C, hi, lo);
        s = lo + carry; c2 = (s < carry);
        r[i] = s;
        carry = hi + c2;
    }
    r[4] = carry;
}

/* r = a * b  (mod p).                                                    */
static void fmul(fe *r, const fe *a, const fe *b) {
    u64 w8[8], u5[5], carry;
    fe lo_fe;
    u64 fold[4], c2;

    mul_full(w8, a->w, b->w);
    mul_C5(u5, w8 + 4);                          /* hi_half * C           */

    memcpy(lo_fe.w, w8, 32);
    add_limbs(r->w, lo_fe.w, u5, &carry);        /* lo + u[0..3]          */

    if (u5[4] + carry) {
        u64 th, tl, tc;
        MUL64(u5[4] + carry, C, th, tl);
        fold[0] = tl; fold[1] = th; fold[2] = 0; fold[3] = 0;
        add_limbs(r->w, r->w, fold, &c2);
        if (c2) { u64 c3; add_limbs(r->w, r->w, C_LIMB, &c3); }
    }

    /* normalize: r < 2p  -->  at most 2 subtracts */
    { int g = 0;
      while (cmp_fe(r, &FIELD_P) >= 0 && g++ < 3) {
          u64 br; sub_limbs(r->w, r->w, FIELD_P.w, &br); } }
}

static void fsqr(fe *r, const fe *a) { fmul(r, a, a); }

/* ──────────────── Fermat exponentiation:  base^exp  ────────────────── */

/* Left-to-right binary method.  Processes all 256 bits unconditionally.   *
 * The skipped leading zeros cost only squarings (no multiplications),      *
 * so the overhead vs a tuned MSB-scan is negligible.                       */
static void fpow(fe *r, const fe *base, const fe *exp) {
    int i, b;
    *r = FE_ONE;
    for (i = 3; i >= 0; i--) {
        u64 e = exp->w[i];
        for (b = 63; b >= 0; b--) {
            fmul(r, r, r);
            if ((e >> b) & 1) fmul(r, r, base);
        }
    }
}

/* ──────────────── Jacobian projective  (a = 0) ─────────────────────── */

typedef struct { fe x, y, z; } jac;   /* z == 0  -->  point at infinity  */

static int  jac_is_inf(const jac *p) { return fe_is_zero(&p->z); }

/* Doubling  (matches algorithms/curve.py jac_double exactly).             */
static void jac_dbl(jac *r, const jac *p) {
    fe x2, y2, y4, s, d, e, t, t2, y4x8;
    if (jac_is_inf(p)) { *r = *p; return; }

    fsqr(&x2, &p->x);
    fsqr(&y2, &p->y);
    fsqr(&y4, &y2);

    /* s = (x + y2)^2 - x2 - y4 */
    addmod(&t, &p->x, &y2);
    fsqr(&s, &t);
    submod(&s, &s, &x2);
    submod(&s, &s, &y4);

    addmod(&d, &s, &s);                        /* d = 2*s                */
    addmod(&e, &x2, &x2); addmod(&e, &e, &x2); /* e = 3*x2             */

    /* xn = e^2 - 2*d */
    fsqr(&t, &e);
    submod(&t, &t, &d);
    submod(&t, &t, &d);

    /* yn = e*(d - xn) - 8*y4 */
    submod(&t2, &d, &t);
    fmul(&t2, &e, &t2);
    addmod(&y4x8, &y4, &y4); addmod(&y4x8, &y4x8, &y4x8);
    addmod(&y4x8, &y4x8, &y4x8);               /* y4x8 = 8*y4           */
    submod(&t2, &t2, &y4x8);

    /* zn = 2*y*z */
    fmul(&r->z, &p->y, &p->z);
    addmod(&r->z, &r->z, &r->z);

    r->x = t;  r->y = t2;
}

/* Mixed addition: Jacobian + affine.  Matches algorithms/curve.py.        */
static void jac_madd(jac *r, const jac *p, const u64 ax[4], const u64 ay[4]) {
    fe z2, u_fe, s_fe, h, h2, h3, rn, v, xn, vn, tmp;
    fe axf, ayf;

    if (jac_is_inf(p)) {
        memcpy(r->x.w, ax, 32);
        memcpy(r->y.w, ay, 32);
        r->z = FE_ONE;
        return;
    }

    memcpy(axf.w, ax, 32);
    memcpy(ayf.w, ay, 32);

    fsqr(&z2, &p->z);                           /* z2 = z*z             */
    fmul(&u_fe, &axf, &z2);                     /* u  = ax*z2           */
    fmul(&s_fe, &p->z, &z2);                    /*    = z*z2             */
    fmul(&s_fe, &ayf, &s_fe);                   /* s  = ay*z*z2         */

    if (cmp_fe(&u_fe, &p->x) == 0) {
        if (cmp_fe(&s_fe, &p->y) == 0) { jac_dbl(r, p); return; }
        r->z = FE_ZERO;                          /* point at infinity    */
        return;
    }

    submod(&h,   &u_fe, &p->x);                 /* h  = u - x           */
    fsqr (&h2,  &h);
    fmul (&h3,  &h2, &h);                       /* h3 = h^3             */
    submod(&rn, &s_fe, &p->y);                  /* rn = s - y  (r)      */
    fmul (&v,   &p->x, &h2);                    /* v  = x*h2            */

    /* xn = r^2 - 2v - h3 */
    fsqr (&xn, &rn);
    submod(&xn, &xn, &v);
    submod(&xn, &xn, &v);
    submod(&xn, &xn, &h3);

    /* yn = r*(v - xn) - y*h3 */
    submod(&vn, &v, &xn);
    fmul (&vn, &rn, &vn);
    fmul (&tmp, &p->y, &h3);
    submod(&vn, &vn, &tmp);

    /* zn = z*h */
    fmul(&r->z, &p->z, &h);

    r->x = xn;  r->y = vn;
}

/* ───────────────── affine conversion + table precompute ────────────── */

static void to_affine(fe *ax, fe *ay, const jac *p) {
    fe zi, zi2, zi3;
    fpow(&zi,  &p->z, &FIELD_P2);               /* z^-1 = z^(p-2)      */
    fsqr (&zi2, &zi);
    fmul (&zi3, &zi2, &zi);
    fmul (ax, &p->x, &zi2);
    fmul (ay, &p->y, &zi3);
}

/* ──────────────── 4-bit-window scalar multiply ─────────────────────── */

static void scalar_mult(jac *r, const u64 k[4],
                        const fe Wx[15], const fe Wy[15]) {
    u8 nib[64];
    int i, j, started = 0;

    /* extract nibbles: nib[0] = LSB nibble of k */
    for (i = 0; i < 4; i++)
        for (j = 0; j < 16; j++)
            nib[i*16+j] = (u8)((k[i] >> (j*4)) & 0xF);

    r->z = FE_ZERO;

    /* MSB first: nib[63] .. nib[0] */
    for (i = 63; i >= 0; i--) {
        int v = nib[i];
        if (!started && v == 0) continue;
        if (started) {              /* double x4 */
            jac t;
            jac_dbl(&t, r); *r = t;
            jac_dbl(&t, r); *r = t;
            jac_dbl(&t, r); *r = t;
            jac_dbl(&t, r); *r = t;
        }
        if (v != 0) {
            jac_madd(r, r, Wx[v-1].w, Wy[v-1].w);
            started = 1;
        }
    }
    if (!started) r->z = FE_ZERO;   /* k == 0 */
}

/* ══════════════════════════════════════════════════════════════════════
 *  SHA-256   (verbatim from hash160.c -- proven, tested)
 * ══════════════════════════════════════════════════════════════════════ */

static const u32 K256[64]={
  0x428a2f98,0x71374491,0xb5c0fbcf,0xe9b5dba5,0x3956c25b,0x59f111f1,0x923f82a4,0xab1c5ed5,
  0xd807aa98,0x12835b01,0x243185be,0x550c7dc3,0x72be5d74,0x80deb1fe,0x9bdc06a7,0xc19bf174,
  0xe49b69c1,0xefbe4786,0x0fc19dc6,0x240ca1cc,0x2de92c6f,0x4a7484aa,0x5cb0a9dc,0x76f988da,
  0x983e5152,0xa831c66d,0xb00327c8,0xbf597fc7,0xc6e00bf3,0xd5a79147,0x06ca6351,0x14292967,
  0x27b70a85,0x2e1b2138,0x4d2c6dfc,0x53380d13,0x650a7354,0x766a0abb,0x81c2c92e,0x92722c85,
  0xa2bfe8a1,0xa81a664b,0xc24b8b70,0xc76c51a3,0xd192e819,0xd6990624,0xf40e3585,0x106aa070,
  0x19a4c116,0x1e376c08,0x2748774c,0x34b0bcb5,0x391c0cb3,0x4ed8aa4a,0x5b9cca4f,0x682e6ff3,
  0x748f82ee,0x78a5636f,0x84c87814,0x8cc70208,0x90befffa,0xa4506ceb,0xbef9a3f7,0xc67178f2};

#define RR(x,n) (((x)>>(n))|((x)<<(32-(n))))
#define CH(x,y,z) (((x)&(y))^(~(x)&(z)))
#define MAJ(x,y,z) (((x)&(y))^((x)&(z))^((y)&(z)))
#define EP0(x) (RR(x,2)^RR(x,13)^RR(x,22))
#define EP1(x) (RR(x,6)^RR(x,11)^RR(x,25))
#define SIG0(x) (RR(x,7)^RR(x,18)^((x)>>3))
#define SIG1(x) (RR(x,17)^RR(x,19)^((x)>>10))

static void sha256_transform(u32 state[8], const u8 block[64]) {
    u32 W[64], a,b,c,d,e,f,g,h, t1, t2;
    int i;
    for (i=0;i<16;i++)
        W[i]=((u32)block[i*4]<<24)|((u32)block[i*4+1]<<16)|
              ((u32)block[i*4+2]<<8)|(u32)block[i*4+3];
    for (i=16;i<64;i++)
        W[i]=SIG1(W[i-2])+W[i-7]+SIG0(W[i-15])+W[i-16];
    a=state[0];b=state[1];c=state[2];d=state[3];
    e=state[4];f=state[5];g=state[6];h=state[7];
    for (i=0;i<64;i++){
        t1=h+EP1(e)+CH(e,f,g)+K256[i]+W[i];
        t2=EP0(a)+MAJ(a,b,c);
        h=g;g=f;f=e;e=d+t1;d=c;c=b;b=a;a=t1+t2;
    }
    state[0]+=a;state[1]+=b;state[2]+=c;state[3]+=d;
    state[4]+=e;state[5]+=f;state[6]+=g;state[7]+=h;
}

static void sha256(const u8 *in, size_t len, u8 out[32]) {
    u32 state[8]={0x6a09e667,0xbb67ae85,0x3c6ef372,0xa54ff53a,
                   0x510e527f,0x9b05688c,0x1f83d9ab,0x5be0cd19};
    u8 buf[64];
    size_t i, j, nb = len / 64;
    for (i=0;i<nb;i++) sha256_transform(state, in+i*64);
    j = len % 64;
    memset(buf, 0, 64);
    memcpy(buf, in+nb*64, j);
    buf[j] = 0x80;
    if (j > 55) { sha256_transform(state, buf); memset(buf,0,64); }
    { u64 bits = (u64)len * 8;
      buf[56]=(u8)(bits>>56); buf[57]=(u8)(bits>>48);
      buf[58]=(u8)(bits>>40); buf[59]=(u8)(bits>>32);
      buf[60]=(u8)(bits>>24); buf[61]=(u8)(bits>>16);
      buf[62]=(u8)(bits>>8);  buf[63]=(u8)(bits); }
    sha256_transform(state, buf);
    for (i=0;i<8;i++){
        out[i*4]  =(u8)(state[i]>>24); out[i*4+1]=(u8)(state[i]>>16);
        out[i*4+2]=(u8)(state[i]>>8);  out[i*4+3]=(u8)(state[i]);
    }
}

/* ────────────────────────── RIPEMD-160 ─────────────────────────────── */

static const u32 KL[80]={
    0x00000000,0x5a827999,0x6ed9eba1,0x8f1bbcdc,0xa953fd4e,
    0x50a28be6,0x5c4dd124,0x6d703ef3,0x7a6d76e9,0x00000000};
static const u32 KR[80]={
    0x50a28be6,0x5c4dd124,0x6d703ef3,0x7a6d76e9,0x00000000,
    0x5a827999,0x6ed9eba1,0x8f1bbcdc,0xa953fd4e,0x00000000};
static const int RL[80]={
    0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,
    7,4,13,1,10,6,15,3,12,0,9,5,2,14,11,8,
    3,10,14,4,9,15,8,1,2,7,0,6,13,11,5,12,
    1,9,11,10,0,8,12,4,13,3,7,15,14,5,6,2,
    4,0,5,9,7,12,2,10,14,1,3,8,11,6,15,13};
static const int RR2[80]={
    5,14,7,0,9,2,11,4,13,6,15,8,1,10,3,12,
    6,11,3,7,0,13,5,10,14,15,8,12,4,9,1,2,
    15,5,1,3,7,14,6,9,11,8,12,2,10,0,4,13,
    8,6,4,1,3,11,15,0,5,12,2,13,9,7,10,14,
    12,15,10,4,1,5,8,7,6,2,13,14,0,3,9,11};
static const int SL[80]={
    11,14,15,12,5,8,7,9,11,13,14,15,6,7,9,8,
    7,6,8,13,11,9,7,15,7,12,15,9,11,7,13,12,
    11,13,6,7,14,9,13,15,14,8,13,6,5,12,7,5,
    11,12,14,15,14,15,9,8,9,14,5,6,8,6,5,12,
    9,15,5,11,6,8,13,12,5,12,13,14,11,8,5,6};
static const int SR2[80]={
    8,9,9,11,13,15,15,5,7,7,8,11,14,14,12,6,
    9,13,15,7,12,8,9,11,7,7,12,7,6,15,13,11,
    9,7,15,11,8,6,6,14,12,13,5,14,13,13,7,5,
    15,5,8,11,14,14,6,14,6,9,12,9,12,5,15,8,
    8,5,12,9,12,5,14,6,8,13,6,5,15,13,11,11};

#define RL32(x,n) (((x)<<(n))|((x)>>(32-(n))))

static void ripemd160_transform(u32 state[5], const u8 block[64]) {
    u32 al=state[0],bl=state[1],cl=state[2],dl=state[3],el=state[4];
    u32 ar=state[0],br=state[1],cr=state[2],dr=state[3],er=state[4];
    u32 X[16], t;
    int i;
    for (i=0;i<16;i++)
        X[i]=((u32)block[i*4])|((u32)block[i*4+1]<<8)|
             ((u32)block[i*4+2]<<16)|((u32)block[i*4+3]<<24);
    /* (the loop below is the same as hash160.c; included verbatim) */
    for (i=0;i<80;i++){
        u32 fl,fr,kl,kr,wl,wr;
        if      (i<16) fl=bl^cl^dl;
        else if (i<32) fl=(bl&cl)|(~bl&dl);
        else if (i<48) fl=(bl|~cl)^dl;
        else if (i<64) fl=(bl&dl)|(cl&~dl);
        else           fl=bl^(cl|~dl);

        if      (i<16) fr=br^(cr|~dr);
        else if (i<32) fr=(br&dr)|(cr&~dr);
        else if (i<48) fr=(br|~cr)^dr;
        else if (i<64) fr=(br&cr)|(~br&dr);
        else           fr=br^cr^dr;

        if      (i<16) kl=0x00000000;
        else if (i<32) kl=0x5a827999;
        else if (i<48) kl=0x6ed9eba1;
        else if (i<64) kl=0x8f1bbcdc;
        else           kl=0xa953fd4e;

        if      (i<16) kr=0x50a28be6;
        else if (i<32) kr=0x5c4dd124;
        else if (i<48) kr=0x6d703ef3;
        else if (i<64) kr=0x7a6d76e9;
        else           kr=0x00000000;

        wl=X[RL[i]]; wr=X[RR2[i]];

        t=al+fl+wl+kl; t=RL32(t,SL[i])+el;
        al=el;el=dl;dl=RL32(cl,10);cl=bl;bl=t;

        t=ar+fr+wr+kr; t=RL32(t,SR2[i])+er;
        ar=er;er=dr;dr=RL32(cr,10);cr=br;br=t;
    }
    t=state[1]+cl+dr; state[1]=state[2]+dl+er;
    state[2]=state[3]+el+ar; state[3]=state[4]+al+br;
    state[4]=state[0]+bl+cr; state[0]=t;
}

static void ripemd160(const u8 *in, size_t len, u8 out[20]) {
    u32 state[5]={0x67452301,0xefcdab89,0x98badcfe,0x10325476,0xc3d2e1f0};
    u8 buf[64];
    size_t i, j, n = len / 64;
    for (i=0;i<n;i++) ripemd160_transform(state, in+i*64);
    j = len % 64;
    memset(buf, 0, 64);
    memcpy(buf, in+n*64, j);
    buf[j] = 0x80;
    if (j > 55) { ripemd160_transform(state, buf); memset(buf,0,64); }
    { u64 bits = (u64)len * 8;
      buf[56]=(u8)bits; buf[57]=(u8)(bits>>8);
      buf[58]=(u8)(bits>>16); buf[59]=(u8)(bits>>24);
      buf[60]=(u8)(bits>>32); buf[61]=(u8)(bits>>40);
      buf[62]=(u8)(bits>>48); buf[63]=(u8)(bits>>56); }
    ripemd160_transform(state, buf);
    for (i=0;i<5;i++){
        out[i*4]  =(u8)(state[i]);     out[i*4+1]=(u8)(state[i]>>8);
        out[i*4+2]=(u8)(state[i]>>16); out[i*4+3]=(u8)(state[i]>>24);
    }
}

/* hash160 = RIPEMD160(SHA256(data)) */
static void hash160_raw(const u8 *in, size_t len, u8 out[20]) {
    u8 tmp[32];
    sha256(in, len, tmp);
    ripemd160(tmp, 32, out);
}

/* ──────────────────────── context structure ────────────────────────── */

typedef struct {
    fe     key;                         /* current scalar (as fe; < N < p) */
    jac    pt;                          /* current point  key*G            */
    fe     Wx[15], Wy[15];             /* affine window: (i+1)*G, i=0..14 */
    int    max_batch;
    /* target matching */
    u8     targets[1280];               /* up to 64 x 20-byte hash160     */
    int    ntargets;
    /* batch scratch (single allocation) */
    u8    *batch_mem;
    fe    *bufX, *bufY, *bufZ;
    fe    *prefix, *invz;
    /* hit bookkeeping */
    int    last_hit_idx;
    u8     last_hit_key[32];
} s256_ctx;

static void _precompute_window(s256_ctx *ctx) {
    int i;
    jac cur;
    cur.z = FE_ZERO;  /* start at infinity */
    for (i = 0; i < 15; i++) {
        jac_madd(&cur, &cur, GX_W, GY_W);     /* (i+1)*G               */
        to_affine(&ctx->Wx[i], &ctx->Wy[i], &cur);
    }
}

/* ───────────────────── public C API ────────────────────────────────── */

EXPORT void *s256_ctx_new(int max_batch) {
    s256_ctx *ctx;
    u8 *mem;
    size_t offX, offY, offZ, offP, offI, total;
    if (max_batch < 1 || max_batch > 65536) return NULL;
    ctx = (s256_ctx *)calloc(1, sizeof(s256_ctx));
    if (!ctx) return NULL;
    ctx->max_batch = max_batch;
    ctx->ntargets  = 0;

    /* single contiguous allocation for all batch arrays                     *
     *  X (max*32) | Y | Z | prefix (max*32) | invz                         */
    total = (size_t)max_batch * 32 * 5;
    mem = (u8 *)calloc(1, total);
    if (!mem) { free(ctx); return NULL; }
    ctx->batch_mem = mem;
    offX = 0;
    offY = (size_t)max_batch * 32;
    offZ = (size_t)max_batch * 64;
    offP = (size_t)max_batch * 96;
    offI = (size_t)max_batch * 128;
    ctx->bufX   = (fe *)(mem + offX);
    ctx->bufY   = (fe *)(mem + offY);
    ctx->bufZ   = (fe *)(mem + offZ);
    ctx->prefix = (fe *)(mem + offP);
    ctx->invz   = (fe *)(mem + offI);

    _precompute_window(ctx);

    /* start at key = 1 */
    ctx->key = FE_ONE;
    memcpy(ctx->pt.x.w, GX_W, 32);
    memcpy(ctx->pt.y.w, GY_W, 32);
    ctx->pt.z = FE_ONE;

    return ctx;
}

EXPORT void s256_ctx_free(void *p) {
    s256_ctx *ctx = (s256_ctx *)p;
    if (!ctx) return;
    free(ctx->batch_mem);
    free(ctx);
}

EXPORT int s256_set_targets(void *p, const u8 *targets20, int n) {
    s256_ctx *ctx = (s256_ctx *)p;
    if (!ctx) return -1;
    if (n < 0) n = 0;
    if (n > 64) n = 64;
    ctx->ntargets = n;
    if (n > 0 && targets20)
        memcpy(ctx->targets, targets20, (size_t)n * 20);
    return 0;
}

EXPORT int s256_seek(void *p, const u8 key32[32]) {
    s256_ctx *ctx = (s256_ctx *)p;
    fe kf;
    if (!ctx || !key32) return -1;
    be32_to_fe(&kf, key32);
    /* reduce mod N (at most once since key < 2^256 < 2*N) */
    if (cmp_fe(&kf, &GROUP_N) >= 0) {
        u64 br; sub_limbs(kf.w, kf.w, GROUP_N.w, &br);
    }
    ctx->key = kf;
    if (fe_is_zero(&kf)) {
        ctx->pt.z = FE_ZERO;
    } else {
        scalar_mult(&ctx->pt, kf.w, ctx->Wx, ctx->Wy);
    }
    return 0;
}

EXPORT void s256_get_key(void *p, u8 out32[32]) {
    s256_ctx *ctx = (s256_ctx *)p;
    if (!ctx || !out32) return;
    fe_to_be32(out32, &ctx->key);
}

EXPORT int s256_run(void *p, int count,
                    u8 *keys_be, u8 *pubkeys33,
                    u8 *hash160s20, u8 *matches)
{
    s256_ctx *ctx = (s256_ctx *)p;
    jac ppt; fe kkey;
    int i, j;

    if (!ctx || count < 1 || count > ctx->max_batch) return -1;
    if (!keys_be || !pubkeys33 || !hash160s20 || !matches) return -1;

    ppt  = ctx->pt;
    kkey = ctx->key;

    /* ── gather: snapshot each key/point and advance ──────────────────── *
     * A row whose point is infinity (key == 0 mod N) is fully processed   *
     * below as a zero-output row, then the scan continues at key = 1.     */
    for (i = 0; i < count; i++) {
        ctx->bufX[i] = ppt.x;
        ctx->bufY[i] = ppt.y;
        ctx->bufZ[i] = ppt.z;
        fe_to_be32(keys_be + (size_t)i * 32, &kkey);

        /* advance: key += 1,  pt += G  (jac_madd(G) maps inf -> G) */
        {   fe nk;
            fe one = FE_ONE;
            addmod(&nk, &kkey, &one);
            if (cmp_fe(&nk, &GROUP_N) >= 0) {
                kkey = FE_ZERO;
                ppt.z = FE_ZERO;
            } else {
                kkey = nk;
                {   jac nxt;
                    jac_madd(&nxt, &ppt, GX_W, GY_W);
                    ppt = nxt;
                }
            }
        }
    }

    {   int actual = count;

        /* ── batch Montgomery inversion of all Z values ──────────────── *
         * The prefix product and the back-substitution skip any row whose
         * Z == 0 (point at infinity, i.e. key == 0 mod N).  For a zero row
         * the inverse is 0 and never feeds back into the accumulator, so a
         * single infinity row cannot poison the whole batch.  A correct
         * non-zero row i satisfies  invz[i] * bufZ[i] == 1.                 */
        {   fe acc = FE_ONE;
            for (i = 0; i < actual; i++) {
                ctx->prefix[i] = acc;                 /* nonzero-only prefix */
                if (!fe_is_zero(&ctx->bufZ[i]))
                    fmul(&acc, &acc, &ctx->bufZ[i]);
            }
            {   fe inv_acc;
                fpow(&inv_acc, &acc, &FIELD_P2);       /* acc^(p-2)      */
                for (i = actual - 1; i >= 0; i--) {
                    if (fe_is_zero(&ctx->bufZ[i])) {
                        ctx->invz[i] = FE_ZERO;
                    } else {
                        fmul(&ctx->invz[i], &inv_acc, &ctx->prefix[i]);
                        fmul(&inv_acc, &inv_acc, &ctx->bufZ[i]);
                    }
                }
            }
        }

        /* ── extract compressed pubkey + hash160 + match check ──────── */
        ctx->last_hit_idx = -1;
        for (i = 0; i < actual; i++) {
            fe iz2, iz3, xa, ya;
            if (fe_is_zero(&ctx->bufZ[i])) {
                /* point at infinity: output zeros */
                memset(pubkeys33  + (size_t)i * 33, 0, 33);
                memset(hash160s20 + (size_t)i * 20, 0, 20);
                matches[i] = 0;
                continue;
            }
            fsqr (&iz2, &ctx->invz[i]);
            fmul (&iz3, &iz2, &ctx->invz[i]);
            fmul (&xa,  &ctx->bufX[i], &iz2);
            fmul (&ya,  &ctx->bufY[i], &iz3);

            pubkeys33[(size_t)i * 33] = 0x02 | (u8)(ya.w[0] & 1);
            fe_to_be32(pubkeys33 + (size_t)i * 33 + 1, &xa);

            hash160_raw(pubkeys33 + (size_t)i * 33, 33,
                        hash160s20 + (size_t)i * 20);

            matches[i] = 0;
            for (j = 0; j < ctx->ntargets; j++) {
                if (memcmp(hash160s20 + (size_t)i * 20,
                           ctx->targets + (size_t)j * 20, 20) == 0)
                {
                    matches[i] = 1;
                    ctx->last_hit_idx = i;
                    memcpy(ctx->last_hit_key,
                           keys_be + (size_t)i * 32, 32);
                    break;
                }
            }
        }

        /* ── advance ctx state past the last processed key ──────────── */
        ctx->key = kkey;
        ctx->pt  = ppt;
        return actual;
    }
}

/* ── standalone hash160 batch (reuses the proven hash160 kernel) ─────── */

EXPORT void s256_hash160_batch(const u8 *pubkeys33, int n, u8 *out20) {
    int i;
    for (i = 0; i < n; i++)
        hash160_raw(pubkeys33 + (size_t)i * 33, 33,
                    out20     + (size_t)i * 20);
}

/* ──────────────────────── self-test ────────────────────────────────── */

EXPORT int s256_selftest(void) {
    s256_ctx *ctx;
    u8 keys[320], pub[330], h160[200], match[10];
    int rc, i;

    /* SHA-256("abc") vector */
    {   u8 msg[] = "abc"; u8 digest[32];
        u8 expected[] = {
            0xba,0x78,0x16,0xbf,0x8f,0x01,0xcf,0xea,
            0x41,0x41,0x40,0xde,0x5d,0xae,0x22,0x23,
            0xb0,0x03,0x61,0xa3,0x96,0x17,0x7a,0x9c,
            0xb4,0x10,0xff,0x61,0xf2,0x00,0x15,0xad };
        sha256(msg, 3, digest);
        if (memcmp(digest, expected, 32) != 0) return -10;
    }

    /* RIPEMD-160("abc") vector */
    {   u8 msg[] = "abc"; u8 digest[20];
        u8 expected[] = {
            0x8e,0xb2,0x08,0xf7,0xe0,0x5d,0x98,0x7a,
            0x9b,0x04,0x4a,0x8e,0x98,0xc6,0xb0,0x87,
            0xf1,0x5a,0x0b,0xfc };
        ripemd160(msg, 3, digest);
        if (memcmp(digest, expected, 20) != 0) return -11;
    }

    /* hash160("abc") = RIPEMD160(SHA256("abc")) */
    {   u8 msg[] = "abc"; u8 h[20];
        hash160_raw(msg, 3, h);
        /* RIPEMD160(sha256("abc")) -- compute inline:
           sha256("abc") = ba7816bf...f20015ad (32 bytes)
           ripemd160 of that = 4b5320... we just check it doesn't crash;
           the exact vector is tested in the Python suite. */
    }

    /* fe arithmetic: addmod(p-1, 1) == 0 */
    {   fe a = FIELD_P, b = FE_ONE, r;
        submod(&a, &a, &FE_ONE);               /* a = p-1              */
        addmod(&r, &a, &b);
        if (!fe_is_zero(&r)) return -20;
    }

    /* submod(0, 1) == p-1 */
    {   fe a = FE_ZERO, b = FE_ONE, r, expected;
        submod(&r, &a, &b);
        submod(&expected, &FIELD_P, &FE_ONE);  /* expected = p-1       */
        if (cmp_fe(&r, &expected) != 0) return -21;
    }

    /* mulmod(p-1, p-1) == 1 */
    {   fe a = FIELD_P, r;
        submod(&a, &a, &FE_ONE);               /* a = p-1              */
        fmul(&r, &a, &a);
        if (cmp_fe(&r, &FE_ONE) != 0) return -22;
    }

    /* invmod(2)*2 == 1 */
    {   fe base = {{2,0,0,0}}, one = FE_ONE, r;
        fpow(&r, &base, &FIELD_P2);            /* r = 2^(p-2) = 1/2   */
        fmul(&r, &r, &base);                   /* r * 2                */
        if (cmp_fe(&r, &one) != 0) return -23;
    }

    /* Point on curve: G is on secp256k1  (y^2 == x^3 + 7) */
    {   fe x, y, x3, y2;
        memcpy(x.w, GX_W, 32);
        memcpy(y.w, GY_W, 32);
        fsqr(&y2, &y);
        fsqr(&x3, &x); fmul(&x3, &x3, &x);    /* x^3                 */
        {   fe seven = {{7,0,0,0}};
            addmod(&x3, &x3, &seven);           /* x^3 + 7             */
        }
        if (cmp_fe(&y2, &x3) != 0) return -30;
    }

    /* Create context, seek to k=1, check compressed pubkey */
    ctx = (s256_ctx *)s256_ctx_new(16);
    if (!ctx) return -40;

    {   u8 key1[32] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
                        0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1};
        u8 pk1_expected[] = {
            0x02,0x79,0xbe,0x66,0x7e,0xf9,0xdc,0xbb,
            0xac,0x55,0xa0,0x62,0x95,0xce,0x87,0x0b,
            0x07,0x02,0x9b,0xfc,0xdb,0x2d,0xce,0x28,
            0xd9,0x59,0xf2,0x81,0x5b,0x16,0xf8,0x17,
            0x98 };

        rc = s256_seek(ctx, key1);
        if (rc != 0) { s256_ctx_free(ctx); return -41; }
        rc = s256_run(ctx, 1, keys, pub, h160, match);
        if (rc != 1) { s256_ctx_free(ctx); return -42; }
        if (memcmp(pub, pk1_expected, 33) != 0) { s256_ctx_free(ctx); return -43; }
    }

    /* Seek to k=2, check compressed pubkey */
    {   u8 key2[32] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
                        0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2};
        u8 pk2_expected[] = {
            0x02,0xc6,0x04,0x7f,0x94,0x41,0xed,0x7d,
            0x6d,0x30,0x45,0x40,0x6e,0x95,0xc0,0x7c,
            0xd8,0x5c,0x77,0x8e,0x4b,0x8c,0xef,0x3c,
            0xa7,0xab,0xac,0x09,0xb9,0x5c,0x70,0x9e,
            0xe5 };

        rc = s256_seek(ctx, key2);
        if (rc != 0) { s256_ctx_free(ctx); return -44; }
        rc = s256_run(ctx, 1, keys, pub, h160, match);
        if (rc != 1) { s256_ctx_free(ctx); return -45; }
        if (memcmp(pub, pk2_expected, 33) != 0) { s256_ctx_free(ctx); return -46; }
    }

    /* Batch: seek to k=1, run 10, verify k=1,2,3 pubkeys correct */
    {   u8 key1[32] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
                        0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1};
        u8 pk1[] = {0x02,0x79,0xbe,0x66,0x7e,0xf9,0xdc,0xbb,
                     0xac,0x55,0xa0,0x62,0x95,0xce,0x87,0x0b,
                     0x07,0x02,0x9b,0xfc,0xdb,0x2d,0xce,0x28,
                     0xd9,0x59,0xf2,0x81,0x5b,0x16,0xf8,0x17,0x98};
        u8 pk2[] = {0x02,0xc6,0x04,0x7f,0x94,0x41,0xed,0x7d,
                     0x6d,0x30,0x45,0x40,0x6e,0x95,0xc0,0x7c,
                     0xd8,0x5c,0x77,0x8e,0x4b,0x8c,0xef,0x3c,
                     0xa7,0xab,0xac,0x09,0xb9,0x5c,0x70,0x9e,0xe5};
        u8 pk3[] = {0x02,0xf9,0x30,0x8a,0x01,0x92,0x58,0xc3,
                     0x10,0x49,0x34,0x4f,0x85,0xf8,0x9d,0x52,
                     0x29,0xb5,0x31,0xc8,0x45,0x83,0x6f,0x99,
                     0xb0,0x86,0x01,0xf1,0x13,0xbc,0xe0,0x36,0xf9};

        s256_seek(ctx, key1);
        rc = s256_run(ctx, 10, keys, pub, h160, match);
        if (rc != 10) { s256_ctx_free(ctx); return -50; }
        if (memcmp(pub+0,  pk1, 33) != 0) { s256_ctx_free(ctx); return -51; }
        if (memcmp(pub+33, pk2, 33) != 0) { s256_ctx_free(ctx); return -52; }
        if (memcmp(pub+66, pk3, 33) != 0) { s256_ctx_free(ctx); return -53; }
    }

    s256_ctx_free(ctx);
    return 1;  /* all passed */
}
