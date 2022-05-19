# Built-in/Generic Imports
import pytest

# Local Functions
from ictoolkit.data_structure.list import (
    remove_duplicate_dict_values_in_list,
    get_list_of_dicts_duplicates,
    get_list_duplicates,
)

# Exceptions
from fexception import FValueError


__author__ = "IncognitoCoding"
__copyright__ = "Copyright 2022, test_list"
__credits__ = ["IncognitoCoding"]
__license__ = "MIT"
__version__ = "0.1"
__maintainer__ = "IncognitoCoding"
__status__ = "Production"


def test_remove_duplicate_dict_values_in_list():
    """
    This tests removing duplicate dictionary values in a list.

    Raises:
        ValueError: A failure occurred in section 1.0 while testing the function 'remove_duplicate_dict_values_in_list' using a full check.
        ValueError: A failure occurred in section 1.1 while testing the function 'remove_duplicate_dict_values_in_list' using an index.
    """
    print("")
    print("-" * 65)
    print("-" * 65)
    print("Testing Function: remove_duplicate_dict_values_in_list")
    print("-" * 65)
    print("-" * 65)
    print("")

    # ############################################################
    # ######Section Test Part 1 (Successful Value Checking)#######
    # ############################################################
    # ========Tests for a successful output return.========
    # Sets sample list
    sample_list_dictionary = list(
        [
            {"search_entry": "|Error|", "found_entry": "the entry found"},
            {"search_entry": "|Warning|", "found_entry": "the entry found"},
        ]
    )
    # Tests removing duplicate dictionary entries.
    check_all = remove_duplicate_dict_values_in_list(sample_list_dictionary)
    # Return length should equal 2.
    # Expected Return: [{'search_entry': '|Error|', 'found_entry': 'the entry found'}, {'search_entry': '|Warning|', 'found_entry': 'the entry found'}]
    if len(check_all) != 2:
        exc_args = {
            "main_message": "A failure occurred in section 1.0 while testing the function 'remove_duplicate_dict_values_in_list' using a full check.",
            "expected_result": 2,
            "returned_result": len(check_all),
        }
        raise FValueError(exc_args)

    # ========Tests for a successful output return.========
    # Tests removing duplicates from index 1 of each dictionary entry.
    check_index = remove_duplicate_dict_values_in_list(sample_list_dictionary, 1)
    # Return length should equal 1.
    # Expected Return: [{'search_entry': '|Error|', 'found_entry': 'the entry found'}]
    if len(check_index) != 1:
        exc_args = {
            "main_message": "A failure occurred in section 1.1 while testing the function 'remove_duplicate_dict_values_in_list' using an index.",
            "expected_result": 1,
            "returned_result": len(check_index),
        }
        raise FValueError(exc_args)


def test_get_list_of_dicts_duplicates():
    """
    Tests getting a list of dictionary duplicates.

    Raises:
        ValueError: A failure occurred in section 1.0 while testing the function 'get_list_of_dicts_duplicates'.
        ValueError: A failure occurred in section 1.1 while testing the function 'get_list_of_dicts_duplicates'.
    """
    print("")
    print("-" * 65)
    print("-" * 65)
    print("Testing Function: get_list_of_dicts_duplicates")
    print("-" * 65)
    print("-" * 65)
    print("")

    # ############################################################
    # ######Section Test Part 1 (Successful Value Checking)#######
    # ############################################################
    # ========Tests for a successful output return.========
    # Sets sample list
    sample_list_dictionary = [
        {"key1": "ValueA"},
        {"key1": "ValueA"},
        {"key1": "ValueA"},
        {"key1": "ValueB"},
        {"key1": "ValueB"},
    ]
    # Tests finding duplicate values for key (key1).
    check_all = get_list_of_dicts_duplicates("key1", sample_list_dictionary)
    # Return length should equal 5.
    # Expected Return: [{'index': 0, 'value': 'ValueA'}, {'index': 1, 'value': 'ValueA'}, {'index': 2, 'value': 'ValueA'}, {'index': 3, 'value': 'ValueB'}, {'index': 4, 'value': 'ValueB'}]
    if len(check_all) != 5:
        exc_args = {
            "main_message": "A failure occurred in section 1.0 while testing the function 'get_list_of_dicts_duplicates'.",
            "expected_result": 5,
            "returned_result": len(check_all),
        }
        raise FValueError(exc_args)

    # ========Tests for a successful output return.========
    # Tests finding duplicate values for key (key1).
    check_all = get_list_of_dicts_duplicates("key1", sample_list_dictionary, True)
    # Return length should equal 2.
    # Expected Return: {'ValueA': [{'index': 0, 'value': 'ValueA'}, {'index': 1, 'value': 'ValueA'}, {'index': 2, 'value': 'ValueA'}], 'ValueB': [{'index': 3, 'value': 'ValueB'}, {'index': 4, 'value': 'ValueB'}]}
    if len(check_all) != 2:
        exc_args = {
            "main_message": "A failure occurred in section 1.1 while testing the function 'get_list_of_dicts_duplicates'.",
            "expected_result": 2,
            "returned_result": len(check_all),
        }
        raise FValueError(exc_args)


