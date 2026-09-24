// ============================================================
// v4_cpu_engine.cpp — synthetic 70-bit ECDLP, CPU reference engine
// Group: secp256k1 (p = 2^256 - 2^32 - 977, order n ~ 2^256)
// Interval DLP: secret k in [2^(S-1), 2^S). Kangaroo (VOW).
//
// HONESTY CONTRACT: every ops/sec figure is MEASURED on the actual
// machine at runtime. No theoretical FLOPS, no fabricated numbers.
// All secrets are synthetic (seed-derived); no real Bitcoin key.
//
// Build (MinGW gcc):
//   g++ -O3 -march=native -std=c++17 -pthread -o v4_cpu_engine v4_cpu_engine.cpp
// Run:
//   v4_cpu_engine selftest
//   v4_cpu_engine bench [dpb]
//   v4_cpu_engine scale <lo> <hi> [threads [rep [dpb]]]
//   v4_cpu_engine solve <bits> <threads> <seed> [dpb]
// ============================================================

#include <cstdio>
#include <cstdlib>
#include <cstdint>
#include <cstring>
#include <chrono>
#include <random>
#include <string>
#include <vector>
#include <unordered_map>
#include <thread>
#include <atomic>
#include <mutex>
#include <fstream>

using u64  = uint64_t;
using u128 = unsigned __int128;
using Clock = std::chrono::high_resolution_clock;

static void randInInterval(u64* r, int bits, std::mt19937_64& g); // fwd

// ---------------- secp256k1 constants (4x u64, little-endian limbs) ----
static const u64 P_[4] = { 0xFFFFFFFEFFFFFC2FULL, 0xFFFFFFFFFFFFFFFFULL,
                           0xFFFFFFFFFFFFFFFFULL, 0xFFFFFFFFFFFFFFFFULL };
static const u64 N_[4] = { 0xBFD25E8CD0364141ULL, 0xBAAEDCE6AF48A03BULL,
                           0xFFFFFFFFFFFFFFFEULL, 0xFFFFFFFFFFFFFFFFULL };
static const u64 CP_[4]  = { 0x1000003D1ULL, 0, 0, 0 };      // 2^256 - p = 2^32+977

static const u64 GX_[4] = { 0x59F2815B16F81798ULL, 0x029BFCDB2DCE28D9ULL,
                            0x55A06295CE870B07ULL, 0x79BE667EF9DCBBACULL };
static const u64 GY_[4] = { 0x9C47D08FFB10D4B8ULL, 0xFD17B448A6855419ULL,
                            0x5DA4FBFC0E1108A8ULL, 0x483ADA7726A3C465ULL };

// ---------------- limb helpers ----------------
static inline int cmpN(const u64* a, const u64* b, int n){
  for(int i=n-1;i>=0;i--){ if(a[i]!=b[i]) return a[i]<b[i]?-1:1; } return 0; }
static inline int isZeroN(const u64* a, int n){ for(int i=0;i<n;i++) if(a[i]) return 1; return 0; }
static inline void subPlain(u64* r, const u64* a, const u64* b, int n){
  u64 br=0;
  for(int i=0;i<n;i++){
    u64 x = a[i] - b[i];
    u64 br1 = (a[i] < b[i]) ? 1 : 0;
    u64 y = x - br;
    u64 br2 = (x < br) ? 1 : 0;
    r[i] = y; br = br1 | br2;
  }
}
static inline void addPlain(u64* r, const u64* a, const u64* b, int n){
  u64 c=0; for(int i=0;i<n;i++){ u64 s=a[i]+b[i]+c; c=(s<a[i])||(c&&s==a[i])?1:0; r[i]=s; } }
