// gpu_main.cpp — Phase 8: OpenCL experiment on AMD Vega 8 iGPU.
// Runs the EC mixed-add (Jacobian + affine, ec.hpp add_affine — the Phase 7 kanga/VOW
// jump-step) as a data-parallel OpenCL kernel over many independent walkers and times
// GPU vs CPU (4 threads) for the SAME work.
//
// Correctness gate: CPU reference uses EC::Jacobian<FpNaive>::add_affine directly; the
// OpenCL kernel replicates the identical 8M+3S sequence with p=TOY_P mod arithmetic.
// Both accumulate the same per-walker checksum over (X,Y,Z); `match=1` iff checendersums equal.
//
// Output: PHASE8_GPU_RESULTS.csv row (ops,gpu_ms,gpu_Gops,cpu_ms,cpu_Gops,ratio,matched)
#include <cstdio>
#include <cstdint>
#include <cmath>
#include <random>
#include <vector>
#include <thread>
#include <chrono>
#include <atomic>
#include "instance.hpp"
#include "src/fp.hpp"
#include "src/ec.hpp"
#include "ocl_min.h"

using F = fp::FpNaive<TOY_P>;
using A = ec::Affine<F>;
using J = ec::Jacobian<F>;
using namespace std::chrono;

static inline uint64_t now_ns() {
    return duration_cast<nanoseconds>(steady_clock::now().time_since_epoch()).count();
}

// ---------- CPU reference walk: EXACTLY ec::Jacobian::add_affine ----------
static uint64_t cpu_run(const std::vector<A>& jumps, std::vector<uint64_t>& seeds,
                        uint64_t iters, int nthreads) {
    std::atomic<uint64_t> acc(0);
    size_t n = seeds.size() / 2;
    std::vector<std::thread> th;
    size_t per = n / nthreads;
    for (int t = 0; t < nthreads; t++) {
        th.emplace_back([&, t]() {
            size_t lo = (size_t)t * per, hi = (t == nthreads - 1) ? n : lo + per;
            uint64_t local = 0;
            for (size_t i = lo; i < hi; i++) {
                uint64_t X = seeds[2 * i], Y = seeds[2 * i + 1], Z = 1;
                for (uint64_t it = 0; it < iters; it++) {
                    int sel = (int)((X >> 8) & 31);
                    const A& b = jumps[sel];
                    // --- add_affine step, 32-bit FpNaive arithmetic ---
                    uint64_t Z1Z1 = (Z * Z) % TOY_P;
                    uint64_t U2 = (b.x * Z1Z1) % TOY_P;
                    uint64_t S2 = (b.y * ((Z1Z1 * Z) % TOY_P)) % TOY_P;
                    uint64_t H  = (U2 >= X) ? (U2 - X) : (U2 - X + TOY_P);
                    uint64_t R  = (S2 >= Y) ? (S2 - Y) : (S2 - Y + TOY_P);
                    uint64_t HH = (H * H) % TOY_P;
                    uint64_t HHH = (H * HH) % TOY_P;
                    uint64_t V  = (X * HH) % TOY_P;
                    uint64_t X3 = (R * R) % TOY_P;
                    X3 = (X3 >= HHH) ? (X3 - HHH) : (X3 - HHH + TOY_P);
                    uint64_t twoV = V + V; if (twoV >= TOY_P) twoV -= TOY_P;
                    X3 = (X3 >= twoV) ? (X3 - twoV) : (X3 - twoV + TOY_P);
                    uint64_t VmX3 = (V >= X3) ? (V - X3) : (V - X3 + TOY_P);
                    uint64_t Y3 = (R * VmX3) % TOY_P;
                    uint64_t aH = (Y * HHH) % TOY_P;
                    Y3 = (Y3 >= aH) ? (Y3 - aH) : (Y3 - aH + TOY_P);
                    uint64_t Z3 = (Z * H) % TOY_P;
                    X = X3; Y = Y3; Z = Z3;
                    local ^= (X * 6364136223846793005ull + Y * 1442695040888963407ull + Z) % TOY_P;
                }
            }
            acc.fetch_xor(local);
        });
    }
    for (auto& tt : th) tt.join();
    return acc.load();
}

