// micro_main.cpp — Phase 1: honest microbenchmarks of field ops & EC formulas.
// CSV lines: KIND,strategy,op,ns_per_op   (compile per flag set)
#include <cstdio>
#include <cstdint>
#include <chrono>
#include <random>
#include "instance.hpp"
#include "src/fp.hpp"
#include "src/ec.hpp"

static inline uint64_t now_ns() {
    using namespace std::chrono;
    return duration_cast<nanoseconds>(steady_clock::now().time_since_epoch()).count();
}

template <typename F, typename FN>
double measure(unsigned reps, size_t N, FN fn, typename F::Elem a[256], typename F::Elem b[256], typename F::Elem c[256]) {
    double best = 1e18;
    for (unsigned r = 0; r < reps; r++) {
        volatile typename F::Elem sink = 0;
        size_t i = 0;
        uint64_t t0 = now_ns();
        for (uint64_t it = 0; it < N; it++) {
            sink ^= fn(a[i & 255], b[i & 255], c[i & 255]);
            i++;
        }
        uint64_t t1 = now_ns();
        double per = (double)(t1 - t0) / N;
        if (per < best) best = per;
        (void)sink;
    }
    return best;
}

template <typename F>
void bench_field(const char* which) {
    typedef typename F::Elem E;
    const size_t N = 10000000;
    E a[256], b[256], c[256];
    std::mt19937 rng(42);
    for (int i=0;i<256;i++){ a[i]=(uint32_t)rng() % E(F::mod); b[i]=(uint32_t)rng() % E(F::mod); c[i]=0; }
    auto fn_add = [](E x, E y, E& z)->E { z = F::add(x,y); return z; };
    auto fn_sub = [](E x, E y, E& z)->E { z = F::sub(x,y); return z; };
    auto fn_mul = [](E x, E y, E& z)->E { z = F::mul(x,y); return z; };
    auto fn_sqr = [](E x, E y, E& z)->E { z = F::sqr(x); return z; };
    auto fn_inv = [](E x, E y, E& z)->E { z = F::inv(x); return z; };
    printf("FIELD,%s,add,%.3f\n", which, measure<F>(5, N, fn_add, a, b, c));
    printf("FIELD,%s,sub,%.3f\n", which, measure<F>(5, N, fn_sub, a, b, c));
    printf("FIELD,%s,mul,%.3f\n", which, measure<F>(5, N, fn_mul, a, b, c));
    printf("FIELD,%s,sqr,%.3f\n", which, measure<F>(5, N, fn_sqr, a, b, c));
    printf("FIELD,%s,inv,%.3f\n", which, measure<F>(3, N/40, fn_inv, a, b, c));
}

template <typename F>
void bench_ec(const char* which) {
    typedef typename F::Elem E;
    using A = ec::Affine<F>;
    using J = ec::Jacobian<F>;
    const size_t N = 3000000;
    A base = A::point(TOY_Gx, TOY_Gy);
    J jbase = J::from_affine(TOY_Gx, TOY_Gy);
    E a[256], b[256], c[256];
    {   // affine double
        A r = base;
        auto fn = [&](E, E, E& z)->E { r = A::dbl(r); z = (uint32_t)r.x; return z; };
        printf("EC,%s,affine_dbl,%.3f\n", which, measure<F>(3, N, fn, a, b, c));
    }
    {   // affine add
        A r = base;
        auto fn = [&](E, E, E& z)->E { r = A::add(r, base); z = (uint32_t)r.x; return z; };
        printf("EC,%s,affine_add,%.3f\n", which, measure<F>(3, N, fn, a, b, c));
    }
    {   // jacobian double
        J r = jbase;
        auto fn = [&](E, E, E& z)->E { r = J::dbl(r); z = (uint32_t)r.X; return z; };
        printf("EC,%s,jacobian_dbl,%.3f\n", which, measure<F>(3, N, fn, a, b, c));
    }
    {   // jacobian mixed add (Z2=1)
        J r = jbase;
        auto fn = [&](E, E, E& z)->E { r = J::add_affine(r, base); z = (uint32_t)r.X; return z; };
        printf("EC,%s,jacobian_mixed_add,%.3f\n", which, measure<F>(3, N, fn, a, b, c));
    }
    {   // full jacobian add (distinct points, r + other walk)
        J r = jbase, s = J::dbl(jbase);
        auto fn = [&](E, E, E& z)->E { J nr = J::add(r, s); r = nr; z = (uint32_t)r.X; return z; };
        printf("EC,%s,jacobian_add,%.3f\n", which, measure<F>(3, N, fn, a, b, c));
    }
}

int main() {
    bench_field<fp::FpNaive<TOY_P>>("naive");
    bench_field<fp::FpBarrett<TOY_P>>("barrett");
    bench_field<fp::FpMont<TOY_P>>("mont");
    bench_field<fp::FpPseudo<TOY_P>>("pseudo");
    bench_ec<fp::FpNaive<TOY_P>>("naive");
    bench_ec<fp::FpBarrett<TOY_P>>("barrett");
    bench_ec<fp::FpMont<TOY_P>>("mont");
    bench_ec<fp::FpPseudo<TOY_P>>("pseudo");
    return 0;
}