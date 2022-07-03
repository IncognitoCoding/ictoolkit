# Built-in/Generic Imports
import pytest

# Local Functions

from ictoolkit.data_structure.common import common_case_isupper, common_case_islower


__author__ = "IncognitoCoding"
__copyright__ = "Copyright 2022, test_common"
__credits__ = ["IncognitoCoding"]
__license__ = "MIT"
__version__ = "0.3"
__maintainer__ = "IncognitoCoding"
__status__ = "Production"


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
