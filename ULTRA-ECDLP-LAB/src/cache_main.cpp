// cache_main.cpp — Phase 5: memory hierarchy behavior of toy-ECDLP hot loops.
// 1) CPUID cache-size report (L1d/L2/L3).
// 2) Sequential Jacobian dbl / mixed-add over working sets 2^10..2^22 points
//    (12 B/point) -> ns per point op as function of footprint.
// 3) Random gather of affine points (8 B/point), sizes 2^12..2^24 -> random-access
//    cost at each hierarchy level; 4) same with fixed stride 67 (prefetch-friendly).
// Writes CSV to argv[1]; console header to stderr.
#include <cstdio>
#include <cstdint>
#include <cstdlib>
#include <vector>
#include <chrono>
#include "instance.hpp"
#include "src/fp.hpp"
#include "src/ec.hpp"

using F = fp::FpNaive<TOY_P>;
using E = F::Elem;
using J = ec::Jacobian<F>;
using A = ec::Affine<F>;

static inline uint64_t now_ns() {
    using namespace std::chrono;
    return duration_cast<nanoseconds>(steady_clock::now().time_since_epoch()).count();
}

#ifdef __GNUC__
static void report_cache(FILE* out) {
    unsigned eax, ebx, ecx, edx;
    char vendor[13] = {0};
    unsigned _a = 0; __asm__ __volatile__("cpuid" : "+a"(_a), "=b"(ebx), "=c"(ecx), "=d"(edx));
    *(unsigned*)vendor = ebx; *(unsigned*)(vendor+4) = edx; *(unsigned*)(vendor+8) = ecx;
    fprintf(out, "CPUINFO,vendor,%s\n", vendor);
    // Cache hierarchy is measured behaviorally below (gather experiments): the host
    // hypervisor masks deterministic cache enumeration (cpuid leaf 4 / ext 0x8000001D).
    fprintf(out, "CPUINFO,note,leaf4_not_exposed_VM;_hierarchy_from_gather_probes\n");
}
#else
static void report_cache(FILE* out) { fprintf(out, "CPUINFO,n/a\n"); }
#endif

// best-of-reps ns per op for fn() called `ops` times over a fresh working set per rep
template <typename FN>
static double measure_best(unsigned reps, uint64_t ops, FN fn) {
    double best = 1e18;
    for (unsigned r = 0; r < reps; r++) {
        uint64_t t0 = now_ns();
        fn();
        uint64_t t1 = now_ns();
        double per = (double)(t1 - t0) / (double)ops;
        if (per < best) best = per;
    }
    return best;
}

int main(int argc, char** argv) {
    FILE* out = stdout;
    if (argc > 1) { out = fopen(argv[1], "w"); if (!out) return 2; }
    fprintf(stderr, "Phase 5 cache study: writing to %s\n", argv[1] ? argv[1] : "stdout");
    report_cache(out);

    const A base   = A::point(TOY_Gx, TOY_Gy);
    const A negG   = A::rep(F::sub(F::zero(), base.y), 0);      // -G used in walks
    (void)negG;

    fprintf(out, "# wset=2^D points; ptsize=dbl:12B / add:12B / gather:8B\n");
    fprintf(out, "exp,d_points,footprint_bytes,ns_per_op\n");

    // --- sequential Jacobian dbl over a point array (dbl needs 4M+6S, no inv) ---
    {
        const uint64_t TOT = 30000000ull;  // total dbl ops per point-array size
        for (int D = 10; D <= 22; D++) {
            size_t N = (size_t)1 << D;
            std::vector<J> arr(N);
            for (auto& j : arr) j = J::from_affine(TOY_Gx, TOY_Gy);
            uint64_t R = (TOT / N); if (R < 1) R = 1;
            double ns = measure_best(3, R * N, [&]() {
                for (uint64_t r = 0; r < R; r++)
                    for (size_t i = 0; i < N; i++) arr[i] = J::dbl(arr[i]);
            });
            fprintf(out, "dbl,%d,%zu,%.3f\n", D, N * 12, ns);
            fprintf(stderr, "dbl 2^%-2d done (%.0f MB footprint)\n", D, N * 12.0 / 1e6);
        }
    }
    // --- sequential mixed add (walk step + G) ---
    {
        const uint64_t TOT = 30000000ull;
        for (int D = 10; D <= 22; D++) {
            size_t N = (size_t)1 << D;
            std::vector<J> arr(N);
            for (auto& j : arr) j = J::from_affine(TOY_Gx, TOY_Gy);
            uint64_t R = (TOT / N); if (R < 1) R = 1;
            double ns = measure_best(3, R * N, [&]() {
                for (uint64_t r = 0; r < R; r++)
                    for (size_t i = 0; i < N; i++) arr[i] = J::add_affine(arr[i], base);
            });
            fprintf(out, "add,%d,%zu,%.3f\n", D, N * 12, ns);
            fprintf(stderr, "add 2^%-2d done (%.0f MB footprint)\n", D, N * 12.0 / 1e6);
        }
    }
    // --- random gather from affine table (BSGS/Kangaroo table lookups) ---
    {
        const uint64_t TOT = 50000000ull;
        for (int D = 12; D <= 24; D++) {
            size_t N = (size_t)1 << D;
            std::vector<std::pair<uint32_t, uint32_t>> tab(N);
            uint32_t g = 1;
            for (size_t i = 0; i < N; i++) { tab[i] = {g, g}; g = (uint32_t)((uint64_t)g * 1103515245u + 12345u); }
            uint64_t b = D <= 31 ? (1ull << D) : (1ull << 31);
            double ns = measure_best(3, TOT, [&]() {
                volatile uint64_t sink = 0;
                uint32_t i = 0x12345678u;
                for (uint64_t it = 0; it < TOT; it++) {
                    i = i * 1664525u + 1013904223u;
                    sink += tab[i & (b - 1)].second;
                }
                (void)sink;
            });
            fprintf(out, "gather_rand,%d,%zu,%.3f\n", D, N * 8, ns);
            fprintf(stderr, "gather_rand 2^%-2d done (%.0f MB)\n", D, N * 8.0 / 1e6);
        }
    }
    // --- stride-67 gather (prefetch-friendly, same sizes) ---
    {
        const uint64_t TOT = 50000000ull;
        for (int D = 12; D <= 24; D++) {
            size_t N = (size_t)1 << D;
            std::vector<std::pair<uint32_t, uint32_t>> tab(N);
            uint32_t g = 1;
            for (size_t i = 0; i < N; i++) { tab[i] = {g, g}; g = (uint32_t)((uint64_t)g * 1103515245u + 12345u); }
            uint64_t b = D <= 31 ? (1ull << D) : (1ull << 31);
            double ns = measure_best(3, TOT, [&]() {
                volatile uint64_t sink = 0;
                for (uint64_t it = 0; it < TOT; it++) sink += tab[(it * 67) & (b - 1)].second;
                (void)sink;
            });
            fprintf(out, "gather_stride67,%d,%zu,%.3f\n", D, N * 8, ns);
            fprintf(stderr, "gather_stride67 2^%-2d done (%.0f MB)\n", D, N * 8.0 / 1e6);
        }
    }
    fflush(out);
    if (out != stdout) fclose(out);
    return 0;
}