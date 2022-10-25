from Crypto.Util.number import *

(p1, a1, b1) = (1383333670554863678551666822362196239242273588051,
                299446119796668317821474260946629183722027371877, 722591700505463573820128374277044703680164144116)
E1 = EllipticCurve(GF(p1), [a1, b1])
assert E1.order() == p1

P1 = E1(221504092673696048756389221905190313468598958747,
        1294055609263533522129037670663961210779668618001)

print(factor(P1.order()))