import pydes
from hashlib import md5

des = pydes.des()

text = "\x00\x00\x00\x00\x00\x00\x00\x00"

cipher = "\xf6\xff\x60\xa7\xd1\xc3\x94\x90"

known_key = ["AAA{xxxx", "x_xxxxx}"]

print(des.encrypt(known_key[0],text))