#!interpreter

"""
This module is designed to assist with INI-related actions.

This module does not have a test file to run with pytest. The INI function will be tested at the start of any program utilizing this method, so additional testing is not provided.
"""

# Built-in/Generic Imports
import traceback

# Libraries
import configparser

__author__ = 'IncognitoCoding'
__copyright__ = 'Copyright 2021, ini_config_director'
__credits__ = ['IncognitoCoding']
__license__ = 'GPL'
__version__ = '1.0'
__maintainer__ = 'IncognitoCoding'
__status__ = 'Development'


def read_ini_config(ini_file_path):
    """
    Reads configuration ini file data and returns the returns the read configuration.

    Args:
        ini_file_path (str): the file path to the ini file

    Raises:
        ValueError: General error when reading the ini configuration file

    Returns:
        ini: INI read configuration
    """

    # Checks for issues while reading the ini file.
    try:

        # Calls function to pull in ini configuration.
        # Uses RawConfigParser for special characters.
        config = configparser.RawConfigParser()
        config.read(ini_file_path)

    except Exception as err:
        raise ValueError(f'{err}, Originating error on line {traceback.extract_stack()[-1].lineno} in <{__name__}>')
    else:
        return config


def get_ini_config(ini_config, section, key):
    """
    Gets the ini configuration section key based on the read configuration and the section.

    Args:
        ini_config (ini): INI read configuration
        section (str): section value
        key (str): key value

    Raises:
        ValueError: General error getting INI configuration information

    Returns:
        str: section key
    """

    # Checks for configuratin errors while getting output.
    try:

        # Gets value from config.
        # ini_config must contain .get, .getboolean, etc.
        result = ini_config(section, key)

    except Exception as err:
        raise ValueError(f'{err}, Originating error on line {traceback.extract_stack()[-1].lineno} in <{__name__}>')
    else:
        return result
  