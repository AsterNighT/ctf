import pydes
from hashlib import md5

des = pydes.des()

text = "\x00\x00\x00\x00\x00\x00\x00\x00"

cipher = "\xf6\xff\x60\xa7\xd1\xc3\x94\x90"

known_key = ["AAA{xxxx", "x_xxxxx}"]

key_possible_characters = [
    "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz"]

dict = {}


def check(key_no, key):
    global dict
    if key_no == 0:
        if des.encrypt(key, text) in dict:
            dict[des.encrypt(key, text)].append(key)
        else:
            dict[des.encrypt(key, text)] = [key]
    else:
        if key[3] != key[6]:
            return False
        if des.decrypt(key, cipher) in dict:
            for key_ in dict[des.decrypt(key, cipher)]:
                whole_key = key_ + key
                if md5(whole_key.encode()).digest()[0] == 0x89:
                    print("Key: "+whole_key)
                    exit(0)
    return False

def dfs(key_no, pos, key):
    if pos == 8:
        #print(key)
        check(key_no, key)
    else:
        if known_key[key_no][pos] == "x":
            for c in key_possible_characters[key_no]:
                dfs(key_no, pos + 1, key + c)
        else:
            dfs(key_no, pos + 1, key + known_key[key_no][pos])


if __name__ == "__main__":
    dfs(0, 0, "")
    print("encrypt part done")
    dfs(1, 0, "")
    print("decrypt part done")
