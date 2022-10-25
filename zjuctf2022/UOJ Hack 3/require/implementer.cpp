#include "convince.h"
#include "uoj_secure.h"
#include <stdio.h>
#include <string.h>
#include <assert.h>

#define SECRET "AAATOKEN"
#define SPLIT_TOKEN "fake{flag}"

int main()
{
	uoj_secure_io io;
	io.init_with_key(SECRET);
	convince();
	io.out << SPLIT_TOKEN << "\n";
	io.out << "0\nWo bu sou qian\n";
	
	io.end();

	return 0;
}
