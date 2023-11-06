# Built-in/Generic Imports
from dataclasses import asdict
import pytest

# Local Functions
from ictoolkit.data_structure.dataclass import create_dataclass


__author__ = "IncognitoCoding"
__copyright__ = "Copyright 2022, test_dataclass"
__credits__ = ["IncognitoCoding"]
__license__ = "MIT"
__version__ = "0.2"
__maintainer__ = "IncognitoCoding"
__status__ = "Production"


def test_create_dataclass():
    """
    This tests creating a dataclass.

    Raises:
    """
    print("")
    print("-" * 65)
    print("-" * 65)
    print("Testing Function: create_dataclass")
    print("-" * 65)
    print("-" * 65)
    print("")

    # ############################################################
    # ######Section Test Part 1 (Successful Value Checking)#######
    # ############################################################
    # =====================================================
    # ========Tests for a successful output return.========
    # =====================================================
    # Creating the dictionary
    my_dict = {"name": "Bob", "room_number": 1223, "teaching_subject": "Python"}
    new_dataclass = create_dataclass(dataclass_name="MyTestClass", my_dict=my_dict)
    assert """<class '__main__.MyTestClass'>""" == str(type(new_dataclass))
    assert """MyTestClass()""" == str(new_dataclass)
    assert """{'name': 'Bob', 'room_number': 1223, 'teaching_subject': 'Python'}""" == str(asdict(new_dataclass))
    assert "Bob" == str(new_dataclass.name)
    assert 1223 == int(new_dataclass.room_number)
    assert "Python" == str(new_dataclass.teaching_subject)

    # Tests changing dataclass value.
    new_dataclass.name = "John"
    assert "John" == str(new_dataclass.name)

    # =====================================================
    # ========Tests for a successful output return.========
    # =====================================================
    # Creating the dictionary
    my_dict = [
        {"name": "Bob", "room_number": 1223, "teaching_subject": "Python"},
        {"name": "Tim", "room_number": 1333, "teaching_subject": "Python2"},
    ]

    new_dataclass = create_dataclass(dataclass_name="MyTestClass", my_dict=my_dict)
    assert """<class 'list'>""" == str(type(new_dataclass))
    assert """<class '__main__.MyTestClass'>""" == str(type(new_dataclass[0]))
    assert """{'name': 'Bob', 'room_number': 1223, 'teaching_subject': 'Python'}""" == str(asdict(new_dataclass[0]))
    assert """{'name': 'Tim', 'room_number': 1333, 'teaching_subject': 'Python2'}""" == str(asdict(new_dataclass[1]))

    # ############################################################
    # ######Section Test Part 2 (Error/Catch Value Checking)######
    # ############################################################
    # =====================================================
    # ========Tests for an incorrectly sent info.==========
    # =====================================================
    # =====================================================
    # ========Tests for an incorrectly sent info.==========
    # =====================================================
    with pytest.raises(Exception) as excinfo:
        my_dict = {"name": "Bob", "room_number": 1223, "teaching_subject": "Python"}
        req_keys = {"name", "room_number", "teaching_subject", "grade_level"}
        new_dataclass = create_dataclass("MyTestClass", my_dict=my_dict, req_keys=req_keys)

    assert """MyTestClass got an unexpected keyword argument.""" in str(excinfo.value)
    assert """'grade_level', 'name', 'room_number', 'teaching_subject'""" in str(excinfo.value)
    assert """'name', 'room_number', 'teaching_subject'""" in str(excinfo.value)

    # =====================================================
    # ========Tests for an incorrectly sent info.==========
    # =====================================================
    with pytest.raises(Exception) as excinfo:
        my_dict = [
            {"name": "Bob", "room_number": 1223, "teaching_subject": "Python"},
            {"name": "Tim", "teaching_subject": "Python2", "teaching_subject": "Python2"},
        ]
        new_dataclass = create_dataclass(dataclass_name="MyTestClass", my_dict=my_dict)
    assert """MyTestClass got an unexpected keyword argument.""" in str(excinfo.value)
    # =====================================================
    # ========Tests for an incorrectly sent info.==========
    # =====================================================
    with pytest.raises(Exception) as excinfo:
        my_dict = [
            {"name": "Bob", "room_number": 1223, "teaching_subject": "Python"},
            {"name": "Tim", "teaching_subject": "Python2"},
        ]
        req_keys = {"name", "room_number", "teaching_subject", "grade_level"}
        new_dataclass = create_dataclass("MyTestClass", my_dict=my_dict, req_keys=req_keys)
    assert """MyTestClass got an unexpected keyword argument.""" in str(excinfo.value)
