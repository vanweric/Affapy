"""Use of precision module: decorators"""
from affapy.precision import precision
from mpmath import mp


@precision(dps=50)
def test_dps_precision():
    print("Decimal precision during function:", mp.dps)
    print("Pi =", mp.pi)
    print("End of function")


@precision(prec=60)
def test_prec_precision():
    print("Binary precision during function:", mp.prec)
    print("Pi =", mp.pi)
    print("End of function")


if __name__ == "__main__":
    precision.set_dps(dps=20)

    print("Decimal precision before function:", mp.dps)
    test_dps_precision()
    print("Decimal precision after function:", mp.dps, "\n")

    precision.set_prec(prec=50)
    print("Binary precision before function:", mp.prec)
    test_prec_precision()
    print("Binary precision after function:", mp.prec, "\n")

    print("Decimal precision before with statement:", mp.dps)
    with precision(dps=10):
        print("Decimal precision during with statement:", mp.dps)
        print("Pi =", mp.pi, "\n")

        print("Decimal precision during with statement before function:",
              mp.dps, "\n")
        test_dps_precision()
        print("Decimal precision during with statement after function:",
              mp.dps, "\n")

    print("Decimal precision after with statement:", mp.dps)
