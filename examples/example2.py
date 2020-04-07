"""Example 2"""
from AffApy.intervalArithmetic import Interval
from mpmath import mp

# Conversion
x = Interval(-mp.pi, mp.e)
print("x interval:", x)
a = x.toAffine()
print("x affine form:", a)
y = a.toInterval()
print("x interval:", y)

i = Interval(1, 2)
aff = i.toAffine()
print("aff =", aff)
print("sqrt(aff) =", aff.sqrt())
print("inv(aff) =", aff.inv())
