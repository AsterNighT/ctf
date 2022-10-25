from pwn import *
from pwnlib import util
import re
r = remote("10.214.160.13", 13333)


def debug(target):
    print(target)


def padding(m, k):
    return b'\x00\x02'+b'\xFF'*(k-len(m)-3)+b'\x00'+m


def fpow(a, n, m):
    if (n == 0):
        return 1
    x = fpow(a, n//2, m)
    x = x*x % m
    if (n % 2 == 1):
        x = x*a % m
    return x

assert(fpow(2,10,1023)==1)

def os2ip(em):
    iem = 0
    for i in range(0, len_k, 2):
        iem += (em[i]*16+em[i+1])*(256**(len_k//2-i//2-1))
    return iem

def i2osp(iem:int):
    octets = b''
    for i in range(0, len_k, 2):
        octets+=(iem%256).to_bytes(2,'big')
        iem//=256
    # octets = b'0x'+octets;
    return octets

def pkcs15(m, e: int, n: int):
    em = padding(m, len_k)
    # debug(em)
    iem = os2ip(em)
    # debug(iem)
    c = fpow(iem, e, n)
    # debug(c)
    return c


pow = r.recvline_contains(b"sha256").decode("utf-8")

match = re.match(r"sha256\(XXXX \+ (\w+)\) == (\w+)", pow)
pow_question = match.group(1)
pow_target = match.group(2)

answer = util.iters.mbruteforce(lambda x: util.hashes.sha256sumhex(
    (x + pow_question).encode("utf-8")) == pow_target, string.ascii_letters+string.digits, 4, "fixed")

r.send(answer.encode("utf-8"))
rsa_params_N = r.recvline_contains(b"N=").decode("utf-8")
len_k = len(rsa_params_N)//2-2
rsa_params_e = r.recvline_contains(b"e=").decode("utf-8")
match = re.match(r"N=(\w+)", rsa_params_N)
N = int(match.group(1), base=16)
debug(N)
match = re.match(r"e=(\w+)", rsa_params_e)
e = int(match.group(1), base=16)
message = b"I am not a noob!"
c = pkcs15(message, e, N)
# debug(c)
r.send(hex(c).encode('utf-8'))
r.interactive()
