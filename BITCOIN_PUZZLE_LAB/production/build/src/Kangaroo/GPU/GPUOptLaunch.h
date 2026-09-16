#ifndef GPUOPTLAUNCH_H
#define GPUOPTLAUNCH_H

#include "GPUOpt.h"
#include "GPUOptKernel.cu"

// ============================================================================
// Host-side launch configuration tuned for Tesla T4 (SM75)
// ============================================================================
//
// T4 SM75 resources per SM:
//   65536 registers/SM, 2048 threads/SM max, 64 warps/SM max,
//   96 KB shared mem/SM max, 4 warp schedulers.
//
// Kernel design (persistent, one kangaroo per thread):
//   - 128 threads/block = 4 warps; each warp carries 32 kangaroos.
//   - Persistent state per thread = 10 u64 (px,py,dist) → trivial registers.
//   - Per step: warp computes dx = px-jx for its 32 kangaroos, then ONE
//     warp-parallel batch inversion (Kogge-Stone prefix/suffix scans +
//     a single fe256_inv via square-and-multiply) replaces v2.2's per-thread
//     serial product tree over 128 kangaroos.
//   - __launch_bounds__(128, 8): compiler must cap registers at 64/thread
//     for 8 blocks/SM to be resident. Field-mul temporaries dominate; if it
//     spills we lower to 4 blocks/SM (128 regs) — measured by occupancy API.
//
// Total kangaroos in flight = grid * blockThreads (1 each).
//   40 SMs × 8 blocks/SM × 128 threads = 40,960 kangaroos.
// vs v2.2's 2560 threads × 128 = 327,680 kangaroos, but with 4× the warp
// parallelism at ¼ the per-thread state and O(log W) inversion amortization.
// ============================================================================

struct OptLaunchConfig {
    int blocksPerGrid;        // grid blocks (40 SMs × blocksPerSM)
    int threadsPerBlock;      // OPT_BLOCK_THREADS
    int kangaroosPerThread;   // 1 (register-resident, warp-parallel inv)
    int totalKangaroos;
    int maxItersPerLaunch;    // steps before host re-seeds / checks stop
};

// Auto-tuned config for the running device
inline bool opt_tune_config(OptLaunchConfig &cfg, int desiredKangaroos = 0) {
    int dev = 0;
    cudaGetDevice(&dev);

    cudaDeviceProp prop;
    if (cudaGetDeviceProperties(&prop, dev) != cudaSuccess) return false;

    // Blocks per SM: thread-limited for sm_75 (2048/128 = 16) but register-
    // limited. Use occupancy API to get the real achievable number.
    int numBlocksPerSM = 0;
    cudaOccupancyMaxActiveBlocksPerMultiprocessor(
        &numBlocksPerSM, kernOpt, OPT_BLOCK_THREADS, 0);

    if (numBlocksPerSM <= 0) numBlocksPerSM = 2;   // register-bound fallback

    // Target: fill all SMs with the achieved occupancy grid.
    int grid = prop.multiProcessorCount * numBlocksPerSM;

    cfg.threadsPerBlock    = OPT_BLOCK_THREADS;
    cfg.kangaroosPerThread = 1;
    cfg.blocksPerGrid      = grid;
    cfg.totalKangaroos     = grid * OPT_BLOCK_THREADS;
    cfg.maxItersPerLaunch  = 1 << 24;      // 16.7M steps then host checkpoint
    return true;
}

// Pinned host buffer sizing for the DP arena (one per GPU launch)
inline size_t opt_dp_arena_size(uint32_t maxFound) {
    // header (4 words) + maxFound DP entries × 16 words
    //   x (4×u64) + dist (2×u64) + reserved (4×u64 for kIdx etc.)
    return (OPT_DP_HEADER_WORDS + (size_t)maxFound * 16) * sizeof(uint32_t);
}

#endif // GPUOPTLAUNCH_H