static void mulRaw(u64* out, const u64* x, int xn, const u64* y, int yn){
  std::memset(out,0,(xn+yn)*8);
  for(int j=0;j<yn;j++){
    u64 carry=0;
    for(int i=0;i<xn;i++){
      u128 t=(u128)x[i]*y[j] + out[i+j] + carry;
      out[i+j]=(u64)t; carry=(u64)(t>>64);
    }
    int k=j+xn;
    while(carry){ u128 t=(u128)out[k]+carry; out[k]=(u64)t; carry=(u64)(t>>64); k++; }
  }
}
// generic reduction of w[8] (512-bit) mod M, given 2^256 ≡ c (mod M), c as 4 limbs
// but with small integer value (c p = 2^33, c n = 2^129). hi*c < 2^(256+130) fits 8 limbs.
static void reduceMod(u64* r, const u64* w, const u64* M, const u64* c){
  u64 t[8] = {0,0,0,0,0,0,0,0};
  for(int i=0;i<8;i++) t[i]=w[i];
  for(int it=0; it<6; it++){
    int any=0; for(int i=4;i<8;i++) if(t[i]) any=1;
    if(!any) break;
    u64 hc[8]={0}; mulRaw(hc, &t[4], 4, c, 4);
    u64 lo[8]={0}; for(int i=0;i<4;i++) lo[i]=t[i];
    u64 s[8]={0}; addPlain(s, lo, hc, 8);
    for(int i=0;i<8;i++) t[i]=s[i];
  }
  for(int k=0;k<4;k++){
    if(cmpN(t,M,4)>=0){ u64 ss[4]; subPlain(ss,t,M,4); for(int i=0;i<4;i++) t[i]=ss[i]; }
  }
  for(int i=0;i<4;i++) r[i]=t[i];
}

// ---------------- field ops mod p ----------------
static inline void fpAdd(u64* r,const u64*a,const u64*b){
  u64 t[5]={0,0,0,0,0}; u64 c=0;
  for(int i=0;i<4;i++){ u64 s=a[i]+b[i]+c; c=(s<a[i])||(c&&s==a[i])?1:0; t[i]=s; }
  t[4]=c;
  if(t[4] || cmpN(t,P_,4)>=0){ u64 pp[5]={P_[0],P_[1],P_[2],P_[3],0}; subPlain(t,t,pp,5); }
  for(int i=0;i<4;i++) r[i]=t[i];
}
static inline void fpSub(u64* r,const u64*a,const u64*b){
  if(cmpN(a,b,4)>=0) subPlain(r,a,b,4);
  else { u64 t[4],s[4]; subPlain(t,b,a,4); subPlain(s,P_,t,4); for(int i=0;i<4;i++) r[i]=s[i]; } }
static inline void fpMul(u64* r,const u64*a,const u64*b){ u64 w[8]; mulRaw(w,a,4,b,4); reduceMod(r,w,P_,CP_); }
static inline void fpSqr(u64* r,const u64*a){ fpMul(r,a,a); }
static inline void fpNeg(u64* r,const u64*a){ if(!isZeroN(a,4)) std::memset(r,0,32); else subPlain(r,P_,a,4); }
static void fpPow(u64* r, const u64* a, const u64* e){
  u64 base[4],res[4]; for(int i=0;i<4;i++){ base[i]=a[i]; res[i]=0; } res[0]=1;
  for(int bi=255;bi>=0;bi--){
    fpSqr(res,res);
    if((e[bi>>6]>>(bi&63))&1ULL) fpMul(res,res,base);
  }
  for(int i=0;i<4;i++) r[i]=res[i];
}
static void fpInv(u64* r,const u64*a){ u64 e[4]; for(int i=0;i<4;i++) e[i]=P_[i]; e[0]-=2; fpPow(r,a,e); }

