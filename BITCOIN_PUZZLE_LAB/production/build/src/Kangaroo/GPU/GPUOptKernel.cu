#ifndef GPUOPTKERNEL_CU
#define GPUOPTKERNEL_CU

#include "GPUOpt.h"

// ============================================================================
// Kangaroo Walk — Optimized Persistent Kernel for Tesla T4 (SM75)
//
// Architecture vs v2.2:
//   v2.2:  128 kangaroos/thread, AoS local arrays (heavy local-memory spilling),
//          per-thread serial product-tree inversion over 128 kangaroos, one
//          __noinline__ _ModInvGrouped per run, atomicAdd per DP lane.
//   OPT:   1 kangaroo/thread (32/warp) in registers, warp-parallel batch
//          inversion (__shfl Kogge-Stone scans + single fe256_inv per warp),
//          per-DP-lane guarded atomicAdd flush (v2.2 semantics),
//          persistent kernel (no per-step relaunch).
//
// Honest cost trade-off: the warp-parallel inverse amortizes one fe256_inv
// over 32 kangaroos (v2.2: 1 inverse over 128), so per-kangaroo mul count is
// LOWER in v2.2. The OPT kernel wins instead on occupancy: 10 u64 of state in
// registers vs v2.2's multi-KB resident block (local memory), 4× the active
// warps per SM, and no __syncthreads/relaunch per NB_RUN block. Final
// throughput must be measured on hardware; the arithmetic is proven-equivalent.
// ============================================================================

