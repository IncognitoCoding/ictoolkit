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
__version__ = '1.2'
__maintainer__ = 'IncognitoCoding'
__status__ = 'Development'


def read_yaml_config(yaml_file_path, loader):
    """
    Reads configuration yaml file data and returns the returns the read configuration.

    Args:
        yaml_file_path (str): YAML file path.
        loader (str): Loader for the YAML file.
            Options: 
                - FullLoader
                    - Used for more trusted YAML input. This option will avoid unpredictable code execution.
                - SafeLoader
                    - Used for untrusted YAML input. This will only load a subset of the YAML language.
                - BaseLoader
                    - Used for the most basic YAML input. All loading is strings.
                - UnsafeLoader
                    - Used for original Loader code but could be easily exploitable by untrusted YAML input.
        
    Raises:
        ValueError: A failure occurred while opening the YAML file.

    Returns:
        yaml: YAML read configuration.
    """

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
    except Exception as err:
        if 'Incorrect YAML loader parameter' in str(err):
            error_message = (
                'Incorrect YAML loader parameter.\n\n' +
                (('-' * 150) + '\n') + (('-' * 65) + 'Additional Information' + ('-' * 63) + '\n') + (('-' * 150) + '\n') +
                'Expected Result:\n'
                '  - loader = FullLoader or SafeLoader or BaseLoader or UnsafeLoader\n\n'
                'Returned Result:\n'
                f'  - loader = {loader}.\n\n'
                f'Originating error on line {traceback.extract_stack()[-1].lineno} in <{__name__}>\n' +
                (('-' * 150) + '\n') * 2 
            )
            raise ValueError(error_message)
        else:
            error_message = (
                'A failure occurred while opening the YAML file.\n\n' +
                (('-' * 150) + '\n') + (('-' * 65) + 'Additional Information' + ('-' * 63) + '\n') + (('-' * 150) + '\n') +
                f'{err}\n\n'
                f'Originating error on line {traceback.extract_stack()[-1].lineno} in <{__name__}>\n' +
                (('-' * 150) + '\n') * 2 
            )   
        raise ValueError(error_message)
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
        ValueError: Incorrect {key} YAML value.
        ValueError: No value has been entered for \'{key}\' in the YAML file.
    """

    # Verifies a YAML value is returned.
    if value or value == False:
        # Verifies the returning YAML value.
        if not isinstance(value, type):
            error_message = (
                f'Incorrect \'{key}\' YAML value.\n\n' +
                (('-' * 150) + '\n') + (('-' * 65) + 'Additional Information' + ('-' * 63) + '\n') + (('-' * 150) + '\n') +
                'Suggested Resolution:\n'
                f'  - {type} is required.\n\n'
                f'Originating error on line {traceback.extract_stack()[-1].lineno} in <{__name__}>\n' +
                (('-' * 150) + '\n') * 2 
            )   
            raise ValueError(error_message)
    else:
        error_message = (
            f'No value has been entered for \'{key}\' in the YAML file.\n\n' +
            (('-' * 150) + '\n') + (('-' * 65) + 'Additional Information' + ('-' * 63) + '\n') + (('-' * 150) + '\n') +
            'Suggested Resolution:\n'
            f'  - Please check the YAML configuration for correct formatting.\n\n'
            f'Originating error on line {traceback.extract_stack()[-1].lineno} in <{__name__}>\n' +
            (('-' * 150) + '\n') * 2 
        )   
        raise ValueError(error_message)