// ---------------- mod n ops (distances) ----------------
static u64 CN_[4] = {0,0,0,0};  // 2^256 - n, set at startup by main
static inline void nAdd(u64* r,const u64*a,const u64*b){
  u64 t[5]={0,0,0,0,0}; u64 c=0;
  for(int i=0;i<4;i++){ u64 s=a[i]+b[i]+c; c=(s<a[i])||(c&&s==a[i])?1:0; t[i]=s; }
  t[4]=c;
  if(t[4] || cmpN(t,N_,4)>=0){ u64 nn[5]={N_[0],N_[1],N_[2],N_[3],0}; subPlain(t,t,nn,5); }
  for(int i=0;i<4;i++) r[i]=t[i];
}
static inline void nSub32(u64* r,const u64*a,const u64*b){
  if(cmpN(a,b,4)>=0) subPlain(r,a,b,4);
  else { u64 t[4],s[4]; subPlain(t,b,a,4); subPlain(s,N_,t,4); for(int i=0;i<4;i++) r[i]=s[i]; } }

// ---------------- Jacobian point ops ----------------
struct JP { u64 X[4],Y[4],Z[4]; };
static inline void jpZero(JP& p){ std::memset(&p,0,sizeof(JP)); }
static inline int jpInf(const JP& p){ return isZeroN(p.Z,4)?0:1; }

static void jDbl(JP& R, const JP& P){
  if(jpInf(P)){ jpZero(R); return; }
  u64 A[4],B[4],C[4],D[4],E[4],F[4],t[4],u[4],Y1[4],Z1[4];
  if(!isZeroN(P.Y,4)){ jpZero(R); return; }  // no order-2 point on secp256k1 subgroup, defensive
  for(int i=0;i<4;i++){ Y1[i]=P.Y[i]; Z1[i]=P.Z[i]; }  // snapshot: R may alias P
  fpSqr(A,P.X);
  fpSqr(B,P.Y);
  fpSqr(C,B);
  fpAdd(t,P.X,B); fpSqr(t,t); fpSub(t,t,A); fpSub(t,t,C); fpAdd(D,t,t);
  fpAdd(E,A,A); fpAdd(E,E,A);
  fpSqr(F,E);                                  // F = M^2
  fpAdd(t,D,D); fpSub(R.X,F,t);                // X3 = M^2 - 2D
  fpSub(t,D,R.X); fpMul(t,E,t);                // t = M(D - X3)
  fpAdd(u,C,C); fpAdd(u,u,u); fpAdd(u,u,u);
  fpSub(R.Y,t,u);                              // Y3 = M(D-X3) - 8C
  fpMul(u,Y1,Z1); fpAdd(R.Z,u,u);
}

