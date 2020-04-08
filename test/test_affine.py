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
        x = Affine(0, {1: 10})
        y = Affine(5, {1: 10, 2: 5})
        self.assertEqual(x + y, Affine(5, {1: 20, 2: 5}))
        self.assertEqual(x + x, Affine(0, {1: 20}))
        self.assertEqual(x + 4, Affine(4, {1: 10}))
        self.assertEqual(x + 7.536 + y, Affine("12.536", {1: 20, 2: 5}))

    def test_sub_affine(self):
        """Test 'sub' function from class Affine"""
        x = Affine(0, {1: 10})
        y = Affine(5, {1: 10, 2: 5})
        self.assertEqual(x - x, Affine(0, {}))
        self.assertEqual(x - y, Affine(-5, {2: -5}))
        self.assertEqual(x + y - y, x)
        self.assertEqual(x - 4, Affine(-4, {1: 10}))
        self.assertEqual(x - 7.536 - y, Affine("-12.536", {2: -5}))

    def test_mult_affine(self):
        """Test 'mult' function from class Affine"""
        x = Affine(0, {1: 10})
        y = Affine(5, {1: 10, 2: 5})
        self.assertEqual(x * y, Affine(0, {1: 50, 2: 0, 3: 150}))   #TODO: enlever clé de epsilon lorsque valeur vaut 0
        self.assertEqual(x * x, Affine(0, {1: 0, 2: 100}))
        # TODO: pb car la conversion en intervalle donne [-100, 100] pour x²
        self.assertEqual(y * 4, Affine(20, {1: 40, 2: 20}))
        self.assertEqual(y * 7.536, Affine("37.68", {1: 75.36, 2: 37.68}))

    def test_contains_affine(self):
        """Test 'contains' function from class Affine"""
        x = Affine(0, {1: 10})
        y = Affine(5, {1: 10, 2: 5})
        z = Interval(-7, 5)
        self.assertTrue(x in y)
        self.assertTrue(0 in x)
        self.assertTrue(z in x)

    def test_inv_affine(self):
        """Test 'inv' function from class Affine"""
        x = Affine(10, {1: 6})
        y = Affine(-20, {1: -2, 2: 6})
        self.assertTrue(Interval(1/16, 1/4) in x.inv())
        self.assertTrue(Interval(-1/28, -1/12) in y.inv())

    def test_truediv_affine(self):
        """Test 'truediv' function from class Affine"""
        x = Affine(10, {1: 6})
        y = Affine(-20, {1: -2, 2: 6})
        X = Interval(4, 16)
        Y = Interval(-28, -12)
        self.assertTrue(x / y == x * y.inv())
        self.assertTrue(X / Y in x / y)

    def test_neq_affine(self):
        """Test 'neq' function from class Affine"""
        x = Affine(10, {1: 6})
        y = Affine(-20, {1: -2, 2: 6})
        self.assertTrue(-x == Affine(-10, {1: -6}))
        self.assertTrue(-y == Affine(20, {1: 2, 2: -6}))
        self.assertTrue(x + (-x) == Affine(0, {}))

    def test_eq_affine(self):
        """Test 'eq' function from class Affine"""
        x = Affine(0, {1: 10})
        y = Affine(5, {1: 10, 2: 5})
        z = Affine(0, {1: 4, 2: 6})
        X = Affine(0, {2: 10})
        self.assertFalse(x == y)
        self.assertFalse(x == z)
        self.assertFalse(x == X)

    def test_ne_affine(self):
        """Test 'ne' function from class Affine"""
        x = Affine(0, {1: 10})
        y = Affine(5, {1: 10, 2: 5})
        z = Affine(0, {1: 4, 2: 6})
        X = Affine(0, {2: 10})
        self.assertTrue(x != y)
        self.assertTrue(x != z)
        self.assertTrue(x != X)

    def test_sqrt_affine(self):
        """Test 'sqrt' function from class Affine"""
        x = Affine(5, {1: 5})
        y = Affine(20, {2: 5, 5: 7})
        self.assertTrue(Interval(0, sqrt(10) in x.sqrt()))
        self.assertTrue(y.toInterval().sqrt() in y.sqrt())






if __name__ == "__main__":
    unittest.main()
