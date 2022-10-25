from __future__ import print_function
print('''pysandbox3: easy ls
how about eval in empty dict? Python2.7
flag in current folder, but not ./flag''')

try:
    input = raw_input
except:
    pass
c = input()
x=globals
_eval = eval

print(_eval(c, {'__builtins__':{}}, {}))