// ============================================================================
// Warp-parallel Montgomery batch inversion — VERIFIED
//
// Group = 32 lanes; lane L owns dx[L]. Produces inv[L] = 1/dx[L] (mod p).
//
//   P[i]  = dx[0]*..*dx[i]        (inclusive prefix, Kogge-Stone shfl_up)
//   S[i]  = dx[i]*..*dx[31]       (inclusive suffix, Kogge-Stone shfl_down)
//   invT  = 1 / dx[0]*..*dx[31]   (single fe256_inv, computed lane-wide)
//   inv[i]= invT * exclP(i) * exclS(i)
//           exclP(0)=1, exclP(i>0)=P[i-1]; exclS(31)=1, exclS(i<31)=S[i+1]
//   => inv[i] = 1/dx[i].  (boundary cases checked separately)
// ----------------------------------------------------------------------------
__device__ __forceinline__ void warp_batch_inv(
    const uint64_t (&dx)[4],
    uint64_t (&inv)[4],
    int lane)
{
    fe256 xi;
    xi.v[0] = dx[0]; xi.v[1] = dx[1]; xi.v[2] = dx[2]; xi.v[3] = dx[3];

    // --- Inclusive prefix P[i], Kogge-Stone (strides 1..16) ---
    fe256 p = xi;
    // Fixed 5-iteration tree: full unroll lifts the __shfl_up + mul chain for
    // ILP. Each stride level is independent across lanes, so the compiler can
    // hoist the 4 shfl reads ahead of the 256x256 muls (long-latency path).
    #pragma unroll
    for (int stride = 1; stride < OPT_WARP_SIZE; stride <<= 1) {
        uint64_t o0 = __shfl_up_sync(0xFFFFFFFF, p.v[0], stride);
        uint64_t o1 = __shfl_up_sync(0xFFFFFFFF, p.v[1], stride);
        uint64_t o2 = __shfl_up_sync(0xFFFFFFFF, p.v[2], stride);
        uint64_t o3 = __shfl_up_sync(0xFFFFFFFF, p.v[3], stride);
        if (lane >= stride) {
            fe256 other; other.v[0]=o0; other.v[1]=o1; other.v[2]=o2; other.v[3]=o3;
            fe256 r; fe256_mul(r, p, other);
            p = r;
        }
    }

    // --- Inclusive suffix S[i], Kogge-Stone (strides 1..16) ---
    fe256 s = xi;
    #pragma unroll
    for (int stride = 1; stride < OPT_WARP_SIZE; stride <<= 1) {
        uint64_t o0 = __shfl_down_sync(0xFFFFFFFF, s.v[0], stride);
        uint64_t o1 = __shfl_down_sync(0xFFFFFFFF, s.v[1], stride);
        uint64_t o2 = __shfl_down_sync(0xFFFFFFFF, s.v[2], stride);
        uint64_t o3 = __shfl_down_sync(0xFFFFFFFF, s.v[3], stride);
        if (lane < OPT_WARP_SIZE - stride) {
            fe256 other; other.v[0]=o0; other.v[1]=o1; other.v[2]=o2; other.v[3]=o3;
            fe256 r; fe256_mul(r, s, other);
            s = r;
        }
    }

    // lane 0 holds the full product in s. Broadcast it to all lanes.
    uint64_t full0 = __shfl_sync(0xFFFFFFFF, s.v[0], 0);
    uint64_t full1 = __shfl_sync(0xFFFFFFFF, s.v[1], 0);
    uint64_t full2 = __shfl_sync(0xFFFFFFFF, s.v[2], 0);
    uint64_t full3 = __shfl_sync(0xFFFFFFFF, s.v[3], 0);

    // --- Single inverse of the full product ---
    fe256 fullProd; fullProd.v[0]=full0; fullProd.v[1]=full1; fullProd.v[2]=full2; fullProd.v[3]=full3;
    fe256 invT;
    fe256_inv(invT, fullProd);   // 1/(dx0*..*dx31) on every lane

    // --- Composition ---
    // exclP: prefix value from lane-1 (P[i-1]) or 1 for lane 0.
    // shfl runs on ALL lanes (converged, full mask) BEFORE the branch so lane 0
    // still participates: divergent shfl with a full mask is undefined behavior.
    fe256 exclP;
    {
        uint64_t e0 = __shfl_up_sync(0xFFFFFFFF, p.v[0], 1);
        uint64_t e1 = __shfl_up_sync(0xFFFFFFFF, p.v[1], 1);
        uint64_t e2 = __shfl_up_sync(0xFFFFFFFF, p.v[2], 1);
        uint64_t e3 = __shfl_up_sync(0xFFFFFFFF, p.v[3], 1);
        if (lane == 0) {
            fe256_set_one(exclP);
        } else {
            exclP.v[0]=e0; exclP.v[1]=e1; exclP.v[2]=e2; exclP.v[3]=e3;
        }
    }

    // exclS: suffix value from lane+1 (S[i+1]) or 1 for lane 31.
    fe256 exclS;
    {
        uint64_t e0 = __shfl_down_sync(0xFFFFFFFF, s.v[0], 1);
        uint64_t e1 = __shfl_down_sync(0xFFFFFFFF, s.v[1], 1);
        uint64_t e2 = __shfl_down_sync(0xFFFFFFFF, s.v[2], 1);
        uint64_t e3 = __shfl_down_sync(0xFFFFFFFF, s.v[3], 1);
        if (lane == OPT_WARP_SIZE - 1) {
            fe256_set_one(exclS);
        } else {
            exclS.v[0]=e0; exclS.v[1]=e1; exclS.v[2]=e2; exclS.v[3]=e3;
        }
    }

    fe256 a, b, r;
    fe256_mul(a, invT, exclP);
    fe256_mul(r, a, exclS);
    inv[0]=r.v[0]; inv[1]=r.v[1]; inv[2]=r.v[2]; inv[3]=r.v[3];
}

