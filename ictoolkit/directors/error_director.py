"""
This module creates formatted error output for clean consistency across all modules. All modules will not return any data but throw exception errors when validation fails.
"""

# Own modules
from ictoolkit.directors.validation_director import value_type_validation
from ictoolkit.helpers.py_helper import get_line_number

__author__ = 'IncognitoCoding'
__copyright__ = 'Copyright 2022, error_director'
__credits__ = ['IncognitoCoding']
__license__ = 'GPL'
__version__ = '2.1'
__maintainer__ = 'IncognitoCoding'
__status__ = 'Production'


def error_formatter(error_args: dict, caller_module: str, caller_line: int) -> None:
    """
    An error formatter to create consistent error output. No logging will take place within this function.
    The error output will have an origination location based on the error section. Any formatted raised errors will originate
    from the calling function. All local function or Attribute errors will originate from this function.

    You can use many different variations in error_args to format a custom formatted message.
    The only two required error_args dictionary values are "error_message" and "type_error".

    Args:
        error_args (dict): Dictionary values to populate the formatted error message.
        \tParmaters:\\
        \t\tmain_message (str): The main error message.\\
        \t\ttype_error (error type): The error type. Example: KeyError, ValueError, TypeError.\\
        \t\texpected_result (Union[str, list], Optional): The expected result.\\
        \t\t\tstr vs list:
        \t\t\t\tA string will be a single formatted line.\\
        \t\t\t\tA list will be split into individual formatted lines.\\
        \t\treturned_result (Union[str, list], Optional): The returned result.\\
        \t\t\tstr vs list:
        \t\t\t\tA string will be a single formatted line.\\
        \t\t\t\tA list will be split into individual formatted lines.\\
        \t\tsuggested_resolution (Union[str, list], Optional): A suggested resolution.\\
        \t\t\tstr vs list:
        \t\t\t\tA string will be a single formatted line.\\
        \t\t\t\tA list will be split into individual formatted lines.\\
        \t\toriginal_error (any, Optional): The original error.\\
        caller_module (str): The name of the caller module. Use '__name__'.
        caller_line (int): The calling function line. Use 'ictoolkit.helpers.py_helper' to pull the line.
    """
    # Checks function launch variables and logs passing parameters.
    try:
        # Validates required types.
        value_type_validation(error_args, dict, __name__, get_line_number())
        value_type_validation(caller_module, str, __name__, get_line_number())
        value_type_validation(caller_line, int, __name__, get_line_number())
    except Exception as error:
        if 'Originating error on line' in str(error):
            raise error
        else:
            error_args = {
                'main_message': 'A general exception occurred during the value type validation.',
                'error_type': Exception,
                'original_error': error,
            }
            error_formatter(error_args, __name__, error.__traceback__.tb_lineno)

    # Gets all error_args.
    try:
        main_message = error_args.get('main_message')
        error_type = error_args.get('error_type')
        expected_result = error_args.get('expected_result')
        returned_result = error_args.get('returned_result')
        suggested_resolution = error_args.get('suggested_resolution')
        original_error = error_args.get('original_error')

        # Validates sent values. main_message and error_type are required.
        # The original_error is not validated because the error could be different class types or whatever the user chooses.
        value_type_validation(main_message, str, __name__, get_line_number())
        value_type_validation(error_type, type, __name__, get_line_number())
    except Exception as error:
        raise error

    try:
        if expected_result:
            if isinstance(expected_result, list):
                formatted_expected_result = str('  - ' + '\n  - '.join(map(str, expected_result)))
            else:
                formatted_expected_result = f'  - {expected_result}'
        if returned_result:
            if isinstance(returned_result, list):
                formatted_returned_result = str('  - ' + '\n  - '.join(map(str, returned_result)))
            else:
                formatted_returned_result = f'  - {returned_result}'
        if suggested_resolution:
            if isinstance(suggested_resolution, list):
                formatted_suggested_resolution = str('  - ' + '\n  - '.join(map(str, suggested_resolution)))
            else:
                formatted_suggested_resolution = f'  - {suggested_resolution}'
        if original_error:
            formatted_original_error = str('\n            ' + '\n            '.join(map(str, str(original_error).splitlines())))

        # Checks which variables are populated with data to create the formatted error message.
        if (
            main_message
            and not expected_result
            and not returned_result
            and not suggested_resolution
            and not original_error
        ):
            error_message = (
                f'{main_message}\n'
                + (('-' * 150) + '\n') + (('-' * 65) + 'Additional Information' + ('-' * 63) + '\n') + (('-' * 150) + '\n')
                + 'None provided\n\n'
                f'Originating error on line {caller_line} in <{caller_module}>\n'
                + (('-' * 150) + '\n') * 2
            )
            raise error_type(error_message)
        elif (
            main_message
            and expected_result
            and not returned_result
            and not suggested_resolution
            and not original_error
        ):
            error_message = (
                f'{main_message}\n'
                + (('-' * 150) + '\n') + (('-' * 65) + 'Additional Information' + ('-' * 63) + '\n') + (('-' * 150) + '\n')
                + 'Expected Result:\n'
                f'{formatted_expected_result}\n\n'
                f'Originating error on line {caller_line} in <{caller_module}>\n'
                + (('-' * 150) + '\n') * 2
            )
            raise error_type(error_message)
        elif (
            main_message
            and expected_result
            and returned_result
            and not suggested_resolution
            and not original_error
        ):
            error_message = (
                f'{main_message}\n'
                + (('-' * 150) + '\n') + (('-' * 65) + 'Additional Information' + ('-' * 63) + '\n') + (('-' * 150) + '\n')
                + 'Expected Result:\n'
                f'{formatted_expected_result}\n\n'
                'Returned Result:\n'
                f'{formatted_returned_result}\n\n'
                f'Originating error on line {caller_line} in <{caller_module}>\n'
                + (('-' * 150) + '\n') * 2
            )
            raise error_type(error_message)
        elif (
            main_message
            and expected_result
            and returned_result
            and suggested_resolution
            and not original_error
        ):
            error_message = (
                f'{main_message}\n'
                + (('-' * 150) + '\n') + (('-' * 65) + 'Additional Information' + ('-' * 63) + '\n') + (('-' * 150) + '\n')
                + 'Expected Result:\n'
                f'{formatted_expected_result}\n\n'
                'Returned Result:\n'
                f'{formatted_returned_result}\n\n'
                'Suggested Resolution:\n'
                f'{formatted_suggested_resolution}\n\n'
                f'Originating error on line {caller_line} in <{caller_module}>\n'
                + (('-' * 150) + '\n') * 2
            )
            raise error_type(error_message)
        elif (
            main_message
            and expected_result
            and returned_result
            and suggested_resolution
            and original_error
        ):
            error_message = (
                f'{main_message}\n'
                + (('-' * 150) + '\n') + (('-' * 65) + 'Additional Information' + ('-' * 63) + '\n') + (('-' * 150) + '\n')
                + 'Expected Result:\n'
                f'{formatted_expected_result}\n\n'
                'Returned Result:\n'
                f'{formatted_returned_result}\n\n'
                'Original Exception:\n\n'
                + '            ' + (('~' * 150) + '\n            ') + (('~' * 63) + 'Start Original Exception' + ('~' * 63) + '\n            ') + (('~' * 150) + '\n            \n')
                + f'{formatted_original_error}\n\n'
                + '            ' + (('~' * 150) + '\n            ') + (('~' * 65) + 'End Original Exception' + ('~' * 63) + '\n            ') + (('~' * 150) + '\n            \n')
                + 'Suggested Resolution:\n'
                f'{formatted_suggested_resolution}\n\n'
                f'Originating error on line {caller_line} in <{caller_module}>\n'
                + (('-' * 150) + '\n') * 2
            )
            raise error_type(error_message)
        elif (
            main_message
            and not expected_result
            and not returned_result
            and not suggested_resolution
            and original_error
        ):
            error_message = (
                f'{main_message}\n'
                + (('-' * 150) + '\n') + (('-' * 65) + 'Additional Information' + ('-' * 63) + '\n') + (('-' * 150) + '\n')
                + 'Original Exception:\n\n'
                + '            ' + (('~' * 150) + '\n            ') + (('~' * 63) + 'Start Original Exception' + ('~' * 63) + '\n            ') + (('~' * 150) + '\n            \n')
                + f'{formatted_original_error}\n\n'
                + '            ' + (('~' * 150) + '\n            ') + (('~' * 65) + 'End Original Exception' + ('~' * 63) + '\n            ') + (('~' * 150) + '\n            \n')
                + f'Originating error on line {caller_line} in <{caller_module}>\n'
                + (('-' * 150) + '\n') * 2
            )
            raise error_type(error_message)
        elif (
            main_message
            and not expected_result
            and not returned_result
            and suggested_resolution
            and not original_error
        ):
            error_message = (
                f'{main_message}\n'
                + (('-' * 150) + '\n') + (('-' * 65) + 'Additional Information' + ('-' * 63) + '\n') + (('-' * 150) + '\n')
                + 'Suggested Resolution:\n'
                f'{formatted_suggested_resolution}\n\n'
                f'Originating error on line {caller_line} in <{caller_module}>\n'
                + (('-' * 150) + '\n') * 2
            )
            raise error_type(error_message)
        else:
            # Sets custom output for values that are None.
            if not expected_result:
                expected_result = 'None provided'
            if not returned_result:
                returned_result = 'None provided'
            if not original_error:
                original_error = 'None provided'
            if not suggested_resolution:
                suggested_resolution = 'None provided'

            # Catch all other variations. Includes all possible formatted error options with values set to "None provided" if the value is None.
            # Most common variations are already setup. If another variation is required it can be added without causing any issues to calling modules.
            # Converts the error into a formatted string with tab spacing.
            original_error = str('\n            ' + '\n            '.join(map(str, str(original_error).splitlines())))
            error_message = (
                f'{main_message}\n'
                + (('-' * 150) + '\n') + (('-' * 65) + 'Additional Information' + ('-' * 63) + '\n') + (('-' * 150) + '\n')
                + 'Expected Result:\n'
                f'{formatted_expected_result}\n\n'
                'Returned Result:\n'
                f'{formatted_returned_result}\n\n'
                'Original Exception:\n\n'
                + '            ' + (('~' * 150) + '\n            ') + (('~' * 63) + 'Start Original Exception' + ('~' * 63) + '\n            ') + (('~' * 150) + '\n            \n')
                + f'{formatted_original_error}\n\n'
                + '            ' + (('~' * 150) + '\n            ') + (('~' * 65) + 'End Original Exception' + ('~' * 63) + '\n            ') + (('~' * 150) + '\n            \n')
                + 'Suggested Resolution:\n'
                f'{formatted_suggested_resolution}\n\n'
                f'Originating error on line {caller_line} in <{caller_module}>\n'
                + (('-' * 150) + '\n') * 2
            )
            raise error_type(error_message)
    except Exception as error:
        if 'Originating error on line' in str(error):
            raise error
        else:
            # Converts the error into a formatted string with tab spacing.
            original_error = str('\n            ' + '\n            '.join(map(str, str(error).splitlines())))
            error_message = (
                f'A general error has occurred while validating a value type.\n'
                + (('-' * 150) + '\n') + (('-' * 65) + 'Additional Information' + ('-' * 63) + '\n') + (('-' * 150) + '\n')
                + 'Returned Result:\n'
                '  - Original Exception listed below:\n\n'
                + '            ' + (('~' * 150) + '\n            ') + (('~' * 63) + 'Start Original Exception' + ('~' * 63) + '\n            ') + (('~' * 150) + '\n            \n')
                + f'{formatted_original_error}\n\n'
                + '            ' + (('~' * 150) + '\n            ') + (('~' * 65) + 'End Original Exception' + ('~' * 63) + '\n            ') + (('~' * 150) + '\n            \n\n')
                + f'Originating error on line {error.__traceback__.tb_lineno} in <{__name__}>\n'
                + (('-' * 150) + '\n') * 2
            )
            raise Exception(error_message)
