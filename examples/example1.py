"""Example 1"""
from AffApy.affineArithmetic import Affine
from mpmath import mp

# Precision
mp.dps = 10
print("Decimal places:", mp.dps)
print("Binary precision:", mp.prec)

x = Affine(mp.pi, {1: mp.e})
# print(x.__repr__())
print("x =", x)
print("x + x =", x + x)
y = Affine(2, {1: 3, 2: 4})
print("y =", y)
z = x + y
print("z =", z)
# print(z.__repr__())
print("x - 1 =", x - 1)
print("x + 1 =", x + 1)
print("x - x =", x - x)
print("y - y =", y - y)
print("x - y =", x - y)
print("y * 2 = ", y*2)
print("x * y =", x*y)
print("x + x - x - x =", x + x - x - x)
print("-x + x =", -x + x)
print("Interval x :", x.toInterval())

# Init with list
a = Affine(mp.pi, [3, 5, 2])
print("a =", a)
