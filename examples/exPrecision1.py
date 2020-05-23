"""Use of precision module with *affapy*"""
from affapy.precision import precision
from affapy.ia import Interval
from affapy.aa import Affine
from mpmath import mp


print("== Interval ==")
with precision(dps=20):
    x = Interval(-mp.pi, mp.pi)
    print("x =", x)
    y = Interval(0, mp.e)
    print("y =", y)
    print("x + y =", x + y)
    print("x - y =", x - y)
    print("x * y =", x * y)
    print("exp(x) =", x.exp())

print("== Affine ==")
with precision(dps=30):
    x = Affine(interval=[-mp.pi, mp.pi])
    print("x =", x)
    y = Affine(interval=[0, mp.e])
    print("y =", y)
    print("x + y =", x + y)
    print("x - y =", x - y)
    print("x * y =", x * y)
    print("exp(x) =", x.exp())
    z = Affine(interval=[-mp.phi, mp.pi])
    print("z =", z)
    a = 2*x - y + 4*z
    print("2x - y + 4z =", a)
    print("Interval:", a.interval)
