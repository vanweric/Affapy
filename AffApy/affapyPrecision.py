from contextlib import ContextDecorator
from mpmath import mp
from AffApy.affapyError import AffApyError


class precision(ContextDecorator):
    """Manage precision for AffApy library"""
    def __init__(self, dps=None, prec=None):
        """
        Init the context manager for precision.
        You need to mention dps or prec. Both is useless.

        Args:
            dps (int): decimal precision of mpmath
            prec (int): binary precision of mpmath

        """
        self._dps = dps
        self._prec = prec
        self._old_dps = None
        self._old_prec = None

    # Getter
    @property
    def dps(self):
        """Get dps"""
        return self._dps

    @property
    def prec(self):
        """Get prec"""
        return self._prec

    @property
    def old_dps(self):
        """Get old dps"""
        return self._old_dps

    @property
    def old_prec(self):
        """Get old prec"""
        return self._old_prec

    # Setter
    @dps.setter
    def dps(self, value):
        """Set dps"""
        self._dps = value

    @prec.setter
    def prec(self, value):
        """Set prec"""
        self._prec = value

    @old_dps.setter
    def old_dps(self, value):
        """Set old dps"""
        self._old_dps = value

    @old_prec.setter
    def old_prec(self, value):
        """Set old prec"""
        self._old_prec = value

    def __enter__(self):
        """
        Set the mpmath precision for a portion of code

        Raises:
            AffApyError: No precision mentionned

        """
        self.old_dps, self.old_prec = mp.dps, mp.prec
        if self.dps is not None:
            mp.dps = self.dps
        elif self.prec is not None:
            mp.prec = self.prec
        else:
            raise AffApyError("No precision mentionned")

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Reset the mpmath precision to its last value

        Raises:
            AffApyError: No precision saved

        """
        if self.dps is not None:
            mp.dps = self.old_dps
        elif self.prec is not None:
            mp.prec = self.old_prec
        else:
            raise AffApyError("No precision saved")
