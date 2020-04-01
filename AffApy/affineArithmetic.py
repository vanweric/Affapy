"""Affine Arithmetic module"""
from AffApy.intervalArithmetic import Interval
from AffApy.affapyError import AffApyError
from math import pi


class Affine:
    """Representation of an affine form"""
    def __init__(self, x0, xi):
        self._x0 = x0           # x0 : centre
        self._xi = xi.copy()    # xi : dictionnaire

    # Getter
    @property
    def x0(self):
        """Return x0"""
        return self._x0

    @property
    def xi(self):
        """Return xi"""
        return self._xi

    # Setter
    @x0.setter
    def x0(self, value):
        """Set x0"""
        self._x0 = value

    @xi.setter
    def xi(self, value):
        """Set xi"""
        self._xi = value

    def rad(self):
        """
        Return the radius of affine form
        :rtype: int or float
        """
        return sum(abs(self.xi[i]) for i in self.xi)

    # Binary operators
    def __add__(self, other):
        """
        Operator +
        :type other: Affine or int or float
        :rtype: Affine
        """
        if isinstance(other, self.__class__):
            x0 = self.x0 + other.x0
            xi = {}
            for i in self.xi:
                if i in other.xi:
                    val = self.xi[i] + other.xi[i]
                    if val != 0:
                        xi[i] = val
                else:
                    xi[i] = self.xi[i]
            for i in other.xi:
                if i not in self.xi:
                    xi[i] = other.xi[i]
            return Affine(x0, xi)
        if isinstance(other, int) or isinstance(other, float):
            x0 = self.x0 + other
            xi = self.xi.copy()
            return Affine(x0, xi)
        raise AffApyError("type error")

    def __sub__(self, other):
        """
        Operator -
        :type other: Affine or int or float
        :rtype: Affine
        """
        if isinstance(other, self.__class__):
            x0 = self.x0 - other.x0
            xi = {}
            for i in self.xi:
                if i in other.xi:
                    val = self.xi[i] - other.xi[i]
                    if val != 0:
                        xi[i] = val
                else:
                    xi[i] = self.xi[i]
            for i in other.xi:
                if i not in self.xi:
                    xi[i] = other.xi[i]
            return Affine(x0, xi)
        if isinstance(other, int) or isinstance(other, float):
            x0 = self.x0 - other
            xi = self.xi.copy()
            return Affine(x0, xi)
        raise AffApyError("type error")

    def __mul__(self, other):
        """
        Operator *
        :type other: Affine
        :rtype: Affine
        """
        # if isinstance(other, self.__class__):
        #     xi = {0: self.xi[0] * other.xi[0]}
        #     for x in self.keyXi:
        #         for y in other.keyXi:
        #             if self.xi[x] * other.xi[y] != 0:
        #                 xi[Affine._COUNT] = self.xi[x] * other.xi[y]
        #                 Affine._COUNT += 1
        #     return Affine(xi)
        if isinstance(other, int) or isinstance(other, float):
            x0 = other*self.x0
            xi = {i: other*self.xi[i] for i in self.xi}
            return Affine(x0, xi)
        raise AffApyError("type error")

    def __truediv__(self, other):
        """
        Operator /
        :type other: Affine
        :rtype: Affine
        """
        pass

    def __pow__(self, n):
        """
        Operator **
        :type other: int or float
        :rtype: Affine
        """
        pass

    # Unary operator
    def __neg__(self):
        """
        Operator - (unary)
        :rtype: Affine
        """
        x0 = -self.x0
        xi = {i: -self.xi[i] for i in self.xi}
        return Affine(x0, xi)

    # Comparison operators
    def __eq__(self, other):
        """
        Operator ==
        :type other: Affine
        :rtype: bool
        """
        return self.x0 == other.x0 and self.xi == other.xi

    def __ne__(self, other):
        """
        Operator !=
        :type other: Affine
        :rtype: bool
        """
        return self.x0 != other.x0 or self.xi != other.xi

    # Formats
    def __str__(self):
        """
        Make the string format
        :rtype: string
        """
        return " + ".join([str(self.x0)] + ["".join([str(self.xi[i]),
                          "*eps", str(i)]) for i in self.xi])

    def __repr__(self):
        """
        Make the repr format
        :rtype: string
        """
        return "Affine({}, {})".format(self.x0, self.xi)

    # Methods
    def __abs__(self):
        """
        Return the absolute value of an affine form
        :rtype: Affine
        """
        pass

    def sqrt(self):
        """
        Return the square root of an affine form
        :rtype: Affine
        """
        pass

    def exp(self):
        """
        Return the exponential of an affine form
        :rtype: Affine
        """
        pass

    def log(self):
        """
        Return the logarithm of an affine form
        :rtype: Affine
        """
        pass

    # Trigo
    def sin(self):  # TODO et toutes les fonctions d'après seront définies
        """
        Return the sinus of an affine form
        :rtype: Affine
        """
        pass

    def cos(self):
        """
        Return the cosinus of an affine form
        We use the identity cos(x) = sin(x + PI/2)
        :rtype: Affine
        """
        x = self + pi/2
        return x.sin()

    def tan(self):
        """
        Return the tangent of an affine form
        We use the identity tan(x) = sin(x)/cos(x)
        :rtype: Affine
        """
        return self.sin() / self.cos()

    def cotan(self):
        """
        Return the cotangent of an affine form
        We use the identity cotan(x) = cos(x)/sin(x)
        :rtype: Affine
        """
        return self.cos() / self.sin()

    # Convertion
    def toInterval(self):
        """Convert an affine form to an interval form"""
        return Interval(self.x0 + self.rad(), self.x0 - self.rad())


if __name__ == "__main__":
    x = Affine(0, {1: 10})
    print("x= :", x)
    print("x+x= :", x + x)
    y = Affine(5, {1: 10, 2: 5})
    print(y)
    z = x + y
    print(z)
    print(z.__repr__())
    print(x - 1)
    print(x + 1)
    print(x - x)
    print(y - y)
    print(x - y)
    print(y*2)
    # print(x*y)
    x = Affine(0, {1: 10})
    print("x+x-x-x= :", x+x-x-x)
    print(-x+x)
