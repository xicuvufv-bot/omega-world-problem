// algos_main.cpp — Phase 6: toy-ECDLP algorithm landscape.
// Interval ECDLP: P = k*G, k uniform in [1, N). Report group-steps (point ops),
// wall ms, ns/step; every solution is re-verified by independent scalar mul.
#include <cstdio>
#include <cstdint>
#include <cmath>
#include <random>
#include <vector>
#include <atomic>
#include <thread>
#include <chrono>
#include "instance.hpp"
#include "src/fp.hpp"
#include "src/ec.hpp"

using F  = fp::FpNaive<TOY_P>;
using E  = F::Elem;
using A  = ec::Affine<F>;
using J  = ec::Jacobian<F>;

static inline uint64_t now_ns() {
    using namespace std::chrono;
    return duration_cast<nanoseconds>(steady_clock::now().time_since_epoch()).count();
}
static inline void flush_all() { fflush(stdout); fflush(stderr); }
static void progress(const char* m) { fprintf(stderr, "[%s]\n", m); fflush(stderr); }

static bool verify(uint32_t k, uint32_t Px, uint32_t Py) {
    A got = ec::Jacobian<F>::mul(ec::Jacobian<F>::from_affine(TOY_Gx, TOY_Gy), k).to_affine();
    return (!got.inf) && (uint32_t)got.x == Px && (uint32_t)got.y == Py;
}

// ================================================================ brute
struct BruteResult { uint64_t steps; double ns; uint32_t k; };
static BruteResult brute(uint32_t k, uint64_t N) {
    A P = ec::Jacobian<F>::mul(ec::Jacobian<F>::from_affine(TOY_Gx, TOY_Gy), k).to_affine();
    J Q = J::from_affine(P.x, P.y);
    const A gneg = A::rep(F::from_raw(TOY_Gx), F::sub(F::zero(), F::from_raw(TOY_Gy)));
    uint64_t t0 = now_ns();
    uint64_t steps = (uint64_t)k;            // walk P-kG -> identity requires k subtracts
    uint32_t sol = 0;
    for (uint64_t i = 1; i <= k; i++) {
        Q = J::add_affine(Q, gneg);
        if (Q.is_zero()) { sol = (uint32_t)i; break; }
        steps = i;
    }
    uint64_t t1 = now_ns();
    if (sol != k) printf("BRUTE FAIL k=%u sol=%u\n", k, sol);
    return { steps, (double)(t1 - t0), sol };
}

// ================================================================ BSGS
struct BsgsResult { uint64_t steps; double ns; uint32_t k; size_t mem_entries; };
static BsgsResult bsgs(uint32_t k, uint64_t N) {
    A P = ec::Jacobian<F>::mul(ec::Jacobian<F>::from_affine(TOY_Gx, TOY_Gy), k).to_affine();
    uint64_t m = (uint64_t)std::ceil(std::sqrt((double)N)); if (m < 1) m = 1;
    // baby table: affine x -> j  (open addressing on x; x collisions rarer than 1/2^32)
    std::vector<uint32_t> keys(0);
    std::vector<uint32_t> vals(0);
    size_t cap = 1; while (cap < m * 4) cap <<= 1;
    keys.assign(cap, 0xFFFFFFFFu); vals.assign(cap, 0);
    auto slot = [&](uint32_t key) { size_t i = (key * 2654435761u) & (cap - 1);
        while (keys[i] != 0xFFFFFFFFu && keys[i] != key) i = (i + 1) & (cap - 1); return i; };
    J cur = J::from_affine(TOY_Gx, TOY_Gy);
    uint64_t t0 = now_ns();
    size_t entries = 0;
    for (uint64_t j = 1; j <= m; j++) {
        A af = cur.to_affine();
        if (!af.inf) { size_t s = slot((uint32_t)af.x); if (keys[s] == 0xFFFFFFFFu) { keys[s] = (uint32_t)af.x; vals[s] = (uint32_t)j; entries++; } }
        cur = J::add_affine(cur, A::point(TOY_Gx, TOY_Gy));
    }
    J mG = ec::Jacobian<F>::mul(J::from_affine(TOY_Gx, TOY_Gy), m);
    A amG = mG.to_affine();
    A gmG = amG.inf ? A::point(0,0) : A::rep(F::from_raw(amG.x), F::sub(F::zero(), amG.y));
    J R = J::from_affine(P.x, P.y);
    uint64_t steps = 0;
    uint32_t sol = 0;
    for (uint64_t i = 0; i <= m; i++) {
        A af = R.to_affine(); steps++;
        if (!af.inf) {
            size_t s = slot((uint32_t)af.x);
            if (keys[s] != 0xFFFFFFFFu) {
                uint32_t j = vals[s];
                uint32_t cand = (uint32_t)(i * m + j);
                if (cand >= 1 && cand <= N && verify(cand, P.x, P.y)) { sol = cand; break; }
            }
        }
        if (!gmG.inf) R = J::add_affine(R, gmG); steps++;
    }
    uint64_t t1 = now_ns();
    if (sol != k) printf("BSGS FAIL k=%u sol=%u N=%llu m=%llu\n", k, sol, N, m);
    return { steps, (double)(t1 - t0), sol, entries };
}

