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

# Libraries
from fchecker.type import type_check

# Local Functions
from ..helpers.py_helper import get_function_name

# Full path required to avoid partially initialized module error.
from ..directors.yaml_director import read_yaml_config

# Exceptions
from fexception import FKeyError, FCustomException

__author__ = "IncognitoCoding"
__copyright__ = "Copyright 2022, log_director"
__credits__ = ["IncognitoCoding"]
__license__ = "MIT"
__version__ = "3.4"
__maintainer__ = "IncognitoCoding"
__status__ = "Production"


class LoggerSetupFailure(Exception):
    """Exception raised for a logger setup failure."""

    __module__ = "builtins"
    pass


def create_logger(logger_settings: dict) -> logging.Logger:
    """
    This function creates a logger based on specific parameters.\\
    The logger is passed back and can be used throughout the program.\\
    This function is ideal when needing to create new loggers on the fly or for custom usage.\\
    General programing logging should utilize a YAML file with the setup_logger_yaml function.\\
    Checks that existing log handlers do not exist. Log handlers can exist when looping.\\
    This check will prevent child loggers from being created and having duplicate entries.

    Args:
        logger_settings (dict):
        \t\\- formatted dictionary containing all the logger settings.

    Arg Keys:
        logger_settings Keys:\\
        \t\\- save_path (str):\\
        \t\t\\- log file save path\\
        \t\\- logger_name (str):\\
        \t\t\\- logger name\\
        \t\\- log_name (str):\\
        \t\t\\- logger file name\\
        \t\\- max_bytes (int):\\
        \t\t\\- max log size in bytes\\
        \t\\- file_log_level (str):\\
        \t\t\\- file output log level\\
        \t\\- console_log_level (str):\\
        \t\t\\- console output log level\\
        \t\\- backup_count (int):\\
        \t\t\\- backup log copies\\
        \t\\- format_option (int or str):\\
        \t\t\\- allows the ability to select a pre-defined option\\
        \t\t\t\\- options:\\
        \t\t\t\t 1 - '%(asctime)s|%(levelname)s|%(message)s (Module:%(module)s, Function:%(funcName)s,\\
        \t\t\t\t       Line:%(lineno)s)',datefmt='%Y-%m-%d %H:%M:%S' (Default)\\
        \t\t\t\t 2 - '%(message)s'\\
        \t\t\t\t (str) - '%(asctime)s|%(levelname)s|%(funcName)s|%(message)s' - Manual Entry\\
        \t\\- handler_option (int): handler option\\
        \t\t\\- options:\\
        \t\t\t 1 - Both (Default)\\
        \t\t\t 2 - File Handler\\
        \t\t\t 3 - Console Handler

    Raises:
        FTypeError (fexception):
        \t\\- The object value '{logger_settings}' is not an instance of the required class(es) or subclass(es).
        FValueError (fexception):
        \t\\- A general error occurred while validating the logger dictionary keys.
        FKeyError (fexception):
        \t\\- The logger settings dictionary is missing keys.
        FTypeError (fexception):
        \t\\- The object value '{save_path}' is not an instance of the required class(es) or subclass(es).
        FTypeError (fexception):
        \t\\- The object value '{logger_name}' is not an instance of the required class(es) or subclass(es).
        FTypeError (fexception):
        \t\\- The object value '{max_bytes}' is not an instance of the required class(es) or subclass(es).
        FTypeError (fexception):
        \t\\- The object value '{file_log_level}' is not an instance of the required class(es) or subclass(es).
        FTypeError (fexception):
        \t\\- The object value '{console_log_level}' is not an instance of the required class(es) or subclass(es).
        FTypeError (fexception):
        \t\\- The object value '{backup_count}' is not an instance of the required class(es) or subclass(es).
        FTypeError (fexception):
        \t\\- The object value '{format_option}' is not an instance of the required class(es) or subclass(es).
        FTypeError (fexception):
        \t\\- The object value '{handler_option}' is not an instance of the required class(es) or subclass(es).
        LoggerSetupFailure:
        \t\\- Incorrect format_option selection.
        LoggerSetupFailure:
        \t\\- Incorrect handler_option selection.

    Returns:
        logger:
        \t\\- returns the new logger

    Return Example:
    \t\\- <Logger MySoftware1 (DEBUG)>)
    """
    logger = logging.getLogger(__name__)
    logger.debug(f"=" * 20 + get_function_name() + "=" * 20)
    # Custom flowchart tracking. This is ideal for large projects that move a lot.
    # For any third-party modules, set the flow before making the function call.
    logger_flowchart = logging.getLogger("flowchart")
    # Deletes the flowchart log if one already exists.
    logger_flowchart.debug(f"Flowchart --> Function: {get_function_name()}")

    type_check(value=logger_settings, required_type=dict, tb_remove_name="create_logger")

    formatted_logger_settings = "  - logger_settings (dict):\n        - " + "\n        - ".join(
        ": ".join((key, str(val))) for (key, val) in logger_settings.items()
    )
    logger.debug("Passing parameters:\n" f"{formatted_logger_settings}\n")

    # Checks for required dictionary keys.
    # Gets a list of all expected keys.
    # Return Output: ['save_path', 'logger_name', 'log_name', 'max_bytes', 'file_log_level',
    #                 'console_log_level', 'backup_count', 'format_option', 'handler_option']
    logger_settings_keys = list(logger_settings.keys())
    # Checks if the key words exist in the dictionary.
    # This validates the correct dictionary keys for the logger settings.
    if (
        "save_path" not in str(logger_settings_keys)
        or "logger_name" not in str(logger_settings_keys)
        or "log_name" not in str(logger_settings_keys)
        or "max_bytes" not in str(logger_settings_keys)
        or "file_log_level" not in str(logger_settings_keys)
        or "console_log_level" not in str(logger_settings_keys)
        or "backup_count" not in str(logger_settings_keys)
        or "format_option" not in str(logger_settings_keys)
        or "handler_option" not in str(logger_settings_keys)
    ):
        exc_args = {
            "main_message": "The logger settings dictionary is missing keys.",
            "expected_result": [
                "save_path",
                "logger_name",
                "log_name",
                "max_bytes",
                "file_log_level",
                "console_log_level",
                "backup_count",
                "format_option",
                "handler_option",
            ],
            "returned_result": logger_settings_keys,
            "suggested_resolution": "Please verify you have set all required keys and try again.",
        }
        raise FKeyError(exc_args)

    save_path = logger_settings.get("save_path")
    logger_name = logger_settings.get("logger_name")
    log_name = logger_settings.get("log_name")
    max_bytes = logger_settings.get("max_bytes")
    file_log_level = logger_settings.get("file_log_level")
    console_log_level = logger_settings.get("console_log_level")
    backup_count = logger_settings.get("backup_count")
    format_option = logger_settings.get("format_option")
    handler_option = logger_settings.get("handler_option")

    type_check(value=save_path, required_type=str)
    type_check(value=logger_name, required_type=str)
    type_check(value=log_name, required_type=str)
    type_check(value=max_bytes, required_type=int)
    type_check(value=file_log_level, required_type=str)
    type_check(value=console_log_level, required_type=str)
    type_check(value=backup_count, required_type=int)
    type_check(value=format_option, required_type=(str, int))
    type_check(value=handler_option, required_type=int)

    # Sets the log to save the path using namespace.
    namespace = {}
    namespace["base_dir"] = os.path.abspath(save_path)
    namespace["logfile"] = os.path.join(namespace["base_dir"], log_name)
    # Sets flag as False to start.
    existing_logger_flag = False

    # Loops through all active loggers
    for active_logger_names, active_logger_details in logging.Logger.manager.loggerDict.items():
        # Checks if the logger already exists.
        if str(logger_name) in str(active_logger_names):
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
            formatter = logging.Formatter(
                fmt="%(asctime)s|%(levelname)s|%(message)s (Module:%(module)s, Function:%(funcName)s,  Line:%(lineno)s)",
                datefmt="%Y-%m-%d %H:%M:%S",
            )
        elif format_option == 2:
            # Sets custom format and date.
            formatter = logging.Formatter(fmt="%(message)s")
        elif "%" in f"{format_option}":
            formatter = logging.Formatter(fmt=format_option)
        else:
            exc_args = {
                "main_message": "Incorrect format_option selection.",
                "custom_type": LoggerSetupFailure,
                "suggested_resolution": "Please verify you entered a valid format option number or custom format string.",
            }
            raise LoggerSetupFailure(FCustomException(exc_args))

        # Sets handler option based on parameter.
        if handler_option == 1 or handler_option is None:
            # Sets log rotator.
            file_rotation_handler = RotatingFileHandler(
                namespace["logfile"], maxBytes=max_bytes, backupCount=backup_count
            )
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
            file_rotation_handler = RotatingFileHandler(
                namespace["logfile"], maxBytes=max_bytes, backupCount=backup_count
            )
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
            exc_args = {
                "main_message": "Incorrect handler_option selection.",
                "custom_type": LoggerSetupFailure,
                "suggested_resolution": "Please verify you entered a valid handler option number.",
            }
            raise LoggerSetupFailure(FCustomException(exc_args))
    else:
        # Setting the existing logger.
        created_logger = logging.getLogger(logger_name)

    logger.debug(f"Returning value(s):\n  - Return = {created_logger}")
    # Returns logger
    return created_logger


