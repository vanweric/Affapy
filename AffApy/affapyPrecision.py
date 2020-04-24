from collections import deque
from contextlib import ContextDecorator
from mpmath import mp


class precision(ContextDecorator):
    """Manage precision for AffApy Library"""
    _precisionStack = deque()

    def __enter__(self, bin_prec=0, dec_prec=0):
        """
        Use to set the mpmath precision for a portion of code
        :type bin_prec: int
        :param bin_prec: binary precision of mpmath
        :type dec_prec: int
        :param dec_prec: int for decimal precision of mpmath
        """
        precision._precisionStack.append(mp.dps)
        if dec_prec:
            mp.dps = dec_prec
        elif bin_prec:
            mp.prec = bin_prec
        else:
            mp.dps = 0

    def __exit__(self, *exc):
        """
        Reset the mpmath precision to its last value
        :param exc:
        :rtype: bool
        :return: on error
        """
        if precision._precisionStack:
            mp.dps = precision._precisionStack.pop()
        else:
            mp.dps = 0
        return False

    # Getter
    @property
    def precisionDec(self):
        """
        Return decimal precision
        :rtype: int
        :return: decimal precision
        """
        return mp.dps

    @property
    def precisionBin(self):
        """
        Return binary precision
        :rtype: int
        :return: binary precision
        """
        return mp.prec

    # Setter
    @precisionDec.setter
    def precisionDec(self, dec_prec):
        """
        Set decimal precision
        :type dec_prec: int
        :param dec_prec: decimal precision
        """
        mp.dps = dec_prec

    @precisionDec.setter
    def precisionBin(self, bin_prec):
        """
        Set binary precision
        :type  bin_prec: int
        :param bin_prec: binary precision
        """
        mp.prec = bin_prec

    @staticmethod
    def getOldPrecision():
        """
        Return Older decimal precision
        :rtype: int
        :return: last decimal precision
        """
        if precision._precisionStack:
            return precision._precisionStack[-1]
        else:
            return 0
