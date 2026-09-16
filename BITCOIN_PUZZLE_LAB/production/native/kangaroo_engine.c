/*
 * kangaroo_engine.c -- Pollard Kangaroo (lambda) DLP range solver for secp256k1
 *
 * Solves  k in [A, B]  such that  k*G == Q  (Q from an SEC1 public key), using
 * the parallel kangaroo / distinguished-point method.  Expected work is
 * O(sqrt(B - A)) group operations, vs O(B - A) for a linear scan.
 *
 * Design
 *   - Pseudo-random walk:  each step, the current point's affine x-coordinate
 *     selects one of KR_NUSE precomputed jump vectors  d_i * G  (stored in
 *     affine form; d_i uniform around sqrt(W)).  A kangaroo jumps by that
 *     vector (mixed JW addition) and its scalar "distance" grows by d_i.
 *   - Tame kangaroos start at (A + s_i)*G with known distance A + s_i; wild
 *     kangaroos start at Q + s_i*G with tracked offset s_i.  A tame/wild
 *     x-collision gives candidates k = T - U and k = N - (T + U); both are
 *     verified against the target key.
 *   - Distinguished points (affine x with dpbits trailing zero bits) are
 *     logged into a shared, lock-free collision table living in an mmap file.
 *     The table IS the checkpoint: on resume, fresh tames collide with wild
 *     DPs retained from a previous process.  Slot writes use 64-bit CAS.
 *   - Kangaroos are walked in herds with one Fermat inversion per herd per
 *     round (Montgomery prefix-product trick), so inversion overhead is
 *     ~2 field multiplications per kangaroo per round.
 *   - The hot loop does zero heap allocation, no hashing, no RNG and no
 *     system calls.  ctx is read-only except the CAS slots and mmap header.
 *
 * Interval arithmetic: A, B arrive as 32-byte big-endian scalars (widths up to
 * 2^128 supported).  Distances accumulate in raw 256-bit limbs; jump sums stay
 * below 2^82 for any feasible run (< 2^41 per-kangaroo steps), so distances
 * never need modular reduction and never reach the group order.
 *
 * Target is a single SEC1 public key (33 or 65 bytes).  Compressed keys are
 * expanded to the full point via sqrt mod p (p = 3 mod 4, so
 * y = (x^3+7)^((p+1)/4)) and the prefix parity selects y vs p - y.
 *
 * Build
 *   MSVC  x64:  call vcvars64.bat first, then
 *               cl /O2 /LD /Febin\kangaroo.dll kangaroo_engine.c
 *   GCC / Clang: gcc -O3 -shared -fPIC -o bin/kangaroo.so kangaroo_engine.c
 */

/* ──────────────────────────── portability ──────────────────────────── */

#ifdef _MSC_VER
#  include <intrin.h>
#  define MUL64(a,b,hi,lo) do { (lo) = _umul128((a),(b),&(hi)); } while(0)
#  define EXPORT __declspec(dllexport)
#else
   typedef unsigned __int128 u128;
#  define MUL64(a,b,hi,lo) do { u128 _p=(u128)(a)*(u128)(b); \
      (hi)=(uint64_t)(_p>>64); (lo)=(uint64_t)(_p); } while(0)
#  define EXPORT __attribute__((visibility("default")))
#endif

#include <string.h>
#include <stdint.h>
#include <stdlib.h>
#include <stdio.h>

typedef uint8_t  u8;
typedef uint32_t u32;
typedef uint64_t u64;

#if defined(_MSC_VER)
static u64 kr_cas64(volatile u64 *p, u64 e, u64 n) {
    return (u64)_InterlockedCompareExchange64((volatile __int64 *)p,
                                              (__int64)n, (__int64)e);
}
static u64 kr_xchg64(volatile u64 *p, u64 n) {
    return (u64)_InterlockedExchange64((volatile __int64 *)p, (__int64)n);
}
#else
static inline u64 kr_cas64(volatile u64 *p, u64 e, u64 n) {
    return __sync_val_compare_and_swap(p, e, n);
}
static inline u64 kr_xchg64(volatile u64 *p, u64 n) {
    return __sync_lock_test_and_set(p, n);
}
#endif

/* ─────────────────────────── field constants ───────────────────────── */

#define C 0x00000001000003D1ULL          /* 2^256 - p                     */

typedef struct { u64 w[4]; } fe;          /* field element / 256-bit LE   */

static const fe FIELD_P  = {{ 0xFFFFFFFEFFFFFC2FULL, 0xFFFFFFFFFFFFFFFFULL,
                              0xFFFFFFFFFFFFFFFFULL, 0xFFFFFFFFFFFFFFFFULL }};
static const fe FIELD_P2 = {{ 0xFFFFFFFEFFFFFC2DULL, 0xFFFFFFFFFFFFFFFFULL,
                              0xFFFFFFFFFFFFFFFFULL, 0xFFFFFFFFFFFFFFFFULL }};/* p-2 */
static const fe P_QUAR   = {{ 0xFFFFFFFFBFFFFF0CULL, 0xFFFFFFFFFFFFFFFFULL,
                              0xFFFFFFFFFFFFFFFFULL, 0x3FFFFFFFFFFFFFFFULL }};/* (p+1)/4 */
