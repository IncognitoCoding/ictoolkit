#!interpreter

"""
This module is designed to assist with subprocess actions.
"""

# Built-in/Generic Imports
import io
import traceback
import subprocess
import logging

__author__ = 'IncognitoCoding'
__copyright__ = 'Copyright 2021, subprocess_director'
__credits__ = ['IncognitoCoding']
__license__ = 'GPL'
__version__ = '1.2'
__maintainer__ = 'IncognitoCoding'
__status__ = 'Development'


class AttributeDictionary(dict):
    """
    This class helps convert an object in a dictionary to dict.key opposed to using dict['key'].

    This class was created to return data for the function start_subprocess in a dot notation format. 
    
    Args:
        dict (dict): A dictionary key and value.
    """
    def __init__(self, adict):
        self.__dict__.update(adict)


def start_subprocess(program_arguments):
    """
    This function runs a subprocess when called and returns the output in an easy-to-reference attribute style dictionary similar to the original subprocess output return.
    This function is not designed for sub-processing continuous output. Calling this function will run the sub-process and will wait until the process ends before returning the output.
    
    Args:
        program_arguments (str or list): Processing arguments such as ifconfig, ipconfig, python, PowerShell.exe, or any other arguments may be passed.
        program_path (str): Program path to run based on the programs argument entry.

    Raises:
        ValueError: An error occurred while running the subprocess ({program_arguments}).

    Returns:
        AttributeDictionary(dict): Attribute dictionary containing args and stdout

        The return code can be called using dict.key notation. 
        
        Two options are avaliable:
            - <process return name>.args
            - <process return name>.stdout
    """
    logger = logging.getLogger(__name__)
    logger.debug(f'=' * 20 + traceback.extract_stack(None, 2)[1][2] + '=' * 20)
    # Custom flowchart tracking. This is ideal for large projects that move a lot. 
    # For any third-party modules, set the flow before making the function call.
    logger_flowchart = logging.getLogger('flowchart')
    logger_flowchart.debug(f'Flowchart --> Function: {traceback.extract_stack(None, 2)[1][2]}')

    try:
        # Runs the subprocess and returns output
        output = subprocess.Popen(program_arguments,stdout=subprocess.PIPE)
        
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
    except Exception as err:
        error_message = (
            f'An error occurred while running the subprocess ({program_arguments}).\n\n' +
            (('-' * 150) + '\n') + (('-' * 65) + 'Additional Information' + ('-' * 63) + '\n') + (('-' * 150) + '\n') +
            f'{err}\n\n'
            f'Originating error on line {traceback.extract_stack()[-1].lineno} in <{__name__}>\n' +
            (('-' * 150) + '\n') * 2 
        )   
        raise ValueError(error_message)
    else:
         return subprocess_output