// cpuid_probe.c — report SIMD features and cache topology on x86-64 (fixed bits)
#include <stdio.h>
#include <stdint.h>
#if defined(_MSC_VER)
#include <intrin.h>
#else
#include <cpuid.h>
#endif

static void get_cpuid(unsigned leaf, unsigned sub, unsigned *a, unsigned *b, unsigned *c, unsigned *d) {
#if defined(_MSC_VER)
    int regs[4];
    __cpuidex(regs, (int)leaf, (int)sub);
    *a=(unsigned)regs[0]; *b=(unsigned)regs[1]; *c=(unsigned)regs[2]; *d=(unsigned)regs[3];
#else
    unsigned eax, ebx, ecx, edx;
    __cpuid_count(leaf, sub, eax, ebx, ecx, edx);
    *a=eax; *b=ebx; *c=ecx; *d=edx;
#endif
}

int main(void) {
    unsigned a,b,c,d;
    char brand[49]={0};
    get_cpuid(0,0,&a,&b,&c,&d);
    unsigned max_leaf=a;
    unsigned ids[3]={b,d,c};
    for(int i=0;i<3;i++){ brand[i*4+0]=(char)(ids[i]>>0); brand[i*4+1]=(char)(ids[i]>>8); brand[i*4+2]=(char)(ids[i]>>16); brand[i*4+3]=(char)(ids[i]>>24); }
    printf("Vendor: %s\n", brand);
    printf("Max CPUID leaf: 0x%X\n", max_leaf);

    get_cpuid(1,0,&a,&b,&c,&d);
    printf("Family:%u Model:%u Stepping:%u\n", (a>>8)&0xF, (a>>4)&0xF, a&0xF);
    printf("Hypervisor present: %d\n", (c>>31)&1);
    printf("SSE2: %d SSE3:%d SSSE3:%d SSE4.1:%d SSE4.2:%d POPCNT:%d AVX:%d FMA:%d MOVBE:%d\n",
        (d>>26)&1,(c>>0)&1,(c>>9)&1,(c>>19)&1,(c>>20)&1,(c>>23)&1,(c>>28)&1,(c>>12)&1,(c>>22)&1);
    if (max_leaf>=7){
        get_cpuid(7,0,&a,&b,&c,&d);
        printf("FSGSBASE:%d BMI1:%d BMI2:%d AVX2:%d ADX:%d AVX512F:%d AVX512DQ:%d\n",
            b&1,(b>>3)&1,(b>>8)&1,(b>>5)&1,(b>>19)&1,(b>>16)&1,(b>>17)&1);
        printf("AVX512BW:%d AVX512VL:%d AVX512CD:%d\n",(b>>30)&1,(b>>31)&1,(c>>28)&1);
    }
    // cache topology via leaf 4
    unsigned long long l1d=0,l2=0,l3=0;
    if (max_leaf>=4){
        for(unsigned i=0;i<16;i++){
            get_cpuid(4,i,&a,&b,&c,&d);
            unsigned type=a&0x1F;
            if(type==0) break;
            unsigned level=(a>>5)&0x7;
            unsigned ways=((b>>22)&0x3FF)+1;
            unsigned part=((b>>12)&0x3FF)+1;
            unsigned sets=c+1;
            unsigned long long sz=(unsigned long long)ways*part*sets*64;
            if(level==1&&type==1) l1d=sz;
            if(level==2&&type==3) l2=sz;
            if(level==3&&type==3) l3=sz;
        }
    }
    printf("L1D: %llu KB  L2: %llu KB  L3: %llu KB\n", l1d/1024, l2/1024, l3/1024);
    // logical processors / cores from leaf 1 + leaf 4 topology (Zen: cores in L3 sets)
    printf("LogicalProc(leaf1): %u\n", (b>>16)&1 ? ((b>>24)) : 1);
    return 0;
}