#!interpreter

"""
This module is designed to assist with log-related actions.
"""

# Built-in/Generic Imports
import os
import logging
import logging.config
import traceback
from logging.handlers import RotatingFileHandler

# Own modules
from ictoolkit.directors.yaml_director import read_yaml_config

__author__ = 'IncognitoCoding'
__copyright__ = 'Copyright 2021, log_director'
__credits__ = ['IncognitoCoding']
__license__ = 'GPL'
__version__ = '1.3'
__maintainer__ = 'IncognitoCoding'
__status__ = 'Development'


def create_logger(save_path, logger_name, log_name, max_bytes, file_log_level, console_log_level, backup_count, format_option, handler_option, rollover):
    """
    Creates a logger based on specific parameters. The logger is passed back and can be used throughout the program.

    Checks that existing log handlers do not exist. Log handlers can exist when looping. This check will prevent child loggers from being created and having duplicate entries.

    Args:
        save_path (str): log file save path
        logger_name (str): logger name
        log_name (str): logger file name
        max_bytes (int): max log size in bytes
        file_log_level (str): file output log level
        console_log_level (str): consoel output log level
        backup_count (int): backup log copies
        format_option (int or st): allows the ability to select a pre-defined option
            options:
                1 - '%(asctime)s|%(levelname)s|%(message)s (Module:%(module)s, Function:%(funcName)s,  Line:%(lineno)s)',datefmt='%Y-%m-%d %H:%M:%S' (Default)
                2 - '%(message)s'
                '%(asctime)s|%(levelname)s|%(funcName)s|%(message)s' - Manual Entry
        handler_option (int): handler option
            options:
                1 - Both (Default)
                2 - File Handler
                3 - Console Handler
        rollover (bool): rolling over to simulate the log file reaching maxBytes size.
        
    Raises:
        ValueError: Incorrect format_option selection
        ValueError: Incorrect handler_option selection
        ValueError: General exceptions when creating logger

    Returns:
        logger: returns the logger (Return Example: create_logger[0]: <Logger __main__ (DEBUG)>)
    """
    
    try:

        # Sets the log save path using namespace.
        namespace = {}
        namespace['base_dir'] = os.path.abspath(save_path)
        namespace['logfile'] = os.path.join(namespace['base_dir'], log_name)
        
        # Sets logger name.
        logger = logging.getLogger(logger_name)
        
        # Checks if a log handler already exists.
        # Log handlers can exist when looping. This check will prevent child loggers from being created and having duplicate entries.
        if not logger.hasHandlers():
               
            # Sets logger level to Debug to cover all handelers levels that are preset.
            # Default = Warning and will restrict output to the handlers even if they are set to a lower level.
            logger.setLevel(logging.DEBUG)
            
            # Changes character format for logging levels.
            logging.addLevelName(logging.DEBUG, 'Debug')
            logging.addLevelName(logging.INFO, 'Info')
            logging.addLevelName(logging.WARNING, 'Warning')
            logging.addLevelName(logging.ERROR, 'Error')
            logging.addLevelName(logging.CRITICAL, 'Critical')
            logging.addLevelName(logging.FATAL, 'Fatal')

            # Custom level used for supported programs.
            # Created for use when monitoring logs to show its an alert and not an error.
            logging.addLevelName(39,"Alert")

            # Sets the log format based on a number option or manual based on parameter.
            if format_option == 1 or format_option is None:

                # Sets custom format and date
                formatter = logging.Formatter(fmt='%(asctime)s|%(levelname)s|%(message)s (Module:%(module)s, Function:%(funcName)s,  Line:%(lineno)s)',datefmt='%Y-%m-%d %H:%M:%S')

            elif format_option == 2:

                # Sets custom format and date.
                formatter = logging.Formatter(fmt='%(message)s')

            elif '%' in f'{format_option}':

                formatter = logging.Formatter(fmt=format_option)

            else:
                raise ValueError(f'Incorrect format_option selection. Please verify you entered a valid format option number or custom format string. Originating error on line {traceback.extract_stack()[-1].lineno} in <{__name__}>')


            # Sets handler option based on parameter.
            if handler_option == 1 or handler_option is None:

                # Sets log rotator.
                file_rotation_handler = RotatingFileHandler(namespace['logfile'], maxBytes=max_bytes, backupCount=backup_count)
                # Sets the level logging entry from a variable.
                file_level = logging.getLevelName(file_log_level)
                # Sets the logging level.
                file_rotation_handler.setLevel(file_level)

                # Sets logging stream handler.
                console_stream_handler = logging.StreamHandler()
                # Sets the level logging entry from a variable.
                console_level = logging.getLevelName(console_log_level)
                # Sets the logging level.
                console_stream_handler.setLevel(console_level)

                console_stream_handler.setFormatter(formatter)
                file_rotation_handler.setFormatter(formatter)
                logger.addHandler(console_stream_handler)
                logger.addHandler(file_rotation_handler)
                   
                # Checks if log file exists and if Rollover is enabled.
                if os.path.isfile(namespace['logfile']) and rollover == True:

                    # Rolling over to simulate the log file reaching maxBytes size.
                    file_rotation_handler.doRollover()
                    
            elif handler_option == 2:

                # Sets log rotator.
                file_rotation_handler = RotatingFileHandler(namespace['logfile'], maxBytes=max_bytes, backupCount=backup_count)
                # Sets the level logging entry from a variable.
                file_level = logging.getLevelName(file_log_level)
                # Sets the logging level.
                file_rotation_handler.setLevel(file_level)

                file_rotation_handler.setFormatter(formatter)
                logger.addHandler(file_rotation_handler)
                
                # Checks if log file exists and if Rollover is enabled.
                if os.path.isfile(namespace['logfile']) and rollover == True:

                    # Rolling over to simulate the log file reaching maxBytes size.
                    file_rotation_handler.doRollover()
                    
            elif handler_option == 3:

                # Sets logging stream handler.
                console_stream_handler = logging.StreamHandler()
                # Sets the level logging entry from a variable.
                console_level = logging.getLevelName(console_log_level)
                # Sets the logging level.
                console_stream_handler.setLevel(console_level)

                console_stream_handler.setFormatter(formatter)
                logger.addHandler(console_stream_handler)

            else:
                raise ValueError(f'Incorrect handler_option selection. Please verify you entered a valid handler option number. Originating error on line {traceback.extract_stack()[-1].lineno} in <{__name__}>')
    
    except Exception as err:
        raise ValueError(f'{err}')

    # Returns logger
    return logger


def setup_logger_yaml(yaml_path):
    """
    This function sets up a logger for the program. The configuration must be setup with a YAML file. This method is the best method for using logging in to additional modules.

    See the sample folder for an example configuration file.

    Usage:
        Setup your logger by running the command below.
            - logger = logging.getLogger(__name__)
        Call this function to setup the logger. No return is required.
        Call the logger using something similar to the command below.
            - logger.info('testing')

        Note: When using the same logger in other modules the only requirement is to run the command below within the function. Do not run at the module level. This can cause issues.
            - logger = logging.getLogger(__name__)

    Args:
        yaml_path (str): yaml configuration file.
    """
    try:
        # Calls function to pull in YAML configuration.
        config = read_yaml_config(yaml_path)
        logging.config.dictConfig(config)
    except:
        logging.basicConfig(level=logging.INFO)