# Built-in/Generic Imports
import pytest

# Local Functions
from ictoolkit.data_structure.str import (
    find_longest_common_substring,
    clean_non_word_characters,
)

# Exceptions
from fexception import FValueError


__author__ = "IncognitoCoding"
__copyright__ = "Copyright 2022, test_str"
__credits__ = ["IncognitoCoding"]
__license__ = "MIT"
__version__ = "0.1"
__maintainer__ = "IncognitoCoding"
__status__ = "Production"


def test_find_longest_common_substring():
    """
    Tests finding a common grouping substring.

    Raises:
        ValueError: A failure occurred in section 1.0 while testing the function \'find_longest_common_substring\'. The test did return the correct common substring.
        ValueError: A failure occurred in section 2.0 while testing the function \'find_longest_common_substring\'. The test did not fail when sending a non-string parameter.
    """
    print("")
    print("-" * 65)
    print("-" * 65)
    print("Testing Function: find_longest_common_substring")
    print("-" * 65)
    print("-" * 65)
    print("")

    # ############################################################
    # ######Section Test Part 1 (Successful Value Checking)#######
    # ############################################################
    # ========Tests for a successful output return.========
    common_substring = find_longest_common_substring("mysamplechangeshere", "mysampleneverchanges")
    # Checks if the return substring is not equal the expected result.
    if not common_substring == "mysample":
        exc_args = {
            "main_message": "A failure occurred in section 1.0 while testing the function 'find_longest_common_substring'. The test did return the correct common substring.",
            "expected_result": "mysample",
            "returned_result": common_substring,
        }
        raise FValueError(exc_args)

    # ############################################################
    # ######Section Test Part 2 (Error/Catch Value Checking)######
    # ############################################################
    # ========Tests for an incorrectly sent config format.========
    try:

        common_substring = find_longest_common_substring("mysamplechangeshere", ["INCORRECT or EMPTY DATA TEST"])
    except Exception as error:
        if (
            """The object value '['INCORRECT or EMPTY DATA TEST']' is not an instance of the required class(es) or subclass(es)."""
            not in str(error)
        ):
            exc_args = {
                "main_message": "A failure occurred in section 2.0 while testing the function 'find_longest_common_substring'. The test did not fail when sending a non-string parameter.",
                "expected_result": "non-string parameter error",
                "returned_result": error,
            }
            raise FValueError(exc_args)


def test_clean_non_word_characters():
    """
    Tests cleaning non-word characters.

    Raises:
        ValueError: A failure occurred in section 1.0 while testing the function \'clean_non_word_characters\'. The test did return the correct cleaned substring.
        ValueError: A failure occurred in section 2.0 while testing the function \'clean_non_word_characters\'. The test did not fail when sending a non-string parameter.
    """
    print("")
    print("-" * 65)
    print("-" * 65)
    print("Testing Function: clean_non_word_characters")
    print("-" * 65)
    print("-" * 65)
    print("")

    # ############################################################
    # ######Section Test Part 1 (Successful Value Checking)#######
    # ############################################################
    # ========Tests for a successful output return.========
    cleaned_string = clean_non_word_characters("BTW-N5K\x06")
    # Checks if the return substring is not equal the expected result.
    if not cleaned_string == "BTW-N5K":
        exc_args = {
            "main_message": "A failure occurred in section 1.0 while testing the function 'clean_non_word_characters'. The test did return the correct cleaned substring.",
            "expected_result": "BTW-N5K",
            "returned_result": cleaned_string,
        }
        raise FValueError(exc_args)

    # ############################################################
    # ######Section Test Part 2 (Error/Catch Value Checking)######
    # ############################################################
    # ========Tests for an incorrectly sent config format.========
    try:

        cleaned_string = clean_non_word_characters(["INCORRECT or EMPTY DATA TEST"])
    except Exception as error:
        if (
            """The object value '['INCORRECT or EMPTY DATA TEST']' is not an instance of the required class(es) or subclass(es)."""
            not in str(error)
        ):
            exc_args = {
                "main_message": "A failure occurred in section 2.0 while testing the function 'clean_non_word_characters'. The test did not fail when sending a non-string parameter.",
                "expected_result": "non-string parameter error",
                "returned_result": error,
            }
            raise FValueError(exc_args)
