#include <cstdio>
int main() {
    unsigned a=0x80000000,b,c,d; __asm__ __volatile__("cpuid" : "+a"(a), "=b"(b), "=c"(c), "=d"(d));
    printf("maxExt=0x%08x\n", a);
    a=1; unsigned a1,b1,c1,d1; __asm__ __volatile__("cpuid" : "+a"(a), "=b"(b), "=c"(c), "=d"(d));
    printf("leaf1 family=%u model=%u stepping=%u\n", (a1>>8)&0xf, (a1>>4)&0xf, a1&0xf);
    printf("bit_hypervisor=%u\n", (c1>>31)&1);
    a=0x80000008; __asm__ __volatile__("cpuid" : "+a"(a), "=b"(b), "=c"(c), "=d"(d));
    printf("physbits=%u lut3=%u\n", a&0xff, (c>>12)&0xf);
    return 0;
}
