"""
This module is designed for validation checks. All modules will not return any data but throw exception errors when validation fails.

Some ictoolkit support modules that use the "value_type_validation" can not be imported (ex: error_formatter). Some code is duplicate to those modules.
"""
# Built-in/Generic Imports
from typing import Optional, Union, Any
import warnings
# Own modules
from ictoolkit.helpers.py_helper import get_function_name, get_line_number

__author__ = 'IncognitoCoding'
__copyright__ = 'Copyright 2022, validation_director'
__credits__ = ['IncognitoCoding']
__license__ = 'GPL'
__version__ = '2.2'
__maintainer__ = 'IncognitoCoding'
__status__ = 'Production'


class InvalidKeyError(Exception):
    """
    Exception raised for an invalid dictionary key.

    Built in KeyErrors do not format cleanly.

    Attributes:
        error_message: The invalid key reason.
    """
    error_message: str

    def __ini__(self, error_message: str) -> None:
        self.error_message = error_message


class TypeValidationError(Exception):
    """
    Exception raised for a a value type error.

    Attributes:
        message: The reason the value failure.
    """
    def __init__(self, error: Any, function_name: str, trackback: int) -> None:
        if 'Originating error on line' in str(error):
            raise error
        else:
            if type(error).__name__ == str('KeyError'):
                # KeyError output does not process the escape sequence cleanly. This fixes the output and removes the string double quotes.
                original_error = str('\n            ' + '\n            '.join(map(str, str(str(error).replace(r'\n', '\n')[1:-1]).splitlines())))
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
                + f'Originating error on line {function_name} in <{trackback}>\n'
                + (('-' * 150) + '\n') * 2
            )
            raise Exception(error_message)