// ================================================================ Pollard rho
// Single forward walk with distinguished points (van Oorschot–Wiener style):
// x_{i+1} = x_i + aux[partition(x_i)], DPs (low bits of affine x == 0) recorded.
// A later DP equal to an earlier DP with different coeffs delivers the log.
struct RhoResult { uint64_t steps; double ns; uint32_t k; };
static RhoResult pollard_rho(uint32_t k, uint64_t l) {
    A P = ec::Jacobian<F>::mul(J::from_affine(TOY_Gx, TOY_Gy), k).to_affine();
    A G = A::point(TOY_Gx, TOY_Gy);
    // Teske-style r-adding walk: 2^R random points, each a_j·G + b_j·P (16-bit coeffs)
    const int R = 7;
    const size_t K = (size_t)1 << R;
    std::mt19937_64 rng(4242u + (uint64_t)k);
    A aux[K]; uint64_t ca[K], cb[K];
    for (size_t i = 0; i < K; i++) {
        uint32_t aj = 1 + (uint32_t)(rng() & 0xFFFFu);
        uint32_t bj = 0; for (int z=0;z<2;z++) bj=(((uint64_t)bj<<16)|(uint32_t)(rng()&0xFFFFu))% (uint32_t)l;
        ca[i] = aj; cb[i] = bj;
        aux[i] = ec::Jacobian<F>::add(
            ec::Jacobian<F>::mul(J::from_affine(TOY_Gx, TOY_Gy), aj),
            ec::Jacobian<F>::mul(J::from_affine(P.x, P.y), bj)).to_affine();
    }
    const uint32_t DP_MASK = 0x3u;            // x & 3 == 0 distinguished (θ = 1/4)
    uint64_t t0 = now_ns();
    // DP hash: key = affine-x (32-bit), value packs (a,b) 32-bit each
    std::vector<uint32_t> kk(1 << 16, 0xFFFFFFFFu);
    std::vector<uint64_t> vv(1 << 16, 0);
    size_t cap = kk.size(), mask = cap - 1, used = 0;
    auto sinsert = [&](uint32_t z, uint64_t ab) {
        if (used * 3 > cap * 2) {
            std::vector<uint32_t> ok = kk; std::vector<uint64_t> ov = vv;
            cap <<= 1; mask = cap - 1;
            kk.assign(cap, 0xFFFFFFFFu); vv.assign(cap, 0); used = 0;
            for (size_t i = 0; i < ok.size(); i++) if (ok[i] != 0xFFFFFFFFu) {
                size_t h = (ok[i] * 2654435761u) & mask; while (kk[h] != 0xFFFFFFFFu) h = (h + 1) & mask;
                kk[h] = ok[i]; vv[h] = ov[i]; used++;
            }
        }
        size_t h = (z * 2654435761u) & mask; while (kk[h] != 0xFFFFFFFFu && kk[h] != z) h = (h + 1) & mask;
        if (kk[h] == 0xFFFFFFFFu) { kk[h] = z; vv[h] = ab; used++; }
    };
    auto sfind = [&](uint32_t z, uint64_t* out) -> bool {
        size_t h = (z * 2654435761u) & mask;
        while (kk[h] != 0xFFFFFFFFu && kk[h] != z) h = (h + 1) & mask;
        if (kk[h] == 0xFFFFFFFFu) return false;
        *out = vv[h]; return true;
    };
    A X = G; uint64_t a = 1, b = 0;         // X = aG + bP
    uint64_t steps = 0; uint32_t sol = 0;
    uint64_t lim = (uint64_t)(30.0 * 2.0 * 1.5 * std::sqrt((double)l)) + 10000;
    for (; steps < lim; steps++) {
        if (X.inf) break;
        uint32_t s = (uint32_t)(((uint32_t)((uint64_t)(uint32_t)X.x * 2654435761u)) >> (32 - R));  // Knuth-mix top bits
        X = A::add(X, aux[s]);
        a = (a + ca[s]) % l;
        b = (b + cb[s]) % l;
        if ((uint32_t)X.x & DP_MASK) {
            uint64_t ab = ((uint64_t)a << 32) | b;
            uint64_t prev;
            if (sfind((uint32_t)X.x, &prev)) {
                int64_t da = (int64_t)((a + l - (prev >> 32)) % l);
                int64_t db = (int64_t)(((prev & 0xFFFFFFFFull) + l - b) % l);
                if (db != 0) {
                    uint32_t dbinv = fp::inv_mod_u32((uint32_t)db, (uint32_t)l);
                    uint32_t cand = (uint32_t)(((uint64_t)da * dbinv) % l);
                    if (cand >= 1 && verify(cand, P.x, P.y)) { sol = cand; break; }
                }
            } else sinsert((uint32_t)X.x, ab);
        }
    }
    uint64_t t1 = now_ns();
    if (sol != k) printf("RHO FAIL k=%u sol=%u steps=%llu\n", k, sol, steps);
    return { steps, (double)(t1 - t0), sol };
}

