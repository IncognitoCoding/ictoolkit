"""
This module is designed to assist with log-related actions.
"""

# Built-in/Generic Imports
import os
import sys
import pathlib
import logging
import logging.config
from logging.handlers import RotatingFileHandler
from typing import Optional

# Own modules
from ictoolkit.directors.yaml_director import read_yaml_config
from ictoolkit.directors.validation_director import value_type_validation
from ictoolkit.directors.error_director import error_formatter
from ictoolkit.helpers.py_helper import get_function_name, get_line_number

__author__ = 'IncognitoCoding'
__copyright__ = 'Copyright 2021, log_director'
__credits__ = ['IncognitoCoding']
__license__ = 'GPL'
__version__ = '2.10'
__maintainer__ = 'IncognitoCoding'
__status__ = 'Development'


def create_logger(logger_settings: dict) -> logging.Logger:
    """
    This function creates a logger based on specific parameters. The logger is passed back and can be used throughout the program.
    This function is ideal when needing to create new loggers on the fly or for custom usage. General programing logging should utilize a YAML file with the setup_logger_yaml function.

    Checks that existing log handlers do not exist. Log handlers can exist when looping. This check will prevent child loggers from being created and having duplicate entries.

    Note: Version 2.3 has updated all the passing parameters into a single dictionary. Please update any previous code from individual parameters to a single dictionary. This function
          has been deprecated since v1.8.

    Args:
        logger_settings (dict): formatted dictionary containing all the logger settings.\n
            \\- Key Value:
                save_path (str): log file save path
                logger_name (str): logger name
                log_name (str): logger file name
                max_bytes (int): max log size in bytes
                file_log_level (str): file output log level
                console_log_level (str): console output log level
                backup_count (int): backup log copies
                format_option (int or str): allows the ability to select a pre-defined option
                    options:
                        1 - '%(asctime)s|%(levelname)s|%(message)s (Module:%(module)s, Function:%(funcName)s,  Line:%(lineno)s)',datefmt='%Y-%m-%d %H:%M:%S' (Default)\\
                        2 - '%(message)s'\\
                        \\'%(asctime)s|%(levelname)s|%(funcName)s|%(message)s' - Manual Entry
                handler_option (int): handler option
                    options:
                        1 - Both (Default)
                        2 - File Handler
                        3 - Console Handler

            \\- For Example: logger_settings = {
                'save_path': central_log_path,
                'logger_name': container_name,
                'log_name': log_name,
                'max_bytes': max_log_file_size,
                'file_log_level': 'INFO',
                'console_log_level': 'INFO',
                'backup_count': 4,
                'format_option': '%(message)s',
                'handler_option': 2,
            }

    Raises:
        ValueError: The logger settings dictionary is missing keys.
        ValueError: Incorrect format_option selection
        ValueError: Incorrect handler_option selection
        ValueError: General exceptions when creating logger

    Returns:
        logger: returns the new logger (Return Example: create_logger: <Logger MySoftware1 (DEBUG)>)
    """
    logger = logging.getLogger(__name__)
    logger.debug(f'=' * 20 + get_function_name() + '=' * 20)
    # Custom flowchart tracking. This is ideal for large projects that move a lot.
    # For any third-party modules, set the flow before making the function call.
    logger_flowchart = logging.getLogger('flowchart')
    # Deletes the flowchart log if one already exists.
    logger_flowchart.debug(f'Flowchart --> Function: {get_function_name()}')

    # Checks function launch variables and logs passing parameters.
    try:
        value_type_validation(logger_settings, dict, __name__, get_line_number())

        # Requires pre-logger formatting because the logger can not use one line if/else or join without excluding sections of the the output.
        formatted_logger_settings = '  - logger_settings (dict):\n        - ' + '\n        - '.join(': '.join((key, str(val))) for (key, val) in logger_settings.items())
        logger.debug(
            'Passing parameters:\n'
            f'{formatted_logger_settings}\n'
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
    
    # Checks for required dictionary keys.
    try:
        # ####################################################################
        # ###################Dictionary Key Validation########################
        # ####################################################################
        # Gets a list of all expected keys.
        # Return Output: ['save_path', 'logger_name', 'log_name', 'max_bytes', 'file_log_level', 'console_log_level', 'backup_count', 'format_option', 'handler_option']
        logger_settings_keys = list(logger_settings.keys())
        # Checks if the key words exist in the dictionary.
        # This validates the correct dictionary keys for the logger settings.
        if (
            'save_path' not in str(logger_settings_keys)
            or 'logger_name' not in str(logger_settings_keys)
            or 'log_name' not in str(logger_settings_keys)
            or 'max_bytes' not in str(logger_settings_keys)
            or 'file_log_level' not in str(logger_settings_keys)
            or 'console_log_level' not in str(logger_settings_keys)
            or 'backup_count' not in str(logger_settings_keys)
            or 'format_option' not in str(logger_settings_keys)
            or 'handler_option' not in str(logger_settings_keys)
        ):
            error_args = {
                'main_message': 'The logger settings dictionary is missing keys.',
                'error_type': KeyError,
                'expected_result': ['save_path', 'logger_name', 'log_name', 'max_bytes', 'file_log_level', 'console_log_level', 'backup_count', 'format_option', 'handler_option'],
                'returned_result': logger_settings_keys,
                'suggested_resolution': 'Please verify you have set all required keys and try again.',
            }
            error_formatter(error_args, __name__, get_line_number())
    except Exception as error:
        if 'Originating error on line' in str(error):
            logger.debug(f'Forwarding caught {type(error).__name__} at line {error.__traceback__.tb_lineno} in <{__name__}>')
            raise error
        else:
            error_args = {
                'main_message': 'A general error occurred while validating the logger dictionary keys.',
                'error_type': Exception,
                'original_error': error,
            }
            error_formatter(error_args, __name__, error.__traceback__.tb_lineno)

    # Gets dictionary values and validates value types.
    try:
        save_path = logger_settings.get('save_path')
        logger_name = logger_settings.get('logger_name')
        log_name = logger_settings.get('log_name')
        max_bytes = logger_settings.get('max_bytes')
        file_log_level = logger_settings.get('file_log_level')
        console_log_level = logger_settings.get('console_log_level')
        backup_count = logger_settings.get('backup_count')
        format_option = logger_settings.get('format_option')
        handler_option = logger_settings.get('handler_option')

        value_type_validation(save_path, str, __name__, get_line_number())
        value_type_validation(logger_name, str, __name__, get_line_number())
        value_type_validation(log_name, str, __name__, get_line_number())
        value_type_validation(max_bytes, int, __name__, get_line_number())
        value_type_validation(file_log_level, str, __name__, get_line_number())
        value_type_validation(console_log_level, str, __name__, get_line_number())
        value_type_validation(backup_count, int, __name__, get_line_number())
        value_type_validation(format_option, [str, int], __name__, get_line_number())
        value_type_validation(handler_option, int, __name__, get_line_number())
    except Exception as error:
        if 'Originating error on line' in str(error):
            logger.debug(f'Forwarding caught {type(error).__name__} at line {error.__traceback__.tb_lineno} in <{__name__}>')
            raise error
        else:
            error_args = {
                'main_message': 'A general error occurred while getting and validating the logger dictionary values.',
                'error_type': Exception,
                'original_error': error,
            }
            error_formatter(error_args, __name__, error.__traceback__.tb_lineno)

    # Creates or returns a logger.
    try:
        # Sets the log save path using namespace.
        namespace = {}
        namespace['base_dir'] = os.path.abspath(save_path)
        namespace['logfile'] = os.path.join(namespace['base_dir'], log_name)
        # Sets flag as False to start.
        existing_logger_flag = False

        # Loops through all active loggers
        for active_logger_names, active_logger_details in logging.Logger.manager.loggerDict.items():
            # Checks if the logger already exists.
            if logger_name in active_logger_names:
                existing_logger_flag = True
                break
            else:
                existing_logger_flag = False
        # Checks if a log handler already exists.
        # Log handlers can exist when looping. This check will prevent child loggers from being created and having duplicate entries.
        if existing_logger_flag is False:
            # Sets logger name.
            created_logger = logging.getLogger(logger_name)
            # Sets logger level to Debug to cover all handelers levels that are preset.
            # Default = Warning and will restrict output to the handlers even if they are set to a lower level.
            created_logger.setLevel(logging.DEBUG)
            # Custom level used for supported programs.
            # Created for use when monitoring logs to show its an alert and not an error.
            logging.addLevelName(39, "ALERT")

            # Sets the log format based on a number option or manual based on parameter.
            if format_option == 1 or format_option is None:
                # Sets custom format and date
                formatter = logging.Formatter(fmt='%(asctime)s|%(levelname)s|%(message)s (Module:%(module)s, Function:%(funcName)s,  Line:%(lineno)s)', datefmt='%Y-%m-%d %H:%M:%S')
            elif format_option == 2:
                # Sets custom format and date.
                formatter = logging.Formatter(fmt='%(message)s')
            elif '%' in f'{format_option}':
                formatter = logging.Formatter(fmt=format_option)
            else:
                error_args = {
                    'main_message': 'Incorrect format_option selection.',
                    'error_type': ValueError,
                    'suggested_resolution': 'Please verify you entered a valid format option number or custom format string.',
                }
                error_formatter(error_args, __name__, get_line_number())

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
                created_logger.addHandler(console_stream_handler)
                created_logger.addHandler(file_rotation_handler)
            elif handler_option == 2:
                # Sets log rotator.
                file_rotation_handler = RotatingFileHandler(namespace['logfile'], maxBytes=max_bytes, backupCount=backup_count)
                # Sets the level logging entry from a variable.
                file_level = logging.getLevelName(file_log_level)
                # Sets the logging level.
                file_rotation_handler.setLevel(file_level)
                file_rotation_handler.setFormatter(formatter)
                created_logger.addHandler(file_rotation_handler)
            elif handler_option == 3:
                # Sets logging stream handler.
                console_stream_handler = logging.StreamHandler()
                # Sets the level logging entry from a variable.
                console_level = logging.getLevelName(console_log_level)
                # Sets the logging level.
                console_stream_handler.setLevel(console_level)

                console_stream_handler.setFormatter(formatter)
                created_logger.addHandler(console_stream_handler)
            else:
                error_args = {
                    'main_message': 'Incorrect handler_option selection.',
                    'error_type': ValueError,
                    'suggested_resolution': 'Please verify you entered a valid handler option number.',
                }
                error_formatter(error_args, __name__, get_line_number())
        else:
            # Setting the existing logger.
            created_logger = logging.getLogger(logger_name)
        
        logger.debug(f'Returning value(s):\n  - Return = {created_logger}')
        # Returns logger
        return created_logger
    except Exception as error:
        if 'Originating error on line' in str(error):
            logger.debug(f'Forwarding caught {type(error).__name__} at line {error.__traceback__.tb_lineno} in <{__name__}>')
            raise error
        else:
            error_args = {
                'main_message': 'A general issue occurred while create the new logger.',
                'error_type': Exception,
                'original_error': error,
            }
            error_formatter(error_args, __name__, error.__traceback__.tb_lineno)


def setup_logger_yaml(yaml_path: str, separate_default_logs: Optional[bool] = False, allow_basic: Optional[bool] = None) -> None:
    """
    This function sets up a logger for the program. The configuration must be setup with a YAML file. This method is the best method for using logging in to additional modules.

    Default file log handler paths are supported. Cross-platform usage can be a pain and require the path to be the full path. Having default enabled allows the program to set the\\
    filename for each log handler. This function allows the ability to have all file log handlers log to the same file, which is named the same name as the main program, or be
    individual log files per file hander, which will be named based on the file handler key name. The "filename:" key value has to be "DEFAULT" in call caps to work.\\
    Also, user defined DEFAULT path logs can be added by adding :<log name> to the end of DEFAULT.
    All default logs will be at the root of the main program in a folder called logs.
    - default YAML example1 = filename: DEFAULT
    - default YAML example2 = filename: DEFAULT:mylog

    See the sample folder for an example configuration file.

    Usage:
    - Setup your logger by running the command below.
            - logger = logging.getLogger(__name__)
    - Call this function to setup the logger. No return is required.
    - Call the logger using something similar to the command below.
            - logger.info('testing')
   - Note: When using the same logger in other modules the only requirement is to run the command below within the function. Do not run at the module level. This can cause issues.
            - logger = logging.getLogger(__name__)

    Args:
        yaml_path (str): yaml configuration file.
        separate_default_logs (bool, optional): If default file handelers are being used this allows the files to be separated using the file handler YAML key name. Defaults to False.
            \- Note: Default log paths per file hander can only be enabled by setting the key value for filename: to DEFAULT.
        allow_basic (bool, optional): Allows the default log level of "INFO" to be used if the YAML file configuration fails when set to "True".

    Raises:
        ValueError: The logging hander failed to create.
        ValueError: The logger failed to setup.
    """

    # Checks function launch variables.
    try:
        value_type_validation(yaml_path, str, __name__, get_line_number())
        if separate_default_logs:
            value_type_validation(separate_default_logs, bool, __name__, get_line_number())
        if allow_basic:
            value_type_validation(allow_basic, bool, __name__, get_line_number())
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

    # Sets up the logger based on the YAML.
    try:
        # Calls function to pull in YAML configuration.
        config = read_yaml_config(yaml_path, 'FullLoader')

        # #######################################################################
        # ###########Checks/Sets Up Default File Logger Path If Required#########
        # #######################################################################
        # Gets YAML return keys.
        all_keys = list(config.keys())
        # Checks if the log handler is a key.
        if 'handlers' in str(all_keys):
            # Gets all handler keys.
            handler_keys = list(config['handlers'].keys())
            # Loops through each hander key.
            for handler_key in handler_keys:
                # Gets all handler setting keys for the specific handler entry.
                handler_setting_keys = list(config['handlers'][handler_key].keys())
                # Loops through each handler setting.
                for setting_keys in handler_setting_keys:
                    # Checks if one of the keys contains filename to check if it needs the default log path set.
                    if 'filename' in str(setting_keys):
                        # Gets the value from the filename: key.
                        filename_value = config['handlers'][handler_key]['filename']
                        # Checks if the filename value is "DEFAULT" to set the log with the main program name.
                        if 'DEFAULT' == filename_value:
                            # Gets the main program path and file name of the program.
                            # Note: The main program path should not be pulled from the os.path.split command because it does not work correctly on Linux.
                            main_program_path = pathlib.Path.cwd()
                            main_program_file_name = os.path.split(sys.argv[0])[1]
                            # Sets the program log path for the default log path in the YAML.
                            log_path = os.path.abspath(f'{main_program_path}/logs')
                            # Check if main file path exists with a "logs" folder. If not create the folder.
                            # Checks if the save_log_path exists and if not it will be created.
                            # This is required because the logs do not save to the root directory.
                            if not os.path.exists(log_path):
                                os.makedirs(log_path)
                            # Checks if the user wants default log file hander files to be separate.
                            if separate_default_logs:
                                log_file_path = os.path.abspath(f'{log_path}/{handler_key}.log')
                            else:
                                # Removes the .py from the main program name
                                main_program_name = main_program_file_name.replace('.py', '')
                                log_file_path = os.path.abspath(f'{log_path}/{main_program_name}.log')
                            # Update the file log handler file path to the main root.
                            config['handlers'][handler_key]['filename'] = log_file_path
                        # Checks if the filename value is "DEFAULT:" to set the log with the user defined log name.
                        elif 'DEFAULT:' in filename_value:
                            # Gets the main program path.
                            # Note: The main program path should not be pulled from the os.path.split command because it does not work correctly on Linux.
                            main_program_path = pathlib.Path.cwd()
                            # Sets the program log path for the default log path in the YAML.
                            log_path = os.path.abspath(f'{main_program_path}/logs')
                            # Check if main file path exists with a "logs" folder. If not create the folder.
                            # Checks if the save_log_path exists and if not it will be created.
                            # This is required because the logs do not save to the root directory.
                            if not os.path.exists(log_path):
                                os.makedirs(log_path)
                            # Checks if the user wants default log file hander files to be separate.
                            if separate_default_logs:
                                log_file_path = os.path.abspath(f'{log_path}/{handler_key}.log')
                            else:
                                # Removes the .py from the main program name
                                # Original Example: DEFAULT:mylog
                                # Returned Example: mylog
                                user_defined_log_name = filename_value.split(':')[1]
                                log_file_path = os.path.abspath(f'{log_path}/{user_defined_log_name}.log')
                            # Update the file log handler file path to the main root.
                            config['handlers'][handler_key]['filename'] = log_file_path
        # Sets the logging configuration from the YAML configuration.
        logging.config.dictConfig(config)
    except Exception as error:
        if 'Originating error on line' in str(error):
            raise error
        else:
            # Checks if allow_default is enabled to setup default "Info" logging.
            if allow_basic:
                # Sets the basic logger setup configuration.
                logging.basicConfig(level=logging.INFO)
            else:
                if 'Unable to configure handler' in str(error):
                    error_args = {
                        'main_message': 'The logging hander failed to create.',
                        'error_type': Exception,
                        'original_error': 'Please verify YAML file configuration.',
                    }
                    error_formatter(error_args, __name__, error.__traceback__.tb_lineno)
                else:
                    error_args = {
                        'main_message': 'A general exception occurred the logger setup.',
                        'error_type': Exception,
                        'original_error': error,
                    }
                    error_formatter(error_args, __name__, error.__traceback__.tb_lineno)
