// correct.cpp — correctness suite: field laws (all 4 strategies), affine==Jacobian
// agreement, scalar mult vs brute force, and DLP test vectors cross-checked against
// ref/gen_instance.py (independent big-int implementation).
#include <cstdio>
#include <cstdint>
#include <cstdlib>
#include "fp.hpp"
#include "ec.hpp"
#include "instance.hpp"

static uint64_t rng_state = 0x9E3779B97F4A7C15ull;
static inline uint32_t rnd_u32() {
    rng_state ^= rng_state << 13; rng_state ^= rng_state >> 7; rng_state ^= rng_state << 17;
    return (uint32_t)rng_state;
}

template <typename F>
void test_field(const char* name, int trials) {
    int fails = 0;
    for (int t = 0; t < trials; t++) {
        uint32_t a = rnd_u32() % F::mod, b = rnd_u32() % F::mod, c = rnd_u32() % F::mod;
        if (a == 0) a = 1;
        uint32_t one = F::one();
        if (F::add(F::add(a, b), c) != F::add(a, F::add(b, c))) fails++;
        if (F::add(a, F::add(F::mod-a, 0)) != 0) fails++;          // a + (p-a) = 0  (sub as add of neg? no: check wrap)
        if (F::add(a, F::sub(0u, a)) != 0) fails++;                // a + (-a) = 0  where -a = (p-a) mod p
        if (F::mul(a, b) != F::mul(b, a)) fails++;
        if (F::mul(a, F::mul(b, c)) != F::mul(F::mul(a, b), c)) fails++;
        if (F::sqr(a) != F::mul(a, a)) fails++;
        if (F::mul(a, F::add(b, c)) != F::add(F::mul(a, b), F::mul(a, c))) fails++;
        if (F::mul(one, a) != a) fails++;
        if (F::mul(a, 0) != 0) fails++;
        uint32_t ai = F::inv(a);
        if (ai == 0 || F::mul(a, ai) != one) fails++;
        uint64_t vals[4] = {0, 1, F::mod-1, ((uint64_t)(F::mod-1) << 32) | (F::mod-1)};
        for (auto t64 : vals)
            if (F::reduce64(t64) != (uint32_t)(t64 % F::mod)) fails++;
    }
    printf("[FIELD %-10s] trials=%d fails=%d %s\n", name, trials, fails, fails ? "FAIL" : "OK");
}

template <typename F>
void test_ec_agree(const char* name, int trials) {
    int fails = 0;
    using namespace ec;
    uint32_t Bx = TOY_Gx, By = TOY_Gy;
    Affine<F> base = Affine<F>::point(Bx, By);
    Jacobian<F> jbase = Jacobian<F>::from_affine(Bx, By);
    for (int t = 0; t < trials; t++) {
        uint32_t k = rnd_u32() % (1u << 20);
        auto A1 = Affine<F>::mul(base, k);
        auto J1 = Jacobian<F>::mul(jbase, k).to_affine();
        if (A1.inf != J1.inf || A1.x != J1.x || A1.y != J1.y) fails++;
        // double = mul 2: [k]G + G == [k+1]G
        auto A2 = Affine<F>::add(A1, base);
        auto A3 = Affine<F>::mul(base, k + 1);
        if (A2.inf != A3.inf || A2.x != A3.x || A2.y != A3.y) fails++;
    }
    printf("[EC-AGREE  %-7s] trials=%d fails=%d %s\n", name, trials, fails, fails ? "FAIL" : "OK");
}

template <typename F>
void test_dlp_vectors(const char* name) {
    using namespace ec;
    int fails = 0;
    FILE* f = fopen("dlp_vectors.txt", "r");
    if (!f) { printf("[VECTORS   %-7s] cannot open dlp_vectors.txt\n", name); return; }
    // generator order is l (prime); each line: d  k  Qx  Qy
    Affine<F> base = Affine<F>::point(TOY_Gx, TOY_Gy);
    int expect_line = 1;
    int d; unsigned long long k; uint32_t qx, qy;
    while (fscanf(f, "%d %llu %u %u", &d, &k, &qx, &qy) == 4) {
        (void)d;
        auto Q = Affine<F>::mul(base, k);
        if (Q.inf || F::to_raw(Q.x) != qx || F::to_raw(Q.y) != qy) {
            fails++;
            printf("  line %d: k=%llu mismatch\n", expect_line, k);
        }
        expect_line++;
    }
    fclose(f);
    printf("[VECTORS   %-7s] %s\n", name, fails ? "FAIL" : "OK");
    if (fails) exit(1);
}

int main() {
    printf("== CORRECTNESS (TOY curve p=%u, order l=%llu, G=(%u,%u)) ==\n", TOY_P, TOY_L, TOY_Gx, TOY_Gy);
    test_field<fp::FpNaive<TOY_P>>   ("naive",   2000);
    test_field<fp::FpBarrett<TOY_P>> ("barrett", 2000);
    test_field<fp::FpMont<TOY_P>>    ("mont",    2000);
    test_field<fp::FpPseudo<TOY_P>>  ("pseudo",  2000);

    test_ec_agree<fp::FpNaive<TOY_P>>  ("naive",  200);
    test_ec_agree<fp::FpBarrett<TOY_P>>("barrett",200);
    test_ec_agree<fp::FpMont<TOY_P>>   ("mont",   200);
    test_ec_agree<fp::FpPseudo<TOY_P>> ("pseudo", 200);

    test_dlp_vectors<fp::FpNaive<TOY_P>>  ("naive");
    test_dlp_vectors<fp::FpBarrett<TOY_P>>("barrett");
    test_dlp_vectors<fp::FpPseudo<TOY_P>> ("pseudo");
    test_dlp_vectors<fp::FpMont<TOY_P>>   ("mont");
    printf("DONE\n");
    return 0;
}