"""
This module is designed for validation checks. All modules will not return any data but throw exception errors when validation fails.
"""
# Built-in/Generic Imports
import traceback
import logging
from typing import Any, Optional, Union

__author__ = 'IncognitoCoding'
__copyright__ = 'Copyright 2021, validation_director'
__credits__ = ['IncognitoCoding']
__license__ = 'GPL'
__version__ = '1.3'
__maintainer__ = 'IncognitoCoding'
__status__ = 'Development'


def value_type_validation(value: any, required_type: Union[type, list], caller_module: Optional[str] = None, caller_function: Optional[str] = None, caller_line: Optional[int] = None) -> None:
    """
    A simple type validation validation check.

    Adding the caller_module, caller_function, or caller_line will provide more error return details.

    Args:
        value (any): Any value needing its type validated.
        required_type (type or list of types): The required type the value should match. Can be a single type or list of types.
        caller_module (str, optional): The name of the caller module. Use \'__name__\'. Defaults to None.
        caller_function (str, optional): The calling function name. Defaults to None.
        caller_line (int, optional): The calling function line. Defaults to None.
    Raises:
        TypeError: The value \'{value}\' is not in {required_type} format.
    """
    logger = logging.getLogger(__name__)
    logger.debug(f'=' * 20 + traceback.extract_stack(None, 2)[1][2] + '=' * 20)
    # Custom flowchart tracking. This is ideal for large projects that move a lot.
    # For any third-party modules, set the flow before making the function call.
    logger_flowchart = logging.getLogger('flowchart')
    # Deletes the flowchart log if one already exists.
    logger_flowchart.debug(f'Flowchart --> Function: {traceback.extract_stack(None, 2)[1][2]}')

    logger.debug(
        'Passing parameters:\n'
        f'  - value (any):\n        - {value}\n'
        f'  - required_type (type):\n        - {required_type}'
    )

    # Verifies a value is sent.
    if (
        value is not None
        and value != ''
    ):
        # Verifies a type or list is sent.
        if (
            isinstance(required_type, list)
            or isinstance(required_type, type)
        ):
            if isinstance(required_type, list):
                for value_type in required_type:
                    if isinstance(value, value_type):
                        matching_type_flag = True
                        break
                    else:
                        matching_type_flag = False
            else:
                # Verifies the returning YAML value.
                if not isinstance(value, required_type):
                    matching_type_flag = False
                else:
                    matching_type_flag = True
            # Checks for no match.
            if matching_type_flag is False:
                if (
                    caller_module
                    and caller_function
                    and caller_line
                ):
                    error_message = (
                        f'The value \'{value}\' is not in {required_type} format.\n'
                        + (('-' * 150) + '\n') + (('-' * 65) + 'Additional Information' + ('-' * 63) + '\n') + (('-' * 150) + '\n')
                        + 'Caller Module:\n'
                        f'  - {caller_module}\n\n'
                        'Caller Function:\n'
                        f'  - {caller_function}\n\n'
                        'Caller Line:\n'
                        f'  - {caller_line}\n\n'
                        'Expected Result:\n'
                        f'  - Type = {required_type}\n\n'
                        'Returned Result:\n'
                        f'  - Type = {type(value)}\n\n'
                        f'Originating error on line {traceback.extract_stack()[-1].lineno} in <{__name__}>\n'
                        + (('-' * 150) + '\n') * 2
                    )
                    logger.error(error_message)
                    raise TypeError(error_message)
                elif (
                    caller_module
                    and not caller_function
                    and not caller_line
                ):
                    error_message = (
                        f'The value \'{value}\' is not in {required_type} format.\n'
                        + (('-' * 150) + '\n') + (('-' * 65) + 'Additional Information' + ('-' * 63) + '\n') + (('-' * 150) + '\n')
                        + 'Caller Module:\n'
                        f'  - {caller_module}\n\n'
                        'Expected Result:\n'
                        f'  - Type = {required_type}\n\n'
                        'Returned Result:\n'
                        f'  - Type = {type(value)}\n\n'
                        f'Originating error on line {traceback.extract_stack()[-1].lineno} in <{__name__}>\n'
                        + (('-' * 150) + '\n') * 2
                    )
                    logger.error(error_message)
                    raise TypeError(error_message)
                elif (
                    caller_module
                    and not caller_function
                    and caller_line
                ):
                    error_message = (
                        f'The value \'{value}\' is not in {required_type} format.\n'
                        + (('-' * 150) + '\n') + (('-' * 65) + 'Additional Information' + ('-' * 63) + '\n') + (('-' * 150) + '\n')
                        + 'Caller Module:\n'
                        f'  - {caller_module}\n\n'
                        'Caller Line:\n'
                        f'  - {caller_line}\n\n'
                        'Expected Result:\n'
                        f'  - Type = {required_type}\n\n'
                        'Returned Result:\n'
                        f'  - Type = {type(value)}\n\n'
                        f'Originating error on line {traceback.extract_stack()[-1].lineno} in <{__name__}>\n'
                        + (('-' * 150) + '\n') * 2
                    )
                    logger.error(error_message)
                    raise TypeError(error_message)
                elif (
                    not caller_module
                    and caller_line
                    and caller_function
                ):
                    error_message = (
                        f'The value \'{value}\' is not in {required_type} format.\n'
                        + (('-' * 150) + '\n') + (('-' * 65) + 'Additional Information' + ('-' * 63) + '\n') + (('-' * 150) + '\n')
                        + 'Caller Function:\n'
                        f'  - {caller_function}\n\n'
                        'Caller Line:\n'
                        f'  - {caller_line}\n\n'
                        'Expected Result:\n'
                        f'  - Type = {required_type}\n\n'
                        'Returned Result:\n'
                        f'  - Type = {type(value)}\n\n'
                        f'Originating error on line {traceback.extract_stack()[-1].lineno} in <{__name__}>\n'
                        + (('-' * 150) + '\n') * 2
                    )
                    logger.error(error_message)
                    raise TypeError(error_message)
                elif (
                    not caller_module
                    and not caller_function
                    and not caller_line
                ):
                    error_message = (
                        f'The value \'{value}\' is not in {required_type} format.\n'
                        + (('-' * 150) + '\n') + (('-' * 65) + 'Additional Information' + ('-' * 63) + '\n') + (('-' * 150) + '\n')
                        + 'Expected Result:\n'
                        f'  - Type = {required_type}\n\n'
                        'Returned Result:\n'
                        f'  - Type = {type(value)}\n\n'
                        f'Originating error on line {traceback.extract_stack()[-1].lineno} in <{__name__}>\n'
                        + (('-' * 150) + '\n') * 2
                    )
                    logger.error(error_message)
                    raise TypeError(error_message)
        else:
            error_message = (
                f'No type or list of types has been entered for type validation.\n\n'
                + (('-' * 150) + '\n') + (('-' * 65) + 'Additional Information' + ('-' * 63) + '\n') + (('-' * 150) + '\n')
                + 'Suggested Resolution:\n'
                f'  - Please check the calling function.\n\n'
                f'Originating error on line {traceback.extract_stack()[-1].lineno} in <{__name__}>\n'
                + (('-' * 150) + '\n') * 2
            )
            logger.error(error_message)
            raise ValueError(error_message)
    else:
        error_message = (
            f'No value has been entered for type validation.\n\n'
            + (('-' * 150) + '\n') + (('-' * 65) + 'Additional Information' + ('-' * 63) + '\n') + (('-' * 150) + '\n')
            + 'Suggested Resolution:\n'
            f'  - Please check the calling function.\n\n'
            f'Originating error on line {traceback.extract_stack()[-1].lineno} in <{__name__}>\n'
            + (('-' * 150) + '\n') * 2
        )
        logger.error(error_message)
        raise ValueError(error_message)
