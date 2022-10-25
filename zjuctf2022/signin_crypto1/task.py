import os

real_flag = 'ZJUCTF{...}'
fake_flag = 'ZJUCTF{d9f0995d706ccc255aea356335e74fcf}'

def xor(a, b):
	return ''.join(chr(ord(x) ^ ord(y)) for (x, y) in zip(a, b))

def str_to_hex(s):
    return s.encode().hex()

def swap(a):
    return a[16: ] + a[ :16]

def single(m, k):
	assert len(m) == 32
	l = m[: 16]
	r = m[16: ]
	nl, nr = r, xor(k, xor(l, r))
	return nl + nr

def encrypt(m, k):
	for i in k:
		m = single(m, i)
	return swap(m)

k = []
for i in range(0, 16):
	k.append(os.urandom(8).hex())

print(str_to_hex(encrypt(fake_flag[7: -1], k)))
print(str_to_hex(encrypt(real_flag[7: -1], k)))

# 3a6d603c3d656d61673e6c6e653934316d6a393b646d67613b36613165363d37
# 180f371830755d0f3078102b673b65396d54391a24210e3438715b7f61250163