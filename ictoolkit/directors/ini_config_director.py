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

__author__ = 'IncognitoCoding'
__copyright__ = 'Copyright 2021, ini_config_director'
__credits__ = ['IncognitoCoding']
__license__ = 'GPL'
__version__ = '1.1'
__maintainer__ = 'IncognitoCoding'
__status__ = 'Development'


def read_ini_config(ini_file_path):
    """
    Reads configuration ini file data and returns the returns the read configuration.

    Args:
        ini_file_path (str): The file path to the ini file.

    Raises:
        ValueError: A failure occurred while reading the ini configuration file.

    Returns:
        ini: INI read configuration.
    """
    logger = logging.getLogger(__name__)
    logger.debug(f'=' * 20 + traceback.extract_stack(None, 2)[1][2] + '=' * 20)
    # Custom flowchart tracking. This is ideal for large projects that move a lot. 
    # For any third-party modules, set the flow before making the function call.
    logger_flowchart = logging.getLogger('flowchart')
    logger_flowchart.info(f'Flowchart --> Function: {traceback.extract_stack(None, 2)[1][2]}')

    # Checks for issues while reading the ini file.
    try:
        # Calls function to pull in ini configuration.
        # Uses RawConfigParser for special characters.
        config = configparser.RawConfigParser()
        config.read(ini_file_path)
    except Exception as err:
        error_message = (
            'A failure occurred while reading the ini configuration file.\n\n' +
            (('-' * 150) + '\n') + (('-' * 65) + 'Additional Information' + ('-' * 63) + '\n') + (('-' * 150) + '\n') +
            f'{err}\n\n'
            f'Originating error on line {traceback.extract_stack()[-1].lineno} in <{__name__}>\n' +
            (('-' * 150) + '\n') * 2 
        )   
        raise ValueError(error_message)
    else:
        return config


def get_ini_config(ini_config, section, key):
    """
    Gets the ini configuration section key based on the read configuration and the section.

    Args:
        ini_config (ini): INI read configuration.
        section (str): Section value.
        key (str): Key value.

    Raises:
        ValueError: A failure occurred while getting INI configuration information.

    Returns:
        str: Section key.
    """

    # Checks for configuratin errors while getting output.
    try:
        # Gets value from config.
        # ini_config must contain .get, .getboolean, etc.
        result = ini_config(section, key)
    except Exception as err:
        error_message = (
            'A failure occurred while getting INI configuration information.\n\n' +
            (('-' * 150) + '\n') + (('-' * 65) + 'Additional Information' + ('-' * 63) + '\n') + (('-' * 150) + '\n') +
            f'{err}\n\n'
            f'Originating error on line {traceback.extract_stack()[-1].lineno} in <{__name__}>\n' +
            (('-' * 150) + '\n') * 2 
        )   
        raise ValueError(error_message)
    else:
        return result
  