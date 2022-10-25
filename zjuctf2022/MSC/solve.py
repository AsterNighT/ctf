from sage.all import *
from random import Random
from tqdm import tqdm
from Crypto.Util.strxor import strxor
# 根据文件中的信息，构造矩阵

length = 19968


def buildMatrix():
    length = 19968
    cnt = 0
    m = matrix(GF(2), length, length)
    file = open("Matrix", "r")
    for i in tqdm(range(length*length)):
        num = int(file.read(1))
        row = cnt // 19968
        col = cnt % 19968
        m[row, col] = num
        cnt += 1
    return m


m = buildMatrix()


def read_data():
    data = []
    file = open("data_extracted.bin", "rb")
    for i in range(length//8):
        x = file.read(1)
        data += [int(b) for b in bin(int.from_bytes(x,'little'))[2:].zfill(8)]
    return data

# X = Z*(T^-1)


def recoverState(leak):
    x = m.solve_left(leak)
    x = ''.join([str(i) for i in x])
    state = []
    for i in range(624):
        tmp = int(x[i * 32:(i + 1) * 32], 2)
        state.append(tmp)
    return (3, tuple(state+[0]), None)


# 根据题型2,还原state,有两种可能,这时候可以用暴破
def backfirst(state):
    high = 0x80000000
    low = 0x7fffffff
    mask = 0x9908b0df
    tmp = state[623] ^ state[396]
    if tmp & high == high:
        tmp ^= mask
        tmp <<= 1
        tmp |= 1
    else:
        tmp <<= 1
    return (1 << 32 - 1) | tmp & low, tmp & low


def pwn(leak):
    state = recoverState(leak)
    L = [leak[i] for i in range(100)]
    prng = Random()
    guess1, guess2 = backfirst(state)
    print(guess1, guess2)
    state[0] = guess1
    s = state
    prng.setstate((3, tuple(s + [0]), None))
    g1 = [prng.getrandbits(1) for i in range(100)]
    if g1 == L:
        print("first")
        prng.setstate((3, tuple(s + [0]), None))
        return prng

    state[0] = guess2
    s = state
    prng.setstate((3, tuple(s + [0]), None))
    g2 = [prng.getrandbits(1) for i in range(100)]
    if g2 == L:
        print("second")
        prng.setstate((3, tuple(s + [0]), None))
        return prng


def run():
    prng = Random()
    data = read_data()
    leak = vector(GF(2), data)
    # 恢复state
    state = recoverState(leak)
    prng.setstate(state)
    for i in range(28*89):
        prng.getrandbits(8)
    key = b''
    file = open("flag.bin", "rb")
    data = file.read(28)
    for i in range(28):
        key += bytes([prng.getrandbits(8)])
    print(strxor(key, data))


run()
