# Built-in/Generic Imports
import logging

from typing import Union, Any

# Libraries
from fchecker.type import type_check

# Local Functions
from ..helpers.py_helper import get_function_name

# Exceptions
from fexception import FGeneralError, FTypeError, FValueError

__author__ = "IncognitoCoding"
__copyright__ = "Copyright 2022, common"
__credits__ = ["IncognitoCoding"]
__license__ = "MIT"
__version__ = "0.2"
__maintainer__ = "IncognitoCoding"
__status__ = "Production"


def str_to_list(value: Union[str, list], sep: str) -> list[Any]:
    """
    Take any string and converts it based on the separator.\\
    The difference between this function and .split() is this function\\
    allows the ability to convert single values or multiple values to a list.

    Ideal for converting database cells that were converted from\\
    list to str for storage. Ex: .join('my_list_values')

    Whitespace is stripped from the start or end.

    Usage Notes:
    \t\\- If a list is sent the original list will forward.\\
    \t\\- If the separator never matches the entry will be considered\\
    \t   a single entry and add to the list.

    Args:
        value (Union[str, list]):
        \t\\- The string getting split.
        \t\\- A list will forward through.
        sep (str):
        \t\\- The delimiter that will split the string.

    Raises:
        FTypeError (fexception):
        \t\\- The object value '{value}' is not an instance of the required class(es) or subclass(es).
        FGeneralError:
        \t\\- A general failure occurred while converting the string to list.

    Returns:
        list[Any]:
        \t\\- A converted string to a list or the original forwarded list.
        \t\\- Empty lists can pass through.
    """
    logger = logging.getLogger(__name__)
    logger.debug(f"=" * 20 + get_function_name() + "=" * 20)
    # Custom flowchart tracking. This is ideal for large projects that move a lot.
    # For any third-party modules, set the flow before making the function call.
    logger_flowchart = logging.getLogger("flowchart")
    logger_flowchart.debug(f"Flowchart --> Function: {get_function_name()}")

    try:
        type_check(value=value, required_type=(str, list))
    except FTypeError:
        raise

    if isinstance(value, str):
        formatted_value = f"  - string (str):\n        - {value}\n"
    else:
        formatted_value = "  - value (list):" + str("\n        - " + "\n        - ".join(map(str, value)))
    logger.debug("Passing parameters:\n" f"{formatted_value}\n")

    try:
        new_list: list = []
        if isinstance(value, str):
            # Converts if the delimiter is in the value.
            if sep in str(value):
                new_list = str(value.strip()).split(sep)
            else:
                new_list.append(value.strip())
        else:
            new_list = value
    except FTypeError as exc:  # pragma: no cover
        raise
    except Exception as exc:  # pragma: no cover
        exc_args = {
            "main_message": "A general failure occurred while converting the string to list.",
            "original_exception": exc,
        }
        raise FGeneralError(exc_args)
    else:
        return new_list


def common_case_isupper(list_of_strings: list[str]) -> bool:
    """
    Checks if the common case of the strings in the list is upper case.

    Upper case will will a tie.

    Args:
        list_of_strings (list[str]):
        \t\\- A list of strings.

    Raises:
        FValueError:
        \t\\- Unexpected upper_count vs lower_count match.
        FGeneralError:
        \t\\- A general failure occurred while getting the common case.

    Returns:
        bool:
        \t\\- True if the common case is upper.
        \t\\- False if the common case is lower.
    """
    logger = logging.getLogger(__name__)
    logger.debug(f"=" * 20 + get_function_name() + "=" * 20)
    # Custom flowchart tracking. This is ideal for large projects that move a lot.
    # For any third-party modules, set the flow before making the function call.
    logger_flowchart = logging.getLogger("flowchart")
    logger_flowchart.debug(f"Flowchart --> Function: {get_function_name()}")

    try:
        type_check(value=list_of_strings, required_type=list)
    except FTypeError:
        raise

    formatted_list_of_strings = "  - list_of_strings (list):" + str(
        "\n        - " + "\n        - ".join(map(str, list_of_strings))
    )
    logger.debug("Passing parameters:\n" f"{formatted_list_of_strings}\n")

    try:
        upper_count: int = 0
        lower_count: int = 0
        # Loops through every string in the list to check for common case
        # (ex: A or a) to determine sort.
        for string in list_of_strings:
            # Checks the case and increases count.
            if string.isupper():
                upper_count += 1
            elif string.islower():
                lower_count += 1
        # Checks the difference between the upper and lower count to determine
        # the sort based on the common case. Tie goes to Upper.
        if upper_count > lower_count:
            return True
        elif lower_count > upper_count:
            return False
        elif upper_count == lower_count:
            return True
        else:
            exc_args = {
                "main_message": "Unexpected upper_count vs lower_count match.",
                "returned_result": [f"upper_count = {upper_count}", f"lower_count = {lower_count}"],
            }
            raise FValueError(exc_args)
    except Exception as exc:  # pragma: no cover
        exc_args = {
            "main_message": "A general failure occurred while getting the common case.",
            "original_exception": exc,
        }
        raise FGeneralError(exc_args)


