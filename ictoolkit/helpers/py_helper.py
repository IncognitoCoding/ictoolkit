"""
This module is designed to help retrieve python information. The module only contains short, simple, helpful python helper functions. No error checking or logging is done on these functions because they are not receiving any variables.
"""

# Built-in/Generic Imports
from inspect import currentframe
import inspect
from types import FrameType
from typing import cast

__author__ = 'IncognitoCoding'
__copyright__ = 'Copyright 2021, py_helper'
__credits__ = ['IncognitoCoding']
__license__ = 'GPL'
__version__ = '1.0'
__maintainer__ = 'IncognitoCoding'
__status__ = 'Development'


def get_line_number() -> int:
    """Returns the calling function's line number."""
    cf = currentframe()
    return cf.f_back.f_lineno


def get_function_name() -> str:
    """Return the calling function's name."""
    return cast(FrameType, cast(FrameType, inspect.currentframe()).f_back).f_code.co_name
