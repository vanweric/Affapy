"""Interval Arithmetic module"""
import AffApy.affineArithmetic
from AffApy.affapyError import AffApyError
from mpmath import (mp, fadd, fsub, fmul, fdiv, fneg, fabs, floor, ceil,
                    sqrt, exp, log, cos, fmod)


class Interval:
    """Representation of an interval"""

    def __init__(self, inf, sup):
        """
        :type inf: float or int
        :type sup: float or int
        """
        if inf < sup:
            self._inf = mp.mpf(inf, rounding='d')
            self._sup = mp.mpf(sup, rounding='u')
        else:
            self._inf = mp.mpf(sup, rounding='d')
            self._sup = mp.mpf(inf, rounding='u')

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

    def __pow__(self, n):
        """
        Operator **
        :type self: Interval
        :type n: int
        :rtype: Interval
        """
        return (self.log()*n).exp()

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
            return Interval(fabs(self.sup),
                            fabs(self.inf))
        if 0 in self:
            return Interval(0, max(fabs(self.inf),
                                   fabs(self.sup)))
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
        raise AffApyError("type error : other must be Interval, int or float")

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
        raise AffApyError("type error : other must be Interval, int or float")

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
        raise AffApyError("type error : other must be Interval, int or float")

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
        raise AffApyError("type error : other must be Interval, int or float")

    # Formats
    def __str__(self):
        """
        Make the string format
        :rtype: string
        """
        return "[{}, {}]".format(self.inf, self.sup)

    def __repr__(self):
        """
        Make the repr format
        :rtype: string
        """
        return "Interval({}, {})".format(self.inf, self.sup)

    # Precision
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
            return Interval(log(self.inf),
                            log(self.sup))
        raise AffApyError("inf must be > 0")

    def exp(self):
        """
        Return the exponential of an interval
        :rtype: Interval
        """
        return Interval(exp(self.inf, rounding='d'),
                        exp(self.sup, rounding='u'))

    def sqrt(self):
        """
        Return the square root of an interval
        :rtype: Interval
        """
        if self.inf >= 0:
            return Interval(sqrt(self.inf, rounding='d'),
                            sqrt(self.sup, rounding='u'))
        raise AffApyError("inf must be >= 0")

    def minTrigo(self):
        """
        Return the minimal 2pi periodic interval of an interval
        :return: Interval
        """
        inf, sup = self.inf, self.sup
        pi_fois_2 = fmul(2, mp.pi)
        a = fmod(inf, pi_fois_2)
        if inf < 0:
            a = fneg(a)
        if fsub(sup, inf) >= pi_fois_2:
            b = fadd(a, pi_fois_2)
        else:
            b = fmod(sup, pi_fois_2)
            if b <= a:
                b = fadd(b, pi_fois_2)
        return Interval(a, b)

    def cos(self):
        """
        Return the cosinus of an interval
        inf must be in [0, 2pi]
        :rtype: Interval
        """
        inf, sup = self.minTrigo().inf, self.minTrigo().sup
        if inf <= mp.pi:
            if sup <= mp.pi:
                return Interval(cos(sup, rounding='d'), cos(inf, rounding='u'))
            if mp.pi < sup <= 2 * mp.pi:
                return Interval(-1, max(cos(inf, rounding='u'),
                                        cos(sup, rounding='u')))
            if sup > 2 * mp.pi:
                return Interval(-1, 1)
        if mp.pi < inf <= 2 * mp.pi:
            if sup <= 2 * mp.pi:
                return Interval(cos(inf, rounding='d'), cos(sup, rounding='u'))
            if 2 * mp.pi < sup <= 3 * mp.pi:
                return Interval(min(cos(inf, rounding='d'),
                                    cos(sup, rounding='u')), 1)
            if sup >= 3 * mp.pi:
                return Interval(-1, 1)

    def sin(self):
        """
        Return the sinus of an interval
        We use the identity sin(x) = cos(pi/2 - x)
        :rtype: Interval
        """
        return (-self + float(mp.pi/2)).cos()

    def tan(self):
        """
        Return the tangent of an interval
        We use the identity tan(x) = sin(x)/cos(x)
        :rtype: Interval
        """
        return self.sin() / self.cos()

    def cotan(self):
        """
        Return the cotangent of an interval
        We use the identity cotan(x) = cos(x)/sin(x)
        :rtype: Interval
        """
        return self.cos() / self.sin()

    def toAffine(self):
        """
        Convert an interval form to an affine form
        :rtype: Affine
        """
        inf, sup = self.inf, self.sup
        return AffApy.affineArithmetic.Affine(
            (inf + sup) / 2, [(inf - sup) / 2])
