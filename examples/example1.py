"""Example 1"""
from AffApy.affineArithmetic import Affine
from AffApy.affapyPrecision import precision
from mpmath import mp


@precision(dec_prec=5)
def functionTest():
    print("This is a test function for the precision module.")
    print("Here the decimal precision is %i and the binary one is %i".format(precision.getActualDecPrecision(),
                                                                             precision.getActualBinPrecision()))


# Precision
mp.dps = 10
print("Decimal places:", mp.dps)
print("Binary precision:", mp.prec)

functionTest()
with precision(dec_prec=10):
    functionTest()

x = Affine(x0=mp.pi, xi={1: mp.e})
# print(x.__repr__())
print("x =", x)
print("x + x =", x + x)
y = Affine(x0=2, xi={1: 3, 2: 4})
print("y =", y)
z = x + y
print("z =", z)
# print(z.__repr__())
print("x - 1 =", x - 1)
print("x + 1 =", x + 1)
print("x - x =", x - x)
print("y - y =", y - y)
print("x - y =", x - y)
print("y * 2 = ", y * 2)
print("x * y =", x * y)
print("x + x - x - x =", x + x - x - x)
print("-x =", -x)
print("-x + x =", -x + x)

x = Affine(interval=[-mp.pi, mp.pi])
print(x)
print(x.interval)
y = Affine(interval=[-1, 1])
print(y)
print(y.interval)
