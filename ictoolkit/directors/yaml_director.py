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

__author__ = 'IncognitoCoding'
__copyright__ = 'Copyright 2021, yaml_director'
__credits__ = ['IncognitoCoding']
__license__ = 'GPL'
__version__ = '1.7'
__maintainer__ = 'IncognitoCoding'
__status__ = 'Development'


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
        ValueError: A failure occurred while opening the YAML file.

    Returns:
        yaml: YAML read configuration.
    """
    logger = logging.getLogger(__name__)
    logger.debug(f'=' * 20 + traceback.extract_stack(None, 2)[1][2] + '=' * 20)
    # Custom flowchart tracking. This is ideal for large projects that move a lot.
    # For any third-party modules, set the flow before making the function call.
    logger_flowchart = logging.getLogger('flowchart')
    logger_flowchart.debug(f'Flowchart --> Function: {traceback.extract_stack(None, 2)[1][2]}')
    logger.debug(
        'Passing parameters:\n'
        f'  - yaml_file_path (str):\n        - {yaml_file_path}\n'
        f'  - loader (str):\n        - {loader}\n'
    )

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
            error_message = (
                'Incorrect YAML loader parameter.\n\n'
                + (('-' * 150) + '\n') + (('-' * 65) + 'Additional Information' + ('-' * 63) + '\n') + (('-' * 150) + '\n')
                + 'Expected Result:\n'
                '  - loader = FullLoader or SafeLoader or BaseLoader or UnsafeLoader\n\n'
                'Returned Result:\n'
                f'  - loader = {loader}.\n\n'
                f'Originating error on line {error.__traceback__.tb_lineno} in <{__name__}>\n'
                + (('-' * 150) + '\n') * 2
            )
            raise ValueError(error_message)
        elif 'expected <block end>, but found \'<scalar>\'' in str(error):
            error_message = (
                'A failure occurred while reading the YAML file.\n'
                + (('-' * 150) + '\n') + (('-' * 65) + 'Additional Information' + ('-' * 63) + '\n') + (('-' * 150) + '\n')
                + 'Returned Error:\n'
                f'{error}\n\n'
                'Suggested Resolution:\n'
                '   - Please verify you have the correct punctuation on your entries. For example, having three single quotes will cause this error to occur.\n'
                '     If you are using three single quotes, it will help if you use double quotes to begin and end with a single quote in the middle.\n\n'
                f'Originating error on line {error.__traceback__.tb_lineno} in <{__name__}>\n'
                + (('-' * 150) + '\n') * 2
            )
            raise ValueError(error_message)
        else:
            error_message = (
                'A failure occurred while opening the YAML file.\n\n'
                + (('-' * 150) + '\n') + (('-' * 65) + 'Additional Information' + ('-' * 63) + '\n') + (('-' * 150) + '\n')
                + f'{error}\n\n'
                f'Originating error on line {error.__traceback__.tb_lineno} in <{__name__}>\n'
                + (('-' * 150) + '\n') * 2
            )
        raise ValueError(error_message)
    else:
        logger.debug(f'Returning value(s):\n  - Return = {config}')
        return config


def yaml_value_validation(key: str, input_value: str, required_value_type: Union[type, list]) -> None:
    """
    YAML value validations are performed within this function. Any validation that does not pass will throw a ValueError message statement that a try exception statement can handle.

    The pre-configured output message uses the key and type entries to notify the user of what value is missing.

    Args:
        key (str): key used inside the YAML configuration file. This entry is only used for the message output and can contain additional information.
        input_value_type (YAML value): value used inside the YAML configuration file
        required_value_type (type or list): The type of value used inside the YAML configuration file or a list of types.

    Raises:
        ValueError: Incorrect {key} YAML value.
        ValueError: No value has been entered for \'{key}\' in the YAML file.
    """
    logger = logging.getLogger(__name__)
    logger.debug(f'=' * 20 + traceback.extract_stack(None, 2)[1][2] + '=' * 20)
    # Custom flowchart tracking. This is ideal for large projects that move a lot.
    # For any third-party modules, set the flow before making the function call.
    logger_flowchart = logging.getLogger('flowchart')
    logger_flowchart.debug(f'Flowchart --> Function: {traceback.extract_stack(None, 2)[1][2]}')
    # Requires pre-logger formatting because the logger can not use one line if/else or join without excluding sections of the the output.
    if isinstance(required_value_type, list):
        formatted_required_value_type = '  - required_value_type (list):' + str('\n        - ' + '\n        - '.join(map(str, required_value_type)))
    else:
        formatted_required_value_type = f'  - required_value_type (type):\n        - {required_value_type}'
    logger.debug(
        'Passing parameters:\n'
        f'  - key (str):\n        - {key}\n'
        f'  - input_value (str):\n        - {input_value}\n'
        f'{formatted_required_value_type}\n'
    )

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
            error_message = (
                f'Incorrect \'{key}\' YAML value.\n\n'
                + (('-' * 150) + '\n') + (('-' * 65) + 'Additional Information' + ('-' * 63) + '\n') + (('-' * 150) + '\n')
                + 'Expected Result:\n'
                f'  - The value ({input_value}) in for key ({key}) should have matched the required value type(s) ({required_value_type})\n\n'
                'Returned Result:\n'
                f'  - input_value_type = {input_value_type}\n'
                f'  - required_value_type = {required_value_type}\n\n'
                'Suggested Resolution:\n'
                f'  - Review your YAML configuration to see if it contains the required values.\n\n'
                f'Originating error on line {traceback.extract_stack()[-1].lineno} in <{__name__}>\n'
                + (('-' * 150) + '\n') * 2
            )
            raise ValueError(error_message)
        else:
            logger.debug(f'The value ({input_value}) in for key ({key}) matched the required value type(s) ({required_value_type})')
    else:
        error_message = (
            f'No value has been entered for \'{key}\' in the YAML file.\n\n'
            + (('-' * 150) + '\n') + (('-' * 65) + 'Additional Information' + ('-' * 63) + '\n') + (('-' * 150) + '\n')
            + 'Suggested Resolution:\n'
            f'  - Please check the YAML configuration for correct formatting.\n\n'
            f'Originating error on line {traceback.extract_stack()[-1].lineno} in <{__name__}>\n'
            + (('-' * 150) + '\n') * 2
        )
        raise ValueError(error_message)
