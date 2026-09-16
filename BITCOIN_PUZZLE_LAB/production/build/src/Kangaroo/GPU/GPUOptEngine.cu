/*
 * GPUOptEngine.cu — Host execution controller for the persistent kangaroo
 * kernel (GPUOptKernel.cu) targeting Tesla T4 (SM 7.5).
 *
 * GPL-3.0. Portions derive from the BTCCollider/Kangaroo distribution
 * (https://github.com/JeanLucPons/Kangaroo) (c) 2020 Jean Luc PONS.
 */

#include <cstdio>
#include <cstring>
#include <cstdlib>
#include <stdint.h>
#include <string>

#ifdef _WIN32
#include <windows.h>
#else
#include <unistd.h>
#endif

#include <cuda.h>
#include <cuda_runtime.h>

#include "GPUOpt.h"         // scalar128, OPT_BLOCK_THREADS, OPT_NB_JUMP helpers
#include "GPUOptLaunch.h"   // opt_tune_config, opt_dp_arena_size, kernOpt decl
#include "GPUOptEngine.h"   // CUDA_CHK, Int, ITEM, GPUOptEngine

// The stop flag is a plain device buffer (avoids __managed__ host-write
// visibility caveats mid-run). The host stores 0 before launch and stores 1
// (via cudaMemsetAsync on the poll stream) to stop the persistent kernel
// early; the device polls it with a volatile load each iteration.

// ============================================================================
// Internal constants + helpers
// ============================================================================
#define OPT_DP_PUBLISHED 0u          // dpDev[0] : entries visible to host
#define OPT_DP_ALLOCATOR 1u          // dpDev[1] : reservations made by kernel
#define OPT_DP_STOP_MARGIN 1024u     // stop kernel when allocator this close
                                     // to maxFound (drain headroom)
#define OPT_POLL_INTERVAL_US 250     // poll sleep when not spinning

// Bytes of the SoA kangaroo buffer (kangaroo count shall match nbKangaroos).
static inline size_t opt_state_bytes(size_t n) {
    return n * 10u * sizeof(uint64_t);
}

static void opt_sleep_us(long usec) {
#ifdef _WIN32
    Sleep((DWORD)((usec + 999L) / 1000L));
#else
    usleep(static_cast<useconds_t>(usec));
#endif
}

// ============================================================================

