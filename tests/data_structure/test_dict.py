# Built-in/Generic Imports
import pytest

# Local Functions
from ictoolkit.data_structure.dict import dict_keys_upper, dict_keys_lower, string_grouper, sort_dict, move_dict_value


__author__ = "IncognitoCoding"
__copyright__ = "Copyright 2022, test_dict"
__credits__ = ["IncognitoCoding"]
__license__ = "MIT"
__version__ = "0.3"
__maintainer__ = "IncognitoCoding"
__status__ = "Production"


def test_1_dict_keys_upper():
    my_dict = {"tb": "sample1", "bb": "sample2"}
    my_dict = dict_keys_upper(my_dict=my_dict)
    assert {"TB": "sample1", "BB": "sample2"} == my_dict


def test_1_1_dict_keys_upper():
    my_dict = {"tb": {"cc": "sample1"}, "bb": "sample2"}
    my_dict = dict_keys_upper(my_dict=my_dict)
    assert {"TB": {"CC": "sample1"}, "BB": "sample2"} == my_dict


def test_1_dict_keys_lower():
    my_dict = {"TB": "sample1", "BB": "sample2"}
    my_dict = dict_keys_lower(my_dict=my_dict)
    assert {"tb": "sample1", "bb": "sample2"} == my_dict


def test_1_1_dict_keys_lower():
    my_dict = {"TB": {"CC": "sample1"}, "BB": "sample2"}
    my_dict = dict_keys_lower(my_dict=my_dict)
    assert {"tb": {"cc": "sample1"}, "bb": "sample2"} == my_dict


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


def test_1_move_dict_value():
    my_dict = {
        "TB": ["sample1", "sample5", "sample6"],
        "BB": "sample8",
        "CC": "sample15",
    }
    my_dict = move_dict_value(my_dict=my_dict, src_key="TB", dest_key="BB", value="sample5")
    assert {"TB": ["sample1", "sample6"], "BB": ["sample5", "sample8"], "CC": "sample15"} == my_dict


def test_1_1_move_dict_value():
    """Tests string with number sort"""
    my_dict = {
        "TB": ["sample1", "sample5", "sample6"],
        "BB": ["zip", "sample28"],
        "CC": "sample15",
    }
    my_dict = move_dict_value(my_dict=my_dict, src_key="TB", dest_key="BB", value="sample5")
    assert {"BB": ["sample28", "sample5", "zip"], "CC": "sample15", "TB": ["sample1", "sample6"]} == my_dict


def test_1_2_move_dict_value():
    """Tests string with number sort"""
    my_dict = {
        "TB": ["sample1", "sample5", "sample6"],
        "BB": ["zip", "sample28"],
        "CC": "sample15",
    }
    my_dict = move_dict_value(my_dict=my_dict, src_key="TB", dest_key="BB", value="sample5", sort=False)
    assert {"TB": ["sample1", "sample6"], "BB": ["zip", "sample28", "sample5"], "CC": "sample15"} == my_dict


def test_1_3_move_dict_value():
    """Tests int sort"""
    my_dict = {
        "TB": [1, 5, 25],
        "BB": [80, 35],
        "CC": 6,
    }
    my_dict = move_dict_value(my_dict=my_dict, src_key="TB", dest_key="BB", value=5)
    assert {"TB": [1, 25], "BB": [5, 35, 80], "CC": 6} == my_dict


def test_1_4_move_dict_value():
    """Tests with mix key types"""
    my_dict = {
        2: "sample2",
        "BB": "sample8",
        "CC": "sample15",
        "AA": "sample16",
        1: "sample1",
    }
    my_dict = move_dict_value(my_dict=my_dict, src_key="BB", dest_key=1, value="sample8")
    assert {1: ["sample1", "sample8"], 2: "sample2", "AA": "sample16", "CC": "sample15"} == my_dict


def test_1_5_move_dict_value():
    """Tests no sort when enabled because bool"""
    my_dict = {
        "TB": ["sample1", "sample5", "sample6"],
        "BB": [True, "zip", "sample28"],
        "CC": "sample15",
    }
    my_dict = move_dict_value(my_dict=my_dict, src_key="TB", dest_key="BB", value="sample5")
    assert {"BB": [True, "sample5", "sample28", "zip"], "CC": "sample15", "TB": ["sample1", "sample6"]} == my_dict


def test_1_6_move_dict_value():
    """Tests no sort when enabled because mixed int and str"""
    my_dict = {
        "TB": [50, "sample5", "sample6"],
        "BB": [85, "sample28"],
        "CC": "sample15",
    }
    my_dict = move_dict_value(my_dict=my_dict, src_key="TB", dest_key="BB", value=50)
    assert {"BB": [50, 85, "sample28"], "CC": "sample15", "TB": ["sample5", "sample6"]} == my_dict


def test_1_7_move_dict_value():
    """Tests lists of values."""
    my_dict = {
        "KV": ["KV-MyTest1", "KV-MyTest2"],
        "TI": ["TI-MyTest1", "TI-MyTest2"],
        "WZ": ["WZ-MyTest1"],
    }
    my_dict = move_dict_value(my_dict=my_dict, src_key="TI", dest_key="WZ", value="TI-MyTest2")
    assert {"KV": ["KV-MyTest1", "KV-MyTest2"], "TI": ["TI-MyTest1"], "WZ": ["TI-MyTest2", "WZ-MyTest1"]} == my_dict


def test_1_8_move_dict_value():
    """Tests a new destination key"""
    my_dict = {
        "KV": ["KV-MyTest1", "KV-MyTest2"],
        "TI": ["TI-MyTest1", "TI-MyTest2"],
        "WZ": ["WZ-MyTest1"],
    }
    my_dict = move_dict_value(my_dict=my_dict, src_key="TI", dest_key="YO", value="TI-MyTest2")
    assert {
        "KV": ["KV-MyTest1", "KV-MyTest2"],
        "TI": ["TI-MyTest1"],
        "WZ": ["WZ-MyTest1"],
        "YO": ["TI-MyTest2"],
    } == my_dict


def test_1_9_move_dict_value():
    """Tests a new destination key"""
    my_dict = {
        True: ["KV-MyTest1", "KV-MyTest2"],
        "TI": ["TI-MyTest1", "TI-MyTest2"],
        "WZ": ["WZ-MyTest1"],
    }
    my_dict = move_dict_value(my_dict=my_dict, src_key="TI", dest_key=True, value="TI-MyTest2")
    assert {"TI": ["TI-MyTest1"], True: ["KV-MyTest1", "KV-MyTest2", "TI-MyTest2"], "WZ": ["WZ-MyTest1"]} == my_dict


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
