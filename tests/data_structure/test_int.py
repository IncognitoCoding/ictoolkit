# Built-in/Generic Imports
import pytest

# Local Functions
from ictoolkit.data_structure.int import char_count


__author__ = "IncognitoCoding"
__copyright__ = "Copyright 2022, test_int"
__credits__ = ["IncognitoCoding"]
__license__ = "MIT"
__version__ = "0.1"
__maintainer__ = "IncognitoCoding"
__status__ = "Production"


def test_1_char_count():
    """
    This function tests getting the character count.
    """
    my_count = char_count(value="sample1", character="m")
    assert 1 == my_count


def test_1_1_char_count():
    """
    This function tests getting the character count.
    """
    my_count = char_count(value="AAABBBCCCCCCCDDDD", character="C")
    assert 7 == my_count


def test_1_2_char_count():
    """
    This function tests getting the character count.
    """
    my_count = char_count(value="AAABBBCCCCCCCDDDD", character="F")
    assert 0 == my_count
