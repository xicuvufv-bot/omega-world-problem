// ============================================================
// kangaroo_cuda.cu — T4 / T4x2 payload for the synthetic 70-bit
// interval ECDLP (interval [2^(B-1), 2^B), B=70, Q=k*G, k hidden).
//
// Group: secp256k1. Field arithmetic = the SAME plain right-shift
// reduction ops validated in v4_cpu_engine.cpp (36-bit solves pass,
// independent_verify=1). Every arithmetic routine is ship __device__
// AND __host__ so CPU/GPU results are bit-identical.
//
// Algorithm: parallel kangaroo (VOW) with an AFFINE-x driven walk
// (representation-independent jump tap + DP predicate — the exact
// bug class that broke the CPU engine until the affine fix).
// Per-step inversion is warp-batched (one Fermat inverse per 32
// lanes via the Montgomery trick). A simple per-lane kernel is kept
// for cross-check on-device.
//
// Multi-GPU (T4x2): each device owns its own buffers and writes
// DpRec's; the host merges all devices' DP dumps, finds tame/wild
// affine-x collisions, reconstructs k = d_tame - d_wild (mod n), and
// re-verifies k*G == Q on host before accepting.
//
// HONESTY CONTRACT (matches v4 CPU engine / STATE_SNAPSHOT):
//   * zero-guess: every figure is MEASURED on the actual hardware
//     at runtime; nothing theoretical.
//   * `selftest` first solves a KNOWN 24-bit key on-device and
//     verifies the recovered k == the secret (host compare).  A
//     failure aborts bench/solve.  Without an nvidia box this file
//     is STAGED ONLY — nothing below is a measured number yet.
//   * `solve` writes out.json; the Python orchestrator independently
//     re-verifies k*G == Q before the result counts.
//
// Build (on the GPU box; CUDA 12.x, T4 = sm_75):
//   nvcc -O3 -std=c++17 -arch=sm_75 -Xptxas -O3 -lineinfo \
//     -maxrregcount=80 -o kangaroo_cuda kangaroo_cuda.cu
//
// Usage:
//   kangaroo_cuda selftest [gpus]
//   kangaroo_cuda bench <sec> [dpbits] [gpus]
//   kangaroo_cuda prof <sec> [dpbits] [gpus]
//   kangaroo_cuda solve <challenge.json> <index> <out.json> \
//        [dpbits=24] [nTamePow=19] [nWildPow=19] [gpus=all]
//   kangaroo_cuda scale <lo> <hi> <rep> [dpbits] [gpus]
// ============================================================

#include <cuda_runtime.h>
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <string>
#include <vector>
#include <array>
#include <unordered_map>
#include <algorithm>
#include <chrono>
#include <thread>

typedef std::uint64_t u64;
typedef std::int64_t  i64;
typedef std::uint32_t u32;

#define CHECK_CUDA(x) do { cudaError_t _e = (x); if (_e != cudaSuccess) { \
    std::fprintf(stderr, "CUDA %s @ %s:%d: %s\n", #x, __FILE__, __LINE__, \
                 cudaGetErrorString(_e)); std::exit(1); } } while (0)

// ---------------- secp256k1 constants (identical to CPU engine) ----
// The field routines are __host__ __device__, and they pass these tables
// by pointer (ODR-use), so a host-side object has no device symbol.
// Device compilation therefore reads them from __constant__ memory while
// host compilation keeps ordinary host arrays; the macros redirect each
// compilation pass to the right symbol. The __constant__ mirrors stay
// visible to BOTH passes (nvcc's host stub must register them); only the
// macro redirects are pass-conditional.
__constant__ u64 P_d[4] = { 0xFFFFFFFEFFFFFC2FULL, 0xFFFFFFFFFFFFFFFFULL,
                     0xFFFFFFFFFFFFFFFFULL, 0xFFFFFFFFFFFFFFFFULL };
__constant__ u64 N_d[4] = { 0xBFD25E8CD0364141ULL, 0xBAAEDCE6AF48A03BULL,
                     0xFFFFFFFFFFFFFFFEULL, 0xFFFFFFFFFFFFFFFFULL };
__constant__ u64 CP_d[4] = { 0x1000003D1ULL, 0, 0, 0 };          // 2^256 - p
__constant__ u64 GX_d[4] = { 0x59F2815B16F81798ULL, 0x029BFCDB2DCE28D9ULL,
                      0x55A06295CE870B07ULL, 0x79BE667EF9DCBBACULL };
__constant__ u64 GY_d[4] = { 0x9C47D08FFB10D4B8ULL, 0xFD17B448A6855419ULL,
                      0x5DA4FBFC0E1108A8ULL, 0x483ADA7726A3C465ULL };
#ifdef __CUDA_ARCH__
#define P_ P_d
#define N_ N_d
#define CP_ CP_d
#define GX_ GX_d
#define GY_ GY_d
#else
static u64 P_[4] = { 0xFFFFFFFEFFFFFC2FULL, 0xFFFFFFFFFFFFFFFFULL,
                     0xFFFFFFFFFFFFFFFFULL, 0xFFFFFFFFFFFFFFFFULL };
static u64 N_[4] = { 0xBFD25E8CD0364141ULL, 0xBAAEDCE6AF48A03BULL,
                     0xFFFFFFFFFFFFFFFEULL, 0xFFFFFFFFFFFFFFFFULL };
static u64 CP_[4] = { 0x1000003D1ULL, 0, 0, 0 };          // 2^256 - p
static u64 GX_[4] = { 0x59F2815B16F81798ULL, 0x029BFCDB2DCE28D9ULL,
                      0x55A06295CE870B07ULL, 0x79BE667EF9DCBBACULL };
static u64 GY_[4] = { 0x9C47D08FFB10D4B8ULL, 0xFD17B448A6855419ULL,
                      0x5DA4FBFC0E1108A8ULL, 0x483ADA7726A3C465ULL };
#endif

// ============================================================
// field ops (4x u64 little-endian).  __device__ + __host__.
// ============================================================
__device__ __host__ __forceinline__
int cmpN(const u64* a, const u64* b, int n){
  for(int i=n-1;i>=0;i--){ if(a[i]!=b[i]) return a[i]<b[i]?-1:1; } return 0; }
__device__ __host__ __forceinline__
int isZeroN(const u64* a, int n){ for(int i=0;i<n;i++) if(a[i]) return 1; return 0; }
__device__ __host__ __forceinline__
void subPlain(u64* r, const u64* a, const u64* b, int n){
  u64 br=0;
  for(int i=0;i<n;i++){
    u64 x=a[i]-b[i];
    u64 br1=(a[i]<b[i])?1:0;
    u64 y=x-br;
    u64 br2=(x<br)?1:0;
    r[i]=y; br=br1|br2;
  }
}
__device__ __host__ __forceinline__
void addPlain(u64* r, const u64* a, const u64* b, int n){
  u64 c=0; for(int i=0;i<n;i++){ u64 s=a[i]+b[i]+c; c=(s<a[i])||(c&&s==a[i])?1:0; r[i]=s; } }