GPUOptEngine::GPUOptEngine(int nbThreadGroup,int nbThreadPerGroup,int gpuId,
                           uint32_t maxFound)
    : wildOffset(), dpMask(0), maxFound(0), maxItersPerLaunch(0),
      kangarooDev(NULL), jumpDev(NULL), dpDev(NULL), stopDev(NULL),
      kangarooPinned(NULL), jumpPinned(NULL), dpPinned(NULL),
      streamKernel(0), streamPoll(0), evStart(0), evStop(0), evStaging(0),
      gpuId(gpuId), nbKangaroos(0), blocksPerGrid(0), initialised(false),
      lostWarning(false), lastChunkIters(0), lastElapsed(0.0),
      lastChunkSteps(0)
{
    if (!InitCUDA(gpuId)) return;
    this->maxFound = maxFound;

    OptLaunchConfig cfg;
    if (!opt_tune_config(cfg)) {
        fprintf(stderr,"GPUOptEngine: occupancy tuning failed\n");
        return;
    }

    // Grid: caller-specified block count wins, else auto-tuned occupancy.
    if (nbThreadGroup > 0)
        blocksPerGrid = nbThreadGroup;
    else
        blocksPerGrid = cfg.blocksPerGrid;

    this->maxItersPerLaunch = cfg.maxItersPerLaunch;
    this->nbKangaroos       = blocksPerGrid * OPT_BLOCK_THREADS;

    // Streams
    CUDA_CHK(cudaStreamCreateWithFlags(&streamKernel,cudaStreamNonBlocking));
    CUDA_CHK(cudaStreamCreateWithFlags(&streamPoll,cudaStreamNonBlocking));
    // evStart/evStop measure the kernel span -> timing enabled (default).
    CUDA_CHK(cudaEventCreate(&evStart));
    CUDA_CHK(cudaEventCreate(&evStop));
    CUDA_CHK(cudaEventCreateWithFlags(&evStaging,cudaEventDisableTiming));

    // State buffer (device + pinned staging, same SoA layout)
    size_t kangSize = opt_state_bytes(nbKangaroos);
    CUDA_CHK(cudaMalloc((void**)&kangarooDev,kangSize));
    CUDA_CHK(cudaHostAlloc(&kangarooPinned,kangSize,
                           cudaHostAllocMapped|cudaHostAllocWriteCombined));
    memset(kangarooPinned,0,kangSize);

    // Jump table (device + pinned)
    size_t jumpSize = (size_t)OPT_NB_JUMP * 10u * sizeof(uint64_t);
    CUDA_CHK(cudaMalloc((void**)&jumpDev,jumpSize));
    CUDA_CHK(cudaHostAlloc(&jumpPinned,jumpSize,
                           cudaHostAllocMapped|cudaHostAllocWriteCombined));
    memset(jumpPinned,0,jumpSize);

    // DP arena (device + pinned)
    size_t arenaBytes = (size_t)(OPT_DP_HEADER_WORDS + maxFound*16u)*sizeof(uint32_t);
    CUDA_CHK(cudaMalloc((void**)&dpDev,arenaBytes));
    CUDA_CHK(cudaHostAlloc(&dpPinned,arenaBytes,cudaHostAllocMapped));
    memset(dpPinned,0,arenaBytes);

    // Stop-flag buffer (1 word, device-only) polled by the kernel.
    CUDA_CHK(cudaMalloc((void**)&stopDev,sizeof(uint32_t)));
    CUDA_CHK(cudaMemset(stopDev,0,sizeof(uint32_t)));

    // Wait for staging allocations to be valid (single event on default ctx)
    CUDA_CHK(cudaEventRecord(evStaging,streamKernel));
    CUDA_CHK(cudaEventSynchronize(evStaging));

    initialised = true;
}

// ----------------------------------------------------------------------------

GPUOptEngine::~GPUOptEngine()
{
    if (initialised) {
        // Ensure no kernel still running before freeing any resource.
        CUDA_CHK(cudaStreamSynchronize(streamKernel));
    }
    if (kangarooDev)  cudaFree(kangarooDev);
    if (jumpDev)      cudaFree(jumpDev);
    if (dpDev)        cudaFree(dpDev);
    if (stopDev)      cudaFree(stopDev);
    if (kangarooPinned) cudaFreeHost(kangarooPinned);
    if (jumpPinned)     cudaFreeHost(jumpPinned);
    if (dpPinned)       cudaFreeHost(dpPinned);
    if (streamKernel) cudaStreamDestroy(streamKernel);
    if (streamPoll)   cudaStreamDestroy(streamPoll);
    if (evStart)      cudaEventDestroy(evStart);
    if (evStop)       cudaEventDestroy(evStop);
    if (evStaging)    cudaEventDestroy(evStaging);
}

// ----------------------------------------------------------------------------

