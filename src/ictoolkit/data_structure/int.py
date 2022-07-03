# Built-in/Generic Imports
import logging

# Libraries
from fchecker.type import type_check

# Local Functions
from ..helpers.py_helper import get_function_name

# Exceptions
from fexception import FValueError


__author__ = "IncognitoCoding"
__copyright__ = "Copyright 2022, int"
__credits__ = ["IncognitoCoding"]
__license__ = "MIT"
__version__ = "0.1"
__maintainer__ = "IncognitoCoding"
__status__ = "Production"


def char_count(value: str, character: str) -> int:
    """
    Counts the characters in value and returns the count of a specific character.

    Args:
        value (str):
        \t\\- The value.
        character (str):
        \t\\- The character to return the count.

    Raises:
        FTypeError (fexception):
        \t\\- The object value '{value}' is not an instance of the required class(es) or subclass(es).
        FTypeError (fexception):
        \t\\- The object value '{character}' is not an instance of the required class(es) or subclass(es).
        FValueError (fexception):
        \t\\- The 'character' value must contain only one character.

    Returns:
        int:
        \t\\- The return count of the character.
    """
    logger = logging.getLogger(__name__)
    logger.debug(f"=" * 20 + get_function_name() + "=" * 20)
    # Custom flowchart tracking. This is ideal for large projects that move a lot.
    # For any third-party modules, set the flow before making the function call.
    logger_flowchart = logging.getLogger("flowchart")
    logger_flowchart.debug(f"Flowchart --> Function: {get_function_name()}")

    type_check(value=value, required_type=str, tb_remove_name="char_count")
    type_check(value=character, required_type=str, tb_remove_name="char_count")

    # Checks that only one exclude character was sent.
    if len(character) >= 2:
        exc_args = {
            "main_message": "The 'character' value must contain only one character.",
            "expected_result": "1",
            "returned_result": len(character),
        }
        raise FValueError(message_args=exc_args, tb_remove_name="char_count")

    all_freq: dict = {}
    for char in value:
        if char in all_freq:
            all_freq[char] += 1
        else:
            all_freq[char] = 1

    if character in all_freq.keys():
        return all_freq[character]
    else:
        return 0
