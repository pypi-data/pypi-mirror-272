from typing import Any
import json


def validate_type(variable: Any, expected_type: Any, variable_name: str) -> None:
    """
    Validates that the given variable is of the expected type or types.

    This function checks if the variable matches the expected type or any type in a tuple of expected types.
    It raises a TypeError if the variable does not match the expected type(s).

    Parameters:
        variable (Any): The variable to be checked.
        expected_type (Any): The expected type or a tuple of expected types.
        variable_name (str): The name of the variable, used in the error message to identify the variable.

    Raises:
        TypeError: If the variable is not of the expected type(s).

    Returns:
        None: This function does not return a value; it raises an exception if the type check fails.
    """

    if not isinstance(expected_type, tuple):
        expected_type = (expected_type,)

    expected_type_names = ', '.join(type_.__name__ for type_ in expected_type)

    if not any(isinstance(variable, type_) for type_ in expected_type):
        raise TypeError(
            f"{variable_name} must be of type '{expected_type_names}', but '{type(variable).__name__}' was provided")


def set_method_call(method):
    """
    Decorates a method to ensure it is properly registered and tracked within the builder's workflow.

    This decorator adds the method's name to a set that tracks method calls

    Parameters:
        method (function): The method to be decorated.

    Returns:
        function: The wrapped method with added functionality to register its call.

    Raises:
        None: This decorator does not raise exceptions by itself but ensures the method call is registered.
    """

    def wrapper(self, *args):
        self.method_calls.append(method.__name__)
        return method(self, *args)

    return wrapper


def parse_json(value):
    """
    Attempts to convert a string into a Python object by interpreting it as JSON.

    Args:
        value (str | Any): The value to attempt to convert. If the value is not a string,
                           it is returned directly without attempting conversion.

    Returns:
        Any: The Python object resulting from the JSON conversion if `value` is a valid JSON string.
             If the conversion fails due to a formatting error (ValueError), the original value is returned.
             If `value` is not a string, it is returned as is.
    """
    try:
        if isinstance(value, str):
            return json.loads(value)
        return value
    except ValueError:
        return value
