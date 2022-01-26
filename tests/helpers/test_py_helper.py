
"""
This script is used to test the validation_director module using pytest.

Run: py.test to validate.
"""
# Built-in/Generic Imports
import traceback

# Local Functions
from ictoolkit import get_line_number
from ictoolkit import get_function_name


def test_get_line_number():
    """
    This function tests validating a value type.

    Raises:
        ValueError: The line number did not return correctly.
    """
    print('')
    print('-' * 65)
    print('-' * 65)
    print('Testing Function: get_line_number')
    print('-' * 65)
    print('-' * 65)
    print('')
    # ############################################################
    # ######Section Test Part 1 (Successful Value Checking)#######
    # ############################################################
    # ========Tests for a successful output return.========
    line = get_line_number()

    if not isinstance(line, int):
        error_message = (
            f'The line number did not return correctly.\n'
            + (('-' * 150) + '\n') + (('-' * 65) + 'Additional Information' + ('-' * 63) + '\n') + (('-' * 150) + '\n')
            + 'Expected Result:\n'
            f'  - Type = int\n\n'
            'Returned Result:\n'
            f'  - Type = {type(line)}\n\n'
            f'Originating error on line {traceback.extract_stack()[-1].lineno} in <{__name__}>\n'
            + (('-' * 150) + '\n') * 2
        )
        raise TypeError(error_message)


def test_get_function_name():
    """
    This function tests validating a value type.

    Raises:
        ValueError: The function name did not return correctly.
    """
    print('')
    print('-' * 65)
    print('-' * 65)
    print('Testing Function: get_function_name')
    print('-' * 65)
    print('-' * 65)
    print('')
    # ############################################################
    # ######Section Test Part 1 (Successful Value Checking)#######
    # ############################################################
    # ========Tests for a successful output return.========
    function_name = get_function_name()

    if not isinstance(function_name, str):
        error_message = (
            f'The function name did not return correctly.\n'
            + (('-' * 150) + '\n') + (('-' * 65) + 'Additional Information' + ('-' * 63) + '\n') + (('-' * 150) + '\n')
            + 'Expected Result:\n'
            f'  - Type = str\n\n'
            'Returned Result:\n'
            f'  - Type = {type(function_name)}\n\n'
            f'Originating error on line {traceback.extract_stack()[-1].lineno} in <{__name__}>\n'
            + (('-' * 150) + '\n') * 2
        )
        raise TypeError(error_message)
