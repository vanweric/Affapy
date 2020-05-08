from contextlib import ContextDecorator
from mpmath import mp

from AffApy.affapyError import AffApyError


class precision(ContextDecorator):
    """Manage precision for AffApy library"""
    _dec: int
    _bin: int
    _old_dec: int
    _old_bin: int

    def __init__(self, dec_precision: int = None, bin_precision: int = None):
        """
        Init the context manager for precision.
        You need to mention dec_prec or bin_prec. Both is useless.

        Args:
            dec_precision (int): decimal precision of mpmath
            bin_precision (int): binary precision of mpmath

        """
        if isinstance(dec_precision, int) or isinstance(bin_precision, int):
            self._dec = dec_precision
            self._bin = bin_precision
        else:
            raise AffApyError("Invalid value for precision")
        self._old_dec = None
        self._old_bin = None

    # Getter
    @property
    def dec_precision(self):
        """
        Get decimal precision

        :rtype int
        """
        return self._dec

    @property
    def bin_precision(self):
        """
        Get binary precision

        :rtype int
        """
        return self._bin

    @property
    def old_dec_precision(self):
        """Get old decimal precision

        :rtype int
        """
        return self._old_dec

    @property
    def old_bin_precision(self):
        """
        Get old binary precision

        :rtype int
        """
        return self._old_bin

    # Setter
    @dec_precision.setter
    def dec_precision(self, dec_precision: int):
        """
        Set decimal precision
        
        :type dec_precision: int
        """
        self._dec = dec_precision
        mp.dps = self._dec

    @bin_precision.setter
    def bin_precision(self, bin_precision: int):
        """
        Set binary precision

        :type bin_precision: int
        """
        self._bin = bin_precision
        mp.prec = self._bin

    @old_dec_precision.setter
    def old_dec_precision(self, dec_precision: int):
        """
        Set old decimal value

        :type dec_precision: int
        """
        self._old_dec = dec_precision

    @old_bin_precision.setter
    def old_bin_precision(self, bin_precision: int):
        """
        Set old binary value

        :type bin_precision: int
        """
        self._old_bin = bin_precision

    # Static Method - If you want to modify directly the precision
    @staticmethod
    def set_dec_precision(dec_precision: int):
        """
        Set decimal precision outside precision class
        
        :type dec_precision: int
        """
        mp.dps = dec_precision

    @staticmethod
    def set_bin_precision(bin_precision: int):
        """
        Set binary precision outside precision class

        :type bin_precision: int
        """
        mp.prec = bin_precision

    # functions for with statement
    def __enter__(self):
        """
        Set the mpmath precision for a portion of code

        Raises:
            AffApyError: No precision mentioned

        """
        self.old_dec_precision, self.old_bin_precision = mp.dps, mp.prec
        if self.dec_precision is not None:
            mp.dps = self.dec_precision
        elif self.bin_precision is not None:
            mp.prec = self.bin_precision
        else:
            raise AffApyError("No precision mentioned")

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Reset the mpmath precision to its last value

        Raises:
            AffApyError: No precision saved

        """
        if self.dec_precision is not None:
            mp.dps = self.old_dec_precision
        elif self.bin_precision is not None:
            mp.prec = self.old_bin_precision
        else:
            raise AffApyError("No precision saved")
        return False
