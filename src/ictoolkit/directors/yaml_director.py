"""
This module is designed to assist with log-related actions.

This module does not have a test file to run with pytest. The YAML function will be tested at the start of any program utilizing this method, so additional testing is not provided.
"""
# Built-in/Generic Imports
import logging

# Libraries
import yaml
from typing import Any
from fchecker.type import type_check

# Local Functions
from ..helpers.py_helper import get_function_name

# Exceptions
from fexception import FTypeError, FCustomException, FGeneralError

__author__ = "IncognitoCoding"
__copyright__ = "Copyright 2022, yaml_director"
__credits__ = ["IncognitoCoding"]
__license__ = "MIT"
__version__ = "3.3"
__maintainer__ = "IncognitoCoding"
__status__ = "Production"


class YamlReadFailure(Exception):
    """Exception raised for the thread start failure."""

    __module__ = "builtins"
    pass


def read_yaml_config(yaml_file_path: str, loader: str) -> dict[Any, Any]:
    """
    Reads configuration YAML file data and returns the read configuration.

    Args:
        yaml_file_path (str):
        \t\\- YAML file path.\\
        loader (str):
        \t\\- Loader for the YAML file.\\
        \t\t\\- loader Options:\\
        \t\t\t\\- FullLoader\\
        \t\t\t\t\\- Used for more trusted YAML input.\\
        \t\t\t\t\\- This option will avoid unpredictable code execution.\\
        \t\t\t\\- SafeLoader\\
        \t\t\t\t\\- Used for untrusted YAML input.\\
        \t\t\t\t\\- This will only load a subset of the YAML language.\\
        \t\t\t\\- BaseLoader\\
        \t\t\t\t\\- Used for the most basic YAML input.\\
        \t\t\t\t\\- All loading is strings.\\
        \t\t\t\\- UnsafeLoader\\
        \t\t\t\t\\- Used for original Loader code but could be\\
        \t\t\t\t   easily exploitable by untrusted YAML input.

    Raises:
        FTypeError (fexception):
        \t\\- The object value '{yaml_file_path}' is not an instance of the required class(es) or subclass(es).
        FTypeError (fexception):
        \t\\- The object value '{loader}' is not an instance of the required class(es) or subclass(es).
        YamlReadFailure:
        \t\\- Incorrect YAML loader parameter.
        YamlReadFailure:
        \t\\- A failure occurred while reading the YAML file.
        FGeneralError (fexception):
        \t\\- A general failure occurred while opening the YAML file.

    Returns:
        dict[Any, Any]:
        \t\\- YAML read configuration.
    """
    logger = logging.getLogger(__name__)
    logger.debug(f"=" * 20 + get_function_name() + "=" * 20)
    # Custom flowchart tracking. This is ideal for large projects that move a lot.
    # For any third-party modules, set the flow before making the function call.
    logger_flowchart = logging.getLogger("flowchart")
    logger_flowchart.debug(f"Flowchart --> Function: {get_function_name()}")

    try:
        type_check(value=yaml_file_path, required_type=str)
        type_check(value=loader, required_type=str)
    except FTypeError:
        raise

    logger.debug(
        "Passing parameters:\n"
        f"  - yaml_file_path (str):\n        - {yaml_file_path}\n"
        f"  - loader (str):\n        - {loader}\n"
    )

    # Checks for issues while reading the yaml file.
    try:
        # Calls function to pull in yaml configuration.
        with open(yaml_file_path) as file:
            if "FullLoader" == loader:
                config = yaml.load(file, Loader=yaml.FullLoader)
            elif "SafeLoader" == loader:
                config = yaml.load(file, Loader=yaml.SafeLoader)
            elif "BaseLoader" == loader:
                config = yaml.load(file, Loader=yaml.BaseLoader)
            elif "UnsafeLoader" == loader:
                config = yaml.load(file, Loader=yaml.UnsafeLoader)
            else:
                raise ValueError("Incorrect YAML loader parameter.")
    except Exception as exc:
        if "Incorrect YAML loader parameter" in str(exc):
            exc_args = {
                "main_message": "Incorrect YAML loader parameter.",
                "custom_type": YamlReadFailure,
                "expected_result": ["FullLoader", "SafeLoader", "BaseLoader", "UnsafeLoader"],
                "returned_result": loader,
                "suggested_resolution": "Please verify you have set all required keys and try again.",
            }
            raise YamlReadFailure(FCustomException(exc_args))
        elif "expected <block end>, but found '<scalar>'" in str(exc):
            exc_args = {
                "main_message": "A failure occurred while reading the YAML file.",
                "custom_type": YamlReadFailure,
                "expected_result": ["FullLoader", "SafeLoader", "BaseLoader", "UnsafeLoader"],
                "returned_result": loader,
                "suggested_resolution": [
                    "Please verify you have the correct punctuation on your entries",
                    "For example, having three single quotes will cause this error to occur",
                    "you are using three single quotes, it will help if you use double quotes to begin and end with a single quote in the middle.",
                ],
            }
            raise YamlReadFailure(FCustomException(exc_args))
        else:  # pragma: no cover
            exc_args = {
                "main_message": "A general failure occurred while opening the YAML file.",
                "original_exception": exc,
            }
            raise FGeneralError(exc_args)
    else:
        logger.debug(f"Returning value(s):\n  - Return = {config}")
        print(type(config))
        return config
