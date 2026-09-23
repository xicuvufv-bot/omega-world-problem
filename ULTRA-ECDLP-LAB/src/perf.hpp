// perf.hpp — timing helpers, cycle estimation, op counters
#pragma once
#include <chrono>
#include <cstdint>
#include <cstdio>
#include <thread>

namespace perf {

using Clock = std::chrono::steady_clock;
using ns = std::chrono::nanoseconds;

inline double now_s() { return std::chrono::duration<double>(Clock::now().time_since_epoch()).count(); }

// Estimate effective CPU clock by correlating rdtsc with steady_clock over ~0.1s.
inline double estimate_ghz() {
    auto t0 = Clock::now();
    uint64_t c0;
#if defined(_MSC_VER)
    c0 = __rdtsc();
#else
    unsigned lo, hi;
    __asm__ __volatile__("rdtsc" : "=a"(lo), "=d"(hi));
    c0 = ((uint64_t)hi << 32) | lo;
#endif
    std::this_thread::sleep_for(std::chrono::milliseconds(120));
    auto t1 = Clock::now();
    uint64_t c1;
#if defined(_MSC_VER)
    c1 = __rdtsc();
#else
    __asm__ __volatile__("rdtsc" : "=a"(lo), "=d"(hi));
    c1 = ((uint64_t)hi << 32) | lo;
#endif
    double secs = std::chrono::duration<double>(t1 - t0).count();
    return (double)(c1 - c0) / secs / 1e9;
}

// Run fn() n times, return ns/op. fn may take an int index.
template <typename Fn>
double bench_ns(int64_t n, const Fn& fn) {
    // warmup
    for (int i = 0; i < 3; i++) fn(i);
    auto t0 = Clock::now();
    for (int64_t i = 0; i < n; i++) fn(i);
    auto t1 = Clock::now();
    return std::chrono::duration<double>(t1 - t0).count() * 1e9 / (double)n;
}

} // namespace perf