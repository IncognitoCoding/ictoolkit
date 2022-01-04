#!interpreter

"""
This module is designed to assist with INI-related actions.

This module does not have a test file to run with pytest. The INI function will be tested at the start of any program utilizing this method, so additional testing is not provided.
"""

# Built-in/Generic Imports
import traceback
import logging

# Libraries
import configparser

# Own modules
from ictoolkit.directors.validation_director import value_type_validation
from ictoolkit.directors.error_director import error_formatter
from ictoolkit.helpers.py_helper import get_function_name, get_line_number

__author__ = 'IncognitoCoding'
__copyright__ = 'Copyright 2022, ini_config_director'
__credits__ = ['IncognitoCoding']
__license__ = 'GPL'
__version__ = '2.0'
__maintainer__ = 'IncognitoCoding'
__status__ = 'Production'


def read_ini_config(ini_file_path: str) -> configparser:
    """
    Reads configuration ini file data and returns the returns the read configuration.

    Args:
        ini_file_path (str): The file path to the ini file.

    Raises:
        TypeError: The value '{ini_file_path}' is not in str or list format.
        Exception: Forwarding caught {type(error).__name__} at line {error.__traceback__.tb_lineno} in <{__name__}>
        Exception: A general exception occurred during the value type validation.
        Exception: Forwarding caught {type(error).__name__} at line {error.__traceback__.tb_lineno} in <{__name__}>
        Exception: A general exception occurred while reading the ini configuration file.

    Returns:
        [ini]: INI read configuration.
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
        value_type_validation(ini_file_path, str, __name__, get_line_number())

        logger.debug(
            'Passing parameters:\n'
            f'  - ini_file_path (str):\n        - {ini_file_path}\n'
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

    # Checks for issues while reading the ini file.
    try:
        # Calls function to pull in ini configuration.
        # Uses RawConfigParser for special characters.
        config = configparser.RawConfigParser()
        config.read(ini_file_path)
    except Exception as err:
        error_args = {
            'main_message': 'A general exception occurred while reading the ini configuration file.',
            'error_type': Exception,
            'original_error': error,
        }
        error_formatter(error_args, __name__, error.__traceback__.tb_lineno)
    else:
        return config


def get_ini_config(ini_config: configparser, section: str, key: str) -> str:
    """
    Gets the ini configuration section key based on the read configuration and the section.

    Args:
        ini_config (configparser): INI read configuration.
        section (str): Section value.
        key (str): Key value.

    Raises:
        TypeError: The value '{section}' is not in str or list format.
        TypeError: The value '{key}' is not in str or list format.
        Exception: Forwarding caught {type(error).__name__} at line {error.__traceback__.tb_lineno} in <{__name__}>
        Exception: A general exception occurred during the value type validation.
        Exception: Forwarding caught {type(error).__name__} at line {error.__traceback__.tb_lineno} in <{__name__}>
        Exception: A general exception occurred while getting INI configuration information.

    Returns:
        [str]: Section key.
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
        value_type_validation(section, str, __name__, get_line_number())
        value_type_validation(key, str, __name__, get_line_number())

        logger.debug(
            'Passing parameters:\n'
            f'  - ini_config (configparser):\n        - {ini_config}\n'
            f'  - section (str):\n        - {section}\n'
            f'  - key (str):\n        - {key}\n'
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

    # Checks for configuration errors while getting output.
    try:
        # Gets value from config.
        # ini_config must contain .get, .getboolean, etc.
        result = ini_config(section, key)
    except Exception as err:
        error_args = {
            'main_message': 'A general exception occurred while getting INI configuration information.',
            'error_type': Exception,
            'original_error': error,
        }
        error_formatter(error_args, __name__, error.__traceback__.tb_lineno)
    else:
        return result
