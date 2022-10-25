from math import inf
import random
import os
from randcrack import RandCrack

rc = RandCrack()

random.seed(os.urandom(64))

for i in range(624):
    r = random.getrandbits(32)
    choice = r%3
    id_num = (r // 3) ^ (r % 3)

    randombits = (id_num ^ choice)*3+choice
    assert(randombits==r)
    rc.submit(randombits)

for i in range(512)


