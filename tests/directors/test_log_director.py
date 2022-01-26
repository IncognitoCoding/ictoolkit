"""
This script is used to test the log_director module using pytest.
"""
# Built-in/Generic Imports
import os
import os.path

# Local Functions
from ictoolkit import create_logger

# Exceptions
from fexception import FValueError


def test_create_logger():
    """
    This tests creating a logger.

    Raises:
        ValueError: A failure occurred in section 1.0 while testing the function 'create_logger'. No logger was setup during pytest.
    """
    print('')
    print('-' * 65)
    print('-' * 65)
    print('Testing Function: create_logger')
    print('-' * 65)
    print('-' * 65)
    print('')

    # ############################################################
    # ######Section Test Part 1 (Successful Value Checking)#######
    # ############################################################
    # ========Tests for a successful output return.========
    # Gets the programs root directory.
    preset_root_directory = os.path.dirname(os.path.realpath(__file__))

    # Sets the temp log file name.
    log_name = 'temp_pytest_read_write.py'

    # Sets the logger name.
    logger_name = 'pytest_logger'

    # Sets logging format option
    # Option 1 = Default
    # Options:
    #   1 - '%(asctime)s|%(levelname)s|%(message)s (Module:%(module)s, Function:%(funcName)s,  Line:%(lineno)s)',datefmt='%Y-%m-%d %H:%M:%S'
    #   2 - '%(message)s'
    #   '%(asctime)s|%(levelname)s|%(funcName)s|%(message)s' - Manual Entry
    logging_format_option = 1
    # Sets handler option
    # Option 1 = Default
    #   1 - Both
    #   2 - File Handler
    #   3 - Console Handler
    logging_handler_option = 1
    # Sets backup copy count
    logging_backup_log_count = 3
    # Sets logging level
    # Configure based on the LoggingHandlerOption option
    # Options:
    #   - NOTSET
    #   - DEBUG
    #   - INFO
    #   - WARNING
    #   - ERROR
    #   - CRITICAL
    file_log_level = 'DEBUG'
    console_log_level = 'INFO'
    # Sets max log size in bytes
    # Used for issue tracking and program log
    # Default 1000000 Byltes (1 Megabyte)
    max_log_file_size = 1000000
    # Rolling over log file on startup
    rollover = False

    # Gets/Sets the logger for the docker container.
    #
    # These settings are hardcoded and not user programable in the YAML.
    #
    logger_settings = {
        'save_path': preset_root_directory,  # Sets the log save path.
        'logger_name': logger_name,  # Sets the name of the logger.
        'log_name': log_name,  # Set the name of the log file.
        'max_bytes': max_log_file_size,  # Sets the max log file size.
        'file_log_level': file_log_level,  # Sets the file log level. Use DEBUG to keep output from going to the console when using the create_logger function with the YAML logger import function (setup_logger_yaml).
        'console_log_level': console_log_level,  # Sets the console log level. Use DEBUG to keep output from going to the console when using the create_logger function with the YAML logger import function (setup_logger_yaml).
        'backup_count': logging_backup_log_count,  # Sets backup copy count
        'format_option': logging_format_option,  # Sets the log format based on a number option or manual.
        'handler_option': logging_handler_option,  # Sets handler option.
        'rollover': rollover,  # Sets rollover
    }
    # Calls function to setup logging and create the tracker logger.
    logger = create_logger(logger_settings)

    # Expected Return: <class 'logging.Logger'>
    if not isinstance(logger, type(logger)):
        exc_args = {
            'main_message': 'A failure occurred in section 1.0 while testing the function \'create_logger\'. No logger was setup during pytest.',
            'expected_result': 'A logger',
            'returned_result': 'No logger was setup during pytest',
        }
        raise FValueError(exc_args)

    # Sets the sample file path.
    # Uses temp file from write_file test
    sample_file_path = os.path.abspath(f'{preset_root_directory}\\temp_pytest_read_write.py')

    # Gets all handlers.
    handlers = logger.handlers[:]
    for handler in handlers:

        # Closes and removes the handlers.
        handler.close()
        logger.removeHandler(handler)

    # Removes sample write/read file used in all the testing functions.
    # This line needs to be in the last tested function.
    if os.path.isfile(sample_file_path):
        os.remove(sample_file_path)
