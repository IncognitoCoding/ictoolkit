# Built-in/Generic Imports
import pytest

# Local Functions
from ictoolkit.data_structure.dict import string_grouper, sort_dict


__author__ = "IncognitoCoding"
__copyright__ = "Copyright 2022, test_dict"
__credits__ = ["IncognitoCoding"]
__license__ = "MIT"
__version__ = "0.2"
__maintainer__ = "IncognitoCoding"
__status__ = "Production"


def test_1_sort_dict():
    """Tests sorting keys"""
    my_dict = {
        "TB": [50, "sample5", "sample6"],
        "BB": [85, "sample28"],
        "CC": "sample15",
    }
    my_dict = sort_dict(my_dict=my_dict, sort="key")
    assert {"BB": [85, "sample28"], "CC": "sample15", "TB": [50, "sample5", "sample6"]} == my_dict


def test_1_1_sort_dict():
    """Tests sorting values"""
    my_dict = {
        "ZZ": "zipzip14",
        "TB": [50, "sample8", "sample6"],
        "BB": [85, "sample28"],
        "CC": "sample15",
    }
    my_dict = sort_dict(my_dict=my_dict, sort="key", sort_values=True)
    assert {"BB": [85, "sample28"], "CC": "sample15", "TB": [50, "sample6", "sample8"], "ZZ": "zipzip14"} == my_dict


def test_1_2_sort_dict():
    """Tests sorting values"""
    my_dict = {
        "ZZ": "zipzip14",
        "TB": [50, "sample8", "sample6"],
        "BB": [85, "sample28"],
        "CC": "sample15",
    }
    my_dict = sort_dict(my_dict=my_dict, sort="value")
    assert {"TB": [50, "sample8", "sample6"], "BB": [85, "sample28"], "CC": "sample15", "ZZ": "zipzip14"} == my_dict


def test_1_3_sort_dict():
    """Tests sorting values"""
    my_dict = {
        "ZZ": "zipzip14",
        "TB": [50, "sample8", "sample6"],
        "BB": [85, "sample28"],
        "CC": "sample15",
    }
    my_dict = sort_dict(my_dict=my_dict, sort="value", sort_values=True)
    assert {"TB": [50, "sample6", "sample8"], "BB": [85, "sample28"], "CC": "sample15", "ZZ": "zipzip14"} == my_dict


def test_1_string_grouper():
    """
    Tests grouping strings.

    Option: 1
    """
    # List of sample switch names for multiple sites. Case insensitive testing.
    list_of_strings = [
        "JJ-MDF-9200-1_2",
        "KV-MDF-9200-1_2",
        "KV-MDF1-9200-1_2",
        "KZV-MDF1-9200-1_2",
        "kv-IDF1-9200-1_2",
        "KV-IDF2-9200-1_2",
        "TI-IDF1-9200-1_2",
        "TI-IDF2-9200-1_2",
    ]

    group_check = string_grouper(list_of_strings=list_of_strings, grouping_value="-", grouping_option=1)

    assert 5 == len(group_check.items())
    assert ("JJ", ["JJ-MDF-9200-1_2"]) == list(group_check.items())[0]
    assert ('KV', ['KV-IDF2-9200-1_2', 'KV-MDF-9200-1_2', 'KV-MDF1-9200-1_2']) == list(group_check.items())[1]  # fmt: skip
    assert ("KZV", ["KZV-MDF1-9200-1_2"]) == list(group_check.items())[2]
    assert ("TI", ["TI-IDF1-9200-1_2", "TI-IDF2-9200-1_2"]) == list(group_check.items())[3]
    assert ("kv", ["kv-IDF1-9200-1_2"]) == list(group_check.items())[4]


def test_1_1_string_grouper():
    """
    Tests grouping strings.

    Option: 1
    """
    # List of sample switch names for multiple sites. Case insensitive testing.
    list_of_strings = [
        "JJ-MDF-9200-1_2",
        "KV-MDF-9200-1_2",
        "KV-MDF1-9200-1_2",
        "KZV-MDF1-9200-1_2",
        "kv-IDF1-9200-1_2",
        "KV-IDF2-9200-1_2",
        "TI-IDF1-9200-1_2",
        "TI-IDF2-9200-1_2",
    ]

    group_check = string_grouper(
        list_of_strings=list_of_strings, grouping_value="-", grouping_option=1, case_insensitive=True
    )
    assert 4 == len(group_check.items())
    assert ("JJ", ["JJ-MDF-9200-1_2"]) == list(group_check.items())[0]
    assert ('KV', ['kv-IDF1-9200-1_2', 'KV-IDF2-9200-1_2', 'KV-MDF-9200-1_2', 'KV-MDF1-9200-1_2']) == list(group_check.items())[1]  # fmt: skip
    assert ("KZV", ["KZV-MDF1-9200-1_2"]) == list(group_check.items())[2]
    assert ("TI", ["TI-IDF1-9200-1_2", "TI-IDF2-9200-1_2"]) == list(group_check.items())[3]


