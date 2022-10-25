#!/usr/bin/env python3

import os, base64, time, random, string
from Crypto.Cipher import AES
from hashlib import sha1, sha256, md5

key = os.urandom(16)
iv = os.urandom(16)

def pad(msg: bytes) -> bytes:
    pad_length = 16-len(msg)%16
    return msg+(chr(pad_length)*pad_length).encode()

def unpad(msg: bytes):
    # assert bytes([msg[-1]]) * msg[-1] == msg[-msg[-1]:], "padding error!"
    return msg[:-msg[-1]]

def encrypt(msg: bytes):
    msg = pad(msg)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    encrypted = cipher.encrypt(msg)
    return encrypted

def decrypt(iv:bytes, msg: bytes):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted = cipher.decrypt(msg)
    decrypted = unpad(decrypted)
    return decrypted

def send_msg(msg):
    encrypted = encrypt(msg)
    msg = iv+encrypted
    msg = base64.b64encode(msg)
    print(msg.decode())
    return

def recv_msg():
    msg = input().encode()
    try:
        msg = base64.b64decode(msg)
        assert len(msg) < 500
        decrypted = decrypt(msg[:16], msg[16:])
        return decrypted
    except:
        print(b'Error')
        exit(0)

def proof_of_work():
    proof = ''.join([random.choice(string.ascii_letters+string.digits) for _ in range(20)])
    digest = sha256(proof.encode()).hexdigest()
    print("sha256(XXXX+%s) == %s" % (proof[4:], digest))
    x = input('Give me XXXX:')
    if len(x)!=4 or sha256((x+proof[4:]).encode()).hexdigest() != digest: 
        print("Sorry~ bye~")
        return False
    print("Right!")
    return True

msg = b"1234567890123456"
send_msg(msg)


if __name__1 == '__main__':
    if not proof_of_work():
        exit(0)

    with open('/flag.txt', 'rb') as f:
        flag = f.read().strip()

    # give you some knowledge of flag
    assert flag.startswith(b'AAA{') and flag.endswith(b'}')
    assert len(flag) == 16

    # encrypt and sent it
    send_msg(b'Welcome!!')

    while True:
        try:

            msg = recv_msg().strip()
            if msg.startswith(b'exit'):
                print("OK, exit")
                exit(0)

            elif msg.startswith(b'flag'):
                print("OK, here is flag:")
                send_msg(flag)

            elif msg.startswith(b'md5'):
                print("OK, here is md5:")
                send_msg(md5(msg[7:]).digest())

            elif msg.startswith(b'time'):
                print("OK, here is time:")
                send_msg(str(time.time()))

            elif msg.startswith(b'sha1'):
                print("OK, here is sha1:")
                send_msg(sha1(msg[8:]).digest())

            elif msg.startswith(b'sha256'):
                print("OK, here is sha256:")
                send_msg(sha256(msg[10:]).digest())

            else:
                print("Sorry???")
                send_msg(b'command not found')
        except:
            exit(0)
