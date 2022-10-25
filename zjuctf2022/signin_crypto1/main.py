import os

real_flag = 'ZJUCTF{...}'
fake_flag = 'ZJUCTF{Fe15tel_c1pher_i5_e@sy_f0r_y0u_2}'


def xor(a, b):
    return ''.join(chr(ord(x) ^ ord(y)) for (x, y) in zip(a, b))


def str_to_hex(s):
    return s.encode().hex()


def swap(a):
    return a[16:] + a[:16]


def single(m, k):
    assert len(m) == 32
    l = m[: 16]
    r = m[16:]
    nl, nr = r, xor(k, xor(l, r))
    return nl + nr


def encrypt(m, k):
    for i in k:
        m = single(m, i)
    return swap(m)


k = []
for i in range(0, 16):
    k.append(os.urandom(8).hex())

# print(str_to_hex(encrypt(fake_flag[7: -1], k)))
# print(str_to_hex(encrypt(real_flag[7: -1], k)))

enc_fake = bytes.fromhex(
    '3a6d603c3d656d61673e6c6e653934316d6a393b646d67613b36613165363d37').decode('utf-8')
enc_real = bytes.fromhex(
    '180f371830755d0f3078102b673b65396d54391a24210e3438715b7f61250163').decode('utf-8')

def get_k():
    em = swap(enc_fake)
    eml = em[: 16]
    emr = em[16: ]
    ml = fake_flag[7: -1][: 16]
    mr = fake_flag[7: -1][16: ]
    ka = xor(mr,eml)
    kb = xor(xor(ml, mr), emr)
    return [ka, kb]

def get_ans(ka, kb):
    em = swap(enc_real)
    eml = em[: 16]
    emr = em[16: ]
    mr = xor(eml, ka) 
    ml = xor(xor(emr, mr), kb)
    return ml + mr

ka, kb = get_k()
print(get_ans(ka, kb))
