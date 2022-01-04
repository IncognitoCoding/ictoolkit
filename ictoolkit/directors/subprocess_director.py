#!interpreter

"""
This module is designed to assist with subprocess actions.
"""

# Built-in/Generic Imports
import io
import traceback
import subprocess
import logging
from typing import Union

# Own modules
from ictoolkit.directors.validation_director import value_type_validation
from ictoolkit.directors.error_director import error_formatter
from ictoolkit.helpers.py_helper import get_function_name, get_line_number

__author__ = 'IncognitoCoding'
__copyright__ = 'Copyright 2022, subprocess_director'
__credits__ = ['IncognitoCoding']
__license__ = 'GPL'
__version__ = '2.0'
__maintainer__ = 'IncognitoCoding'
__status__ = 'Production'


class AttributeDictionary(dict):
    """
    This class helps convert an object in a dictionary to dict.key opposed to using dict['key'].

    This class was created to return data for the function start_subprocess in a dot notation format.

    Args:
        dict (dict): A dictionary key and value.
    """
    def __init__(self, adict):
        self.__dict__.update(adict)


def start_subprocess(program_arguments: Union[str, list]) -> dict:
    """
    This function runs a subprocess when called and returns the output in an easy-to-reference attribute style dictionary similar to the original subprocess output return.
    This function is not designed for sub-processing continuous output. Calling this function will run the sub-process and will wait until the process ends before returning the output.

    Args:
        program_arguments (str or list): Processing arguments such as ifconfig, ipconfig, python, PowerShell.exe, or any other arguments may be passed.

    Raises:
        TypeError: The value '{program_arguments}' is not in str or list format.
        Exception: Forwarding caught {type(error).__name__} at line {error.__traceback__.tb_lineno} in <{__name__}>
        Exception: A general exception occurred during the value type validation.
        Exception: Forwarding caught {type(error).__name__} at line {error.__traceback__.tb_lineno} in <{__name__}>
        Exception: An error occurred while running the subprocess ({program_arguments}).

    Returns:
        AttributeDictionary(dict): Attribute dictionary containing args and stdout

        The return code can be called using dict.key notation.

        Two options are avaliable:
        \t\- <process return name>.args\\
        \t\- <process return name>.stdout
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
        value_type_validation(program_arguments, [str, list], __name__, get_line_number())

        if isinstance(program_arguments, list):
            formatted_program_arguments = '  - program_arguments (list):' + str('\n        - ' + '\n        - '.join(map(str, program_arguments)))
        elif isinstance(program_arguments, str):
            formatted_program_arguments = f'  - program_arguments (str):\n        - {program_arguments}'

        logger.debug(
            'Passing parameters:\n'
            f'{formatted_program_arguments}\n'
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
        # Runs the subprocess and returns output
        output = subprocess.Popen(program_arguments, stdout=subprocess.PIPE)

        # Creates an empty list to store standard output.
        process_output = []
        # Creates an empty list to store error output.
        process_error = []

        # Reads through each standard output line.
        for line in io.TextIOWrapper(output.stdout, encoding="utf-8"):
            # Adds found line to the list and removes whitespace.
            process_output.append(line.rstrip())

        # Adds entries into the dictionary using the attribute notation. Attribute notation is used to give a similar return experience.
        subprocess_output = AttributeDictionary({'args': output.args, 'stdout': process_output})

        output.wait()
    except Exception as error:
        if 'Originating error on line' in str(error):
            logger.debug(f'Forwarding caught {type(error).__name__} at line {error.__traceback__.tb_lineno} in <{__name__}>')
            raise error
        else:
            error_args = {
                'main_message': f'An error occurred while running the subprocess ({program_arguments}).',
                'error_type': Exception,
                'original_error': error,
            }
            error_formatter(error_args, __name__, error.__traceback__.tb_lineno)
    else:
        return subprocess_output
