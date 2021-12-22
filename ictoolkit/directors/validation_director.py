"""
This module is designed for validation checks. All modules will not return any data but throw exception errors when validation fails.
"""
# Built-in/Generic Imports
import traceback
from typing import Union

__author__ = 'IncognitoCoding'
__copyright__ = 'Copyright 2021, validation_director'
__credits__ = ['IncognitoCoding']
__license__ = 'GPL'
__version__ = '1.6'
__maintainer__ = 'IncognitoCoding'
__status__ = 'Development'


def value_type_validation(value: any, required_type: Union[type, list], caller_module: str, caller_line: int) -> None:
    """
    A simple type validation validation check. This function is designed to be widely used to check any values. No logging will take place within this function.
    All error output will list that the information originated from the calling function.

    Error Output Origination:
        - TypeError: Will originate from the calling function using the passing parameters.
        - AttributeError: Will originate within this function.
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

    # Verifies a value is sent.
    if (
        value is None
        or value == ''
    ):
        error_message = (
            f'The value \'{value}\' sent is not an accepted input.\n'
            + (('-' * 150) + '\n') + (('-' * 65) + 'Additional Information' + ('-' * 63) + '\n') + (('-' * 150) + '\n')
            + 'Suggested Resolution:\n'
            f'  - Please check the calling function.\n\n'
            + f'Originating error on line {traceback.extract_stack()[-1].lineno} in <{__name__}>\n'
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
            + 'Suggested Resolution:\n'
            f'  - Please check the calling function.\n\n'
            + f'Originating error on line {traceback.extract_stack()[-1].lineno} in <{__name__}>\n'
            + (('-' * 150) + '\n') * 2
        )
        raise AttributeError(error_message)

    # Verifies the caller module is sent.
    if not isinstance(caller_module, str):
        error_message = (
            f'The caller_module \'{caller_module}\' sent is not an accepted input.\n'
            + (('-' * 150) + '\n') + (('-' * 65) + 'Additional Information' + ('-' * 63) + '\n') + (('-' * 150) + '\n')
            + 'Suggested Resolution:\n'
            f'  - Please check the calling function.\n\n'
            + f'Originating error on line {traceback.extract_stack()[-1].lineno} in <{__name__}>\n'
            + (('-' * 150) + '\n') * 2
        )
        raise AttributeError(error_message)

    # Verifies the caller line number is sent.
    if not isinstance(caller_line, int):
        error_message = (
            f'The caller_line \'{caller_line}\' sent is not an accepted input.\n'
            + (('-' * 150) + '\n') + (('-' * 65) + 'Additional Information' + ('-' * 63) + '\n') + (('-' * 150) + '\n')
            + 'Suggested Resolution:\n'
            f'  - Please check the calling function.\n\n'
            + f'Originating error on line {traceback.extract_stack()[-1].lineno} in <{__name__}>\n'
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
