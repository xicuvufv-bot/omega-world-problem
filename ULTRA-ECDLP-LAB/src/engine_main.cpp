// engine_main.cpp — Phase 7 CLI: parallel collision engine (VOW kangaroo) benchmark.
// Thin driver over vow_engine.hpp; emits the CSV rows for PHASE7_PARALLEL_CS.csv.
// CSV: arc,T,db,N_label,steps,wall_ms,ns_per_step,mem_entries,dps,k,verified
#include <cstdio>
#include <cstdint>
#include <cmath>
#include <random>
#include "instance.hpp"
#include "src/vow_engine.hpp"

using namespace vow;

static inline const char* prog() { return "phase7"; }

int main(int argc, char** argv) {
    setvbuf(stdout, NULL, _IOLBF, 0);
    int dbmax = 28;
    int Tmax = 4;
    int WPF = 8;     // walkers PER THREAD (total = WPF*T)
    int bfix = -1;   // default b = ceil(0.5*log2(N))
    int REP = 5;     // repeats per (T,db); best (min) wall kept
    if (argc > 1) dbmax = atoi(argv[1]);
    if (argc > 2) Tmax = atoi(argv[2]);
    if (argc > 3) WPF = atoi(argv[3]);
    if (argc > 4) bfix = atoi(argv[4]);
    if (argc > 5) REP = atoi(argv[5]);
    printf("%s parallel collision engine (VOW kangaroo). p=%u, l=%llu, G=(%u,%u) dbmax=%d Tmax=%d W=%d/thread REP=%d\n",
           prog(), TOY_P, TOY_L, TOY_Gx, TOY_Gy, dbmax, Tmax, WPF, REP);
    printf("%s,T,db,N_label,steps,wall_ms,ns_per_step,mem_entries,dps,k,verified\n", prog());
    std::mt19937_64 rng(20260922);
    for (int db = 12; db <= dbmax; db += 4) {
        uint64_t N = 1ull << db;
        uint32_t k = 1 + (uint32_t)(rng() % N);
        int b = (bfix >= 0) ? bfix : (int)std::max(1, (int)std::ceil(0.5 * db));
        uint64_t walkcap = 6 * (uint64_t)std::sqrt((double)N) + 64;
        for (int T = 1; T <= Tmax; T <<= 1) {
            int W = WPF * T;
            uint64_t budget = (uint64_t)W * 24 * (uint64_t)std::sqrt((double)N) + 65536;
            EngineOpt o; o.N = N; o.T = T; o.W = W; o.b = b; o.K = 32;
            o.walkcap = walkcap; o.budget = budget;
            o.seed = 20260922 + (uint64_t)db * 1000 + T * 100;
            auto r0 = run(o, k);
            for (int rep = 1; rep < REP; rep++) {
                o.seed = 20260922 + (uint64_t)db * 1000 + T * 100 + rep;
                auto r1 = run(o, k);
                if (r1.ns < r0.ns) r0 = r1;    // keep min-wall run
            }
            printf("%s,%d,%d,2^%d,%llu,%.3f,%.2f,%zu,%zu,%u,%d\n",
                   prog(), T, db, db, r0.steps, r0.ns / 1e6, r0.ns / (double)r0.steps, r0.mem, r0.dps, k, (int)(r0.ok && r0.k == k));
            fflush(stdout);
        }
        printf("db%d done\n", db);
    }
    return 0;
}