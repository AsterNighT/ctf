from ecdaa import *
from pwn import *

rr = process(['python3', 'ecdaa.py'], stderr=2)
X, Y = deserialize4json(E, rr.recvline().strip().decode())
A, B, C, Ev = deserialize4json(E, rr.recvline().strip().decode())
pa = e(A, X)
pb = e(B, X)
pc = e(C, H)
bsn = b'ZJU_AAA'
for _ in range(10):
    r2, = deserialize4json(E, rr.recvline().strip().decode())
    A2 = r2 * A
    B2 = r2 * B
    C2 = r2 * C
    E2 = r2 * Ev
    print('send ABCE')
    rr.sendline(serialize2json(A2, B2, C2, E2).encode())
    D2, = deserialize4json(E, rr.recvline().strip().decode())
    pa2 = pa ** r2
    pb2 = pb ** r2
    pc2 = pc ** r2
    t = e(D2, X)
    c2 = Hn(q, 3, bsn, X, Y, A2, B2, C2, D2, E2, pa2, pb2, pc2, t)
    print('send c2')
    rr.sendline(serialize2json(c2).encode())
    print(rr.recvline().strip().decode())

print(rr.recvline().strip().decode())
