#! /bin/bash/env python3
from sage.all import *
from random import Random
from tqdm import tqdm
prng = Random()
length = 19968


def myState():
    state = [0]*624
    i = 0
    while i < length:
        ind = i//32
        expont = i % 32
        state[ind] = 1 << (31-expont)
        s = (3, tuple(state+[0]), None)
        yield s
        state[ind] = 0
        i += 1


def getRow():
    rng = Random()
    gs = myState()
    for i in range(length):
        s = next(gs)
        rng.setstate(s)
#         print(s[1][0])
        row = vector(GF(2), [rng.getrandbits(1) for j in range(length)])
        yield row


def buildBox():
    b = matrix(GF(2), length, length)
    rg = getRow()
    for i in tqdm(range(length)):
        b[i] = next(rg)
    return b


def test():
    prng = Random()
    originState = prng.getstate()
    # 这里都是用的MSB,如果采用不同的二进制位(如LSB)最后的矩阵T 也会不同
    leak = vector(GF(2), [prng.getrandbits(1) for i in range(length)])
    b = buildBox()
    f = open("Matrix", "w")
    for i in range(b.nrows()):
        for j in range(b.ncols()):
            f.write(str(b[i, j])+"n")
    f.close()
    x = b.solve_left(leak)
    x = ''.join([str(i) for i in x])
    state = []
    for i in range(624):
        tmp = int(x[i*32:(i+1)*32], 2)
        state.append(tmp)
    prng.setstate(originState)
    prng.getrandbits(1)
    originState = [x for x in prng.getstate()[1][:-1]]
    print(originState[1:] == state[1:])
#     print(state)
    return state, b


test()
