#include <stdio.h>
#include <string.h>
#include <stdint.h>

#define RL32(x,n) (((x)<<(n))|((x)>>(32-(n))))

static const int RL[80] = {
    0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,
    7,4,13,1,10,6,15,3,12,0,9,5,2,14,11,8,
    3,10,14,4,9,15,8,1,2,7,0,6,13,11,5,12,
    1,9,11,10,0,8,12,4,13,3,7,15,14,5,6,2,
    4,0,5,9,7,12,2,10,14,1,3,8,11,6,15,13
};
static const int RR2[80] = {
    5,14,7,0,9,2,11,4,13,6,15,8,1,10,3,12,
    6,11,3,7,0,13,5,10,14,15,8,12,4,9,1,2,
    15,5,1,3,7,14,6,9,11,8,12,2,10,0,4,13,
    8,6,4,1,3,11,15,0,5,12,2,13,9,7,10,14,
    12,15,10,4,1,5,8,7,6,2,13,14,0,3,9,11
};
static const int SL[80] = {
    11,14,15,12,5,8,7,9,11,13,14,15,6,7,9,8,
    7,6,8,13,11,9,7,15,7,12,15,9,11,7,13,12,
    11,13,6,7,14,9,13,15,14,8,13,6,5,12,7,5,
    11,12,14,15,14,15,9,8,9,14,5,6,8,6,5,12,
    9,15,5,11,6,8,13,12,5,12,13,14,11,8,5,6
};
static const int SR2[80] = {
    8,9,9,11,13,15,15,5,7,7,8,11,14,14,12,6,
    9,13,15,7,12,8,9,11,7,7,12,7,6,15,13,11,
    9,7,15,11,8,6,6,14,12,13,5,14,13,13,7,5,
    15,5,8,11,14,14,6,14,6,9,12,9,12,5,15,8,
    8,5,12,9,12,5,14,6,8,13,6,5,15,13,11,11
};

static void ripemd160_transform(uint32_t state[5], const uint8_t block[64]) {
    uint32_t al=state[0],bl=state[1],cl=state[2],dl=state[3],el=state[4];
    uint32_t ar=state[0],br=state[1],cr=state[2],dr=state[3],er=state[4];
    uint32_t X[16], t;
    int i;
    for (i = 0; i < 16; i++)
        X[i] = ((uint32_t)block[i*4])|((uint32_t)block[i*4+1]<<8)|
               ((uint32_t)block[i*4+2]<<16)|((uint32_t)block[i*4+3]<<24);
    for (i = 0; i < 80; i++) {
        uint32_t fl, fr, kl, kr, wl, wr;
        if (i < 16)       fl = bl ^ cl ^ dl;
        else if (i < 32)  fl = (bl & cl) | (~bl & dl);
        else if (i < 48)  fl = (bl | ~cl) ^ dl;
        else if (i < 64)  fl = (bl & dl) | (cl & ~dl);
        else               fl = bl ^ (cl | ~dl);
        if (i < 16)       fr = br ^ (cr | ~dr);
        else if (i < 32)  fr = (br & dr) | (cr & ~dr);
        else if (i < 48)  fr = (br | ~cr) ^ dr;
        else if (i < 64)  fr = (br & cr) | (~br & dr);
        else               fr = br ^ cr ^ dr;
        if (i < 16)       kl = 0x00000000;
        else if (i < 32)  kl = 0x5a827999;
        else if (i < 48)  kl = 0x6ed9eba1;
        else if (i < 64)  kl = 0x8f1bbcdc;
        else               kl = 0xa953fd4e;
        if (i < 16)       kr = 0x50a28be6;
        else if (i < 32)  kr = 0x5c4dd124;
        else if (i < 48)  kr = 0x6d703ef3;
        else if (i < 64)  kr = 0x7a6d76e9;
        else               kr = 0x00000000;
        wl = X[RL[i]];
        wr = X[RR2[i]];
        t = al + fl + wl + kl;
        t = RL32(t, SL[i]) + el;
        al = el; el = dl; dl = RL32(cl, 10); cl = bl; bl = t;
        t = ar + fr + wr + kr;
        t = RL32(t, SR2[i]) + er;
        ar = er; er = dr; dr = RL32(cr, 10); cr = br; br = t;
    }
    t = state[1] + cl + dr; state[1] = state[2] + dl + er;
    state[2] = state[3] + el + ar; state[3] = state[4] + al + br;
    state[4] = state[0] + bl + cr; state[0] = t;
}

static void ripemd160(const uint8_t *in, size_t len, uint8_t out[20]) {
    uint32_t state[5] = {0x67452301, 0xefcdab89, 0x98badcfe, 0x10325476, 0xc3d2e1f0};
    uint8_t buf[64];
    size_t i, j, n = len / 64;
    for (i = 0; i < n; i++)
        ripemd160_transform(state, in + i * 64);
    j = len % 64;
    memset(buf, 0, 64);
    memcpy(buf, in + n * 64, j);
    buf[j] = 0x80;
    if (j > 55) { ripemd160_transform(state, buf); memset(buf, 0, 64); }
    uint64_t bits = (uint64_t)len * 8;
    buf[56] = (uint8_t)bits; buf[57] = (uint8_t)(bits>>8);
    buf[58] = (uint8_t)(bits>>16); buf[59] = (uint8_t)(bits>>24);
    buf[60] = (uint8_t)(bits>>32); buf[61] = (uint8_t)(bits>>40);
    buf[62] = (uint8_t)(bits>>48); buf[63] = (uint8_t)(bits>>56);
    ripemd160_transform(state, buf);
    for (i = 0; i < 5; i++) {
        out[i*4]   = (uint8_t)(state[i]);
        out[i*4+1] = (uint8_t)(state[i]>>8);
        out[i*4+2] = (uint8_t)(state[i]>>16);
        out[i*4+3] = (uint8_t)(state[i]>>24);
    }
}

int main(void) {
    uint8_t out[20];
    int i;
    /* Test 1: empty string */
    ripemd160(NULL, 0, out);
    printf("RIPEMD160(\"\") = ");
    for (i = 0; i < 20; i++) printf("%02x", out[i]);
    printf("\nExpected:        9c1185a5c5e9fc54612808977ee8f548b2258d31\n");
    /* Test 2: "abc" */
    ripemd160((const uint8_t*)"abc", 3, out);
    printf("RIPEMD160(\"abc\") = ");
    for (i = 0; i < 20; i++) printf("%02x", out[i]);
    printf("\nExpected:         8eb208f7e05d987a9b044a8e98c6b087f15a0bfc\n");
    return 0;
}