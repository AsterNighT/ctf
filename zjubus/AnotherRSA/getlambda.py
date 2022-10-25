from random import randint
import re
import pwn
import math

server = pwn.remote('kuroneko.nekotachi.sshz.org', 25286)

server.recvuntil(b'd =')

r = 0

for _ in range(100):
    d = randint(1000000000, 9999999999)
    server.sendline(str(d).encode())
    data = server.recvuntil(b'd =').decode()
    e = re.search(r'(?<=e \= )\d+', data).group(0)
    print(e)
    e = int(e)
    if e == 0:
        continue
    if r == 0:
        r = d*e-1
    else:
        r = math.gcd(r, d*e-1)

print('r = '+str(r))
