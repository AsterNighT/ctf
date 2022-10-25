import sympy

print(sympy.solve("((((-1)-(2+2))-((i%2)-(3+2)))*(((3+1)+(-2))%((3+i)*(3-2))))-34254154830",
      [sympy.Symbol('i')]))
