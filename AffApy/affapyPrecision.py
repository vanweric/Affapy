from contextlib import ContextDecorator
from mpmath import mp
from AffApy.affapyError import AffApyError


class precision(ContextDecorator):
    """Manage precision for AffApy library"""
    def __init__(self, dec_precision=None, bin_precision=None):
        """
        Init the context manager for precision.
        You need to mention dec_prec or bin_prec. Both is useless.

        Args:
            dec_precision (int): decimal precision of mpmath
            bin_precision (int): binary precision of mpmath

        """
        self._dec = dec_precision
        self._bin = bin_precision
        self._old_dec = None
        self._old_bin = None

    # Getter
    @property
    def dec_precision(self):
        """Get decimal precision"""
        return self._dec

    @property
    def bin_precision(self):
        """Get binary precision"""
        return self._bin

    @property
    def old_dec_precision(self):
        """Get old decimal precision"""
        return self._old_dec

    @property
    def old_bin_precision(self):
        """Get old binary precision"""
        return self._old_bin

    # Setter
    @dec_precision.setter
    def dec_precision(self, value):
        """Set decimal precision"""
        self._dec = value
        mp.dps = self._dec

    @bin_precision.setter
    def bin_precision(self, value):
        """Set binary precision"""
        self._bin = value
        mp.prec = self._bin

    @old_dec_precision.setter
    def old_dec_precision(self, value):
        """Set old decimal value"""
        self._old_dec = value

    @old_bin_precision.setter
    def old_bin_precision(self, value):
        """Set old binary value"""
        self._old_bin = value

    # Static Method - If you want to modify directly the precision
    @staticmethod
    def set_dec_precision(dec_precision):
        """Set decimal precision outside precision class"""
        mp.dps = dec_precision

    @staticmethod
    def set_bin_precision(bin_precision):
        """Set binary precision outside precision class"""
        mp.prec = bin_precision

    # functions for with statement
    def __enter__(self):
        """
        Set the mpmath precision for a portion of code

        Raises:
            AffApyError: No precision mentionned

        """
        self.old_dec_precision, self.old_bin_precision = mp.dps, mp.prec
        if self.dec_precision is not None:
            mp.dps = self.dec_precision
        elif self.bin_precision is not None:
            mp.prec = self.bin_precision
        else:
            raise AffApyError("No precision mentionned")

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
