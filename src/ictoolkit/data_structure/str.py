# Built-in/Generic Imports
import re
import logging
from typing import Union

# Libraries
from fchecker.type import type_check

# Local Functions
from ..helpers.py_helper import get_function_name

# Exceptions
from fexception import FGeneralError, FTypeError, FValueError


__author__ = "IncognitoCoding"
__copyright__ = "Copyright 2022, str"
__credits__ = ["IncognitoCoding"]
__license__ = "MIT"
__version__ = "0.1"
__maintainer__ = "IncognitoCoding"
__status__ = "Production"


def find_longest_common_substring(string1: str, string2: str) -> Union[str, None]:
    """
    This function finds the longest substring between two different strings.

    Args:
        string1 (string):
        \t\\- string to compare against string2
        string2 (string):
        \t\\- string to compare against string1

    Raises:
        FTypeError (fexception):
        \t\\- The object value '{string1}' is not an instance of the required class(es) or subclass(es).
        FTypeError (fexception):
        \t\\- The object value '{string2}'' is not an instance of the required class(es) or subclass(es).
        FGeneralError (fexception):
        \t\\- A general exception occurred interating the two strings.

    Returns:
        str:\\
        \t\\- returns the string up to the point the characters no longer match.
    """
    logger = logging.getLogger(__name__)
    logger.debug(f"=" * 20 + get_function_name() + "=" * 20)
    # Custom flowchart tracking. This is ideal for large projects that move a lot.
    # For any third-party modules, set the flow before making the function call.
    logger_flowchart = logging.getLogger("flowchart")
    logger_flowchart.debug(f"Flowchart --> Function: {get_function_name()}")

    try:
        type_check(value=string1, required_type=str)
        type_check(value=string2, required_type=str)
    except FTypeError:
        raise

    logger.debug(
        "Passing parameters:\n"
        f"  - string1 (str):\n        - {string1}\n"
        f"  - string2 (str):\n        - {string2}\n"
    )

    def _iter():
        for a, b in zip(string1, string2):
            if a == b:
                yield a
            else:
                return

    try:
        if "".join(_iter()):
            substring = "".join(_iter())
        else:
            substring = None
    except Exception as exc:  # pragma: no cover
        exc_args = {
            "main_message": "A general exception occurred interating the two strings.",
            "original_exception": exc,
        }
        raise FGeneralError(exc_args)
    else:
        return substring


def clean_non_word_characters(string: str) -> str:
    """
    This function will remove any non-word hex characters from any passing string.

    Strings without non-word hex will be passed through without any errors.

    Args:
        string (str):
        \t\\- A string with non-word hex characters.

    Raises:
        FTypeError (fexception):
        \t\\- The object value '{string}' is not an instance of the required class(es) or subclass(es).
        FValueError (fexception):
        \t\\- The string ({string}) with non-word characters did not clean.

    Returns:
        str:\\
        \t\\- A cleaned string with valid only words.
    """
    logger = logging.getLogger(__name__)
    logger.debug(f"=" * 20 + get_function_name() + "=" * 20)
    # Custom flowchart tracking. This is ideal for large projects that move a lot.
    # For any third-party modules, set the flow before making the function call.
    logger_flowchart = logging.getLogger("flowchart")
    logger_flowchart.debug(f"Flowchart --> Function: {get_function_name()}")

    try:
        type_check(value=string, required_type=str)
    except FTypeError:
        raise

    logger.debug("Passing parameters:\n" f"  - string (str):\n        - {string}\n")

    # Some Python returned information will return with trailing hex characters (non-words). These are unescaped control characters, which is what Python displays using hexadecimal notation.
    # This expression will remove the hex characters. It can be written with either [^\x20-\x7e] or [^ -~].*
    # Note: When viewing non-word characters it can very from console or logging. You may see output similar BTW-N5K\x06 or BTW-N5K♠ or BTW-N5K\u00006 or BTW-N5K.
    # Example1:
    #   - Input: BTW-N5K\x06
    #   - Output: BTW-N5K
    cleaned_string = re.sub(r"[^ -~].*", "", string)
    encoded_string = cleaned_string.encode("ascii", "ignore")
    if "\\x" in str(encoded_string):
        exc_args = {
            "main_message": f"The string ({string}) with non-word characters did not clean.",
            "expected_result": "The string should not have contained any hex characters.",
            "returned_result": encoded_string,
        }
        raise FValueError(exc_args)
    else:
        # Checks if the lengths are different from the parameter string and cleaned string to know if the string contained non-word values.
        if len(string) > len(cleaned_string):
            logger.debug(
                f"The string was cleaned of all non-word characters. Set Value (str):\n    - Original Value: {string}\n    - Cleaned Value: {cleaned_string}"
            )
        else:
            logger.debug(f"The string did not contain any non-word characters. No change required.")
        return cleaned_string