__device__ __host__ __forceinline__
void mulRaw(u64* out, const u64* x, int xn, const u64* y, int yn){
  for(int j=0;j<xn+yn;j++) out[j]=0;
  for(int j=0;j<yn;j++){
    u64 carry=0;
    for(int i=0;i<xn;i++){
      unsigned __int128 t=(unsigned __int128)x[i]*y[j]+out[i+j]+carry;
      out[i+j]=(u64)t; carry=(u64)(t>>64);
    }
    int k=j+xn;
    while(carry){ unsigned __int128 t=(unsigned __int128)out[k]+carry; out[k]=(u64)t; carry=(u64)(t>>64); k++; }
  }
}
__device__ __host__ __forceinline__
void reduceMod(u64* r, const u64* w, const u64* M, const u64* c){
  u64 t[8]={0,0,0,0,0,0,0,0};
  for(int i=0;i<8;i++) t[i]=w[i];
  for(int it=0;it<6;it++){
    int any=0; for(int i=4;i<8;i++) if(t[i]) any=1;
    if(!any) break;
    u64 hc[8]={0}; mulRaw(hc,&t[4],4,c,4);
    u64 lo[8]={0}; for(int i=0;i<4;i++) lo[i]=t[i];
    u64 s[8]={0}; addPlain(s,lo,hc,8);
    for(int i=0;i<8;i++) t[i]=s[i];
  }
  for(int k=0;k<4;k++){ if(cmpN(t,M,4)>=0){ u64 ss[4]; subPlain(ss,t,M,4); for(int i=0;i<4;i++) t[i]=ss[i]; } }
  for(int i=0;i<4;i++) r[i]=t[i];
}
__device__ __host__ __forceinline__ void fpAdd(u64*r,const u64*a,const u64*b){
  u64 t[5]={0,0,0,0,0}; u64 c=0;
  for(int i=0;i<4;i++){ u64 s=a[i]+b[i]+c; c=(s<a[i])||(c&&s==a[i])?1:0; t[i]=s; }
  t[4]=c;
  if(t[4]||cmpN(t,P_,4)>=0){ u64 pp[5]={P_[0],P_[1],P_[2],P_[3],0}; subPlain(t,t,pp,5); }
  for(int i=0;i<4;i++) r[i]=t[i];
}
__device__ __host__ __forceinline__ void fpSub(u64*r,const u64*a,const u64*b){
  if(cmpN(a,b,4)>=0) subPlain(r,a,b,4);
  else { u64 t[4],s[4]; subPlain(t,b,a,4); subPlain(s,P_,t,4); for(int i=0;i<4;i++) r[i]=s[i]; } }
__device__ __host__ __forceinline__ void fpMul(u64*r,const u64*a,const u64*b){ u64 w[8]; mulRaw(w,a,4,b,4); reduceMod(r,w,P_,CP_); }
__device__ __host__ __forceinline__ void fpSqr(u64*r,const u64*a){ fpMul(r,a,a); }
__device__ __host__ __forceinline__ void fpNeg(u64*r,const u64*a){
  if(!isZeroN(a,4)){ u64 z[4]={0,0,0,0}; for(int i=0;i<4;i++) r[i]=z[i]; }
  else subPlain(r,P_,a,4);
}
__device__ __host__ void fpPow(u64* r, const u64* a, const u64* e){
  u64 base[4]; for(int i=0;i<4;i++) base[i]=a[i];
  u64 res[4]={1,0,0,0};
  for(int bi=255;bi>=0;bi--){
    fpSqr(res,res);
    if((e[bi>>6]>>(bi&63))&1ULL) fpMul(res,res,base);
  }
  for(int i=0;i<4;i++) r[i]=res[i];
}
__device__ __host__ void fpInv(u64* r,const u64* a){ u64 e[4]; for(int i=0;i<4;i++) e[i]=P_[i]; e[0]-=2; fpPow(r,a,e); }
__device__ __host__ __forceinline__ void nAdd(u64*r,const u64*a,const u64*b){
  u64 t[5]={0,0,0,0,0}; u64 c=0;
  for(int i=0;i<4;i++){ u64 s=a[i]+b[i]+c; c=(s<a[i])||(c&&s==a[i])?1:0; t[i]=s; }
  t[4]=c;
  if(t[4]||cmpN(t,N_,4)>=0){ u64 nn[5]={N_[0],N_[1],N_[2],N_[3],0}; subPlain(t,t,nn,5); }
  for(int i=0;i<4;i++) r[i]=t[i];
}
__device__ __host__ __forceinline__ void nSub(u64*r,const u64*a,const u64*b){
  if(cmpN(a,b,4)>=0) subPlain(r,a,b,4);
  else { u64 t[4],s[4]; subPlain(t,b,a,4); subPlain(s,N_,t,4); for(int i=0;i<4;i++) r[i]=s[i]; } }

// ============================================================
// Jacobian point ops (bit-identical to CPU engine jDbl/jAddAff)
// ============================================================
struct JP { u64 X[4],Y[4],Z[4]; };
__device__ __host__ __forceinline__ void jpZero(JP& p){
  for(int i=0;i<4;i++){ p.X[i]=p.Y[i]=p.Z[i]=0; } }
__device__ __host__ __forceinline__ int jpInf(const JP& p){ return isZeroN(p.Z,4)?0:1; }

__device__ __host__ void jDbl(JP& R, const JP& P){
  if(jpInf(P)){ jpZero(R); return; }
  u64 A[4],B[4],C[4],D[4],E[4],F[4],t[4],u[4],Y1[4],Z1[4];
  if(!isZeroN(P.Y,4)){ jpZero(R); return; }  // no order-2 point on secp256k1 subgroup, defensive
  for(int i=0;i<4;i++){ Y1[i]=P.Y[i]; Z1[i]=P.Z[i]; }  // snapshot: R may alias P
  fpSqr(A,P.X);
  fpSqr(B,P.Y);
  fpSqr(C,B);
  fpAdd(t,P.X,B); fpSqr(t,t); fpSub(t,t,A); fpSub(t,t,C); fpAdd(D,t,t);
  fpAdd(E,A,A); fpAdd(E,E,A);
  fpSqr(F,E);
  fpAdd(t,D,D); fpSub(R.X,F,t);
  fpSub(t,D,R.X); fpMul(t,E,t);
  fpAdd(u,C,C); fpAdd(u,u,u); fpAdd(u,u,u);
  fpSub(R.Y,t,u);
  fpMul(u,Y1,Z1); fpAdd(R.Z,u,u);
}

