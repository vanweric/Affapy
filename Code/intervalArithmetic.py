import numpy as np

class Interval:
    """Representation of an interval"""
    def __init__(self, inf, sup):
        """
        :type inf: float or int
        :type sup: float or int
        """
        if inf < sup:
            self.inf = inf
            self.sup = sup
        else:
            self.inf = sup
            self.sup = inf

    # Inclusion
    def __contains__(self, other):
        """
        Operator in
        :type other: Interval or int or float
        :rtype: bool
        """
        if isinstance(other, self.__class__):
            return self.inf <= other.inf and self.sup >= other.sup
        elif isinstance(other, int) or isinstance(other, float):
            return self.inf <= other and self.sup >= other
        print("Error : unknown type")
        return None

    # Binary operators
    def __add__(self, other):
        """
        Operator +
        :type other: Interval or int or float
        :rtype: Interval
        """
        if isinstance(other, self.__class__):
            inf = self.inf + other.inf
            sup = self.sup + other.sup
            return Interval(inf, sup)
        elif isinstance(other, int) or isinstance(other, float):
            inf = self.inf + other
            sup = self.sup + other
            return Interval(inf, sup)
        print("Error : unknown type")
        return None

    def __sub__(self, other):
        """
        Operator -
        :type other: Interval or int or float
        :rtype: Interval
        """
        if isinstance(other, self.__class__):
            inf = self.inf - other.sup
            sup = self.sup - other.inf
            return Interval(inf, sup)
        elif isinstance(other, int) or isinstance(other, float):
            inf = self.inf - other
            sup = self.sup - other
            return Interval(inf, sup)
        print("Error : unknown type")
        return None

    def __mul__(self, other):
        """
        Operator *
        :type other: Interval
        :rtype: Interval
        """
        a, b = self.inf, self.sup
        c, d = other.inf, other.sup
        inf = min([a*c, a*d, b*c, b*d])
        sup = max([a*c, a*d, b*c, b*d])
        return Interval(inf, sup)

    def __truediv__(self, other):
        """
        Operator /
        :type other: Interval
        :rtype: Interval
        """
        c, d = other.inf, other.sup
        if not 0 in other:
            return self * Interval(1 / d, 1 / c)
        print("Error : division by 0")

    def __pow__(self, n):
        """
        Operator **
        :type other: Interval
        :type n: int
        :rtype: Interval
        """
        if n == 2:
            inf, sup = self.inf, self.sup
            if not 0 in self:
                return Interval(min(inf**n, sup**n), max(inf**n, sup**n))
            else:
                return Interval(0, max(inf**n, sup**n))
        print("Error : only power 2 accepted for the moment")

    # Unary operator
    def __neg__(self):
        """
        Operator - (unary)
        :type other: Interval
        :rtype: Interval
        """
        return Interval(-self.sup, -self.inf)

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

    def __ge__(self, n):
        """
        Operator >=
        :type other: int or float
        :rtype: bool
        """
        return self.inf >= n

    def __gt__(self, n):
        """
        Operator >
        :type other: int or float
        :rtype: bool
        """
        return self.inf > n

    def __le__(self, n):
        """
        Operator <=
        :type other: int or float
        :rtype: bool
        """
        return self.sup <= n

    def __lt__(self, n):
        """
        Operator <
        :type other: int or float
        :rtype: bool
        """
        return self.sup < n

    # String form  
    def __str__(self):
        """
        Make the string format
        :rtype: string
        """
        return "[" + str(self.inf) + " ; " + str(self.sup) + "]"

    # Methods
    def rad(self):
        """
        Return the radius of the interval
        :rtype: int or float
        """
        return self.sup - self.inf

    def middle(self):
        """
        Return the middle of the interval
        :rtype: float
        """
        return (self.inf + self.sup) / 2

    def log(self):
        return Interval(np.log(self.inf), np.log(self.sup))

    def exp(self): 
        return Interval(np.exp(self.inf), np.exp(self.sup))

    def sqrt(self):
        if 0 <= self.inf:
            return Interval(np.sqrt(self.inf), np.sqrt(self.sup))
        print("Error : inf must be >= 0")
        return None


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
    print(x / z)
    print(z * (x + y))
    print(y**2)
    print(z**2)
    print(x**3)
    print(x**2 + y**2 - x * y)
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
    print(x.rad())
    print(z.rad())
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
    print(x2**2)
    print(x2 * (y2 + z2))
    print(x2 * y2 + x2 * z2)
    print(x2 * (y2 + z2) in x2 * y2 + x2 * z2)