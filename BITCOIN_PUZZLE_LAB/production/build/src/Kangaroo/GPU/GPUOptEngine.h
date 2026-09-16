#ifndef GPUOPTENGINE_H
#define GPUOPTENGINE_H

// ============================================================================
// GPUOptEngine — host-side execution controller for the persistent kangaroo
// kernel (kernOpt, see GPUOptKernel.cu). Drop-in replacement for GPUEngine
// for the Tesla T4 / SM75 path.
//
// Kernel contract (must stay in sync with GPUOptKernel.cu):
//   state    kan[ b*(10*OPT_BLOCK_THREADS) + l*OPT_BLOCK_THREADS + t ]
//            l: 0..3 px, 4..7 py, 8..9 dist.  1 kangaroo per thread.
//   jump     jump[ OPT_NB_JUMP ][10]: {jx0..3, jy0..3, jd0,jd1}
//   dpOut    [4-word header][maxFound * 16-word entries]
//            header[0] published count, header[1] slot allocator.
//            entry {x[8](4×u64 LE), dist[8](2×u64 LE), kIdx[4](u64+pad)}.
//
// Host responsibilities implemented here:
//   1. Jump-table staging + upload   (SetParams)
//   2. Kangaroo state staging        (SetKangaroos/GetKangaroos/SetKangaroo)
//   3. DP arena (pinned + device)    (constructor, opt_dp_arena_size)
//   4. Persistent kernel launch + async stream management (Launch)
//   5. Collision/deadlock resolution: mid-run DP polling, arena-full stop
//      handling, item extraction for the host HashTable
//   6. Strict CUDA error checks + CUDA-event timing (Keys/s metrics)
//
// The DP buffer is filled concurrently with kernel execution; the kernel
// publishes entries with a release pattern (write entry, __threadfence,
// atomic count) so a polled counter always refers to fully-written slots.
// ============================================================================

#include <string>
#include <vector>
#include "../SECPK1/SECP256k1.h"
#include "../GPU/GPUEngine.h"   // ITEM, KSIZE, etc.

// ----------------------------------------------------------------------------
// Strict CUDA error macros. Abort host path on any failure.
// ----------------------------------------------------------------------------
#ifndef CUDA_CHK
#define CUDA_CHK(call)                                                        \
    do {                                                                      \
        cudaError_t _e = (call);                                              \
        if (_e != cudaSuccess) {                                              \
            fprintf(stderr, "CUDA error %s at %s:%d (%s)\n",                  \
                    cudaGetErrorString(_e), __FILE__, __LINE__, #call);       \
            fflush(stderr);                                                   \
            abort();                                                          \
        }                                                                     \
    } while (0)
#endif

class GPUOptEngine {

public:

    // nbThreadGroup/nbThreadPerGroup keep GPUEngine's calling signature.
    // nbThreadGroup  -> grid blocks (multiples of 32; 0 = auto-tuned).
    // nbThreadPerGroup -> ignored for launch shape; kernOpt is fixed at
    //                     OPT_BLOCK_THREADS per block. Kept for API parity.
    // maxFound       -> DP slots (arena sized maxFound*16 words).
    GPUOptEngine(int nbThreadGroup,int nbThreadPerGroup,int gpuId,
                 uint32_t maxFound);
    ~GPUOptEngine();

    // Jump tables. distance = jump distances (Int), px/py = jump point affine
    // coordinates. Arrays must be NB_JUMP long. Rebuilds the combined
    // [NB_JUMP][10] table on pinned memory and uploads to device.
    void SetParams(uint64_t dpMask,Int *distance,Int *px,Int *py);

    // Bulk kangaroo state. Arrays of GetNbThread() kangaroos, 4-limb Int.
    void SetKangaroos(Int *px,Int *py,Int *d);
    void GetKangaroos(Int *px,Int *py,Int *d);

    // Single-kangaroo reseed (used when a same-herd collision is detected so
    // the GPU herd does not die). kIdx is the global kangaroo serial.
    void SetKangaroo(uint64_t kIdx,Int *px,Int *py,Int *d);

    // Run one persistent-kernel chunk (opt_cfg.maxItersPerLaunch steps) while
    // polling the DP arena. Returns true when no CUDA error occurred. The
    // caller owns collision resolution: it feeds returned ITEMs to its
    // HashTable; for ADD_COLLISION it must reseed with SetKangaroo.
    bool Launch(std::vector<ITEM> &hashFound,bool spinWait = false);

    // Wild herd offset (added to wild distances device-side, subtracted on
    // retrieval). Needed for correct distance reconstruction.
    void SetWildOffset(Int *offset);

    void SetMaxItersPerLaunch(long long iters);

    // Query interface (GPUEngine parity)
    int  GetNbThread();      // number of herds (GPU_GRP_SIZE kangaroos each)
    int  GetGroupSize();     // kangaroos per block
    int  GetMemory();        // total device+pinned bytes
    std::string deviceName;

    // Throughput metrics
    double GetElapsedGPU();   // seconds, last chunk (CUDA event time)
    double GetKeysPerSec();   // last chunk keys/sec
    double GetItersPerSec();  // last chunk steps/sec

private:

    bool InitCUDA(int gpuId);
    void ResetDPCounter();
    void ForceStop();            // write 1 to the device stop-flag buffer
    void ClearStop();            // write 0 to the device stop-flag buffer
    size_t ArenaBytes() const;

    Int      wildOffset;
    uint64_t dpMask;
    uint32_t maxFound;
    long long maxItersPerLaunch;

    // Device memory
    uint64_t *kangarooDev;   // SoA state
    uint64_t *jumpDev;       // [NB_JUMP][10]
    uint32_t *dpDev;         // DP arena (device)
    uint32_t *stopDev;       // 1-word stop flag polled by kernOpt

    // Pinned host memory
    uint64_t *kangarooPinned;
    uint64_t *jumpPinned;
    uint32_t *dpPinned;

    // Streams/events
    cudaStream_t streamKernel;   // kernel launch stream
    cudaStream_t streamPoll;     // DP-poll H2D copies
    cudaEvent_t  evStart;        // kernel start
    cudaEvent_t  evStop;         // kernel end (elapsed time window)
    cudaEvent_t  evStaging;      // staging upload complete (default stream)

    int      gpuId;
    int      nbKangaroos;        // grid * OPT_BLOCK_THREADS
    int      blocksPerGrid;
    bool     initialised;
    bool     lostWarning;

    // Last-chunk metrics
    uint64_t lastChunkIters;
    double   lastElapsed;
    uint64_t lastChunkSteps;     // nbKangaroos * iters (for flushing reports)
};

#endif // GPUOPTENGINE_H