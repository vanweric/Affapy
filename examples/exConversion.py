"""Conversion between IA and AA"""
from affapy.ia import Interval
from affapy.aa import Affine

# IA to AA
i = Interval(-1, 2)
print("i interval:", i)
a = i.convert()
print("i affine form:", a)
print("i interval:", a.interval)

# AA to IA
a = Affine([-1, 2])
print("a affine:", a)
i = a.convert()
print("a interval:", i)