bool GPUOptEngine::InitCUDA(int gpuId)
{
    int deviceCount = 0;
    cudaError_t err = cudaGetDeviceCount(&deviceCount);
    if (err != cudaSuccess) {
        fprintf(stderr,"GPUOptEngine: cudaGetDeviceCount: %s\n",
                cudaGetErrorString(err));
        return false;
    }
    if (deviceCount == 0) {
        fprintf(stderr,"GPUOptEngine: no CUDA device\n");
        return false;
    }
    if (gpuId >= deviceCount) {
        fprintf(stderr,"GPUOptEngine: invalid GPU id %d\n",gpuId);
        return false;
    }

    err = cudaSetDevice(gpuId);
    if (err != cudaSuccess) {
        fprintf(stderr,"GPUOptEngine: cudaSetDevice(%d): %s\n",
                gpuId,cudaGetErrorString(err));
        return false;
    }

    cudaDeviceProp prop;
    CUDA_CHK(cudaGetDeviceProperties(&prop,gpuId));

    char tmp[512];
    snprintf(tmp,sizeof(tmp),
             "GPU #%d %s (Cap %d.%d) %d SMs (%.0f MB)",gpuId,prop.name,
             prop.major,prop.minor,prop.multiProcessorCount,
             (double)prop.totalGlobalMem/1048576.0);
    deviceName = std::string(tmp);

    // No __shared__ use in kernOpt; maximize L1 cache for the local-memory
    // spill paths of the field-multiply temporaries.
    err = cudaDeviceSetCacheConfig(cudaFuncCachePreferL1);
    if (err != cudaSuccess) {
        fprintf(stderr,"GPUOptEngine: cudaDeviceSetCacheConfig: %s\n",
                cudaGetErrorString(err));
        return false;
    }

    return true;
}

// ----------------------------------------------------------------------------
// Jump table: host packs distance+point into vaulted [NB_JUMP][10] layout:
//   { jx[4], jy[4], jd[2] }   all little-endian u64
// ----------------------------------------------------------------------------

void GPUOptEngine::SetParams(uint64_t dpMask,Int *distance,Int *px,Int *py)
{
    this->dpMask = dpMask;

    for(int i = 0; i < OPT_NB_JUMP; i++) {
        uint64_t *dst = jumpPinned + (size_t)i * 10u;
        // jx
        dst[0] = px[i].bits64[0]; dst[1] = px[i].bits64[1];
        dst[2] = px[i].bits64[2]; dst[3] = px[i].bits64[3];
        // jy
        dst[4] = py[i].bits64[0]; dst[5] = py[i].bits64[1];
        dst[6] = py[i].bits64[2]; dst[7] = py[i].bits64[3];
        // jd (128-bit low limbs, full Int is clamped on device to wrap-add)
        dst[8] = distance[i].bits64[0];
        dst[9] = distance[i].bits64[1];
    }

    size_t jumpSize = (size_t)OPT_NB_JUMP * 10u * sizeof(uint64_t);
    CUDA_CHK(cudaMemcpyAsync(jumpDev,jumpPinned,jumpSize,
                             cudaMemcpyHostToDevice,streamKernel));
    CUDA_CHK(cudaStreamSynchronize(streamKernel));
    CUDA_CHK(cudaDeviceSynchronize());
}

// ----------------------------------------------------------------------------
// Kangaroo state: host Int arrays (herd-major, herd = block of 128) to SoA.
//   serial = b*OPT_BLOCK_THREADS + t
//   base   = b*(10*OPT_BLOCK_THREADS) + t
// Wild kangaroos get +wildOffset added device-side pre-add; stored raw here.
// ----------------------------------------------------------------------------

