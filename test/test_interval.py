"""Defining test cases for Interval class"""
from AffApy.intervalArithmetic import Interval
import unittest
from math import sqrt, log, exp, pi, sin, cos, floor, ceil, trunc


class TestInterval(unittest.TestCase):
    """Test case used to test functions from class Interval"""

    def test_add_interval(self):
        """Test 'add' function from class Interval"""
        x = Interval(1, 2)
        y = Interval(3, 4)
        z = Interval(-1, 1)
        b1 = (x + y == Interval(4, 6))
        b2 = (x + 2 == Interval(3, 4))
        b3 = (x + y + z == Interval(3, 7))
        self.assertTrue(b1 and b2 and b3)

    def test_sub_interval(self):
        """Test 'sub' function from class Interval"""
        x = Interval(1, 2)
        y = Interval(3, 4)
        z = Interval(-1, 1)
        b1 = (x - y == Interval(-3, -1))
        b2 = (x - 2 == Interval(-1, 0))
        b3 = (x - y - z == Interval(-4, 0))
        b4 = (x - x == Interval(-1, 1))
        self.assertTrue(b1 and b2 and b3 and b4)

    def test_mul_interval(self):         # TODO: test interval * real, interval * 0
        """Test 'mul' function from class Interval"""
        x = Interval(1, 2)
        y = Interval(3, 4)
        z = Interval(-1, 1)
        b1 = (x * y == Interval(3, 8))
        b2 = (z * (x + y) == Interval(-6, 6))
        self.assertTrue(b1 and b2)

    def test_truediv_interval(self):         # TODO: test interval / interval contains 0
        """Test 'truediv' function from class Interval"""
        x = Interval(1, 2)
        y = Interval(3, 4)
        #z = Interval(-1, 1)
        b1 = (x / y == Interval(1/4, 2/3))
        #b2 = (x / z == None)
        self.assertTrue(b1)

    def test_pow_interval(self):
        """Test 'pow' function from class Interval"""
        x = Interval(-3, -1)
        y = Interval(3, 4)
        z = Interval(-1, 1)

        b1 = (y ** 2 == Interval(9, 16))
        b2 = (z ** 2 == Interval(0, 1))
        b3 = (x ** 2 == Interval(1, 9))
        b4 = (x ** 2 + y ** 2 - x * y == Interval(13, 37))
        self.assertTrue(b1 and b2 and b3 and b4)

    def test_neg_interval(self):
        """Test 'neg' function from class Interval"""
        x = Interval(-3, -1)
        y = Interval(3, 4)
        z = Interval(-1, 1)
        b1 = (-x == Interval(1, 3))
        b2 = (-y == Interval(-4, -3))
        b3 = (-z == Interval(-1, 1))
        self.assertTrue(b1 and b2 and b3)

    def test_abs_interval(self):
        """Test 'abs' function from class Interval"""
        x = Interval(-3, -1)
        y = Interval(3, 4)
        z = Interval(-1, 1)
        b1 = (abs(x) == Interval(1, 3))
        b2 = (abs(y) == Interval(3, 4))
        b3 = (abs(z) == Interval(0, 1))
        self.assertTrue(b1 and b2 and b3)

    def test_eq_interval(self):
        """Test 'eq' function from class Interval"""
        x = Interval(-3, -1)
        y = Interval(3, 4)
        self.assertTrue(x == Interval(-3, -1) and not(x == y))

    def test_neq_interval(self):
        """Test 'neq' function from class Interval"""
        x = Interval(-3, -1)
        y = Interval(3, 4)
        self.assertTrue(not(x != Interval(-3, -1)) and x != y and not(x != x))

    def test_ge_interval(self):
        """Test 'ge' function from class Interval"""
        x = Interval(-3, -1)
        y = Interval(3, 4)
        self.assertTrue(not(x >= 0.1) and x >= -3 and not(x >= -2) and y >= x)

    def test_gt_interval(self):
        """Test 'gt' function from class Interval"""
        x = Interval(-3, 1)
        y = Interval(1, 4)
        self.assertTrue(not(x > 0.2) and not(x > -3) and not (x > -2) and not(y > x))

    def test_le_interval(self):
        """Test 'le' function from class Interval"""
        x = Interval(-3, 1)
        y = Interval(3, 4)
        self.assertTrue(x <= 1 and x <= 2.3 and not(x <= 0) and not(x <= -4) and x <= y)

    def test_lt_interval(self):
        """Test 'lt' function from class Interval"""
        x = Interval(-3, 1)
        y = Interval(1, 4)
        self.assertTrue(not(x < 1) and x < 2 and not(x < 0) and not(x < -4) and not (x < y))

    def test_radius_interval(self):
        """Test 'radius' function from class Interval"""
        x = Interval(-3, 1)
        y = Interval(3.5, 6.7)
        self.assertTrue(x.radius() == 4, y.radius() == 3.2)

    def test_middle_interval(self):
        """Test 'middle' function from class Interval"""
        x = Interval(-3, 1)
        y = Interval(3, 4)
        b1 = (x.middle() == -1)
        b2 = (y.middle() == 3.5)
        self.assertTrue(b1 and b2)

    def test_log_interval(self):
        """Test 'log' function from class Interval"""
        x = Interval(3, 4)
        self.assertTrue((x.log() == Interval(log(3), log(4))))

    def test_exp_interval(self):
        """Test 'exp' function from class Interval"""
        x = Interval(-3, -1)
        y = Interval(-3, 1)
        z = Interval(1, 5)
        b1 = (x.exp() == Interval(exp(-3), exp(-1)))
        b2 = (y.exp() == Interval(exp(-3), exp(1)))
        b3 = (z.exp() == Interval(exp(1), exp(5)))
        self.assertTrue(b1 and b2 and b3)

    def test_sqrt_interval(self):
        """Test 'sqrt' function from class Interval"""
        x = Interval(0, 3)
        y = Interval(1, 10)
        b1 = (x.sqrt() == Interval(0, sqrt(3)))
        b2 = (y.sqrt() == Interval(sqrt(1), sqrt(10)))
        self.assertTrue((b1 and b2))

    def test_sin_interval(self):
        """test 'sin' function from class Interval"""
        x = Interval(0, pi/2)
        y = Interval(pi/3, pi)
        z = Interval(pi/4, 2*pi)
        x1 = Interval(pi, pi)
        y1 = Interval(4*pi/3, 2*pi + pi/3)
        z1 = Interval(3*pi/2, 2*pi + pi/2)
        b1 = (x.sin() == Interval(0, 1))
        b2 = (y.sin() == Interval(sin(pi), 1))
        b3 = (z.sin() == Interval(-1, 1))
        b4 = (x1.sin() == Interval(sin(pi), sin(pi)))
        b5 = (y1.sin() == Interval(-1, sin(2*pi + pi/3)))
        b6 = (z1.sin() == Interval(-1, 1))
        self.assertTrue(b1 and b2 and b3 and b4 and b5 and b6)

    def test_cos_interval(self):
        """Test 'cos' function from class Interval"""
        x = Interval(pi / 2, pi)
        y = Interval(pi / 3, 3 * pi / 2)
        z = Interval(pi / 4, 3 * pi)
        x1 = Interval(3 * pi / 2, 2 * pi)
        y1 = Interval(4 * pi / 3, 2 * pi + pi / 3)
        z1 = Interval(3 * pi / 2, 4 * pi)
        b1 = (x.cos() == Interval(-1, cos(pi/2)))
        b2 = (y.cos() == Interval(-1, cos(pi / 3)))
        b3 = (z.cos() == Interval(-1, 1))
        b4 = (x1.cos() == Interval(cos(3 * pi / 2), cos(2 * pi)))
        b5 = (y1.cos() == Interval(cos(4 * pi / 3), 1))
        b6 = (z1.cos() == Interval(-1, 1))
        self.assertTrue(b1 and b2 and b3 and b4 and b5 and b6)

    def test_contains_interval(self):
        """Test 'sin' function from class Interval"""
        x = Interval(1, 2)
        y = Interval(3, 4)
        z = Interval(-1, 1)
        x2 = Interval(-2, 3)
        y2 = Interval(1, 4)
        z2 = Interval(-2, 1)
        b1 = x in Interval(0, 4)
        b2 = x in Interval(2, 4)
        b3 = 0 in z
        b4 = 0 in y
        b5 = x2 * (y2 + z2) in x2 * y2 + x2 * z2
        self.assertTrue((b1 and not(b2) and b3 and not(b4) and b5))

    def test_round_interval(self):
        """Test 'round' function from class Interval"""
        b1 = (round(Interval(-pi, pi), 2) == Interval(-3.14, 3.14))
        b2 = (round(Interval(-pi, pi), 7) == Interval(-3.1415927, 3.1415927))
        b3 = (round(Interval(-pi, pi), 0) == Interval(-3, 3))
        self.assertTrue(b1 and b2 and b3)

    def test_trunc_interval(self):
        """Test 'trunc' function from class Interval"""
        b1 = (trunc(Interval(-pi, pi)) == Interval(-3, 3))
        b2 = (trunc(Interval(-1/3, 1/6)) == Interval(0, 0))
        self.assertTrue(b1 and b2)

    def test_floor_interval(self):
        """Test 'floor' function from class Interval"""
        b1 = (floor(Interval(-pi, pi)) == Interval(-4, 3))
        b2 = (floor(Interval(1/6, 1/3)) == Interval(0, 0))
        self.assertTrue(b1 and b2)

    def test_ceil_interval(self):
        """Test 'ceil' function from class Interval"""
        b1 = (ceil(Interval(-pi, pi)) == Interval(-3, 4))
        b2 = (ceil(Interval(1/6, 4/3)) == Interval(1, 2))
        self.assertTrue(b1 and b2)


if __name__ == "__main__":
    unittest.main()
