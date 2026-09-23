// simd_main.cpp — Phase 3: SIMD-verified field ops for the toy field p=2^32-1119.
// Lanes are stored as 64-bit values in [0,P); kernels operate on __m256i of 4 lanes
// per vector (256-bit). add/sub/mul each validated against scalar reference.
// Output rows: op,scalar_ns,avx2_4lane_ns,speedup,valid
#include <cstdio>
#include <cstdint>
#include <chrono>
#include <random>
#include <immintrin.h>
#include "instance.hpp"

static const uint64_t P = TOY_P;          // 4294966177 = 2^32 - 1119
static const uint64_t FOLD = 1119;
static const uint64_t M32 = 0xFFFFFFFFull;

static inline uint64_t now_ns() {
    using namespace std::chrono;
    return duration_cast<nanoseconds>(steady_clock::now().time_since_epoch()).count();
}

// ---------- scalar reference (exact) ----------
static inline uint64_t s_add(uint64_t a, uint64_t b) {
    uint64_t t = a + b;
    return t >= P ? t - P : t;
}
static inline uint64_t s_sub(uint64_t a, uint64_t b) {
    int64_t t = (int64_t)a - b;
    return (uint64_t)(t < 0 ? t + (int64_t)P : t);
}
static inline uint64_t s_mul(uint64_t a, uint64_t b) {
    uint64_t t = a * b;
    uint64_t lo = t & M32;
    uint64_t hi = t >> 32;
    uint64_t r = lo + hi * FOLD;
    uint64_t lo2 = r & M32;
    uint64_t hi2 = r >> 32;
    r = lo2 + hi2 * FOLD;
    if (r >= P) r -= P;
    return r;
}

// ---------- AVX2 4-lane kernels (64-bit lanes) ----------
static inline __m256i v_add(__m256i a, __m256i b) {
    __m256i s = _mm256_add_epi64(a, b);
    __m256i p = _mm256_set1_epi64x((long long)P);
    __m256i ge = _mm256_cmpgt_epi64(_mm256_sub_epi64(s, p), _mm256_set1_epi64x(-1)); // s >= P
    return _mm256_blendv_epi8(s, _mm256_sub_epi64(s, p), ge);
}
static inline __m256i v_sub(__m256i a, __m256i b) {
    __m256i d = _mm256_sub_epi64(a, b);
    __m256i p = _mm256_set1_epi64x((long long)P);
    __m256i lt = _mm256_cmpgt_epi64(_mm256_setzero_si256(), d); // 0 > d
    return _mm256_blendv_epi8(d, _mm256_add_epi64(d, p), lt);   // select d+p when negative
}
static inline __m256i v_mul(__m256i a, __m256i b) {
    __m256i m64 = _mm256_set1_epi64x((long long)M32);
    __m256i lo = _mm256_mul_epu32(a, b);          // 4 low products in qword lanes
    __m256i hi_a = _mm256_srli_epi64(a, 32);
    __m256i hi_b = _mm256_srli_epi64(b, 32);
    __m256i hi_hi = _mm256_mul_epu32(hi_a, hi_b); // 4 high products
    __m256i lo_hi = _mm256_mul_epu32(a, hi_b);
    __m256i hi_lo = _mm256_mul_epu32(hi_a, b);
    __m256i t = _mm256_add_epi64(_mm256_add_epi64(lo, hi_hi),
                _mm256_slli_epi64(_mm256_add_epi64(lo_hi, hi_lo), 32)); // 64-bit products
    // fold: r = low32 + high32*FOLD
    __m256i lo32 = _mm256_and_si256(t, m64);
    __m256i hi32 = _mm256_srli_epi64(t, 32);
    __m256i r = _mm256_add_epi64(lo32, _mm256_mul_epu32(hi32, _mm256_set1_epi64x((long long)FOLD)));
    __m256i lo32b = _mm256_and_si256(r, m64);
    __m256i hi32b = _mm256_srli_epi64(r, 32);
    __m256i r2 = _mm256_add_epi64(lo32b, _mm256_mul_epu32(hi32b, _mm256_set1_epi64x((long long)FOLD)));
    // r2 < P + 2^21 < 2^33: one unsigned compare handles it (all positive)
    __m256i p = _mm256_set1_epi64x((long long)P);
    __m256i ge = _mm256_cmpgt_epi64(_mm256_sub_epi64(r2, p), _mm256_set1_epi64x(-1));
    return _mm256_and_si256(_mm256_blendv_epi8(r2, _mm256_sub_epi64(r2, p), ge), m64);
}

