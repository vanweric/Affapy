"""Affine Arithmetic module"""
import AffApy.intervalArithmetic
from AffApy.affapyError import AffApyError
from mpmath import mp, fdiv, fadd, fsub, fsum, fabs, fneg, fmul, sqrt


class Affine:
    """Representation of an affine form"""
    _weightCount = 1

    def __init__(self, interval=None, x0=None, xi=None):
        """
        Two ways for init Affine:
        - Affine(interval=[inf, sup])
        - Affine(x0=0, xi={})
        If no arguments, x0=0 and xi={}
        """
        if interval and isinstance(interval, list) and len(interval) == 2:
            inf, sup = min(interval), max(interval)
            self._x0 = fdiv(fadd(inf, sup), 2)
            self._xi = {Affine._weightCount: fdiv(fsub(inf, sup), 2)}
            Affine._weightCount += 1
            self._interval = AffApy.intervalArithmetic.Interval(inf, sup)
        elif x0 and xi:
            self._x0 = mp.mpf(x0)
            self._xi = {i: mp.mpf(str(xi[i])) for i in xi}
            Affine._weightCount = max(xi) + 1
            self._interval = AffApy.intervalArithmetic.Interval(
                fadd(self._x0, self.rad()), fsub(self._x0, self.rad()))
        else:
            self._x0 = mp.mpf(0)
            self._xi = {}
            self._interval = AffApy.intervalArithmetic.Interval(0, 0)

    # Getter
    @property
    def x0(self):
        """Return x0"""
        return self._x0

    @property
    def xi(self):
        """Return xi"""
        return self._xi

    @property
    def interval(self):
        """Return interval"""
        return self._interval

    # Setter
    @x0.setter
    def x0(self, value):
        """Set x0"""
        self._x0 = value

    @xi.setter
    def xi(self, value):
        """Set xi"""
        self._xi = value

    @interval.setter
    def interval(self, value):
        """Set interval"""
        self._interval = value

    def rad(self):
        """
        Return the radius of affine form
        :rtype: int or float
        """
        return fsum(fabs(self.xi[i]) for i in self.xi)

    # Unary operator
    def __neg__(self):
        """
        Operator - (unary)
        :rtype: Affine
        """
        x0 = fneg(self.x0)
        xi = {i: fneg(self.xi[i]) for i in self.xi}
        return Affine(x0=x0, xi=xi)

    # Affine operations
    def __add__(self, other):
        """
        Operator +
        :type other: Affine or int or float
        :rtype: Affine
        """
        if isinstance(other, self.__class__):
            x0 = fadd(self.x0, other.x0)
            xi = {}
            for i in self.xi:
                if i in other.xi:
                    val = fadd(self.xi[i], other.xi[i])
                    if val != 0:
                        xi[i] = val
                else:
                    xi[i] = self.xi[i]
            for i in other.xi:
                if i not in self.xi:
                    xi[i] = other.xi[i]
            return Affine(x0=x0, xi=xi)
        if isinstance(other, int) or isinstance(other, float):
            x0 = fadd(self.x0, mp.mpf(str(other)))
            xi = self.xi.copy()
            return Affine(x0=x0, xi=xi)
        raise AffApyError("type error : other must be Affine, int or float")

    def __radd__(self, other):
        """
        Reverse operator + : other + self
        :type other: Affine or int or float
        :rtype: Affine
        """
        return self + other

    def __sub__(self, other):
        """
        Operator -
        :type other: Affine or int or float
        :rtype: Affine
        """
        if isinstance(other, self.__class__):
            x0 = fsub(self.x0, other.x0)
            xi = {}
            for i in self.xi:
                if i in other.xi:
                    val = fsub(self.xi[i], other.xi[i])
                    if val != 0:
                        xi[i] = val
                else:
                    xi[i] = self.xi[i]
            for i in other.xi:
                if i not in self.xi:
                    xi[i] = fneg(other.xi[i])
            return Affine(x0=x0, xi=xi)
        if isinstance(other, int) or isinstance(other, float):
            x0 = fsub(self.x0, mp.mpf(str(other)))
            xi = self.xi.copy()
            return Affine(x0=x0, xi=xi)
        raise AffApyError("type error : other must be Affine, int or float")

    def __rsub__(self, other):
        """
        Reverse operator - : other - self
        :type other: Affine or int or float
        :rtype: Affine
        """
        return -self + other

    def __mul__(self, other):
        """
        Operator *
        :type other: Affine or int or float
        :rtype: Affine
        """
        if isinstance(other, self.__class__):
            x0 = fmul(self.x0, other.x0)
            xi = {}
            if self.xi == {} and other.xi != {}:
                keyMax = max(other.xi)
            elif self.xi != {} and other.xi == {}:
                keyMax = max(self.xi)
            elif self.xi != {} and other.xi != {}:
                keyMax = max(max(self.xi), max(other.xi))
            else:
                keyMax = 0
            for i in range(keyMax + 1):
                v = 0
                if i in self.xi and i not in other.xi:
                    v = fmul(self.xi[i], other.x0)
                elif i not in self.xi and i in other.xi:
                    v = fmul(other.xi[i], self.x0)
                elif i in self.xi and i in other.xi:
                    v = fadd(fmul(self.xi[i], other.x0),
                             fmul(other.xi[i], self.x0))
                if v != 0:
                    xi[i] = v
            xi[Affine._weightCount] = fmul(self.rad(), other.rad())
            Affine._weightCount += 1
            return Affine(x0=x0, xi=xi)
        if isinstance(other, int) or isinstance(other, float):
            x0 = fmul(mp.mpf(str(other)), self.x0)
            xi = {i: fmul(mp.mpf(str(other)), self.xi[i]) for i in self.xi}
            return Affine(x0=x0, xi=xi)
        raise AffApyError("type error : other must be Affine, int or float")

    def __rmul__(self, other):
        """
        Reverse operator * : other*self
        :type other: Affine or int or float
        :rtype: Affine
        """
        return self * other

    # Non-affine operations
    def affineConstructor(self, alpha, dzeta, delta):
        """
        Return the affine form for non-affine operations
        :rtype: Affine
        """
        x0 = fadd(fmul(alpha, self.x0), dzeta)
        xi = {i: fmul(alpha, self.xi[i]) for i in self.xi}
        xi[Affine._weightCount] = delta
        Affine._weightCount += 1
        return Affine(x0=x0, xi=xi)

    def inv(self):
        """
        Inverse of an affine form
        :rtype: Affine
        """
        if 0 not in self.interval:
            inf, sup = self.interval.inf, self.interval.sup
            a, b = min(abs(inf), abs(sup)), max(abs(inf), abs(sup))
            alpha = fdiv(fneg(1), fmul(b, b))
            i = AffApy.intervalArithmetic.Interval(fsub(fdiv(1, a),
                                                   fmul(alpha, a)), fdiv(2, b))
            dzeta = i.middle()
            if inf < 0:
                dzeta = fneg(dzeta)
            delta = i.radius()
            return self.affineConstructor(alpha, dzeta, delta)
        raise AffApyError(
            "the interval associated to the affine form contains 0")

    def __truediv__(self, other):
        """
        Operator /
        :type other: Affine
        :rtype: Affine
        """
        if isinstance(other, self.__class__):
            return self * other.inv()
        raise AffApy("only / between two affine forms")

    def __pow__(self, n):
        """
        Operator **
        :type other: int or float
        :rtype: Affine
        """
        return (n * self.log(self)).exp()

    # Methods
    def __abs__(self):  # TODO
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
        if self.interval >= 0:
            a, b = self.interval.inf, self.interval.sup
            t = fadd(sqrt(a), sqrt(b))
            alpha = fdiv(1, t)
            dzeta = fadd(fdiv(t, 8), fdiv(fmul(0.5, sqrt(fmul(a, b))), t))
            rdelta = fsub(sqrt(b), sqrt(a))
            delta = fdiv(fmul(rdelta, rdelta), fmul(8, t))
            return self.affineConstructor(alpha, dzeta, delta)
        raise AffApyError(
            "the interval associated to the affine form must be >= 0")

    def exp(self):  # TODO
        """
        Return the exponential of an affine form
        :rtype: Affine
        """
        pass

    def log(self):  # TODO
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
        x = self + mp.mpf(mp.pi / 2)
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
        return " + ".join(
            [str(self.x0)] +
            ["".join([str(self.xi[i]), "*eps", str(i)]) for i in self.xi])

    def __repr__(self):
        """
        Make the repr format
        :rtype: string
        """
        return "Affine({}, {})".format(self.x0, self.xi)

    # Inclusion
    def __contains__(self, other):
        """
        Operator in
        :type other: Affine or int or float
        :rtype: bool
        """
        int1 = self.toInterval()
        if isinstance(other, self.__class__):
            int2 = other.toInterval()
            return int2 in int1
        if isinstance(other, AffApy.intervalArithmetic.Interval):
            return other in int1
        if isinstance(other, int) or isinstance(other, float):
            return other in int1
        raise AffApyError("type error")
