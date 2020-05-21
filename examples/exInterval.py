"""Example: Interval module"""
from AffApy.intervalArithmetic import Interval

# Init
x = Interval(inf=1, sup=2)
print("x =", x)

y = Interval(3, 4)
print("y =", y)

# Simple operations
print("x + x =", x + x)
z = x + y
print("z =", z)
print("x - 1 =", x - 1)
print("1 + x =", 1 + x)
print("x - x =", x - x)
print("y - y =", y - y)
print("x - y =", x - y)
print("y * 2 = ", y * 2)
print("x * y =", x * y)
print("x + x - x - x =", x + x - x - x)
print("-x =", -x)
print("-x + x =", -x + x)

# Advanced operations
print("x / y =", x / y)
print("y / 2 =", y / 2)
print("x**2 =", x**2)
print("abs(x) =", abs(x))
print("sqrt(y) =", y.sqrt())
print("exp(y) =", y.exp())
print("log(y) =", y.log())
print("sin(y) =", y.sin())
print("cos(y) =", y.cos())
