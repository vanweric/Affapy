from mpmath import mp

from AffApy.affapyParametrize import parametrize


@parametrize(precision={"dec_precision": 10, "bin_precision": 20}, test_1=1, test_2=1)
def test_parametrize():
    print("Decimal precision during function:", mp.dps)
    print("Pi =", mp.pi)
    print("End of function")


@parametrize(precision=["test", 30, 40, 50])
def test_parametrize2():
    print("Decimal precision during function 2:", mp.dps)
    print("Pi =", mp.pi)
    print("End of function")


if __name__ == "__main__":
    with parametrize(precision=50):
        print("Decimal precision during with:", mp.dps)
        print("Pi =", mp.pi)
    print("Decimal precision after with:", mp.dps)
    print("Pi =", mp.pi)
    test_parametrize()
    test_parametrize2()
    print("Decimal precision after functions:", mp.dps)
    print("Pi =", mp.pi)
