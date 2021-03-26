#!interpreter

"""
This module is designed to assist with log-related actions.

This module does not have a test file to run with pytest. The YAML function will be tested at the start of any program utilizing this method, so additional testing is not provided.
"""

# Built-in/Generic Imports
import traceback

# Libraries
import yaml

__author__ = 'IncognitoCoding'
__copyright__ = 'Copyright 2021, yaml_director'
__credits__ = ['IncognitoCoding']
__license__ = 'GPL'
__version__ = '1.0'
__maintainer__ = 'IncognitoCoding'
__status__ = 'Development'


def read_yaml_config(yaml_file_path):
    """
    Reads configuration yaml file data and returns the returns the read configuration.

    Args:
        yaml_file_path (str): YAML file path

    Raises:
        ValueError: General errors when opening YAML file
    Returns:
        yaml: YAML read configuration
    """

    # Checks for issues while reading the yaml file.
    try:
        # Calls function to pull in yaml configuration.
        with open(yaml_file_path) as file:

            # Using the fullLoader parameter to handle the conversion from yaml.
            config = yaml.load(file, Loader=yaml.FullLoader)

    except Exception as err:
        raise ValueError(f'{err}, Originating error on line {traceback.extract_stack()[-1].lineno} in <{__name__}>')
    else:
        return config


def yaml_value_validation(key, value, type):
    """
    YAML value validations are performed within this function. Any validation that does not pass will throw a message statement, and the program will exit.

    The pre-configured output message uses the key and type entries to notify the user of what value is missing.

    Args:
        key (str): key used inside the YAML configuration file. This entry is only used for the message output and can contain additional information.
        value (YAML value): value used inside the YAML configuration file
        type (type): type of value used inside the YAML configuration file
    Raises:
        ValueError: Incorrect {key} YAML value. {type} is required
        ValueError: No value has been entered for {key} in the YAML file
    """

    # Verifies a YAML value is returned.
    if value or value == False:
        # Verifies the returning YAML value.
        if not isinstance(value, type):
            raise ValueError(f'Incorrect \'{key}\' YAML value. {type} is required, Originating error on line {traceback.extract_stack()[-1].lineno} in <{__name__}>')
    else:
        raise ValueError(f'No value has been entered for \'{key}\' in the YAML file, Originating error on line {traceback.extract_stack()[-1].lineno} in <{__name__}>')