"""Use of Interval Arithmetic"""
from math import sqrt, log, exp
from affapyError import AffApyError


class Interval:
    """Representation of an interval"""

    def __init__(self, inf, sup):
        """
        :type inf: float or int
        :type sup: float or int
        """
        if inf < sup:
            self._inf = inf
            self._sup = sup
        else:
            self._inf = sup
            self._sup = inf

    @property
    def inf(self):
        """Returns the inf"""
        return self._inf

    @property
    def sup(self):
        """Returns the sup"""
        return self._sup

    # Inclusion
    def __contains__(self, other):
        """
        Operator in
        :type other: Interval or int or float
        :rtype: bool
        """
        if isinstance(other, self.__class__):
            return self._inf <= other._inf and self._sup >= other._sup
        if isinstance(other, int) or isinstance(other, float):
            return self._inf <= other <= self._sup
        raise AffApyError("type error")
        return None

    # Binary operators
    def __add__(self, other):
        """
        Operator +
        :type other: Interval or int or float
        :rtype: Interval
        """
        if isinstance(other, self.__class__):
            inf = self._inf + other._inf
            sup = self._sup + other._sup
            return Interval(inf, sup)
        if isinstance(other, int) or isinstance(other, float):
            inf = self._inf + other
            sup = self._sup + other
            return Interval(inf, sup)
        raise AffApyError("type error")
        return None

    def __sub__(self, other):
        """
        Operator -
        :type other: Interval or int or float
        :rtype: Interval
        """
        if isinstance(other, self.__class__):
            inf = self._inf - other._sup
            sup = self._sup - other._inf
            return Interval(inf, sup)
        if isinstance(other, int) or isinstance(other, float):
            inf = self._inf - other
            sup = self._sup - other
            return Interval(inf, sup)
        raise AffApyError("type error")
        return None

    def __mul__(self, other):
        """
        Operator *
        :type other: Interval
        :rtype: Interval
        """
        a, b = self._inf, self._sup
        c, d = other._inf, other._sup
        inf = min([a * c, a * d, b * c, b * d])
        sup = max([a * c, a * d, b * c, b * d])
        return Interval(inf, sup)

    def __truediv__(self, other):  # TRAITER LES CAS INFINIS ?
        """
        Operator /
        :type other: Interval
        :rtype: Interval
        """
        c, d = other._inf, other._sup
        if 0 not in other:
            return self * Interval(1 / d, 1 / c)
        raise AffApyError("division by 0")
        return None

    def __pow__(self, n):  # SEULEMENT PUISSANCE 2 POUR L'INSTANT
        """
        Operator **
        :type self: Interval
        :type n: int
        :rtype: Interval
        """
        if n == 2:
            inf, sup = self._inf, self._sup
            if 0 not in self:
                return Interval(min(inf ** n, sup ** n),
                                max(inf ** n, sup ** n))
            return Interval(0, max(inf ** n, sup ** n))
        raise AffApyError("only power 2 accepted for the moment")
        return None

    # Unary operator
    def __neg__(self):
        """
        Operator - (unary)
        :type self: Interval
        :rtype: Interval
        """
        return Interval(-self._sup, -self._inf)

    # Comparison operators
    def __eq__(self, other):
        """
        Operator ==
        :type other: Interval
        :rtype: bool
        """
        return self._inf == other._inf and self._sup == other._sup

    def __ne__(self, other):
        """
        Operator !=
        :type other: Interval
        :rtype: bool
        """
        return self._inf != other._inf or self._sup != other._sup

    def __ge__(self, n):
        """
        Operator >=
        :type n: int or float
        :rtype: bool
        """
        return self._inf >= n

    def __gt__(self, n):
        """
        Operator >
        :type n: int or float
        :rtype: bool
        """
        return self._inf > n

    def __le__(self, n):
        """
        Operator <=
        :type n: int or float
        :rtype: bool
        """
        return self._sup <= n

    def __lt__(self, n):
        """
        Operator <
        :type n: int or float
        :rtype: bool
        """
        return self._sup < n

    # Formats
    def __str__(self):
        """
        Make the string format
        :rtype: string
        """
        return "".join(["[", str(self._inf), " ; ", str(self._sup), "]"])

    def __repr__(self):
        """
        Make the repr format
        :rtype: string
        """
        return "Interval([{0} ; {1}])".format(self._inf, self._sup,)

    # Methods
    def radius(self):
        """
        Return the radius of the interval
        :rtype: int or float
        """
        return self._sup - self._inf

    def middle(self):
        """
        Return the middle of the interval
        :rtype: float
        """
        return (self._inf + self._sup) / 2

    def log(self):
        """
        Return the logarithm of an interval
        :rtype: Interval
        """
        if self._inf > 0:
            return Interval(log(self._inf), log(self._sup))
        raise AffApyError("inf must be > 0")
        return None

    def exp(self):
        """
        Return the exponential of an interval
        :rtype: Interval
        """
        return Interval(exp(self._inf), exp(self._sup))

    def sqrt(self):
        """
        Return the square root of an interval
        :rtype: Interval
        """
        if self._inf >= 0:
            return Interval(sqrt(self._inf), sqrt(self._sup))
        raise AffApyError("inf must be >= 0")
        return None

    def sin(self):
        """
        Return the sinus of an interval
        :rtype: Interval
        """
        pass

    def cos(self):
        """
        Return the cosinus of an interval
        :rtype: Interval
        """
        pass

    def abs(self):
        """
        Return the absolute value of an interval
        :rtype: Interval
        """
        pass

    def toAffine(self):
        """Convert an interval form to an affine form"""
        from affineArithmetic import Affine
        inf, sup = self._inf, self._sup
        return Affine([(inf + sup) / 2, (inf - sup) / 2])


if __name__ == "__main__":
    x = Interval(1, 2)
    y = Interval(3, 4)
    z = Interval(-1, 1)
    print(x + y)
    print(x + 2)
    print(x - y)
    print(x - 2)
    print(x * y)
    print(x / y)
    # print(x / z)
    print(z * (x + y))
    print(y ** 2)
    print(z ** 2)
    # print(x ** 3)
    print(x ** 2 + y ** 2 - x * y)
    print(-x)
    print(x == y)
    print(x != y)
    print(x == Interval(1, 2))
    print(x != Interval(1, 2))
    print(x >= 0)
    print(x > 1)
    print(x <= 2)
    print(x < 2)
    print(x.middle())
    print(z.middle())
    print(x.radius())
    print(z.radius())
    print(x in Interval(0, 4))
    print(x in Interval(2, 4))
    print(0 in z)
    print(0 in y)
    print(x.exp())
    print(x.log())
    print(y.sqrt())
    x2 = Interval(-2, 3)
    y2 = Interval(1, 4)
    z2 = Interval(-2, 1)
    print(x2 * x2)
    print(x2 ** 2)
    print(x2 * (y2 + z2))
    print(x2 * y2 + x2 * z2)
    print(x2 * (y2 + z2) in x2 * y2 + x2 * z2)
    # print(Interval(-2, 0).sqrt())
    # print(Interval(0, 1).log())
    print(Interval(-10, 10).toAffine())
    print(x.__repr__())
