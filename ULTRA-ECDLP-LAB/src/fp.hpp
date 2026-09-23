// fp.hpp — fixed-modulus field arithmetic for toy-ECDLP research (p <= 2^32)
// Four honest reduction strategies for one 64-bit product:
//   naive   : uint64 % P  (GCC emits multiply-magic for constant P)          [baseline]
//   barrett : q = (t*mu)>>64, r = t - q*P, 1-2 corrections                  [division-free]
//   mont    : Montgomery radix 2^32 (n0 = -P^-1 mod 2^32), product in mont  [division-free]
//   pseudo  : specialized P = 2^32 - c pseudo-Mersenne fold                 [worst-case best for these P]
// Correctness cross-checked against Python in ref/.
#pragma once
#include <cstdint>
#include <cstddef>
#include <type_traits>

namespace fp {

constexpr uint32_t P_32m5  = 4294967291u;   // 2^32 - 5,   prime
constexpr uint32_t P_32m99 = 4294967197u;   // 2^32 - 99,  prime, p = 1 (mod 3) -> endomorphism lives

// ---- helpers ---------------------------------------------------------------
// modular inverse mod m, 1 < m <= 2^32, m odd, a < m (Euclid)
static inline constexpr uint32_t inv_mod_u32(uint32_t a, uint32_t m) {
    int64_t t = 0, newt = 1;
    int64_t r = m, newr = a;
    while (newr != 0) {
        int64_t q = r / newr;
        int64_t tmp = t - q * newt;  t = newt;  newt = tmp;
        tmp = r - q * newr;  r = newr;  newr = tmp;
    }
    if (r > 1) return 0;
    if (t < 0) t += m;
    return (uint32_t)t;
}

// inverse mod 2^32 of an odd a (Newton-Hensel: correct bits double per step)
static inline constexpr uint32_t inv_mod_2e32(uint32_t a) {
    uint64_t x = 1;                 // a*1 = a ≡ 1 (mod 2) for a odd
    for (int i = 0; i < 5; i++)     // 1 -> 2 -> 4 -> 8 -> 16 -> 32 bits
        x = x * (2 - a * x);
    return (uint32_t)x;             // exact mod 2^32
}

// ---- naive : % P ------------------------------------------------------------
template <uint32_t P>
struct FpNaive {
    static constexpr uint32_t mod = P;
    using Elem = uint32_t;
    static inline Elem add(Elem a, Elem b) { uint64_t s = (uint64_t)a + b; return (s >= P) ? (Elem)(s - P) : (Elem)s; }
    static inline Elem sub(Elem a, Elem b) { return (a >= b) ? a - b : (Elem)((uint64_t)a + P - b); }
    static inline Elem mul(Elem a, Elem b) { return (Elem)(((uint64_t)a * b) % P); }
    static inline Elem sqr(Elem a)         { return (Elem)(((uint64_t)a * a) % P); }
    static inline Elem reduce64(uint64_t t){ return (Elem)(t % P); }
    static inline Elem inv(Elem a)         { return inv_mod_u32(a, P); }
    static inline Elem one() { return 1; }
    static inline Elem zero(){ return 0; }
    static inline Elem from_raw(Elem x){ return x % P; }
    static inline Elem to_raw(Elem x){ return x % P; }
};

// ---- barrett ----------------------------------------------------------------
template <uint32_t P>
struct FpBarrett {
    static constexpr uint32_t mod = P;
    using Elem = uint32_t;
    // mu = floor(2^64 / P),  fits u64 ( < 2^33 )
    static constexpr uint64_t mu = ((uint64_t)(~0ull) / P);
    static inline Elem add(Elem a, Elem b) { uint64_t s = (uint64_t)a + b; return (s >= P) ? (Elem)(s - P) : (Elem)s; }
    static inline Elem sub(Elem a, Elem b) { return (a >= b) ? a - b : (Elem)((uint64_t)a + P - b); }
    static inline Elem reduce64(uint64_t t) {
        // t < P^2 < 2^64 ; q = floor(t*mu / 2^64) = floor(t/P) +/- 1
        uint64_t q = (uint64_t)(((unsigned __int128)t * mu) >> 64);
        uint64_t r = t - q * P;
        if (r >= P) r -= P;
        if (r >= P) r -= P;
        return (Elem)r;
    }
    static inline Elem mul(Elem a, Elem b) { return reduce64((uint64_t)a * b); }
    static inline Elem sqr(Elem a)         { return reduce64((uint64_t)a * a); }
    static inline Elem inv(Elem a)         { return inv_mod_u32(a, P); }
    static inline Elem one(){ return 1; } static inline Elem zero(){ return 0; }
    static inline Elem from_raw(Elem x){ return x % P; }
    static inline Elem to_raw(Elem x){ return x % P; }
};

// ---- Montgomery (radix 2^32) -------------------------------------------------
template <uint32_t P>
struct FpMont {
    static constexpr uint32_t mod = P;
    using Elem = uint32_t;                       // stored in Montgomery form: x*R mod P, R = 2^32
    static constexpr uint32_t n0   = (uint32_t)(0u - inv_mod_2e32(P)); // -P^-1 mod 2^32
    static constexpr uint32_t R    = (uint32_t)(0x100000000ull % P);   // R mod P = mont(1)
    static constexpr uint32_t R2   = (uint32_t)(((uint64_t)R * R) % P);
    static inline Elem to_mont(Elem x) { return mul(x, R2); }
    static inline Elem from_mont(Elem x){ return mul(x, 1); }          // *R^-1
    static inline Elem mul(Elem a, Elem b) {
        uint64_t t   = (uint64_t)a * b;               // t = a*b < P^2
        uint32_t m   = (uint32_t)(((uint64_t)(uint32_t)t * n0) & 0xffffffffu);
        uint64_t hi  = (uint64_t)(((unsigned __int128)t + (uint64_t)m * P) >> 32);
        return (hi >= P) ? (Elem)(hi - P) : (Elem)hi;
    }
    static inline Elem sqr(Elem a) { return mul(a, a); }
    // reduce64: TRUE reduction t mod P for arbitrary 64-bit t (division-free Barrett;
    // used by correctness tests / conversions, not by the mul hot path)
    static constexpr uint64_t mu64 = (~0ull) / P;
    static inline Elem reduce64(uint64_t t) {
        uint64_t q = (uint64_t)(((unsigned __int128)t * mu64) >> 64);
        uint64_t r = t - q * P;
        if (r >= P) r -= P;
        if (r >= P) r -= P;
        return (Elem)r;
    }
    static inline Elem add(Elem a, Elem b) { uint64_t s = (uint64_t)a + b; return (s >= P) ? (Elem)(s - P) : (Elem)s; }
    static inline Elem sub(Elem a, Elem b) { return (a >= b) ? a - b : (Elem)((uint64_t)a + P - b); }
    static inline Elem inv(Elem a) {
        // montgomery inverse via binary xgcd then to-mont
        return to_mont(inv_mod_u32(from_mont(a), P));
    }
    static inline Elem one(){ return R; }           // 1 * R  (Montgomery form of 1)
    static inline Elem zero(){ return 0; }
    static inline Elem from_raw(Elem x){ return to_mont(x % P); }
    static inline Elem to_raw(Elem x){ return from_mont(x); }
};

// ---- pseudo-Mersenne P = 2^32 - c -------------------------------------------
template <uint32_t P>
struct FpPseudo {
    static constexpr uint32_t mod = P;
    using Elem = uint32_t;
    static constexpr uint32_t c = (uint32_t)((uint64_t)0x100000000ull - P); // few bits
    static inline Elem add(Elem a, Elem b) { uint64_t s = (uint64_t)a + b; return (s >= P) ? (Elem)(s - P) : (Elem)s; }
    static inline Elem sub(Elem a, Elem b) { return (a >= b) ? a - b : (Elem)((uint64_t)a + P - b); }
    static inline Elem reduce64(uint64_t t) {
        // t = hi*2^32 + lo ; 2^32 == c (mod P)
        uint64_t r = ((uint64_t)(uint32_t)(t >> 32)) * c + (uint32_t)t;   // < c*2^32 + 2^32
        r = ((r >> 32) * c) + (uint32_t)r;                                 // < c^2 + 2^32
        // r < 2^32 + c^2 ; fold may still exceed P by a few
        if (r >= P) r -= P;
        if (r >= P) r -= P;
        if (r >= P) r -= P;                                                 // safe bound: r < P + c^2, c<64 => <= 3 folds
        return (uint32_t)r;
    }
    static inline Elem mul(Elem a, Elem b) { return reduce64((uint64_t)a * b); }
    static inline Elem sqr(Elem a)         { return reduce64((uint64_t)a * a); }
    static inline Elem inv(Elem a)         { return inv_mod_u32(a, P); }
    static inline Elem one(){ return 1; } static inline Elem zero(){ return 0; }
    static inline Elem from_raw(Elem x){ return x % P; }
    static inline Elem to_raw(Elem x){ return x % P; }
};

// ---- binary extended-gcd inverse (division-free, used by EC affine later) ----
static inline uint32_t inv_binary(uint32_t a, uint32_t m) {
    // Stein binary xgcd: returns a^-1 (mod m), m odd
    int64_t u = a, v = m, A = 1, B = 0;
    while (u != 0) {
        while (!(u & 1)) { u >>= 1; if (!(A & 1)) A >>= 1; else A = (A + m) >> 1; }
        while (!(v & 1)) { v >>= 1; if (!(B & 1)) B >>= 1; else B = (B + m) >> 1; }
        if (u >= v) { u -= v; A -= B; } else { v -= u; B -= A; }
    }
    if (B < 0) B += m;
    return (uint32_t)B;
}

} // namespace fp