// ================================================================ Kangaroo
constexpr int KJUMP = 32;
struct KangaResult { uint64_t steps; double ns; uint32_t k; bool ok; };

// jump-offset from Jacobian X low bits (deterministic DP-pseudo-random jump rule)
static int jumpx(const J& j, uint64_t reset) {
    if (j.is_zero()) return (int)(reset & (KJUMP - 1));
    return (int)(((uint32_t)j.X >> 8) & (KJUMP - 1));
}

// keyed-on-(x,y) open addressing hash with per-point owner/dist; grows at 2/3 load
struct KTab {
    uint32_t mask, cap, used;
    std::vector<uint32_t> x;
    std::vector<uint32_t> y;
    std::vector<int64_t> dist;
    std::vector<uint8_t> owner;      // 0=tame, 1=wild
    void init(size_t n) {
        cap = 16; while (cap < n * 4) cap <<= 1; mask = cap - 1; used = 0;
        x.assign(cap, 0xFFFFFFFFu); y.assign(cap, 0); dist.assign(cap, 0); owner.assign(cap, 0);
    }
    size_t slot(uint32_t kx, uint32_t ky) const {
        size_t i = (kx * 2654435761u) & mask;
        size_t start = i;
        while (x[i] != 0xFFFFFFFFu && !(x[i] == kx && y[i] == ky)) i = (i + 1) & mask;
        return i;
    }
    void insert(uint32_t kx, uint32_t ky, int64_t dd, uint8_t own) {
        if (used * 3 > cap * 2) {
            std::vector<uint32_t> ox = x, oy = y;
            std::vector<int64_t> od = dist;
            std::vector<uint8_t> oo = owner;
            uint32_t ocap = cap;
            cap <<= 1; mask = cap - 1;
            x.assign(cap, 0xFFFFFFFFu); y.assign(cap, 0); dist.assign(cap, 0); owner.assign(cap, 0);
            used = 0;
            for (uint32_t i = 0; i < ocap; i++)
                if (ox[i] != 0xFFFFFFFFu) insert(ox[i], oy[i], od[i], oo[i]);
        }
        size_t s = slot(kx, ky);
        if (x[s] == 0xFFFFFFFFu) { x[s] = kx; y[s] = ky; dist[s] = dd; owner[s] = own; used++; }
        // same point re-seen: keep first (tame or wild) — distances are equivalent
    }
    bool find(uint32_t kx, uint32_t ky, int64_t* dd, uint8_t* own) const {
        size_t s = slot(kx, ky);
        if (x[s] == 0xFFFFFFFFu) return false;
        *dd = dist[s]; *own = owner[s];
        return true;
    }
};

