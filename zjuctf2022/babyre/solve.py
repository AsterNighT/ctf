from operator import xor
from pysm4 import *
from pwn import *
key = 'xpLBYaJVKyjX^cwd'
xorresult = b'\x36\x6D\xED\x6B\xFE\x88\x3B\xC9\x01\xA5\x37\xA5\x03\xC2\x3C\x02'
v6 = b'\x64\x08\x9B\x58\xCA\xBD\x5E\x96\x30\xD6\x68\xC0\x62\xF7\x45\x23'
buffer = bytes(a ^ b for a, b in zip(v6, xorresult))
print(buffer)