// ---------- OpenCL error strings ----------
static const char* clerr(cl_int e) {
    switch (e) {
        case 0: return "CL_SUCCESS";
        case -1: return "DEVICE_NOT_FOUND"; case -2: return "DEVICE_NOT_AVAILABLE";
        case -3: return "COMPILER_NOT_AVAILABLE"; case -4: return "MEM_OBJECT_ALLOCATION_FAILURE";
        case -5: return "OUT_OF_RESOURCES"; case -6: return "OUT_OF_HOST_MEMORY";
        case -11: return "BUILD_PROGRAM_FAILURE"; case -19: return "KERNEL_ARG_INFO_NOT_AVAILABLE";
        case -30: return "INVALID_VALUE"; case -31: return "INVALID_DEVICE_TYPE";
        case -33: return "INVALID_DEVICE"; case -34: return "INVALID_CONTEXT";
        case -36: return "INVALID_COMMAND_QUEUE"; case -38: return "INVALID_MEM_OBJECT";
        case -42: return "INVALID_BINARY"; case -43: return "INVALID_BUILD_OPTIONS";
        case -44: return "INVALID_PROGRAM"; case -46: return "INVALID_KERNEL_NAME";
        case -47: return "INVALID_KERNEL_DEFINITION"; case -48: return "INVALID_KERNEL";
        case -49: return "INVALID_ARG_INDEX"; case -50: return "INVALID_ARG_VALUE";
        case -51: return "INVALID_ARG_SIZE"; case -52: return "INVALID_KERNEL_ARGS";
        case -53: return "INVALID_WORK_DIMENSION"; case -54: return "INVALID_WORK_GROUP_SIZE";
        case -55: return "INVALID_WORK_ITEM_SIZE"; case -57: return "INVALID_EVENT_WAIT_LIST";
        case -63: return "INVALID_GLOBAL_WORK_SIZE";
        default: return "UNKNOWN";
    }
}

