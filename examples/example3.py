"""Example 3: underflow demonstration"""
from AffApy.affineArithmetic import Affine

eps = 1e-10

a = Affine(interval=[77617-eps, 77617+eps])
b = Affine(interval=[33096-eps, 33096+eps])

result = (333.75*b**6 + a*a*(11*a*a*b*b - b**6 - 121*b**4 - 2)
          + 5.5*b**8 + a/(2*b))
print("result =", result)

print(
    f"""
    Although the input values ({a.x0}, {b.x0})
    only had an uncertainty of {eps}, the output interval is:
    {result.interval}".
    The correct value is actually about -0.82740.""")
