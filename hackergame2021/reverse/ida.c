#include <stdio.h>
#include <stdlib.h>
unsigned long long sub_1160(long long a1, long long a2, unsigned long long x1, unsigned long long x2)
{
    unsigned long long v4; // rdi
    signed long long i;    // [rsp+0h] [rbp-48h]

    for (i = a1 - a2;; i += 0x236FB161CF24921BLL)
    {
        while (1)
        {
            while (1)
            {
                while (i > (long long)0xF90A1445BE4269A7LL)
                {
                    if (i > (long long)0xFF263764591E957FLL)
                    {
                        if (i == 0xFF263764591E9580LL)
                        {
                            i = 0xE2A71A46F20857D5LL;
                        }
                        else
                        {
                            if (i != 0x1E315A8BD1DE33FFLL)
                                goto LABEL_2;
                            i = 0xE2A71A46F20857D5LL;
                            x1 = (x1 & 0x850F266C39DD823BLL ^ 0x8007204029000032LL | (0x850F266C39DD823BLL * x1) ^ 0xEE895D6C20781AC6LL | x2 & 0x4297CF57329641CFLL ^ 0x421700002090410DLL | (0x4297CF57329641CFLL * x2) ^ 0xA363D80CA57F7483LL) != 0;
                        }
                    }
                    else if (i == 0xF90A1445BE4269A8LL)
                    {
                        i = 0xE2A71A46F20857D5LL;
                        printf("2");
                        x1 = x2 | x2 ^ x1;
                    }
                    else
                    {
                        if (i != 0xFBF655FBE11F2B0ALL)
                            goto LABEL_2;
                        i = 0xE2A71A46F20857D5LL;
                        printf("3");
                        x1 = x2 & (x2 ^ x1);
                    }
                }
                if (i > (long long)0xC797982676D65936LL)
                    break;
                if (i == 0x91A9D395DF2B5E71LL)
                {
                    i = 0xE2A71A46F20857D5LL;
                    printf("4");
                    x1 ^= x2;
                }
                else
                {
                    if (i != 0xC6F1C29BEC82A33BLL)
                        goto LABEL_2;
                    i = 0xE2A71A46F20857D5LL;
                    x1 = x2 * (x2 ^ x1);
                }
            }
            if (i != 0xC797982676D65937LL)
                break;
            i = 0xE2A71A46F20857D5LL;
            x1 += x2;
        }
        if (i == 0xE2A71A46F20857D5LL)
            break;
    LABEL_2:
        v4 = x1 * (((x2 - 0x2390937CFD599EB5LL) | 1) & 0x9AB7943E333D2205LL);
        x1 = x2;
        x2 = v4;
    }
    return x1;
}

char printable[] = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!\"#$%&'()*+, -./:;<=>?@[\\]^_`{|}~";

unsigned long long genNum(){
    int length = 99;
    unsigned long long ret = 0;
    for(int i=0;i<8;i++){
        ret <<= 8;
        ret += printable[rand()%length];
    }
    return ret;
} 

int main()
{
    srand(9982757);
    while (1)
    {
        unsigned long long n1 = genNum();
        unsigned long long n2 = genNum();
        if (sub_1160(0x764f7afe2c38e9bd, 0xba7b0e4471c86acc, n1, n2)==0)
        {
            printf("0x%llx 0x%llx",n1,n2);
            return 0;
        }
    }
    return 0;
}
//8g37K3dG4h7IaT7G