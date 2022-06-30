# Built-in/Generic Imports
import pytest

# Local Functions
from ictoolkit.data_structure.dict import move_dict_value
from ictoolkit.data_structure.common import (
    str_to_list,
    list_to_str,
    common_case_isupper,
    common_case_islower,
    dict_keys_upper,
    dict_keys_lower,
)


__author__ = "IncognitoCoding"
__copyright__ = "Copyright 2022, test_common"
__credits__ = ["IncognitoCoding"]
__license__ = "MIT"
__version__ = "0.2"
__maintainer__ = "IncognitoCoding"
__status__ = "Production"


def test_1_str_to_list():
    """
    This function tests converting a single string to list.
    """
    my_list = str_to_list(value="sample1", sep=", ")
    assert ["sample1"] == my_list


def test_1_1_str_to_list():
    """
    This function tests converting a single string to list.
    """
    my_list = str_to_list(value="10.10.200.11", sep=", ")
    assert ["10.10.200.11"] == my_list


def test_1_2_str_to_list():
    """
    This function tests converting a string to list.
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


def test_1_list_to_str():
    """
    This function tests converting a list to str.
    """
    my_str = list_to_str(value="sample1")
    assert "sample1" == my_str


def test_1_1_list_to_str():
    """
    This function tests converting a list to str.
    """
    my_str = list_to_str(value=["sample1", "sample2"])
    assert "sample1 sample2" == my_str


def test_1_2_list_to_str():
    """
    This function tests converting a list to str.
    """
    my_str = list_to_str(value=["sample1", "sample2"], sep=", ")
    assert "sample1, sample2" == my_str


def test_1_3_list_to_str():
    """
    This function tests converting a list to str.
    """
    my_str = list_to_str(value=["sample1", 2], sep=", ")
    assert "sample1, 2" == my_str


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


def test_1_common_case_isupper():
    my_list = ["lower", "UPPER", "SAMPLE"]
    assert True is common_case_isupper(my_list)


def test_1_1_common_case_isupper():
    my_list = ["l", "U"]
    assert True is common_case_isupper(my_list)


def test_1_2_common_case_isupper():
    my_list = ["lower", "UPPER", "sample"]
    assert False is common_case_isupper(my_list)


def test_1_common_case_islower():
    my_list = ["lower", "UPPER", "sample"]
    assert True is common_case_islower(my_list)


def test_1_1_common_case_islower():
    my_list = ["l", "U"]
    assert False is common_case_islower(my_list)


def test_1_2_common_case_islower():
    my_list = ["lower", "UPPER", "SAMPLE"]
    assert False is common_case_islower(my_list)


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
