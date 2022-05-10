"""
This script is used to test the file_director module using pytest.
A sample file is used for writing and reading. The last testing function will remove the testing file.
"""

# Built-in/Generic Imports
import os

# Local Functions
from fchecker.type import type_check
from ictoolkit import write_file, search_file, convert_relative_to_full_path

# Exceptions
from fexception import FTypeError, FValueError


def test_write_file():
    """
    Tests writing a file.

    Raises:
        ValueError: A failure occurred in section 1.0 while testing the function 'write_file'. The test did not write.
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
    # Gets the programs root directory.
    preset_root_directory = os.path.dirname(os.path.realpath(__file__))

    # Sets the sample save file path.
    # No return value. Throws an exception if the file does not write.
    sample_write_file_path = os.path.abspath(f"{preset_root_directory}\\temp_pytest_read_write.py")

    try:
        # Writes to file.
        # This temp file is used for additional tests in other functions.
        write_file(sample_write_file_path, "testing line1")
        write_file(sample_write_file_path, "testing line2")
        write_file(sample_write_file_path, "testing line3")
    except Exception as exc:
        exc_args = {
            "main_message": "A failure occurred in section 1.0 while testing the function 'write_file'. The test did not write.",
            "expected_result": "non-list error",
            "returned_result": exc,
        }
        raise FValueError(exc_args)


def test_search_file():
    """
    Tests searching a file.

    Raises:
        ValueError: A failure occurred in section 1.0 while testing the function 'search_file'. The function did not return a type 'list'.
        ValueError: A failure occurred in section 1.1 while testing the function 'search_file'. The returned search list length should have equaled 1.
        ValueError: A failure occurred in section 1.2 while testing the function 'search_multiple_files' with a single search value against multiple paths.. The function did not return a type \'list\'.
        ValueError: A failure occurred in section 1.3 while testing the function 'search_multiple_files' with a single search value against multiple paths. The returned search list length should have equaled 2.
        ValueError: A failure occurred in section 1.4 while testing the function 'search_multiple_files' with multiple search values against multiple paths. The function did not return a type \'list\'.
        ValueError: A failure occurred in section 1.5 while testing the function 'search_multiple_files' with multiple search values against multiple paths. The returned search list length should have equaled 2.
    """
    print("")
    print("-" * 65)
    print("-" * 65)
    print("Testing Function: search_file")
    print("-" * 65)
    print("-" * 65)
    print("")

    # ############################################################
    # ######Section Test Part 1 (Successful Value Checking)#######
    # ############################################################
    # ========Tests for a successful output return.========
    # Gets the programs root directory.
    preset_root_directory = os.path.dirname(os.path.realpath(__file__))
    # Sets the sample file path.
    sample_file_path = os.path.abspath(f"{preset_root_directory}\\temp_pytest_read_write.py")
    found_value = search_file(sample_file_path, "line1")

    try:
        type_check(found_value, list)
    except FTypeError as exc:
        exc_args = {
            "main_message": "A failure occurred in section 1.0 while testing the function 'search_file'. The function did not return a type 'list'.",
            "expected_result": "non-list error",
            "returned_result": exc,
        }
        raise FValueError(exc_args)

    # Return length should equal 1.
    # Expected Return: [{'search_entry': 'line1', 'found_entry': 'testing line1'}]
    if len(found_value) != 1:
        exc_args = {
            "main_message": "A failure occurred in section 1.1 while testing the function 'search_file'. The returned search list length should have equaled 1.",
        }
        raise FValueError(exc_args)

    # ========Tests for a successful output return.========
    # Gets the programs root directory.
    preset_root_directory = os.path.dirname(os.path.realpath(__file__))

    # Sets the sample file path.
    sample_file_path = os.path.abspath(f"{preset_root_directory}\\temp_pytest_read_write.py")

    # Single search value against the same path twice.
    found_value = search_file(list([sample_file_path, sample_file_path]), "line1")

    try:
        type_check(found_value, list)
    except FTypeError as exc:
        exc_args = {
            "main_message": "A failure occurred in section 1.2 while testing the function 'search_multiple_files' with a single search value against multiple paths.. The function did not return a type 'list'.",
            "expected_result": "non-list error",
            "returned_result": exc,
        }
        raise FValueError(exc_args)

    # Return length should equal 2.
    # Expected Return: [{'search_entry': 'line1', 'found_entry': 'testing line1'}, {'search_entry': 'line1', 'found_entry': 'testing line1'}]
    if len(found_value) != 2:
        exc_args = {
            "main_message": "A failure occurred in section 1.3 while testing the function 'search_multiple_files' with a single search value against multiple paths. The returned search list length should have equaled 2.",
        }
        raise FValueError(exc_args)

    # ========Tests for a successful output return.========
    # Multi search value against the same path twice.
    found_value = search_file(list([sample_file_path, sample_file_path]), list(["line1", "line2"]))

    try:
        type_check(found_value, list)
    except FTypeError as exc:
        exc_args = {
            "main_message": "A failure occurred in section 1.4 while testing the function 'search_multiple_files' with multiple search values against multiple paths. The function did not return a type 'list'.",
            "expected_result": "non-list error",
            "returned_result": exc,
        }
        raise FValueError(exc_args)

    # Return length should equal 2.
    # Expected Return: [{'search_entry': ['line1', 'line2'], 'found_entry': 'testing line1'}, {'search_entry': ['line1', 'line2'], 'found_entry': 'testing line2'}]
    if len(found_value) != 2:
        exc_args = {
            "main_message": "A failure occurred in section 1.5 while testing the function 'search_multiple_files' with multiple search values against multiple paths. The returned search list length should have equaled 2.",
        }
        raise FValueError(exc_args)

    # Removes the testing file once the test is complete.
    os.remove(sample_file_path)


def test_convert_relative_to_full_path():
    """
    Tests converting a relative path to a full path.

    Raises:
        ValueError: A failure occurred in section 1.0 while testing the function 'convert_relative_to_full_path'. The full path did not return correctly.
    """
    print("")
    print("-" * 65)
    print("-" * 65)
    print("Testing Function: convert_relative_to_full_path")
    print("-" * 65)
    print("-" * 65)
    print("")

    # ############################################################
    # ######Section Test Part 1 (Successful Value Checking)#######
    # ############################################################
    # ========Tests for a successful output return.========
    full_path = convert_relative_to_full_path("mytest\\sample.txt")

    if "\\mytest\\sample.txt" not in full_path:
        exc_args = {
            "main_message": "A failure occurred in section 1.0 while testing the function 'convert_relative_to_full_path'. The full path did not return correctly.",
        }
        raise FValueError(exc_args)
