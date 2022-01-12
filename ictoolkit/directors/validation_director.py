"""
This module is designed for validation checks. All modules will not return any data but throw exception errors when validation fails.
"""
# Built-in/Generic Imports
import logging
import sys
from typing import Union

# Own modules
from ictoolkit.helpers.py_helper import get_function_name, get_line_number

__author__ = 'IncognitoCoding'
__copyright__ = 'Copyright 2022, validation_director'
__credits__ = ['IncognitoCoding']
__license__ = 'GPL'
__version__ = '2.1'
__maintainer__ = 'IncognitoCoding'
__status__ = 'Production'


def value_type_validation(value: any, required_type: Union[type, list], caller_module: str, caller_line: int) -> None:
    """
    A simple type validation check. This function is designed to be widely used to check any values. No logging will take place within this function.
    The error output will have an origination location based on the error section.

    Error Output Origination:
        TypeError: Will originate from the calling function using the passing parameters.
        AttributeError: Will originate from the calling function using the passing parameters.
        Exception: Will originate within this function.

    Args:
        value (any): Any value needing its type validated.
        required_type (type or list of types): The required type the value should match. Can be a single type or list of types.
        caller_module (str): The name of the caller module. Use '__name__'.
        caller_line (int): The calling function line. Use 'ictoolkit.helpers.py_helper' to pull the line.

    Calling Example:
        value_type_validation('My String', str, __name__, get_line_number())
    """

    # ################################################################################################################################
    # Note: This module has to have manually formatted error output because the error_formatter uses this function to validate types.
    # ################################################################################################################################

    # Verifies a value is sent.
    if (
        value is None
        or value == ''
    ):
        error_message = (
            f'The value \'{value}\' sent is not an accepted input.\n'
            + (('-' * 150) + '\n') + (('-' * 65) + 'Additional Information' + ('-' * 63) + '\n') + (('-' * 150) + '\n')
            + 'Expected Result:\n'
            f'  - Type = Any value other than None or an empty string\n\n'
            'Returned Result:\n'
            f'  - Type = {type(value)}\n\n'
            + 'Suggested Resolution:\n'
            f'  - Please check the calling function.\n\n'
            f'Originating error on line {caller_line} in <{caller_module}>\n'
            + (('-' * 150) + '\n') * 2
        )
        raise AttributeError(error_message)

    # Verifies a type or list is sent.
    if (
        not (isinstance(required_type, list) or isinstance(required_type, type))
    ):
        error_message = (
            f'No type or list of types has been entered for type validation.\n'
            + (('-' * 150) + '\n') + (('-' * 65) + 'Additional Information' + ('-' * 63) + '\n') + (('-' * 150) + '\n')
            + 'Expected Result:\n'
            f'  - Type = type or list of types\n\n'
            'Returned Result:\n'
            f'  - Type = {type(required_type)}\n\n'
            + 'Suggested Resolution:\n'
            f'  - Please check the calling function.\n\n'
            f'Originating error on line {caller_line} in <{caller_module}>\n'
            + (('-' * 150) + '\n') * 2
        )
        raise AttributeError(error_message)

    # Verifies the caller module is sent.
    if not isinstance(caller_module, str):
        error_message = (
            f'The caller_module \'{caller_module}\' sent is not an accepted input.\n'
            + (('-' * 150) + '\n') + (('-' * 65) + 'Additional Information' + ('-' * 63) + '\n') + (('-' * 150) + '\n')
            + 'Expected Result:\n'
            f'  - Type = {required_type}\n\n'
            'Returned Result:\n'
            f'  - Type = {type(caller_module)}\n\n'
            + 'Suggested Resolution:\n'
            f'  - Please check the calling function.\n\n'
            f'Originating error on line {caller_line} in <{caller_module}>\n'
            + (('-' * 150) + '\n') * 2
        )
        raise AttributeError(error_message)

    # Verifies the caller line number is sent.
    if not isinstance(caller_line, int):
        error_message = (
            f'The caller_line \'{caller_line}\' sent is not an accepted input.\n'
            + (('-' * 150) + '\n') + (('-' * 65) + 'Additional Information' + ('-' * 63) + '\n') + (('-' * 150) + '\n')
            + 'Expected Result:\n'
            f'  - Type = {required_type}\n\n'
            'Returned Result:\n'
            f'  - Type = {type(caller_line)}\n\n'
            + 'Suggested Resolution:\n'
            f'  - Please check the calling function.\n\n'
            f'Originating error on line {caller_line} in <{caller_module}>\n'
            + (('-' * 150) + '\n') * 2
        )
        raise AttributeError(error_message)

    try:
        # Checks if the required type option one type or multiple.
        if isinstance(required_type, list):
            for value_type in required_type:
                if isinstance(value, value_type):
                    matching_type_flag = True
                    break
                else:
                    matching_type_flag = False
        else:
            if not isinstance(value, required_type):
                matching_type_flag = False
            else:
                matching_type_flag = True

        # Checks for no match.
        if matching_type_flag is False:
            error_message = (
                f'The value \'{value}\' is not in {required_type} format.\n'
                + (('-' * 150) + '\n') + (('-' * 65) + 'Additional Information' + ('-' * 63) + '\n') + (('-' * 150) + '\n')
                + 'Expected Result:\n'
                f'  - Type = {required_type}\n\n'
                'Returned Result:\n'
                f'  - Type = {type(value)}\n\n'
                f'Originating error on line {caller_line} in <{caller_module}>\n'
                + (('-' * 150) + '\n') * 2
            )
            raise TypeError(error_message)
    except TypeError as error:
        raise error
    except Exception as error:
        # Converts the error into a formatted string with tab spacing.
        original_error = str('\n            ' + '\n            '.join(map(str, str(error).splitlines())))
        error_message = (
            f'A general error has occurred while validating a value type.\n'
            + (('-' * 150) + '\n') + (('-' * 65) + 'Additional Information' + ('-' * 63) + '\n') + (('-' * 150) + '\n')
            + 'Returned Result:\n'
            '  - Original Exception listed below:\n\n'
            + '            ' + (('~' * 150) + '\n            ') + (('~' * 63) + 'Start Original Exception' + ('~' * 63) + '\n            ') + (('~' * 150) + '\n            \n')
            + f'{original_error}\n\n'
            + '            ' + (('~' * 150) + '\n            ') + (('~' * 65) + 'End Original Exception' + ('~' * 63) + '\n            ') + (('~' * 150) + '\n            \n\n')
            + f'Originating error on line {error.__traceback__.tb_lineno} in <{__name__}>\n'
            + (('-' * 150) + '\n') * 2
        )
        raise Exception(error_message)


