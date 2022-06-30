# Built-in/Generic Imports
import logging

from typing import Union, Any

# Libraries
from fchecker.type import type_check

# Local Functions
from ..helpers.py_helper import get_function_name

# Exceptions
from fexception import FValueError

__author__ = "IncognitoCoding"
__copyright__ = "Copyright 2022, common"
__credits__ = ["IncognitoCoding"]
__license__ = "MIT"
__version__ = "0.5"
__maintainer__ = "IncognitoCoding"
__status__ = "Production"


def str_to_list(value: Union[str, list], sep: str) -> list[Any]:
    """
    Take any string and converts it based on the separator.\\
    The difference between this function and .split() is this function\\
    allows the ability to convert single values or multiple values to a list.

    Ideal for converting database cells that were converted from\\
    list to str for storage. Ex: .join('my_list_values') or list_to_str(value=[1,2])

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

    type_check(value=value, required_type=(str, list), tb_remove_name="str_to_list")

    if isinstance(value, str):
        formatted_value = f"  - string (str):\n        - {value}\n"
    else:
        formatted_value = "  - value (list):" + str("\n        - " + "\n        - ".join(map(str, value)))
    logger.debug("Passing parameters:\n" f"{formatted_value}\n")

    new_list: list = []
    if isinstance(value, str):
        # Converts if the delimiter is in the value.
        if sep in str(value):
            new_list = str(value.strip()).split(sep)
        else:
            new_list.append(value.strip())
    else:
        new_list = value

    return new_list


def list_to_str(value: Union[str, list], sep: str = " ") -> str:
    """
    Take any list and converts the list to a string.\\

    Usage Notes:
    \t\\- If str is sent the original str will forward.\\

    Args:
        value (Union[str, list]):
        \t\\- The list getting converted.
        \t\\- A str will forward through.
        sep (str, optional):
        \t\\- The delimiter that will separate each list entry.
        \t\\- Blanks are supported.
        \t\\- Defaults to a single blank space.

    Raises:
        FTypeError (fexception):
        \t\\- The object value '{value}' is not an instance of the required class(es) or subclass(es).

    Returns:
        str:
        \t\\- A converted list to a string or the original forwarded list.
    """
    logger = logging.getLogger(__name__)
    logger.debug(f"=" * 20 + get_function_name() + "=" * 20)
    # Custom flowchart tracking. This is ideal for large projects that move a lot.
    # For any third-party modules, set the flow before making the function call.
    logger_flowchart = logging.getLogger("flowchart")
    logger_flowchart.debug(f"Flowchart --> Function: {get_function_name()}")

    type_check(value=value, required_type=(str, list), tb_remove_name="list_to_str")

    formatted_value = "  - value (list):" + str("\n        - " + "\n        - ".join(map(str, value)))
    logger.debug("Passing parameters:\n" f"{formatted_value}\n")

    if isinstance(value, list):
        new_list = sep.join(map(str, value))
    else:
        new_list = value

    return new_list


def common_case_isupper(list_of_strings: list[str]) -> bool:
    """
    Checks if the common case of the strings in the list is upper case.

    Upper case will will a tie.

    Args:
        list_of_strings (list[str]):
        \t\\- A list of strings.

    Raises:
        FTypeError (fexception):
        \t\\- The object value '{list_of_strings}' is not an instance of the required class(es) or subclass(es).
        FValueError:
        \t\\- Unexpected upper_count vs lower_count match.

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

    type_check(value=list_of_strings, required_type=list, tb_remove_name="common_case_isupper")

    formatted_list_of_strings = "  - list_of_strings (list):" + str(
        "\n        - " + "\n        - ".join(map(str, list_of_strings))
    )
    logger.debug("Passing parameters:\n" f"{formatted_list_of_strings}\n")

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
        raise FValueError(message_args=exc_args)


def common_case_islower(list_of_strings: list[str]) -> bool:
    """
    Checks if the common case of the strings in the list is lower case.

    Upper case will will a tie.

    Args:
        list_of_strings (list[str]):\
        \t\\- A list of strings.

    Raises:
        FTypeError (fexception):
        \t\\- The object value '{list_of_strings}' is not an instance of the required class(es) or subclass(es).
        FValueError:
        \t\\- Unexpected upper_count vs lower_count match.

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

    type_check(value=list_of_strings, required_type=list, tb_remove_name="common_case_islower")

    formatted_list_of_strings = "  - list_of_strings (list):" + str(
        "\n        - " + "\n        - ".join(map(str, list_of_strings))
    )
    logger.debug("Passing parameters:\n" f"{formatted_list_of_strings}\n")

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
        raise FValueError(message_args=exc_args)


def dict_keys_upper(my_dict: dict[str, Any]) -> dict[str, Any]:
    """
    Converts all dictionary keys to upper case.

    Args:
        my_dict (dict[str, Any]):
        \t\\- The dictionary needing the keys converted.

    Raises:
        FTypeError (fexception):
        \t\\- The object value '{my_dict}' is not an instance of the required class(es) or subclass(es).

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

    type_check(value=my_dict, required_type=dict, tb_remove_name="dict_keys_upper")

    formatted_my_dict = "  - my_dict (dict):\n        - " + "\n        - ".join(
        ": ".join((key, str(val))) for (key, val) in my_dict.items()
    )
    logger.debug("Passing parameters:\n" f"{formatted_my_dict}\n")

    res = dict()
    for key in my_dict.keys():
        if isinstance(my_dict[key], dict):
            res[key.upper()] = dict_keys_upper(my_dict[key])
        else:
            res[key.upper()] = my_dict[key]
    return res


def dict_keys_lower(my_dict: dict[str, Any]) -> dict[str, Any]:
    """
    Converts all dictionary keys to lower case.

    Args:
        my_dict (dict[str, Any]):
        \t\\- The dictionary needing the keys converted.

    Raises:
        FTypeError (fexception):
        \t\\- The object value '{my_dict}' is not an instance of the required class(es) or subclass(es).

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

    type_check(value=my_dict, required_type=dict, tb_remove_name="dict_keys_lower")

    formatted_my_dict = "  - my_dict (dict):\n        - " + "\n        - ".join(
        ": ".join((key, str(val))) for (key, val) in my_dict.items()
    )
    logger.debug("Passing parameters:\n" f"{formatted_my_dict}\n")

    res = dict()
    for key in my_dict.keys():
        if isinstance(my_dict[key], dict):
            res[key.lower()] = dict_keys_lower(my_dict[key])
        else:
            res[key.lower()] = my_dict[key]
    return res
