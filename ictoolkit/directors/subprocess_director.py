#!interpreter

"""
This module is designed to assist with subprocess actions.
"""

# Built-in/Generic Imports
import sys
import os
import io
import traceback
import subprocess

__author__ = 'IncognitoCoding'
__copyright__ = 'Copyright 2021, subprocess_director'
__credits__ = ['IncognitoCoding']
__license__ = 'GPL'
__version__ = '1.1'
__maintainer__ = 'IncognitoCoding'
__status__ = 'Development'


class AttributeDictionary(dict):
    """
    This class helps convert an object in a dictionary to dict.key opposed to using dict['key'].

    This class was created to return data for the function start_subprocess in a dot notation format. 
    
    Args:
        dict (adict): a dictionary key and value
    """

    def __init__(self, adict):
        self.__dict__.update(adict)


def start_subprocess(program_arguments):
    """
    This function runs a subprocess when called and returns the output in an easy-to-reference attribute style dictionary similar to the original subprocess output return.
    This function is not designed for sub-processing continuous output. Calling this function will run the sub-process and will wait until the process ends before returning the output.
    
    Args:
        program_arguments (str or list): processing arguments such as ifconfig, ipconfig, python, PowerShell.exe, or any other arguments may be passed
        program_path (str): program path to run based on the programs argument entry

    Raises:
        ValueError: An error occurred while starting the subprocess
    Returns:
        AttributeDictionary: attribute dictionary containing args and stdout

        The return code can be called using dict.key notation. 
        
        Two options are avaliable:
            - <process return name>.args
            - <process return name>.stdout
    """

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
        raise ValueError(f'An error occurred while running the subprocess ({program_arguments}), {err}, Originating error on line {traceback.extract_stack()[-1].lineno} in <{__name__}>')

    finally:

         return subprocess_output