int main() {
    std::mt19937 rng(2026);
    alignas(32) uint64_t A[4], B[4], R[4];
    bool val_add = true, val_sub = true, val_mul = true;
    for (int t = 0; t < 400000; t++) {
        for (int i = 0; i < 4; i++) { A[i] = (uint64_t)rng() % P; B[i] = (uint64_t)rng() % P; R[i] = 0; }
        __m256i va = _mm256_loadu_si256((const __m256i*)A);
        __m256i vb = _mm256_loadu_si256((const __m256i*)B);
        __m256i ra = v_add(va, vb);
        _mm256_storeu_si256((__m256i*)R, ra);
        for (int i = 0; i < 4; i++) if (R[i] != s_add(A[i], B[i])) val_add = false;
        ra = v_sub(va, vb);
        _mm256_storeu_si256((__m256i*)R, ra);
        for (int i = 0; i < 4; i++) if (R[i] != s_sub(A[i], B[i])) val_sub = false;
        ra = v_mul(va, vb);
        _mm256_storeu_si256((__m256i*)R, ra);
        for (int i = 0; i < 4; i++) if (R[i] != s_mul(A[i], B[i])) val_mul = false;
    }
    printf("// simd validation add=%s sub=%s mul=%s\n",
           val_add ? "OK" : "FAIL", val_sub ? "OK" : "FAIL", val_mul ? "OK" : "FAIL");

    double best[6] = {1e18,1e18,1e18,1e18,1e18,1e18};
    const uint64_t NN = 6000000;
    const uint64_t NV = NN / 4;
    alignas(32) uint64_t SA[260], SB[260];
    for (int i = 0; i < 260; i++) { SA[i] = (uint64_t)rng() % P; SB[i] = (uint64_t)rng() % P; }
    for (int rep = 0; rep < 7; rep++) {
        volatile uint64_t sink = 0;
        uint64_t t0 = now_ns();
        for (uint64_t i = 0; i < NN; i++) sink ^= s_add(SA[i & 255], SB[i & 255]);
        uint64_t t1 = now_ns();
        double per = (double)(t1 - t0) / NN; if (per < best[0]) best[0] = per; (void)sink;
        t0 = now_ns();
        for (uint64_t i = 0; i < NN; i++) sink ^= s_sub(SA[i & 255], SB[i & 255]);
        t1 = now_ns(); per = (double)(t1 - t0) / NN; if (per < best[1]) best[1] = per; (void)sink;
        t0 = now_ns();
        for (uint64_t i = 0; i < NN; i++) sink ^= s_mul(SA[i & 255], SB[i & 255]);
        t1 = now_ns(); per = (double)(t1 - t0) / NN; if (per < best[2]) best[2] = per; (void)sink;
        // SIMD: load contiguous 4-lane blocks in round-robin (i&255 indexing => hoisting-resistant,
        // same memory pattern as the scalar loops)
        t0 = now_ns();
        __m256i acc = _mm256_setzero_si256();
        for (uint64_t i = 0; i < NV; i++) {
            const uint64_t j = i & 255;
            __m256i va = _mm256_loadu_si256((const __m256i*)&SA[j]);
            __m256i vb = _mm256_loadu_si256((const __m256i*)&SB[j]);
            acc = _mm256_xor_si256(acc, v_add(va, vb));
        }
        t1 = now_ns(); per = (double)(t1 - t0) / (NV * 4); if (per < best[3]) best[3] = per;
        _mm256_storeu_si256((__m256i*)SA, acc); (void)acc;
        t0 = now_ns();
        acc = _mm256_setzero_si256();
        for (uint64_t i = 0; i < NV; i++) {
            const uint64_t j = i & 255;
            __m256i va = _mm256_loadu_si256((const __m256i*)&SA[j]);
            __m256i vb = _mm256_loadu_si256((const __m256i*)&SB[j]);
            acc = _mm256_xor_si256(acc, v_sub(va, vb));
        }
        t1 = now_ns(); per = (double)(t1 - t0) / (NV * 4); if (per < best[4]) best[4] = per;
        _mm256_storeu_si256((__m256i*)SA, acc); (void)acc;
        t0 = now_ns();
        acc = _mm256_setzero_si256();
        for (uint64_t i = 0; i < NV; i++) {
            const uint64_t j = i & 255;
            __m256i va = _mm256_loadu_si256((const __m256i*)&SA[j]);
            __m256i vb = _mm256_loadu_si256((const __m256i*)&SB[j]);
            acc = _mm256_xor_si256(acc, v_mul(va, vb));
        }
        t1 = now_ns(); per = (double)(t1 - t0) / (NV * 4); if (per < best[5]) best[5] = per;
        _mm256_storeu_si256((__m256i*)SA, acc); (void)acc;
    }
    printf("op,scalar_ns,avx2_4lane_ns,speedup,valid\n");
    printf("add,%.4f,%.4f,%.3f,%s\n", best[0], best[3], best[0] / best[3], val_add ? "YES" : "NO");
    printf("sub,%.4f,%.4f,%.3f,%s\n", best[1], best[4], best[1] / best[4], val_sub ? "YES" : "NO");
    printf("mul,%.4f,%.4f,%.3f,%s\n", best[2], best[5], best[2] / best[5], val_mul ? "YES" : "NO");
    return 0;
}