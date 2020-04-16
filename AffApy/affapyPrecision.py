from collections import deque
from mpmath import mp
from contextlib import ContextDecorator


class precision(ContextDecorator):
    """Manage precision for AffApy Library"""
    _precisionStack = deque()

    def __enter__(self, dec_prec=0, bin_prec=0):
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

    @staticmethod
    def getActualDecPrecision():
        return mp.dps

    @staticmethod
    def getActualBinPrecision():
        return mp.prec

    @staticmethod
    def setActualDecPrecision(dec_prec):
        mp.dps = dec_prec

    @staticmethod
    def setActualBinPrecision(bin_prec):
        mp.prec = bin_prec

    @staticmethod
    def getOlderPrecision():
        if precision._precisionStack:
            return precision._precisionStack[-1]
        else:
            return 0
