from affineArithmetic import Affine
import unittest


class MyTest(unittest.TestCase):
    """Test case utilisé pour tester les fonctions de la classe Affine"""

    def test_add(self):
        """Test le fonctionnement de la fonction 'add'."""
        x = Affine({0: 0, 1: 10})
        y = Affine({0: 5, 1: 10, 2: 5})
        z = x + y
        ze = Affine({0: 5, 3: 20, 2: 5})
        self.assertEqual(z, ze)

    def test_sub(self):
        """Test le fonctionnement de la fonction 'sub'."""
        x = Affine({0: 0, 1: 10})
        y = Affine({0: 5, 1: 10, 2: 5})
        rep1 = x - x == Affine({0: 0})
        rep2 = x - y == Affine({0: -5, 2: -5})
        self.assertTrue(rep1 and rep2)


if __name__ == "__main__":
    unittest.main()