__device__ __host__ void jAddAff(JP& R, const JP& J, const u64* a2, const u64* b2){
  if(jpInf(J)){ for(int i=0;i<4;i++){ R.X[i]=a2[i]; R.Y[i]=b2[i]; R.Z[i]=0; } R.Z[0]=1; return; }
  u64 Z1Z1[4],U2[4],S2[4],H[4],I[4],J2[4],RR[4],V[4],t[4],u[4];
  fpSqr(Z1Z1,J.Z);
  fpMul(U2,a2,Z1Z1);
  fpMul(t,J.Z,Z1Z1); fpMul(S2,b2,t);
  fpSub(H,U2,J.X);
  if(!isZeroN(H,4)){
    if(cmpN(S2,J.Y,4)==0){ jDbl(R,J); return; }
    jpZero(R); return;
  }
  fpAdd(t,H,H); fpSqr(I,t);
  fpMul(J2,H,I);
  fpSub(t,S2,J.Y); fpAdd(RR,t,t);
  fpMul(V,J.X,I);
  fpSqr(t,RR); fpAdd(u,V,V); fpAdd(u,u,J2);
  fpSub(R.X,t,u);
  fpSub(t,V,R.X); fpMul(t,RR,t);
  fpMul(u,J.Y,J2); fpAdd(u,u,u);
  fpSub(R.Y,t,u);
  fpAdd(u,J.Z,H); fpSqr(u,u); fpSub(u,u,Z1Z1); fpSqr(t,H); fpSub(R.Z,u,t);
}

__device__ __host__ void jToAff(u64* ax,u64* ay,const JP& P){
  u64 zi[4],z2[4],z3[4]; fpInv(zi,P.Z); fpSqr(z2,zi); fpMul(z3,z2,zi);
  fpMul(ax,P.X,z2); fpMul(ay,P.Y,z3);
}

__device__ __host__ void scalarMult(JP& R, const u64* k, int bits){
  jpZero(R);
  int started=0;
  for(int bi=bits-1;bi>=0;bi--){
    if(started) jDbl(R,R);
    if((k[bi>>6]>>(bi&63))&1ULL){
      if(started){ JP t; jAddAff(t,R,GX_,GY_); R=t; }
      else { for(int i=0;i<4;i++){ R.X[i]=GX_[i]; R.Y[i]=GY_[i]; R.Z[i]=0; } R.Z[0]=1; started=1; }
    }
  }
  if(!started) jpZero(R);
}

__device__ __host__ __forceinline__ u64 xs64(u64* s){
  u64 x=*s; x^=(x<<13); x^=(x>>7); x^=(x<<17); *s=x; return x;
}
// interval start/tame/wild distance: uniform in [2^(bits-1), 2^bits)
__device__ __host__ __forceinline__ void randIntervalX(u64* r,int bits,u64* s){
  for(int i=0;i<4;i++) r[i]=xs64(s);
  int q=(bits-1)>>6, rem=(bits-1)&63;
  for(int i=q+1;i<4;i++) r[i]=0;
  if(rem<63) r[q]&=((1ULL<<(rem+1))-1);
  r[q]|=(1ULL<<rem);
}
// jump distance: uniform in [0, 2^bits) under the top bit, guaranteed nonzero
// (matches validated CPU v4 buildJumps distribution, minus the d==0 hole).
__device__ __host__ __forceinline__ void randJump(u64* r,int bits,u64* s){
  u64 tmp[4]; for(int i=0;i<4;i++) tmp[i]=xs64(s);
  int q=(bits-1)>>6, rem=(bits-1)&63;
  for(int i=q+1;i<4;i++) tmp[i]=0;
  if(rem<63) tmp[q]&=((1ULL<<(rem+1))-1);
  int nonzero=0; for(int i=0;i<4;i++) if(tmp[i]) nonzero=1;
  if(!nonzero) tmp[q]=1;
  for(int i=0;i<4;i++) r[i]=tmp[i];
}

// ============================================================
// KANGAROO payload
// ============================================================
#define W_          64
#define MAXDP_GLOBAL (1u<<20)   // per-device record buffer; rounds typically fill ~1<<14

struct JumpEnt { u64 d[4]; u64 x[4], y[4]; };
struct Start   { JP pt; u64 d[4]; int tame; };
struct __align__(64) DpRec { u64 x[4]; u64 d[4]; u32 kind; u32 dev; };

// ---- device: jump table generation (one block of W threads) ----
__global__ void genJumpsKernel(JumpEnt* out, int wbits, u64 seed){
  int i=threadIdx.x; if(i>=W_) return;
  u64 s = seed ^ ((u64)i*0x9E3779B97F4A7C15ULL);
  u64 d[4]; randJump(d,wbits,&s);
  JP t; scalarMult(t,d,wbits);
  u64 ay[4]; jToAff(out[i].x,out[i].y,t);
  for(int k=0;k<4;k++) out[i].d[k]=d[k];
}

// ---- device: tame/wild start generation (one thread per start) ----
__global__ void genStartsKernel(Start* out, int nT, int nW, int bits, u64 seed,
                                const u64* Qx, const u64* Qy){
  int i=blockIdx.x*blockDim.x+threadIdx.x;
  int n=nT+nW;
  if(i>=n) return;
  u64 s = seed ^ ((u64)i*0x9E3779B97F4A7C15ULL) ^ 0x11111111ULL;
  if(i<nT){
    u64 d[4]; randIntervalX(d,bits,&s);
    JP t; scalarMult(t,d,bits);
    out[i].pt=t; out[i].tame=1;
    for(int k=0;k<4;k++) out[i].d[k]=d[k];
  } else {
    u64 d[4]; randIntervalX(d,bits,&s);
    JP t; scalarMult(t,d,bits);
    JP Wp; jAddAff(Wp,t,Qx,Qy);
    out[i].pt=Wp; out[i].tame=0;
    for(int k=0;k<4;k++) out[i].d[k]=d[k];
  }
}

