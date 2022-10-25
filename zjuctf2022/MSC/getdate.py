from pwn import *
from Crypto.Util.strxor import strxor

sh = remote('10.214.160.76', 33940)

data = b''

pad = b'c'*28
small_pad = b'AAA{'
sleep(1)
sh.recv()
for i in range(89):
    sh.sendline(b'1')
    sh.recv()
    sh.sendline(pad)
    data_get_xor = sh.recv()[2:30]
    print(data_get_xor)
    data += strxor(data_get_xor, pad)

sleep(1)
sh.sendline(b'2')
tmp = sh.recv()
print(tmp)
flag_enc = tmp[:28]
data += strxor(flag_enc[:4], small_pad)
with open("data_extracted.bin", "wb") as binary_file:
    # Write bytes to file
    binary_file.write(data)

with open("flag.bin", "wb") as binary_file:
    # Write bytes to file
    binary_file.write(flag_enc)
