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