static const fe GROUP_N  = {{ 0xBFD25E8CD0364141ULL, 0xBAAEDCE6AF48A03BULL,
                              0xFFFFFFFFFFFFFFFEULL, 0xFFFFFFFFFFFFFFFFULL }};
static const fe FE_ONE   = {{ 1ULL, 0, 0, 0 }};
static const fe FE_ZERO  = {{ 0, 0, 0, 0 }};

static const u64 GX_W[4] = { 0x59F2815B16F81798ULL, 0x029BFCDB2DCE28D9ULL,
                             0x55A06295CE870B07ULL, 0x79BE667EF9DCBBACULL };
static const u64 GY_W[4] = { 0x9C47D08FFB10D4B8ULL, 0xFD17B448A6855419ULL,
                             0x5DA4FBFC0E1108A8ULL, 0x483ADA7726A3C465ULL };

static const u64 C_LIMB[4] = { C, 0, 0, 0 };

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

static void add_limbs(u64 r[4], const u64 a[4], const u64 b[4], u64 *carry) {
    int i; u64 c = 0;
    for (i = 0; i < 4; i++) {
        u64 t = a[i] + c;  c = (t < a[i]);
        u64 s = t + b[i];  c += (s < t);
        r[i] = s;
    }
    *carry = c;
}

static void sub_limbs(u64 r[4], const u64 a[4], const u64 b[4], u64 *borrow) {
    int i; u64 br = 0;
    for (i = 0; i < 4; i++) {
        u64 t = a[i] - br;  br = (a[i] < br);
        u64 s = t - b[i];   br += (t < b[i]);
        r[i] = s;
    }
    *borrow = br;
}

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
        for (j = 0; j < 4; j++) { int bi=k-j;
            if (bi>=0 && bi<4) { u64 v=loP[j*4+bi]; lo+=v; hi+=(lo<v); } }
        for (j = 0; j < 4; j++) { int bi=k-1-j;
            if (bi>=0 && bi<4) { u64 v=hiP[j*4+bi]; lo+=v; hi+=(lo<v); } }
        s  = lo + carry; c2 = (s < lo);
        r[k] = s;
        carry = hi + c2;
    }
}

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

static void fmul(fe *r, const fe *a, const fe *b) {
    u64 w8[8], u5[5], carry;
    fe lo_fe;
    u64 fold[4], c2;

    mul_full(w8, a->w, b->w);
    mul_C5(u5, w8 + 4);

    memcpy(lo_fe.w, w8, 32);
    add_limbs(r->w, lo_fe.w, u5, &carry);

    if (u5[4] + carry) {
        u64 th, tl, tc;
        MUL64(u5[4] + carry, C, th, tl);
        fold[0] = tl; fold[1] = th; fold[2] = 0; fold[3] = 0;
        add_limbs(r->w, r->w, fold, &c2);
        if (c2) { u64 c3; add_limbs(r->w, r->w, C_LIMB, &c3); }
    }

    { int g = 0;
      while (cmp_fe(r, &FIELD_P) >= 0 && g++ < 3) {
          u64 br; sub_limbs(r->w, r->w, FIELD_P.w, &br); } }
}

static void fsqr(fe *r, const fe *a) { fmul(r, a, a); }

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

typedef struct { fe x, y, z; } jac;

static int  jac_is_inf(const jac *p) { return p->z.w[0]==0 && p->z.w[1]==0
                                     && p->z.w[2]==0 && p->z.w[3]==0; }

static void jac_dbl(jac *r, const jac *p) {
    fe x2, y2, y4, s, d, e, t, t2, y4x8;
    if (jac_is_inf(p)) { *r = *p; return; }

    fsqr(&x2, &p->x);
    fsqr(&y2, &p->y);
    fsqr(&y4, &y2);

    addmod(&t, &p->x, &y2);
    fsqr(&s, &t);
    submod(&s, &s, &x2);
    submod(&s, &s, &y4);

    addmod(&d, &s, &s);
    addmod(&e, &x2, &x2); addmod(&e, &e, &x2);

    fsqr(&t, &e);
    submod(&t, &t, &d);
    submod(&t, &t, &d);

    submod(&t2, &d, &t);
    fmul(&t2, &e, &t2);
    addmod(&y4x8, &y4, &y4); addmod(&y4x8, &y4x8, &y4x8);
    addmod(&y4x8, &y4x8, &y4x8);
    submod(&t2, &t2, &y4x8);

    fmul(&r->z, &p->y, &p->z);
    addmod(&r->z, &r->z, &r->z);

    r->x = t;  r->y = t2;
}

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

    fsqr(&z2, &p->z);
    fmul(&u_fe, &axf, &z2);
    fmul(&s_fe, &p->z, &z2);
    fmul(&s_fe, &ayf, &s_fe);

    if (cmp_fe(&u_fe, &p->x) == 0) {
        if (cmp_fe(&s_fe, &p->y) == 0) { jac_dbl(r, p); return; }
        r->z = FE_ZERO;
        return;
    }

    submod(&h,   &u_fe, &p->x);
    fsqr (&h2,  &h);
    fmul (&h3,  &h2, &h);
    submod(&rn, &s_fe, &p->y);
    fmul (&v,   &p->x, &h2);

    fsqr (&xn, &rn);
    submod(&xn, &xn, &v);
    submod(&xn, &xn, &v);
    submod(&xn, &xn, &h3);

    submod(&vn, &v, &xn);
    fmul (&vn, &rn, &vn);
    fmul (&tmp, &p->y, &h3);
    submod(&vn, &vn, &tmp);

    fmul(&r->z, &p->z, &h);

    r->x = xn;  r->y = vn;
}