def key_validation(values: dict, required_keys: Union[str, list], caller_module: str, caller_line: int) -> None:
    """
    A simple dictionary key validation check. This function is designed to be widely used to check any values.
    The error output will have an origination location based on the error section.

    Error Output Origination:
        KeyError: Will originate from the calling function using the passing parameters.
        AttributeError: Will originate from the calling function using the passing parameters.
        Exception: Will originate within this function.

    Args:
        values (dict): A dictionary that needs the keys validated.
        required_key (Union[str, list])): The required key(s) that should match. Can be a single str or list of keys.
        caller_module (str): The name of the caller module. Use '__name__'.
        caller_line (int): The calling function line. Use 'ictoolkit.helpers.py_helper' to pull the line.
    """
    # Checks function launch variables and logs passing parameters.
    try:
        # Validates required types.
        value_type_validation(values, dict, __name__, get_line_number())
        value_type_validation(required_keys, [str, list], __name__, get_line_number())
        value_type_validation(caller_module, str, __name__, get_line_number())
        value_type_validation(caller_line, int, __name__, get_line_number())
    except Exception as error:
        if 'Originating error on line' in str(error):
            raise error
        else:
            # Converts the error into a formatted string with tab spacing.
            original_error = str('\n            ' + '\n            '.join(map(str, str(error).splitlines())))
            error_message = (
                f'A general exception occurred during the value type validation.\n'
                + (('-' * 150) + '\n') + (('-' * 65) + 'Additional Information' + ('-' * 63) + '\n') + (('-' * 150) + '\n')
                + 'Returned Result:\n'
                '  - Original Exception listed below:\n\n'
                + '            ' + (('~' * 150) + '\n            ') + (('~' * 63) + 'Start Original Exception' + ('~' * 63) + '\n            ') + (('~' * 150) + '\n            \n')
                + f'{original_error}\n\n'
                + '            ' + (('~' * 150) + '\n            ') + (('~' * 65) + 'End Original Exception' + ('~' * 63) + '\n            ') + (('~' * 150) + '\n            \n\n')
                + f'Originating error on line {error.__traceback__.tb_lineno} in <{__name__}>\n'
                + (('-' * 150) + '\n') * 2
            )
            raise Exception(error_message)

    try:
        dict_keys: list = list(values.keys())
        mismatched_input: bool
        # Checks 1:1 input and requirement.
        if isinstance(required_keys, list):
            if len(required_keys) != len(dict_keys):
                mismatched_input = True
            else:
                mismatched_input = False
        else:
            if len(values) > 1:
                mismatched_input = True
            else:
                mismatched_input = False

        if mismatched_input is True:
            error_message = (
                f'A dictionary key validation could not be performed because of inconsistent value and requirement key input.\n'
                + (('-' * 150) + '\n') + (('-' * 65) + 'Additional Information' + ('-' * 63) + '\n') + (('-' * 150) + '\n')
                + 'Returned Result:\n'
                f'  - values = {dict_keys}\n'
                f'  - required_keys = {required_keys}\n\n'
                f'Originating error on line {caller_line} in <{caller_module}>\n'
                + (('-' * 150) + '\n') * 2
            )
            raise AttributeError(error_message)

        # Checks for duplicate values.
        if isinstance(required_keys, list):
            if len(required_keys) != len(set(required_keys)):
                error_message = (
                    f'The required key list contains duplicate keys. All keys must be unique.\n'
                    + (('-' * 150) + '\n') + (('-' * 65) + 'Additional Information' + ('-' * 63) + '\n') + (('-' * 150) + '\n')
                    + 'Returned Result:\n'
                    f'  - required_keys = {required_keys}\n\n'
                    f'Originating error on line {caller_line} in <{caller_module}>\n'
                    + (('-' * 150) + '\n') * 2
                )
                raise AttributeError(error_message)

        # Loops through to find any keys that do not match.
        dict_keys: list = list(values.keys())
        # Sets the keys in reverse order so the no-match is the last entry checked
        # but the first no-match in the list of keys.
        sorted_dict_keys: list = sorted(dict_keys, reverse=True)

        if isinstance(required_keys, list):
            required_keys: list
            for required_key in required_keys:
                for dict_key in sorted_dict_keys:
                    if required_key == dict_key:
                        no_matching_key = None
                        break
                    else:
                        no_matching_key = required_key
                # If a match is not found on the first required
                # key check the loop will exit and return the no-matched key.
                if no_matching_key:
                    break
        else:
            # Variable name swap for easier loop reading.
            required_key: str = required_keys
            for dict_key in sorted_dict_keys:
                if required_key == dict_key:
                    no_matching_key = None
                    break
                else:
                    no_matching_key = required_key

        # Checks if a no matching key exists, to output the error
        if no_matching_key:
            error_message = (
                f'The dictionary key (\'{no_matching_key}\') does not exist in the sent data.\n'
                + (('-' * 150) + '\n') + (('-' * 65) + 'Additional Information' + ('-' * 63) + '\n') + (('-' * 150) + '\n')
                + 'Expected Result:\n'
                f'  - Key = {required_keys}\n\n'
                'Returned Result:\n'
                f'  - Keys = {dict_keys}\n\n'
                f'Originating error on line {caller_line} in <{caller_module}>\n'
                + (('-' * 150) + '\n') * 2
            )
            raise KeyError(error_message)
    except Exception as error:
        # Converts the error into a formatted string with tab spacing.
        original_error = str('\n            ' + '\n            '.join(map(str, str(error).splitlines())))
        error_message = (
            f'A general exception occurred during the value key validation.\n'
            + (('-' * 150) + '\n') + (('-' * 65) + 'Additional Information' + ('-' * 63) + '\n') + (('-' * 150) + '\n')
            + 'Returned Result:\n'
            '  - Original Exception listed below:\n\n'
            + '            ' + (('~' * 150) + '\n            ') + (('~' * 63) + 'Start Original Exception' + ('~' * 63) + '\n            ') + (('~' * 150) + '\n            \n')
            + f'{original_error}\n\n'
            + '            ' + (('~' * 150) + '\n            ') + (('~' * 65) + 'End Original Exception' + ('~' * 63) + '\n            ') + (('~' * 150) + '\n            \n\n')
            + f'Originating error on line {error.__traceback__.tb_lineno} in <{__name__}>\n'
            + (('-' * 150) + '\n') * 2
        )
        raise Exception(error_message)