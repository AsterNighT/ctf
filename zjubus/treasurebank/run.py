from pwn import *
from hashpumpy import hashpump
from base64 import *

new_username = "asternight"
password = "fb791ff6717243fcc8dd9e37c79bb29f"
vip = "aaadwg"

for salt_length in range(8,33):
    target = remote('10.214.160.13', 11013)
    new_hash, message = hashpump(password, new_username, vip, salt_length)
    target.recv()
    print(message,new_hash)
    payload = '{{"username":"{}","passcode":"{}"}}'.format(
        b64encode(message).decode(), b64encode(new_hash.encode()).decode())
    print(payload)
    target.sendline(payload.encode())
    try:
        response = target.recv()
        print(response)
    except EOFError:
        continue
