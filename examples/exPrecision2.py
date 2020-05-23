"""Use of precision module 2"""
from affapy.precision import precision
from mpmath import mp


@precision(dec_precision=20)
def test_dps_precision():
    print("Decimal precision during function:", mp.dps)
    print("Pi =", mp.pi)
    print("End of function")


@precision(bin_precision=60)
def test_prec_precision():
    print("Binary precision during function:", mp.prec)
    print("Pi =", mp.pi)
    print("End of function")


if __name__ == "__main__":
    precision.set_dec_precision(dec_precision=50)

    print("Decimal precision before function:", mp.dps)
    test_dps_precision()
    print("Decimal precision after function:", mp.dps, "\n")

    print("Binary precision before function:", mp.prec)
    test_prec_precision()
    print("Binary precision after function:", mp.prec, "\n")

    print("Decimal precision before with statement:", mp.dps)
    with precision(dec_precision=10):
        print("\tDecimal precision during with statement:", mp.dps)
        print("\tPi =", mp.pi)

        print("\n\tDecimal precision during with statement before function:",
              mp.dps)
        test_dps_precision()
        print("\tDecimal precision during with statement after function:",
              mp.dps, "\n")

        print("\tDecimal precision before second with statement:", mp.dps)
        with precision(dec_precision=30):
            print("\t\tDecimal precision during second with statement:",
                  mp.dps)
            print("\t\tPi =", mp.pi)

            print("\n\t\tDecimal precision during second with statement before function:",
                  mp.dps)
            test_dps_precision()
            print("\t\tDecimal precision during second with statement after function:",
                  mp.dps)
            print("\t\tExit second with")

        print("\tDecimal precision after second with statement:", mp.dps)
        print("\tExit with (dps = 10)")

    print("Decimal precision after with statement:", mp.dps)
