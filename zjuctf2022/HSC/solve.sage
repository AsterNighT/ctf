from socketserver import ThreadingUnixStreamServer
from pwn import *

# assert MT.is_invertible()
# flag = "AAA{?????????????????????????}"  # ? means unknown printable char
# FT = matrix(Zmod(256), 3, 10)
# for i in range(3):
# 	for j in range(10):
# 		FT[i, j] = ord(flag[i+j*3])
# RT = MT * FT
# result = b''
# for i in range(10):
# 	for j in range(3):
# 		result += bytes([RT[j, i]])

result = b"\xfc\xf2\x1dE\xf7\xd8\xf7\x1e\xed\xccQ\x8b9:z\xb5\xc7\xca\xea\xcd\xb4b\xdd\xcb\xf2\x939\x0b\xec\xf2"

# result = b'A\xc3A{\x9000\x90}?\xbd??\xbd??\xbd??\xbd??\xbd??\xbd??\xbd}'


RT = matrix(Zmod(256), 3, 10)
for i in range(10):
    for j in range(3):
        RT[j, i] = result[i*3+j]

ResultT = RT[:, :2].augment(RT[:, -1:])

# print(RT)
# print(ResultT.is_invertible())

alphabet = string.digits + string.ascii_letters + string.punctuation

def test(candidate: str):
    assert (len(candidate) == 4)
    if (candidate == 'Bl&4'): 
        return False;
    known = ("AAA{"+candidate+'}')
    NT = matrix(Zmod(256), 3, 3)
    for i in range(3):
        for j in range(3):
            NT[i, j] = ord(known[i+j*3])
    if (not NT.is_invertible()):
        # print('NT inrevetible')
        return False
    MT = ResultT * NT.inverse()
    assert (MT*NT == ResultT)
    if (not MT.is_invertible()):
        # print('MT inrevetible')
        return False
    OT = MT.inverse() * RT
    res = b''
    for i in range(10):
        for j in range(3):
            res += bytes([OT[j, i]])
            if (not chr(OT[j, i]) in alphabet):
                return False
    print(res)
    return True

# sl&1
pwnlib.util.iters.mbruteforce(test, alphabet, 4, 'fixed')
