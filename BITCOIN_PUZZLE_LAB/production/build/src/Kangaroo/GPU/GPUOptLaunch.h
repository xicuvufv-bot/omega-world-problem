#ifndef GPUOPTLAUNCH_H
#define GPUOPTLAUNCH_H

#include "GPUOpt.h"

// ============================================================================
// LARGE TU FIX — GPUOptKernel.cu is now a SEPARATE compilation unit.
//
// Previously GPUOptLaunch.h did `#include "GPUOptKernel.cu"`, which textually
// dragged the __global__ kernOpt (and every __device__ helper) into every TU
// that included this header. Any build that ALSO listed GPUOptKernel.cu on the
// nvcc command line then hit "multiple definition of kernOpt / warp_batch_inv /
// fe256_*" at link time.
//
// Fix: forward-declare kernOpt here (the exact signature is the contract used
// by opt_tune_config → cudaOccupancyMaxActiveBlocksPerMultiprocessor). The
// single definition lives in GPUOptKernel.cu, which MUST be compiled exactly
// once per executable.
//
// Build (Colab/Linux); note both .cu units:
//   nvcc -O3 -std=c++14 -gpu-architecture=... -c Kangaroo.cpp
//   nvcc -O3 -std=c++14 -gpu-architecture=... -c GPUOptEngine.cu
//   nvcc -O3 -std=c++14 -gpu-architecture=... -c GPUOptKernel.cu
//   (then link all objects; see build_gpuopt.sh)
// ============================================================================
extern "C" __global__ void kernOpt(
    uint64_t *kan,
    uint32_t *dpOut,
    const uint64_t *jump,
    uint64_t dpMask,
    int maxFound,
    int maxIters,
    const uint32_t *stopFlag);

// ============================================================================
// Host-side launch configuration — Tesla T4 (SM75) / L4 (SM89) / A100 (SM80)
// ============================================================================
//
// Resource budget per SM (same register file on all three):
//   65536 registers/SM, 2048 threads/SM max, 64 warps/SM max, 4 warp schedulers.
//
// Kernel design (persistent, one kangaroo per thread):
//   - 128 threads/block = 4 warps; each warp carries 32 kangaroos.
//   - Persistent state per thread = 10 u64 (px,py,dist) → trivial registers.
//   - Per step: warp computes dx = px-jx for its 32 kangaroos, then ONE
//     warp-parallel batch inversion (Kogge-Stone prefix/suffix scans +
//     a single fe256_inv via square-and-multiply) replaces v2.2's per-thread
//     serial product tree over 128 kangaroos.
//
// REGISTER-FIRST POLICY — __launch_bounds__(128, 2):
//   With 2 resident blocks/SM requested, ptxas budgets up to
//       floor(65536 / (2 * 128)) = 256 regs/thread,
//   so the field-mul temporaries NEVER spill (v2.2's 64-reg/thread cap at
//   8 blocks/SM was the #1 local-memory-spill source). T4/L4/A100 each keep
//   8 resident warps/SM (2 per scheduler), which is enough latency coverage
//   for a mul-heavy kernel: every warp has an independent 5-deep ILP tree in
//   the batch inversion. Do NOT raise the block count without re-measuring —
//   spilling back in costs more MIO throughput than the extra warps win.
//
// Fat-binary (the SAME source, no __CUDA_ARCH__ ifdefs needed — zero
// arch-specific intrinsics) for Colab's three GPU classes:
//
//   nvcc -O3 --use_fast_math -Xptxas -O3,-v \
//        -gencode arch=compute_75,code=sm_75  \   # T4
//        -gencode arch=compute_80,code=sm_80  \   # A100
//        -gencode arch=compute_89,code=sm_89  \   # L4
//        -o gpuopt.obj GPUOptEngine.cu
//
//   (--use_fast_math is inert for the u64 only field path — it only remaps
//    float/double libm; retained for the host-side timing/seed code that
//    mixes FP. -Xptxas -v prints the register/spill audit per arch.)
//
// Total kangaroos in flight = grid * blockThreads (1 each).
//   40 SMs × 2 blocks/SM × 128 threads = 10,240 kangaroos on T4 (register-
//   first policy); the occupancy API below reports the REAL achievable block
//   count for the register allocation ptxas actually emitted, so the grid
//   always fills the device no matter what was compiled.
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