// ---- simple per-lane walk (cross-check and selftest) ----
__global__ void walkKernelSimple(const JumpEnt* __restrict__ J,
                                 const Start* __restrict__ starts, int nStart,
                                 int dpbits, int maxSteps,
                                 DpRec* __restrict__ dpBuf,
                                 unsigned* __restrict__ dpCount,
                                 volatile int* __restrict__ stopFlag,
                                 u64* __restrict__ actStep){
  int t=blockIdx.x*blockDim.x+threadIdx.x;
  if(t>=nStart) return;
  JP pt=starts[t].pt;
  u64 d[4]; for(int k=0;k<4;k++) d[k]=starts[t].d[k];
  int tame=starts[t].tame;
  u64 m=(dpbits>=64)?~0ULL:((1ULL<<dpbits)-1);
  u64 ax[4],ay[4]; jToAff(ax,ay,pt);
  int ran;
  for(ran=0;ran<maxSteps;ran++){
    // whole-warp stop check (converged: no lane exits the warp early)
    if(*stopFlag) break;
    u32 idx=(u32)(ax[0]&(W_-1));
    jAddAff(pt,pt,J[idx].x,J[idx].y);
    nAdd(d,d,J[idx].d);
    jToAff(ax,ay,pt);
    if((ax[0]&m)==0){
      unsigned slot=atomicAdd(dpCount,1u);
      if(slot<MAXDP_GLOBAL){
        for(int k=0;k<4;k++){ dpBuf[slot].x[k]=ax[k]; dpBuf[slot].d[k]=d[k]; }
        dpBuf[slot].kind=tame?0u:1u;
        dpBuf[slot].dev=0;
      } else { atomicExch((int*)stopFlag,1); }
    }
  }
  actStep[t]=(u64)ran;
}

// ---- batched (warp) walk : one walker per lane, warp lockstep ----
// One Fermat inverse per 32 lanes per step (Montgomery batch trick).
__device__ __forceinline__ void warpBatchInv(u64 out[4], const u64* den){
  int lane=threadIdx.x&31;
  // per-lane den stays on its lane: all scan values are per-lane registers.
  u64 pre0=den[0], pre1=den[1], pre2=den[2], pre3=den[3];
  u64 d0=pre0,d1=pre1,d2=pre2,d3=pre3;
  for(int ds=1;ds<=16;ds<<=1){
    u64 v0=__shfl_up_sync(0xffffffffu,pre0,ds), v1=__shfl_up_sync(0xffffffffu,pre1,ds),
        v2=__shfl_up_sync(0xffffffffu,pre2,ds), v3=__shfl_up_sync(0xffffffffu,pre3,ds);
    if(lane>=ds){ u64 a[4]={pre0,pre1,pre2,pre3}, b[4]={v0,v1,v2,v3}, c[4];
      fpMul(c,a,b); pre0=c[0]; pre1=c[1]; pre2=c[2]; pre3=c[3]; }
  }
  u64 inv40,inv41,inv42,inv43;
  if(lane==31){ u64 a[4]={pre0,pre1,pre2,pre3}, c[4]; fpInv(c,a);
    inv40=c[0]; inv41=c[1]; inv42=c[2]; inv43=c[3]; }
  inv40=__shfl_sync(0xffffffffu,inv40,31); inv41=__shfl_sync(0xffffffffu,inv41,31);
  inv42=__shfl_sync(0xffffffffu,inv42,31); inv43=__shfl_sync(0xffffffffu,inv43,31);
  // exclusive suffix scan: s_i = product of den_{i+1..31}
  // (accumulate: s_i = s_i * s_{i+ds} * den_{i+ds})
  u64 s0=1,s1=0,s2=0,s3=0;
  for(int ds=1;ds<=16;ds<<=1){
    u64 vd0=__shfl_down_sync(0xffffffffu,d0,ds), vd1=__shfl_down_sync(0xffffffffu,d1,ds),
        vd2=__shfl_down_sync(0xffffffffu,d2,ds), vd3=__shfl_down_sync(0xffffffffu,d3,ds);
    u64 vs0=__shfl_down_sync(0xffffffffu,s0,ds), vs1=__shfl_down_sync(0xffffffffu,s1,ds),
        vs2=__shfl_down_sync(0xffffffffu,s2,ds), vs3=__shfl_down_sync(0xffffffffu,s3,ds);
    if(lane+ds<32){
      u64 a[4]={s0,s1,s2,s3}, b[4]={vs0,vs1,vs2,vs3}, c[4];
      fpMul(c,a,b);
      u64 g[4]={vd0,vd1,vd2,vd3}, h[4];
      fpMul(h,c,g);
      s0=h[0]; s1=h[1]; s2=h[2]; s3=h[3];
    }
  }
  // exclusive prefix prex = inclusive-prefix of lane-1
  u64 px0,px1,px2,px3;
  if(lane==0){ px0=1; px1=0; px2=0; px3=0; }
  else { px0=__shfl_up_sync(0xffffffffu,pre0,1); px1=__shfl_up_sync(0xffffffffu,pre1,1);
         px2=__shfl_up_sync(0xffffffffu,pre2,1); px3=__shfl_up_sync(0xffffffffu,pre3,1); }
  u64 a[4]={inv40,inv41,inv42,inv43}, b[4]={px0,px1,px2,px3}, c[4];
  fpMul(c,a,b);
  u64 e[4]={s0,s1,s2,s3}; fpMul(out,c,e);
}

__global__ void walkKernelBatch(const JumpEnt* __restrict__ J,
                                const Start* __restrict__ starts, int nStart,
                                int dpbits, int maxSteps,
                                DpRec* __restrict__ dpBuf,
                                unsigned* __restrict__ dpCount,
                                volatile int* __restrict__ stopFlag,
                                u64* __restrict__ actStep){
  int t=blockIdx.x*blockDim.x+threadIdx.x;
  if(t>=nStart) return;
  int lane=threadIdx.x&31;
  JP pt; for(int k=0;k<4;k++){ pt.X[k]=starts[t].pt.X[k]; pt.Y[k]=starts[t].pt.Y[k]; pt.Z[k]=starts[t].pt.Z[k]; }
  u64 d[4]; for(int k=0;k<4;k++) d[k]=starts[t].d[k];
  int tame=starts[t].tame;
  u64 m=(dpbits>=64)?~0ULL:((1ULL<<dpbits)-1);
  u64 ax[4];
  int ran;
  for(ran=0;ran<maxSteps;ran++){
    // whole-warp stop check (converged: no lane exits the warp early,
    // keeping the __shfl_sync(0xffffffff) lockstep inside warpBatchInv valid)
    if(*stopFlag) break;
    // affine x of the CURRENT point via warp-batched inversion (one inv/32 lanes)
    u64 z2[4]; fpSqr(z2,pt.Z);
    u64 invz[4]; warpBatchInv(invz,z2);
    fpMul(ax,pt.X,invz);
    u32 idx=(u32)(ax[0]&(W_-1));
    if((ax[0]&m)==0){
      unsigned slot=atomicAdd(dpCount,1u);
      if(slot<MAXDP_GLOBAL){
        for(int k=0;k<4;k++){ dpBuf[slot].x[k]=ax[k]; dpBuf[slot].d[k]=d[k]; }
        dpBuf[slot].kind=tame?0u:1u;
        dpBuf[slot].dev=0;
      } else { atomicExch((int*)stopFlag,1); }
    }
    jAddAff(pt,pt,J[idx].x,J[idx].y);
    nAdd(d,d,J[idx].d);
  }
  actStep[t]=(u64)ran;
}

