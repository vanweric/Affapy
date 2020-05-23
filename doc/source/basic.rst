Basic usage
===========

Affine Arithmetic
-----------------

With *affapy*, you can create affine forms and perform operations:

.. code-block:: python

    from affapy.aa import Affine

    # Init
    x = Affine([1, 2])
    y = Affine([3, 4])

    # Get the interval
    x.interval
    y.interval

    # Basic operations
    x + y
    x + 5
    x - y
    x - 5
    -x

    # Advanced operations
    x * y
    x * 2
    x / y
    2 / x
    x ** y
    x ** 3

    # Functions
    abs(x)
    x.sqrt()
    x.exp()
    x.log()

    # Trigonometry
    x.sin()
    x.cos()
    x.tan()
    x.cotan()
    x.cosh()
    x.sinh()
    x.tanh()

    # Comparisons
    x == y
    x != y
    x in y


Interval Arithmetic
-------------------

You can also create intervals and perform operations:

.. code-block:: python

    from affapy.ia import Interval

    # Init
    x = Interval(1, 2)
    y = Interval(3, 4)

The operators and the functions have the same syntax than Affine Arithmetic.
Nevertheless, there are other comparison operators for intervals:

.. code-block:: python

    # Comparisons
    x == y
    x != y
    x in y
    x >= y
    x > y
    x <= y
    x < y

Precicion context
-----------------

You can set the precision of your calculations with the module **precision**:

.. code-block:: python

    from affapy.precision import precision

    with precision(bin_prec=30):
        x + y

    @precision(bin_prec=30)
    def eval_fct(x, y):
        return x + y