int main(int argc, char** argv) {
    setvbuf(stdout, NULL, _IOLBF, 0);
    uint64_t n_walkers = 1ull << 16;
    uint64_t iters = 4096;
    if (argc > 1) n_walkers = (uint64_t)1 << atoi(argv[1]);
    if (argc > 2) iters = (uint64_t)1 << atoi(argv[2]);

    printf("Phase 8 OpenCL: Vega 8 iGPU, p=%u, G=(%u,%u). walkers=%llu iters=%llu total_ops=%llu\n",
           TOY_P, TOY_Gx, TOY_Gy, n_walkers, iters, n_walkers * iters);

    // ---------------- GPU path ----------------
    cl_platform_id plat = 0; cl_device_id dev = 0;
    cl_int err = clGetPlatformIDs(1, &plat, NULL);
    if (err != CL_SUCCESS) { printf("no platform (%s)\n", clerr(err)); return 2; }
    err = clGetDeviceIDs(plat, CL_DEVICE_TYPE_GPU, 1, &dev, NULL);
    if (err != CL_SUCCESS) { printf("no gpu device (%s)\n", clerr(err)); return 2; }
    char dname[128] = {0}; cl_uint cu = 0, maxclk = 0; size_t wgs = 0;
    clGetDeviceInfo(dev, CL_DEVICE_NAME, sizeof(dname), dname, NULL);
    clGetDeviceInfo(dev, CL_DEVICE_MAX_COMPUTE_UNITS, sizeof(cu), &cu, NULL);
    clGetDeviceInfo(dev, CL_DEVICE_MAX_CLOCK_FREQUENCY, sizeof(maxclk), &maxclk, NULL);
    clGetDeviceInfo(dev, CL_DEVICE_MAX_WORK_GROUP_SIZE, sizeof(wgs), &wgs, NULL);
    printf("device : %s | CUs=%u clock=%u MHz max_wg=%zu\n", dname, cu, maxclk, wgs);

    cl_context ctx = clCreateContext(NULL, 1, &dev, NULL, NULL, &err);
    if (err != CL_SUCCESS) { printf("ctx err %s\n", clerr(err)); return 3; }
    cl_command_queue q = clCreateCommandQueue(ctx, dev, 0, &err);
    if (err != CL_SUCCESS) { printf("queue err %s\n", clerr(err)); return 3; }

    const char* src =
        "typedef unsigned int  u32;\n"
        "typedef unsigned long u64;\n"
        "#define P 4294966177u\n"
        "static inline u64 mm(u64 a, u64 b) { return (a * b) % P; }\n"   // field mul (via tools: 64-bit mul+mod)
        "__kernel void walk(const __global ulong2* jp, const __global ulong2* seeds, ulong iters, __global ulong* out) {\n"
        "    int i = get_global_id(0);\n"
        "    u64 X = seeds[i].x, Y = seeds[i].y, Z = 1ul;\n"
        "    u64 checksum = 0;\n"
        "    for (u64 it = 0; it < iters; it++) {\n"
        "        int sel = (int)((X >> 8) & 31);\n"
        "        u64 bx = jp[sel].x, by = jp[sel].y;\n"
        "        u64 Z1Z1 = mm(Z, Z);\n"
        "        u64 U2 = mm(bx, Z1Z1);\n"
        "        u64 S2 = mm(by, mm(Z1Z1, Z));\n"
        "        u64 H = (U2 >= X) ? (U2 - X) : (U2 - X + P);\n"
        "        u64 R = (S2 >= Y) ? (S2 - Y) : (S2 - Y + P);\n"
        "        u64 HH = mm(H, H);\n"
        "        u64 HHH = mm(H, HH);\n"
        "        u64 V = mm(X, HH);\n"
        "        u64 X3 = mm(R, R);\n"
        "        X3 = (X3 >= HHH) ? (X3 - HHH) : (X3 - HHH + P);\n"
        "        u64 twoV = V + V; if (twoV >= P) twoV -= P;\n"
        "        X3 = (X3 >= twoV) ? (X3 - twoV) : (X3 - twoV + P);\n"
        "        u64 VmX3 = (V >= X3) ? (V - X3) : (V - X3 + P);\n"
        "        u64 Y3 = mm(R, VmX3);\n"
        "        u64 aH = mm(Y, HHH);\n"
        "        Y3 = (Y3 >= aH) ? (Y3 - aH) : (Y3 - aH + P);\n"
        "        u64 Z3 = mm(Z, H);\n"
        "        X = X3; Y = Y3; Z = Z3;\n"
        "        checksum ^= (X * 6364136223846793005ul + Y * 1442695040888963407ul + Z) % P;\n"
        "    }\n"
        "    out[i] = checksum;\n"
        "}\n";

    cl_program prog = clCreateProgramWithSource(ctx, 1, &src, NULL, &err);
    if (err != CL_SUCCESS) { printf("src err %s\n", clerr(err)); return 3; }
    err = clBuildProgram(prog, 1, &dev, "-cl-std=CL1.2", NULL, NULL);
    if (err != CL_SUCCESS) {
        char log[16384] = {0};
        clGetProgramBuildInfo(prog, dev, CL_PROGRAM_BUILD_LOG, sizeof(log), log, NULL);
        printf("BUILD FAIL err=%s\n---\n%s\n", clerr(err), log);
        return 3;
    }
    cl_kernel ker = clCreateKernel(prog, "walk", &err);
    if (err != CL_SUCCESS) { printf("kernel err %s\n", clerr(err)); return 3; }

    // ---- data: 32 affine jumps d*G (d in [1, 2*sqrt(l)]), as in Phase 7 ----
    std::vector<A> jumps;
    {
        std::mt19937_64 rng(20260922);
        double sl = std::sqrt((double)TOY_L);
        for (int i = 0; i < 32; i++) {
            uint64_t d = 1 + (uint64_t)(rng() % (uint64_t)std::max(2.0, 2.0 * sl));
            jumps.push_back(J::mul(J::from_affine(TOY_Gx, TOY_Gy), d).to_affine());
        }
    }
    std::vector<uint64_t> jp(64);
    for (int i = 0; i < 32; i++) { jp[2 * i] = jumps[i].x; jp[2 * i + 1] = jumps[i].y; }

    std::vector<uint64_t> seeds(n_walkers * 2);
    {
        std::mt19937_64 rs(777);
        for (size_t i = 0; i < n_walkers; i++) {
            seeds[2 * i] = rs() % TOY_P; seeds[2 * i + 1] = (rs() % (TOY_P - 1)) + 1;
        }
    }

    cl_mem dJ = clCreateBuffer(ctx, CL_MEM_READ_WRITE | CL_MEM_COPY_HOST_PTR, jp.size() * sizeof(uint64_t), jp.data(), &err);
    cl_mem dS = clCreateBuffer(ctx, CL_MEM_READ_WRITE | CL_MEM_COPY_HOST_PTR, seeds.size() * sizeof(uint64_t), seeds.data(), &err);
    cl_mem dO = clCreateBuffer(ctx, CL_MEM_READ_WRITE, n_walkers * sizeof(uint64_t), NULL, &err);

    clSetKernelArg(ker, 0, sizeof(dJ), &dJ);
    clSetKernelArg(ker, 1, sizeof(dS), &dS);
    clSetKernelArg(ker, 2, sizeof(uint64_t), &iters);
    clSetKernelArg(ker, 3, sizeof(dO), &dO);

    size_t gsz = (size_t)n_walkers;
    std::vector<uint64_t> gpu_out(n_walkers);
    uint64_t tg = now_ns();
    err = clEnqueueNDRangeKernel(q, ker, 1, NULL, &gsz, NULL, 0, NULL, NULL);
    if (err != CL_SUCCESS) { printf("ndrange err %s\n", clerr(err)); return 3; }
    err = clEnqueueReadBuffer(q, dO, CL_TRUE, 0, gpu_out.size() * sizeof(uint64_t), gpu_out.data(), 0, NULL, NULL);
    clFinish(q);
    uint64_t gpu_ns = now_ns() - tg;
    uint64_t gpu_acc = 0; for (auto v : gpu_out) gpu_acc ^= v;

    // ---- CPU same-work reference (4 threads) ----
    uint64_t tc = now_ns();
    uint64_t cpu_acc = cpu_run(jumps, seeds, iters, 4);
    uint64_t cpu_ns = now_ns() - tc;

    uint64_t ops = n_walkers * iters;
    // rates in operations per second (dividing ns by 1e9)
    double gpu_gs = (double)ops / gpu_ns * 1e9;
    double cpu_gs = (double)ops / cpu_ns * 1e9;
    printf("gpu : %llu addmixes in %.1f ms (%.3f Mops/s) checksum=%016llx\n",
           ops, gpu_ns / 1e6, gpu_gs / 1e6, (unsigned long long)gpu_acc);
    printf("cpu : %llu addmixes in %.1f ms (%.3f Mops/s) checksum=%016llx  (4 threads, FpNaive)\n",
           ops, cpu_ns / 1e6, cpu_gs / 1e6, (unsigned long long)cpu_acc);
    int matched = (cpu_acc == gpu_acc);
    printf("match: %s | ratio GPU/CPU = %.2fx\n", matched ? "YES" : "NO", gpu_gs / cpu_gs);

    printf("phase8,ops,%llu,gpu_ms,%.1f,gpu_mops,%.3f,cpu_ms,%.1f,cpu_mops,%.3f,ratio,%.4f,matched,%d\n",
           ops, gpu_ns / 1e6, gpu_gs / 1e6, cpu_ns / 1e6, cpu_gs / 1e6, gpu_gs / cpu_gs, matched);

    clReleaseMemObject(dO); clReleaseMemObject(dS); clReleaseMemObject(dJ);
    clReleaseKernel(ker); clReleaseProgram(prog);
    clReleaseCommandQueue(q); clReleaseContext(ctx);
    return 0;
}