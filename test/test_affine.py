"""Defining test cases for Affine class"""

from AffApy.affineArithmetic import Affine
from mpmath import mpf
from math import sqrt, pi, sin, cos
import unittest

from AffApy.intervalArithmetic import Interval


class TestAffine(unittest.TestCase):
    """Test case used to test functions from class Affine"""

    def test_add_affine(self):
        """Test 'add' function from class Affine"""
        x = Affine(x0=0, xi={1: 10})
        y = Affine(x0=5, xi={1: 10, 2: 5})
        self.assertEqual(x + y, Affine(x0=5, xi={1: 20, 2: 5}))
        self.assertEqual(x + x, Affine(x0=0, xi={1: 20}))
        self.assertEqual(x + 4, Affine(x0=4, xi={1: 10}))
        self.assertEqual(x + 7.536 + y, Affine(x0=12.536, xi={1: 20, 2: 5}))

    def test_sub_affine(self):
        """Test 'sub' function from class Affine"""
        x = Affine(x0=0, xi={1: 10})
        y = Affine(x0=5, xi={1: 10, 2: 5})
        self.assertEqual(x - x, Affine(x0=0, xi={}))
        self.assertEqual(x - y, Affine(x0=-5, xi={2: -5}))
        self.assertEqual(x + y - y, x)
        self.assertEqual(x - 4, Affine(x0=-4, xi={1: 10}))
        self.assertEqual(x - 7.536 - y, Affine(x0=12.536, xi={2: -5}))

    def test_mult_affine(self):
        """Test 'mult' function from class Affine"""
        x = Affine(xi={1: 10}, x0=0)
        y = Affine(xi={1: 10, 2: 5}, x0=5)
        self.assertEqual(x * y, Affine(xi={1: 50, 3: 150}, x0=0))   #TODO: enlever clé de epsilon lorsque valeur vaut 0
        self.assertEqual(x * x, Affine(xi={2: 100}, x0=0))
        # TODO: pb car la conversion en intervalle donne [-100, 100] pour x²
        self.assertEqual(y * 4, Affine(xi={1: 40, 2: 20}, x0=20))
        self.assertEqual(y * 7.536, Affine(xi={1: 75.36, 2: 37.68}, x0=37.68))

    def test_contains_affine(self):
        """Test 'contains' function from class Affine"""
        x = Affine(xi={1: 10}, x0=0)
        y = Affine(xi={1: 10, 2: 5}, x0=5)
        z = Interval(-7, 5)
        self.assertTrue(x in y)
        self.assertTrue(0 in x)
        self.assertTrue(z in y)
        # self.assertFalse(y in z) TODO
        # self.assertFalse(x in 0) TODO

    def test_inv_affine(self):
        """Test 'inv' function from class Affine"""
        x = Affine(xi={1: 6}, x0=10)
        y = Affine(xi={1: -2, 2: 6}, x0=-20)
        self.assertTrue(Interval(1/16, 1/4) in x.inv())
        self.assertTrue(Interval(-1/28, -1/12) in y.inv())

    def test_truediv_affine(self):
        """Test 'truediv' function from class Affine"""
        x = Affine(xi={1: 6}, x0=10)
        y = Affine(xi={1: -2, 2: 6}, x0=-20)
        X = Interval(4, 16)
        Y = Interval(-28, -12)
        self.assertTrue(x / y == x * y.inv())
        self.assertTrue(X / Y in x / y)

    def test_neq_affine(self):
        """Test 'neq' function from class Affine"""
        x = Affine(xi={1: 6}, x0=10)
        y = Affine(xi={1: -2, 2: 6}, x0=-20)
        self.assertTrue(-x == Affine(xi={1: -6}, x0=-10))
        self.assertTrue(-y == Affine(xi={1: 2, 2: -6}, x0=20))
        self.assertTrue(x + (-x) == Affine({}, x0=0))
        self.assertTrue(x + (-y) == x - y)

    def test_eq_affine(self):
        """Test 'eq' function from class Affine"""
        x = Affine(xi={1: 10}, x0=0)
        y = Affine(xi={1: 10, 2: 5}, x0=5)
        z = Affine(xi={1: 4, 2: 6}, x0=0)
        X = Affine(xi={2: 10}, x0=0)
        print('voici x', x)
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

    def test_sqrt_affine(self):
        """Test 'sqrt' function from class Affine"""
        x = Affine(x0=5, xi={1: 5})
        y = Affine(x0=20, xi={2: 5, 5: 7})
        self.assertTrue(Interval(0, sqrt(10) in x.sqrt()))
        self.assertTrue(y.toInterval().sqrt() in y.sqrt())


if __name__ == "__main__":
    unittest.main()