def common_case_islower(list_of_strings: list[str]) -> bool:
    """
    Checks if the common case of the strings in the list is lower case.

    Upper case will will a tie.

    Args:
        list_of_strings (list[str]):\
        \t\\- A list of strings.

    Raises:
        FValueError:
        \t\\- Unexpected upper_count vs lower_count match.
        FGeneralError:
        \t\\- A general failure occurred while getting the common case.

    Returns:
        bool:
        \t\\- True if the common case is lower.
        \t\\- False if the common case is upper.
    """
    logger = logging.getLogger(__name__)
    logger.debug(f"=" * 20 + get_function_name() + "=" * 20)
    # Custom flowchart tracking. This is ideal for large projects that move a lot.
    # For any third-party modules, set the flow before making the function call.
    logger_flowchart = logging.getLogger("flowchart")
    logger_flowchart.debug(f"Flowchart --> Function: {get_function_name()}")

    try:
        type_check(value=list_of_strings, required_type=list)
    except FTypeError:
        raise

    formatted_list_of_strings = "  - list_of_strings (list):" + str(
        "\n        - " + "\n        - ".join(map(str, list_of_strings))
    )
    logger.debug("Passing parameters:\n" f"{formatted_list_of_strings}\n")

    try:
        upper_count: int = 0
        lower_count: int = 0
        # Loops through every string in the list to check for common case
        # (ex: A or a) to determine sort.
        for string in list_of_strings:
            # Checks the case and increases count.
            if string.isupper():
                upper_count += 1
            elif string.islower():
                lower_count += 1
        # Checks the difference between the upper and lower count to determine
        # the sort based on the common case. Tie goes to Upper.
        if upper_count > lower_count:
            return False
        elif lower_count > upper_count:
            return True
        elif upper_count == lower_count:
            return False
        else:
            exc_args = {
                "main_message": "Unexpected upper_count vs lower_count match.",
                "returned_result": [f"upper_count = {upper_count}", f"lower_count = {lower_count}"],
            }
            raise FValueError(exc_args)
    except Exception as exc:  # pragma: no cover
        exc_args = {
            "main_message": "A general failure occurred while getting the common case.",
            "original_exception": exc,
        }
        raise FGeneralError(exc_args)


def dict_keys_upper(my_dict: dict[str, Any]) -> dict[str, Any]:
    """
    Converts all dictionary keys to upper case.

    Args:
        my_dict (dict[str, Any]):
        \t\\- The dictionary needing the keys converted.

    Raises:
        FGeneralError:
        \t\\- A general failure occurred while converting the dictionary keys to upper case.

    Returns:
        dict[str, Any]:
        \t\\- The original dictionary with upper case keys.
    """
    logger = logging.getLogger(__name__)
    logger.debug(f"=" * 20 + get_function_name() + "=" * 20)
    # Custom flowchart tracking. This is ideal for large projects that move a lot.
    # For any third-party modules, set the flow before making the function call.
    logger_flowchart = logging.getLogger("flowchart")
    logger_flowchart.debug(f"Flowchart --> Function: {get_function_name()}")

    try:
        type_check(value=my_dict, required_type=dict)
    except FTypeError:
        raise

    formatted_my_dict = "  - my_dict (dict):\n        - " + "\n        - ".join(
        ": ".join((key, str(val))) for (key, val) in my_dict.items()
    )
    logger.debug("Passing parameters:\n" f"{formatted_my_dict}\n")

    try:
        res = dict()
        for key in my_dict.keys():
            if isinstance(my_dict[key], dict):
                res[key.upper()] = dict_keys_upper(my_dict[key])
            else:
                res[key.upper()] = my_dict[key]
        return res
    except Exception as exc:  # pragma: no cover
        exc_args = {
            "main_message": "A general failure occurred while converting the dictionary keys to upper case.",
            "original_exception": exc,
        }
        raise FGeneralError(exc_args)


def dict_keys_lower(my_dict: dict[str, Any]) -> dict[str, Any]:
    """
    Converts all dictionary keys to lower case.

    Args:
        my_dict (dict[str, Any]):
        \t\\- The dictionary needing the keys converted.

    Raises:
        FGeneralError:
        \t\\- A general failure occurred while converting the dictionary keys to lower case.

    Returns:
        dict[str, Any]:
        \t\\- The original dictionary with lower case keys.
    """
    logger = logging.getLogger(__name__)
    logger.debug(f"=" * 20 + get_function_name() + "=" * 20)
    # Custom flowchart tracking. This is ideal for large projects that move a lot.
    # For any third-party modules, set the flow before making the function call.
    logger_flowchart = logging.getLogger("flowchart")
    logger_flowchart.debug(f"Flowchart --> Function: {get_function_name()}")

    try:
        type_check(value=my_dict, required_type=dict)
    except FTypeError:
        raise

    formatted_my_dict = "  - my_dict (dict):\n        - " + "\n        - ".join(
        ": ".join((key, str(val))) for (key, val) in my_dict.items()
    )
    logger.debug("Passing parameters:\n" f"{formatted_my_dict}\n")

    try:
        res = dict()
        for key in my_dict.keys():
            if isinstance(my_dict[key], dict):
                res[key.lower()] = dict_keys_lower(my_dict[key])
            else:
                res[key.lower()] = my_dict[key]
        return res
    except Exception as exc:  # pragma: no cover
        exc_args = {
            "main_message": "A general failure occurred while converting the dictionary keys to lower case.",
            "original_exception": exc,
        }
        raise FGeneralError(exc_args)
