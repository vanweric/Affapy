from collections import deque
from contextlib import ContextDecorator
from mpmath import mp


class precision(ContextDecorator):
    """Manage precision for AffApy Library"""
    _precisionStack = deque()

    def __enter__(self, bin_prec=0, dec_prec=0):
        """
        Use to set the mpmath precision for a portion of code

        Args:
            bin_prec (int): binary precision of mpmath
            dec_prec (int): decimal precision of mpmath

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

        Args:
            exc

        Returns:
            bool: on error

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

        Returns:
            int: decimal precision

        """
        return mp.dps

    @property
    def precisionBin(self):
        """
        Return binary precision

        Returns:
            int: binary precision

        """
        return mp.prec

    # Setter
    @precisionDec.setter
    def precisionDec(self, dec_prec):
        """
        Set decimal precision

        Args:
            dec_prec (int): decimal precision

        """
        mp.dps = dec_prec

    @precisionBin.setter
    def precisionBin(self, bin_prec):
        """
        Set binary precision

        Args:
            bin_prec (int): binary precision

        """
        mp.prec = bin_prec

    @staticmethod
    def getOldPrecision():
        """
        Return Older decimal precision

        Returns:
            int: last decimal precision

        """
        if precision._precisionStack:
            return precision._precisionStack[-1]
        else:
            return 0
