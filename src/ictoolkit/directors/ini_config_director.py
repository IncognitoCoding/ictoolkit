"""
This module is designed to assist with INI-related actions.

This module does not have a test file to run with pytest. The INI function will be tested at the start of any program utilizing this method, so additional testing is not provided.
"""
# Built-in/Generic Imports
import logging

# Libraries
from fchecker.type import type_check
from configparser import RawConfigParser, ConfigParser

# Local Functions
from ..helpers.py_helper import get_function_name

# Exceptions
from fexception import FGeneralError, FTypeError

__author__ = "IncognitoCoding"
__copyright__ = "Copyright 2022, ini_config_director"
__credits__ = ["IncognitoCoding"]
__license__ = "MIT"
__version__ = "3.2"
__maintainer__ = "IncognitoCoding"
__status__ = "Production"


def read_ini_config(ini_file_path: str) -> RawConfigParser:
    """
    Reads configuration INI file data and returns the read configuration.

    Args:
        ini_file_path (str):
        \t\\- The file path to the INI file.

    Raises:
        FTypeError (fexception):
        \t\\- The object value '{ini_file_path}' is not an instance of the required class(es) or subclass(es).
        FGeneralError (fexception):
        \t\\- A general exception occurred while reading the INI configuration file.

    Returns:
        ini:
        \t\\- INI read configuration.
    """
    logger = logging.getLogger(__name__)
    logger.debug(f"=" * 20 + get_function_name() + "=" * 20)
    # Custom flowchart tracking. This is ideal for large projects that move a lot.
    # For any third-party modules, set the flow before making the function call.
    logger_flowchart = logging.getLogger("flowchart")
    logger_flowchart.debug(f"Flowchart --> Function: {get_function_name()}")

    try:
        type_check(value=ini_file_path, required_type=str)
    except FTypeError:
        raise

    logger.debug("Passing parameters:\n" f"  - ini_file_path (str):\n        - {ini_file_path}\n")

    # Checks for issues while reading the ini file.
    try:
        # Calls function to pull in ini configuration.
        # Uses RawConfigParser for special characters.
        config: RawConfigParser = RawConfigParser()
        config.read(ini_file_path)
    except Exception as exc:  # pragma: no cover
        exc_args = {
            "main_message": "A general exception occurred while reading the ini configuration file.",
            "original_exception": exc,
        }
        raise FGeneralError(exc_args)
    else:
        return config
