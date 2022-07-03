# Built-in/Generic Imports
import logging

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
__version__ = "0.6"
__maintainer__ = "IncognitoCoding"
__status__ = "Production"


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
