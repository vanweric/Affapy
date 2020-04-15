"""Example 2"""
from AffApy.intervalArithmetic import Interval
from mpmath import mp

# Conversion
x = Interval(-mp.pi, mp.e)
print("x interval:", x)
a = x.toAffine()
print("x affine form:", a)
y = a.interval
print("x interval:", y)

i = Interval(1, 2)
aff = i.toAffine()
print("aff =", aff)
print("interval aff = ", aff.interval)
print("sqrt(aff) =", aff.sqrt())
print("interval sqrt(aff) =", aff.sqrt().interval)
print("inv(aff) =", aff.inv())
print("interval inv(aff) =", aff.inv().interval)
