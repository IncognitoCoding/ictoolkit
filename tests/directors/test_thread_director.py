"""
This script is used to test the thread_director module using pytest.
"""
# Built-in/Generic Imports
import os
import time
import threading

# Libraries
from functools import partial

# Local Functions
from ictoolkit import start_function_thread

# Exceptions
from fexception import FValueError


def test_start_function_thread():
    """
    Tests starting a function thread.

    Raises:
        ValueError: A failure occurred in section 1.0 while testing the function 'start_function_thread'. The function did not start a new thread. No 'sample_test_thread' detected.
    """
    print('')
    print('-' * 65)
    print('-' * 65)
    print('Testing Function: start_function_thread')
    print('-' * 65)
    print('-' * 65)
    print('')

    # ############################################################
    # ######Section Test Part 1 (Successful Value Checking)#######
    # ############################################################
    # ========Tests for a successful output return.========
    # Gets the programs root directory.
    preset_root_directory = os.path.dirname(os.path.realpath(__file__))

    # Sets the sample file path.
    sample_file_path = os.path.abspath(f'{preset_root_directory}\\setup.py')

    # Uses sample time.sleep (separate function) to wait 5 seconds. This allows the sleep to run as a separate thread but sleep so that the validation check can detect the separate thread.
    start_function_thread(partial(time.sleep, 5), 'sample_test_thread', False)

    # Checks if the thread is not running
    if 'sample_test_thread' not in str(threading.enumerate()):
        exc_args = {
            'main_message': 'A failure occurred in section 1.0 while testing the function \'start_function_thread\'. The function did not start a new thread. No \'sample_test_thread\' detected.',
        }
        raise FValueError(exc_args)