void GPUOptEngine::SetKangaroos(Int *px,Int *py,Int *d)
{
    if (!initialised || kangarooPinned == NULL) return;

    const int BLOCK = OPT_BLOCK_THREADS;
    for(int b = 0; b < blocksPerGrid; b++) {
        for(int t = 0; t < BLOCK; t++) {
            size_t serial = (size_t)b * BLOCK + (size_t)t;
            size_t base   = (size_t)b * (10u*(size_t)BLOCK) + (size_t)t;
            uint64_t *ks  = kangarooPinned + base;
            ks[0*BLOCK] = px[serial].bits64[0];
            ks[1*BLOCK] = px[serial].bits64[1];
            ks[2*BLOCK] = px[serial].bits64[2];
            ks[3*BLOCK] = px[serial].bits64[3];
            ks[4*BLOCK] = py[serial].bits64[0];
            ks[5*BLOCK] = py[serial].bits64[1];
            ks[6*BLOCK] = py[serial].bits64[2];
            ks[7*BLOCK] = py[serial].bits64[3];

            Int dOff;
            dOff.Set(&d[serial]);
            if(serial % 2 == WILD) dOff.ModAddK1order(&wildOffset);
            ks[8*BLOCK]  = dOff.bits64[0];
            ks[9*BLOCK]  = dOff.bits64[1];
        }
    }

    size_t kangSize = opt_state_bytes(nbKangaroos);
    CUDA_CHK(cudaMemcpyAsync(kangarooDev,kangarooPinned,kangSize,
                             cudaMemcpyHostToDevice,streamKernel));
    CUDA_CHK(cudaStreamSynchronize(streamKernel));
    CUDA_CHK(cudaDeviceSynchronize());
}

// ----------------------------------------------------------------------------

void GPUOptEngine::GetKangaroos(Int *px,Int *py,Int *d)
{
    if (!initialised || kangarooPinned == NULL) {
        fprintf(stderr,"GPUOptEngine: GetKangaroos: memory freed\n");
        return;
    }

    size_t kangSize = opt_state_bytes(nbKangaroos);
    CUDA_CHK(cudaStreamSynchronize(streamKernel));
    CUDA_CHK(cudaMemcpyAsync(kangarooPinned,kangarooDev,kangSize,
                             cudaMemcpyDeviceToHost,streamKernel));
    CUDA_CHK(cudaStreamSynchronize(streamKernel));

    const int BLOCK = OPT_BLOCK_THREADS;
    for(int b = 0; b < blocksPerGrid; b++) {
        for(int t = 0; t < BLOCK; t++) {
            size_t serial = (size_t)b * BLOCK + (size_t)t;
            size_t base   = (size_t)b * (10u*(size_t)BLOCK) + (size_t)t;
            const uint64_t *ks = kangarooPinned + base;
            px[serial].bits64[0] = ks[0*BLOCK];
            px[serial].bits64[1] = ks[1*BLOCK];
            px[serial].bits64[2] = ks[2*BLOCK];
            px[serial].bits64[3] = ks[3*BLOCK];
            px[serial].bits64[4] = 0;
            py[serial].bits64[0] = ks[4*BLOCK];
            py[serial].bits64[1] = ks[5*BLOCK];
            py[serial].bits64[2] = ks[6*BLOCK];
            py[serial].bits64[3] = ks[7*BLOCK];
            py[serial].bits64[4] = 0;
            d[serial].SetInt32(0);
            d[serial].bits64[0] = ks[8*BLOCK];
            d[serial].bits64[1] = ks[9*BLOCK];
            if(serial % 2 == WILD) d[serial].ModSubK1order(&wildOffset);
        }
    }
}

// ----------------------------------------------------------------------------

void GPUOptEngine::SetKangaroo(uint64_t kIdx,Int *px,Int *py,Int *d)
{
    if (!initialised) return;

    const int BLOCK = OPT_BLOCK_THREADS;
    int b = (int)(kIdx / BLOCK);
    int t = (int)(kIdx % BLOCK);
    if (b < 0 || b >= blocksPerGrid) return;

    // Synchronize so a residual kernel run does not overwrite the patch.
    CUDA_CHK(cudaStreamSynchronize(streamKernel));

    size_t base = (size_t)b * (10u*(size_t)BLOCK) + (size_t)t;
    uint64_t *ks = kangarooPinned + base;
    ks[0*BLOCK] = px->bits64[0];
    ks[1*BLOCK] = px->bits64[1];
    ks[2*BLOCK] = px->bits64[2];
    ks[3*BLOCK] = px->bits64[3];
    ks[4*BLOCK] = py->bits64[0];
    ks[5*BLOCK] = py->bits64[1];
    ks[6*BLOCK] = py->bits64[2];
    ks[7*BLOCK] = py->bits64[3];

    Int dOff;
    dOff.Set(d);
    if(kIdx % 2 == WILD) dOff.ModAddK1order(&wildOffset);
    ks[8*BLOCK] = dOff.bits64[0];
    ks[9*BLOCK] = dOff.bits64[1];

    // SoA layout: this kangaroo's 10 u64 limbs are strided by BLOCK, not
    // contiguous. Patch each plane element individually (8 bytes each).
    for(int l = 0; l < 10; l++) {
        CUDA_CHK(cudaMemcpyAsync(kangarooDev + base + (size_t)l * BLOCK,
                                 kangarooPinned + base + (size_t)l * BLOCK,
                                 sizeof(uint64_t),
                                 cudaMemcpyHostToDevice,streamKernel));
    }
    CUDA_CHK(cudaStreamSynchronize(streamKernel));
}

