"""définir des test unitaires"""
from intervalArithmetic import Interval
from affineArithmetic import Affine
import unittest
import numpy as np


class MyTest(unittest.TestCase):
    """Test case utilisé pour tester les fonctions de la classe Affine"""

    def test_add_interval(self):
        """Test le fonctionnement de la fonction 'add' de Interval"""
        x = Interval(1, 2)
        y = Interval(3, 4)
        z = Interval(-1, 1)
        b1 = (x + y == Interval(4, 6))
        b2 = (x + 2 == Interval(3, 4))
        b3 = (x + y + z == Interval(3, 7))
        self.assertTrue(b1 and b2 and b3)

    def test_sub_interval(self):
        """Test le fonctionnement de la fonction 'sub' de Interval"""
        x = Interval(1, 2)
        y = Interval(3, 4)
        z = Interval(-1, 1)
        b1 = (x - y == Interval(-3, -1))
        b2 = (x - 2 == Interval(-1, 0))
        b3 = (x - y - z == Interval(-4, 0))
        b4 = (x - x == Interval(-1, 1))
        self.assertTrue(b1 and b2 and b3 and b4)

    def test_mul_interval(self): #TODO: test interval * reel, interval * 0
        """Test le fonctionnement de la fonction 'mul' de Interval"""
        x = Interval(1, 2)
        y = Interval(3, 4)
        z = Interval(-1, 1)
        b1 = (x * y == Interval(3, 8))
        b2 = (z * (x + y) == Interval(-6, 6))
        self.assertTrue(b1 and b2)

    def test_truediv_interval(self): #TODO: test interval / interval contient 0
        """Test le fonctionnement de la fonction 'truediv' de Interval"""
        x = Interval(1, 2)
        y = Interval(3, 4)
        #z = Interval(-1, 1)
        b1 = (x / y == Interval(1/4, 2/3))
        #b2 = (x / z == None)
        self.assertTrue(b1)

    def test_pow_interval(self):
        """Test le fonctionnement de la fonction 'pow' de Interval"""
        x = Interval(-3, -1)
        y = Interval(3, 4)
        z = Interval(-1, 1)

        b1 = (y ** 2 == Interval(9, 16))
        b2 = (z ** 2 == Interval(0, 1))
        b3 = (x ** 2 == Interval(1, 9))
        b4 = (x ** 2 + y ** 2 - x * y == Interval(13, 37))
        self.assertTrue(b1 and b2 and b3 and b4)

    def test_neg_interval(self):
        """Test le fonctionnement de la fonction 'nef' de Interval"""
        x = Interval(-3, -1)
        y = Interval(3, 4)
        z = Interval(-1, 1)
        b1 = (-x == Interval(1, 3))
        b2 = (-y == Interval(-4, -3))
        b3 = (-z == Interval(-1, 1))
        self.assertTrue(b1 and b2 and b3)

    def test_abs_interval(self):
        """Test le fonctionnement de la fonction 'abs' de Interval"""
        x = Interval(-3, -1)
        y = Interval(3, 4)
        z = Interval(-1, 1)
        b1 = (abs(x) == Interval(1, 3))
        b2 = (abs(y) == Interval(3, 4))
        b3 = (abs(z) == Interval(0, 1))
        self.assertTrue(b1 and b2 and b3)

    def test_eq_interval(self):
        """Test le fonctionnement de la fonction 'eq' de Interval"""
        x = Interval(-3, -1)
        y = Interval(3, 4)
        self.assertTrue(x == Interval(-3, -1) and not(x == y))

    def test_neq_interval(self):
        """Test le fonctionnement de la fonction 'neq' de Interval"""
        x = Interval(-3, -1)
        y = Interval(3, 4)
        self.assertTrue(not(x != Interval(-3, -1)) and x != y and not(x != x))

    def test_ge_interval(self):
        """Test le fonctionnement de la fonction 'ge' de Interval"""
        x = Interval(-3, -1)
        y = Interval(3, 4)
        self.assertTrue(not(x >= 0.1) and x >= -3 and not(x >= -2) and y >= x)

    def test_gt_interval(self):
        """Test le fonctionnement de la fonction 'gt' de Interval"""
        x = Interval(-3, 1)
        y = Interval(1, 4)
        self.assertTrue(not(x > 0.2) and not(x > -3) and not (x > -2) and not(y > x))

    def test_le_interval(self):
        """Test le fonctionnement de la fonction 'le' de Interval"""
        x = Interval(-3, 1)
        y = Interval(3, 4)
        self.assertTrue(x <= 1 and x <= 2.3 and not(x <= 0) and not(x <= -4) and x <= y)

    def test_lt_interval(self):
        """Test le fonctionnement de la fonction 'lt' de Interval"""
        x = Interval(-3, 1)
        y = Interval(1, 4)
        self.assertTrue(not(x < 1) and x < 2 and not(x < 0) and not(x < -4) and not (x < y))

    def test_radius_interval(self):
        """Test le fonctionnement de la fonction 'radius' de Interval"""
        x = Interval(-3, 1)
        y = Interval(3.5, 6.7)
        self.assertTrue(x.radius() == 4, y.radius() == 3.2)

    def test_middle_interval(self):
        """Test le fonctionnement de la fonction 'middle' de Interval"""
        x = Interval(-3, 1)
        y = Interval(3, 4)
        b1 = (x.middle() == -1)
        b2 = (y.middle() == 3.5)
        self.assertTrue(b1 and b2)

    def test_log_interval(self):
        """Test le fonctionnement de la fonction 'log' de Interval"""
        x = Interval(3, 4)
        self.assertTrue((x.log() == Interval(np.log(3), np.log(4))))

    def test_exp_interval(self):
        """Test le fonctionnement de la fonction 'exp' de Interval"""
        x = Interval(-3, -1)
        y = Interval(-3, 1)
        z = Interval(1, 5)
        b1 = (x.exp() == Interval(np.exp(-3), np.exp(-1)))
        b2 = (y.exp() == Interval(np.exp(-3), np.exp(1)))
        b3 = (z.exp() == Interval(np.exp(1), np.exp(5)))
        self.assertTrue(b1 and b2 and b3)

    def test_sqrt_interval(self):
        """Test le fonctionnement de la fonction 'sqrt' de Interval"""
        x = Interval(0, 3)
        y = Interval(1, 10)
        b1 = (x.sqrt() == Interval(0, np.sqrt(3)))
        b2 = (y.sqrt() == Interval(np.sqrt(1), np.sqrt(10)))
        self.assertTrue((b1 and b2))







    #def test_add(self):
     #   """Test le fonctionnement de la fonction 'add'."""
      #  x = Affine([0, 10])
       # y = Affine([5, 5])
        #z = x + y
        #ze = Affine([5, 10, 5])
        #self.assertEqual(z, ze)

    #def test_sub(self):
     #   """Test le fonctionnement de la fonction 'sub'."""
      #  x = Affine([0, 10])
       # y = Affine([5, 5])
        #z = x - x
        #z1 = Affine([0, 0])
        #z2 = x - y
        #z3 = Affine([-5, 10, -5])
        #rep1 = z == z1  # rectifier le cas x-x=0
        #rep2 = z2 == z3
        #self.assertTrue(rep1 and rep2)


if __name__ == "__main__":
    unittest.main()