static KangaResult kangaroo(uint32_t k, uint64_t N, int nthreads) {
    A P = ec::Jacobian<F>::mul(J::from_affine(TOY_Gx, TOY_Gy), k).to_affine();
    const uint64_t Px = P.x, Py = P.y;
    double mu = std::sqrt((double)N);
    std::mt19937_64 rng(1234 + k);
    std::vector<A> jumps(KJUMP);
    std::vector<uint64_t> jd(KJUMP);
    for (int i = 0; i < KJUMP; i++) {
        uint64_t d = 1 + (uint64_t)(rng() % (uint64_t)std::max(2.0, mu * 2.0));
        jd[i] = d;
        jumps[i] = ec::Jacobian<F>::mul(J::from_affine(TOY_Gx, TOY_Gy), d).to_affine();
    }
    uint64_t t0 = now_ns();
    std::atomic<bool> done(false);
    std::atomic<uint32_t> solved(0);
    std::atomic<uint64_t> steps(0);
    // Simultaneous tame+wild: same deterministic walk f, so their orbits coalesce
    // in O(sqrt(|state space|)). Tame starts at random known offset in [0,N); wild at P.
    uint64_t caps = (uint64_t)(12.0 * std::sqrt((double)N)) + 64;
    std::vector<std::thread> th;
    for (int t = 0; t < nthreads; t++) {
        th.emplace_back([&, t]() {
            std::mt19937_64 r2(777 + t * 101 + (uint64_t)k);
            uint64_t td0 = (uint64_t)r2() % N;        // known tame offset
            J tame = (td0 == 0) ? J::zero() : ec::Jacobian<F>::mul(J::from_affine(TOY_Gx, TOY_Gy), td0);
            int64_t td = (int64_t)td0;
            J wild = J::from_affine((uint32_t)Px, (uint32_t)Py);
            int64_t wd = 0;
            KTab tab; tab.init(caps);
            auto store = [&](const J& p, int64_t dd, uint8_t own) {
                A af = p.to_affine(); if (af.inf) return;
                tab.insert((uint32_t)af.x, (uint32_t)af.y, dd, own);
            };
            auto lookup = [&](const J& p, int64_t* dd, uint8_t* own) -> bool {
                A af = p.to_affine(); if (af.inf) return false;
                return tab.find((uint32_t)af.x, (uint32_t)af.y, dd, own);
            };
            auto trysolve = [&](int64_t td_, int64_t wd_, int64_t dd, uint8_t own, uint64_t i) {
                if (done.load()) return;
                int64_t cand;
                if (own == 0) cand = (dd - wd_); else cand = (td_ - dd);
                if (cand > 0 && (uint64_t)cand <= N && verify((uint32_t)cand, (uint32_t)Px, (uint32_t)Py)) {
                    bool e = false;
                    if (done.compare_exchange_strong(e, true)) solved = (uint32_t)cand;
                }
            };
            store(tame, td, 0);
            store(wild, wd, 1);
            for (uint64_t i = 1; i <= caps; i++) {
                if (done.load()) break;
                int tj = jumpx(tame, i);
                tame = J::add_affine(tame, jumps[tj]); td += (int64_t)jd[tj];
                int wj = jumpx(wild, i);
                wild = J::add_affine(wild, jumps[wj]); wd += (int64_t)jd[wj];
                int64_t dd; uint8_t own;
                if (lookup(tame, &dd, &own)) { trysolve(td, wd, dd, own, i); }
                else store(tame, td, 0);
                if (done.load()) break;
                if (lookup(wild, &dd, &own)) { trysolve(td, wd, dd, own, i); }
                else store(wild, wd, 1);
                steps.fetch_add(2);
            }
        });
    }
    for (auto& tt : th) if (tt.joinable()) tt.join();
    uint64_t t1 = now_ns();
    uint32_t sol = solved.load();
    bool ok = (done.load() && sol == k);
    if (!ok) printf("KANGA FAIL k=%u sol=%u nthreads=%d N=%llu caps=%llu\n", k, sol, nthreads, N, caps);
    return { steps.load(), (double)(t1 - t0), sol, ok };
}

