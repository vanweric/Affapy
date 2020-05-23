"""
**Example 1**: A simple example of using the lib
"""
from affapy.ia import Interval
from affapy.aa import Affine

u = Interval(-2, 2)
v = Interval(-1, 1)
x = Affine(interval=u)
r = Affine(interval=v)
s = Affine(interval=v)

temp1 = 10 + x + r
temp2 = 10 - x + s

z = (10 + x + r) * (10 - x + s)

print("x =", x)
print("r =", r)
print("s =", s)

print("10 + x + r =", temp1)
print("10 - x + r =", temp2)

print("(10 + x + r) * (10 - x + s) =", z)
print("Interval:", z.interval)
