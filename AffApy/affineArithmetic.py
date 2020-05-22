"""Affine Arithmetic module

This module can create affines form and perform operations.

Affine Arithmetic (AA) has been developed to overcome the error explosion
problem of standard Interval Arithmetic.
This method represents a quantity x as an affine form x', which is a first
degree polynomial:

            x' = x0 + x1e1 + x2e2 + · · · + xnen

The xi coefficient are finite floating-point numbers.
x0 is the central value of the affine form x' and xi are it's partial
deviation.
The ei coefficients are real values called noise symbol. Their values are
unknown between [0,1].
This representation enables a better tracking of the different quantities
inside the affine form.

For example, the quantitie [0, 10] can be represented as the following affine
form:

        A = [0, 10] = 5 + 5e1   where x0 = 1 and x1 = 5

But we could also represent it like this :

        B = [0, 10] = 5 + 3e1 + 2e2     where x0 = 5, x1 = 3 and x2 = 2

Both form represent the same quantity but they are handling differently the
storage of internal quantities.
They will behave differently during operation:

        A - A = 0,  no surprises here  (1)

        A - B = 0 + 2e1 - 2e2 = [0, 4]  (2)

Example (2) illustrate this behaviour. Even though A and B represent the
same quantity, they manage their quantity
differently, they are therefore not equal.
"""
import AffApy.intervalArithmetic
from AffApy.affapyError import AffApyError
import mpmath
from mpmath import (
    mp, fdiv, fadd, fsub, fsum, fneg, fmul, fabs, sqrt, exp, log, sin)