class KeyCheck():
    """
    An advanced dictionary key checker that offers two different check options.

    Options:\\
    \tcontains_keys(): Checks if some required keys exist in the dictionary.\\
    \tall_keys(): Checks if all required keys exist in the dictionary.

    Args:
        values (dict): A dictionary that needs the keys validated.
        caller_module (str): The name of the caller module. Use '__name__'.
        caller_name (str): The name of the caller (func or method).
        caller_line (int): The calling function line. Use 'ictoolkit.helpers.py_helper' to pull the line.
    """
    def __init__(self, values: dict, caller_name: str, caller_module: str, caller_line: int) -> None:
        warnings.warn('Version 2.5 of ictoolkit deprecation. This module has been replaced with the fchecker module. '
                      'Please switch to using the fchecker module (pip install fchecker).', DeprecationWarning)

        # Checks function launch variables and logs passing parameters.
        try:
            # Validates required types.
            value_type_validation(values, dict, __name__, get_line_number())
            value_type_validation(caller_module, str, __name__, get_line_number())
            value_type_validation(caller_line, int, __name__, get_line_number())
        except Exception as error:
            raise TypeValidationError(error, __name__, error.__traceback__.tb_lineno)

        self._values = values
        self._caller_module = caller_module
        self._caller_name = caller_name
        self._caller_line = caller_line

    def contains_keys(self, required_keys: Union[str, list]):
        """
        Checks if some required keys exist in the dictionary.

        Reverse Tip:\\ 
        \tReverses the key check error output, so the expected result and returned results\\
        \tare flipped to allow value checks on expected dynamic keys.

        Args:
            required_keys (Union[str, list])): The required key(s) that should match. Can be a single str or list of keys.
            reverse (bool, optional): Reverses the key check error output, so the expected result and returned results are flipped.
        """
        # Checks function launch variables and logs passing parameters.
        try:
            value_type_validation(required_keys, [str, list], __name__, get_line_number())
        except Exception as error:
            raise TypeValidationError(error, __name__, error.__traceback__.tb_lineno)

        self._required_keys = required_keys
        self._all_key_check = False
        self._key_validation()

    def all_keys(self, required_keys: Union[str, list]):
        """
        Checks if all required keys exist in the dictionary

        Args:
            required_keys (Union[str, list])): The required key(s) that should match. Can be a single str or list of keys.
        """
        # Checks function launch variables and logs passing parameters.
        try:
            value_type_validation(required_keys, [str, list], __name__, get_line_number())
        except Exception as error:
            raise TypeValidationError(error, __name__, error.__traceback__.tb_lineno)

        self._required_keys = required_keys
        self._all_key_check = True
        self._key_validation()

    def _key_validation(self) -> None:
        try:
            # Checks for 1:1 input when using the all_keys option.
            if self._all_key_check:
                dict_keys: list = list(self._values.keys())
                mismatched_input: bool
                if isinstance(self._required_keys, list):
                    if len(self._required_keys) != len(dict_keys):
                        mismatched_input = True
                    else:
                        mismatched_input = False
                else:
                    if len(self._values) > 1:
                        mismatched_input = True
                    else:
                        mismatched_input = False

                if mismatched_input is True:
                    error_message = (
                        f'A dictionary key validation could not be performed because of inconsistent value and requirement key input.\n'
                        + (('-' * 150) + '\n') + (('-' * 65) + 'Additional Information' + ('-' * 63) + '\n') + (('-' * 150) + '\n')
                        + 'Returned Result:\n'
                        f'  - self._values = {dict_keys}\n'
                        f'  - self._required_keys = {self._required_keys}\n\n'
                        + f'Trace Details:\n'
                        f'  - Exception: AttributeError\n'
                        f'  - Module: {self._caller_module}\n'
                        f'  - Name: {self._caller_name}\n'
                        f'  - Line: {self._caller_line}\n'
                        + (('-' * 150) + '\n') * 2
                    )
                    raise AttributeError(error_message)

            # Checks for duplicate values.
            if isinstance(self._required_keys, list):
                if len(self._required_keys) != len(set(self._required_keys)):
                    error_message = (
                        f'The required key list contains duplicate keys. All keys must be unique.\n'
                        + (('-' * 150) + '\n') + (('-' * 65) + 'Additional Information' + ('-' * 63) + '\n') + (('-' * 150) + '\n')
                        + 'Returned Result:\n'
                        f'  - self._required_keys = {self._required_keys}\n\n'
                        + f'Trace Details:\n'
                        f'  - Exception: AttributeError\n'
                        f'  - Module: {self._caller_module}\n'
                        f'  - Name: {self._caller_name}\n'
                        f'  - Line: {self._caller_line}\n'
                        + (('-' * 150) + '\n') * 2
                    )
                    raise AttributeError(error_message)

            # Loops through to find any keys that do not match.
            dict_keys = list(self._values.keys())
            # Sets the keys in reverse order so the no-match is the last entry checked
            # but the first no-match in the list of keys.
            sorted_dict_keys = sorted(dict_keys, reverse=True)

            if isinstance(self._required_keys, list):
                for required_key in self._required_keys:
                    # Checks if the validation requires all the required keys
                    # to match all sorted_dict_keys or the required keys to match
                    # some of the sorted_dict_keys.
                    if self._all_key_check:
                        for dict_key in sorted_dict_keys:
                            # Checks for exact match.
                            if required_key == dict_key:
                                no_matching_key = None
                                break
                            else:
                                no_matching_key = required_key
                    else:
                        if required_key in sorted_dict_keys:
                            no_matching_key = None
                        else:
                            no_matching_key = required_key
                    # If a match is not found on the first required
                    # key check the loop will exit and return the no-matched key.
                    if no_matching_key:
                        break
            else:
                # Variable name swap for easier loop reading.
                required_key: str = self._required_keys
                for dict_key in sorted_dict_keys:
                    if required_key == dict_key:
                        # Checks for exact match.
                        no_matching_key = None
                        break
                    else:
                        no_matching_key = required_key

            # Checks if a no matching key exists, to output the error
            if no_matching_key:
                # Checks if the no matching key is in the required keys.
                # If the no matching key exists in the required keys the expected result and returned result will
                # be flipped, so the output is represented cleanly.
                # This can occur when using the reverse check.
                #   Example: A sample dictionary set is used to compare required keys.
                if no_matching_key in self._required_keys:
                    expected_key = dict_keys
                    returned_key = self._required_keys
                else:
                    expected_key = self._required_keys
                    returned_key = dict_keys

                # Formats the output based on the check option.
                if self._all_key_check:
                    main_message = f'The dictionary key (\'{no_matching_key}\') does not exist in the expected required key(s).\n'
                    expected_result = f'  - Required Key(s) = {expected_key}'
                    returned_result = f'  - Failed Key(s) = {returned_key}'
                else:
                    main_message = f'The dictionary key (\'{no_matching_key}\') does not match any expected match option key(s).\n'
                    expected_result = f'  - Match Option Key(s) = {expected_key}'
                    returned_result = f'  - Failed Key(s) = {returned_key}'

                error_message = (
                    f'{main_message}'
                    + (('-' * 150) + '\n') + (('-' * 65) + 'Additional Information' + ('-' * 63) + '\n') + (('-' * 150) + '\n')
                    + 'Expected Result:\n'
                    f'{expected_result}\n\n'
                    'Returned Result:\n'
                    f'{returned_result}\n\n'
                    + f'Trace Details:\n'
                    f'  - Exception: AttributeError\n'
                    f'  - Module: {self._caller_module}\n'
                    f'  - Name: {self._caller_name}\n'
                    f'  - Line: {self._caller_line}\n'
                    + (('-' * 150) + '\n') * 2
                )
                raise InvalidKeyError(error_message)
        except Exception as error:
            # Converts the error into a formatted string with tab spacing.
            original_error = str('\n            ' + '\n            '.join(map(str, str(error).splitlines())))
            if 'Originating error on line' in str(error):
                raise error
            else:
                error_message = (
                    f'A general exception occurred during the value key validation.\n'
                    + (('-' * 150) + '\n') + (('-' * 65) + 'Additional Information' + ('-' * 63) + '\n') + (('-' * 150) + '\n')
                    + 'Returned Result:\n'
                    '  - Original Exception listed below:\n\n'
                    + '            ' + (('~' * 150) + '\n            ') + (('~' * 63) + 'Start Original Exception' + ('~' * 63) + '\n            ') + (('~' * 150) + '\n            \n')
                    + f'{original_error}\n\n'
                    + '            ' + (('~' * 150) + '\n            ') + (('~' * 65) + 'End Original Exception' + ('~' * 63) + '\n            ') + (('~' * 150) + '\n            \n\n')
                    + f'Trace Details:\n'
                    f'  - Exception: AttributeError\n'
                    f'  - Module: {self._caller_module}\n'
                    f'  - Name: {self._caller_name}\n'
                    f'  - Line: {self._caller_line}\n'
                    + (('-' * 150) + '\n') * 2
                )
                raise Exception(error_message)


