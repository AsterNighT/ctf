from sage.all import *
from Crypto.Hash import keccak
from Crypto.Util.number import long_to_bytes, bytes_to_long
from struct import unpack
from random import SystemRandom
from json import loads, dumps

def curve_gen(q, a, gx, gy, n):
    Fq = GF(q)
    E = EllipticCurve(Fq, a)
    G = 2 * E(gx, gy)
    G.set_order(n // 2)
    return (E, G)

E, G = curve_gen(16883071526461729727845365244775250968853779238387590508529343289688406548156898561121755709582605065974415626338418885206169694955938439285172466321629894047112152673890080193271092158984773170409123807574649665886686958584517, [16883071526461729727845365244775250968853779238387590508529343289688406548156898561121755709582605065974415626338418885206169694955938439285172466321629894047112152673890080193271092158984773170409123807574649665886686958584513, 50649214579385189183536095734325752906561337715162771525588029869065219644470695683365267128747815197923246879015256655618509084867815317855517398964889682141336458021670240579813276476954319511227371422723948997660060875753551], 14210586178493131406373190825820561003702506574011169828934446821536638945014471344113633023777761432403862087346540040982532990086531969109648355583610945828488439781287611999333627004372849450097379152416521048148055212429932, 7940930756869397961969852165330305368117788150170640034809962841577789648806280962338902036326685993547448607633972933475226268575544844316990777006161391199019112160116189041944360780606412770726712110640687030917392143404191, 129934874173417083152641070462750529831810853051271596159072328195848188613591686285280068379888878197177498309746)
H = 2 * E(558502762260882368459100959026702189372961874916046935897584379942575091607773755509785872627683092849646763384923491591737048593593911906848644811657443277980186172014888060411213151459022266424905365693967579209745952778762, 5244497032739641374363689610162896907859634278068877212817118029249551959220656759501163866935794467197122778877280355210299933485519765003782178469195042075397340131431018419860106520716072042537547362606695008442528534605810)

assert E.order() == E.base_field().order() - 1
A = sqrt(E.order())
q = A // 2
assert isinstance(A, Integer)

def e(P, Q):
    return P.weil_pairing(Q, A)

prng = SystemRandom()

def n2s(n):
    buf = long_to_bytes(n)
    return len(buf).to_bytes(8, 'big') + buf

def s2n(s):
    length = int.from_bytes(s[:8], 'big')
    return bytes_to_long(s[8:8+length]), s[8+length]

def serialize2bytes(*args) -> bytes:
    result = b''
    for arg in args:
        if isinstance(arg, bytes):
            result += arg
        elif isinstance(arg, int):
            result += n2s(arg)
        elif arg is None:
            pass
        elif isinstance(arg, list):
            result += n2s(len(arg))
            result += serialize2bytes(*arg)
        elif arg in E:
            result += n2s(int(arg.xy()[0])) + n2s(int(arg.xy()[1]))
        else:
            result += n2s(int(arg))
    return result

def HF(*args):
    k = keccak.new(digest_bits=256)
    k.update(serialize2bytes(*args))
    return k.digest()

def Hn(n, *args):
    value = int.from_bytes(HF(b'H_n', *args), 'big')
    return value % (n - 1) + 1

def Hp(E, G, *args):
    value = int.from_bytes(HF(b'H_p', *args), 'big')
    q = E.base_field().order()
    x = value % (q - 1) + 1
    jump, iter = unpack('<QI', HF(b'H_p_additional', *args)[:12])
    while True:
        pts = E.lift_x(x, all=True)
        if len(pts) > 0:
            candidate = pts[iter % len(pts)]
            if G.order() * candidate == E(0):
                return candidate
        x = (x - 1 + jump) % (q - 1) + 1

def serialize2json(*args):
    def s2d(v):
        if isinstance(v, tuple):
            return {"type": "tuple", "value": [s2d(i) for i in v]}
        elif isinstance(v, list):
            return {"type": "list", "value": [s2d(i) for i in v]}
        elif isinstance(v, set):
            return {"type": "set", "value": [s2d(i) for i in list(v)]}
        elif isinstance(v, int):
            return {"type": "int", "value": str(v)}
        elif isinstance(v, Integer):
            return {"type": "integer", "value": str(v)}
        elif isinstance(v, bytes):
            return {"type": "bytes", "value": v.hex()}
        elif isinstance(v, str):
            return {"type": "str", "value": v}
        elif isinstance(v, dict):
            return {"type": "dict", "value": [[s2d(key), s2d(value)] for key, value in v.items()]}
        else:
            return {"type": "point", "value": [str(v.xy()[0]), str(v.xy()[1])]}
    return dumps(s2d(args))

def deserialize4json(E, json):
    def d4d(v: dict):
        type_str = v['type']
        value = v['value']
        if type_str == "tuple":
            return (d4d(i) for i in value)
        elif type_str == "list":
            return [d4d(i) for i in value]
        elif type_str == "set":
            return set([d4d(i) for i in value])
        elif type_str == "int":
            return int(value)
        elif type_str == "integer":
            return Integer(int(value))
        elif type_str == "bytes":
            return bytes.fromhex(value)
        elif type_str == "dict":
            ret = dict()
            for [k, v] in value:
                ret[d4d(k)] = d4d(v)
            return ret
        elif type_str == "point":
            return E(int(value[0]), int(value[1]))
    return d4d(loads(json))

def ecdaa(cnt):
    # Inter(Issuer) generate it's private key and public key
    x = prng.randint(0, q)
    y = prng.randint(0, q)
    X = x * H
    Y = y * H
    print(serialize2json(X, Y))
    ## Inter initialize the TPM device on your brand new computer
    # step 1. I generate n1 -> M
    pass
    # step 2. M gen f and F=fG
    f = prng.randint(0, q)
    F = f * G
    # step 3. M zkProof {(f): F=fG} -> I
    pass
    # step 4/5. I gen r, A=rG, B=yA, C=xA+rxyF -> M
    r = prng.randint(0, q)
    A = r * G
    B = y * A
    C = x * A + r * x * y * F
    # step 6. M E=fB, A,B,C -> H
    Ev = f * B
    print(serialize2json(A, B, C, Ev))
    bsn = b'ZJU_AAA'
    full = set()
    for _ in range(cnt):
        ## SIGN: this part is complete by your HOST(you can change it), and TPM(which you cannot change here)
        r2 = Hn(q, 2, f, bsn)
        print(serialize2json(r2))
        A2, B2, C2, E2 = deserialize4json(E, input())
        A2 = E(int(A2.xy()[0]), int(A2.xy()[1]))
        B2 = E(int(B2.xy()[0]), int(B2.xy()[1]))
        C2 = E(int(C2.xy()[0]), int(C2.xy()[1]))
        E2 = E(int(E2.xy()[0]), int(E2.xy()[1]))
        assert E2 == f * B2
        assert e(A2, X) * e(B2, X) ** f == e(C2, H)
        v = prng.randint(0, q)
        D2 = v * r2 * B
        print(serialize2json(D2))
        c2, = deserialize4json(E, input())
        c2 = int(c2) % q
        c = Hn(q, 4, c2)
        s = v + c * f
        ## VERIFICATION: the netizens check you're right
        assert e(A2, Y) == e(B2, H)
        pa = e(A2, X)
        pb = e(B2, X)
        pc = e(C2, H)
        t = pb**s / (pc / pa)**c
        D2 = s * B2 - c * E2
        c2 = Hn(q, 3, bsn, X, Y, A2, B2, C2, D2, E2, pa, pb, pc, t)
        assert c == Hn(q, 4, c2)
        ## LINK: the netizens check the count of you're device
        full.add(serialize2json(E2))
        print('nice, you prove me that you have', len(full), 'computers')
    if len(full) == cnt:
        print('you\'re richman, QAQ! flag: ', open('flag').read())

if __name__ == '__main__':
    ecdaa(10)