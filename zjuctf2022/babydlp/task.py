from Crypto.Util.number import *
from sympy.ntheory.modular import crt
from math import ceil, sqrt

p = 22874236765582512818346580947708667745188778288884101219751361699392149989458510773797824610944321686257783426829474659298957510513578978620495392070614563  # prime
# p-1 = 2 · 17 · 2509983517<10> · 2544123481<10> · 2569813369<10> · 2894510363<10> · 2958235517<10> · 4159802197<10> · 4166439437<10> · 2762558262...19<87>

factors = [2, 17, 2509983517, 2544123481,
           2569813369, 2894510363, 2958235517, 4159802197, 4166439437]

# 3*19*83*2746346838107494410916004620610220405114947440834076125445650433925355607575816470554639183290804479291237493373398461949803256064268162370489441087787
g = 12992966891086556058043617860106952736598816342586014149483372202900857379441187722193997976148795991526844581149548123484519204440052676174785545786320297

# c = g^x%p

c = 4006948706881298103593084841644986324930377713436980291670378524564662999515313693489885343780490631115314181593435331209712709857825836348345723998675361
# 7*572421243840185443370440691663569474990053959062425755952911217794951857073616241927126477682927233016473454513347904458530387122546548049763674856953623


def bsgs(a, b, p, ub):
    '''
    Solve for x in a^x=b mod p given a prime p.
    If p is not prime, you shouldn't use BSGS anyway.
    '''
    N = ceil(sqrt(ub))  # phi(p) is p-1 if p is prime
    # Store hashmap of g^{1...m} (mod p). Baby step.
    tbl = {pow(a, i, p): i for i in range(N)}
    # Precompute via Fermat's Little Theorem
    c = pow(a, N * (p - 2), p)

    # Search for an equivalence in the table. Giant step.
    for j in range(N):
        y = (b * pow(c, j, p)) % p
        if y in tbl:
            return j * N + tbl[y]

    # Solution not found
    return None


def pohlighellman(a: int, b: int, p: int, known_factors: list[int]):
    m = known_factors
    v = []
    for f in known_factors:
        u = (p-1)//f
        # for i in range(f):
        #     if pow(a,i*u, p) == pow(b,u,p):
        #         v.append(i)
        #         break
        a0 = bsgs(pow(a, u, p), pow(b, u, p), p, f)
        if (a0 == None):
            print(pow(a, u, p), pow(b, u, p), p, f)
        v.append(a0)
    for i in range(2**9):
        new_m = []
        new_v = []
        for l in range(len(known_factors)):
            if ((i>>l)&(0b1)) == 1:
                new_m.append(m[l])
                new_v.append(v[l])
        print(int.to_bytes(crt(new_m, new_v)[0], 32, 'big'))
    return 
        
pohlighellman(g, c, p, factors)
# print(int.to_bytes(m, 32, 'big'))