// ============================================================
// host helpers
// ============================================================
static void usage(){
  std::printf(
    "kangaroo_cuda <cmd>\n"
    "  selftest [gpus]\n"
    "  bench <sec> [dpbits] [gpus]\n"
    "  solve <challenge.json> <index> <out.json> [dpbits=24] [nTamePow=19] [nWildPow=19] [gpus=all]\n"
    "  scale <lo> <hi> <rep> [dpbits] [gpus]\n");
}
static int deviceCount(){ int n=0; cudaGetDeviceCount(&n); return n<1?0:n; }

static bool readFile(const std::string& p, std::string& buf){
  FILE* f=fopen(p.c_str(),"rb"); if(!f) return false;
  fseek(f,0,SEEK_END); long n=ftell(f); fseek(f,0,SEEK_SET);
  buf.resize(n>0?(size_t)n:0);
  if(n>0) fread(&buf[0],1,(size_t)n,f);
  fclose(f); return true;
}
static int hexVal(char c){
  if(c>='0'&&c<='9') return c-'0';
  if(c>='a'&&c<='f') return 10+c-'a';
  if(c>='A'&&c<='F') return 10+c-'A';
  return 0;
}
static void hexToLimbs(const std::string& h, u64 r[4]){
  memset(r,0,32);
  size_t n=h.size();
  for(size_t i=0;i<n;i++){
    int v=hexVal(h[n-1-i]);
    size_t limb=i/16, off=i%16;
    r[limb]|=((u64)v)<<(off*4);
  }
}
static std::string limbsToHex(const u64 r[4]){
  char buf[128]; int n=0; buf[n++]='0'; buf[n++]='x';
  char tmp[17];
  for(int i=3;i>=0;i--){ sprintf(tmp,"%016llx",(unsigned long long)r[i]); memcpy(buf+n,tmp,16); n+=16; }
  buf[n]=0; return std::string(buf);
}

// locate instance `target` and read its "bits", "Qx", "Qy"
static bool parseQ(const std::string& json, int target, int* bits, u64 Qx[4], u64 Qy[4]){
  const char* s=json.c_str();
  size_t pos=0; int idx=-1;
  for(;;){
    const char* p=strstr(s+pos,"\"index\"");
    if(!p) break;
    const char* c=p+6; while(*c&&(*c<'0'||*c>'9')) c++;
    int val=0; while(*c>='0'&&*c<='9'){ val=val*10+(*c-'0'); c++; }
    idx=val; pos=(size_t)(p-s)+1;
    if(idx==target) break;
  }
  if(idx!=target) return false;
  const char* pb=strstr(s+pos,"\"bits\""); 
  int bv=0;
  if(pb){ const char* c=pb+5; while(*c&&(*c<'0'||*c>'9')) c++; while(*c>='0'&&*c<='9'){ bv=bv*10+(*c-'0'); c++; } }
  const char* px=strstr(s+pos,"\"Qx\"");
  const char* py=strstr(s+pos,"\"Qy\"");
  if(!px||!py) return false;
  const char* hx=strstr(px,"0x"); const char* hy=strstr(py,"0x");
  if(!hx||!hy) return false;
  std::string sx, sy;
  const char* c=hx+2; while(*c&&*c!='"') sx+=*c++;
  c=hy+2; while(*c&&*c!='"') sy+=*c++;
  hexToLimbs(sx,Qx); hexToLimbs(sy,Qy);
  if(bits) *bits=bv;
  return true;
}

// host merge: insert DPs, on tame/wild affine-x collision recover k and
// verify k*G == Q on host. outK/found set on success.
static void mergeDps(std::unordered_map<std::string,std::pair<std::array<u64,4>,int>>& tab,
                     const DpRec* recs, int n,
                     const u64* Qx, const u64* Qy,
                     u64* outK, int* found){
  for(int i=0;i<n;i++){
    std::string key=limbsToHex(recs[i].x);
    auto it=tab.find(key);
    if(it!=tab.end()){
      if(it->second.second!=(int)recs[i].kind){
        u64 k[4];
        if(recs[i].kind==1) nSub(k,it->second.first.data(),recs[i].d);
        else nSub(k,recs[i].d,it->second.first.data());
        JP R; scalarMult(R,k,256); u64 ax[4],ay[4]; jToAff(ax,ay,R);
        if(cmpN(ax,Qx,4)==0){
          for(int z=0;z<4;z++) outK[z]=k[z];
          *found=1;
          return;
        }
      }
    } else {
      std::array<u64,4> dd; for(int z=0;z<4;z++) dd[z]=recs[i].d[z];
      tab[key]=std::make_pair(dd,(int)recs[i].kind);
    }
  }
}

