from pwn import *
import itertools
import string
import hashlib
from base64 import *

IP = "10.214.160.13"
PORT = 12900

p = remote(IP, PORT)

def proof_of_work(suffix, chall):
	for comb in itertools.product(string.ascii_letters+string.digits, repeat=4):
		m = ''.join(comb)
		if hashlib.sha256(m.encode() + suffix).hexdigest() == chall.decode():
			return m
	raise Exception("Not found...")

p.recvuntil(b"XXXX+")
suffix = p.recvuntil(b")")[:-1]
p.recvuntil(b"== ")
chall = p.recvuntil(b"\n")[:-1]
s = proof_of_work(suffix, chall)
p.recvuntil(b"XXXX:")
p.sendline(s.encode())
p.recvuntil(b"Right!\n")

plain = b"Welcome!!"
iv_and_cipher_b64 = p.recvline()
iv_and_cipher = b64decode(iv_and_cipher_b64)
given_iv = iv_and_cipher[:16]
cipher = iv_and_cipher[16:]
log.success(str(len(cipher)))
get_flag = b'flag'

# Now that we got plain and its corresponding cipher, we would construct a b'flag', pad it and create certain iv to make it equal to b"Welcome!!"


def pad(msg: bytes) -> bytes:
    pad_length = 16-len(msg) % 16
    return msg+(chr(pad_length)*pad_length).encode()

pad_plain = pad(plain)
real_bytes = xor(pad_plain, given_iv) # This is the real bytes that yield the iv_and_cipher

def packinst(msg: bytes):
    padded_msg = pad(msg)
    iv = xor(real_bytes, padded_msg)
    return b64encode(iv+cipher)


p.sendline(packinst(get_flag))
p.recvuntil(b"OK, here is flag:\n")
iv_and_flag_b64 = p.recvline()
iv_and_flag = b64decode(iv_and_flag_b64)
print(len(iv_and_flag))
flag = iv_and_flag[16:] # After that are zero paddings

known_flag = b"AAA{"

for i in range(16-4):
    for c in string.printable:
        test_flag = known_flag + c.encode()
        target_sha1 = (i+1)*b" "+b"sha1"
        test_iv = xor(given_iv, xor(test_flag, target_sha1))
        p.sendline(b64encode(test_iv+flag))
        recv = p.recvuntil(b"\n")
        p.recvuntil(b"\n")
        if b'OK' in recv:
            known_flag = known_flag + c.encode()
            print(known_flag)
            break
