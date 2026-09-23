// tuner_main.cpp — Phase 9: auto-tuner for the VOW kangaroo engine.
// Grid search over {b (DP bits), K (jump table size), wcm (walkcap multiplier x sqrt(N))}
// at a fixed target interval db (default 2^24). Each config runs REP repeats with
// per-config seeds (same k), keeps min-wall run, then ranks configs and prints best.
// CSV rows: config,db,b,K,wcm,steps,wall_ms,ns_per_step,addressable_2^b,verified
#include <cstdio>
#include <cstdint>
#include <cmath>
#include <random>
#include <algorithm>
#include <vector>
#include "instance.hpp"
#include "src/vow_engine.hpp"

using namespace vow;

struct Res {
    int b, K, wcm;
    uint64_t steps;
    double ns;
    uint64_t dps;
};

int main(int argc, char** argv) {
    setvbuf(stdout, NULL, _IOLBF, 0);
    int db = 24;
    int T = 4;
    int WPF = 8;
    int REP = 3;
    if (argc > 1) db = atoi(argv[1]);
    if (argc > 2) T = atoi(argv[2]);
    if (argc > 3) WPF = atoi(argv[3]);
    if (argc > 4) REP = atoi(argv[4]);

    uint64_t N = 1ull << db;
    std::mt19937_64 rng(20260922);
    uint32_t k = 1 + (uint32_t)(rng() % N);
    printf("phase9 auto-tuner. db=%d N=2^%d T=%d W=%d/thread REP=%d k=%u\n",
           db, db, T, WPF, k);
    printf("config,db,b,K,wcm,steps,wall_ms,ns_per_step,addressable_2^b,dps,verified\n");

    const int bs[] = {2, 4, 6, 8, 10, 12};
    const int ks[] = {8, 16, 32, 64};
    const int wcms[] = {3, 6, 12, 24};

    std::vector<Res> out;
    double best_ns = 1e300; Res best{};
    for (int b : bs) for (int K : ks) for (int wcm : wcms) {
        EngineOpt o; o.N = N; o.T = T; o.W = WPF * T; o.b = b; o.K = K;
        o.walkcap = (uint64_t)wcm * (uint64_t)std::sqrt((double)N) + 64;
        o.budget = (uint64_t)(WPF * T) * 24 * (uint64_t)std::sqrt((double)N) + 65536;
        uint64_t seed0 = 500000u + (uint64_t)db * 100000 + (uint64_t)b * 10000 + (uint64_t)K * 100 + (uint64_t)wcm;
        o.seed = seed0;
        auto r0 = run(o, k);
        for (int rep = 1; rep < REP; rep++) {
            o.seed = seed0 + rep;
            auto r1 = run(o, k);
            if (r1.ns < r0.ns) r0 = r1;
        }
        bool ok = r0.ok && r0.k == k;
        printf("config,%d,%d,%d,%d,%llu,%.3f,%.2f,%d,%zu,%d\n",
               db, b, K, wcm, r0.steps, r0.ns / 1e6, r0.ns / (double)r0.steps, (1 << b), r0.dps, (int)ok);
        fflush(stdout);
        if (ok) {
            out.push_back({b, K, wcm, r0.steps, r0.ns, r0.dps});
            if (r0.ns < best_ns) { best_ns = r0.ns; best = {b, K, wcm, r0.steps, r0.ns, r0.dps}; }
        }
    }
    std::sort(out.begin(), out.end(), [](const Res& a, const Res& b) { return a.ns < b.ns; });
    printf("BEST(db=%d): steps=%llu wall_ms=%.3f ns/step=%.2f b=%d K=%d wcm=%d dps=%zu\n",
           db, best.steps, best.ns / 1e6, best.ns / (double)best.steps, best.b, best.K, best.wcm, best.dps);
    printf("TOP5:\n");
    for (size_t i = 0; i < out.size() && i < 5; i++)
        printf("  %zu) b=%d K=%d wcm=%d  %llu steps  %.3f ms\n", i + 1,
               out[i].b, out[i].K, out[i].wcm, out[i].steps, out[i].ns / 1e6);
    return 0;
}