// ---------------- solve one challenge ----------------
static int runSolve(const std::string& jf, int target, const std::string& of,
                    int dpbits, int nT, int nW, int gpus){
  std::string js; if(!readFile(jf,js)){ std::fprintf(stderr,"cannot read %s\n",jf.c_str()); return 1; }
  u64 Qx[4],Qy[4]; int bits=70;
  if(!parseQ(js,target,&bits,Qx,Qy)){ std::fprintf(stderr,"instance %d not found\n",target); return 1; }
  int nStart=nT+nW;
  if(nStart%256){ std::fprintf(stderr,"nStart must be a multiple of 256 (full-warp __shfl_sync safety)\n"); return 1; }
  int devCnt=deviceCount();
  int dev=std::min(gpus,devCnt);
  if(dev<1){ std::fprintf(stderr,"no CUDA device\n"); return 1; }

  std::unordered_map<std::string,std::pair<std::array<u64,4>,int>> tab;
  u64 foundK[4]={0,0,0,0}; int solved=0;
  u64 totalSteps=0;
  auto t0=std::chrono::high_resolution_clock::now();
  // per round collect ~1<<14 DPs (expected table size needed for a collision
  // is just ~2*sqrt(N)/2^dpbits ~ 2^12 at 70 bits/24 dpbits), so size the
  // round so each walker produces ~ (1<<14)/nStart DPs on average.
  int maxSteps=(int)(((u64)(1u<<14)<<dpbits)/(u64)nStart);
  if(maxSteps<1) maxSteps=1;
  if(maxSteps>(1<<26)) maxSteps=1<<26;

  // per-device persistent resources
  std::vector<JumpEnt*> Jd(dev); std::vector<Start*> Sd(dev);
  std::vector<DpRec*>   Dd(dev); std::vector<unsigned*> Cc(dev); std::vector<int*> Ff(dev);
  std::vector<u64*>     AXd(dev);
  std::vector<u64*>     QXd(dev), QYd(dev);

  for(int di=0;di<dev;di++){
    cudaSetDevice(di);
    CHECK_CUDA(cudaMalloc(&Jd[di],sizeof(JumpEnt)*W_));
    CHECK_CUDA(cudaMalloc(&Sd[di],sizeof(Start)*nStart));
    CHECK_CUDA(cudaMalloc(&Dd[di],sizeof(DpRec)*MAXDP_GLOBAL));
    CHECK_CUDA(cudaMalloc(&Cc[di],4)); CHECK_CUDA(cudaMalloc(&Ff[di],4));
    CHECK_CUDA(cudaMalloc(&AXd[di],sizeof(u64)*nStart));
    CHECK_CUDA(cudaMalloc(&QXd[di],32)); CHECK_CUDA(cudaMalloc(&QYd[di],32));
    CHECK_CUDA(cudaMemcpy(QXd[di],Qx,32,cudaMemcpyHostToDevice));
    CHECK_CUDA(cudaMemcpy(QYd[di],Qy,32,cudaMemcpyHostToDevice));
    // jump table once per device (IDENTICAL on all devices so a DP from
    // any device merges against any other device's DP in the same walk graph)
    genJumpsKernel<<<1,W_>>>(Jd[di],bits/2,0x0BADF00DCAFEBABEULL);
    CHECK_CUDA(cudaGetLastError());
  }
  CHECK_CUDA(cudaDeviceSynchronize());

  // rounds: refresh starts (fresh entropy) until solved or cap.
  // All devices walk CONCURRENTLY (one worker thread per device) so
  // dual-T4 time ~= single-T4 time, not 2x; readback+merge after join.
  std::vector<unsigned> ndp(dev,0);
  for(int rd=0;rd<1024 && !solved;rd++){
    if(tab.size()>(1u<<22)) tab.clear();   // safety: never let the map blow up
    for(int di=0;di<dev;di++) ndp[di]=0;
    std::vector<std::thread> workers;
    for(int di=0;di<dev;di++){
      workers.emplace_back([&,di](){
        cudaSetDevice(di);
        if(cudaGetLastError()!=cudaSuccess) return;
        genStartsKernel<<<(nStart+255)/256,256>>>(Sd[di],nT,nW,bits,
            0xC0FFEEULL^((u64)rd<<33)^((u64)di<<41), QXd[di], QYd[di]);
        unsigned z=0; int s0=0;
        cudaMemcpy(Cc[di],&z,4,cudaMemcpyHostToDevice);
        cudaMemcpy(Ff[di],&s0,4,cudaMemcpyHostToDevice);
        walkKernelBatch<<<(nStart+255)/256,256>>>(Jd[di],Sd[di],nStart,dpbits,maxSteps,Dd[di],Cc[di],Ff[di],AXd[di]);
        cudaError_t e=cudaGetLastError(); if(e!=cudaSuccess) return;
        cudaDeviceSynchronize();
        unsigned n=0; cudaMemcpy(&n,Cc[di],4,cudaMemcpyDeviceToHost);
        ndp[di]=n;
      });
    }
    for(auto& t:workers) t.join();
    for(int di=0;di<dev;di++){
      cudaSetDevice(di);
      std::vector<u64> act(nStart);
      CHECK_CUDA(cudaMemcpy(act.data(),AXd[di],sizeof(u64)*nStart,cudaMemcpyDeviceToHost));
      u64 ssum=0; for(int i=0;i<nStart;i++) ssum+=act[i];
      totalSteps+=ssum;
      std::vector<DpRec> recs(ndp[di]);
      if(ndp[di]) CHECK_CUDA(cudaMemcpy(recs.data(),Dd[di],sizeof(DpRec)*ndp[di],cudaMemcpyDeviceToHost));
      for(auto& r:recs) r.dev=di;
      mergeDps(tab,recs.data(),(int)ndp[di],Qx,Qy,foundK,&solved);
      if(solved) break;
    }
  }
  auto t1=std::chrono::high_resolution_clock::now();
  double ms=std::chrono::duration<double,std::milli>(t1-t0).count();
  for(int di=0;di<dev;di++){ cudaSetDevice(di);
    cudaFree(Jd[di]); cudaFree(Sd[di]); cudaFree(Dd[di]); cudaFree(Cc[di]); cudaFree(Ff[di]);
    cudaFree(AXd[di]); cudaFree(QXd[di]); cudaFree(QYd[di]); }

  FILE* f=fopen(of.c_str(),"w");
  if(!f){ std::fprintf(stderr,"cannot write %s\n",of.c_str()); return 1; }
  std::fprintf(f,"{\n  \"solved\": %d,\n  \"k\": \"%s\",\n", solved, limbsToHex(foundK).c_str());
  std::fprintf(f,"  \"steps\": %llu,\n  \"time_ms\": %.1f,\n", (unsigned long long)totalSteps, ms);
  std::fprintf(f,"  \"target\": %d,\n  \"dpbits\": %d,\n  \"nT\": %d,\n  \"nW\": %d,\n  \"gpus\": %d\n}\n",
      target,dpbits,nT,nW,dev);
  fclose(f);
  std::printf("solve target=%d solved=%d steps=%llu time=%.1f ms gpus=%d\n",
      target,solved,(unsigned long long)totalSteps,ms,dev);
  if(solved) std::printf("k=%s\n", limbsToHex(foundK).c_str());
  return solved?0:1;
}

// ---------------- selftest: KNOWN key, enforce k match ----------------
static int runSelftest(int gpus){
  int n=deviceCount(); if(n<1){ std::fprintf(stderr,"no CUDA device\n"); return 2; }
  u64 k[4]={0,0,0,0}; k[0]=0x800000ULL|0x0A1B2CULL;   // 24-bit secret
  JP Qj; scalarMult(Qj,k,24);
  u64 Qx[4],Qy[4]; jToAff(Qx,Qy,Qj);
  std::printf("selftest: known k=%s bits=24\n", limbsToHex(k).c_str());
  std::string js="{\n\"instance\":[{\"index\":0,\"bits\":24,\"Qx\":\"";
  js+=limbsToHex(Qx); js+="\",\"Qy\":\""; js+=limbsToHex(Qy);
  js+="\"}]\n}\n";
  FILE* f=fopen("_selftest_challenge.json","w"); fputs(js.c_str(),f); fclose(f);
  int rc=runSolve("_selftest_challenge.json",0,"_selftest_out.json",12,1<<12,1<<12,gpus);
  if(rc!=0){ std::printf("selftest: FAIL (solve rc=%d)\n",rc); return 1; }
  std::string ob; readFile("_selftest_out.json",ob);
  size_t p=ob.find("\"k\": \"");
  if(p==std::string::npos){ std::printf("selftest: FAIL (no k)\n"); return 1; }
  std::string hk=ob.substr(p+6); size_t e=hk.find("\""); hk=hk.substr(0,e);
  u64 kk[4]; hexToLimbs(hk.substr(2),kk);
  int ok=memcmp(kk,k,32)==0;
  std::printf("selftest: k match = %d (expect 1)\n", ok);
  return ok?0:1;
}

