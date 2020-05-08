import functools
import warnings
from typing import Dict

from AffApy.affapyError import AffApyError, AffApyWarning
from AffApy.affapyPrecision import precision


class parametrize:
    """Manage parameters for AffApy library"""
    _args: list
    _parameters: Dict[str, object]

    def __init__(self, **args):
        """
        Init the context manager.

        Args:
            args (dict) : Dictionary of parameters to set in this context

        UserWarnings:
            AffApyWarning: Parameter does not exist
            AffApyWarning: Invalid value for parameter

        """
        self._args = []
        self._parameters = {}

        for key, values in args.items():  # Select which parameters and which values are valid to store them
            try:
                eval(key + "(0)")
            except NameError:
                warnings.warn(f"Parameter does not exist -> parameter {key} will be drop", AffApyWarning)
                continue
            if type(values) not in [list, set, tuple, dict]:
                transformed_values = [values]
            elif type(values) is dict:
                transformed_values = [str(values).replace(":", "=").replace("'", "").replace("{", "").replace("}", "")]
            else:
                transformed_values = values
            for value in transformed_values:
                try:
                    if isinstance(value, str) and type(values) is not dict:
                        eval(key + "('" + str(value) + "')")
                    else:
                        eval(key + "(" + str(value) + ")")
                    self._args.append((key, value))
                except (NameError, AffApyError):
                    warnings.warn(
                        f"Invalid value for parameter -> value : {value} for parameter : {key} will be drop",
                        AffApyWarning)

    def __call__(self, func):
        """
        Set a list of parameters for a function

        Args:
            func : function to be decorated

        UserWarnings:
            AffApyWarning: No valid parameters

        """
        if self.args:
            @functools.wraps(func)
            def f(*args, **kwargs):
                for (key, value) in self.args:
                    param = eval(key + "(" + str(value) + ")")
                    with param:
                        func(*args, **kwargs)

            return f
        else:
            warnings.warn(f"No valid parameters -> function {func.__name__} will be executed with default parameters",
                          AffApyWarning)
            return func

    # Getter
    @property
    def args(self):
        """Get parameters name & value"""
        return self._args

    @property
    def parameters(self):
        """Get parameters as Python object"""
        return self._parameters

    # Setter
    @args.setter
    def args(self, args: dict):
        """
        Set parameters name & value
        
        :type args: dict
        """
        self._args = args

    @parameters.setter
    def parameters(self, parameters: Dict[str, object]):
        """
        Set parameters objects

        :type parameters: dict
        """
        self._parameters = parameters

    # functions for with statement
    def __enter__(self):
        """
        Set a list of parameter for a portion of code

        UserWarnings:
            AffApyWarning: Several values for parameter

        Raises:
            AffApyError: No valid parameters
            AffApyError: Invalid value for parameter

        """
        if self.args is None:
            raise AffApyError("No valid parameters")
        for key, value in self.args:
            if key in self.parameters:
                warnings.warn(
                    f"Several values for parameter -> parameter {key} will keep the value {self.parameters[key]}",
                    AffApyWarning)
            else:
                try:
                    if isinstance(value, str):
                        obj = eval(key + "('" + value + "')")
                    else:
                        obj = eval(key + "(" + str(value) + ")")
                    self.parameters[key] = obj
                    self.parameters[key].__enter__()
                    break
                except (NameError, AffApyError):
                    raise AffApyError("Invalid value for parameter")

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit the particular portion of code and reset its parameters to default"""
        for obj in self.parameters.values():
            try:
                obj.__exit__(None, None, None)
            finally:
                return False
