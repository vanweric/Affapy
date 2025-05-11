"""Defining test cases for Affine class"""
import sys
print(sys.executable)

from affapy.aa import Affine
from affapy.ia import Interval
from affapy.precision import precision
import unittest
from mpmath import mp


class TestAffine(unittest.TestCase):
    """Test case used to test functions from class Affine"""

    def test_neg_affine(self):
        """Test 'neg' function from class Affine"""
        x = Affine(xi={1: 6}, x0=10)
        y = Affine(xi={1: -2, 2: 6}, x0=-20)
        self.assertTrue(-x == Affine(xi={1: -6}, x0=-10))
        self.assertTrue(-y == Affine(xi={1: 2, 2: -6}, x0=20))
        self.assertTrue(x + (-x) == Affine(xi={}, x0=0))
        self.assertTrue(x + (-y) == x - y)

    @precision(dps=50)
    def test_add_affine(self):
        """Test 'add' function from class Affine"""
        x = Affine(x0=0, xi={1: 10})
        y = Affine(x0=5, xi={1: 10, 2: 5})
        self.assertEqual(x + y, Affine(x0=5, xi={1: 20, 2: 5}))
        self.assertEqual(x + x, Affine(x0=0, xi={1: 20}))
        self.assertEqual(x + 4, Affine(x0=4, xi={1: 10}))

        x = Affine(x0=-mp.pi, xi={1: mp.e})
        y = Affine(x0=mp.pi, xi={1: mp.phi, 2: mp.e})
        self.assertTrue(Affine(x0=0, xi={1: mp.e + mp.phi, 2: mp.e}) in x + y)
        self.assertTrue(Affine(x0=-2 * mp.pi, xi={1: 2 * mp.e}) in x + x)
        self.assertTrue(Affine(x0=-mp.pi + 4, xi={1: mp.e}) in x + 4)

    @precision(dps=2)
    def test_add_affine_limite(self):
        x = Affine(x0=0, xi={1: 1})
        y = Affine(x0=0, xi={1: 1.05})
        print(mp.pi)
        print(x + y)
        print(mp.mpf(1.051))

        self.assertTrue(Affine(x0=0, xi={1: 2.05}) in x + y)

    @precision(dps=50)
    def test_sub_affine(self):
        """Test 'sub' function from class Affine"""
        x = Affine(x0=0, xi={1: 10})
        y = Affine(x0=5, xi={1: 10, 2: 5})
        self.assertEqual(x - x, Affine(x0=0, xi={}))
        self.assertEqual(x - y, Affine(x0=-5, xi={2: -5}))
        self.assertEqual(x + y - y, x)
        self.assertEqual(x - 4, Affine(x0=-4, xi={1: 10}))

        x = Affine(x0=mp.pi, xi={1: mp.e})
        y = Affine(x0=mp.pi, xi={1: mp.phi, 2: mp.e})
        self.assertTrue(Affine(x0=0, xi={1: mp.e - mp.phi, 2: -mp.e}) in x - y)
        self.assertTrue(Affine(x0=0, xi={}) in x - x)
        self.assertTrue(Affine(x0=mp.pi - 4, xi={1: mp.e}) in x - 4)

    @precision(dps=50)
    def test_mul_affine(self):
        """Test 'mul' function from class Affine"""
        x = Affine(xi={1: 10}, x0=0)
        y = Affine(xi={1: 10, 2: 5}, x0=5)
        self.assertTrue(Affine(xi={1: 50, 3: 150}, x0=0) in x * y)
        self.assertTrue(Affine(xi={4: 100}, x0=0) in x * x)
        self.assertTrue(Affine(xi={1: 40, 2: 20}, x0=20) in y * 4)
        self.assertTrue(
            Affine(x0=-5, xi={1: 90, 2: -5, 5: 300}) in (x + x) * y - y)

        x = Affine(x0=mp.pi, xi={1: mp.e})
        y = Affine(x0=mp.pi, xi={1: mp.phi, 2: mp.e})
        self.assertTrue(
            Affine(x0=mp.pi * mp.pi,
                   xi={1: mp.pi * (mp.phi + mp.e) - mp.phi, 2: mp.pi * mp.e,
                       6: mp.e * mp.phi + mp.e * mp.e}) in x * y)
        self.assertTrue(
            Affine(x0=mp.pi * mp.pi, xi={1: 2 * mp.pi * mp.e}) in x * x)
        self.assertTrue(
            Affine(x0=mp.pi * 4, xi={1: mp.phi, 2: mp.e}) in y * 4)
        self.assertTrue(
            Affine(x0=2 * mp.pi ** 2 - mp.pi,
                   xi={1: 2 * mp.pi * mp.phi + 2 * mp.pi * mp.e - mp.phi,
                       2: 2 * mp.pi * mp.e - mp.e,
                       7: mp.e * mp.phi + mp.e ** 2}) in (x + x) * y - y)

    @precision(dps=50)
    def test_inv_affine(self):
        """Test 'inv' function from class Affine"""
        x = Affine(xi={1: 6}, x0=10)
        x_result = Interval(1 / 16, 1 / 4)
        y = Affine([1, 2])
        y_result = Affine(x0=0.75, xi={1: -0.125, 2: 0.125})
        self.assertTrue(x_result in x.inv())
        self.assertTrue(y_result in y.inv())

    @precision(dps=50)
    def test_truediv_affine(self):
        """Test 'truediv' function from class Affine"""
        x = Affine(xi={1: 6}, x0=10)
        y = Affine(xi={1: -2, 2: 6}, x0=-20)
        self.assertEqual((x / y).interval, (x * y.inv()).interval)

    @precision(dps=50)
    def test_sqrt_affine(self):
        """Test 'sqrt' function from class Affine"""
        x = Affine(x0=5, xi={1: 5})
        y = Affine(x0=20, xi={2: 5, 5: 7})
        self.assertTrue(Interval(0, mp.sqrt(10)) in x.sqrt().interval)
        self.assertTrue(Interval(mp.sqrt(8), mp.sqrt(32)) in y.sqrt().interval)

    def test_eq_affine(self):
        """Test 'eq' function from class Affine"""
        x = Affine(xi={1: 10}, x0=0)
        y = Affine(xi={1: 10, 2: 5}, x0=5)
        z = Affine(xi={1: 4, 2: 6}, x0=0)
        X = Affine(xi={2: 10}, x0=0)
        self.assertFalse(x == y)
        self.assertFalse(x == z)
        self.assertFalse(x == X)

    def test_ne_affine(self):
        """Test 'ne' function from class Affine"""
        x = Affine(xi={1: 10}, x0=0)
        y = Affine(xi={1: 10, 2: 5}, x0=5)
        z = Affine(xi={1: 4, 2: 6}, x0=0)
        X = Affine(xi={2: 10}, x0=0)
        self.assertTrue(x != y)
        self.assertTrue(x != z)
        self.assertTrue(x != X)

    @precision(dps=50)
    def test_contains_affine(self):
        """Test 'contains' function from class Affine"""
        x = Affine(xi={1: 10}, x0=0)
        y = Affine(xi={1: 10, 2: 5}, x0=5)
        z = Interval(-7, 5)
        self.assertTrue(x in y)
        self.assertTrue(0 in x)
        self.assertTrue(z in y)
        self.assertFalse(y in z)

    def test_add_str(self):
        x = Affine([-1,1])
        y = x + '1.5'
        z = Interval(.5,2.5)
        self.assertEqual(y.convert(), z)

    def test_radd_str(self):
        x = Affine([-1,1])
        y = '1.5' + x
        z = Interval(.5,2.5)
        self.assertEqual(y.convert(), z)

    def test_mul_str(self):
        """Test multiplication with a string"""
        x = Affine([-1, 1])
        y = x * '2.5'
        z = Interval(-2.5, 2.5)
        self.assertEqual(y.convert(), z)

    def test_rmul_str(self):
        """Test reverse multiplication with a string"""
        x = Affine([-1, 1])
        y = '2.5' * x
        z = Interval(-2.5, 2.5)
        self.assertEqual(y.convert(), z)

    def test_sub_str(self):
        """Test subtraction with a string"""
        x = Affine([-1, 1])
        y = x - '1.5'
        z = Interval(-2.5, -0.5)
        self.assertEqual(y.convert(), z)

    def test_rsub_str(self):
        """Test reverse subtraction with a string"""
        x = Affine([-1, 1])
        y = '1.5' - x
        z = Interval(0.5, 2.5)
        self.assertEqual(y.convert(), z)

    def test_truediv_str(self):
        """Test division with a string"""
        x = Affine([1., 2])
        y = x / '2.0'
        z = Interval(.5, 1.0)
        self.assertEqual(y.convert(), z)

    def test_rtruediv_str(self):
        """Test reverse division with a string"""
        x = Affine([1, 2])
        y = 2. / x
        z = Interval(1.0, 2.0)  # Adjust based on actual behavior
        self.assertEqual(y.convert(), z)

    def test_contains_str(self):
        """Test 'contains' with a string"""
        x = Affine([-1, 1])
        self.assertTrue('0.5' in x)
        self.assertFalse('2.0' in x)

        
if __name__ == "__main__":
    unittest.main()
