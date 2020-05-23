from affapy.parametrize import parametrize

from mpmath import mp


@parametrize(precision={"dps": 10, "prec": 20},
             test_1=1, test_2=2)
def test_parametrize():
    print("Decimal precision during function:", mp.dps)
    print("\tPi =", mp.pi)
    print("End of function")


@parametrize(precision=["test", 30, 40, 50])
def test_parametrize2():
    print("Decimal precision during function 2:", mp.dps)
    print("\tPi =", mp.pi)
    print("End of function")


if __name__ == "__main__":
    with parametrize(precision=80):
        print("Decimal precision during with:", mp.dps)
        print("\tPi =", mp.pi)
    print("Decimal precision after with:", mp.dps)
    print("\tPi =", mp.pi)
    test_parametrize()
    test_parametrize2()
    print("Decimal precision after functions:", mp.dps)
    print("\tPi =", mp.pi)
