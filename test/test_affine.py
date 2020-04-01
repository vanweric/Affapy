"""Defining test cases for Affine class"""

from AffApy.affineArithmetic import Affine
import unittest


class TestAffine(unittest.TestCase):
    """Test case used to test functions from class Affine"""

    def test_add_affine(self):
        """Test 'add' function from class Affine"""
        x = Affine(0, {1: 10})
        y = Affine(5, {1: 10, 2: 5})
        self.assertEqual(x + y, Affine(5, {1: 20, 2: 5}))
        self.assertEqual(x + x, Affine(0, {1: 20}))

    def test_sub_affine(self):
        """Test 'sub' function from class Affine"""
        x = Affine(0, {1: 10})
        y = Affine(5, {1: 10, 2: 5})
        self.assertEqual(x - x, Affine(0, {}))
        self.assertEqual(x - y, Affine(-5, {2: -5}))
        self.assertEqual(x + y - y, x)


if __name__ == "__main__":
    unittest.main()