// ----------------------------------------------------------------------------
// DP arena housekeeping
// ----------------------------------------------------------------------------

size_t GPUOptEngine::ArenaBytes() const
{
    return (size_t)(OPT_DP_HEADER_WORDS + maxFound*16u) * sizeof(uint32_t);
}

void GPUOptEngine::ResetDPCounter()
{
    // Zero the published count and the allocator (header words only).
    CUDA_CHK(cudaMemsetAsync(dpDev,0,2u*sizeof(uint32_t),streamKernel));
}

void GPUOptEngine::ForceStop()
{
    // Device-side write of the stop flag from the host on streamPoll. Because
    // it is a plain device-global store issued while the kernel is running on
    // streamKernel, the persistent kernel observes it through its volatile
    // polled load on its next iteration.
    CUDA_CHK(cudaMemsetAsync(stopDev,1,sizeof(uint32_t),streamPoll));
    CUDA_CHK(cudaEventRecord(evStaging,streamPoll));
    CUDA_CHK(cudaEventSynchronize(evStaging));
}

void GPUOptEngine::ClearStop()
{
    // Zero the stop flag before (re)publishing the arena counters.
    CUDA_CHK(cudaMemsetAsync(stopDev,0,sizeof(uint32_t),streamKernel));
}

// ----------------------------------------------------------------------------
// Main launch. Runs maxItersPerLaunch steps, polling the DP arena on a second
// stream, extracting fully-published entries, and force-stopping the kernel
// when the DP budget is nearly exhausted so no entry is silently lost.
// ----------------------------------------------------------------------------