static void to_affine(fe *ax, fe *ay, const jac *p) {
    fe zi, zi2, zi3;
    fpow(&zi,  &p->z, &FIELD_P2);
    fsqr (&zi2, &zi);
    fmul (&zi3, &zi2, &zi);
    fmul (ax, &p->x, &zi2);
    fmul (ay, &p->y, &zi3);
}

static void scalar_mult(jac *r, const u64 k[4],
                        const fe Wx[15], const fe Wy[15]) {
    u8 nib[64];
    int i, j, started = 0;

    for (i = 0; i < 4; i++)
        for (j = 0; j < 16; j++)
            nib[i*16+j] = (u8)((k[i] >> (j*4)) & 0xF);

    r->z = FE_ZERO;

    for (i = 63; i >= 0; i--) {
        int v = nib[i];
        if (!started && v == 0) continue;
        if (started) {
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
    if (!started) r->z = FE_ZERO;
}

/* ──────────────── 128-bit helpers + integer square root ────────────── */

static void u128_add(u64 r[2], const u64 a[2], const u64 b[2]) {
    u64 lo = a[0] + b[0];
    r[0] = lo;
    r[1] = a[1] + b[1] + (lo < a[0]);
}
static void u128_sub(u64 r[2], const u64 a[2], const u64 b[2]) {
    u64 lo = a[0] - b[0];
    r[1] = a[1] - b[1] - (a[0] < b[0]);
    r[0] = lo;
}
static int u128_cmp(const u64 a[2], const u64 b[2]) {
    if (a[1] != b[1]) return a[1] < b[1] ? -1 : 1;
    if (a[0] != b[0]) return a[0] < b[0] ? -1 : 1;
    return 0;
}
static void u128_mul64(u64 r[2], u64 a, u64 b) {
    u64 hi, lo;
    MUL64(a, b, hi, lo);
    r[0] = lo; r[1] = hi;
}

static u64 isqrt64(u64 n) {
    u64 x;
    if (n == 0) return 0;
    x = (u64)sqrt((double)n);
    while (x > 0 && x > n / x) x--;
    while (x + 1 <= n / (x + 1)) x++;
    return x;
}

static u64 isqrt_u128(const u64 a[2]) {
    u64 x, y, sq[2];
    double d;
    if (a[1] == 0) return isqrt64(a[0]);
    d = (double)a[1] * 18446744073709551616.0 + (double)a[0];
    x = (u64)sqrt(d);
    for (;;) {
        u128_mul64(sq, x, x);
        if (sq[1] < a[1]) break;
        if (sq[1] > a[1]) { x--; continue; }
        if (sq[0] <= a[0]) break;
        x--;
    }
    for (;;) {
        y = x + 1;
        u128_mul64(sq, y, y);
        if (sq[1] > a[1]) break;
        if (sq[1] < a[1]) { x = y; continue; }
        if (sq[0] > a[0]) break;
        x = y;
    }
    return x;
}

/* ────────────────── deterministic PRNG (splitmix64) ────────────────── */

static u64 sm64(u64 *s) {
    u64 z = (*s += 0x9E3779B97F4A7C15ULL);
    z = (z ^ (z >> 30)) * 0xBF58476D1CE4E5B9ULL;
    z = (z ^ (z >> 27)) * 0x94D049BB133111EBULL;
    return z ^ (z >> 31);
}

/* uniform 256-bit offset in [0, W):  bit-by-bit long division over a random
 * 256-bit draw; init-time only, never in the hot walk.  Invariant rem < W is
 * preserved after each bit because 2*rem+1 <= 2W-1 < 2W (one subtract).   */
static void rnd_mod_fe(u64 out[4], u64 *rng, const u64 W[4]) {
    u64 rw[4], rem[4] = {0, 0, 0, 0}, c;
    int i, j;
    fe Wf, R;
    Wf.w[0] = W[0]; Wf.w[1] = W[1]; Wf.w[2] = W[2]; Wf.w[3] = W[3];
    rw[0] = sm64(rng); rw[1] = sm64(rng);
    rw[2] = sm64(rng); rw[3] = sm64(rng);
    for (i = 255; i >= 0; i--) {
        c = 0;
        for (j = 0; j < 4; j++) { u64 t = rem[j]; rem[j] = (t << 1) | c; c = t >> 63; }
        rem[0] |= (rw[i / 64] >> (i & 63)) & 1;
        R.w[0] = rem[0]; R.w[1] = rem[1]; R.w[2] = rem[2]; R.w[3] = rem[3];
        if (cmp_fe(&R, &Wf) >= 0) { u64 br; sub_limbs(rem, rem, W, &br); }
    }
    out[0] = rem[0]; out[1] = rem[1]; out[2] = rem[2]; out[3] = rem[3];
}

/* ───────────── mmap layout: 128-byte header + 64-byte slots ────────── */

static const u8 KR_MAGIC[8]  = { 'K','R','D','P','1',0,0,0 };
#define KR_VERSION            1
#define KR_HDRSIZE            160
#define KR_SLOT               96
#define KR_NUSE               65536

#define HDR_VERSION  8
#define HDR_FLAGS   16
#define HDR_CTRL    24
#define HDR_SEED    32
#define HDR_STEPS   40
#define HDR_DPS     48
#define HDR_CROSS   56
#define HDR_KEY     64
#define HDR_A       96                /* 32-byte BE bounds (256-bit) */
#define HDR_B       128

#define TAG_EMPTY  0ULL
#define TAG_CLAIM  1ULL
#define TAG_FULL   2ULL
#define TAG_TAME   0x100ULL
#define TAG_MASK   3ULL

/* ───────────────────────── DP table (lock-free) ────────────────────── */

typedef struct {
    volatile u8 *base;         /* whole mmap: header then slots          */
    u32 nlog2, dpbits, nslots;
    u64 dpmask;                /* (1<<dpbits)-1, dpbits <= 32            */
} dp_tab;

static u64 hdr_rd64(volatile u8 *base, int off) {
    return *(volatile u64 *)(base + off);
}

/* Returns 0 inserted, 1 collision (fills storeDist/storeTame), 2 full.    *
 * Slot layout (96 B): x (32) | dist (32) | tag (8).                      */
static int dp_insert(dp_tab *t, const fe *x, const u64 dist[4], int isTame,
                     u64 storeDist[4], int *storeTame) {
    u64 hash = x->w[0] ^ (x->w[1] ^ (x->w[1] >> 32));
    u64 mask = (u64)t->nslots - 1;
    u64 probe, limit = (u64)t->nslots;
    volatile u8 *slots = t->base + KR_HDRSIZE;
    u64 typebit = isTame ? TAG_TAME : 0;

    for (probe = 0; probe < limit; probe++) {
        volatile u8 *s = slots + (size_t)((hash + probe) & mask) * KR_SLOT;
        volatile u64 *tagp = (volatile u64 *)(s + 64);
        for (;;) {
            u64 tlv = kr_cas64(tagp, TAG_FULL, TAG_FULL);
            if ((tlv & TAG_MASK) == TAG_FULL) {
                if (memcmp((void *)s, x->w, 32) == 0) {
                    memcpy((void *)storeDist, (const void *)(s + 32), 32);
                    *storeTame = (int)((tlv >> 8) & 1);
                    return 1;
                }
                break;                     /* occupied, different x: probe */
            }
            if ((tlv & TAG_MASK) == TAG_EMPTY) {
                if (kr_cas64(tagp, TAG_EMPTY, TAG_CLAIM | typebit)
                    == TAG_EMPTY)
                {
                    memcpy((void *)s, x->w, 32);
                    memcpy((void *)(s + 32), dist, 32);
                    (void)kr_cas64(tagp, TAG_CLAIM | typebit,
                                   TAG_FULL | typebit);
                    return 0;
                }
                continue;                    /* lost the race: re-read */
            }
            /* TAG_CLAIM in flight: spin until resolve */
        }
    }
    return 2;
}

/* ───────────────────────────── engine ──────────────────────────────── */

typedef struct {
    fe   A, B;                       /* raw bounds (not reduced)          */
    u64  Wv[4];                      /* interval width B - A + 1 (256-bit) */
    jac  Q;                          /* target point                     */
    u8   target33[33];               /* canonical compressed target      */

    fe   nuse_d[KR_NUSE];            /* jump distance (as fe)            */
    u64  nuse_jx[KR_NUSE][4];        /* jump vector x, affine, LE        */
    u64  nuse_jy[KR_NUSE][4];        /* jump vector y, affine, LE        */
    fe   Wx[15], Wy[15];             /* window (i+1)*G affine            */

    dp_tab tab;
    int   nthreads, kpt, ntame, nwild;
    u64   budget;

    u8   *th_mem;
    struct kr_th {
        jac  *tpt; u64 *tdis; int tcnt;
        jac  *wpt; u64 *wdis; int wcnt;
        fe   *bufX, *bufY, *bufZ, *prefix, *invz;
        int   cap;
    } th[32];
} kr_eng;

static void kr_set_found(kr_eng *e, const u64 k[4]) {
    volatile u8 *h = e->tab.base;
    fe_to_be32((u8 *)(h + HDR_KEY), (const fe *)k);    /* BE key */
    (void)kr_cas64((volatile u64 *)(h + HDR_FLAGS), 0, 1);
}
static int kr_stop_req(kr_eng *e) {
    return (hdr_rd64(e->tab.base, HDR_CTRL) & 1) != 0;
}

/* verify pubkey(candidate) == target; returns 1 on solution              */
static int kr_verify(kr_eng *e, const u64 k[4]) {
    jac pt;
    fe ax, ay;
    u8 pk[33];
    scalar_mult(&pt, k, e->Wx, e->Wy);
    to_affine(&ax, &ay, &pt);
    pk[0] = (u8)(0x02 | (ay.w[0] & 1));
    fe_to_be32(pk + 1, &ax);
    return memcmp(pk, e->target33, 33) == 0;
}

/* ────────────── herd walking worker (one per hardware thread) ──────── */

EXPORT int kr_worker(void *p, int tid, int nthreads, u8 out32[32]) {
    kr_eng *e = (kr_eng *)p;
    struct kr_th *th;
    int R, i, k;
    u64 local_steps = 0;

    if (!e || !out32) return -2;
    if (tid < 0 || tid >= nthreads || tid >= 32) return -2;
    th = &e->th[tid];
    R  = th->tcnt + th->wcnt;
    if (R == 0) return -2;
    memset(out32, 0, 32);

    for (;;) {
        /* snapshot herd Jacobian coordinates for the batch inversion */
        for (k = 0; k < th->tcnt; k++) {
            th->bufX[k] = th->tpt[k].x;
            th->bufY[k] = th->tpt[k].y;
            th->bufZ[k] = th->tpt[k].z;
        }
        for (k = 0; k < th->wcnt; k++) {
            th->bufX[th->tcnt + k] = th->wpt[k].x;
            th->bufY[th->tcnt + k] = th->wpt[k].y;
            th->bufZ[th->tcnt + k] = th->wpt[k].z;
        }

        /* one Fermat inversion per herd (Montgomery prefix-product) */
        {   fe acc = FE_ONE;
            for (i = 0; i < R; i++) {
                th->prefix[i] = acc;
                fmul(&acc, &acc, &th->bufZ[i]);
            }
            fpow(&acc, &acc, &FIELD_P2);
            for (i = R - 1; i >= 0; i--) {
                fmul(&th->invz[i], &acc, &th->prefix[i]);
                fmul(&acc, &acc, &th->bufZ[i]);
            }
        }

        /* walk every kangaroo of this thread's herd */
        for (k = 0; k < R; k++) {
            int isTame = k < th->tcnt;
            jac *cur = isTame ? &th->tpt[k] : &th->wpt[k - th->tcnt];
            u64 *dst = isTame ? th->tdis + (size_t)4 * k
                              : th->wdis + (size_t)4 * (k - th->tcnt);
            fe iz2, xa;
            u64 jidx;

            fsqr(&iz2, &th->invz[k]);
            fmul(&xa, &th->bufX[k], &iz2);           /* affine x */

            /* distinguished point computed from the public-key x bits */
            if ((xa.w[0] & e->tab.dpmask) == 0) {
                u64 sdist[4]; int stame, rc;
                rc = dp_insert(&e->tab, &xa, dst, isTame, sdist, &stame);
                if (rc == 0) {
                    volatile u8 *h = e->tab.base;
                    u64 d = hdr_rd64(h, HDR_DPS);
                    (void)kr_cas64((volatile u64 *)(h + HDR_DPS), d, d + 1);
                }
                if (rc == 1 && stame != isTame) {
                    volatile u8 *hx = e->tab.base;
                    u64 cc = hdr_rd64(hx, HDR_CROSS);
                    (void)kr_cas64((volatile u64 *)(hx + HDR_CROSS), cc, cc + 1);
                    /* T = tame abs distance, U = wild offset.  candidate1 *
                     * = T - U  (k = T - U), candidate2 = N - (T + U)      *
                     * (point negation).                                    */
                    u64 distT[4], distU[4], cand1[4], cand2[4], sum[4];
                    u64 br, c2;
                    if (isTame) {
                        memcpy(distT, dst, 32);
                        memcpy(distU, sdist, 32);
                    } else {
                        memcpy(distU, dst, 32);
                        memcpy(distT, sdist, 32);
                    }
                    sub_limbs(cand1, distT, distU, &br);
                    if (br) { add_limbs(cand1, cand1, GROUP_N.w, &c2); }
                    if (kr_verify(e, cand1)) { kr_set_found(e, cand1);
                                               goto found_out; }
                    add_limbs(sum, distT, distU, &c2);
                    sub_limbs(cand2, GROUP_N.w, sum, &br);
                    if (kr_verify(e, cand2)) { kr_set_found(e, cand2);
                                               goto found_out; }
                }
            }

            jidx = xa.w[0] & (KR_NUSE - 1);
            jac_madd(cur, cur, e->nuse_jx[jidx], e->nuse_jy[jidx]);
            {   u64 carry;
                add_limbs(dst, dst, e->nuse_d[jidx].w, &carry);
            }
            local_steps++;
        }

        /* periodic telemetry / budget / stop / found */
        if ((local_steps & 0x3FFFU) == 0) {
            volatile u8 *h = e->tab.base;
            u64 s = hdr_rd64(h, HDR_STEPS);
            if (s >= e->budget) goto budget_out;
            (void)kr_cas64((volatile u64 *)(h + HDR_STEPS), s, s + local_steps);
            local_steps = 0;
            if (kr_stop_req(e))              goto stop_out;
            if (hdr_rd64(h, HDR_FLAGS) & 1)  goto found_out;
        }
    }

found_out:
    memcpy(out32, (void *)(e->tab.base + HDR_KEY), 32);
    return 1;
budget_out:
    return 0;
stop_out:
    return -1;
}

/* ─────────────────────── setup helpers (init-time) ─────────────────── */

static void precompute_window(fe Wx[15], fe Wy[15]) {
    jac cur;
    int i;
    cur.z = FE_ZERO;
    for (i = 0; i < 15; i++) {
        jac_madd(&cur, &cur, GX_W, GY_W);
        to_affine(&Wx[i], &Wy[i], &cur);
    }
}

/* SEC1 pubkey -> target point + canonical compressed form               *
 * returns 0 on success.  Compressed: solve y via sqrt((x^3+7)^((p+1)/4)) */
static int parse_target(jac *Q, u8 target33[33],
                        const u8 *pub, int plen) {
    fe x, y, x3, seven = {{7,0,0,0}}, t, r;
    if (plen != 33 && plen != 65) return -1;
    if (plen == 33) {
        u8 pfx = pub[0];
        if (pfx != 0x02 && pfx != 0x03) return -1;
        be32_to_fe(&x, pub + 1);
        fsqr(&x3, &x); fmul(&x3, &x3, &x);
        addmod(&x3, &x3, &seven);              /* x^3 + 7 */
        fpow(&r, &x3, &P_QUAR);                /* r = sqrt via (p+1)/4 */
        fsqr(&t, &r);
        if (cmp_fe(&t, &x3) != 0) return -1;   /* non-residue: no such y */
        y = r;
        if ((y.w[0] & 1) != (u64)(pfx & 1)) submod(&y, &FIELD_P, &y); /* p-y by parity */
    } else {
        if (pub[0] != 0x04) return -1;
        be32_to_fe(&x, pub + 1);
        be32_to_fe(&y, pub + 33);
        /* verify on curve */
        fsqr(&t, &y);
        fsqr(&x3, &x); fmul(&x3, &x3, &x);
        addmod(&x3, &x3, &seven);
        if (cmp_fe(&t, &x3) != 0) return -1;
    }
    Q->x = x; Q->y = y; Q->z = FE_ONE;
    target33[0] = (u8)(0x02 | (y.w[0] & 1));
    fe_to_be32(target33 + 1, &x);
    return 0;
}

/* Build the jump table: d_i uniform in [mean, 2*mean), vectors d_i*G.   *
 * DP selection uses the low bits of affine x, so no hash is required.   */
static void build_jump_table(kr_eng *e, u64 mean, u64 rng) {
    int i;
    for (i = 0; i < KR_NUSE; i++) {
        u64 d = mean + (sm64(&rng) % mean);     /* [mean, 2*mean) */
        jac pt;
        e->nuse_d[i] = FE_ZERO;
        e->nuse_d[i].w[0] = d;
        scalar_mult(&pt, e->nuse_d[i].w, e->Wx, e->Wy);
        to_affine((fe *)&e->nuse_jx[i], (fe *)&e->nuse_jy[i], &pt);
    }
}

/* Reposition every herd:  tame at (A + s)*G, wild at Q + s*G,             *
 * with starting offsets uniform over the interval width [0, W) so tame     *
 * and wild scalar spaces overlap from the start.                           */
static void seed_herds(kr_eng *e, u64 rng) {
    int tid, g;
    int used[32];
    memset(used, 0, sizeof used);

    for (g = 0; g < e->ntame; g++) {
        fe s, start, off;
        jac pt;
        tid = g % e->nthreads;
        rnd_mod_fe(s.w, &rng, e->Wv);
        start = e->A;
        {   u64 c;
            add_limbs(start.w, start.w, s.w, &c);   /* A + s < B + 1 < 2^256 */
        }
        scalar_mult(&pt, start.w, e->Wx, e->Wy);
        e->th[tid].tpt[used[tid]] = pt;
        memcpy(e->th[tid].tdis + (size_t)4 * used[tid], start.w, 32);
        used[tid]++;
    }
    memset(used, 0, sizeof used);

    for (g = 0; g < e->nwild; g++) {
        fe s;
        jac start, pt;
        fe jx, jy;
        tid = g % e->nthreads;
        rnd_mod_fe(s.w, &rng, e->Wv);
        scalar_mult(&start, s.w, e->Wx, e->Wy);
        to_affine(&jx, &jy, &start);
        jac_madd(&pt, &e->Q, jx.w, jy.w);             /* Q + s*G */
        e->th[tid].wpt[used[tid]] = pt;
        memcpy(e->th[tid].wdis + (size_t)4 * used[tid], s.w, 32);
        used[tid]++;
    }
}

/* ─────────────────────── public API ────────────────────────────────── */

/* Create an engine over dpmem (the mmap holding header + DP slots).       *
 * errcode: 0 ok, 1 bad args, 2 bad target key, 3 bad range, 4 alloc,     *
 *           5 dp buffer too small, 6 dp header mismatch.                   */
EXPORT void *kr_new(const u8 A32[32], const u8 B32[32],
                    const u8 *pub, int publen,
                    void *dpmem, u64 dmem_size,
                    int nthreads, int ntame, int nwild,
                    int dpbits, u64 seed, u64 budget, int *errcode)
{
    kr_eng *e;
    u64 rng;
    int tid;
    void *fail_buf = NULL;

    if (errcode) *errcode = 0;
    if (!A32 || !B32 || !pub || !dpmem || dmem_size < KR_HDRSIZE + 4*KR_SLOT)
        { if (errcode) *errcode = 1; return NULL; }
    if (nthreads < 1 || nthreads > 32 || ntame < 1 || nwild < 1 ||
        dpbits < 1 || dpbits > 31)
        { if (errcode) *errcode = 1; return NULL; }

    e = (kr_eng *)calloc(1, sizeof *e);
    if (!e) { if (errcode) *errcode = 4; return NULL; }

    be32_to_fe(&e->A, A32);
    be32_to_fe(&e->B, B32);
    if (cmp_fe(&e->A, &e->B) >= 0 || cmp_fe(&e->B, &GROUP_N) >= 0)
        { if (errcode) *errcode = 3; free(e); return NULL; }

    if (parse_target(&e->Q, e->target33, pub, publen) != 0)
        { if (errcode) *errcode = 2; free(e); return NULL; }

    /* ── DP table bounds + header init / resume ── */
    {   u64 slots = (dmem_size - KR_HDRSIZE) / KR_SLOT;
        u32 nlog2 = 0;
        while (slots > 1) { slots >>= 1; nlog2++; }
        if (nlog2 < 2) { if (errcode) *errcode = 5; free(e); return NULL; }
        e->tab.base   = (volatile u8 *)dpmem;
        e->tab.nlog2  = nlog2;
        e->tab.nslots = 1u << nlog2;
        e->tab.dpbits = (u32)dpbits;
        e->tab.dpmask = ((u64)1 << dpbits) - 1;
    }

    {   volatile u8 *base = e->tab.base;
        u64 ver = hdr_rd64(base, HDR_VERSION);
        if (ver == 0) {
            /* fresh file */
            memset((void *)base, 0, KR_HDRSIZE);
            memcpy((void *)base, KR_MAGIC, 8);
            ver = KR_VERSION;
            memcpy((void *)(base + HDR_VERSION), &ver, 8);
            memcpy((void *)(base + HDR_SEED), &seed, 8);
            memcpy((void *)(base + HDR_A), A32, 32);
            memcpy((void *)(base + HDR_B), B32, 32);
        } else {
            if (memcmp((void *)base, KR_MAGIC, 8) != 0 ||
                ver != KR_VERSION)
                { if (errcode) *errcode = 6; free(e); return NULL; }
            if (memcmp((void *)(base + HDR_A), A32, 32) != 0 ||
                memcmp((void *)(base + HDR_B), B32, 32) != 0)
                { if (errcode) *errcode = 6; free(e); return NULL; }
        }
    }

    precompute_window(e->Wx, e->Wy);

    {   u64 one[4] = {1, 0, 0, 0}, br, mean;
        sub_limbs(e->Wv, e->B.w, e->A.w, &br);
        add_limbs(e->Wv, e->Wv, one, &br);          /* Wv = B - A + 1 */
        if (e->Wv[3] | e->Wv[2]) mean = ((u64)1 << 62);
        else mean = isqrt_u128(e->Wv);
        if (mean > ((u64)1 << 62)) mean = ((u64)1 << 62);
        if (mean < 1) mean = 1;
        rng = seed ^ 0x4A4B0C1D2E3F4A5BULL;
        build_jump_table(e, mean, rng);
    }

    e->nthreads = nthreads;
    e->ntame    = ntame;
    e->nwild    = nwild;
    e->budget   = budget;

    {   int base_t = ntame / nthreads, rem_t = ntame % nthreads;
        int base_w = nwild / nthreads, rem_w = nwild % nthreads;
        int kpt = 0;
        for (tid = 0; tid < nthreads; tid++) {
            e->th[tid].tcnt = base_t + (tid < rem_t ? 1 : 0);
            e->th[tid].wcnt = base_w + (tid < rem_w ? 1 : 0);
            if (e->th[tid].tcnt + e->th[tid].wcnt > kpt)
                kpt = e->th[tid].tcnt + e->th[tid].wcnt;
        }
        e->kpt = kpt;

        /* one contiguous per-thread block: tpts | tdis | wpts | wdis | scratch */
        {   size_t total = 0, offs[32], i;
            for (tid = 0; tid < nthreads; tid++) {
                offs[tid] = total;
                total += (size_t)e->th[tid].tcnt * sizeof(jac);
                total += (size_t)e->th[tid].tcnt * 32;
                total += (size_t)e->th[tid].wcnt * sizeof(jac);
                total += (size_t)e->th[tid].wcnt * 32;
                total += (size_t)kpt * 5 * sizeof(fe);   /* own scratch */
            }
            e->th_mem = (u8 *)calloc(1, total ? total : 1);
            if (!e->th_mem) { if (errcode) *errcode = 4; free(e); return NULL; }
            for (tid = 0; tid < nthreads; tid++) {
                u8 *p = e->th_mem + offs[tid];
                e->th[tid].tpt = (jac *)p;
                p += (size_t)e->th[tid].tcnt * sizeof(jac);
                e->th[tid].tdis = (u64 *)p;
                p += (size_t)e->th[tid].tcnt * 32;
                e->th[tid].wpt = (jac *)p;
                p += (size_t)e->th[tid].wcnt * sizeof(jac);
                e->th[tid].wdis = (u64 *)p;
                p += (size_t)e->th[tid].wcnt * 32;
                e->th[tid].bufX    = (fe *)p; p += (size_t)kpt * sizeof(fe);
                e->th[tid].bufY    = (fe *)p; p += (size_t)kpt * sizeof(fe);
                e->th[tid].bufZ    = (fe *)p; p += (size_t)kpt * sizeof(fe);
                e->th[tid].prefix  = (fe *)p; p += (size_t)kpt * sizeof(fe);
                e->th[tid].invz    = (fe *)p;
                e->th[tid].cap     = kpt;
            }
        }
    }

    seed_herds(e, seed ^ 0x1A2B3C4D5E6F7081ULL);

    /* remember the seed that produced the current herds */
    memcpy((void *)(e->tab.base + HDR_SEED), &seed, 8);
    (void)fail_buf;
    return e;
}

/* Re-seed the herds and clear found/steps but PRESERVE the DP table.      *
 * This is the checkpoint-friendly "continue with a fresh walk" call.       */
EXPORT int kr_reset(void *p, u64 seed, u64 budget) {
    kr_eng *e = (kr_eng *)p;
    volatile u8 *h;
    if (!e) return -1;
    h = e->tab.base;
    e->budget = budget;
    seed_herds(e, seed ^ 0x1A2B3C4D5E6F7081ULL);
    (void)kr_xchg64((volatile u64 *)(h + HDR_FLAGS), 0);
    (void)kr_xchg64((volatile u64 *)(h + HDR_CTRL), 0);
    (void)kr_xchg64((volatile u64 *)(h + HDR_STEPS), 0);
    memcpy((void *)(h + HDR_SEED), &seed, 8);
    memcpy((void *)(h + HDR_KEY), &FE_ZERO, 32);
    return 0;
}

EXPORT void kr_stop(void *p) {
    kr_eng *e = (kr_eng *)p;
    if (!e) return;
    (void)kr_xchg64((volatile u64 *)(e->tab.base + HDR_CTRL),
                    hdr_rd64(e->tab.base, HDR_CTRL) | 1);
}

EXPORT void kr_stats(void *p, u64 *steps, u64 *dps, u64 *flags, u64 *cross) {
    kr_eng *e = (kr_eng *)p;
    if (!e) return;
    if (steps) *steps = hdr_rd64(e->tab.base, HDR_STEPS);
    if (dps)   *dps   = hdr_rd64(e->tab.base, HDR_DPS);
    if (flags) *flags = hdr_rd64(e->tab.base, HDR_FLAGS);
    if (cross) *cross = hdr_rd64(e->tab.base, HDR_CROSS);
}

EXPORT void kr_free(void *p) {
    kr_eng *e = (kr_eng *)p;
    if (!e) return;
    free(e->th_mem);
    free(e);
}

/* ──────────────────────── self-test ────────────────────────────────── */

EXPORT int kr_selftest(void) {
    /* 1) field arithmetic */
    {   fe a = FIELD_P, b = FE_ONE, r;
        submod(&a, &a, &FE_ONE);               /* a = p-1 */
        addmod(&r, &a, &b);
        if (!fe_is_zero(&r)) return -20;
    }
    {   fe a = FIELD_P, r;
        submod(&a, &a, &FE_ONE);               /* a = p-1 */
        fmul(&r, &a, &a);
        if (memcmp(r.w, FE_ONE.w, 32) != 0) return -22;
    }
    {   fe base = {{2,0,0,0}}, r;
        fpow(&r, &base, &FIELD_P2);
        fmul(&r, &r, &base);
        if (memcmp(r.w, FE_ONE.w, 32) != 0) return -23;
    }
    /* 2) G on curve  (y^2 == x^3 + 7) */
    {   fe x, y, x3, y2, seven = {{7,0,0,0}};
        memcpy(x.w, GX_W, 32);
        memcpy(y.w, GY_W, 32);
        fsqr(&y2, &y);
        fsqr(&x3, &x); fmul(&x3, &x3, &x);
        addmod(&x3, &x3, &seven);
        if (cmp_fe(&y2, &x3) != 0) return -30;
    }
    /* 3) compressed-key y recovery: 02||Gx must give y == Gy */
    {   jac Q2; u8 t33[33], cpk[33], xb[32];
        fe xf, yy;
        memcpy(xf.w, GX_W, 32);
        fe_to_be32(xb, &xf);
        cpk[0] = 0x02;
        memcpy(cpk + 1, xb, 32);
        if (parse_target(&Q2, t33, cpk, 33) != 0) return -31;
        memcpy(yy.w, GY_W, 32);
        if (cmp_fe(&Q2.y, &yy) != 0) return -32;
        if (memcmp(t33, cpk, 33) != 0) return -33;
    }
    /* 4) tiny interval solve: A=4096, B=8191, target k=6000 */
    {   static u8 dptab[KR_HDRSIZE + (1u << 10) * KR_SLOT];
        u8 A32[32] = {0}, B32[32] = {0}, outk[32];
        u64 kk = 6000;
        jac pt, Q2;
        u8 tgt[65];
        void *eng;
        int rc, err = 0;
        fe Wx[15], Wy[15], kf;

        precompute_window(Wx, Wy);
        kf = FE_ZERO; kf.w[0] = kk;
        scalar_mult(&pt, kf.w, Wx, Wy);
        to_affine(&Q2.x, &Q2.y, &pt);
        Q2.z = FE_ONE;
        tgt[0] = 0x04;
        fe_to_be32(tgt + 1, &Q2.x);
        fe_to_be32(tgt + 33, &Q2.y);

        A32[30] = 0x10;                          /* 4096   */
        B32[30] = 0x1F; B32[31] = 0xFF;          /* 8191   */

        eng = kr_new(A32, B32, tgt, 65, dptab, sizeof dptab,
                     1, 6, 6, 8, 12345, 2000000, &err);
        if (!eng) return -40;
        rc = kr_worker(eng, 0, 1, outk);
        kr_free(eng);
        if (rc != 1) return -41;
        {   fe o;
            be32_to_fe(&o, outk);
            if (o.w[0] != kk || o.w[1] || o.w[2] || o.w[3]) return -42;
        }
    }
    return 1;  /* all passed */
}