"""
This module is designed to assist with log-related actions.

This module does not have a test file to run with pytest. The YAML function will be tested at the start of any program utilizing this method, so additional testing is not provided.
"""

# Built-in/Generic Imports
import traceback
import logging
from typing import Union

# Libraries
import yaml

# Own modules
from ictoolkit.directors.validation_director import value_type_validation
from ictoolkit.directors.error_director import error_formatter
from ictoolkit.helpers.py_helper import get_function_name, get_line_number

__author__ = 'IncognitoCoding'
__copyright__ = 'Copyright 2022, yaml_director'
__credits__ = ['IncognitoCoding']
__license__ = 'GPL'
__version__ = '2.1'
__maintainer__ = 'IncognitoCoding'
__status__ = 'Production'


def read_yaml_config(yaml_file_path: str, loader: str) -> yaml:
    """
    Reads configuration yaml file data and returns the returns the read configuration.

    Args:
        yaml_file_path (str): YAML file path.
        loader (str): Loader for the YAML file.
        - loader Options:
            - FullLoader
                - Used for more trusted YAML input. This option will avoid unpredictable code execution.
            - SafeLoader
                - Used for untrusted YAML input. This will only load a subset of the YAML language.
            - BaseLoader
                - Used for the most basic YAML input. All loading is strings.
            - UnsafeLoader
                - Used for original Loader code but could be easily exploitable by untrusted YAML input.

    Raises:
        TypeError: The value '{yaml_file_path}' is not in str format.
        TypeError: The value '{loader}' is not in str format.
        Exception: Forwarding caught {type(error).__name__} at line {error.__traceback__.tb_lineno} in <{__name__}>
        Exception: A general exception occurred during the value type validation.
        ValueError: Incorrect YAML loader parameter.
        ValueError: A failure occurred while reading the YAML file.
        Exception: Forwarding caught {type(error).__name__} at line {error.__traceback__.tb_lineno} in <{__name__}>
        Exception: A general failure occurred while opening the YAML file.

    Returns:
        yaml: YAML read configuration.
    """
    logger = logging.getLogger(__name__)
    logger.debug(f'=' * 20 + get_function_name() + '=' * 20)
    # Custom flowchart tracking. This is ideal for large projects that move a lot.
    # For any third-party modules, set the flow before making the function call.
    logger_flowchart = logging.getLogger('flowchart')
    logger_flowchart.debug(f'Flowchart --> Function: {get_function_name()}')

    # Checks function launch variables and logs passing parameters.
    try:
        # Validates required types.
        value_type_validation(yaml_file_path, str, __name__, get_line_number())
        value_type_validation(loader, str, __name__, get_line_number())

        logger.debug(
            'Passing parameters:\n'
            f'  - yaml_file_path (str):\n        - {yaml_file_path}\n'
            f'  - loader (str):\n        - {loader}\n'
        )
    except Exception as error:
        if 'Originating error on line' in str(error):
            logger.debug(f'Forwarding caught {type(error).__name__} at line {error.__traceback__.tb_lineno} in <{__name__}>')
            raise error
        else:
            error_args = {
                'main_message': 'A general exception occurred during the value type validation.',
                'error_type': Exception,
                'original_error': error,
            }
            error_formatter(error_args, __name__, error.__traceback__.tb_lineno)

    # Checks for issues while reading the yaml file.
    try:
        # Calls function to pull in yaml configuration.
        with open(yaml_file_path) as file:
            if 'FullLoader' == loader:
                config = yaml.load(file, Loader=yaml.FullLoader)
            elif 'SafeLoader' == loader:
                config = yaml.load(file, Loader=yaml.SafeLoader)
            elif 'BaseLoader' == loader:
                config = yaml.load(file, Loader=yaml.BaseLoader)
            elif 'UnsafeLoader' == loader:
                config = yaml.load(file, Loader=yaml.UnsafeLoader)
            else:
                raise ValueError('Incorrect YAML loader parameter.')
    except Exception as error:
        if 'Incorrect YAML loader parameter' in str(error):
            error_args = {
                'main_message': 'Incorrect YAML loader parameter.',
                'error_type': ValueError,
                'expected_result': 'FullLoader or SafeLoader or BaseLoader or UnsafeLoader',
                'returned_result': loader,
                'suggested_resolution': 'Please verify you have set all required keys and try again.',
            }
            error_formatter(error_args, __name__, error.__traceback__.tb_lineno)
        elif 'expected <block end>, but found \'<scalar>\'' in str(error):
            error_args = {
                'main_message': 'A failure occurred while reading the YAML file.',
                'error_type': ValueError,
                'expected_result': 'FullLoader or SafeLoader or BaseLoader or UnsafeLoader',
                'returned_result': loader,
                'suggested_resolution': '- Please verify you have the correct punctuation on your entries. For example, having three single quotes will cause this error to occur.\n- If '
                'you are using three single quotes, it will help if you use double quotes to begin and end with a single quote in the middle.',
            }
            error_formatter(error_args, __name__, error.__traceback__.tb_lineno)
        elif 'Originating error on line' in str(error):
            logger.debug(f'Forwarding caught {type(error).__name__} at line {error.__traceback__.tb_lineno} in <{__name__}>')
            raise error
        else:
            error_args = {
                'main_message': 'A general failure occurred while opening the YAML file.',
                'error_type': Exception,
                'original_error': error,
            }
            error_formatter(error_args, __name__, error.__traceback__.tb_lineno)
    else:
        logger.debug(f'Returning value(s):\n  - Return = {config}')
        return config


