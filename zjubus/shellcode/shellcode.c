#include <stdio.h>

int main()
{
	int i;
	char c;

	printf("Melody: Mom, I want a shell\n");
	printf("Mom: This machine will run your input as assemble instruction\n");
	fflush(NULL);
    char shellcode[35] = "\x31\xdb\x6a\x17\x58\xcd\x80\xf7\xe3\xb0\x0b\x31\xc9\x51\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\xcd\x80\x00\x00\x00\x00\x00\x00\x00";
    (*(void (*)()) shellcode)();
}
