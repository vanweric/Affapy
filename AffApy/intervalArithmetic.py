"""Interval Arithmetic module"""
from math import sqrt, log, exp, pi, sin, cos, floor, ceil, trunc
from AffApy.affapyError import AffApyError


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

    # Getter
    @property
    def inf(self):
        """Return the inf"""
        return self._inf

    @property
    def sup(self):
        """Return the sup"""
        return self._sup

    # Setter
    @inf.setter
    def inf(self, value):
        self._inf = value

    @sup.setter
    def sup(self, value):
        self._sup = value

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
        :type other: Interval or int or float
        :rtype: Interval
        """
        if isinstance(other, self.__class__):
            a, b = self._inf, self._sup
            c, d = other._inf, other._sup
            inf = min([a * c, a * d, b * c, b * d])
            sup = max([a * c, a * d, b * c, b * d])
            return Interval(inf, sup)
        if isinstance(other, int) or isinstance(other, float):
            return Interval(other * self._inf, other * self._sup)
        raise AffApyError("type error")
        return None

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

    def __pow__(self, n):  # TODO: le cas n<0 et n>2
        """
        Operator **
        :type self: Interval
        :type n: int
        :rtype: Interval
        """
        if isinstance(n, int) and n >= 0:
            inf, sup = self._inf, self._sup
            if n % 2 == 1:
                return Interval(inf ** n, sup ** n)
            if inf >= 0:
                return Interval(inf ** n, sup ** n)
            if sup < 0:
                return Interval(sup ** n, inf ** n)
            else:
                return Interval(0, max(inf ** n, sup ** n))
        raise AffApyError("n does not match with pow")
        return None

    # Unary operator
    def __neg__(self):
        """
        Operator - (unary)
        :type self: Interval
        :rtype: Interval
        """
        return Interval(-self._sup, -self._inf)

    def __abs__(self):
        """
        Return the absolute value of an interval
        :rtype: Interval
        """
        if self < 0:
            return Interval(abs(self._sup), abs(self._inf))
        if 0 in self:
            return Interval(0, max(abs(self._inf), abs(self._sup)))
        return self

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

    def __ge__(self, other):
        """
        Operator >=
        :type other: Interval or int or float
        :rtype: bool
        """
        if isinstance(other, self.__class__):
            return self._inf >= other._sup
        if isinstance(other, int) or isinstance(other, float):
            return self._inf >= other
        raise AffApyError("type error")
        return None

    def __gt__(self, other):
        """
        Operator >
        :type other: Interval or int or float
        :rtype: bool
        """
        if isinstance(other, self.__class__):
            return self._inf > other._sup
        if isinstance(other, int) or isinstance(other, float):
            return self._inf > other
        raise AffApyError("type error")
        return None

    def __le__(self, other):
        """
        Operator <=
        :type other: Interval or int or float
        :rtype: bool
        """
        if isinstance(other, self.__class__):
            return self._sup <= other._inf
        if isinstance(other, int) or isinstance(other, float):
            return self._sup <= other
        raise AffApyError("type error")
        return None

    def __lt__(self, other):
        """
        Operator <
        :type other: Interval or int or float
        :rtype: bool
        """
        if isinstance(other, self.__class__):
            return self._sup < other._inf
        if isinstance(other, int) or isinstance(other, float):
            return self._sup < other
        raise AffApyError("type error")
        return None

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
        return "Interval([{0} ; {1}])".format(self._inf, self._sup)

    # Precision
    def __round__(self, ndigits):
        """
        Return the round form of the interval
        :type self: Interval
        :type ndigits: int
        :rtype: Interval
        """
        if isinstance(ndigits, int):
            return Interval(round(self._inf, ndigits),
                            round(self._sup, ndigits))
        raise AffApyError("n must be int")
        return None

    def __trunc__(self):
        """
        Return the truncate of the interval
        :type self: Interval
        :rtype: Interval
        """
        return Interval(trunc(self._inf), trunc(self._sup))

    def __floor__(self):
        """
        Return the floor of the interval
        :type self: Interval
        :rtype: Interval
        """
        return Interval(floor(self._inf), floor(self._sup))

    def __ceil__(self):
        """
        Return the ceiling of the interval
        :type self: Interval
        :rtype: Interval
        """
        return Interval(ceil(self._inf), ceil(self._sup))

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
        inf must be in [-pi/2, 3pi/2]
        :rtype: Interval
        """
        inf, sup = self._inf, self._sup
        if inf <= pi / 2:
            if sup <= pi / 2:
                return Interval(sin(inf), sin(sup))
            if pi / 2 < sup <= 3 * pi / 2:
                print(inf, sin(inf), sup, sin(sup))
                return Interval(min(sin(inf), sin(sup)), 1)
            if sup > 3 * pi / 2:
                return Interval(-1, 1)
        if pi / 2 < inf <= 3 * pi / 2:
            if pi / 2 < sup <= 3 * pi / 2:
                return Interval(sin(sup), sin(inf))
            if 3 * pi / 2 < sup <= 2 * pi + pi / 2:
                return Interval(-1, max(sin(inf), sin(sup)))
            if sup >= 2 * pi + pi / 2:
                return Interval(-1, 1)
        raise AffApyError("the interval does not match with sinus")
        return None

    def cos(self):
        """
        Return the cosinus of an interval
        inf must be in [0, 2pi]
        :rtype: Interval
        """
        inf, sup = self._inf, self._sup
        if inf <= pi:
            if sup <= pi:
                return Interval(cos(sup), cos(inf))
            if pi < sup <= 2 * pi:
                return Interval(-1, max(cos(inf), cos(sup)))
            if sup > 2 * pi:
                return Interval(-1, 1)
        if pi < inf <= 2 * pi:
            if sup <= 2 * pi:
                return Interval(cos(inf), cos(sup))
            if 2 * pi < sup <= 3 * pi:
                return Interval(min(cos(inf), cos(sup)), 1)
            if sup >= 3 * pi:
                return Interval(-1, 1)
        raise AffApyError("the interval does not match with cosinus")
        return None

    def toAffine(self):
        """Convert an interval form to an affine form"""
        from affineArithmetic import Affine
        inf, sup = self._inf, self._sup
        return Affine([(inf + sup) / 2, (inf - sup) / 2])

    def minTrigo(self):
        """
        Return the minimal 2PI periodic interval of an interval
        :return: Interval
        """
        inf, sup = self._inf, self._sup
        a = inf % (2 * pi)
        if inf < 0:
            a = -a
        if (sup - inf) >= (2 * pi):
            b = a + 2 * pi
        else:
            b = sup % (2 * pi)
            if b <= a:
                b += 2*pi
        return Interval(a, b)


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
    # print(Interval(-10, 10).toAffine())
    print(x.__repr__())
    print(abs(Interval(-5, -2)))
    print(abs(Interval(-2, 1)))
    print(abs(Interval(1, 2)))
    print(Interval(-pi / 2, pi / 2).sin())
    print(Interval(pi / 4, pi).sin())
    print(Interval(-pi, pi / 4).cos())
    print(Interval(0, 3 * pi / 2).cos())
    print(Interval(3, 5) ** 3)
    print(Interval(-2, 3) ** 2)
    print(round(Interval(-pi, pi), 2))
    print(trunc(Interval(-pi, pi)))
    print(floor(Interval(-pi, pi)))
    print(ceil(Interval(-pi, pi)))
    print((6*pi - 5*pi) >= 2 * pi)
    print(Interval(5*pi, 6 * pi).minTrigo())
