from base64 import *

cipher = 'Dq4l/8bPnCsynznU2relLC+oGsq+xIBhBrgF+ZKHgjkM6yrxxsOyDzLuB4mDp6kHKZYkyqWf+HIGqDv1xITzJhutD/nGkpwoMp89y82doQcshjjKubX9cwbpAdudk7gGA+lY7I+8+R4umAOKho65CDOsO82lnJx/BrgJyZjA/ycOvg/qwMOYEzCkPdWEgeQMcOUJyLmMjCURkUPbnZeGPA+6WIU='


def xor(text, key, key_len):
    new_text = list(text)
    for i in range(len(text)):
        new_text[i] = key[i % key_len] ^ text[i]
    return bytes(new_text)


d64c = b64decode(cipher)

print(len(d64c))


def inB64(char):
    return (char >= ord('A') and char <= ord('Z')) or (char >= ord('a') and char <= ord('z')) or (char >= ord('0') and char <= ord('9')) or char == ord('+') or char == ord('/') or char == ord('=')


def dfs(key, pos, length):
    if pos == length:
        print(key.hex())
        print(xor(b64decode(xor(b64decode(cipher), key, length)), key, length))
        return
    for value in range(255):
        good = 1
        for p in range(pos, len(d64c), length):
            result = value ^ d64c[p]
            if inB64(result):
                continue
            else :
                good = 0
                break
        if good:
            key[pos] = value
            dfs(key, pos+1, length)


for key_len in range(1, 14):
    key = bytearray(key_len)
    dfs(key,0,key_len)
