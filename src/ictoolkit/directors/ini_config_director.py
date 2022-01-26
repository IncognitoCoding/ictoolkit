"""
This module is designed to assist with INI-related actions.

This module does not have a test file to run with pytest. The INI function will be tested at the start of any program utilizing this method, so additional testing is not provided.
"""
# Built-in/Generic Imports
import logging

# Libraries
import configparser
from fchecker import type_check

# Local Functions
from ..helpers.py_helper import get_function_name

# Exceptions
from fexception import FGeneralError, FTypeError

__author__ = 'IncognitoCoding'
__copyright__ = 'Copyright 2022, ini_config_director'
__credits__ = ['IncognitoCoding']
__license__ = 'MIT'
__version__ = '3.1'
__maintainer__ = 'IncognitoCoding'
__status__ = 'Production'


def read_ini_config(ini_file_path: str) -> configparser:
    """
    Reads configuration ini file data and returns the returns the read configuration.

    Args:
        ini_file_path (str):
        \t\\- The file path to the ini file.

    Raises:
        FTypeError (fexception):
        \t\\- The value '{ini_file_path}' is not in <class 'str'> format.
        FGeneralError (fexception):
        \t\\- A general exception occurred while reading the ini configuration file.

    Returns:
        ini:
        \t\\- INI read configuration.
    """
    logger = logging.getLogger(__name__)
    logger.debug(f'=' * 20 + get_function_name() + '=' * 20)
    # Custom flowchart tracking. This is ideal for large projects that move a lot.
    # For any third-party modules, set the flow before making the function call.
    logger_flowchart = logging.getLogger('flowchart')
    logger_flowchart.debug(f'Flowchart --> Function: {get_function_name()}')

    try:
        type_check(ini_file_path, str)
    except FTypeError:
        raise

    logger.debug(
        'Passing parameters:\n'
        f'  - ini_file_path (str):\n        - {ini_file_path}\n'
    )

    # Checks for issues while reading the ini file.
    try:
        # Calls function to pull in ini configuration.
        # Uses RawConfigParser for special characters.
        config = configparser.RawConfigParser()
        config.read(ini_file_path)
    except Exception as exc:
        exc_args = {
            'main_message': 'A general exception occurred while reading the ini configuration file.',
            'original_exception': exc,
        }
        raise FGeneralError(exc_args)
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
        FTypeError (fexception):
        \t\\- The value '{section}' is not in <class 'str'> format.
        FTypeError (fexception):
        \t\\- The value '{key}' is not in <class 'str'> format.
        FGeneralError (fexception):
        \t\\- A general exception occurred while getting INI configuration information.

    Returns:
        str:
        \t\\- Section key.
    """
    logger = logging.getLogger(__name__)
    logger.debug(f'=' * 20 + get_function_name() + '=' * 20)
    # Custom flowchart tracking. This is ideal for large projects that move a lot.
    # For any third-party modules, set the flow before making the function call.
    logger_flowchart = logging.getLogger('flowchart')
    logger_flowchart.debug(f'Flowchart --> Function: {get_function_name()}')

    try:
        type_check(section, str)
        type_check(key, str)
    except FTypeError:
        raise

    logger.debug(
        'Passing parameters:\n'
        f'  - ini_config (configparser):\n        - {ini_config}\n'
        f'  - section (str):\n        - {section}\n'
        f'  - key (str):\n        - {key}\n'
    )

    # Checks for configuration errors while getting output.
    try:
        # Gets value from config.
        # ini_config must contain .get, .getboolean, etc.
        result = ini_config(section, key)
    except Exception as exc:
        exc_args = {
            'main_message': 'A general exception occurred while getting INI configuration information.',
            'original_exception': exc,
        }
        raise FGeneralError(exc_args)
    else:
        return result