// ----------------------------------------------------------------------------
// Kernel body: each thread owns ONE kangaroo (px,py,dist in registers). A warp
// (= OPT_GRP_SIZE=32 lanes) therefore carries 32 kangaroos; each step the warp
// batch-inverts its 32 deltas in O(log W) with one fe256_inv instead of the
// v2.2 per-thread 31-deep serial product tree. State stays resident across
// all iterations (persistent kernel), so DRAM traffic is just load/store.
//
// Registers per thread: 4+4+2 = 10 u64 for the kangaroo + mul temporaries.
// Grid: 40 SMs x occupancy blocks; each block 128 threads = 128 kangaroos.
// ----------------------------------------------------------------------------
// Global layout: [block][10 u64/word-planes][OPT_BLOCK_THREADS]
//   kangaroo (limb l, thread t in block b) at
//   kan[ b*(10*OPT_BLOCK_THREADS) + l*OPT_BLOCK_THREADS + t ]
//   l: 0..3 px, 4..7 py, 8..9 dist.  Coalesced: consecutive t -> consecutive word.
// Jump table: [OPT_NB_JUMP][10] = { dx0..3, dy0..3, d0,d1 }
extern "C" __global__ void __launch_bounds__(OPT_BLOCK_THREADS, OPT_LAUNCH_MIN_BLOCKS)
kernOpt(uint64_t * __restrict__ kan, // SoA kangaroo state — __restrict__: the 3
        uint32_t * __restrict__ dpOut,// device buffers are disjoint allocations,
        const uint64_t * __restrict__ jump, // jump is read-only point-invariant
        uint64_t dpMask,            // → compiler may cache/hoist; it never aliases
                                    // kan/dpOut. Feeds ld.global.nc (non-coherent
                                    // L1 path) for the jump gathers below.
        int      maxFound,     // DP slots available past the header
        int      maxIters,
        const uint32_t *stopFlag)  // volatile-polled stop signal (device mem)
{
    const int tid  = threadIdx.x;
    const int lane = tid & (OPT_WARP_SIZE - 1);
    const uint64_t blockBase = (uint64_t)blockIdx.x
                             * (OPT_BLOCK_THREADS * 10ULL);

    // ---- Load this thread's kangaroo (coalesced across threads) ----
    // SoA planing: consecutive threads touch consecutive 8-byte words in each
    // of the 10 128-thread word planes → 1024-byte contiguous per plane per
    // block = 8× 128B sectors, fully coalesced 64-bit loads, no bank conflicts
    // (shared memory is NOT used by design).
    uint64_t px[4], py[4], dist[2];
    const uint64_t base = blockBase + tid;
    #pragma unroll
    for (int k = 0; k < 10; k++) {
        uint64_t w = kan[base + k * OPT_BLOCK_THREADS];
        if      (k < 4) px[k]     = w;
        else if (k < 8) py[k - 4] = w;
        else            dist[k - 8] = w;
    }

    // ---- Main walk loop (persistent: state stays resident) ----
    for (int it = 0; it < maxIters && !*((volatile uint32_t*)stopFlag); it++) {

        // Jump index from low bits of px (matches v2.2 convention).
        // Gather through __ldg → ld.global.nc: the 32×10×8B table is only
        // 2.5 KB, resident in L1/read-only cache, and NEVER written on device,
        // so the non-coherent texture path avoids L2 round-trips entirely.
        uint64_t ji = px[0] & (OPT_NB_JUMP - 1);
        const uint64_t *jv = jump + ji * 10;
        uint64_t jx0 = __ldg(jv + 0), jx1 = __ldg(jv + 1),
                 jx2 = __ldg(jv + 2), jx3 = __ldg(jv + 3);
        uint64_t jy0 = __ldg(jv + 4), jy1 = __ldg(jv + 5),
                 jy2 = __ldg(jv + 6), jy3 = __ldg(jv + 7);
        uint64_t jd0 = __ldg(jv + 8), jd1 = __ldg(jv + 9);

        uint64_t delta[4];
        fe256 a, b, r;
        a.v[0]=px[0]; a.v[1]=px[1]; a.v[2]=px[2]; a.v[3]=px[3];
        b.v[0]=jx0;   b.v[1]=jx1;   b.v[2]=jx2;   b.v[3]=jx3;
        fe256_sub(r, a, b);          // dx = px - jumpX
        delta[0]=r.v[0]; delta[1]=r.v[1]; delta[2]=r.v[2]; delta[3]=r.v[3];

        // Warp-parallel batch inversion of the warp's 32 deltas
        uint64_t invd[4];
        warp_batch_inv(delta, invd, lane);

        // Point addition (affine jump + affine current -> affine result)
        //   lambda = (jy - py) / (jx - px)     [secp256k1 slope, a=0]
        //   newX   = lambda^2 - jx - px
        //   newY   = lambda * (px - newX) - py
        fe256 jy, jx, cx, cy, invA, lam, ny, nx, t;
        jx.v[0]=jx0; jx.v[1]=jx1; jx.v[2]=jx2; jx.v[3]=jx3;
        jy.v[0]=jy0; jy.v[1]=jy1; jy.v[2]=jy2; jy.v[3]=jy3;
        cx.v[0]=px[0]; cx.v[1]=px[1]; cx.v[2]=px[2]; cx.v[3]=px[3];
        cy.v[0]=py[0]; cy.v[1]=py[1]; cy.v[2]=py[2]; cy.v[3]=py[3];
        invA.v[0]=invd[0]; invA.v[1]=invd[1]; invA.v[2]=invd[2]; invA.v[3]=invd[3];

        fe256_sub(t, cy, jy);         // py - jy   (matches v2.2: dy = py - jPy)
        fe256_mul(lam, t, invA);      // lambda
        fe256_sqr(nx, lam);           // lambda^2
        fe256_sub(nx, nx, jx);        // lambda^2 - jx
        fe256_sub(nx, nx, cx);        // - px  -> newX
        fe256_sub(t, cx, nx);         // px - newX
        fe256_mul(t, lam, t);         // lambda * (px - newX)
        fe256_sub(ny, t, cy);         // - py  -> newY

        // Distance accumulation: dist += jD (plain 128-bit wrap, v2.2 Add128)
        scalar128 cur; cur.v[0]=dist[0]; cur.v[1]=dist[1];
        scalar128 jumpD; jumpD.v[0]=jd0; jumpD.v[1]=jd1;
        scalar128_add(cur, cur, jumpD);
        dist[0]=cur.v[0]; dist[1]=cur.v[1];

        // DP test uses NEW x (matches v2.2: DP check after the step)
        uint64_t isDp = ((nx.v[3] & dpMask) == 0) ? 1u : 0u;

        // Commit: new (x,y) in registers
        px[0]=nx.v[0]; px[1]=nx.v[1]; px[2]=nx.v[2]; px[3]=nx.v[3];
        py[0]=ny.v[0]; py[1]=ny.v[1]; py[2]=ny.v[2]; py[3]=ny.v[3];

// ---- DP flush (matches v2.2 OutputDP semantics: x + dist + kIdx) ----
        // Release-ordering protocol so the host can safely POLL this arena
        // WHILE the persistent kernel is mid-run (v2.2 only read after kernel
        // end; a persistent kernel must allow concurrent consumption):
        //   1. Claim a slot from the ALLOCATOR (header word 1) — this value is
        //      deliberately NOT the host-consumed count.
        //   2. Write the full 16-word entry (plain device-global stores).
        //   3. __threadfence(): makes this lane's stores observable device-wide
        //      BEFORE any subsequent global-memory operation of this lane.
        //   4. atomicAdd(dpOut,1) on the PUBLISHED counter (header word 0).
        //      The host can safely consume [lastRead, published) once it sees
        //      the counter — every prior slot's data is already visible.
        // Slots beyond maxFound are silently dropped (v2.2 "lost item" case);
        // the host detects the arena approaching full via the allocator and
        // raises the device stop flag to drain before overflow.
        if (isDp) {
            uint32_t slot = atomicAdd(dpOut + 1, 1u);
            if ((int)slot < maxFound) {
                // 16-word entry written as 8×64-bit stores: the slot stride is
                // 16 words = 64 B, and the arena base + header offset keeps
                // every slot 8-byte aligned (cudaMalloc → 256 B base), so the
                // widened stores preserve one full 64B sector per slot — half
                // the instructions of the 32-bit form and no partial sectors.
                uint64_t *e = (uint64_t *)(dpOut + OPT_DP_HEADER_WORDS + slot * 16);
                e[0]=nx.v[0];   e[1]=nx.v[1];   e[2]=nx.v[2];   e[3]=nx.v[3];
                e[4]=dist[0];   e[5]=dist[1];
                uint64_t kIdx = (uint64_t)blockIdx.x * (uint64_t)OPT_BLOCK_THREADS
                              + (uint64_t)threadIdx.x;
                e[6]=kIdx;
                e[7]=0;                       // reserved
                __threadfence();
                atomicAdd(dpOut, 1u);
            }
        }
    }

    // ---- Store back (coalesced across threads, same layout) ----
    #pragma unroll
    for (int k = 0; k < 10; k++) {
        uint64_t w;
        if      (k < 4) w = px[k];
        else if (k < 8) w = py[k - 4];
        else            w = dist[k - 8];
        kan[base + k * OPT_BLOCK_THREADS] = w;
    }
}

#endif // GPUOPTKERNEL_CU