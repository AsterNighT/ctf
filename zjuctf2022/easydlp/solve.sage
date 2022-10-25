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
