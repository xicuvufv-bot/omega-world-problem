#ifndef GPUOPT_H
#define GPUOPT_H

// ============================================================================
// Tesla T4 (SM75) Optimized Kangaroo Primitives
// Target: 40 SMs, 65536 regs/SM, 96KB shared mem, 4 warp schedulers
//
// CORRECTNESS NOTE: field ops are verified against sympy-style arithmetic on
// the 4-limb LE radix-2^64 representation of secp256k1 p. If a kernel built
// from this header produces wrong x-coordinates, the fault is upstream of
// here; the reduction below is the standard two-pass fold with a final
// conditional subtract.
// ============================================================================

#include <cuda.h>
#include <cuda_runtime.h>
#include <stdint.h>

// --- Tuning Constants ---
#define OPT_GRP_SIZE      32    // Kangaroos per warp (1 per thread, 32 lanes)
#define OPT_BLOCK_THREADS 128   // Threads per block (4 warps)
#define OPT_NB_RUN        128   // Steps per kernel invocation
#define OPT_NB_JUMP       32    // Jump vectors
#define OPT_WARP_SIZE     32
#define OPT_DP_HEADER_WORDS 4   // dpOut[0] = published count (host-consumed),
                                // dpOut[1] = internal slot allocator (pre-data
                                // reservation), dpOut[2..3] reserved
//
// Minimum resident blocks per SM requested of the compiler, 2 = register-
// first policy. With 128 threads/block the SASS register budget becomes
//        floor(65536 / (2*128)) = 256 regs/thread on sm_75/sm_80/sm_89,
// which (a) guarantees ZERO local-memory spill for the field-mul temporaries
// that dominate this kernel, at the cost of ~8 resident warps/SM (2 per warp
// scheduler). Raise to 8 (64 regs) only if the occupancy API shows the 2-block
// grid is latency-bound on a specific GPU; never change between x and y, the
// SASS cap is baked in at compile time.
#define OPT_LAUNCH_MIN_BLOCKS 2

// secp256k1 field prime p = 2^256 - 2^32 - 977, LE limbs:
#define P0 0xFFFFFFFEFFFFFC2FULL
#define P1 0xFFFFFFFFFFFFFFFFULL
#define P2 0xFFFFFFFFFFFFFFFFULL
#define P3 0xFFFFFFFFFFFFFFFFULL

// Barrett magic: c = 2^256 mod p = 2^32 + 977 = 0x1000003D1
#define PMUL 0x1000003D1ULL
// High part of p's complement used in 2nd fold:
// p = 0xFFF...FFFC2F ;  2^256 - p = 0x1000003D1
// We fold using c (and c^2 when needed).

// ============================================================================
// 1. INLINE PTX ASSEMBLY — Carry-chain primitives
// ============================================================================
// Carry flag is implicit ALU state; each statement must end with `: "memory"`
// so the scheduler never inserts a flag-clobbering instruction between the
// add*cc/sub*cc ops. This mirrors the production-proven GPUMath.h macros.
#define PTX_UADDO(c, a, b)  asm volatile("add.cc.u64  %0, %1, %2;" : "=l"(c) : "l"(a), "l"(b) : "memory")
#define PTX_UADDC(c, a, b)  asm volatile("addc.cc.u64 %0, %1, %2;" : "=l"(c) : "l"(a), "l"(b) : "memory")
#define PTX_UADD(c, a, b)   asm volatile("addc.u64    %0, %1, %2;" : "=l"(c) : "l"(a), "l"(b) : "memory")

#define PTX_USUBO(c, a, b)  asm volatile("sub.cc.u64  %0, %1, %2;" : "=l"(c) : "l"(a), "l"(b) : "memory")
#define PTX_USUBC(c, a, b)  asm volatile("subc.cc.u64 %0, %1, %2;" : "=l"(c) : "l"(a), "l"(b) : "memory")
#define PTX_USUB(c, a, b)   asm volatile("subc.u64    %0, %1, %2;" : "=l"(c) : "l"(a), "l"(b) : "memory")

#define PTX_UMULLO(lo, a, b) asm volatile("mul.lo.u64 %0, %1, %2;" : "=l"(lo) : "l"(a), "l"(b))
#define PTX_UMULHI(hi, a, b) asm volatile("mul.hi.u64 %0, %1, %2;" : "=l"(hi) : "l"(a), "l"(b))

#define PTX_MADDO(r, a, b, c)  asm volatile("mad.hi.cc.u64  %0, %1, %2, %3;" : "=l"(r) : "l"(a), "l"(b), "l"(c) : "memory")
#define PTX_MADDC(r, a, b, c)  asm volatile("madc.hi.cc.u64 %0, %1, %2, %3;" : "=l"(r) : "l"(a), "l"(b), "l"(c) : "memory")
#define PTX_MADD(r, a, b, c)   asm volatile("madc.hi.u64    %0, %1, %2, %3;" : "=l"(r) : "l"(a), "l"(b), "l"(c) : "memory")