def yaml_value_validation(key: str, input_value: any, required_value_type: Union[type, list]) -> None:
    """
    YAML value validations are performed within this function. Any validation that does not pass will throw a ValueError message statement that a try exception statement can handle.

    The pre-configured output message uses the key and type entries to notify the user of what value is missing.

    Args:
        key (str): key used inside the YAML configuration file. This entry is only used for the message output and can contain additional information.
        input_value_type (any): value used inside the YAML configuration file
        required_value_type (type or list): The type of value used inside the YAML configuration file or a list of types.

    Raises:
        TypeError: The value '{key}' is not in str format.
        TypeError: The value '{required_value_type}' is not in str or list format.
        Exception: Forwarding caught {type(error).__name__} at line {error.__traceback__.tb_lineno} in <{__name__}>
        Exception: A general exception occurred during the value type validation.
        ValueError: Incorrect \'{key}\' YAML value.
        ValueError: No value has been entered for \'{key}\' in the YAML file.
        Exception: Forwarding caught {type(error).__name__} at line {error.__traceback__.tb_lineno} in <{__name__}>
        Exception: A general failure occurred while while validating the YAML value.
    """
    logger = logging.getLogger(__name__)
    logger.debug(f'=' * 20 + get_function_name() + '=' * 20)
    # Custom flowchart tracking. This is ideal for large projects that move a lot.
    # For any third-party modules, set the flow before making the function call.
    logger_flowchart = logging.getLogger('flowchart')
    logger_flowchart.debug(f'Flowchart --> Function: {get_function_name()}')

    # Checks function launch variables and logs passing parameters.
    try:
        # Validates required types.
        value_type_validation(key, str, __name__, get_line_number())
        value_type_validation(required_value_type, [type, list], __name__, get_line_number())

        if isinstance(required_value_type, list):
            formatted_required_value_type = '  - required_value_type (list):' + str('\n        - ' + '\n        - '.join(map(str, required_value_type)))
        elif isinstance(required_value_type, type):
            formatted_required_value_type = f'  - required_value_type (str):\n        - {required_value_type}'

        logger.debug(
            'Passing parameters:\n'
            f'  - key (str):\n        - {key}\n'
            f'  - input_value (any):\n        - {input_value}\n'
            f'{formatted_required_value_type}\n'
        )
    except Exception as error:
        if 'Originating error on line' in str(error):
            logger.debug(f'Forwarding caught {type(error).__name__} at line {error.__traceback__.tb_lineno} in <{__name__}>')
            raise error
        else:
            error_args = {
                'main_message': 'A general exception occurred during the value type validation.',
                'error_type': Exception,
                'original_error': error,
            }
            error_formatter(error_args, __name__, error.__traceback__.tb_lineno)

    try:
        # Verifies a YAML value is returned.
        if input_value is not None:
            if isinstance(required_value_type, list):
                for value_type in required_value_type:
                    if isinstance(input_value, value_type):
                        matching_type_flag = True
                        break
                    else:
                        matching_type_flag = False
            else:
                # Verifies the returning YAML value.
                if not isinstance(input_value, required_value_type):
                    matching_type_flag = False
                else:
                    matching_type_flag = True
            # Throws the ValueError
            if matching_type_flag is False:
                input_value_type = type(input_value)
                error_args = {
                    'main_message': f'Incorrect \'{key}\' YAML value.',
                    'error_type': ValueError,
                    'expected_result': f'The value ({input_value}) in for key ({key}) should have matched the required value type(s) ({required_value_type})',
                    'returned_result': f'  - input_value_type = {input_value_type}\n- required_value_type = {required_value_type}',
                    'suggested_resolution': 'Review your YAML configuration to see if it contains the required values.',
                }
                error_formatter(error_args, __name__, get_line_number())
            else:
                logger.debug(f'The value ({input_value}) in for key ({key}) matched the required value type(s) ({required_value_type})')
        else:
            error_args = {
                'main_message': f'No value has been entered for \'{key}\' in the YAML file.\n',
                'error_type': ValueError,
                'suggested_resolution': 'Please check the YAML configuration for correct formatting.',
            }
            error_formatter(error_args, __name__, get_line_number())
    except Exception as error:
        if 'Originating error on line' in str(error):
            logger.debug(f'Forwarding caught {type(error).__name__} at line {error.__traceback__.tb_lineno} in <{__name__}>')
            raise error
        else:
            error_args = {
                'main_message': 'A general failure occurred while while validating the YAML value.',
                'error_type': Exception,
                'original_error': error,
            }
            error_formatter(error_args, __name__, error.__traceback__.tb_lineno)
