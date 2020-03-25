"""Defining test cases for Affine class"""
import sys
sys.path.insert(0, '../AffApy')
from affineArithmetic import Affine
import unittest


class TestAffine(unittest.TestCase):
    """Test case used to test functions from class Affine"""

    def test_add_affine(self):
        """Test 'add' function from class Affine"""
        x = Affine({0: 0, 1: 10})
        y = Affine({0: 5, 1: 10, 2: 5})
        b1 = x + y == Affine({0: 5, 3: 20, 2: 5})
        b2 = x + x == Affine({0: 0, 4: 20})
        self.assertTrue(b1 and b2)

    def test_sub_affine(self):
        """Test 'sub' function from class Affine"""
        x = Affine({0: 0, 1: 10})
        y = Affine({0: 5, 1: 10, 2: 5})
        rep1 = x - x == Affine({0: 0})
        rep2 = x - y == Affine({0: -5, 2: -5})
        self.assertTrue(rep1 and rep2)


if __name__ == "__main__":
    unittest.main()
