import parser
import copy
import string
import pwn

def dfs(root: parser.Node, target: int, known_values: dict):
    if root.value == '0':
        return target == None or target == 0, known_values
    if root.value in string.ascii_lowercase:
        if target == None:
            new_dict = dict(known_values)
            new_dict[root.value] = 0
            return 1, new_dict
        if (not root.value in known_values) or known_values[root.value] == target:
            new_dict = dict(known_values)
            new_dict[root.value] = target
            return 1, new_dict
        else:
            return 0, known_values
    if target == None:
        ok1, tmp_dict = dfs(root.children[0], None, known_values)
        ok2, new_dict = dfs(root.children[1], None, tmp_dict)
        return ok1 and ok2, new_dict
    if root.value == '+':
        ok1, tmp_dict = dfs(root.children[0], target, known_values)
        ok2, new_dict = dfs(root.children[1], 0, tmp_dict)
        if ok1 and ok2:
            return 1, new_dict
        ok1, tmp_dict = dfs(root.children[0], 0, known_values)
        ok2, new_dict = dfs(root.children[1], target, tmp_dict)
        if ok1 and ok2:
            return 1, new_dict
        ok1, tmp_dict = dfs(root.children[0], 1, known_values)
        ok2, new_dict = dfs(root.children[1], target-1, tmp_dict)
        if ok1 and ok2:
            return 1, new_dict
        ok1, tmp_dict = dfs(root.children[0], target-1, known_values)
        ok2, new_dict = dfs(root.children[1], 1, tmp_dict)
        if ok1 and ok2:
            return 1, new_dict
    if root.value == '-':
        ok1, tmp_dict = dfs(root.children[0], target, known_values)
        ok2, new_dict = dfs(root.children[1], 0, tmp_dict)
        if ok1 and ok2:
            return 1, new_dict
        ok1, tmp_dict = dfs(root.children[0], target+1, known_values)
        ok2, new_dict = dfs(root.children[1], 1, tmp_dict)
        if ok1 and ok2:
            return 1, new_dict
        ok1, tmp_dict = dfs(root.children[0], 0, known_values)
        ok2, new_dict = dfs(root.children[1], -target, tmp_dict)
        if ok1 and ok2:
            return 1, new_dict
        ok1, tmp_dict = dfs(root.children[0], 1, known_values)
        ok2, new_dict = dfs(root.children[1], -target-1, tmp_dict)
        if ok1 and ok2:
            return 1, new_dict
    if root.value == '*':
        ok1, tmp_dict = dfs(root.children[0], target, known_values)
        ok2, new_dict = dfs(root.children[1], 1, tmp_dict)
        if ok1 and ok2:
            return 1, new_dict
        ok1, tmp_dict = dfs(root.children[0], 1, known_values)
        ok2, new_dict = dfs(root.children[1], target, tmp_dict)
        if ok1 and ok2:
            return 1, new_dict
        ok1, tmp_dict = dfs(root.children[0], 0, known_values)
        ok2, new_dict = dfs(root.children[1], 0, tmp_dict)
        if target == 0 and ok1 and ok2:
            return 1, new_dict
    if root.value == '/':
        ok1, tmp_dict = dfs(root.children[0], target, known_values)
        ok2, new_dict = dfs(root.children[1], 1, tmp_dict)
        if ok1 and ok2:
            return 1, new_dict
        ok1, tmp_dict = dfs(root.children[0], 0, known_values)
        ok2, new_dict = dfs(root.children[1], None, tmp_dict)
        if target == 0 and ok1 and ok2:
            return 1, new_dict
    if root.value == '%':
        ok1, tmp_dict = dfs(root.children[0], target, known_values)
        ok2, new_dict = dfs(root.children[1], 0, tmp_dict)
        if ok1 and ok2:
            return 1, new_dict
        ok1, tmp_dict = dfs(root.children[0], target, known_values)
        ok2, new_dict = dfs(root.children[1], target+1, tmp_dict)
        if ok1 and ok2:
            return 1, new_dict
        ok1, tmp_dict = dfs(root.children[0], 0, known_values)
        ok2, new_dict = dfs(root.children[1], None, tmp_dict)
        if target == 0 and ok1 and ok2:
            return 1, new_dict
    return 0, known_values

sh = pwn.remote("202.38.93.111",10700)

sh.sendline(
    b'277:MEUCIQCAoEmqI4k9dTKqYhiibw5OfBQPsOg1ZDW2IhXlMOe7jAIgQ1akwUHixIoX+1KcwZGVpPEgc7pBIEvu8vY1OcS0l6g=')
print(sh.recvline())

for _ in range(100):
    str = sh.recvline().decode().strip()
    print(str)
    target = int(sh.recvline())
    print(target)
    values = dict()
    ast = parser.parse(str)
    ok, values = dfs(ast,target,dict())
    if ok:
        ans = ""
        for key in values:
            ans = ans+"{}={} ".format(key, values[key])
        print(ans)
        sh.sendline(ans.encode())
    else:
        sh.sendline(b"")

sh.interactive()