// ================================================================ main
int main(int argc, char** argv) {
    setvbuf(stdout, NULL, _IOLBF, 0);
    int dbmax = 28;
    if (argc > 1) dbmax = atoi(argv[1]);
    printf("Phase 6 algorithm landscape (p=%u, #E=l=%llu, G=(%u,%u)) dbmax=%d\n", TOY_P, TOY_L, TOY_Gx, TOY_Gy, dbmax);
    printf("alg,db,N_label,steps,wall_ms,ns_per_step,mem_entries,k,verified\n");
    std::mt19937_64 rng(20260922);
    fflush(stderr);
    fprintf(stderr, "[db loop start]\n"); fflush(stderr);
    for (int db = 12; db <= dbmax; db += 4) {
        uint64_t N = 1ull << db;
        uint32_t k = 1 + (uint32_t)(rng() % N);
        if (db <= 20) {
            auto r = brute(k, N);
            printf("brute,%2d,2^%d,%llu,%.3f,%.2f,0,%u,%d\n", db, db, r.steps, r.ns/1e6, r.ns/(double)r.steps, k, (int)(r.k==k));
        } else {
            printf("brute,%2d,2^%d,SKIP,SKIP,SKIP,0,0,0\n", db, db);
        }
        flush_all();
        progress("after brute");
        auto b = bsgs(k, N);
        printf("bsgs, %2d,2^%d,%llu,%.3f,%.2f,%zu,%u,%d\n", db, db, b.steps, b.ns/1e6, b.ns/(double)b.steps, b.mem_entries, k, (int)(b.k==k));
        flush_all();
        progress("after bsgs");
        auto r1 = pollard_rho(k, TOY_L);
        printf("rho,  %2d,2^%d,%llu,%.3f,%.2f,0,%u,%d\n", db, db, r1.steps, r1.ns/1e6, r1.ns/(double)r1.steps, k, (int)(r1.k==k));
        flush_all();
        progress("after rho");
        auto g1 = kangaroo(k, N, 1);
        printf("kanga,%2d,2^%d,%llu,%.3f,%.2f,0,%u,%d\n", db, db, g1.steps, g1.ns/1e6, g1.ns/(double)g1.steps, k, (int)(g1.k==k));
        flush_all();
        progress("after kanga");
        auto g4 = kangaroo(k, N, 4);
        printf("kanga4,%2d,2^%d,%llu,%.3f,%.2f,0,%u,%d\n", db, db, g4.steps, g4.ns/1e6, g4.ns/(double)g4.steps, k, (int)(g4.k==k));
        flush_all();
        progress("after kanga4");
    }
    return 0;
}