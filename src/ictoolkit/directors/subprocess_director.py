"""
This module is designed to assist with subprocess actions.
"""
# Built-in/Generic Imports
import io
import subprocess
import logging
from typing import Union

# Libraries
from fchecker import type_check

# Local Functions
from ..helpers.py_helper import get_function_name

# Exceptions
from fexception import FTypeError, FCustomException

__author__ = 'IncognitoCoding'
__copyright__ = 'Copyright 2022, subprocess_director'
__credits__ = ['IncognitoCoding']
__license__ = 'MIT'
__version__ = '3.2'
__maintainer__ = 'IncognitoCoding'
__status__ = 'Production'


class SubprocessStartFailure(Exception):
    """Exception raised for the subprocess start failure."""
    __module__ = 'builtins'
    pass


class AttributeDictionary(dict):
    """
    This class helps convert an object in a dictionary to dict.key opposed to using dict['key'].

    This class was created to return data for the function start_subprocess in a dot notation format.

    Args:
        adict (dict): A dictionary key and value.
    """
    def __init__(self, adict):
        self.__dict__.update(adict)


def start_subprocess(program_arguments: Union[str, list]) -> AttributeDictionary:
    """
    This function runs a subprocess when called and returns the output in an easy-to-reference\\
    attribute style dictionary similar to the original subprocess output return.

    This function is not designed for sub-processing continuous output.

    Calling this function will run the sub-process and will wait until the process ends before\\
    returning the output.

    Args:
        program_arguments (Union[str, list]):
        \t\\- Processing arguments such as ifconfig, ipconfig, python, PowerShell.exe,
        \t   or any other arguments may be passed.

    Raises:
        FTypeError (fexception):
        \t\\- The value '{program_arguments}' is not in [<class 'str'>, <class 'list'>] format.
        SubprocessStartFailure:
        \t\\- An error occurred while running the subprocess ({program_arguments}).

    Returns:
        AttributeDictionary(dict):
        \t\\- Attribute dictionary containing args and stdout

    Return Options:
    \t Two options are avaliable:
    \t\t\\- <process return name>.args\\
    \t\t\\- <process return name>.stdout
    """
    logger = logging.getLogger(__name__)
    logger.debug(f'=' * 20 + get_function_name() + '=' * 20)
    # Custom flowchart tracking. This is ideal for large projects that move a lot.
    # For any third-party modules, set the flow before making the function call.
    logger_flowchart = logging.getLogger('flowchart')
    logger_flowchart.debug(f'Flowchart --> Function: {get_function_name()}')

    try:
        type_check(program_arguments, [str, list])
    except FTypeError:
        raise

    if isinstance(program_arguments, list):
        formatted_program_arguments = '  - program_arguments (list):' + str('\n        - ' + '\n        - '.join(map(str, program_arguments)))
    elif isinstance(program_arguments, str):
        formatted_program_arguments = f'  - program_arguments (str):\n        - {program_arguments}'

    logger.debug(
        'Passing parameters:\n'
        f'{formatted_program_arguments}\n'
    )

    try:
        # Runs the subprocess and returns output
        output = subprocess.Popen(program_arguments, stdout=subprocess.PIPE)

        # Creates an empty list to store standard output.
        process_output = []

        # Reads through each standard output line.
        for line in io.TextIOWrapper(output.stdout, encoding="utf-8"):
            # Adds found line to the list and removes whitespace.
            process_output.append(line.rstrip())

        # Adds entries into the dictionary using the attribute notation. Attribute notation is used to give a similar return experience.
        subprocess_output = AttributeDictionary({'args': output.args, 'stdout': process_output})

        output.wait()
        output.kill()
    except Exception as exc:
        exc_args = {
            'main_message': f'An error occurred while running the subprocess ({program_arguments}).',
            'custom_type': SubprocessStartFailure,
            'original_exception': exc,
        }
        raise SubprocessStartFailure(FCustomException(exc_args))
    else:
        return subprocess_output
