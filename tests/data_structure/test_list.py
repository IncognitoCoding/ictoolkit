# Built-in/Generic Imports
import pytest

# Local Functions
from ictoolkit.data_structure.list import (
    find_substring,
    str_to_list,
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
__version__ = "0.2"
__maintainer__ = "IncognitoCoding"
__status__ = "Production"


def test_1_find_substring():
    """This function tests getting a single substring"""
    my_substrings = find_substring(value="sample1", start_match="m", end_match="e")
    assert ["pl"] == my_substrings


def test_1_1_find_substring():
    """This function tests getting a single substring"""
    my_substrings = find_substring(
        value="This is my sample. %Excluding this section%. %Excluding this section too%",
        start_match="%",
        end_match="%",
    )
    assert ["Excluding this section", "Excluding this section too"] == my_substrings


def test_1_2_find_substring():
    """This function tests getting a single substring"""
    my_substrings = find_substring(
        value="This is my sample. %Excluding this section%. %Excluding this section too%",
        start_match="%",
        end_match="#",
    )
    assert None is my_substrings


def test_1_str_to_list():
    """
    This function tests converting a single string to a list.
    """
    my_list = str_to_list(value="sample1", sep=", ")
    assert ["sample1"] == my_list


def test_1_1_str_to_list():
    """
    This function tests converting a single string to a list.
    """
    my_list = str_to_list(value="10.10.200.11", sep=", ")
    assert ["10.10.200.11"] == my_list


def test_1_2_str_to_list():
    """
    This function tests converting a string to a list.
    """
    my_list = str_to_list(value="sample1, sample2, sample3", sep=", ")
    assert ["sample1", "sample2", "sample3"] == my_list


def test_1_3_str_to_list():
    """
    This function tests passing an existing list through.
    """
    my_list = str_to_list(value=["sample1", "sample2", "sample3"], sep=", ")
    assert ["sample1", "sample2", "sample3"] == my_list


def test_1_4_str_to_list():
    """
    This function tests passing an existing list through.
    """
    my_list = str_to_list(value=[], sep=", ")
    assert [] == my_list


def test_1_5_str_to_list():
    """
    This function tests converting a string to a list using an exclude character.
    """
    my_list = str_to_list(
        value="This is •my• sample •excluding everything after. 13• Also, this is my section that will split. 16•This section will not.•",
        sep=" ",
        exclude="•",
    )
    assert [
        "This",
        "is",
        "my",
        "sample",
        "excluding everything after. 13",
        "Also,",
        "this",
        "is",
        "my",
        "section",
        "that",
        "will",
        "split.",
        "16",
        "This section will not.",
    ] == my_list


def test_1_6_str_to_list():
    """
    This function tests converting a string to a list using an exclude character.
    """
    my_list = str_to_list(
        value="This is •my sample• excluding everything after. 13 Also, this is my section that will split. This section will not.",
        sep=" ",
        exclude="•",
    )
    assert [
        "This",
        "is",
        "my sample",
        "excluding",
        "everything",
        "after.",
        "13",
        "Also,",
        "this",
        "is",
        "my",
        "section",
        "that",
        "will",
        "split.",
        "This",
        "section",
        "will",
        "not.",
    ] == my_list


def test_1_7_str_to_list():
    """
    This function tests converting a string to a list using an exclude character.
    """
    my_list = str_to_list(
        # value="This is %my% sample %excluding everything after. 13% Also, this is my section that will split. 16%This section will not.%",
        # value="This is %my sample% excluding everything after. 13 Also, this is my section that will split. This section will not.",
        value="This is •my sample excluding everything after. 13 Also, this is my section that will split. This section will not.",
        sep=" ",
        exclude="•",
    )
    assert [
        "This",
        "is",
        "my sample excluding everything after. 13 Also, this is my section that will split. This section will not.",
    ] == my_list


def test_1_8_str_to_list():
    """
    This function tests converting a string to a list using an exclude character.
    """
    my_list = str_to_list(
        # value="This is %my% sample %excluding everything after. 13% Also, this is my section that will split. 16%This section will not.%",
        # value="This is %my sample% excluding everything after. 13 Also, this is my section that will split. This section will not.",
        value="This is my sample excluding everything after. 13 Also, this is my section that will split. This section will not.",
        sep=" ",
        exclude="•",
    )
    assert [
        "This",
        "is",
        "my",
        "sample",
        "excluding",
        "everything",
        "after.",
        "13",
        "Also,",
        "this",
        "is",
        "my",
        "section",
        "that",
        "will",
        "split.",
        "This",
        "section",
        "will",
        "not.",
    ] == my_list


def test_1_9_str_to_list():
    """
    This function tests passing a list through.
    """
    my_list = str_to_list(
        # value="This is %my% sample %excluding everything after. 13% Also, this is my section that will split. 16%This section will not.%",
        # value="This is %my sample% excluding everything after. 13 Also, this is my section that will split. This section will not.",
        value=["sample1"],
        sep=" ",
    )
    assert ["sample1"] == my_list


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
