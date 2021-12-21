"""
This module is designed for validation checks. All modules will not return any data but throw exception errors when validation fails.
"""
# Built-in/Generic Imports
import traceback
import logging

__author__ = 'IncognitoCoding'
__copyright__ = 'Copyright 2021, validation_director'
__credits__ = ['IncognitoCoding']
__license__ = 'GPL'
__version__ = '1.0'
__maintainer__ = 'IncognitoCoding'
__status__ = 'Development'


def value_type_validation(value: any, required_type: type) -> None:
    """
    A simple type validation validation check.

    Args:
        value (any): Any value needing its type validated.
        required_type (type): The required type the value should match.

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

    # Verify the value matches the required type.
    if not isinstance(value, required_type):
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
