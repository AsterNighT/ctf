from __future__ import print_function
print('''pysandbox6: clear __builtins__
why don't we also clear the __builtins__ so that eval can be easier?''')

try:
    input = raw_input
except:
    pass
c = input()
x=globals
_eval = eval

import sys
sys.modules.clear()

for i in list(__builtins__.__dict__.keys()):
    if i not in ["print", "list", ]:
        del(__builtins__.__dict__[i])

for i in (''.__class__.__mro__[-1].__subclasses__()):
    print(i)

print(_eval(c))