def test_get_list_duplicates():
    """
    Tests getting a list of duplicates.

    Raises:
        ValueError: A failure occurred in section 1.0 while testing the function 'get_list_duplicates'.
        ValueError: A failure occurred in section 1.1 while testing the function 'get_list_duplicates'.
        ValueError: A failure occurred in section 1.2 while testing the function 'get_list_duplicates'.
    """
    print("")
    print("-" * 65)
    print("-" * 65)
    print("Testing Function: get_list_duplicates")
    print("-" * 65)
    print("-" * 65)
    print("")

    # ############################################################
    # ######Section Test Part 1 (Successful Value Checking)#######
    # ############################################################
    # ========Tests for a successful output return.========
    # Sets sample list
    sample_list = ["ValueA", "ValueA", "ValueA", "ValueB", "ValueB"]
    # Tests finding duplicate values in the list.
    check_all = get_list_duplicates(sample_list)
    # Return length should equal 5.
    # Expected Return: [{'index': 0, 'value': 'ValueA'}, {'index': 1, 'value': 'ValueA'}, {'index': 2, 'value': 'ValueA'}, {'index': 3, 'value': 'ValueB'}, {'index': 4, 'value': 'ValueB'}]
    if len(check_all) != 5:
        exc_args = {
            "main_message": "A failure occurred in section 1.0 while testing the function 'get_list_duplicates'.",
            "expected_result": 5,
            "returned_result": len(check_all),
        }
        raise FValueError(exc_args)

    # ========Tests for a successful output return.========
    # Sets sample list
    sample_list = [["ValueA", "ValueB"], ["ValueA", "ValueB"], ["ValueD", "ValueB"], ["ValueB"], ["ValueB"]]
    # Tests finding duplicate values in the list.
    check_all = get_list_duplicates(sample_list, None, True)
    # Return length should equal 2.
    # Expected Return: {'ValueA': [{'index': 0, 'value': 'ValueA'}, {'index': 1, 'value': 'ValueA'}, {'index': 2, 'value': 'ValueA'}], 'ValueB': [{'index': 3, 'value': 'ValueB'}, {'index': 4, 'value': 'ValueB'}]}
    if len(check_all) != 2:
        exc_args = {
            "main_message": "A failure occurred in section 1.1 while testing the function 'get_list_duplicates'.",
            "expected_result": 2,
            "returned_result": len(check_all),
        }
        raise FValueError(exc_args)

    # ========Tests for a successful output return.========
    # Sets sample list
    sample_list = [["ValueA", "ValueB"], ["ValueA", "ValueB"], ["ValueD", "ValueB"], ["ValueB"], ["ValueB"]]
    # Tests finding duplicate values in the list.
    check_all = get_list_duplicates(sample_list, 0, True)
    # Return length should equal 2.
    # Expected Return: {'ValueA': [{'index': 0, 'value': 'ValueA'}, {'index': 1, 'value': 'ValueA'}, {'index': 2, 'value': 'ValueA'}], 'ValueB': [{'index': 3, 'value': 'ValueB'}, {'index': 4, 'value': 'ValueB'}]}
    if len(check_all) != 2:
        exc_args = {
            "main_message": "A failure occurred in section 1.2 while testing the function 'get_list_duplicates'.",
            "expected_result": 2,
            "returned_result": len(check_all),
        }
        raise FValueError(exc_args)
