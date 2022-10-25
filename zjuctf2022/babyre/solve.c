
#include <stdio.h>
#include "sm4.h"
char *key = "xpLBYaJVKyjX^cwd";
char cmp[16] = {0x36, 0x6D, 0xED, 0x6B, 0xFE, 0x88, 0x3B, 0xC9, 0x01, 0xA5, 0x37, 0xA5, 0x03, 0xC2, 0x3C, 0x02};
char 
int main()
{
    char output[16];
    sm4_context ctx;
    sm4_setkey_enc(&ctx, key);
    sm4_crypt_ecb(&ctx, SM4_ENCRYPT, 16, key, output);
    for(int i=0;i<16;i++){
        output[i]^=cmp[i];
    }
    printf("%s", output);
}