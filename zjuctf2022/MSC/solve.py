from sage.all import *
from random import Random
from tqdm import tqdm
# 根据文件中的信息，构造矩阵


def buildMatrix():
    length = 19968
    cnt = 0
    m = matrix(GF(2), length, length)
    for line in tqdm(open("Matrix", "r")):
        row = cnt // 19968
        col = cnt % 19968
        m[row, col] = int(line.strip('n'))
        cnt += 1
    return m


m = buildMatrix()


# X = Z*(T^-1)
def recoverState(leak):
    x = m.solve_left(leak)
    x = ''.join([str(i) for i in x])
    state = []
    for i in range(624):
        tmp = int(x[i * 32:(i + 1) * 32], 2)
        state.append(tmp)
    return state


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


def test():
    length = 19968
    prng = Random()
    originState = prng.getstate()
    leak = vector(GF(2), [prng.getrandbits(1) for i in range(length)])
    # 恢复state
    state = recoverState(leak)
    prng.setstate(originState)
    prng.getrandbits(1)
    originState = [x for x in prng.getstate()[1][:-1]]
    # 成功恢复623个state
    print(originState[1:] == state[1:])
    # 获取泄露信息
    L = [leak[i] for i in range(100)]
    # 两种可能
    guess1, guess2 = backfirst(state)
    print(guess1, guess2)
    state[0] = guess1
    s = state
    prng.setstate((3, tuple(s + [0]), None))
    g1 = [prng.getrandbits(1) for i in range(100)]
    if g1 == L:
        print("first")
        prng.setstate((3, tuple(s + [0]), None))
        now = vector(GF(2), [prng.getrandbits(1) for i in range(length)])
        if now == leak:
            print("true")
            return
    state[0] = guess2
    s = state
    prng.setstate((3, tuple(s + [0]), None))
    g2 = [prng.getrandbits(1) for i in range(100)]
    if g2 == L:
        print("second")
        prng.setstate((3, tuple(s + [0]), None))
        now = vector(GF(2), [prng.getrandbits(1) for i in range(length)])
        if now == leak:
            print("true")
            return


test()