bool GPUOptEngine::Launch(std::vector<ITEM> &hashFound,bool spinWait)
{
    if (!initialised) return false;
    hashFound.clear();

    // Reset the run-time stop flag (device buffer, cleared on kernel stream
    // so it is zero before the kernel reads it).
    ClearStop();

    // 1. Zero published count + allocator, upload kangaroos, then launch
    //    the persistent kernel (all ordered on streamKernel).
    ResetDPCounter();
    CUDA_CHK(cudaEventRecord(evStaging,streamKernel));

    CUDA_CHK(cudaMemcpyAsync(kangarooDev,kangarooPinned,
                             opt_state_bytes(nbKangaroos),
                             cudaMemcpyHostToDevice,streamKernel));
    CUDA_CHK(cudaEventRecord(evStaging,streamKernel));

    CUDA_CHK(cudaEventRecord(evStart,streamKernel));
    kernOpt <<< blocksPerGrid,OPT_BLOCK_THREADS,0,streamKernel >>>
        (kangarooDev,dpDev,jumpDev,dpMask,maxFound,(int)maxItersPerLaunch,
         stopDev);
    CUDA_CHK(cudaGetLastError());

    CUDA_CHK(cudaEventRecord(evStop,streamKernel));

    // 2. Poll loop (deadlock-free): keep consuming DP entries while the
    //    kernel runs; stop the kernel early only if the arena is full.
    uint32_t lastPublished = 0;
    bool     forceStopped  = false;
    bool     kernelDone    = false;

    while (!kernelDone) {

        // Read both header words (published + allocator) via async H2D.
        // The release pattern in the kernel guarantees published->data order.
        CUDA_CHK(cudaMemcpyAsync(dpPinned,dpDev,2u*sizeof(uint32_t),
                                 cudaMemcpyDeviceToHost,streamPoll));
        CUDA_CHK(cudaStreamSynchronize(streamPoll));

        uint32_t published = dpPinned[OPT_DP_PUBLISHED];
        uint32_t allocator = dpPinned[OPT_DP_ALLOCATOR];

        // Consume the newly published entries.
        if (published > lastPublished) {
            size_t off = (size_t)OPT_DP_HEADER_WORDS + (size_t)lastPublished*16u;
            size_t nw  = (size_t)(published - lastPublished) * 16u;
            CUDA_CHK(cudaMemcpyAsync(dpPinned + off,dpDev + off,
                                     nw*sizeof(uint32_t),
                                     cudaMemcpyDeviceToHost,streamPoll));
            CUDA_CHK(cudaStreamSynchronize(streamPoll));

            uint32_t *e = dpPinned + OPT_DP_HEADER_WORDS;
            for(uint32_t i = lastPublished; i < published; i++) {

                uint32_t *it = e + (size_t)i*16u;

                ITEM item;
                item.kIdx = (uint64_t)it[12] | ((uint64_t)it[13] << 32);

                uint64_t *x = (uint64_t *)(it + 0);
                item.x.bits64[0]=x[0]; item.x.bits64[1]=x[1];
                item.x.bits64[2]=x[2]; item.x.bits64[3]=x[3];
                item.x.bits64[4]=0;

                uint64_t *d = (uint64_t *)(it + 8);
                item.d.bits64[0]=d[0]; item.d.bits64[1]=d[1];
                item.d.bits64[2]=0;    item.d.bits64[3]=0;
                item.d.bits64[4]=0;

                if(item.kIdx % 2 == WILD) item.d.ModSubK1order(&wildOffset);

                hashFound.push_back(item);
            }
            lastPublished = published;
        }

        // Arena-full guard: stop with drain headroom so concurrent
        // reservations never overflow into lost entries (guard the underflow
        // when maxFound is small).
        if (maxFound > OPT_DP_STOP_MARGIN &&
            allocator >= maxFound - OPT_DP_STOP_MARGIN && !forceStopped) {
            ForceStop();
            forceStopped = true;
        }

        // Kernel completion query.
        cudaError_t q = cudaEventQuery(evStop);
        if (q == cudaSuccess)       kernelDone = true;
        else if (q == cudaErrorNotReady) {
            if (!spinWait) {
                // Yield CPU while the GPU works (frees the host core).
                opt_sleep_us(OPT_POLL_INTERVAL_US);
            }
            // spinWait: busy-poll, no sleep.
        } else {
            CUDA_CHK(q);
        }
    }

    // 3. Kernel finished (event fired on kernel stream because we synced).
    CUDA_CHK(cudaStreamSynchronize(streamKernel));

    // Final drain for the last published entries (kernel fully stopped now).
    CUDA_CHK(cudaMemcpyAsync(dpPinned,dpDev,2u*sizeof(uint32_t),
                             cudaMemcpyDeviceToHost,streamPoll));
    CUDA_CHK(cudaStreamSynchronize(streamPoll));
    uint32_t publishedFinal = dpPinned[OPT_DP_PUBLISHED];

    if (publishedFinal > lastPublished) {
        size_t off = (size_t)OPT_DP_HEADER_WORDS + (size_t)lastPublished*16u;
        size_t nw  = (size_t)(publishedFinal - lastPublished) * 16u;
        CUDA_CHK(cudaMemcpyAsync(dpPinned + off,dpDev + off,
                                 nw*sizeof(uint32_t),
                                 cudaMemcpyDeviceToHost,streamPoll));
        CUDA_CHK(cudaStreamSynchronize(streamPoll));

        uint32_t *e = dpPinned + OPT_DP_HEADER_WORDS;
        for(uint32_t i = lastPublished; i < publishedFinal; i++) {
            uint32_t *it = e + (size_t)i*16u;
            ITEM item;
            item.kIdx = (uint64_t)it[12] | ((uint64_t)it[13] << 32);
            uint64_t *x = (uint64_t *)(it + 0);
            item.x.bits64[0]=x[0]; item.x.bits64[1]=x[1];
            item.x.bits64[2]=x[2]; item.x.bits64[3]=x[3];
            item.x.bits64[4]=0;
            uint64_t *d = (uint64_t *)(it + 8);
            item.d.bits64[0]=d[0]; item.d.bits64[1]=d[1];
            item.d.bits64[2]=0;    item.d.bits64[3]=0;
            item.d.bits64[4]=0;
            if(item.kIdx % 2 == WILD) item.d.ModSubK1order(&wildOffset);
            hashFound.push_back(item);
        }
    }

    // Arena-full bookkeeping (informational, matches v2.2 lost-item warning).
    uint32_t allocatorFinal = dpPinned[OPT_DP_ALLOCATOR];
    if (allocatorFinal > maxFound && !lostWarning) {
        fprintf(stderr,"\nWarning, %u items lost: DP arena full (increase "
                "maxFound or dp bit). Use -d to raise DP difficulty.\n",
                allocatorFinal - maxFound);
        lostWarning = true;
    }

    // 4. Timing: measure the kernel span only (evStart recorded right before the
    //    launch, evStop right after; both on the kernel stream).
    CUDA_CHK(cudaEventSynchronize(evStart));
    CUDA_CHK(cudaEventSynchronize(evStop));
    float ms = 0.0f;
    cudaError_t te = cudaEventElapsedTime(&ms,evStart,evStop);
    if (te == cudaSuccess) lastElapsed = (double)ms / 1000.0;
    else                   lastElapsed = 0.0;

    lastChunkIters = maxItersPerLaunch;
    lastChunkSteps = (uint64_t)nbKangaroos * (uint64_t)maxItersPerLaunch;

    CUDA_CHK(cudaGetLastError());
    return true;
}

