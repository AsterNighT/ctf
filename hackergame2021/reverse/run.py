def exgcd(m, n):
	if n == 0:
		x = 1
		y = 0
		return (m, x, y)
	a1 = b = 1
	a = b1 = 0
	c = m
	d = n
	q = c//d
	r = c % d
	while r:
		c = d
		d = r
		t = a1
		a1 = a
		a = t-q*a
		t = b1
		b1 = b
		b = t-q*b
		q = c//d
		r = c % d
	x = a
	y = b
	return (d, x, y)

def getx(a,b,c,mod) -> int:
    g,s,t = exgcd(a,mod)
    if b%g!=0:
        return -1
    assert(b%g==0)
    mult = b//g
    assert(mod%g==0)
    diff = mod//g
    s %= mod
    s *= mult; # a first answer
    s = s%diff;
    while (s&a)!=c:
        s += diff
        if s>=mod:
            return -1
    
    return s

def getx1(a,b,mod) -> int:
    g, s, t = exgcd(a, mod)
    if b%g!=0:
        return -1
    assert(b%g==0)
    mult = b//g
    assert(mod%g==0)
    diff = mod//g
    s %= mod
    s *= mult; # a first answer
    s %= mod
    # s = s%diff;  
    return s


mod = 0x10000000000000000
a1 = 0x850F266C39DD823B # x1 * a1 = b1
b1 = 0xEE895D6C20781AC6
c1 = 0x8007204029000032 # x1 & a1 = c1
x1 = getx(a1, b1, c1, mod)
print(x1)
a2 = 0x4297CF57329641CF
b2 = 0xA363D80CA57F7483
c2 = 0x421700002090410D
x2 = getx(a2, b2, c2, mod)
print(x2)

iterations = len("7777777777")

for _ in range(iterations):
    b = x2
    x2 = x1
    coef = (((x2 - 0x2390937CFD599EB5) | 1) & 0x9AB7943E333D2205)
    x1 = getx1(coef, b, mod)

print(hex(x1))
print(hex(x2))
#ZVm4FYWV
#yl57tz99
#ZVm4FYWVyl57tz99
