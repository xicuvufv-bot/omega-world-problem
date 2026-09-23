// vow_engine.hpp — Phase 7+9: van Oorschot-Wiener distributed kangaroo engine (shared).
// W walkers over T threads; every walker follows the SAME deterministic jump rule f (indexed
// by affine x), so tame (known offset) and wild (P+u*G) orbits coalesce; distinguished-point
// pruning caps the shared table. Cross-owner DP match => k = d_tame - d_wild (mod l),
// every solution re-verified independently. Parameters tunable: K (jump table size),
// b (DP bits), walkcap factor, budget.
#pragma once
#include <cstdint>
#include <cmath>
#include <random>
#include <vector>
#include <atomic>
#include <thread>
#include <mutex>
#include "instance.hpp"
#include "src/fp.hpp"
#include "src/ec.hpp"

namespace vow {

using F  = fp::FpNaive<TOY_P>;
using E  = F::Elem;
using A  = ec::Affine<F>;
using J  = ec::Jacobian<F>;

static inline uint64_t now_ns() {
    using namespace std::chrono;
    return duration_cast<std::chrono::nanoseconds>(std::chrono::steady_clock::now().time_since_epoch()).count();
}

static constexpr uint64_t L = TOY_L;   // group order (prime, = order of G)

static bool verify(uint32_t k, uint32_t Px, uint32_t Py) {
    A got = ec::Jacobian<F>::mul(ec::Jacobian<F>::from_affine(TOY_Gx, TOY_Gy), k).to_affine();
    return (!got.inf) && (uint32_t)got.x == Px && (uint32_t)got.y == Py;
}

static inline int jumpx(const A& p, int K) {
    int m = 1; while (m < K) m <<= 1;       // next pow2 >= K
    return (int)(((uint32_t)p.x >> 8) & (m - 1));
}

// shared (x,y) -> (owner, dist mod l) distinguished-point table, open addressing, mutexed
struct DPTab {
    std::mutex mtx;
    uint32_t cap = 0, mask = 0, used = 0;
    std::vector<uint32_t> x, y;
    std::vector<uint8_t>  own;   // 0=tame, 1=wild
    std::vector<uint64_t> dst;   // distance from G (mod l)
    void init(size_t n) {
        cap = 64; while (cap < n * 2) cap <<= 1; mask = cap - 1; used = 0;
        x.assign(cap, 0xFFFFFFFFu); y.assign(cap, 0); own.assign(cap, 0); dst.assign(cap, 0);
    }
    size_t slot(uint32_t kx, uint32_t ky) const {
        size_t i = (kx * 2654435761u) & mask;
        while (x[i] != 0xFFFFFFFFu && !(x[i] == kx && y[i] == ky)) i = (i + 1) & mask;
        return i;
    }
    void grow() {
        std::vector<uint32_t> ox = x, oy = y;
        std::vector<uint8_t>  oo = own;
        std::vector<uint64_t> od = dst;
        uint32_t oc = cap;
        cap <<= 1; mask = cap - 1;
        x.assign(cap, 0xFFFFFFFFu); y.assign(cap, 0); own.assign(cap, 0); dst.assign(cap, 0);
        used = 0;
        for (uint32_t i = 0; i < oc; i++)
            if (ox[i] != 0xFFFFFFFFu) {
                size_t s = slot(ox[i], oy[i]);
                x[s] = ox[i]; y[s] = oy[i]; own[s] = oo[i]; dst[s] = od[i]; used++;
            }
    }
    // -1 inserted-new; 0 redundant same-owner merge; 1 cross-owner match -> *cand
    int tryput(uint32_t kx, uint32_t ky, uint8_t og, uint64_t dd, uint64_t* cand) {
        std::lock_guard<std::mutex> lk(mtx);
        if (used * 3 > cap * 2) grow();
        size_t s = slot(kx, ky);
        if (x[s] == 0xFFFFFFFFu) {
            x[s] = kx; y[s] = ky; own[s] = og; dst[s] = dd; used++;
            return -1;
        }
        if (own[s] == og) return 0;
        uint64_t td = (og == 0) ? dd : dst[s];
        uint64_t wk = (og == 0) ? dst[s] : dd;
        *cand = (td + L - wk) % L;
        return 1;
    }
};

struct EngineOpt {
    uint64_t N;          // interval size
    int T;               // threads
    int W;               // total walkers
    int b;               // distinguished bits (DP prob = 2^-b)
    int K;               // jump table size (>=1)
    uint64_t walkcap;    // steps before a walker auto-restarts
    uint64_t budget;     // global step budget
    uint64_t seed;
};

struct EngineRes {
    uint64_t steps;
    double ns;
    uint32_t k;
    bool ok;
    size_t dps;
    size_t mem;
};

static EngineRes run(const EngineOpt& o, uint32_t k_) {
    A P = ec::Jacobian<F>::mul(ec::Jacobian<F>::from_affine(TOY_Gx, TOY_Gy), k_).to_affine();
    const uint32_t Px = (uint32_t)P.x, Py = (uint32_t)P.y;
    const uint64_t sl = (uint64_t)std::sqrt((double)o.N);

    std::mt19937_64 rng(o.seed);
    int K = o.K < 1 ? 1 : o.K;
    std::vector<A> jumps(K);
    std::vector<uint64_t> jd(K);
    for (int i = 0; i < K; i++) {
        uint64_t d = 1 + (uint64_t)(rng() % (uint64_t)std::max(2.0, 2.0 * sl));
        jd[i] = d;
        jumps[i] = ec::Jacobian<F>::mul(ec::Jacobian<F>::from_affine(TOY_Gx, TOY_Gy), d).to_affine();
    }
    const uint32_t DPMASK = (1u << o.b) - 1u;

    DPTab tab; tab.init((size_t)1 << (o.b > 0 ? o.b : 1));
    std::atomic<bool> done(false);
    std::atomic<uint32_t> solved(0);
    std::atomic<uint64_t> steps(0);
    std::atomic<uint64_t> walkers_running(0);

    uint64_t t0 = now_ns();
    const int perT = o.W / o.T;
    if (perT < 1) { EngineRes r; r.steps = 0; r.ns = 0; r.k = 0; r.ok = false; r.dps = 0; r.mem = 0; return r; }
    std::vector<std::thread> th;
    for (int t = 0; t < o.T; t++) {
        th.emplace_back([&, t]() {
            std::mt19937_64 r(777 + t * 131 + (uint64_t)o.seed);
            struct Wk { A X; uint64_t d; int owner; uint64_t cnt; };
            std::vector<Wk> wk;
            wk.reserve(perT);
            auto restart = [&](Wk& w) {
                if (w.owner == 0) {
                    uint64_t a = 1 + (uint64_t)(r() % o.N);
                    w.X = ec::Jacobian<F>::mul(ec::Jacobian<F>::from_affine(TOY_Gx, TOY_Gy), a).to_affine();
                    w.d = a % L;
                } else {
                    uint64_t u = (uint64_t)(r() % o.N);
                    w.X = ec::Jacobian<F>::mul(ec::Jacobian<F>::from_affine(TOY_Gx, TOY_Gy), (k_ + u) % L).to_affine();
                    w.d = u % L;
                }
                w.cnt = 0;
            };
            for (int i = 0; i < perT; i++) {
                Wk w; w.owner = ((i & 1) == 0) ? 0 : 1;
                restart(w);
                wk.push_back(w);
            }
            std::vector<A> bX;
            std::vector<uint8_t>  bOwn;
            std::vector<uint64_t> bDst;
            bX.reserve(256); bOwn.reserve(256); bDst.reserve(256);
            int mi = 0;
            while (!done.load() && steps.load() < o.budget) {
                Wk& w = wk[mi]; mi = (mi + 1) % (int)wk.size();
                if (w.cnt >= o.walkcap) { restart(w); continue; }
                int jj = jumpx(w.X, K);
                J nj = J::add_affine(J::from_affine((uint32_t)w.X.x, (uint32_t)w.X.y), jumps[jj]);
                A af = nj.to_affine();
                if (af.inf) { restart(w); continue; }
                w.X = af;
                w.d = (w.d + jd[jj]) % L;
                w.cnt++;
                steps.fetch_add(1);
                if (((uint32_t)w.X.x & DPMASK) == 0) {
                    bX.push_back(w.X); bOwn.push_back((uint8_t)w.owner); bDst.push_back(w.d);
                    restart(w);
                }
                if (bX.size() >= 128) {
                    for (size_t q = 0; q < bX.size() && !done.load(); q++) {
                        uint64_t cand = 0;
                        int rc = tab.tryput((uint32_t)bX[q].x, (uint32_t)bX[q].y, bOwn[q], bDst[q], &cand);
                        if (rc == 1 && verify((uint32_t)cand, Px, Py)) {
                            bool e = false;
                            if (done.compare_exchange_strong(e, true)) solved = (uint32_t)cand;
                        }
                    }
                    bX.clear(); bOwn.clear(); bDst.clear();
                }
            }
            for (size_t q = 0; q < bX.size() && !done.load(); q++) {
                uint64_t cand = 0;
                int rc = tab.tryput((uint32_t)bX[q].x, (uint32_t)bX[q].y, bOwn[q], bDst[q], &cand);
                if (rc == 1 && verify((uint32_t)cand, Px, Py)) {
                    bool e = false;
                    if (done.compare_exchange_strong(e, true)) solved = (uint32_t)cand;
                }
            }
            walkers_running.fetch_add(1);
        });
    }
    for (auto& tt : th) if (tt.joinable()) tt.join();
    uint64_t t1 = now_ns();

    uint32_t sol = solved.load();
    bool ok = (done.load() && sol == k_);
    EngineRes r;
    r.steps = steps.load();
    r.ns = (double)(t1 - t0);
    r.k = sol;
    r.ok = ok;
    r.dps = tab.used;
    r.mem = tab.cap;
    return r;
}

} // namespace vow