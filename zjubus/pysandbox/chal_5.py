from __future__ import print_function
print('''pysandbox5: clear sys.modules py3
almost same, but move to higher version: Python3.7 with sys.modules.clear() 
try `cat ./flag`''')

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
