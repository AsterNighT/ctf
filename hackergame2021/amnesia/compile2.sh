#!/bin/bash
set -e

function zeroout()
{
	objcopy --dump-section "$1"=sec.bin a.out
	xxd -p sec.bin  | sed 's/[0-9a-f]/0/g' | xxd -r -p > seczero.bin
	objcopy --update-section "$1"=seczero.bin a.out
	rm -f sec.bin
	rm -f seczero.bin
}

gcc -O amnesia2.c -m32 -o a.out
zeroout ".text"
