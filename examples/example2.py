"""
Example 2
---------

**Time performances between AA and IA model**

This example shows the time performances between AA and IA.
It permorms calculations on the following function:

.. math::
    x_1, x_2 \\mapsto 1 + (x_1^2 - 2)x_2 + x_1x_2^2

The result of this example is that AA is slower than IA.

Usage:

.. code-block:: bash

    python3 example5.py [lbound1] [ubound1] [lbound2] [ubound2] [boxn]

* lbound1: lower bound of the interval 1 (default: 10)
* ubound1: upper bound of the interval 1 (default: 100)
* lbound2: lower bound of the interval 2 (default: 10)
* ubound2: upper bound of the interval 2 (default: 100)
* boxn: number of boxes (default: 1000)

"""
from affapy.ia import Interval
from affapy.aa import Affine
from time import time
import sys


def eval_fct(x1, x2):
    return 1 + (x1*x1 - 2)*x2 + x1*x2*x2


if __name__ == "__main__":
    if len(sys.argv) == 1:
        lbound1 = 10
        ubound1 = 100
        lbound2 = 10
        ubound2 = 100
        boxn = 1000

    elif len(sys.argv) != 6:
        print("Usage:", sys.argv[0])
        print("LOWER_BOUND1 UPPER_BOUND1 LOWER_BOUND2 UPPER_BOUND2 BOXN")
        exit()

    else:
        # interval of x1
        lbound1 = float(sys.argv[1])
        ubound1 = float(sys.argv[2])

        # interval of x2
        lbound2 = float(sys.argv[3])
        ubound2 = float(sys.argv[4])

        # number of boxes
        boxn = int(sys.argv[5])

    if lbound1 > ubound1 or lbound2 > ubound2:
        print("The lower bound must be smaller than the upper bound!")
        exit()

    width1 = (ubound1 - lbound1) / boxn
    width2 = (ubound2 - lbound2) / boxn

    print("Time performances between AA and IA models")

    # AA
    tstart1 = time()

    for i in range(boxn):
        # x1
        x1_a = lbound1 + i * width1
        x1_b = x1_a + width1
        itv1 = Interval(x1_a, x1_b)
        u1 = Affine(itv1)

        # x2
        x2_a = lbound2 + i * width2
        x2_b = x2_a + width2
        itv2 = Interval(x2_a, x2_b)
        u2 = Affine(itv2)

        v = eval_fct(u1, u2)

        ydelta = v.rad()
        y = v.x0

    tstop1 = time()

    total1 = tstop1 - tstart1
    print(f"AA: ydelta = {ydelta}, y = {y}")

    # IA
    tstart2 = time()

    for i in range(boxn):
        # x1
        x1_a = lbound1 + i * width1
        x1_b = x1_a + width1
        m1 = Interval(x1_a, x1_b)

        # x2
        x2_a = lbound2 + i * width2
        x2_b = x2_a + width2
        m2 = Interval(x2_a, x2_b)

        n = eval_fct(m1, m2)

        y = n.mid()
        ydelta = n.sup - y

    tstop2 = time()

    total2 = tstop2 - tstart2
    print(f"IA: ydelta = {ydelta}, y = {y}")

    print("AA:", total1, "s")
    print("IA:", total2, "s")