def value_type_validation(value: any, required_type: Union[type, list], caller_module: str, caller_line: int) -> None:
    """
    A simple type validation validation check. This function is designed to be widely used to check any values. No logging will take place within this function.
    The error output will have an origination location based on the error section.

    Error Output Origination:
        - TypeError: Will originate from the calling function using the passing parameters.
        - AttributeError: Will originate from the calling function using the passing parameters.
        - Exception: Will originate within this function.

    Args:
        value (any): Any value needing its type validated.
        required_type (type or list of types): The required type the value should match. Can be a single type or list of types.
        caller_module (str): The name of the caller module. Use '__name__'.
        caller_line (int): The calling function line. Use 'ictoolkit.helpers.py_helper' to pull the line.

    Raises:
        AttributeError: The value '{value}' sent is not an accepted input.
        AttributeError: No type or list of types has been entered for type validation.
        AttributeError: The caller_module '{caller_module}' sent is not an accepted input.
        AttributeError: The caller_line '{caller_line}' sent is not an accepted input.
        TypeError: The value '{value}' is not in {required_type} format.
        Exception: A general error has occurred while validating a value type.

    Calling Example:
        value_type_validation('My String', str, __name__, get_line_number())
    """

    # ################################################################################################################################
    # Note: This module has to have manually formatted error output because the error_formatter uses this function to validate types.
    # ################################################################################################################################

    warnings.warn('Version 2.5 of ictoolkit deprecation. This module has been replaced with the fchecker module. '
                  'Please switch to using the fchecker module (pip install fchecker).', DeprecationWarning)

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
