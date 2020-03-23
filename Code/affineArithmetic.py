"""Affine Arithmetic module"""
from intervalArithmetic import Interval
from affapyError import AffApyError


class Affine:
    """Representation of an affine form"""
    count = 3

    def __init__(self, xi):
        self._xi = xi    # dictionnaire
        self._keyXi = list(xi.keys())[1:]
        # on enlève x0 de la liste des clés, il aura toujours l'id 0
        self._xsi = sum(abs(i) for i in list(xi.values())[1:])

    @property
    def xi(self):
        """Return xi"""
        return self._xi

    @property
    def keyXi(self):
        """Return keyXi """
        return self._keyXi

    @property
    def xsi(self):
        """Returns xsi"""
        return self._xsi

    # Binary operators
    def __add__(self, other):
        """
        Operator +
        :type other: Affine or int or float
        :rtype: Affine
        """
        if isinstance(other, self.__class__):
            xi = {0: self.xi[0] + other.xi[0]}
            for i in self.keyXi:
                if i in other.keyXi:
                    xi[Affine.count] = other.xi[i] + self.xi[i]
                    Affine.count += 1
                else:
                    xi[i] = self.xi[i]
            for i in other.keyXi:
                if i not in self.keyXi:
                    xi[i] = other.xi[i]
            return Affine(xi)
        if isinstance(other, int) or isinstance(other, float):
            xi = dict(self.xi)
            xi[0] += other
            return Affine(xi)
        raise AffApyError("type error")
        return None

    def __sub__(self, other):
        """
        Operator -
        :type other: Affine or int or float
        :rtype: Affine
        """
        if isinstance(other, self.__class__):
            xi = {0: self.xi[0] + other.xi[0]}
            for i in self.keyXi:
                if i in other.keyXi:
                    xi[Affine.count] = other.xi[i] - self.xi[i]
                    Affine.count += 1
                else:
                    xi[i] = self.xi[i]
            for i in other.keyXi:
                if i not in self.keyXi:
                    xi[i] = other.xi[i]
            return Affine(xi)
        if isinstance(other, int) or isinstance(other, float):
            xi = dict(self.xi)
            xi[0] -= other
            return Affine(xi)
        raise AffApyError("type error")
        return None

    def __mul__(self, other):
        """
        Operator *
        :type other: Affine
        :rtype: Affine
        """
        # if isinstance(other, self.__class__):
        #     xi = []
        #     for x in self.xi:
        #         for y in other.xi:
        #             xi.append(x * y)
        #     return Affine(xi)
        # if isinstance(other, int) or isinstance(other, float):
        #     xi = [other * self.xi[0]]
        #     xi += [other * i for i in self.xi[1:]]
        #     return Affine(xi)
        # raise AffApyError("type error")
        return None

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
        pass

    # Comparison operators
    def __eq__(self, other):
        """
        Operator ==
        :type other: Affine
        :rtype: bool
        """
        return self.xi == other.xi

    def __ne__(self, other):
        """
        Operator !=
        :type other: Affine
        :rtype: bool
        """
        return self.xi != other.xi

    # Formats
    def __str__(self):
        """
        Make the string format
        :rtype: string
        """
        return " + ".join([str(self.xi[0])] + ["".join([str(self.xi[i]),
                          "*eps", str(i)]) for i in self.keyXi])

    def __repr__(self):
        """
        Make the repr format
        :rtype: string
        """
        return "Affine({})".format(self.xi)

    # Methods
    def abs(self):
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

    def cos(self):
        """
        Return the cosinus of an affine form
        :rtype: Affine
        """
        pass

    def sin(self):
        """
        Return the sinus of an affine form
        :rtype: Affine
        """
        pass

    def tan(self):
        """
        Return the tangent of an affine form
        :rtype: Affine
        """
        pass

    def toInterval(self):
        """Convert an affine form to an interval form"""
        return Interval(self.xi[0] + self.xsi, self.xi[0] - self.xsi)


if __name__ == "__main__":
    x = Affine({0: 0, 1: 10})
    print(x)
    y = Affine({0: 5, 1: 10, 2: 5})
    print(y)
    z = x + y
    print(z)
    print(z.__repr__())
    print(x - 1)
    print(x + 1)