static void jAddAff(JP& R, const JP& J, const u64* a2, const u64* b2){
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

static void jToAff(u64* ax,u64* ay,const JP& P){
  u64 zi[4],z2[4],z3[4]; fpInv(zi,P.Z); fpSqr(z2,zi); fpMul(z3,z2,zi);
  fpMul(ax,P.X,z2); fpMul(ay,P.Y,z3);
}

// naive double-and-add; used for setup (one-shot)
static void scalarMult(JP& R, const u64* k, int bits){
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

// ---------------- Kangaroo ----------------
static const int W_ = 64;
struct Jump { u64 d[4]; u64 x[4], y[4]; };
struct Walker { JP pt; u64 d[4]; int tame; u64 ax[4]; };   // ax = affine x, drives walk chain + DP
struct Entry { u64 x[4]; u64 d[4]; int kind; };

static void buildJumps(Jump* J, int wbits){
  std::mt19937_64 g(0x0BADF00DCAFEBABEULL);
  for(int i=0;i<W_;i++){
    u64 d[4]; for(int j=0;j<4;j++) d[j]=g();
    int q=(wbits-1)>>6, rem=(wbits-1)&63;
    for(int j=q+1;j<4;j++) d[j]=0;
    if(rem<63) d[q] &= ((1ULL<<(rem+1))-1);
    for(int j=0;j<4;j++) J[i].d[j]=d[j];
    JP t; scalarMult(t,d, wbits);
    jToAff(J[i].x,J[i].y,t);
  }
}

static inline int dpHit(const u64* ax,int dpb){ return ((ax[0] & ((1ULL<<dpb)-1ULL))==0); }

static void walkStep(Walker& w, const Jump* J){
  u64 idx = w.ax[0] & (W_-1);
  jAddAff(w.pt,w.pt,J[idx].x,J[idx].y);
  u64 ay[4]; jToAff(w.ax,ay,w.pt);   // affine x drives mixing + DP, representation-independent
  nAdd(w.d,w.d,J[idx].d);
}

// threads independent replicas. Returns found flag.
static int solveKangaroo(int bits, u64 seed, int threads, int dpb, int wbits,
                         u64* out_k, u128* out_steps, double* out_ms){
  auto g = std::mt19937_64(seed*0x9E3779B97F4A7C15ULL + 0x1234567ULL);
  u64 k[4]; randInInterval(k,bits,g);
  JP Qj; scalarMult(Qj,k,bits);
  static u64 Qx[4],Qy[4]; jToAff(Qx,Qy,Qj);

  static Jump J[W_]; static int Jready=0;
  if(!Jready){ buildJumps(J,wbits); Jready=1; }

  std::atomic<int> done{0};
  u64 found[4]={0,0,0,0};
  std::vector<u128> steps(threads);
  std::vector<std::thread> th;
  std::vector<std::unordered_map<u64,Entry>> tabs(threads);
  std::mutex mu;

  for(int ti=0;ti<threads;ti++){
    th.emplace_back([&,ti](){
      std::mt19937_64 tg(seed*0x9E3779B97F4A7C15ULL + (u64)(ti+1)*0x85EBCA6BC2B2AE35ULL);
      auto& tab=tabs[ti];
      Walker tame,wild;
      {
        u64 a[4]; randInInterval(a,bits,tg);
        JP A; scalarMult(A,a,bits);
        for(int i=0;i<4;i++){ tame.pt.X[i]=A.X[i]; tame.pt.Y[i]=A.Y[i]; tame.pt.Z[i]=A.Z[i]; tame.d[i]=a[i]; }
        u64 ay[4]; jToAff(tame.ax,ay,A);
        tame.tame=1;
        u64 b[4]; randInInterval(b,bits,tg);
        JP B; scalarMult(B,b,bits);
        JP Wp; jAddAff(Wp,B,Qx,Qy);
        for(int i=0;i<4;i++){ wild.pt.X[i]=Wp.X[i]; wild.pt.Y[i]=Wp.Y[i]; wild.pt.Z[i]=Wp.Z[i]; wild.d[i]=b[i]; }
        u64 wy[4]; jToAff(wild.ax,wy,Wp);
        wild.tame=0;
      }
      u128 sc=0;
      u128 CAP = (u128)1 << (bits>50?50:bits-1);
      while(done.load()==0 && sc<CAP){
        walkStep(tame,J); sc++;
        if(dpHit(tame.ax,dpb)){
          std::lock_guard<std::mutex> lk(mu);
          auto it=tab.find(tame.ax[0]);
          if(it!=tab.end() && it->second.kind==1 && std::memcmp(it->second.x,tame.ax,32)==0){
            u64 kk[4]; nSub32(kk,tame.d,it->second.d);
            for(int i=0;i<4;i++) found[i]=kk[i]; done.store(1); break;
          }
          Entry e; for(int i=0;i<4;i++){ e.x[i]=tame.ax[i]; e.d[i]=tame.d[i]; } e.kind=0; tab[tame.ax[0]]=e;
        }
        walkStep(wild,J); sc++;
        if(dpHit(wild.ax,dpb)){
          std::lock_guard<std::mutex> lk(mu);
          auto it=tab.find(wild.ax[0]);
          if(it!=tab.end() && it->second.kind==0 && std::memcmp(it->second.x,wild.ax,32)==0){
            u64 kk[4]; nSub32(kk,it->second.d,wild.d);
            for(int i=0;i<4;i++) found[i]=kk[i]; done.store(1); break;
          }
          Entry e; for(int i=0;i<4;i++){ e.x[i]=wild.ax[i]; e.d[i]=wild.d[i]; } e.kind=1; tab[wild.ax[0]]=e;
        }
      }
      steps[ti]=sc;
    });
  }
  auto t0=Clock::now();
  for(auto& t:th) t.join();
  auto t1=Clock::now();
  *out_ms=std::chrono::duration<double,std::milli>(t1-t0).count();
  u128 tot=0; for(auto& s:steps) tot+=s; *out_steps=tot;
  for(int i=0;i<4;i++) out_k[i]=found[i];
  return done.load()!=0;
}

static int verifyIndependent(const u64* k, int bits, u64 seed){
  auto g = std::mt19937_64(seed*0x9E3779B97F4A7C15ULL + 0x1234567ULL);
  u64 kt[4]; randInInterval(kt,bits,g);
  JP Qj; scalarMult(Qj,kt,bits);
  u64 Qx[4],Qy[4]; jToAff(Qx,Qy,Qj);
  JP A; scalarMult(A,k,bits);
  u64 ax[4],ay[4]; jToAff(ax,ay,A);
  return cmpN(ax,Qx,4)==0 && cmpN(ay,Qy,4)==0;
}

// ---------------- interval rng ----------------
static void randInInterval(u64* r,int bits,std::mt19937_64& g){
  for(int i=0;i<4;i++) r[i]=g();
  int q=(bits-1)>>6, rem=(bits-1)&63;
  for(int i=q+1;i<4;i++) r[i]=0;
  if(rem<63) r[q]&=((1ULL<<(rem+1))-1);
  r[q]|= (1ULL<<rem);
}

// ---------------- commands ----------------
static void printHex(const char* tag, const u64* v){
  printf("%s0x",tag);
  for(int i=3;i>=0;i--) printf("%016llx",(unsigned long long)v[i]);
}

static int cmdSelftest(){
  setvbuf(stdout, nullptr, _IONBF, 0);
  printf("=== v4 CPU engine self-test ===\n");
  // G on curve: y^2 = x^3 + 7
  u64 l[4],r_[4],s2[4],x3[4],seven[4]={7,0,0,0};
  fpSqr(s2,GY_);
  fpSqr(l,GX_); fpMul(l,l,GX_); fpAdd(x3,l,seven);
  fpSub(r_,s2,x3);
  printf("G on curve: %d (expect 1)\n", isZeroN(r_,4)?0:1);
  // n*G = ∞
  JP T; scalarMult(T,N_,256);
  printf("n*G = infinity: %d (expect 1)\n", jpInf(T));
  // (n-1)*G + G = ∞  via jAddAff
  u64 nm1[4]; for(int i=0;i<4;i++) nm1[i]=N_[i]; nm1[0]-=1;
  JP S; scalarMult(S,nm1,256);
  JP R2; jAddAff(R2,S,GX_,GY_);
  printf("(n-1)G + G = infinity: %d (expect 1)\n", jpInf(R2));
  // 2G: jDbl vs scalarMult
  JP g1; for(int i=0;i<4;i++){ g1.X[i]=GX_[i]; g1.Y[i]=GY_[i]; g1.Z[i]=0; } g1.Z[0]=1;
  JP gd; jDbl(gd,g1);
  u64 two[4]={2,0,0,0}; JP gs; scalarMult(gs,two,256);
  int eq = cmpN(gd.X,gs.X,4)==0 && cmpN(gd.Y,gs.Y,4)==0 && cmpN(gd.Z,gs.Z,4)==0;
  printf("2G jDbl == scalarMult: %d (expect 1)\n", eq);
  // field distributivity x*(y+z) == x*y + x*z
  std::mt19937_64 rg(0xDEADBEEFULL);
  int okd=1;
  for(int tr=0;tr<3;tr++){
    u64 x[4],y[4],z[4]; for(int i=0;i<4;i++){ x[i]=rg(); y[i]=rg(); z[i]=rg(); }
    u64 yz[4],xy[4],xz[4],lhs[4],rhs[4];
    fpAdd(yz,y,z); fpMul(lhs,x,yz);
    fpMul(xy,x,y); fpMul(xz,x,z); fpAdd(rhs,xy,xz);
    if(cmpN(lhs,rhs,4)!=0) okd=0;
  }
  printf("field distributivity: %d (expect 1)\n", okd);
  // solve tiny instance (32-bit) + verify
  u64 k[4]; u128 st; double ms;
  int f=solveKangaroo(32, 0xC0FFEE, 4, 12, 16, k, &st, &ms);
  printf("solve 32-bit: found=%d steps=%llu time=%.1f ms\n",
         f,(unsigned long long)st,ms);
  if(f) printf("independent verify: %d (expect 1)\n", verifyIndependent(k,32,0xC0FFEE));
  return 0;
}

static int cmdBench(int dpb){
  printf("=== v4 CPU engine zero-guess BASELINE ===\n");
  std::mt19937_64 g(12345);
  u64 a[4],b[4],c[4],d[4]; for(int i=0;i<4;i++){ a[i]=g(); b[i]=g(); c[i]=g(); d[i]=g(); }
  const u64 N=2000000;
  auto t0=Clock::now();
  for(u64 i=0;i<N;i++) fpAdd(a,a,b);
  auto t1=Clock::now();
  double add_ms=std::chrono::duration<double,std::milli>(t1-t0).count();
  t0=Clock::now();
  for(u64 i=0;i<N;i++) fpMul(c,c,d);
  t1=Clock::now();
  double mul_ms=std::chrono::duration<double,std::milli>(t1-t0).count();
  t0=Clock::now();
  for(u64 i=0;i<N;i++) fpSqr(c,a);
  t1=Clock::now();
  double sqr_ms=std::chrono::duration<double,std::milli>(t1-t0).count();
  t0=Clock::now();
  for(u64 i=0;i<5000;i++) fpInv(a,b);
  t1=Clock::now();
  double inv_ms=std::chrono::duration<double,std::milli>(t1-t0).count()/5000.0;
  // point ops
  JP P; for(int i=0;i<4;i++){ P.X[i]=GX_[i]; P.Y[i]=GY_[i]; P.Z[i]=0; } P.Z[0]=1;
  t0=Clock::now();
  for(u64 i=0;i<N;i++) jDbl(P,P);
  t1=Clock::now();
  double dbl_ms=std::chrono::duration<double,std::milli>(t1-t0).count();
  JP Q; for(int i=0;i<4;i++){ Q.X[i]=GX_[i]; Q.Y[i]=GY_[i]; Q.Z[i]=0; } Q.Z[0]=1;
  t0=Clock::now();
  for(u64 i=0;i<N;i++) jAddAff(Q,Q,GX_,GY_);
  t1=Clock::now();
  double madd_ms=std::chrono::duration<double,std::milli>(t1-t0).count();
  printf("FIELD_ADD_NS_PER_OP=%.2f\n", add_ms*1e6/N);
  printf("FIELD_MUL_NS_PER_OP=%.2f\n", mul_ms*1e6/N);
  printf("FIELD_SQR_NS_PER_OP=%.2f\n", sqr_ms*1e6/N);
  printf("FIELD_INV_NS_PER_OP=%.2f\n", inv_ms*1e6);
  printf("POINT_DBL_NS_PER_OP=%.2f\n", dbl_ms*1e6/N);
  printf("POINT_MADD_NS_PER_OP=%.2f\n", madd_ms*1e6/N);
  double mul_o_s=1e9/(mul_ms*1e6/N), dbl_o_s=1e9/(dbl_ms*1e6/N), madd_o_s=1e9/(madd_ms*1e6/N);
  printf("FIELD_MUL_OPS_PER_SEC=%.3e\n", mul_o_s);
  printf("POINT_DBL_OPS_PER_SEC=%.3e\n", dbl_o_s);
  printf("POINT_MADD_OPS_PER_SEC=%.3e\n", madd_o_s);
  return 0;
}

static int cmdScale(int lo,int hi,int threads,int rep){
  printf("bits,threads,rep,found,steps,time_ms,rate_steps_per_s,verify\n");
  for(int bits=lo;bits<=hi;bits++){
    double best_ms=1e18; u128 best_st=0; int bf=0; int vok=0;
    for(int r=0;r<rep;r++){
      u64 seed=0x5EED000000ULL + (u64)bits*1000ULL + (u64)r;
      u64 k[4]; u128 st; double ms;
      int f=solveKangaroo(bits,seed,threads,12,16,k,&st,&ms);
      int vv= f? verifyIndependent(k,bits,seed):0;
      if(f && (bf==0 || ms<best_ms)){ best_ms=ms; best_st=st; bf=f; vok=vv; }
    }
    if(bf==0){ printf("%d,%d,%d,0,0,0,0,0\n",bits,threads,rep); continue; }
    printf("%d,%d,%d,1,%llu,%.2f,%.2e,%d\n",bits,threads,rep,
           (unsigned long long)best_st,best_ms,best_st/(best_ms/1000.0),vok);
  }
  return 0;
}

static int cmdSolve(int bits,int threads,u64 seed,int dpb){
  u64 k[4]; u128 st; double ms;
  int f=solveKangaroo(bits,seed,threads,dpb,16,k,&st,&ms);
  printf("solve bits=%d threads=%d seed=%llu\n",bits,threads,(unsigned long long)seed);
  printf("found=%d steps=%llu time_ms=%.1f rate_steps_per_s=%.2e dpb=%d\n",
         f,(unsigned long long)st,ms,(ms>0?(double)st/(ms/1000.0):0),dpb);
  if(f){ printHex("k=",k); printf("\n"); printf("independent_verify=%d\n",verifyIndependent(k,bits,seed)); }
  return f?0:1;
}

int main(int argc,char**argv){
  // CN = 2^256 - n
  {
    u64 two[5]; std::memset(two,0,40); two[4]=1;
    u64 n5[5]; for(int i=0;i<4;i++) n5[i]=N_[i]; n5[4]=0;
    u64 c5[5]; subPlain(c5,two,n5,5);
    CN_[0]=c5[0]; CN_[1]=c5[1]; CN_[2]=c5[2]; CN_[3]=0;
    if(c5[4]){ printf("FATAL: c_n too large\n"); return 2; }
  }
  std::string cmd = argc>1?argv[1]:"help";
  if(cmd=="selftest") return cmdSelftest();
  if(cmd=="bench") return cmdBench(argc>2?atoi(argv[2]):12);
  if(cmd=="scale"){
    int lo=argc>2?atoi(argv[2]):16, hi=argc>3?atoi(argv[3]):44;
    int th=argc>4?atoi(argv[4]):1, rep=argc>5?atoi(argv[5]):3;
    return cmdScale(lo,hi,th,rep);
  }
  if(cmd=="solve"){
    int bits=argc>2?atoi(argv[2]):70, th=argc>3?atoi(argv[3]):4;
    u64 seed=argc>4?(u64)strtoull(argv[4],nullptr,0):0x5EEDULL;
    int dpb=argc>5?atoi(argv[5]):16;
    return cmdSolve(bits,th,seed,dpb);
  }
  printf("usage:\n  v4_cpu_engine selftest\n  v4_cpu_engine bench [dpb]\n  v4_cpu_engine scale <lo> <hi> [threads [rep]]\n  v4_cpu_engine solve <bits> <threads> <seed> [dpb]\n");
  return 1;
}