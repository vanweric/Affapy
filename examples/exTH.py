from AffApy.affineArithmetic import Affine

f0, f1, f2, f3, f4 = (Affine(interval=[0, 255]) for _ in range(5))
x = Affine(interval=[0, 1])
y = Affine(interval=[0, 1])

# coefficients
c3 = 3 * (f2-f3) + f4-f1
c2 = 2*f1 - 5*f2 + 4*f3 - f4
c1 = f3 - f1
c0 = f2

# interpolation 1D
interX = ((c3 * x + c2) * x + c1) * x + c0

# 2D
g0, g1, g2, g3, g4 = (Affine(interval=interX.interval) for _ in range(5))

d3 = 3 * (g2-g3) + g4 - g1
d2 = 2*g1 - 5*g2 + 4*g3 - g4
d1 = g3 - g1
d0 = g2

interY = ((d3 * y + d2) * y + d1) * y + d0

# output
print(interX.interval)
print(interY.interval)
