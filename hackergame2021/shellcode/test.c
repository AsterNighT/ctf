
// gcc overflow.c -O0 -g -o overflow
#include <stdio.h>
#include <string.h>
#include <assert.h>
#include <unistd.h>
#include <sys/mman.h>

const char code[100] = "\xba\x10\x00\x00\x00\x68\x72\x6c\x64\x10\x68\x6f\x20\x77\x6f\x68\x68\x65\x6c\x6c\x6a\x00\x89\xe1\xbb\x01\x00\x00\x00\xb8\x04\x00\x00\x00\xcd\x80\xb8\x01\x00\x00\x00\xcd\x80";

int main()
{
    void *addr;
    addr = mmap(0x23333000, 0x1000, PROT_READ | PROT_WRITE | PROT_EXEC, MAP_PRIVATE | MAP_ANONYMOUS, -1, 0);
    assert(addr != MAP_FAILED);
    memcpy(addr, code, 100);
    ((void (*)(void))addr)();
    return 0;
}
