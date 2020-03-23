"""Affine Arithmetic module"""
from intervalArithmetic import Interval
from affapyError import AffApyError


class Affine:
    """Representation of an affine form"""
    count = 3
    def __init__(self, xi):
        self.xi = xi # dictionnaire
        self.keyXi = list(xi.keys())
        self.keyXi.pop(0) # on enleve x0 de la liste des clés, il aura toujours l'id 0
        self.xsi = sum(abs(i) for i in list(xi.values())[1:])
        self.interval = Interval(xi[0] + self.xsi, xi[0] - self.xsi)

    # Binary operators
    def __add__(self, other):
        """
        Operator +
        :type other: Interval or int or float
        :rtype: Interval
        """
        if isinstance(other, self.__class__):
            xi = {0: self.xi[0] + other.xi[0]}
            for i in self.keyXi:
                if i in other.keyXi:
                    xi[Affine.count] = (other.xi[i] + self.xi[i])
                    Affine.count += 1
                else:
                    xi[i] = (self.xi[i])
            for i in other.keyXi:
                if i not in self.keyXi:
                    xi[i] = (other.xi[i])
            return Affine(xi)
        if isinstance(other, int) or isinstance(other, float):
            xi = [self.xi[0] + other]
            xi += self.xi[1:]
            return Affine(xi)
        raise AffApyError("type error")
        return None

    def __sub__(self, other):
        """
        Operator -
        :type other: Interval or int or float
        :rtype: Interval
        """
        if isinstance(other, self.__class__):
            xi = [self.xi[0] - other.xi[0]]
            xi += self.xi[1:] + [-i for i in other.xi[1:]]
            return Affine(xi)
        if isinstance(other, int) or isinstance(other, float):
            xi = [other - self.xi[0]]
            xi += self.xi[1:]
            return Affine(xi)
        raise AffApyError("type error")
        return None

    def __mul__(self, other):
        """
        Operator *
        :type other: Interval
        :rtype: Interval
        """
        if isinstance(other, self.__class__):
            xi = []
            for x in self.xi:
                for y in other.xi:
                    xi.append(x * y)
            return Affine(xi)
        if isinstance(other, int) or isinstance(other, float):
            xi = [other * self.xi[0]]
            xi += [other * i for i in self.xi[1:]]
            return Affine(xi)
        raise AffApyError("type error")
        return None

    def __truediv__(self, other):
        """
        Operator /
        :type other: Interval
        :rtype: Interval
        """
        pass

    def __pow__(self, n):
        """
        Operator **
        :type other: int or float
        :rtype: Interval
        """
        pass

    # Unary operator
    def __neg__(self):
        """
        Operator - (unary)
        :rtype: Interval
        """
        pass

    # Formats
    def __str__(self):
        """
        Make the string format
        :rtype: string
        """
        return " + ".join([str(self.xi[0])] +
                          ["".join([str(self.xi[i]), "*eps", str(i)])
                           for i in range(1, len(self.xi))])

    def __repr__(self):
        """
        Make the repr format
        :rtype: string
        """
        return "Affine({})".format(self.xi)

    # Methods
    def radius(self):
        """
        Return the radius of the interval
        :rtype: int or float
        """
        return self.interval.radius()

    def middle(self):
        """
        Return the middle of the interval
        :rtype: float
        """
        return self.interval.middle()

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
        return self.interval


if __name__ == "__main__":
    dict = {0:0, 10:5, 7:3}
    listKey = dict.keys()
    list(listKey).pop(0)
    print(list(listKey).pop(0))
    print(list(dict.values())[1:])

    """
    x = Affine([0, 10])
    y = Affine([5, 5])
    print(x)
    print(y)
    print(x.interval)
    print(y.interval)
    z = x + y
    print(z)
    print(z.interval)
    x1 = Affine([3 / 2, 1 / 2])
    x2 = Affine([7 / 2, 1 / 2])
    x3 = x1 * x2
    print(x3)
    print(x3.interval)
    x4 = x1 * x1 + x2 * x2 - x1 * x2
    print(x4)
    print(x4.interval)
    print(Affine([0, 10]).toInterval())
    print(x.__repr__())
    """