"""Error module"""
import warnings


class AffApyError(Exception):
    """Manage exception errors"""
    pass


class AffApyWarning(UserWarning):
    pass


if __name__ == "__main__":
    warnings.warn('Message warning', AffApyWarning)
