"""
Example 4
---------

**Comparison AA vs IA**

We consider the function:

.. math::
    \\frac{sin(x)^2 cos(x) - 4}{\\sqrt{x}}

We consider the interval [lbound, ubound] (default: [1, 6])
and a subdivision of this interval containing n boxes (default: 12).
The function is evaluated for each box with AA and IA.
The result is plotted using matplotlib.

Usage:

.. code-block:: bash

    python3 example4.py [lbound] [ubound] [boxn]

* lbound: lower bound of the interval (default: 1)
* ubound: upper bound of the interval (default: 6)
* boxn: number of boxes (default: 12)

You need to install *matplotlib* and *numpy* to run this example.

.. image:: example4.png

Output of example 4

"""
from affapy.ia import Interval
from affapy.aa import Affine
import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

pts = 500


def eval_fct_pt(x):
    return (np.sin(x)**2*np.cos(x) - 4) / np.sqrt(x)


def eval_fct_aa(x):
    return (x.sin()**2*x.cos() - 4) / x.sqrt()


if __name__ == "__main__":
    if len(sys.argv) == 1:
        lbound = 1
        ubound = 6
        boxn = 12

    elif len(sys.argv) != 4:
        print("Usage:", sys.argv[0])
        print("LOWER_BOUND UPPER_BOUND BOXN")
        exit()

    else:
        lbound = float(sys.argv[1])     # lower bound of the interval
        ubound = float(sys.argv[2])     # upper bound of the interval
        boxn = int(sys.argv[3])         # number of boxes

        if lbound > ubound:
            print("The lower bound must be smaller than the upper bound!")
            exit()

    width = (ubound - lbound) / boxn    # width of a box

    x = np.linspace(lbound, ubound, pts)
    y = eval_fct_pt(x)

    fig, ax = plt.subplots(1)

    plt.plot(x, y, linewidth=2, label='f')

    for i in range(boxn):
        x1 = lbound + i*width
        x2 = x1 + width
        xc = (x1 + x2) / 2

        # AA
        u = Affine([x1, x2])
        v = eval_fct_aa(u)

        itv = v.interval
        rect = Rectangle((x1, itv.inf), width, itv.width(),
                         alpha=0.2, linewidth=2, color='r')
        ax.add_patch(rect)

        # IA
        u = Interval(x1, x2)
        v = eval_fct_aa(u)
        rect = Rectangle((x1, v.inf), width, v.width(),
                         alpha=0.2, linewidth=2, color='y')
        ax.add_patch(rect)

    plt.title('Affine Arithmetic representation')
    plt.grid(True)
    plt.legend()
    plt.show()
