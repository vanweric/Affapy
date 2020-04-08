"""Interval Arithmetic module"""
import AffApy.affineArithmetic
from AffApy.affapyError import AffApyError
from mpmath import mp, fadd, fsub, fmul, fdiv, fneg, fabs, floor, ceil


class Interval:
    """Representation of an interval"""

    def __init__(self, inf, sup):
        """
        :type inf: float or int
        :type sup: float or int
        """
        if inf < sup:
            self._inf = mp.mpf(inf)
            self._sup = mp.mpf(sup)
        else:
            self._inf = mp.mpf(sup)
            self._sup = mp.mpf(inf)

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
            return self.inf <= other.inf and self.sup >= other.sup
        if isinstance(other, int) or isinstance(other, float):
            return self.inf <= other <= self.sup
        raise AffApyError("type error")

    # Binary operators
    def __add__(self, other):
        """
        Operator +
        :type other: Interval or int or float
        :rtype: Interval
        """
        if isinstance(other, self.__class__):
            inf = fadd(self.inf, other.inf, rounding='d')
            sup = fadd(self.sup, other.sup, rounding='u')
            return Interval(inf, sup)
        if isinstance(other, int) or isinstance(other, float):
            inf = fadd(self.inf, mp.mpf(other), rounding='d')
            sup = fadd(self.sup, mp.mpf(other), rounding='u')
            return Interval(inf, sup)
        raise AffApyError("type error : other must be Interval, int or float")

    def __sub__(self, other):
        """
        Operator -
        :type other: Interval or int or float
        :rtype: Interval
        """
        if isinstance(other, self.__class__):
            inf = fsub(self.inf, other.sup, rounding='d')
            sup = fsub(self.sup, other.inf, rounding='u')
            return Interval(inf, sup)
        if isinstance(other, int) or isinstance(other, float):
            inf = fsub(self.inf, mp.mpf(other), rounding='d')
            sup = fsub(self.sup, mp.mpf(other), rounding='u')
            return Interval(inf, sup)
        raise AffApyError("type error : other must be Interval, int or float")

    def __mul__(self, other):
        """
        Operator *
        :type other: Interval or int or float
        :rtype: Interval
        """
        if isinstance(other, self.__class__):
            a, b = self.inf, self.sup
            c, d = other.inf, other.sup
            inf = min([fmul(a, c, rounding='d'), fmul(a, d, rounding='d'),
                       fmul(b, c, rounding='d'), fmul(b, d, rounding='d')])
            sup = max([fmul(a, c, rounding='u'), fmul(a, d, rounding='u'),
                       fmul(b, c, rounding='u'), fmul(b, d, rounding='u')])
            return Interval(inf, sup)
        if isinstance(other, int) or isinstance(other, float):
            return Interval(fmul(mp.mpf(other), self.inf, rounding='d'),
                            fmul(mp.mpf(other), self.sup, rounding='u'))
        raise AffApyError("type error : other must be Interval, int or float")

    def __truediv__(self, other):  # TRAITER LES CAS INFINIS ?
        """
        Operator /
        :type other: Interval
        :rtype: Interval
        """
        c, d = other.inf, other.sup
        if 0 not in other:
            return self * Interval(fdiv(1, d, rounding='d'),
                                   fdiv(1, c, rounding='u'))
        raise AffApyError("division by 0")

    def __pow__(self, n):  # TODO: le cas n<0 et n>2
        """
        Operator **
        :type self: Interval
        :type n: int
        :rtype: Interval
        """
        if isinstance(n, int) and n >= 0:
            inf, sup = self.inf, self.sup
            if n % 2 == 1:
                return Interval(inf ** n, sup ** n)
            if inf >= 0:
                return Interval(inf ** n, sup ** n)
            if sup < 0:
                return Interval(sup ** n, inf ** n)
            else:
                return Interval(0, max(inf ** n, sup ** n))
        raise AffApyError("n does not match with pow")

    # Unary operator
    def __neg__(self):
        """
        Operator - (unary)
        :type self: Interval
        :rtype: Interval
        """
        return Interval(fneg(self.sup, rounding='d'),
                        fneg(self.inf, rounding='u'))

    def __abs__(self):
        """
        Return the absolute value of an interval
        :rtype: Interval
        """
        if self < 0:
            return Interval(fabs(self.sup, rounding='d'),
                            fabs(self.inf, rounding='u'))
        if 0 in self:
            return Interval(0, max(fabs(self.inf, rounding='u'),
                                   fabs(self.sup, rounding='u')))
        return self

    # Comparison operators
    def __eq__(self, other):
        """
        Operator ==
        :type other: Interval
        :rtype: bool
        """
        return self.inf == other.inf and self.sup == other.sup

    def __ne__(self, other):
        """
        Operator !=
        :type other: Interval
        :rtype: bool
        """
        return self.inf != other.inf or self.sup != other.sup

    def __ge__(self, other):
        """
        Operator >=
        :type other: Interval or int or float
        :rtype: bool
        """
        if isinstance(other, self.__class__):
            return self.inf >= other.sup
        if isinstance(other, int) or isinstance(other, float):
            return self.inf >= other
        raise AffApyError("type error")

    def __gt__(self, other):
        """
        Operator >
        :type other: Interval or int or float
        :rtype: bool
        """
        if isinstance(other, self.__class__):
            return self.inf > other.sup
        if isinstance(other, int) or isinstance(other, float):
            return self.inf > other
        raise AffApyError("type error")

    def __le__(self, other):
        """
        Operator <=
        :type other: Interval or int or float
        :rtype: bool
        """
        if isinstance(other, self.__class__):
            return self.sup <= other.inf
        if isinstance(other, int) or isinstance(other, float):
            return self.sup <= other
        raise AffApyError("type error")

    def __lt__(self, other):
        """
        Operator <
        :type other: Interval or int or float
        :rtype: bool
        """
        if isinstance(other, self.__class__):
            return self.sup < other.inf
        if isinstance(other, int) or isinstance(other, float):
            return self.sup < other
        raise AffApyError("type error")

    # Formats
    def __str__(self):
        """
        Make the string format
        :rtype: string
        """
        return "".join(["[", str(self.inf), ", ", str(self.sup), "]"])

    def __repr__(self):
        """
        Make the repr format
        :rtype: string
        """
        return "Interval({}, {})".format(self.inf, self.sup)

    # Precision
    def __round__(self, ndigits):
        """
        Return the round form of the interval
        :type self: Interval
        :type ndigits: int
        :rtype: Interval
        """
        if isinstance(ndigits, int):
            return Interval(round(self.inf, ndigits),
                            round(self.sup, ndigits))
        raise AffApyError("n must be int")

    # def __trunc__(self):
    #     """
    #     Return the truncate of the interval
    #     :type self: Interval
    #     :rtype: Interval
    #     """
    #     return Interval(trunc(self.inf), trunc(self.sup))

    def __floor__(self):
        """
        Return the floor of the interval
        :type self: Interval
        :rtype: Interval
        """
        return Interval(floor(self.inf, rounding='d'),
                        floor(self.sup, rounding='u'))

    def __ceil__(self):
        """
        Return the ceiling of the interval
        :type self: Interval
        :rtype: Interval
        """
        return Interval(ceil(self.inf, rounding='d'),
                        ceil(self.sup, rounding='u'))

    # Methods
    def radius(self):
        """
        Return the radius of the interval
        :rtype: int or float
        """
        return fsub(self.sup, self.inf)

    def middle(self):
        """
        Return the middle of the interval
        :rtype: float
        """
        return fdiv(fadd(self.inf, self.sup), 2)

    def log(self):
        """
        Return the logarithm of an interval
        :rtype: Interval
        """
        if self.inf > 0:
            return Interval(log(self.inf), log(self.sup))
        raise AffApyError("inf must be > 0")

    def exp(self):
        """
        Return the exponential of an interval
        :rtype: Interval
        """
        return Interval(exp(self.inf), exp(self.sup))

    def sqrt(self):
        """
        Return the square root of an interval
        :rtype: Interval
        """
        if self.inf >= 0:
            return Interval(sqrt(self.inf), sqrt(self.sup))
        raise AffApyError("inf must be >= 0")

    def sin(self):
        """
        Return the sinus of an interval
        inf must be in [-pi/2, 3pi/2]
        :rtype: Interval
        """
        inf, sup = self.inf, self.sup
        if inf <= mp.pi / 2:
            if sup <= mp.pi / 2:
                return Interval(sin(inf), sin(sup))
            if mp.pi / 2 < sup <= 3 * mp.pi / 2:
                print(inf, sin(inf), sup, sin(sup))
                return Interval(min(sin(inf), sin(sup)), 1)
            if sup > 3 * mp.pi / 2:
                return Interval(-1, 1)
        if mp.pi / 2 < inf <= 3 * mp.pi / 2:
            if mp.pi / 2 < sup <= 3 * mp.pi / 2:
                return Interval(sin(sup), sin(inf))
            if 3 * mp.pi / 2 < sup <= 2 * mp.pi + mp.pi / 2:
                return Interval(-1, max(sin(inf), sin(sup)))
            if sup >= 2 * mp.pi + mp.pi / 2:
                return Interval(-1, 1)
        raise AffApyError("the interval does not match with sinus")

    def cos(self):
        """
        Return the cosinus of an interval
        inf must be in [0, 2pi]
        :rtype: Interval
        """
        inf, sup = self.inf, self.sup
        if inf <= mp.pi:
            if sup <= mp.pi:
                return Interval(cos(sup), cos(inf))
            if mp.pi < sup <= 2 * mp.pi:
                return Interval(-1, max(cos(inf), cos(sup)))
            if sup > 2 * mp.pi:
                return Interval(-1, 1)
        if mp.pi < inf <= 2 * mp.pi:
            if sup <= 2 * mp.pi:
                return Interval(cos(inf), cos(sup))
            if 2 * mp.pi < sup <= 3 * mp.pi:
                return Interval(min(cos(inf), cos(sup)), 1)
            if sup >= 3 * mp.pi:
                return Interval(-1, 1)
        raise AffApyError("the interval does not match with cosinus")

    def toAffine(self):
        """Convert an interval form to an affine form"""
        inf, sup = self.inf, self.sup
        return AffApy.affineArithmetic.Affine(
            (inf + sup) / 2, [(inf - sup) / 2])

    def minTrigo(self):
        """
        Return the minimal 2pi periodic interval of an interval
        :return: Interval
        """
        inf, sup = self.inf, self.sup
        a = inf % (2 * mp.pi)
        if inf < 0:
            a = -a
        if (sup - inf) >= (2 * mp.pi):
            b = a + 2 * mp.pi
        else:
            b = sup % (2 * mp.pi)
            if b <= a:
                b += 2*mp.pi
        return Interval(a, b)
