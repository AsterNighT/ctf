from pwn import *


def test_flag(candidate):
    assert (len(candidate) == 4)
    known = ("AAA{"+candidate+"}")
    NT = matrix(Zmod(256), 3, 3)
    for i in range(3):
        for j in range(3):
            NT[i, j] = ord(known[i+j*3])
    if (not NT.is_invertible()):
        return False
    return True


alphabet = string.digits + string.ascii_letters + string.punctuation
pwnlib.util.iters.mbruteforce(test_flag, alphabet, 4, 'fixed')

