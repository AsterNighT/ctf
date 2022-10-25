/*
flexible:
qword [rsp - 0x8]           x1
qword [rsp - 0x10]          x2
qword [rsp - 0x18]          x3
tmp or const:
rax                         c1
rbx                         c2
rcx                         c2
rdx                         c3
rsi                         c4
rdi                         c3
rbp                         c5
r8                          c6
r9                          c7
r10                         c8
r11                         c9
r12                         c10
r13                         c11
r14                         c12
r15                         c13
*/
#include <stdint.h>
#include <stdio.h>

int check(uint64_t x1, uint64_t x2)
{
    uint64_t x3 = 0xbbd46cb9ba707ef1; // this is quite const
a1230:                                //begin
    if (x3 <= 0xf90a1445be4269a7)
    { //1230
        if (x3 > 0xc797982676d65936)
        { // 1290
            if (x3 != 0xc797982676d65937)
            { // 1371
                if (x3 != 0xe2a71a46f20857d5)
                { //1402
                //11e2
                    uint64_t temp = x2;
                    //printf("1");
                    x3 += 0x236fb161cf24921b;
                    x2 = x1;
                    x1 = (((x1 + 0xdc6f6c8302a6614b) | 1) & 0x9ab7943e333d2205) * temp;
                    goto a1230;
                }
                else
                {
                    //1415
                    //printf("2");
                    return x2;
                }
            }
            else
            {
                // 137a
                //printf("3");
                x3 = 0xaa3eb26d68deb10c - x3;
                x2 += x1;
                goto a1230;
            }
        }
        else
        {
            if (x3 == 0x91a9d395df2b5e71)
            { // 1299
            //13cb
                x3 = 0x7450eddcd133b646 - x3;
                x2 ^= x1;
                goto a1230;
            }
            else
            {
                if (x3 != 0xc6f1c29bec82a33b)
                { // 12a2
                //11e2
                    uint64_t temp = x2;
                    x3 += 0x236fb161cf24921b;
                    x2 = x1;
                    x1 = (((x1 + 0xdc6f6c8302a6614b) | 1) & 0x9ab7943e333d2205) * temp;
                    goto a1230;
                }
                else
                {
                    //12b5
                    x3 ^= 0x2456d8dd1e8af4ee;
                    x2 = (x1 ^ x2) * x1;
                    goto a1230;
                }
            }
        }
    }
    else
    {
        if (x3 > 0xff263764591e957f)
        { //123e
            if (x3 == 0xff263764591e9580)
            { //12e0
                x3 ^= 0x1d812d22ab16c255;
                goto a1230;
            }else{
                if (x3 != 0x1e315a8bd1de33ff){//12e9
                    //11e2
                    uint64_t temp = x2;
                    x3 += 0x236fb161cf24921b;
                    x2 = x1;
                    x1 = (((x1 + 0xdc6f6c8302a6614b) | 1) & 0x9ab7943e333d2205) * temp;
                    goto a1230;
                } else {
                    //12f2
                    // too big
                    goto a1230;
                }
            }
        }else {
            if (x3 == 0xf90a1445be4269a8){ //1247
                //139d
                x3 = 0xdbb12e8cb04ac17d - x3;
                x2 = (x1^x2)|x1;
                goto a1230;
            }else {
                if (x3 == 0xfbf655fbe11f2b0a){ // 1250
                    //11e2
                    uint64_t temp = x2;
                    x3 += 0x236fb161cf24921b;
                    x2 = x1;
                    x1 = (((x1 + 0xdc6f6c8302a6614b) | 1) & 0x9ab7943e333d2205) * temp;
                    goto a1230;
                } else {
                    x3 += 0xe6b0c44b10e92ccb;
                    x2 = (x2^x1)&x1;
                    goto a1230;
                }
            }
        }
    }
}

int main(){
    check(0xbbbbaaaa, 0xddddcccc); 
    return 0;
}