// ----------------------------------------------------------------------------

void GPUOptEngine::SetWildOffset(Int *offset)
{
    wildOffset.Set(offset);
}

void GPUOptEngine::SetMaxItersPerLaunch(long long iters)
{
    if (iters > 0) maxItersPerLaunch = iters;
}

int GPUOptEngine::GetNbThread()
{
    // v2.2 parity: returns the herd/group count (the caller multiplies by
    // GPU_GRP_SIZE to obtain total kangaroos). Each block is one herd of
    // OPT_BLOCK_THREADS = GPU_GRP_SIZE = 128 kangaroos (1 per thread).
    return blocksPerGrid;
}

int GPUOptEngine::GetGroupSize()
{
    return OPT_BLOCK_THREADS;
}

int GPUOptEngine::GetMemory()
{
    size_t m = opt_state_bytes(nbKangaroos)
             + (size_t)OPT_NB_JUMP*10u*sizeof(uint64_t)
             + ArenaBytes();
    return (int)m;
}

double GPUOptEngine::GetElapsedGPU()
{
    return lastElapsed;
}

double GPUOptEngine::GetKeysPerSec()
{
    return (lastElapsed > 0.0) ? (double)lastChunkSteps / lastElapsed : 0.0;
}

double GPUOptEngine::GetItersPerSec()
{
    return (lastElapsed > 0.0)
         ? (double)nbKangaroos * (double)lastChunkIters / lastElapsed
         : 0.0;
}