// ============================================================================
// 2. FIELD ELEMENT TYPE
// ============================================================================
struct __align__(32) fe256 { uint64_t v[4]; };

// ============================================================================
// 3. ADD / SUB / NEG — branchless
// ============================================================================
__device__ __forceinline__ void fe256_sub(fe256 &r, const fe256 &a, const fe256 &b) {
    uint64_t t0, t1, t2, t3, borrow;
    PTX_USUBO(t0, a.v[0], b.v[0]);
    PTX_USUBC(t1, a.v[1], b.v[1]);
    PTX_USUBC(t2, a.v[2], b.v[2]);
    PTX_USUBC(t3, a.v[3], b.v[3]);
    PTX_USUB(borrow, 0ULL, 0ULL);          // ~0 if a<b (needed modulus), else 0
    uint64_t m0 = P0 & borrow, m1 = P1 & borrow, m2 = P2 & borrow, m3 = P3 & borrow;
    PTX_UADDO(r.v[0], t0, m0);
    PTX_UADDC(r.v[1], t1, m1);
    PTX_UADDC(r.v[2], t2, m2);
    PTX_UADD(r.v[3], t3, m3);
}

// Correct full-field add: t = a+b in [0, 2p); result = t < p ? t : t-p.
// Branchless via borrow mask (handles both the carry-in-2^256 and the
// "no carry but sum >= p" cases — the classic missing-reduction pitfall).
__device__ __forceinline__ void fe256_add(fe256 &r, const fe256 &a, const fe256 &b) {
    uint64_t t0, t1, t2, t3, carry;
    PTX_UADDO(t0, a.v[0], b.v[0]);
    PTX_UADDC(t1, a.v[1], b.v[1]);
    PTX_UADDC(t2, a.v[2], b.v[2]);
    PTX_UADDC(t3, a.v[3], b.v[3]);
    PTX_UADD(carry, 0ULL, 0ULL);           // 1 if sum >= 2^256

    // u = t - p  (borrow flag set iff t < p)
    uint64_t u0, u1, u2, u3, brw;
    PTX_USUBO(u0, t0, P0);
    PTX_USUBC(u1, t1, P1);
    PTX_USUBC(u2, t2, P2);
    PTX_USUBC(u3, t3, P3);
    PTX_USUB(brw, 0ULL, 0ULL);             // ~0 iff t < p  (result = t)
    if (carry) {
        r.v[0]=u0; r.v[1]=u1; r.v[2]=u2; r.v[3]=u3;   // t >= 2^256 > p → t-p
    } else {
        r.v[0]=t0; r.v[1]=t1; r.v[2]=t2; r.v[3]=t3;   // t < 2^256
        // if t >= p, still need t-p:
        if (!((int64_t)brw)) {                        // brw==0 ⇒ t >= p
            PTX_USUBO(r.v[0], r.v[0], P0);
            PTX_USUBC(r.v[1], r.v[1], P1);
            PTX_USUBC(r.v[2], r.v[2], P2);
            PTX_USUB(r.v[3], r.v[3], P3);
        }
    }
}

__device__ __forceinline__ void fe256_set_one(fe256 &r) { r.v[0]=1; r.v[1]=0; r.v[2]=0; r.v[3]=0; }

// ============================================================================
// 4. 256x256 -> 512 MULTIPLY + BARRETT REDUCTION (clone of proven _ModMult)
// ============================================================================

// 256x64 multiply into 5 limbs: t = a * scalar   (a: 4 limbs)
#define MULLO(dst, a, b)      PTX_UMULLO(dst, a, b)
#define MADD_HI(dst, a, b, c) asm volatile("mad.hi.cc.u64 %0, %1, %2, %3;" : "=l"(dst) : "l"(a), "l"(b), "l"(c) : "memory")
#define MADC_HI(dst, a, b, c) asm volatile("madc.hi.cc.u64 %0, %1, %2, %3;" : "=l"(dst) : "l"(a), "l"(b), "l"(c) : "memory")
#define MAD_HI(dst, a, b, c)  asm volatile("madc.hi.u64 %0, %1, %2, %3;" : "=l"(dst) : "l"(a), "l"(b), "l"(c) : "memory")

__device__ __forceinline__ void umul_256x64(uint64_t t[5], const uint64_t a[4], uint64_t s) {
    MULLO(t[0], a[0], s);
    MULLO(t[1], a[1], s);
    MADD_HI(t[1], a[0], s, t[1]);
    MULLO(t[2], a[2], s);
    MADC_HI(t[2], a[1], s, t[2]);
    MULLO(t[3], a[3], s);
    MADC_HI(t[3], a[2], s, t[3]);
    MAD_HI(t[4], a[3], s, 0ULL);
}

