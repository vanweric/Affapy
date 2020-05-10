"""Interval Arithmetic module"""
import AffApy.affineArithmetic
from AffApy.affapyError import AffApyError
from mpmath import (mp, fadd, fsub, fmul, fdiv, fneg, fabs, floor, ceil,
                    sqrt, exp, log, cos, fmod)


class Interval:
    """Representation of an interval"""

    def __init__(self, inf, sup):
        """Init an Interval

        Create an interval. It is composed of two fields :
        the infimum and the supremum. If inf > sup, then the init function
        reorganize the two values.

        Args:
            inf (int or float or string): infimum
            sup (int or float or string): supremum

        Returns:
            Interval

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
        """Set the inf"""
        self._inf = value

    @sup.setter
    def sup(self, value):
        """Set the sup"""
        self._sup = value

    def straddles_zero(self):
        """
        Return True if the interval straddles 0, False if not

        Args:
            self (Interval): operand

        Returns:
            bool: 0 in self

        """
        return 0 in self

    # Inclusion
    def __contains__(self, other):
        """Operator in

        Return True if "other", who is Interval, or int, or float is
        in self, who is an Interval.

        Args:
            self (Interval): second operand
            other (Interval or Affine or int or float): first operand

        Returns:
            bool: other in self

        Raises:
            AffApyError: if other is not Interval, int, float, Affine

        """
        if isinstance(other, self.__class__):
            return self.inf <= other.inf and self.sup >= other.sup
        if isinstance(other, int) or isinstance(other, float):
            return self.inf <= other <= self.sup
        if isinstance(other, AffApy.affineArithmetic.Affine):
            return (self.inf <= other.interval.inf
                    and self.sup >= other.interval.sup)
        raise AffApyError("other must be Interval, int, float, Affine")

    # Binary operators
    def __add__(self, other):
        """Operator +

        Add two Intervals or an Interval and an integer or float.
        It adds infimums and supremums.

        Args:
            self (Interval): first operand
            other (Interval or int or float): second operand

        Returns:
            Interval: self + other

        Raises:
            AffApyError: if other is not Interval, int or float

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

    def __radd__(self, other):
        """Reverse operator +

        Add two Intervals or an Interval and an integer or float

        Args:
            self (Interval): second operand
            other (Interval or int or float): first operand

        Returns:
            Interval: other + self

        Raises:
            AffApyError: if other is not Interval, int or float

        """
        return self + other

    def __sub__(self, other):
        """Operator -

        Substract two Intervals or an Interval and an integer or float.
        It substracts infimums and supremums.

        Args:
            self (Interval): first operand
            other (Interval or int or float): second operand

        Returns:
            Interval: self - other

        Raises:
            AffApyError: if other is not Interval, int or float

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

    def __rsub__(self, other):
        """Reverse operator -

        Substract two Intervals or an Interval and an integer or float

        Args:
            self (Interval): second operand
            other (Interval or int or float): first operand

        Returns:
            Interval: other - self

        Raises:
            AffApyError: if other is not Interval, int or float

        """
        return -self + other

    def __mul__(self, other):
        """Operator *

        Multiply two Intervals or an Interval and an integer or float.

        Args:
            self (Interval): first operand
            other (Interval or int or float): second operand

        Returns:
            Interval: self * other

        Raises:
            AffApyError: if other is not Interval, int or float

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

    def __rmul__(self, other):
        """Reverse operator *

        Multiply two Intervals or an Interval and an integer or float

        Args:
            self (Interval): second operand
            other (Interval or int or float): first operand

        Returns:
            Interval: other * self

        Raises:
            AffApyError: if other is not Interval, int or float

        """
        return self * other

    def __truediv__(self, other):  # TRAITER LES CAS INFINIS ?
        """Operator /

        Divide two Intervals.
        It uses the identity : [a, b] / [c, d] = [a, b] * [1/d, 1/c].
        It is possible if other does not contains 0.

        Args:
            self (Interval): first operand
            other (Interval): second operand

        Returns:
            Interval: self / other

        Raises:
            AffApyError: division by 0

        """
        c, d = other.inf, other.sup
        if 0 not in other:
            return self * Interval(fdiv(1, d, rounding='d'),
                                   fdiv(1, c, rounding='u'))
        raise AffApyError("division by 0")

    def __pow__(self, n):
        """Operator /

        Return the power of an Interval.

        Args:
            self (Interval): first operand
            n (int): second operand (power)

        Returns:
            Interval: self ** n

        """
        if self.inf < 0 and self.sup > 0:
            interval = Interval(-self.inf, self.sup)
            result = (interval.log() * n).exp()
            if n % 2 != 0:
                result.inf = -result.inf
                return result
            else:
                maximum = max(result.inf, result.sup)
                result.inf = 0
                result.sup = maximum
                return result
        if self.sup < 0:
            interval = Interval(-self.sup, -self.inf)
            result = (interval.log() * n).exp()
            if n % 2 != 0:
                inf = result.inf
                result.inf = -result.sup
                result.sup = -inf
                return result
            else:
                return result
        if self.inf > 0:
            return (self.log() * n).exp()

    # Unary operator
    def __neg__(self):
        """Operator - (unary)

        Return the additive inverse of an Interval

        Args:
            self (Interval): operand

        Returns:
            Interval: -self

        """
        return Interval(fneg(self.sup, rounding='d'),
                        fneg(self.inf, rounding='u'))

    def __abs__(self):
        """Function abs

        Return the absolute value of an Interval

        Args:
            self (Interval): operand

        Returns:
            Interval: abs(self)

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
        """Operator ==

        Compare two Intervals

        Args:
            self (Interval): first operand
            other (Interval): second operand

        Returns:
            bool: self == other

        """
        return self.inf == other.inf and self.sup == other.sup

    def __ne__(self, other):
        """Operator !=

        Negative comparison of two Intervals

        Args:
            self (Interval): first operand
            other (Interval): second operand

        Returns:
            bool: self != other

        """
        return self.inf != other.inf or self.sup != other.sup

    def __ge__(self, other):
        """Operator >=

        Greater or equal comparison between two Intervals

        Args:
            self (Interval): first operand
            other (Interval): second operand

        Returns:
            bool: self >= other

        """
        if isinstance(other, self.__class__):
            return self.inf >= other.sup
        if isinstance(other, int) or isinstance(other, float):
            return self.inf >= other
        raise AffApyError("type error : other must be Interval, int or float")

    def __gt__(self, other):
        """Operator >

        Greater comparison between two Intervals

        Args:
            self (Interval): first operand
            other (Interval): second operand

        Returns:
            bool: self > other

        """
        if isinstance(other, self.__class__):
            return self.inf > other.sup
        if isinstance(other, int) or isinstance(other, float):
            return self.inf > other
        raise AffApyError("type error : other must be Interval, int or float")

    def __le__(self, other):
        """Operator <=

        Lesser or equal comparison between two Intervals

        Args:
            self (Interval): first operand
            other (Interval): second operand

        Returns:
            bool: self <= other

        """
        if isinstance(other, self.__class__):
            return self.sup <= other.inf
        if isinstance(other, int) or isinstance(other, float):
            return self.sup <= other
        raise AffApyError("type error : other must be Interval, int or float")

    def __lt__(self, other):
        """Operator <

        Lesser comparison between two Intervals

        Args:
            self (Interval): first operand
            other (Interval): second operand

        Returns:
            bool: self < other

        """
        if isinstance(other, self.__class__):
            return self.sup < other.inf
        if isinstance(other, int) or isinstance(other, float):
            return self.sup < other
        raise AffApyError("type error : other must be Interval, int or float")

    # Formats
    def __str__(self):
        """String format

        Make the string format

        Args:
            self (Interval): arg

        Returns:
            string: the infimum and the supremum

        Examples:
            >>> print(Interval(1, 2)
            [1, 2]

        """
        return "[{}, {}]".format(self.inf, self.sup)

    def __repr__(self):
        """Repr format

        Make the repr format

        Args:
            self (Interval): arg

        Returns:
            string: format

        """
        return "Interval({}, {})".format(self.inf, self.sup)

    # Precision
    def __floor__(self):
        """Function floor

        Return the floor of an Interval

        Args:
            self (Interval): arg

        Returns:
            Interval: [floor(inf), floor(sup)]

        """
        return Interval(floor(self.inf, rounding='d'),
                        floor(self.sup, rounding='u'))

    def __ceil__(self):
        """Function ceil

        Return the ceil of an Interval

        Args:
            self (Interval): arg

        Returns:
            Interval: [ceil(inf), ceil(sup)]

        """
        return Interval(ceil(self.inf, rounding='d'),
                        ceil(self.sup, rounding='u'))

    # Methods
    def mid(self):
        """Middle

        Return the middle of an Interval

        Args:
            self (Interval): arg

        Returns:
            float: (inf + sup) / 2

        """
        return fdiv(fadd(self.inf, self.sup), 2)

    def radius(self):
        """Radius

        Return the radius of an Interval

        Args:
            self (Interval): arg

        Returns:
            mpf: max(m - inf, sup - m) where m is middle

        """
        m = self.mid()
        return max(fsub(m, self.inf, rounding='u'),
                   fsub(self.sup, m, rounding='u'))

    def log(self):
        """Function log

        Return the logarithm of an Interval

        Args:
            self (Interval): operand

        Returns:
            Interval: log(self)

        Raises:
            AffApyError: the interval must be > 0

        """
        if self.inf > 0:
            return Interval(log(self.inf),
                            log(self.sup))
        raise AffApyError("inf must be > 0")

    def exp(self):
        """Function exp

        Return the exponential of an Interval

        Args:
            self (Interval): operand

        Returns:
            Interval: exp(self)

        """
        return Interval(exp(self.inf, rounding='d'),
                        exp(self.sup, rounding='u'))

    def sqrt(self):
        """Function log

        Return the square root of an Interval

        Args:
            self (Interval): operand

        Returns:
            Interval: sqrt(self)

        Raises:
            AffApyError: the interval must be >= 0

        """
        if self.inf >= 0:
            return Interval(sqrt(self.inf, rounding='d'),
                            sqrt(self.sup, rounding='u'))
        raise AffApyError("inf must be >= 0")

    def minTrigo(self):
        """Function minTrigo

        Return the minimal 2pi periodic interval of an Interval

        Args:
            self (Interval): operand

        Returns:
            Interval: minimal 2pi periodic interval
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
        """Function cos

        Return the cosinus of an Interval.

        Args:
            self (Interval): operand

        Returns:
            Interval: cos(self)

        """
        inf, sup = self.minTrigo().inf, self.minTrigo().sup
        pi_fois_2 = fmul(2, mp.pi)
        pi_fois_3 = fmul(3, mp.pi)
        if inf <= mp.pi:
            if sup <= mp.pi:
                return Interval(cos(sup, rounding='d'), cos(inf, rounding='u'))
            if mp.pi < sup <= pi_fois_2:
                return Interval(-1, max(cos(inf, rounding='u'),
                                        cos(sup, rounding='u')))
            if sup > pi_fois_2:
                return Interval(-1, 1)
        if mp.pi < inf <= pi_fois_2:
            if sup <= pi_fois_2:
                return Interval(cos(inf, rounding='d'), cos(sup, rounding='u'))
            if pi_fois_2 < sup <= pi_fois_3:
                return Interval(min(cos(inf, rounding='d'),
                                    cos(sup, rounding='u')), 1)
            if sup >= pi_fois_3:
                return Interval(-1, 1)

    def sin(self):
        """Function sin

        Return the sinus of an Interval.
        We use the identity sin(x) = cos(pi/2 - x)

        Args:
            self (Interval): operand

        Returns:
            Interval: sin(self)

        """
        return (-self + float(mp.pi / 2)).cos()  # TODO supprimer le float

    def tan(self):
        """Function tan

        Return the tangent of an Interval.
        We use the identity tan(x) = sin(x)/cos(x).

        Args:
            self (Interval): operand

        Returns:
            Interval: tan(self)

        """
        return self.sin() / self.cos()

    def cotan(self):
        """Function cotan

        Return the cotangent of an Interval.
        We use the identity cotan(x) = cos(x)/sin(x).

        Args:
            self (Interval): operand

        Returns:
            Interval: cotan(self)

        """
        return self.cos() / self.sin()

    def toAffine(self):
        """Method toAffine

        Convert an interval form to an affine form

        Args:
            self (Interval): operand

        Returns:
            Affine: associated to the interval
        """
        return AffApy.affineArithmetic.Affine(interval=[self.inf, self.sup])
