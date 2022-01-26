"""
This module is designed to assist with html content.
"""
# Built-in/Generic Imports
import logging

# Libraries
from html.parser import HTMLParser
from os import linesep
from fchecker import type_check

# Local Functions
from ..helpers.py_helper import get_function_name

# Exceptions
from fexception import FGeneralError, FTypeError, FValueError

__author__ = 'IncognitoCoding'
__copyright__ = 'Copyright 2022, html_director'
__credits__ = ['IncognitoCoding']
__license__ = 'MIT'
__version__ = '3.1'
__maintainer__ = 'IncognitoCoding'
__status__ = 'Production'


class HTMLConverter(HTMLParser):
    """
    Converts HTML to another format.
    """
    def __init__(self):
        """
        Converts HTML to another format.
        """
        HTMLParser.__init__(self)

    def feed(self, html_output: str, convert_option: str) -> str:
        """
        Main feed to convert HTML to text.

        Args:
            html_output (str):
            \t\\- HTML output requiring conversion.
            convert_option (str):
            \t\\- Conversion option.\\
            \t\\- Only 'text' is supported currently.

        Calling Example:
        \t\\- html_output = '<HTML as a string>'\\
        \t\\- convert_option = 'text

        Raises:
            FTypeError (fexception):
            \t\\- The value '{html_output}' is not in <class 'str'> format.
            FTypeError (fexception):
            \t\\- The value '{convert_option}' is not in <class 'str'> format.
            FValueError (fexception):
            \t\\- The HTML output could not be converted because the conversion option is not valid.
            FGeneralError (fexception):
            \t\\- A general failure occurred while converting HTML to text.

        Returns:
            str:
            \t\\- Converted HTML to text.
        """
        logger = logging.getLogger(__name__)
        logger.debug(f'=' * 20 + get_function_name() + '=' * 20)
        # Custom flowchart tracking. This is ideal for large projects that move a lot.
        # For any third-party modules, set the flow before making the function call.
        logger_flowchart = logging.getLogger('flowchart')
        # Deletes the flowchart log if one already exists.
        logger_flowchart.debug(f'Flowchart --> Function: {get_function_name()}')

        try:
            type_check(html_output, str)
            type_check(convert_option, str)
        except FTypeError:
            raise

        logger.debug(
            'Passing parameters:\n'
            f'  - html_output (str):\n        - {str(html_output)}\n'
            f'  - convert_option (str):\n        - {convert_option}\n'
        )

        if not any(convert_option == c for c in (None, 'text')):
            exc_args = {
                'main_message': 'The HTML output could not be converted because the conversion option is not valid.',
                'expected_result': 'text',
                'returned_result': convert_option,
                'suggested_resolution': 'Please verify you have sent a valid conversion option.',
            }
            raise FValueError(exc_args)

        try:
            self.output = ""
            super(HTMLConverter, self).feed(html_output)
            # Supports text conversion, but other conversions such as PDF, image, etc can be added in the future.
            if convert_option == 'text':
                logging.debug('The HTML was converted to text. Returning the output.')
                # Removes all html before the last "}". Some HTML can return additional style information with text output.
                self.output = str(self.output).split('}')[-1].strip()
        except Exception as exc:
            exc_args = {
                'main_message': 'A general failure occurred while converting HTML to text.',
                'original_exception': exc,
            }
            raise FGeneralError(exc_args)
        else:
            return self.output

    def handle_data(self, data: str):
        logger = logging.getLogger(__name__)
        logger.debug(f'=' * 20 + get_function_name() + '=' * 20)
        # Custom flowchart tracking. This is ideal for large projects that move a lot.
        # For any third-party modules, set the flow before making the function call.
        logger_flowchart = logging.getLogger('flowchart')
        # Deletes the flowchart log if one already exists.
        logger_flowchart.debug(f'Flowchart --> Function: {get_function_name()}')
        logging.debug('Setting the HTML output to a variable')
        self.output += data.strip()

    def handle_starttag(self, tag: str, attrs: list):
        logger = logging.getLogger(__name__)
        logger.debug(f'=' * 20 + get_function_name() + '=' * 20)
        # Custom flowchart tracking. This is ideal for large projects that move a lot.
        # For any third-party modules, set the flow before making the function call.
        logger_flowchart = logging.getLogger('flowchart')
        # Deletes the flowchart log if one already exists.
        logger_flowchart.debug(f'Flowchart --> Function: {get_function_name()}')
        logging.debug(f'Converting the start HTML text information:\n        - {tag}\n        - {attrs}')
        if tag == 'li':
            self.output += linesep + '- '
        elif tag == 'blockquote':
            self.output += linesep + linesep + '\t'
        elif tag in ['br', 'p', 'h1', 'h2', 'h3', 'h4', 'tr', 'th']:
            self.output += linesep + '\n'

    def handle_endtag(self, tag: str):
        logger = logging.getLogger(__name__)
        logger.debug(f'=' * 20 + get_function_name() + '=' * 20)
        # Custom flowchart tracking. This is ideal for large projects that move a lot.
        # For any third-party modules, set the flow before making the function call.
        logger_flowchart = logging.getLogger('flowchart')
        # Deletes the flowchart log if one already exists.
        logger_flowchart.debug(f'Flowchart --> Function: {get_function_name()}')
        logging.debug(f'Converting the end HTML text information:\n        - {tag}')
        if tag == 'blockquote':
            self.output += linesep + linesep