// ---------------- bench: aggregate steps/s ----------------
static int runBench(double sec,int dpbits,int gpus){
  int n=deviceCount(); if(n<1){ std::fprintf(stderr,"no CUDA device\n"); return 2; }
  int dev=std::min(gpus,n);
  int bits=40, wbits=20, nStart=1<<20;
  u64 totalSteps=0;
  auto t0=std::chrono::high_resolution_clock::now();
  std::vector<JumpEnt*> Jd(dev); std::vector<Start*> Sd(dev);
  std::vector<DpRec*> Dd(dev); std::vector<unsigned*> Cc(dev); std::vector<int*> Ff(dev);
  std::vector<u64*> Qd(dev); std::vector<u64*> AXd(dev);
  for(int di=0;di<dev;di++){
    cudaSetDevice(di);
    CHECK_CUDA(cudaMalloc(&Jd[di],sizeof(JumpEnt)*W_));
    CHECK_CUDA(cudaMalloc(&Sd[di],sizeof(Start)*nStart));
    CHECK_CUDA(cudaMalloc(&Dd[di],sizeof(DpRec)*MAXDP_GLOBAL));
    CHECK_CUDA(cudaMalloc(&Cc[di],4)); CHECK_CUDA(cudaMalloc(&Ff[di],4));
    CHECK_CUDA(cudaMalloc(&AXd[di],sizeof(u64)*nStart));
    CHECK_CUDA(cudaMalloc(&Qd[di],64));
    u64 QQ[8]; memcpy(QQ,GX_,32); memcpy(QQ+4,GY_,32);
    CHECK_CUDA(cudaMemcpy(Qd[di],QQ,64,cudaMemcpyHostToDevice));
    genJumpsKernel<<<1,W_>>>(Jd[di],wbits,0xCAFEBABEULL);
    genStartsKernel<<<(nStart+255)/256,256>>>(Sd[di],nStart/2,nStart/2,bits,
        0xC0FFEEULL^((u64)di<<41), Qd[di], Qd[di]+4);
    CHECK_CUDA(cudaGetLastError());
  }
  CHECK_CUDA(cudaDeviceSynchronize());
  int maxSteps=1<<10;
  while(std::chrono::duration<double>(std::chrono::high_resolution_clock::now()-t0).count()<sec){
    std::vector<std::thread> workers;
    for(int di=0;di<dev;di++){
      workers.emplace_back([&,di](){
        cudaSetDevice(di);
        unsigned z=0; int s0=0;
        cudaMemcpy(Cc[di],&z,4,cudaMemcpyHostToDevice);
        cudaMemcpy(Ff[di],&s0,4,cudaMemcpyHostToDevice);
        walkKernelBatch<<<(nStart+255)/256,256>>>(Jd[di],Sd[di],nStart,dpbits,maxSteps,Dd[di],Cc[di],Ff[di],AXd[di]);
        cudaDeviceSynchronize();
      });
    }
    for(auto& t:workers) t.join();
    for(int di=0;di<dev;di++){
      cudaSetDevice(di);
      std::vector<u64> act(nStart);
      cudaMemcpy(act.data(),AXd[di],sizeof(u64)*nStart,cudaMemcpyDeviceToHost);
      u64 ssum=0; for(int i=0;i<nStart;i++) ssum+=act[i];
      totalSteps+=ssum;
    }
  }
  auto t1=std::chrono::high_resolution_clock::now();
  double ms=std::chrono::duration<double,std::milli>(t1-t0).count();
  for(int di=0;di<dev;di++){ cudaSetDevice(di);
    cudaFree(Jd[di]); cudaFree(Sd[di]); cudaFree(Dd[di]); cudaFree(Cc[di]); cudaFree(Ff[di]);
    cudaFree(AXd[di]); cudaFree(Qd[di]); }
  std::printf("bench: %.1f s, %llu steps, %.3e steps/s aggregate (gpus=%d, dpbits=%d)\n",
      ms/1000.0,(unsigned long long)totalSteps,(double)totalSteps/(ms/1000.0),dev,dpbits);
  return 0;
}