class Affine:
    """Representation of an affine form"""
    _weightCount = 3

    @staticmethod
    def getNewXi():
        Affine._weightCount += 1
        return Affine._weightCount - 1

    def __init__(self, interval=None, x0=None, xi=None):
        """Init an Affine form

        Create an Affine form. Two different ways:
        Affine(interval=[inf, sup]) or Affine(x0=0, xi={}).
        If no arguments, x0=0 and xi={}.

        Args:
            interval (list or tuple with length 2 or Interval): the interval
            x0 (int or float or mpf): the center
            xi (dict of mpf values): noise symbols

        Returns:
            Affine

        Raises:
            AffApyError: if interval is not list, tuple or Interval

        """
        if interval is not None:
            if isinstance(interval, (list, tuple)) and len(interval) == 2:
                inf, sup = min(interval), max(interval)
            elif isinstance(interval, AffApy.intervalArithmetic.Interval):
                inf, sup = interval.inf, interval.sup
            else:
                raise AffApyError("interval must be list, tuple or Interval")
            self._x0 = (inf + sup) / 2
            self._xi = {Affine.getNewXi(): fdiv(
                fsub(inf, sup, rounding='c'), 2, rounding='c')}
            self._interval = AffApy.intervalArithmetic.Interval(inf, sup)
        elif x0 is not None and xi is not None:
            self._x0 = mp.mpf(x0)
            self._xi = {i: mp.mpf(xi[i], rounding='c') for i in xi}
            self._interval = AffApy.intervalArithmetic.Interval(
                fadd(self._x0, self.rad(), rounding='d'),
                fsub(self._x0, self.rad(), rounding='u'))
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
        return self._xi.copy()

    @property
    def interval(self):
        """Return interval"""
        return self._interval.copy()

    # Setter
    @x0.setter
    def x0(self, val):
        """Set x0"""
        self._x0 = mp.mpf(val)
        self._interval = self.convert()

    @xi.setter
    def xi(self, val):
        """Set xi"""
        self._xi = {i: mp.mpf(val[i], rounding='c') for i in val}
        self._interval = self.convert()

    def rad(self):
        """Radius

        Return the radius of affine form.

        Args:
            self (Affine): operand

        Returns:
            mpf: sum of abs(xi)

        """
        return fsum(self.xi.values(), absolute=True)

    def straddles_zero(self):
        """
        Return True if the affine form straddles 0, False if not.

        Args:
            self (Affine): operand

        Returns:
            bool: 0 in self

        """
        return self.interval.straddles_zero()

    def strictly_neg(self):
        """
        Return True if the affine is strictly negative, False if not.

        Args:
            self (Affine): operand

        Returns:
            bool: 0 in self

        """
        return self.interval < 0

    # Unary operator
    def __neg__(self):
        """Operator - (unary)

        Return the additive inverse of an Affine form.

        Args:
            self (Affine): operand

        Returns:
            Affine: -self

        Examples:
            >>> print(-Affine([1, 2]))
            -1.5 + 0.5e1

        """
        x0 = fneg(self.x0)
        xi = {i: fneg(self.xi[i], rounding='c') for i in self.xi}
        return Affine(x0=x0, xi=xi)

    # Affine operations
    def __add__(self, other):
        """Operator +

        Add two Affines or an Affine form and an integer or float or mpf.

        Args:
            self (Affine): first operand
            other (Affine or int or float or mpf): second operand

        Returns:
            Affine: self + other

        Raises:
            AffApyError: if other is not Affine, int, float, mpf

        Examples:
            >>> print(Affine([0, 1]) + Affine([3, 4]))
            4.0 + -0.5e1 + -0.5e2

        """
        if isinstance(other, self.__class__):
            x0 = self.x0 + other.x0
            xi = {}
            for i in self.xi:
                if i in other.xi:
                    val = fadd(self.xi[i], other.xi[i], rounding='c')
                    if val != 0:
                        xi[i] = val
                else:
                    xi[i] = self.xi[i]
            for i in other.xi:
                if i not in self.xi:
                    xi[i] = other.xi[i]
            return Affine(x0=x0, xi=xi)
        if isinstance(other, (int, float, mpmath.mpf)):
            x0 = self.x0 + mp.mpf(other)
            xi = self.xi.copy()
            return Affine(x0=x0, xi=xi)
        raise AffApyError("other must be Affine, int, float, mpf")

    def __radd__(self, other):
        """Reverse operator +

        Add two Affines or an Affine form and an integer or float or mpf.

        Args:
            self (Affine): second operand
            other (Affine or int or float or mpf): first operand

        Returns:
            Affine: other + self

        Raises:
            AffApyError: if other is not Affine, int, float, mpf

        """
        return self + other

    def __sub__(self, other):
        """Operator -

        Substract two Affines or an Affine form and an integer or float or mpf.

        Args:
            self (Affine): first operand
            other (Affine or int or float): second operand

        Returns:
            Affine: self - other

        Raises:
            AffApyError: if other is not Affine, int, float, mpf

        """
        if isinstance(other, self.__class__):
            x0 = self.x0 - other.x0
            xi = {}
            for i in self.xi:
                if i in other.xi:
                    val = fsub(self.xi[i], other.xi[i], rounding='c')
                    if val != 0:
                        xi[i] = val
                else:
                    xi[i] = self.xi[i]
            for i in other.xi:
                if i not in self.xi:
                    xi[i] = fneg(other.xi[i], rounding='c')
            return Affine(x0=x0, xi=xi)
        if isinstance(other, (int, float, mpmath.mpf)):
            x0 = self.x0 - mp.mpf(other)
            xi = self.xi.copy()
            return Affine(x0=x0, xi=xi)
        raise AffApyError("other must be Affine, int, float, mpf")

    def __rsub__(self, other):
        """Reverse operator -

        Substract two Affines or an integer or float or mpf and an Affine form.

        Args:
            self (Affine): second operand
            other (Affine or int or float or mpf): first operand

        Returns:
            Affine: other - self

        Raises:
            AffApyError: if other is not Affine, int, float, mpf

        """
        return -self + other

    def __mul__(self, other):
        """Operator *

        Multiply two Affines or an Affine form and integer or float or mpf.

        Args:
            self (Affine): first operand
            other (Affine or int or float or mpf): second operand

        Returns:
            Affine: self * other

        Raises:
            AffApyError: if other is not Affine, int, float, mpf

        """
        if isinstance(other, self.__class__):
            x0 = self.x0 * other.x0
            xi = {}
            keyMax = max(max(self.xi) if self.xi else 0,
                         max(other.xi) if other.xi else 0)
            for i in range(keyMax + 1):
                v = 0
                if i in self.xi and i not in other.xi:
                    v = fmul(self.xi[i], other.x0, rounding='c')
                elif i not in self.xi and i in other.xi:
                    v = fmul(other.xi[i], self.x0, rounding='c')
                elif i in self.xi and i in other.xi:
                    v = fadd(fmul(self.xi[i], other.x0, rounding='c'),
                             fmul(other.xi[i], self.x0, rounding='c'),
                             rounding='c')
                if v != 0:
                    xi[i] = v
            xi[Affine.getNewXi()] = fmul(self.rad(), other.rad(), rounding='c')
            return Affine(x0=x0, xi=xi)
        if isinstance(other, (int, float, mpmath.mpf)):
            x0 = mp.mpf(other) * self.x0
            xi = {i: fmul(mp.mpf(other),
                          self.xi[i], rounding='c') for i in self.xi}
            return Affine(x0=x0, xi=xi)
        raise AffApyError("other must be Affine, int, float, mpf")

    def __rmul__(self, other):
        """Reverse operator *

        Multiply two Affines or an integer or float or mpf and an Affine form.

        Args:
            self (Affine): second operand
            other (Affine or int or float or mpf): first operand

        Returns:
            Affine: other * self

        Raises:
            AffApyError: if other is not Affine, int, float, mpf

        """
        return self * other

    # Non-affine operations
    def _affineConstructor(self, alpha, dzeta, delta):
        """Affine constructor

        Return the affine form for non-affine operations.

        Args:
            alpha (mpmath.mpf)
            dzeta (mpmath.mpf)
            delta (mpmath.mpf)

        Returns:
            Affine

        """
        x0 = alpha * self.x0 + dzeta
        xi = {i: fmul(alpha, self.xi[i], rounding='c') for i in self.xi}
        xi[Affine.getNewXi()] = delta
        return Affine(x0=x0, xi=xi)

    def inv(self):
        """Inverse of an affine form

        Return the inverse of an Affine form.

        Args:
            self: operand

        Returns:
            Affine: 1 / self

        Raises:
            AffApyError: if the interval associated to the affine form
            contains 0

        """
        if 0 not in self.interval:
            inf, sup = self.interval.inf, self.interval.sup
            a, b = min(fabs(inf), fabs(sup)), max(fabs(inf), fabs(sup))
            alpha = -1 / (b * b)
            i = AffApy.intervalArithmetic.Interval(
                fsub(fdiv(1, a), fmul(alpha, a), rounding='d'),
                fdiv(2, b, rounding='u'))
            dzeta = i.mid()
            if inf < 0:
                dzeta = -dzeta
            delta = i.radius()
            return self._affineConstructor(alpha, dzeta, delta)
        raise AffApyError(
            "the interval associated to the affine form contains 0")

    def __truediv__(self, other):
        """Operator /

        Divide two Affines or an integer or float or mpf and an Affine form.
        We use the identity x/y = x * (1/y).

        Args:
            self (Affine): first operand
            other (Affine or int or float or mpf): second operand

        Returns:
            Affine: self / other

        Raises:
            AffApyError: if other is not Affine, int, float, mpf

        """
        if isinstance(other, self.__class__):
            return self * other.inv()
        if isinstance(other, (int, float, mpmath.mpf)):
            return self * (1 / other)
        raise AffApyError("other must be Affine, int, float, mpf")

    def __rtruediv__(self, other):
        """Reverse operator /

        Divide two Affines or an Affine form and an integer or float or mpf.
        We use the identity x/y = x * (1/y).

        Args:
            self (Affine): second operand
            other (Affine or int or float or mpf): first operand

        Returns:
            Affine: other / self

        Raises:
            AffApyError: if other is not Affine, int, float, mpf

        """
        if (isinstance(other, self.__class__) or
                isinstance(other, (int, float, mpmath.mpf))):
            return other * self.inv()
        raise AffApyError("other must be Affine, int, float, mpf")

    def sqr(self):
        """
        Return the square of the affine form.

        Args:
            self (Affine): operand

        Returns:
            Affine: self ** 2

        """
        return self * self

    def __pow__(self, n):
        """Operator **

        Return the power of an Affine with another Affine or an integer.
        With Affine, we use the identity : x**n = exp(n * log(x)).

        Args:
            self (Affine): first operand
            n (Affine or int): second operand (exponent)

        Returns:
            Affine: self ** n

        Raises:
            AffApyError: if n is not Affine or int

        """
        if isinstance(n, int):
            if n < 0:
                x = self.inv()
                n = -n
            if n == 0:
                return 1
            y = 1
            x = self.copy()
            while n > 1:
                if n % 2 == 0:
                    x = x * x
                    n = n / 2
                else:
                    y = x * y
                    x = x * x
                    n = (n - 1) / 2
            return x * y
        elif isinstance(n, self.__class__):
            return (n * self.log()).exp()
        raise AffApyError("type error: n must be Affine or int")

    # Functions
    def __abs__(self):
        """
        Return the absolute value of an affine form.
        Args:
            self (Affine): operand

        Returns:
            Affine: abs(self)
        """
        if self.strictly_neg():
            return -self
        if self.straddles_zero():
            x0 = fabs(self.x0 / 2)
            xi = {i: fdiv(self.xi[i], 2, rounding='c') for i in self.xi}
            return Affine(x0=x0, xi=xi)
        return self.copy()

    def sqrt(self):
        """Function sqrt

        Return the square root of an affine form.

        Args:
            self (Affine): operand

        Returns:
            Affine: sqrt(self)

        Raises:
            AffApyError: the interval associated to the affine form
            must be >= 0

        """
        if self.interval >= 0:
            a, b = self.interval.inf, self.interval.sup
            t = fadd(sqrt(a), sqrt(b), rounding='f')
            alpha = fdiv(1, t)
            dzeta = fadd(fdiv(t, 8), fmul(0.5, fdiv(sqrt(fmul(a, b)), t)))
            rdelta = fsub(sqrt(b), sqrt(a), rounding='c')
            delta = fdiv(fmul(rdelta, rdelta, rounding='c'),
                         fmul(8, t, rounding='f'), rounding='c')
            return self._affineConstructor(alpha, dzeta, delta)
        raise AffApyError(
            "the interval associated to the affine form must be >= 0")

    def exp(self):
        """Function exp

        Return the exponential of an affine form.

        Args:
            self (Affine): operand

        Returns:
            Affine: exp(self)

        """
        a, b = self.interval.inf, self.interval.sup
        ea, eb = exp(a), exp(b)
        alpha = fdiv(fsub(eb, ea), fsub(b, a))
        xs = log(alpha)
        maxdelta = fadd(fmul(alpha, fsub(xs, fsub(1, a))), ea)
        dzeta = fmul(alpha, fsub(1, xs))
        delta = fdiv(maxdelta, 2)
        return self._affineConstructor(alpha, dzeta, delta)

    def log(self):
        """Function log

        Return the logarithm of an affine form.

        Args:
            self (Affine): operand

        Returns:
            Affine: log(self)

        Raises:
            AffApyError: the interval associated to the affine form must be > 0

        """
        if self.interval > 0:
            a, b = self.interval.inf, self.interval.sup
            la, lb = log(a), log(b)
            alpha = fdiv(fsub(lb, la), fsub(b, a))
            xs = fdiv(1, alpha)
            ys = fadd(fmul(alpha, fsub(xs, a)), la)
            maxdelta = fsub(log(xs), ys)
            dzeta = fdiv(fmul(alpha, fneg(xs)), fdiv(fadd(log(xs), ys), 2))
            delta = fdiv(maxdelta, 2)
            return self._affineConstructor(alpha, dzeta, delta)
        raise AffApyError(
            "the interval associated to the affine form must be > 0")

    # Trigo
    def sin(self, npts=8):
        """Function sin

        Return the sinus of an affine form.
        It uses the least squares.

        Args:
            self (Affine): operand
            npts (int): number of points for the linear regression
            approximation

        Returns:
            Affine: sin(self)

        """
        w = self.interval.width()
        a, b = self.interval.inf, self.interval.sup
        if w >= 2 * mp.pi:
            return Affine(interval=[-1, 1])
        # Case of the least squares
        x, y = [a], [sin(a)]
        pas = w / (npts - 1)
        for i in range(1, npts - 1):
            x.append(x[i - 1] + pas)
            y.append(sin(x[i]))
        x.append(b)
        y.append(sin(b))
        # Calculation of xm and ym, averages of x and y
        xm, ym = fsum(x) / npts, fsum(y) / npts
        # Calculation of alpha and dzeta
        temp2 = 0
        alpha = 0
        for xi, yi in zip(x, y):
            temp1 = xi - xm
            alpha += yi * temp1
            temp2 += temp1 * temp1
        alpha = alpha / temp2
        dzeta = ym - alpha * xm
        # Calculation of the residues
        r = [fabs(yi - (dzeta + alpha * xi)) for xi, yi in zip(x, y)]
        # The error delta is the maximum of the residues (in absolute values)
        delta = max(r)
        return self._affineConstructor(alpha, dzeta, delta)

    def cos(self):
        """Function cos

        Return the cosinus of an affine form.
        We use the identity cos(x) = sin(x + PI/2).

        Args:
            self (Affine): operand

        Returns:
            Affine: cos(self)

        """
        return (self + mp.pi / 2).sin()

    def tan(self):
        """Function tan

        Return the tangent of an affine form.
        We use the identity tan(x) = sin(x)/cos(x).

        Args:
            self (Affine): operand

        Returns:
            Affine: tan(self)

        """
        return self.sin() / self.cos()

    def cotan(self):
        """Function cotan

        Return the cotangent of an affine form.
        We use the identity cotan(x) = cos(x)/sin(x).

        Args:
            self (Affine): operand

        Returns:
            Affine: cotan(self)

        """
        return self.cos() / self.sin()

    def cosh(self):
        """Function cosh

        Return the hyperbolic cosine of an affine form.
        We use the identity cosh(x) = (exp(x) + exp(-x))/2.

        Args:
            self (Affine): operand

        Returns:
            Affine: cosh(self)

        """
        return (self.exp() + (-self).exp()) * 0.5

    def sinh(self):
        """Function sinh

        Return the hyperbolic sine of an affine form.
        We use the identity sinh(x) = (exp(x) - exp(-x))/2.

        Args:
            self (Affine): operand

        Returns:
            Affine: sinh(self)

        """
        return (self.exp() - (-self).exp()) * 0.5

    def tanh(self):
        """Function tanh

        Return the hyperbolic tangeant of an affine form.
        We use the identity tanh(x) = sinh(x)/cosh(x)

        Args:
            self (Affine): operand

        Returns:
            Affine: tanh(self)

        """
        return self.sinh() / self.cosh()

    # Comparison operators
    def __eq__(self, other):
        """Operator ==

        Compare two Affine forms.

        Args:
            self (Affine): first operand
            other (Affine): second operand

        Returns:
            bool: self == other

        """
        return self.x0 == other.x0 and self.xi == other.xi

    def __ne__(self, other):
        """Operator !=

        Negative comparison of two Affine forms.

        Args:
            self (Affine): first operand
            other (Affine): second operand

        Returns:
            bool: self != other

        """
        return self.x0 != other.x0 or self.xi != other.xi

    # Inclusion
    def __contains__(self, other):
        """Operator in

        Return True if the interval of self is in the interval of other.

        Args:
            self (Affine): first operand
            other (Affine): second operand

        Returns:
            bool: self in other

        Raises:
            AffApyError: if other is not Affine, Interval, int, float, mpf

        """
        if isinstance(other, self.__class__):
            return other.interval in self.interval
        if isinstance(other, AffApy.intervalArithmetic.Interval):
            return other in self.interval
        if isinstance(other, (int, float, mpmath.mpf)):
            return other in self.interval
        raise AffApyError("other must be Affine, Interval, int, float, mpf")

    # Formats
    def __str__(self):
        """String format

        Make the string format.

        Args:
            self (Affine): arg

        Returns:
            string: sum of noise symbols

        Examples:
            >>> print(Affine([1, 2]))
            1.5 - 0.5*e1

        """
        return " + ".join(
            [str(self.x0)] +
            ["".join([str(self.xi[i]), "e", str(i)]) for i in self.xi])

    def __repr__(self):
        """Repr format

        Make the repr format.

        Args:
            self (Affine): arg

        Returns:
            string: format

        """
        return "Affine({}, {})".format(self.x0, self.xi)

    def copy(self):
        """
        Copy the affine form.

        Args:
            self (Affine): arg

        Returns:
            Affine: self copy

        """
        return Affine(x0=self.x0, xi=self.xi.copy())

    def convert(self):
        """
        Convert an affine form to an interval representation.

        Args:
            self (Affine): arg

        Returns:
            Interval: interval of self

        """
        return AffApy.intervalArithmetic.Interval(self.x0 - self.rad(),
                                                  self.x0 + self.rad())
