#!interpreter

"""
This module is designed to assist with log-related actions.
"""

# Built-in/Generic Imports
import threading
import sys
import queue
import time
import traceback
import logging

# Own modules
from ictoolkit.directors.error_director import error_formatter
from ictoolkit.helpers.py_helper import get_function_name, get_line_number
from ictoolkit.directors.validation_director import value_type_validation
from ictoolkit.directors.error_director import error_formatter
from ictoolkit.helpers.py_helper import get_function_name, get_line_number

__author__ = 'IncognitoCoding'
__copyright__ = 'Copyright 2022, thread_director'
__credits__ = ['IncognitoCoding']
__license__ = 'GPL'
__version__ = '2.0'
__maintainer__ = 'IncognitoCoding'
__status__ = 'Production'


def start_function_thread(passing_program_function, program_function_name: str, infinite_loop_option: bool) -> None:
    """
    This function is used to start any other function inside it's own thread. This is ideal if you need to have part of the program sleep and another part of the program always
    active (ex: Web Interface = Always Active & Log Checking = 10 Minute Sleep)

    Thread exception capturing offers a challenge because the initialized child thread is in its dedicated context with its dedicated stack. When an exception is thrown in, the
    child thread can potentially never report to the parent function. The only time the messages can be present is during the initial call to the child thread. A message bucket
    is used to hold any potential exception messages, and a 2 minutes sleep is set to give time for the thread to either start or fail. If neither occurs after 1 minute, the thread
    will end and throw a value error.

    Requires calling program to use "from functools import partial" when calling.

    Calling Example: start_function_thread(partial(PassingFunction, Parameter1, Parameter2, Parameter3, etc), <function name), <bool>)

    Args:
        passing_program_function (function): The function without or with parameters using functools.
        program_function_name (str): The function name used to identify the thread.
        infinite_loop_option (bool): Enabled infinite loop.

    Raises:
        TypeError: The value '{program_function_name}' is not in str format.
        TypeError: The value '{infinite_loop_option}' is not in bool format.
        Exception: Forwarding caught {type(error).__name__} at line {error.__traceback__.tb_lineno} in <{__name__}>
        Exception: A general exception occurred during the value type validation.
        Exception: A failure occurred while staring the function thread.
        Exception: The thread ({program_function_name}) timeout has reached its threshold of 1 minute.
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
        value_type_validation(program_function_name, str, __name__, get_line_number())
        value_type_validation(infinite_loop_option, bool, __name__, get_line_number())

        logger.debug(
            'Passing parameters:\n'
            f'  - program_function_name (str):\n        - {program_function_name}'
            f'  - infinite_loop_option (bool):\n        - {infinite_loop_option}'
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

    # Creates a dedicated thread class to run the companion decryptor.
    # This is required because the main() function will sleep x minutes between checks.
    class start_function_thread(threading.Thread):

        # Automatically creates these items when called.
        def __init__(self, bucket):
            threading.Thread.__init__(self)

            # Sets name to track treads activity.
            self.name = program_function_name
            self.daemon = True
            self.bucket = bucket

        def run(self):
            """Runs the object as self and calls the function."""
            # Stores the exception, if raised by the calling function.
            self.exception = None

            try:
                # Checks if the thread needs to loop.
                if infinite_loop_option:
                    # Infinite Loop.
                    while True:
                        # Starts the function in a loop.
                        passing_program_function()
                        # Sleeps 1 seconds to keep system resources from spiking when called without a sleep inside the calling entry.
                        time.sleep(1)
                else:
                    # Starts the function once.
                    passing_program_function()
            # Returns the calling functions error message if an error occurs.
            except Exception as err:
                # Sets the exception error message
                # self.exception = err
                self.bucket.put(sys.exc_info())

    # Creates a message queue to hold potential exception messages.
    bucket = queue.Queue()
    # Calls class to start the thread.
    thread_obj = start_function_thread(bucket)
    thread_obj.start()

    # Timeout gives enough time for the thread to timeout.
    # This time delay can delay potential incoming streams from a subprocess.
    # If the initial startup is critical, it may be worth creating a small script to delay the start of the subprocess call.
    time.sleep(2)

    # Sets max timeout at 1 minute if the thread does not start or an exception is not thrown.
    timeout = time.time() + 60 * 1

    while True:

        try:
            # Gets the bucket values
            exc = bucket.get(block=False)
        except queue.Empty:
            pass
        else:
            # Sets the bucket values from the exceptions
            exc_type, exc_obj, exc_trace = exc

            # Passes the calling functions error output as the original error.
            error_args = {
                'main_message': 'A failure occurred while staring the function thread.',
                'error_type': Exception,
                'original_error': exc_obj,
            }
            error_formatter(error_args, __name__, get_line_number())

        # Loop breaks if the thread is alive or timeout reached.
        if thread_obj.is_alive() is True:
            break

        if time.time() > timeout:
            error_args = {
                'main_message': f'The thread ({program_function_name}) timeout has reached its threshold of 1 minute.',
                'error_type': Exception,
                'suggested_resolution': 'Manual intervention is required for this thread to start.',
            }
            error_formatter(error_args, __name__, get_line_number())
