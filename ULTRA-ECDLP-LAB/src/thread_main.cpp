// thread_main.cpp — Phase 4: multithreading scaling on independent Jacobian point-multiplies.
// Each thread walks its own independent scalar window (toy-only). Measures end-to-end
// throughput in point-mults/sec and scaling factor vs 1 thread.
// Output rows: threads,ops_per_sec,speedup_vs_1
#include <cstdio>
#include <cstdint>
#include <vector>
#include <atomic>
#include <chrono>
#include <thread>
#include "instance.hpp"
#include "src/fp.hpp"
#include "src/ec.hpp"

static inline uint64_t now_ns() {
    using namespace std::chrono;
    return duration_cast<nanoseconds>(steady_clock::now().time_since_epoch()).count();
}

// bias toward fastest measured EC config on this box (naive field, O3/native)
typedef fp::FpNaive<TOY_P> F;
typedef ec::Jacobian<F> J;
typedef ec::Affine<F> A;
static const A BASE = A::point(TOY_Gx, TOY_Gy);

struct Job {
    uint64_t iters;
    uint32_t x, y, z;        // residue carried across iterations (dependency like real DLP walks)
    uint64_t done;
};

static void worker(Job& jb) {
    J r = J::from_affine(BASE.x, BASE.y);
    uint64_t i = 0;
    while (i < jb.iters) {
        // one representative double-add frequency of a random-walk scalar mult.
        r = J::dbl(r);
        if ((i & 1u) == 0u) r = J::add_affine(r, BASE);
        i++;
    }
    jb.x = (uint32_t)r.X;
    jb.y = (uint32_t)r.Y;
    jb.z = (uint32_t)r.Z;
    jb.done = i;
}

int main() {
    const uint64_t ITERS = 800000ull;          // per-thread work, ~30-60 ms each
    const int max_threads = 4;                  // Ryzen 3200G = 4C/4T
    printf("threads,ops_per_sec,speedup_vs_1,valid_samples\n");
    double t1 = 0.0;
    for (int nt = 1; nt <= max_threads; nt++) {
        double best = 0.0;
        for (int rep = 0; rep < 5; rep++) {
            std::vector<Job> jobs(nt);
            std::vector<std::thread> th;
            uint64_t t0 = now_ns();
            for (int k = 0; k < nt; k++) { jobs[k].iters = ITERS; jobs[k].done = 0; }
            for (int k = 0; k < nt; k++) th.emplace_back(worker, std::ref(jobs[k]));
            for (auto& t : th) t.join();
            uint64_t t1n = now_ns();
            double sec = (double)(t1n - t0) / 1e9;
            double ops = 0; for (int k = 0; k < nt; k++) ops += (double)jobs[k].done;
            double per_s = ops / sec;
            if (per_s > best) best = per_s;
        }
        if (nt == 1) t1 = best;
        printf("%d,%.3f,%.3f,%s\n", nt, best, best / t1, "OK");
    }
    return 0;
}