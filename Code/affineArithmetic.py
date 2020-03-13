from intervalArithmetic import Interval

class Affine:
    def __init__(self, xi):
        self.xi = xi # liste
        self.xsi = sum([abs(i) for i in xi[1:]])
        self.interval = Interval(xi[0] + self.xsi, xi[0] - self.xsi)

    def __add__(self, other):
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
        if isinstance(other, self.__class__):
            xi = []
            for x in self.xi:
                for y in other.xi:
                    xi.append(x*y)
            return Affine(xi)
        elif isinstance(other, int) or isinstance(other, float):
            xi = [other*self.xi[0]]
            xi += [other*i for i in self.xi[1:]]
            return Affine(xi)
        print("Error : unknown type")
        return None

    def __str__(self):
        string = str(self.xi[0])
        compteur = 1
        for i in self.xi[1:]:
            string += " + " + str(i) + "*eps" + str(compteur)
            compteur += 1
        return string

    def __eq__(self, other):
        """
        Operator == 
        : type other: Affine
        : rtype: bool
        """
        return self.xi==other.xi and self.xsi==other.xsi and self.interval==other.interval

    def __ne__(self, other):
        """
        Operator ==
        : type pther: Affine
        : rtype: bool
        """
        return self.xi!=other.xi and self.xsi!=other.xsi and self.interval!=other.interval

    def __ge__(self, other):
        """
        Operator <=
        : type other: 
        """
        return super().__ge__(value)

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
    z1 = Affine([5, 15, 5])
    print(z!=z1)
    print(z)
    print(z.interval)
    x1 = Affine([3 / 2, 1 / 2])
    x2 = Affine([7 / 2, 1 / 2])
    x3 = x1*x2
    print(x3)
    print(x3.interval)
    print((x + 3.2).interval)