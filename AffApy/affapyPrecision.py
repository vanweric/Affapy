from collections import deque
from mpmath import mp
from contextlib import ContextDecorator


class precision(ContextDecorator):
    """Manage precision for AffApy Library"""
    _precisionStack = deque()

    def __enter__(self, bin_prec=0, dec_prec=0):
        """
        
        :param bin_prec: int for binary precision of mpmath
        :param dec_prec: float for decimal precision of mpmath
        :return:
        """
        precision._precisionStack.append(mp.dps)
        if dec_prec:
            mp.dps = dec_prec
        elif bin_prec:
            mp.prec = bin_prec
        else:
            mp.dps = 0
        return self

    def __exit__(self, *exc):
        if precision._precisionStack:
            mp.dps = precision._precisionStack.pop()
        else:
            mp.dps = 0
        return False

    # Getter
    @property
    def precisionDec(self):
        """ Return decimal precision """
        return mp.dps

    @property
    def precisionBin(self):
        """ Return binary precision """
        return mp.prec

    # Setter
    @precisionDec.setter
    def precisionDec(self, dec_prec):
        """ Set decimal precision """
        mp.dps = dec_prec

    @precisionDec.setter
    def precisionBin(self, bin_prec):
        """ Set binary precision """
        mp.prec = bin_prec

    @staticmethod
    def getOldPrecision():
        """ Return Older decimal precision """
        if precision._precisionStack:
            return precision._precisionStack[-1]
        else:
            return 0
