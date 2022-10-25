flag = b'MMMwjau`S]]S}ybS?4:;5:<4<q'

for char in flag:
    char ^= 0xC
    print(chr(char), end="")
