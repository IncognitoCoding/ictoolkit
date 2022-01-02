"""
This module is designed to assist with html content.
"""
# Built-in/Generic Imports
import logging

# Libraries
from html.parser import HTMLParser
from os import linesep

# Own module
from ictoolkit.directors.validation_director import value_type_validation
from ictoolkit.directors.error_director import error_formatter
from ictoolkit.helpers.py_helper import get_function_name, get_line_number

__author__ = 'IncognitoCoding'
__copyright__ = 'Copyright 2021, html_director'
__credits__ = ['IncognitoCoding']
__license__ = 'GPL'
__version__ = '1.0'
__maintainer__ = 'IncognitoCoding'
__status__ = 'Development'


class HTMLConverter(HTMLParser):

    def __init__(self):
        HTMLParser.__init__(self)

    def feed(self, html_output: str, convert_option: str) -> str:
        logger = logging.getLogger(__name__)
        logger.debug(f'=' * 20 + get_function_name() + '=' * 20)
        # Custom flowchart tracking. This is ideal for large projects that move a lot.
        # For any third-party modules, set the flow before making the function call.
        logger_flowchart = logging.getLogger('flowchart')
        # Deletes the flowchart log if one already exists.
        logger_flowchart.debug(f'Flowchart --> Function: {get_function_name()}')
        # Checks function launch variables and logs passing parameters.
        try:
            # Validates required types.
            value_type_validation(html_output, str, __name__, get_line_number())
            value_type_validation(convert_option, str, __name__, get_line_number())

            logger.debug(
                'Passing parameters:\n'
                f'  - html_output (str):\n        - {str(html_output)}'
                f'  - convert_option (str):\n        - {convert_option}'
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

        if not any(convert_option == c for c in (None, 'text')):
            error_args = {
                'main_message': 'The HTML output could not be converted because the conversion option is not valid.',
                'error_type': ValueError,
                'expected_result': 'text',
                'returned_result': convert_option,
                'suggested_resolution': 'Please verify you have sent a valid conversion option.',
            }
            error_formatter(error_args, __name__, get_line_number())

        self.output = ""
        super(HTMLConverter, self).feed(html_output)
        # Supports text conversion, but other conversions such as PDF, image, etc can be added in the future.
        if convert_option == 'text':
            logging.debug('The HTML was converted to text. Returning the output.')
            # Removes all html before the last "}". Some HTML can return additional style information with text output.
            self.output = str(self.output).split('}')[-1].strip()
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
