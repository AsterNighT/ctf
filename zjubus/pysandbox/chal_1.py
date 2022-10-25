from __future__ import print_function
print('''pysandbox1: checkin
Welcome, this is a normal Python2.7 shell, can you get flag in ./flag?''')

try:
    input = raw_input
except:
    pass
c = input()
x=globals
_eval = eval

print(_eval(c))

# print(open("flag").read())