def setup_logger_yaml(yaml_path: str, separate_default_logs: bool = False, allow_basic: Optional[bool] = None) -> None:
    """
    This function sets up a logger for the program using a YAML file.\\
    The configuration must be set up with a YAML file.\\
    This method is the best method for using logging in to additional modules.\\

    Default Path Option Notes:
    \t\\- Default file log handler paths are supported.\\
    \t\\- Cross-platform usage can be a pain and require the path to be the full path.\\
    \t\\- Having default enabled allows the program to set the filename for each log handler.\\
    \t\\- This function allows the ability to have all file log handlers log to the same file,\\
    \t   which is named the same name as the main program, or be individual log files\\
    \t   per file hander, which will be named based on the file handler key name.\\
    \t\\- The "filename:" key value has to be "DEFAULT" in call caps to work.

    Additional Default Option Notes:
    \t\\- A user can define DEFAULT path logs by added :<log name> to the end of DEFAULT.\\
    \t\\- All default logs will be at the root of the main program in a folder called logs.\\
    \t\t\\- default YAML example1 = filename: DEFAULT\\
    \t\t\\- default YAML example2 = filename: DEFAULT:mylog

    Usage:
    \t\\- Setup your logger by running the command below.\\
    \t\t\\- logger = logging.getLogger(__name__)\\
    \t\\- Call this function to setup the logger. No return is required.\\
    \t\\- Call the logger using something similar to the command below.\\
    \t\t\\- logger.info('testing')\\
    \t\\- When using the same logger in other modules the only requirement is to run the command\\
    \t   below within the function. Do not run at the module level. This can cause issues.

    Args:
        yaml_path (str):
        \t\\- yaml configuration file.\\
        separate_default_logs (bool, optional):\\
        \t\\- If default file handelers are being used this allows the files to be separated\\
        \t   using the file handler YAML key name.\\
        \t\t\\- Defaults to False.\\
        \t\t\\- Note:\\
        \t\t\t\\- Default log paths per file hander can only be enabled by setting the key value\\
        \t   for filename: to DEFAULT.\\
        allow_basic (bool, optional):\\
        \t\\- Allows the default log level of "INFO" to be used if the YAML file configuration\\
        \t   fails when set to "True".

    Raises:
        FTypeError (fexception):
        \t\\- The object value '{yaml_path}' is not an instance of the required class(es) or subclass(es).
        FTypeError (fexception):
        \t\\- The object value '{separate_default_logs}' is not an instance of the required class(es) or subclass(es).
        FTypeError (fexception):
        \t\\- The object value '{allow_basic}' is not an instance of the required class(es) or subclass(es).
        LoggerSetupFailure:
        \t\\- The logging hander failed to create.
    """

    type_check(value=yaml_path, required_type=str)
    if separate_default_logs:
        type_check(value=separate_default_logs, required_type=bool)
    if allow_basic:
        type_check(value=allow_basic, required_type=bool)

    # Sets up the logger based on the YAML.
    try:
        # Calls function to pull in YAML configuration.
        config: dict = read_yaml_config(yaml_path, "FullLoader")

        # #######################################################################
        # ###########Checks/Sets Up Default File Logger Path If Required#########
        # #######################################################################
        # Gets YAML return keys.
        all_keys = list(config.keys())
        # Checks if the log handler is a key.
        if "handlers" in str(all_keys):
            # Gets all handler keys.
            handler_keys = list(config["handlers"].keys())
            # Loops through each hander key.
            for handler_key in handler_keys:
                # Gets all handler setting keys for the specific handler entry.
                handler_setting_keys = list(config["handlers"][handler_key].keys())
                # Loops through each handler setting.
                for setting_keys in handler_setting_keys:
                    # Checks if one of the keys contains filename to check if it needs the default log path set.
                    if "filename" in str(setting_keys):
                        # Gets the value from the filename: key.
                        filename_value = config["handlers"][handler_key]["filename"]
                        # Checks if the filename value is "DEFAULT" to set the log with the main program name.
                        if "DEFAULT" == filename_value:
                            # Gets the main program path and file name of the program.
                            # Note: The main program path should not be pulled from the os.path.split command because it does not work correctly on Linux.
                            main_program_path = pathlib.Path.cwd()
                            main_program_file_name = os.path.split(sys.argv[0])[1]
                            # Sets the program log path for the default log path in the YAML.
                            log_path = os.path.abspath(f"{main_program_path}/logs")
                            # Check if main file path exists with a "logs" folder. If not create the folder.
                            # Checks if the save_log_path exists and if not it will be created.
                            # This is required because the logs do not save to the root directory.
                            if not os.path.exists(log_path):
                                os.makedirs(log_path)
                            # Checks if the user wants default log file hander files to be separate.
                            if separate_default_logs:
                                log_file_path = os.path.abspath(f"{log_path}/{handler_key}.log")
                            else:
                                # Removes the .py from the main program name
                                main_program_name = main_program_file_name.replace(".py", "")
                                log_file_path = os.path.abspath(f"{log_path}/{main_program_name}.log")
                            # Update the file log handler file path to the main root.
                            config["handlers"][handler_key]["filename"] = log_file_path
                        # Checks if the filename value is "DEFAULT:" to set the log with the user defined log name.
                        elif "DEFAULT:" in filename_value:
                            # Gets the main program path.
                            # Note: The main program path should not be pulled from the os.path.split command because it does not work correctly on Linux.
                            main_program_path = pathlib.Path.cwd()
                            # Sets the program log path for the default log path in the YAML.
                            log_path = os.path.abspath(f"{main_program_path}/logs")
                            # Check if main file path exists with a "logs" folder. If not create the folder.
                            # Checks if the save_log_path exists and if not it will be created.
                            # This is required because the logs do not save to the root directory.
                            if not os.path.exists(log_path):
                                os.makedirs(log_path)
                            # Checks if the user wants default log file hander files to be separate.
                            if separate_default_logs:
                                log_file_path = os.path.abspath(f"{log_path}/{handler_key}.log")
                            else:
                                # Removes the .py from the main program name
                                # Original Example: DEFAULT:mylog
                                # Returned Example: mylog
                                user_defined_log_name = filename_value.split(":")[1]
                                log_file_path = os.path.abspath(f"{log_path}/{user_defined_log_name}.log")
                            # Update the file log handler file path to the main root.
                            config["handlers"][handler_key]["filename"] = log_file_path
        # Sets the logging configuration from the YAML configuration.
        logging.config.dictConfig(config)
    except Exception as exc:
        # Checks if allow_default is enabled to set up default "Info" logging.
        if allow_basic:
            # Sets the basic logger setup configuration.
            logging.basicConfig(level=logging.INFO)
        else:
            if "Unable to configure handler" in str(exc):
                exc_args = {
                    "main_message": "The logging hander failed to create.",
                    "custom_type": LoggerSetupFailure,
                    "suggested_resolution": "Please verify YAML file configuration.",
                }
                raise LoggerSetupFailure(FCustomException(exc_args))
            else:
                raise exc
