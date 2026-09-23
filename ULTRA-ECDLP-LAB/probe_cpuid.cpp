#include <cstdio>
#include <cstdint>
int main() {
    for (unsigned sub = 0; sub < 4; sub++) {
        unsigned a=4,b=0,c=sub,d=0;
        __asm__ __volatile__("cpuid" : "+a"(a), "=b"(b), "=c"(c), "=d"(d) ::);
        printf("sub=%u eax=%08x ebx=%08x ecx=%08x edx=%08x type=%u\n", sub, a, b, c, d, a & 0x1f);
    }
    // extended leaf 0x8000001d (AMD)
    for (unsigned sub = 0; sub < 4; sub++) {
        unsigned a=0x8000001d,b=0,c=sub,d=0;
        __asm__ __volatile__("cpuid" : "+a"(a), "=b"(b), "=c"(c), "=d"(d) ::);
        printf("ext%u eax=%08x ebx=%08x ecx=%08x type=%u size=%llu\n", sub, a, b, c, d, a & 0x1f,
            (unsigned long long)(((b>>22)&0x3ff)+1) * ((c)+1) * (((b)&0xfff)+1));
    }
    return 0;
}