// ---------------- prof: per-stage time breakdown (Phase 4) ----------------
static int runProf(double sec,int dpbits,int gpus){
  int n=deviceCount(); if(n<1){ std::fprintf(stderr,"no CUDA device\n"); return 2; }
  int dev=std::min(gpus,n);
  int bits=40, wbits=20, nStart=1<<20;
  std::vector<JumpEnt*> Jd(dev); std::vector<Start*> Sd(dev);
  std::vector<DpRec*> Dd(dev); std::vector<unsigned*> Cc(dev); std::vector<int*> Ff(dev);
  std::vector<u64*> Qd(dev); std::vector<u64*> AXd(dev);
  for(int di=0;di<dev;di++){
    cudaSetDevice(di);
    CHECK_CUDA(cudaMalloc(&Jd[di],sizeof(JumpEnt)*W_));
    CHECK_CUDA(cudaMalloc(&Sd[di],sizeof(Start)*nStart));
    CHECK_CUDA(cudaMalloc(&Dd[di],sizeof(DpRec)*MAXDP_GLOBAL));
    CHECK_CUDA(cudaMalloc(&Cc[di],4)); CHECK_CUDA(cudaMalloc(&Ff[di],4));
    CHECK_CUDA(cudaMalloc(&AXd[di],sizeof(u64)*nStart));
    CHECK_CUDA(cudaMalloc(&Qd[di],64));
    u64 QQ[8]; memcpy(QQ,GX_,32); memcpy(QQ+4,GY_,32);
    CHECK_CUDA(cudaMemcpy(Qd[di],QQ,64,cudaMemcpyHostToDevice));
    genJumpsKernel<<<1,W_>>>(Jd[di],wbits,0xCAFEBABEULL);
    genStartsKernel<<<(nStart+255)/256,256>>>(Sd[di],nStart/2,nStart/2,bits,
        0xC0FFEEULL^((u64)di<<41), Qd[di], Qd[di]+4);
    CHECK_CUDA(cudaGetLastError());
  }
  CHECK_CUDA(cudaDeviceSynchronize());
  int maxSteps=1<<10;
  auto w0=std::chrono::high_resolution_clock::now();
  double h2d_ms=0, kernel_ms=0, sync_ms=0, d2h_ms=0, merge_ms=0;
  for(int it=0;it<8;it++){
    auto s=std::chrono::high_resolution_clock::now();
    std::vector<std::thread> workers;
    for(int di=0;di<dev;di++){
      workers.emplace_back([&,di](){
        cudaSetDevice(di);
        unsigned z=0; int s0=0;
        cudaMemcpy(Cc[di],&z,4,cudaMemcpyHostToDevice);
        cudaMemcpy(Ff[di],&s0,4,cudaMemcpyHostToDevice);
        walkKernelBatch<<<(nStart+255)/256,256>>>(Jd[di],Sd[di],nStart,dpbits,maxSteps,Dd[di],Cc[di],Ff[di],AXd[di]);
        cudaError_t e=cudaGetLastError(); if(e!=cudaSuccess) return;
        cudaDeviceSynchronize();
      });
    }
    for(auto& t:workers) t.join();
    auto e0=std::chrono::high_resolution_clock::now();
    h2d_ms+=1e-3*std::chrono::duration<double,std::micro>(e0-s).count();
    std::vector<unsigned> cnt(dev);
    for(int di=0;di<dev;di++){
      cudaSetDevice(di);
      cudaMemcpy(&cnt[di],Cc[di],4,cudaMemcpyDeviceToHost);
    }
    auto e1=std::chrono::high_resolution_clock::now();
    sync_ms+=1e-3*std::chrono::duration<double,std::micro>(e1-e0).count();
    for(int di=0;di<dev;di++){
      cudaSetDevice(di);
      std::vector<u64> act(nStart);
      cudaMemcpy(act.data(),AXd[di],sizeof(u64)*nStart,cudaMemcpyDeviceToHost);
    }
    auto e2=std::chrono::high_resolution_clock::now();
    d2h_ms+=1e-3*std::chrono::duration<double,std::micro>(e2-e1).count();
    for(int di=0;di<dev;di++){
      std::vector<DpRec> recs(cnt[di]);
      if(cnt[di]){ cudaSetDevice(di); cudaMemcpy(recs.data(),Dd[di],sizeof(DpRec)*cnt[di],cudaMemcpyDeviceToHost); }
      // no merge table here; just simulate parse cost (skip)
    }
    auto e3=std::chrono::high_resolution_clock::now();
    merge_ms+=1e-3*std::chrono::duration<double,std::micro>(e3-e2).count();
  }
  double wall=1e-3*std::chrono::duration<double,std::micro>(
      std::chrono::high_resolution_clock::now()-w0).count();
  for(int di=0;di<dev;di++){ cudaSetDevice(di);
    cudaFree(Jd[di]); cudaFree(Sd[di]); cudaFree(Dd[di]); cudaFree(Cc[di]); cudaFree(Ff[di]);
    cudaFree(AXd[di]); cudaFree(Qd[di]); }
  std::printf("prof: gpus=%d iters=8 duration_ms=%.2f\n", dev, wall);
  std::printf("prof: h2d_ms=%.2f kernel_sync_ms=%.2f d2h_ms=%.2f merge_ms=%.2f\n",
              h2d_ms, sync_ms, d2h_ms, merge_ms);
  return 0;
}

// ---------------- scale ----------------
static int runScale(int lo,int hi,int rep,int dpbits,int gpus){
  int okcnt=0, tot=0;
  for(int b=lo;b<=hi;b++){
    int solved=0;
    for(int r=0;r<rep;r++){
      u64 k[4]={0,0,0,0};
      u64 s=0xC0FFEEULL^(u64)b*1000ULL^(u64)r;
      randIntervalX(k,b,&s);
      JP Qj; scalarMult(Qj,k,b);
      u64 Qx[4],Qy[4]; jToAff(Qx,Qy,Qj);
      char tmp[800];
      sprintf(tmp,"{\"instance\":[{\"index\":0,\"bits\":%d,\"Qx\":\"%s\",\"Qy\":\"%s\"}]}",
          b,limbsToHex(Qx).c_str(),limbsToHex(Qy).c_str());
      FILE* f=fopen("_scale_challenge.json","w"); fputs(tmp,f); fclose(f);
      int dp=dpbits>0?dpbits:12;   // matches validated CPU dpb=12
      tot++;
      int rc=runSolve("_scale_challenge.json",0,"_scale_out.json",dp,1<<14,1<<14,gpus);
      if(rc==0){
        std::string ob; readFile("_scale_out.json",ob);
        size_t p=ob.find("\"k\": \"");
        if(p!=std::string::npos){
          std::string hk=ob.substr(p+6); size_t e=hk.find("\""); hk=hk.substr(0,e);
          u64 kk[4]; hexToLimbs(hk.substr(2),kk);
          if(memcmp(kk,k,32)==0){ solved=1; okcnt++; }
        }
      }
    }
    std::printf("scale bits=%d solved=%d/%d\n", b, solved, rep);
  }
  std::printf("scale total: %d/%d correct\n", okcnt, tot);
  return okcnt==tot?0:1;
}

// ---------------- main ----------------
int main(int argc,char**argv){
  if(argc<2){ usage(); return 1; }
  std::string cmd=argv[1];
  int gpus=1024; // sentinel = all
  if(cmd=="selftest"){ return runSelftest(argc>2?atoi(argv[2]):gpus); }
  if(cmd=="bench"){ double sec=argc>2?atof(argv[2]):2.0; int dpb=argc>3?atoi(argv[3]):24;
    gpus=argc>4?atoi(argv[4]):gpus; return runBench(sec,dpb,gpus); }
  if(cmd=="prof"){ double sec=argc>2?atof(argv[2]):2.0; int dpb=argc>3?atoi(argv[3]):24;
    gpus=argc>4?atoi(argv[4]):gpus; return runProf(sec,dpb,gpus); }
  if(cmd=="solve"){
    if(argc<5){ usage(); return 1; }
    int dpb=argc>5?atoi(argv[5]):24;
    int nt=argc>6?(1<<atoi(argv[6])):(1<<19);
    int nw=argc>7?(1<<atoi(argv[7])):(1<<19);
    gpus=argc>8?atoi(argv[8]):gpus;
    return runSolve(argv[2],atoi(argv[3]),argv[4],dpb,nt,nw,gpus);
  }
  if(cmd=="scale"){
    int lo=argc>2?atoi(argv[2]):16, hi=argc>3?atoi(argv[3]):40;
    int rep=argc>4?atoi(argv[4]):3, dpb=argc>5?atoi(argv[5]):0;
    gpus=argc>6?atoi(argv[6]):gpus;
    return runScale(lo,hi,rep,dpb,gpus);
  }
  usage();
  return 1;
}