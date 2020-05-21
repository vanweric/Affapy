"""Example: Affine module"""
from AffApy.affineArithmetic import Affine

# Init
x = Affine(x0=1, xi={1: 2, 2: 3})
print("x =", x)
print("Interval:", x.interval)

y = Affine(interval=[4, 6])
print("y =", y)
print("Interval:", y.interval)

# Simple operations
print("x + x =", x + x)
z = x + y
print("z =", z)
print("Interval:", z.interval)
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

# Advanced operations with interval results
print("x / y =", (x / y).interval)
print("2 / y =", (2 / y).interval)
print("x**2 =", (x**2).interval)
print("abs(x) =", abs(x).interval)
print("sqrt(y) =", y.sqrt().interval)
print("exp(y) =", y.exp().interval)
print("log(y) =", y.log().interval)
print("sin(y) =", y.sin().interval)
print("cos(y) =", y.cos().interval)
print("sinh(y) =", y.sinh().interval)
print("cosh(y) =", y.cosh().interval)