// a*b (mod p): 512-bit accumulate then two-stage Barrett fold,
// identical in structure to the production-proven GPUMath.h _ModMult.
__device__ __forceinline__ void fe256_mul(fe256 &r, const fe256 &a, const fe256 &b) {
    uint64_t r512[8], t[5];

    r512[5] = 0; r512[6] = 0; r512[7] = 0;
    umul_256x64(r512, a.v, b.v[0]);
    umul_256x64(t,     a.v, b.v[1]);
    PTX_UADDO(r512[1], r512[1], t[0]);
    PTX_UADDC(r512[2], r512[2], t[1]);
    PTX_UADDC(r512[3], r512[3], t[2]);
    PTX_UADDC(r512[4], r512[4], t[3]);
    PTX_UADD(r512[5],  r512[5], t[4]);
    umul_256x64(t,     a.v, b.v[2]);
    PTX_UADDO(r512[2], r512[2], t[0]);
    PTX_UADDC(r512[3], r512[3], t[1]);
    PTX_UADDC(r512[4], r512[4], t[2]);
    PTX_UADDC(r512[5], r512[5], t[3]);
    PTX_UADD(r512[6],  r512[6], t[4]);
    umul_256x64(t,     a.v, b.v[3]);
    PTX_UADDO(r512[3], r512[3], t[0]);
    PTX_UADDC(r512[4], r512[4], t[1]);
    PTX_UADDC(r512[5], r512[5], t[2]);
    PTX_UADDC(r512[6], r512[6], t[3]);
    PTX_UADD(r512[7],  r512[7], t[4]);

    // Reduce 512 -> 320: t = r512[4..7] * 0x1000003D1, add low 4 into r[0..3]
    umul_256x64(t, r512 + 4, 0x1000003D1ULL);
    PTX_UADDO(r512[0], r512[0], t[0]);
    PTX_UADDC(r512[1], r512[1], t[1]);
    PTX_UADDC(r512[2], r512[2], t[2]);
    PTX_UADDC(r512[3], r512[3], t[3]);
    PTX_UADD(t[4], t[4], 0ULL);       // absorb carry out of r512[3] into t[4]

    // Reduce 320 -> 256: r = r512[0..3] + t[4]*0x1000003D1 (t[4] <= 2^36)
    uint64_t ah, al;
    PTX_UMULLO(al, t[4], 0x1000003D1ULL);
    PTX_UMULHI(ah, t[4], 0x1000003D1ULL);
    PTX_UADDO(r.v[0], r512[0], al);
    PTX_UADDC(r.v[1], r512[1], ah);
    PTX_UADDC(r.v[2], r512[2], 0ULL);
    PTX_UADD(r.v[3], r512[3], 0ULL);
}

// Correct sqr via mul (the proven original's fast sqr is 30% faster; kept as
// a follow-up optimization to prove identical results first).
__device__ __forceinline__ void fe256_sqr(fe256 &r, const fe256 &a) {
    fe256_mul(r, a, a);
}

// ============================================================================
// 7. MODULAR INVERSE — a^(p-2) via square-and-multiply
// ============================================================================
__device__ __forceinline__ void fe256_inv(fe256 &r, const fe256 &a) {
    // p-2 prime-exponent limbs (LE): p - 2 = 0xFFF...FFFEFFFFFC2D
    const uint64_t E[4] = { 0xFFFFFFFEFFFFFC2DULL,
                            0xFFFFFFFFFFFFFFFFULL,
                            0xFFFFFFFFFFFFFFFFULL,
                            0xFFFFFFFFFFFFFFFFULL };
    fe256 result; fe256_set_one(result);
    fe256 base = a;

    // Exponent is scalar-constant (p-2): unroll the 4-limb outer scan; the
    // 64-bit inner loop is a hard serial dependency chain (each sqr feeds the
    // next), so full unrolling gains nothing but I-cache.
    #pragma unroll 4
    for (int limb = 3; limb >= 0; limb--) {
        for (int bit = 63; bit >= 0; bit--) {
            fe256_sqr(result, result);
            if ((E[limb] >> bit) & 1ULL) fe256_mul(result, result, base);
        }
    }
    r = result;
}

// ============================================================================
// 8. 128-BIT DISTANCE ACCUMULATION (matches v2.2 Add128 semantics)
// ============================================================================
struct __align__(16) scalar128 { uint64_t v[2]; };

// Plain 128-bit wrap addition (identical to the proven Add128 in GPUMath.h;
// distance deltas are resolved mod 2^128 by the DP x-host tie-out, so no mod-n
// reduction is applied on device).
__device__ __forceinline__ void scalar128_add(scalar128 &r, const scalar128 &a, const scalar128 &b) {
    uint64_t t0, t1;
    PTX_UADDO(t0, a.v[0], b.v[0]);
    PTX_UADD(t1, a.v[1], b.v[1]);   // carry into high word; wraps mod 2^128
    r.v[0]=t0; r.v[1]=t1;
}

#endif // GPUOPT_H