from __future__ import print_function
print('''pysandbox4: clear sys.modules
let's continue, how about sys.modules.clear()? Python2.6.6
flag in current folder, but not ./flag''')

try:
    input = raw_input
except:
    pass
c = input()
x=globals
_eval = eval

import sys
sys.modules.clear()

print(_eval(c, {'__builtins__':{}}, {}))
