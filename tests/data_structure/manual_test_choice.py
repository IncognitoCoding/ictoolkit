"""Must run with -s"""
# Built-in/Generic Imports
from dataclasses import asdict
from typing import Any, Union
import pytest

# Local Functions
from ictoolkit.data_structure.choice import user_choice_character_grouping


# Exceptions
from fexception import FValueError


__author__ = "IncognitoCoding"
__copyright__ = "Copyright 2022, test_choice"
__credits__ = ["IncognitoCoding"]
__license__ = "MIT"
__version__ = "0.1"
__maintainer__ = "IncognitoCoding"
__status__ = "Production"


# ############################################################
# ######Section Test Part 1 (Successful Value Checking)#######
# ############################################################


def test_1_user_choice_character_grouping():
    """
    This function tests getting the users character grouping.
    """
    sample_list = ["TI-MyTest1", "TI-MyTest2", "KV1-MyTest1", "KV1-MyTest2", "WZ-MyTest1", "kv1-MyTest3", "kv2-MyTest1"]
    print("Manual run instructions")
    print("")
    print("Select 'Yes' to continue, Character Position Number, Enter 2 for the character position")
    grouped_characters = user_choice_character_grouping(sample_list)

    group_count = len(list(grouped_characters.keys()))
    print(group_count)
    for group in grouped_characters.items():
        print(group)
    # Need To Add Pytest Instructions.
    # Expected Return Example:
    # ('KV', ['KV-MyTest1', 'KV-MyTest2'])
    # ('TI', ['TI-MyTest1', 'TI-MyTest2'])
    # ('WZ', ['WZ-MyTest1'])

    # Test moving the same values back to the same group.


# ############################################################
# ######Section Test Part 2 (Error/Catch Value Checking)######
# ############################################################


def test_2_user_choice_character_grouping():
    """
    Tests sending an invalid list_of_strings type.
    """
    with pytest.raises(Exception) as excinfo:
        grouped_characters = user_choice_character_grouping(list_of_strings={"invalid Type"})
    assert (
        """The object value '{'invalid Type'}' is not an instance of the required class(es) or subclass(es)."""
        in str(excinfo.value)
    )
