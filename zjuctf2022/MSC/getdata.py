from pwn import *
from Crypto.Util.strxor import strxor

sh = remote('10.214.160.76', 46597)
log.setLevel('debug')
data = b''

pad = b'c'*28
small_pad = b'AAA{'
sleep(1)
sh.recv()
for i in range(89):
    sh.sendline(b'1')
    sh.recv()
    sh.sendline(pad)
    data_str = sh.recv().decode('utf-8')
    log.debug(data_str)
    data_get_xor = eval(re.match(r'(b[\'\"].+[\'\"])', data_str).group(1))
    assert(len(data_get_xor) == 28)
    # print(data_get_xor)
    data += strxor(data_get_xor, pad)

sleep(1)
sh.sendline(b'2')
tmp = eval(re.match(r'(b[\'\"].+[\'\"])', sh.recv().decode('utf-8')).group(1))
assert(len(tmp) == 28)
flag_enc = tmp
data += strxor(flag_enc[:4], small_pad)
with open("data_extracted.bin", "w") as binary_file:
    # Write bytes to file
    binary_file.write(data)

with open("flag.bin", "wb") as binary_file:
    # Write bytes to file
    binary_file.write(flag_enc)
