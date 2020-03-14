"""Définir une arithmétique affine"""
from intervalArithmetic import Interval


class Affine:
    """Representation of an affine form"""

    def __init__(self, xi):
        self.xi = xi  # liste
        self.xsi = sum([abs(i) for i in xi[1:]])
        self.interval = Interval(xi[0] + self.xsi, xi[0] - self.xsi)

    # Binary operators
    def __add__(self, other):
        """
        Operator +
        :type other: Interval or int or float
        :rtype: Interval
        """
        if isinstance(other, self.__class__):
            xi = [self.xi[0] + other.xi[0]]
            xi += self.xi[1:] + other.xi[1:]
            return Affine(xi)
        elif isinstance(other, int) or isinstance(other, float):
            xi = [self.xi[0] + other]
            xi += self.xi[1:]
            return Affine(xi)
        print("Error : unknown type")
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
        elif isinstance(other, int) or isinstance(other, float):
            xi = [other - self.xi[0]]
            xi += self.xi[1:]
            return Affine(xi)
        print("Error : unknown type")
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
        elif isinstance(other, int) or isinstance(other, float):
            xi = [other * self.xi[0]]
            xi += [other * i for i in self.xi[1:]]
            return Affine(xi)
        print("Error : unknown type")
        return None

    def __truediv__(self, other):
        pass

    def __pow__(self, n):
        pass

    # Unary operator
    def __neg__(self):
        pass

    # String form
    def __str__(self):
        """
        Make the string format
        :rtype: string
        """
        return " + ".join(
            [str(self.xi[0])] + ["".join([str(self.xi[i]), "*eps", str(i)]) for i in range(1, len(self.xi))])

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
        pass

    def sqrt(self):
        pass

    def exp(self):
        pass

    def log(self):
        pass

    def cos(self):
        pass

    def sin(self):
        pass

    def tan(self):
        pass


def intervalToAffine(interval):
    """Convert an interval form to an affine form"""
    inf, sup = interval.inf, interval.sup
    return Affine([(inf + sup) / 2, (inf - sup) / 2])


def affineToInterval(affine):
    """Convert an affine form to an interval form"""
    return affine.interval


if __name__ == "__main__":
    x = Affine([0, 10])
    y = Affine([5, 5])
    print(x)
    print(y)
    print(intervalToAffine(Interval(-10, 10)))
    print(affineToInterval(Affine([0, 10])))
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
