"""Defining test cases for Interval class"""

from AffApy.intervalArithmetic import Interval
from AffApy.affapyPrecision import precision
import unittest
from mpmath import sqrt, log, exp, pi, sin, cos, mpf, fdiv, mp, workdps
from math import ceil, floor


class TestInterval(unittest.TestCase):
    """Test case used to test functions from class Interval"""

    @precision(dec_precision=50)
    def test_add_interval(self):
        """Test 'add' function from class Interval"""
        x = Interval(1, 2)
        y = Interval(3, 4)
        z = Interval(-1, 1)
        self.assertEqual(x + y, Interval(4, 6))
        self.assertEqual(x + 2, Interval(3, 4))
        self.assertEqual(x + y + z, Interval(3, 7))

        x = Interval(mp.phi, mp.pi)
        y = Interval(mp.euler, mp.e)
        z = Interval(-mp.pi, mp.pi)
        self.assertTrue(Interval(mp.phi + mp.euler, mp.pi + mp.e) in x + y)
        self.assertTrue(Interval(mp.phi + 4, mp.pi + 4) in x + 4)
        self.assertTrue(Interval(mp.phi + mp.euler - mp.pi, mp.pi + mp.e + mp.pi) in x + y + z)

    @precision(dec_precision=50)
    def test_sub_interval(self):
        """Test 'sub' function from class Interval"""
        x = Interval(1, 2)
        y = Interval(3, 4)
        z = Interval(-1, 1)
        self.assertEqual(x - y, Interval(-3, -1))
        self.assertEqual(x - 2, Interval(-1, 0))
        self.assertEqual(x - y - z, Interval(-4, 0))
        self.assertEqual(x - x, Interval(-1, 1))

        x = Interval(mp.phi, mp.pi)
        y = Interval(mp.euler, mp.e)
        z = Interval(-mp.pi, mp.pi)
        self.assertTrue(Interval(mp.phi - mp.euler, mp.pi - mp.e) in x - y)
        self.assertTrue(Interval(mp.phi - 2, mp.pi - 2) in x - 2)
        self.assertTrue(Interval(mp.phi - mp.euler + mp.pi, mp.pi - mp.e - mp.pi) in x - y - z)
        self.assertTrue(Interval(0, 0) in x - x)

    @precision(dec_precision=50)
    def test_mul_interval(self):  # TODO: test interval * real, interval * 0
        """Test 'mul' function from class Interval"""
        x = Interval(1, 2)
        y = Interval(3, 4)
        z = Interval(-1, 1)
        self.assertEqual(x * y, Interval(3, 8))
        self.assertEqual(z * (x + y), Interval(-6, 6))

        x = Interval(mp.phi, mp.pi)
        y = Interval(mp.euler, mp.e)
        z = Interval(-mp.pi, mp.pi)
        self.assertTrue(Interval(mp.phi * mp.euler, mp.pi * mp.e) in x * y)
        self.assertTrue(Interval(- mp.pi * mp.phi + mp.euler, mp.pi * mp.pi + mp.e) in z * (x + y))

    @precision(dec_precision=50)
    def test_truediv_interval(self):  # TODO: test interval/interval contains 0
        """Test 'truediv' function from class Interval"""
        x = Interval(1, 2)
        y = Interval(3, 4)
        z = Interval(-5, -1)
        self.assertEqual(x / y, Interval(fdiv(1, 4, rounding='d'),
                                         fdiv(2, 3, rounding='u')))
        self.assertTrue(Interval(-2, -1 / 5) in x / z)

        x = Interval(mp.phi, mp.pi)
        y = Interval(mp.euler, mp.e)
        z = Interval(-mp.e, -mp.euler)
        self.assertTrue(Interval(mp.phi / mp.e, mp.pi / mp.euler) in x / y)
        self.assertTrue(x / z in Interval(- mp.pi / mp.euler, -mp.phi / mp.e))

    @precision(dec_precision=50)
    def test_pow_interval(self):
        """Test 'pow' function from class Interval"""
        x = Interval(-3, -1)
        y = Interval(3, 4)
        z = Interval(-1, 1)

        self.assertEqual(y ** 2, Interval(9, 16))
        with workdps(2):
            self.assertTrue(Interval(27, 64) in y ** 3)
            self.assertEqual(z ** 2, Interval(0, 1))
            self.assertTrue(x ** 2 in Interval(1, 9))
            self.assertTrue(Interval(13, 37) in x ** 2 + y ** 2 - x * y)

    def test_neg_interval(self):
        """Test 'neg' function from class Interval"""
        x = Interval(-3, -1)
        y = Interval(3, 4)
        z = Interval(-1, 1)
        self.assertEqual(-x, Interval(1, 3))
        self.assertEqual(-y, Interval(-4, -3))
        self.assertEqual(-z, Interval(-1, 1))

    def test_abs_interval(self):
        """Test 'abs' function from class Interval"""
        x = Interval(-3, -1)
        y = Interval(3, 4)
        z = Interval(-1, 1)
        self.assertEqual(abs(x), Interval(1, 3))
        self.assertEqual(abs(y), Interval(3, 4))
        self.assertEqual(abs(z), Interval(0, 1))

    def test_eq_interval(self):
        """Test 'eq' function from class Interval"""
        x = Interval(-3, -1)
        y = Interval(3, 4)
        self.assertTrue(x == Interval(-3, -1))
        self.assertTrue(not (x == y))

    def test_neq_interval(self):
        """Test 'neq' function from class Interval"""
        x = Interval(-3, -1)
        y = Interval(3, 4)
        self.assertTrue(not (x != Interval(-3, -1)))
        self.assertTrue(x != y)
        self.assertTrue(not (x != x))

    def test_ge_interval(self):
        """Test 'ge' function from class Interval"""
        x = Interval(-3, -1)
        y = Interval(3, 4)
        self.assertTrue(not (x >= 0.1))
        self.assertTrue(x >= -3)
        self.assertTrue(not (x >= -2))
        self.assertTrue(y >= x)

    def test_gt_interval(self):
        """Test 'gt' function from class Interval"""
        x = Interval(-3, 1)
        y = Interval(1, 4)
        self.assertTrue(not (x > 0.2))
        self.assertTrue(not (x > -3))
        self.assertTrue(not (x > -2))
        self.assertTrue(not (y > x))

    def test_le_interval(self):
        """Test 'le' function from class Interval"""
        x = Interval(-3, 1)
        y = Interval(3, 4)
        self.assertTrue(x <= 1)
        self.assertTrue(x <= 2.3)
        self.assertTrue(not (x <= 0))
        self.assertTrue(not (x <= -4))
        self.assertTrue(x <= y)

    def test_lt_interval(self):
        """Test 'lt' function from class Interval"""
        x = Interval(-3, 1)
        y = Interval(1, 4)
        self.assertTrue(not (x < 1))
        self.assertTrue(x < 2)
        self.assertTrue(not (x < 0))
        self.assertTrue(not (x < -4))
        self.assertTrue(not (x < y))

    def test_radius_interval(self):
        """Test 'radius' function from class Interval"""
        x = Interval(-3, 1)
        y = Interval(3.5, 6.7)
        self.assertEqual(x.radius(), 4)
        self.assertEqual(y.radius(), 3.2)

    def test_middle_interval(self):
        """Test 'middle' function from class Interval"""
        x = Interval(-3, 1)
        y = Interval(3, 4)
        self.assertEqual(x.middle(), -1)
        self.assertEqual(y.middle(), 3.5)

    @precision(dec_precision=50)
    def test_log_interval(self):
        """Test 'log' function from class Interval"""
        x = Interval(3, 4)
        self.assertEqual(x.log(), Interval(log(3), log(4)))

        x = Interval(mp.phi, mp.pi)
        self.assertTrue(Interval(log(mp.phi), log(mp.pi)) in x.log())

    @precision(dec_precision=50)
    def test_exp_interval(self):
        """Test 'exp' function from class Interval"""
        x = Interval(-3, -1)
        y = Interval(-3, 1)
        z = Interval(1, 5)
        self.assertEqual(x.exp(), Interval(exp(-3, rounding='d'),
                                           exp(-1, rounding='u')))
        self.assertEqual(y.exp(), Interval(exp(-3, rounding='d'),
                                           exp(1, rounding='u')))
        self.assertEqual(z.exp(), Interval(exp(1, rounding='d'),
                                           exp(5, rounding='u')))

        x = Interval(-mp.pi, -mp.euler)
        y = Interval(-mp.pi, mp.euler)
        z = Interval(mp.euler, mp.pi)
        self.assertTrue(Interval(exp(-mp.pi), exp(-mp.euler)) in x.exp())
        self.assertTrue(Interval(exp(-mp.pi), exp(mp.euler)) in y.exp())
        self.assertTrue(Interval(exp(mp.euler), exp(mp.pi)) in z.exp())

    @precision(dec_precision=50)
    def test_sqrt_interval(self):
        """Test 'sqrt' function from class Interval"""
        x = Interval(0, 3)
        y = Interval(1, 10)
        self.assertEqual(x.sqrt(), Interval(0, mpf(sqrt(3, rounding='u'))))
        self.assertTrue(Interval(mpf(sqrt(1)), mpf(sqrt(10))) in y.sqrt())

        x = Interval(0, mp.pi)
        y = Interval(mp.phi, 3*mp.pi)
        self.assertTrue(Interval(0, sqrt(mp.pi)) in x.sqrt())
        self.assertTrue(Interval(sqrt(mp.phi), sqrt(3*mp.pi)) in y.sqrt())


    @precision(dec_precision=50)
    def test_sin_interval(self):
        """test 'sin' function from class Interval"""
        x = Interval(0, pi / 2)
        y = Interval(pi / 3, pi)
        z = Interval(pi / 4, 2 * pi)
        x1 = Interval(pi, pi)
        y1 = Interval(4 * pi / 3, 2 * pi + pi / 3)
        z1 = Interval(3 * pi / 2, 2 * pi + pi / 2)
        self.assertTrue(x.sin() in Interval(cos(0 + mp.pi / 2), sin(pi / 2)))
        self.assertEqual(y.sin(), (-y + float(mp.pi / 2)).cos())
        self.assertTrue(z.sin() in Interval(-1, 1))
        self.assertEqual(x1.sin(), (-x1 + float(mp.pi / 2)).cos())
        self.assertTrue(Interval(-1, sin(pi/3)) in y1.sin())
        self.assertTrue(z1.sin() in Interval(-1, 1))

    @precision(dec_precision=50)
    def test_cos_interval(self):
        """Test 'cos' function from class Interval"""
        x = Interval(pi / 2, pi)
        y = Interval(pi / 3, 3 * pi / 2)
        z = Interval(pi / 4, 3 * pi)
        x1 = Interval(3 * pi / 2, 2 * pi)
        y1 = Interval(4 * pi / 3, 2 * pi + pi / 3)
        z1 = Interval(3 * pi / 2, 4 * pi)
        self.assertTrue(x.cos() in Interval(cos(pi),cos(pi / 2)))
        self.assertTrue(Interval(-1, cos(pi / 3)) in y.cos())
        self.assertEqual(z.cos(), Interval(-1, 1))
        self.assertEqual(x1.cos(), Interval(cos(3 * pi / 2), cos(2 * pi)))
        self.assertEqual(y1.cos(), Interval(cos(4 * pi / 3, rounding='d'), 1))
        self.assertEqual(z1.cos(), Interval(-1, 1))

    def test_contains_interval(self):
        """Test 'sin' function from class Interval"""
        x = Interval(1, 2)
        y = Interval(3, 4)
        z = Interval(-1, 1)
        x2 = Interval(-2, 3)
        y2 = Interval(1, 4)
        z2 = Interval(-2, 1)
        self.assertTrue(x in Interval(0, 4))
        self.assertFalse(x in Interval(2, 4))
        self.assertTrue(0 in z)
        self.assertFalse(0 in y)
        self.assertTrue(x2 * (y2 + z2) in x2 * y2 + x2 * z2)

    def test_floor_interval(self):
        """Test 'floor' function from class Interval"""
        self.assertEqual(floor(Interval(-pi, pi)), Interval(-4, 3))
        self.assertEqual(floor(Interval(1 / 6, 1 / 3)), Interval(0, 0))

    def test_ceil_interval(self):
        """Test 'ceil' function from class Interval"""
        self.assertEqual(ceil(Interval(-pi, pi)), Interval(-3, 4))
        self.assertEqual(ceil(Interval(1 / 6, 4 / 3)), Interval(1, 2))

    def test_mintrigo_interval(self):
        """Test 'minTrigo' function from class Interval"""
        self.assertEqual(Interval(5 * pi, 6 * pi).minTrigo(), Interval(pi, 2 * pi))
        self.assertTrue(Interval(-pi, 2 * pi).minTrigo() in Interval(-pi, pi))
        self.assertEqual(Interval(0, 3 * pi).minTrigo(), Interval(0, 2 * pi))
        self.assertEqual(Interval(-2 * pi, 2 * pi).minTrigo(), Interval(0, 2 * pi))


if __name__ == "__main__":
    unittest.main()