def test_1_2_string_grouper():
    """
    Tests grouping strings.

    Option: 2
    """
    # List of sample switch names for multiple sites. Case insensitive testing.
    list_of_strings = [
        "JJ-MDF-9200-1_2",
        "KV-MDF-9200-1_2",
        "KV-MDF1-9200-1_2",
        "KZV-MDF1-9200-1_2",
        "kv-IDF1-9200-1_2",
        "KV-IDF2-9200-1_2",
        "TI-IDF1-9200-1_2",
        "TI-IDF2-9200-1_2",
    ]

    group_check = string_grouper(list_of_strings=list_of_strings, grouping_value=2, grouping_option=2)

    assert 5 == len(group_check.items())
    assert ("JJ", ["JJ-MDF-9200-1_2"]) == list(group_check.items())[0]
    assert ('KV', ['KV-IDF2-9200-1_2', 'KV-MDF-9200-1_2', 'KV-MDF1-9200-1_2']) == list(group_check.items())[1]  # fmt: skip
    assert ("KZ", ["KZV-MDF1-9200-1_2"]) == list(group_check.items())[2]
    assert ("TI", ["TI-IDF1-9200-1_2", "TI-IDF2-9200-1_2"]) == list(group_check.items())[3]
    assert ("kv", ["kv-IDF1-9200-1_2"]) == list(group_check.items())[4]


def test_1_3_string_grouper():
    """
    Tests grouping strings.

    Option: 2
    """
    # List of sample switch names for multiple sites. Case insensitive testing.
    list_of_strings = [
        "JJ-MDF-9200-1_2",
        "KV-MDF-9200-1_2",
        "KV-MDF1-9200-1_2",
        "KZV-MDF1-9200-1_2",
        "kv-IDF1-9200-1_2",
        "KV-IDF2-9200-1_2",
        "TI-IDF1-9200-1_2",
        "TI-IDF2-9200-1_2",
    ]

    group_check = string_grouper(
        list_of_strings=list_of_strings, grouping_value=2, grouping_option=2, case_insensitive=True
    )

    assert 4 == len(group_check.items())
    assert ("JJ", ["JJ-MDF-9200-1_2"]) == list(group_check.items())[0]
    assert ('KV', ['kv-IDF1-9200-1_2', 'KV-IDF2-9200-1_2', 'KV-MDF-9200-1_2', 'KV-MDF1-9200-1_2']) == list(group_check.items())[1]  # fmt: skip
    assert ("KZ", ["KZV-MDF1-9200-1_2"]) == list(group_check.items())[2]
    assert ("TI", ["TI-IDF1-9200-1_2", "TI-IDF2-9200-1_2"]) == list(group_check.items())[3]


def test_1_4_string_grouper():
    """
    Tests grouping strings.

    Option: 3
    """
    # List of sample switch names for multiple sites. Case insensitive testing.
    list_of_strings = [
        "JJ-MDF-9200-1_2",
        "KV-MDF-9200-1_2",
        "KV-MDF1-9200-1_2",
        "KZV-MDF1-9200-1_2",
        "kv-IDF1-9200-1_2",
        "KV-IDF2-9200-1_2",
        "TI-IDF1-9200-1_2",
        "TI-IDF2-9200-1_2",
    ]

    group_check = string_grouper(list_of_strings=list_of_strings, grouping_option=3)

    assert 5 == len(group_check.items())
    assert ("JJ-MDF-9200-1_2", ["JJ-MDF-9200-1_2"]) == list(group_check.items())[0]
    assert ('KV-', ['KV-IDF2-9200-1_2', 'KV-MDF-9200-1_2', 'KV-MDF1-9200-1_2']) == list(group_check.items())[1]  # fmt: skip
    assert ("KZV-MDF1-9200-1_2", ["KZV-MDF1-9200-1_2"]) == list(group_check.items())[2]
    assert ("TI-IDF", ["TI-IDF1-9200-1_2", "TI-IDF2-9200-1_2"]) == list(group_check.items())[3]
    assert ("kv-IDF1-9200-1_2", ["kv-IDF1-9200-1_2"]) == list(group_check.items())[4]


def test_1_5_string_grouper():
    """
    Tests grouping strings.

    Option: 3
    """
    # List of sample switch names for multiple sites. Case insensitive testing.
    list_of_strings = [
        "JJ-MDF-9200-1_2",
        "KV-MDF-9200-1_2",
        "KV-MDF1-9200-1_2",
        "KZV-MDF1-9200-1_2",
        "kv-IDF1-9200-1_2",
        "KV-IDF2-9200-1_2",
        "TI-IDF1-9200-1_2",
        "TI-IDF2-9200-1_2",
    ]

    group_check = string_grouper(list_of_strings=list_of_strings, grouping_option=3, case_insensitive=True)

    assert 5 == len(group_check.items())
    assert ("JJ-MDF-9200-1_2", ["JJ-MDF-9200-1_2"]) == list(group_check.items())[0]
    assert ("KV-IDF", ["kv-IDF1-9200-1_2", "KV-IDF2-9200-1_2"]) == list(group_check.items())[1]
    assert ("KV-MDF", ["KV-MDF-9200-1_2", "KV-MDF1-9200-1_2"]) == list(group_check.items())[2]
    assert ("KZV-MDF1-9200-1_2", ["KZV-MDF1-9200-1_2"]) == list(group_check.items())[3]
    assert ("TI-IDF", ["TI-IDF1-9200-1_2", "TI-IDF2-9200-1_2"]) == list(group_check.items())[4]