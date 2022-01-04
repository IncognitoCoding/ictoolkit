#!interpreter

"""
This module is designed to assist with file-related actions.
"""
# Built-in/Generic Imports
import os
import sys
import logging
import pathlib
from pathlib import Path
from typing import Optional, Union

# Own modules
from ictoolkit.directors.data_structure_director import remove_duplicate_dict_values_in_list
from ictoolkit.directors.validation_director import value_type_validation
from ictoolkit.directors.error_director import error_formatter
from ictoolkit.helpers.py_helper import get_function_name, get_line_number

__author__ = 'IncognitoCoding'
__copyright__ = 'Copyright 2022, file_director'
__credits__ = ['IncognitoCoding']
__license__ = 'GPL'
__version__ = '2.0'
__maintainer__ = 'IncognitoCoding'
__status__ = 'Production'


def write_file(file_path: str, write_value: str) -> None:
    """
    Writes a value to the file.

    Args:
        file_path (str): The file path being written into.
        write_value (str): The value being written into the file.

    Raises:
        TypeError: The value '{file_path}' is not in str format.
        TypeError: The value '{write_value}' is not in str format.
        Exception: Forwarding caught {type(error).__name__} at line {error.__traceback__.tb_lineno} in <{__name__}>
        Exception: A general exception occurred during the value type validation.
        Exception: Forwarding caught {type(error).__name__} at line {error.__traceback__.tb_lineno} in <{__name__}>
        Exception: A general failure occurred while writing the file.
        ValueError: Writing file value '{write_value}' to file '{file_path}' did not complete.
    """
    logger = logging.getLogger(__name__)
    logger.debug(f'=' * 20 + get_function_name() + '=' * 20)
    # Custom flowchart tracking. This is ideal for large projects that move a lot.
    # For any third-party modules, set the flow before making the function call.
    logger_flowchart = logging.getLogger('flowchart')
    logger_flowchart.debug(f'Flowchart --> Function: {get_function_name()}')

    # Checks function launch variables and logs passing parameters.
    try:
        # Validates required types.
        value_type_validation(file_path, str, __name__, get_line_number())
        value_type_validation(write_value, str, __name__, get_line_number())

        logger.debug(
            'Passing parameters:\n'
            f'  - file_path (str):\n        - {file_path}\n'
            f'  - write_value (str):\n        - {write_value}\n'
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

    try:
        logger.debug(f'Begining to write the value to the file. write_value = {write_value}')
        logger.debug('Writing the value to the file')
        # Using "with" to take care of open and closing.
        with open(file_path, 'a+') as f:
            f.writelines(write_value + "\n")
    except Exception as error:
        if 'Originating error on line' in str(error):
            logger.debug(f'Forwarding caught {type(error).__name__} at line {error.__traceback__.tb_lineno} in <{__name__}>')
            raise error
        else:
            error_args = {
                'main_message': 'A general failure occurred while writing the file.',
                'error_type': Exception,
                'original_error': error,
            }
            error_formatter(error_args, __name__, error.__traceback__.tb_lineno)
    else:
        # Checking if the file entry written to the file.
        # Calling Example: search_file(<log file>, <search string>, <configured logger>)
        return_search = search_file(file_path, write_value)
        # Validates file entry wrote.
        if return_search is None:
            error_args = {
                'main_message': f'Writing file value \'{write_value}\' to file \'{file_path}\' did not complete.',
                'error_type': ValueError,
                'expected_result': 2,
                'returned_result': ' No return search value was returned.',
            }
            error_formatter(error_args, __name__, get_line_number())


def file_exist_check(file_path: str, file_description: str) -> None:
    """
    Validates the file exists. An error will throw if the file does not exist.

    Args:
        file_path (str): The file path being checked.
        file_description (str): Name of the file being checked.

    Raises:
        TypeError: The value '{file_path}' is not in str format.
        TypeError: The value '{file_description}' is not in str format.
        Exception: Forwarding caught {type(error).__name__} at line {error.__traceback__.tb_lineno} in <{__name__}>
        Exception: A general exception occurred during the value type validation.
        FileNotFoundError: {file_description} log file does not exist.
        Exception: Forwarding caught {type(error).__name__} at line {error.__traceback__.tb_lineno} in <{__name__}>
        Exception: A general failure occurred while checking if the file exists.
    """
    logger = logging.getLogger(__name__)
    logger.debug(f'=' * 20 + get_function_name() + '=' * 20)
    # Custom flowchart tracking. This is ideal for large projects that move a lot.
    # For any third-party modules, set the flow before making the function call.
    logger_flowchart = logging.getLogger('flowchart')
    logger_flowchart.debug(f'Flowchart --> Function: {get_function_name()}')

    # Checks function launch variables and logs passing parameters.
    try:
        # Validates required types.
        value_type_validation(file_path, str, __name__, get_line_number())
        value_type_validation(file_description, str, __name__, get_line_number())

        logger.debug(
            'Passing parameters:\n'
            f'  - file_path (str):\n        - {file_path}\n'
            f'  - file_description (str):\n        - {file_description}\n'
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

    try:
        logger.debug(f'Begining to check the file path for {file_description}')
        # Checks if the file does not exist
        file = pathlib.Path(file_path)
        if not file.exists():
            error_args = {
                'main_message': f'{file_description} log file does not exist.',
                'error_type': FileNotFoundError,
                'suggested_resolution': 'Ensure the file path is the correct path to your file.',
            }
            error_formatter(error_args, __name__, get_line_number())
        else:
            logger.debug(f'{file_description} file exists')
    except Exception as error:
        if 'Originating error on line' in str(error):
            logger.debug(f'Forwarding caught {type(error).__name__} at line {error.__traceback__.tb_lineno} in <{__name__}>')
            raise error
        else:
            error_args = {
                'main_message': 'A general failure occurred while checking if the file exists.',
                'error_type': Exception,
                'original_error': error,
            }
            error_formatter(error_args, __name__, error.__traceback__.tb_lineno)


def search_file(file_path: str, searching_value: Union[str, list]) -> Union[list, None]:
    """
    Searches the file for a value. The search can look for multiple values when the searching value arguments are passed as a list. A single-string search is supported as well.

    Args:
        file_path (str): the file path being checked
        searching_value (str or list): search value that is looked for within the file. The entry can be a single string or a list to search

    Raises:
        TypeError: The value '{file_path}' is not in str format.
        TypeError: The value '{searching_value}' is not in str or list format.
        Exception: Forwarding caught {type(error).__name__} at line {error.__traceback__.tb_lineno} in <{__name__}>
        Exception: A general exception occurred during the value type validation.
        ValueError: A failure occurred while searching the file. The file path does not include a file with an extension.
        Exception: Forwarding caught {type(error).__name__} at line {error.__traceback__.tb_lineno} in <{__name__}>
        Exception: A general failure occurred while while searching the file.

    Returns:
        list: a dictionary in a list
        \tExample: [{'search_entry': '|Error|', 'found_entry': 'the entry found'}, {'search_entry': '|Warning|', 'found_entry': 'the entry found'}]

        Usage Keys:
            - search_entry
            - found_entry
    """
    logger = logging.getLogger(__name__)
    logger.debug(f'=' * 20 + get_function_name() + '=' * 20)
    # Custom flowchart tracking. This is ideal for large projects that move a lot.
    # For any third-party modules, set the flow before making the function call.
    logger_flowchart = logging.getLogger('flowchart')
    logger_flowchart.debug(f'Flowchart --> Function: {get_function_name()}')

    # Checks function launch variables and logs passing parameters.
    try:
        # Validates required types.
        value_type_validation(file_path, str, __name__, get_line_number())
        value_type_validation(searching_value, [str, list], __name__, get_line_number())

        if isinstance(searching_value, list):
            formatted_searching_value = '  - searching_value (list):' + str('\n        - ' + '\n        - '.join(map(str, searching_value)))
        elif isinstance(searching_value, str):
            formatted_searching_value = f'  - searching_value (str):\n        - {searching_value}'

        logger.debug(
            'Passing parameters:\n'
            f'  - file_path (str):\n        - {file_path}\n'
            f'{formatted_searching_value}\n'
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

    logger.debug(f'Begining to search the file \"{file_path}\" for a value \"{searching_value}\"')

    # Checks that the passing file_path contains a file extension.
    if '.' not in file_path:
        error_args = {
            'main_message': 'A failure occurred while searching the file. The file path does not include a file with an extension.',
            'error_type': ValueError,
            'expected_result': 'A file with an extension (ex: myfile.txt)',
            'returned_result': file_path,
            'suggested_resolution': 'Please verify you have sent a full file path and not a directory.',
        }
        error_formatter(error_args, __name__, get_line_number())

    try:
        # Stores the search entry and found info.
        # Required to return multiple found strings.
        matched_entries = []

        logger.debug('Reading in all lines from the file')
        # Using "with" to take care of open and closing.
        with open(file_path, 'r') as f:
            lines = f.readlines()
        logger.debug('Looping through all lines from the file 1 by 1')
        # Looping through all lines from the log file 1 by 1.
        for line in lines:
            # Strips off the '\n' character.
            stripped_line = (line.strip())
            # Checks if searching_value is a str or list
            if isinstance(searching_value, str):
                # Checks if a value exists as each line is read.
                if searching_value in stripped_line:
                    logger.debug(f'Searched file value \"{searching_value}\" found. Adding file value to the returning list \"matched_entries\"')
                    # Adds found line and search value to list
                    matched_entries.append({'search_entry': searching_value, 'found_entry': stripped_line})
            elif isinstance(searching_value, list):
                # Loops through each search value
                for search_value in searching_value:
                    # Checks if a value exists as each line is read.
                    if search_value in stripped_line:
                        logger.debug(f'Searched file value \"{search_value}\" from value list \"{searching_value}\" found. Adding file value \"{stripped_line}\" to the returning list \"matched_entries\"')
                        # Adds found line and search value to list
                        matched_entries.append({'search_entry': searching_value, 'found_entry': stripped_line})

            logger.debug('Checking if the list \"matched_entries\" has matched values')

        # Checking if the list has discovered values for potential cleanup.
        if matched_entries:
            # Checks if searching_value is str or list to clean up any potential duplicates
            if isinstance(searching_value, list):

                logger.debug(f'A list of all found search matches is listed below: {matched_entries}')
                logger.debug(f'Removing any duplicate entries that may have matched multiple times with similar search info')
                # Removes any duplicate matched values using the 2nd entry (1st element). This can happen if a search list has a similar search word that discovers the same line.
                # Example Return: [{'search_entry': '|Error|', 'found_entry': 'the entry found2'}]
                matched_entries = remove_duplicate_dict_values_in_list(matched_entries, 1)

                logger.debug(f'The adjusted match list with removed duplicates is listed below: {matched_entries}')
    except Exception as error:
        if 'Originating error on line' in str(error):
            logger.debug(f'Forwarding caught {type(error).__name__} at line {error.__traceback__.tb_lineno} in <{__name__}>')
            raise error
        else:
            error_args = {
                'main_message': 'A general failure occurred while while searching the file.',
                'error_type': Exception,
                'original_error': error,
            }
            error_formatter(error_args, __name__, error.__traceback__.tb_lineno)
    else:
        # Checking if the list has discovered log entry values.
        if matched_entries:
            logger.debug('Returning found values')
            # Returns found lines(s).
            return matched_entries
        elif not matched_entries:
            logger.debug('No searched value has have been found')
            logger.debug('Returning None')
            # Returns "None" because no strings found.
            return None


def search_multiple_files(file_paths: list, searching_value: Union[str, list]) -> Union[list, None]:
    """
    Searches multiple files for a value. Requires the file_path to be sent as a list. The search can look for multiple values when the searching value arguments are passed as a list.
    A single-string search is supported as well.

    Args:
        file_paths (list): a list of file path being checked
        searching_value (str or list): search value that is looked for within the file. The entry can be a single string or a list to search

    Raises:
        TypeError: The value '{file_paths}' is not in list format.
        TypeError: The value '{searching_value}' is not in str or list format.
        Exception: Forwarding caught {type(error).__name__} at line {error.__traceback__.tb_lineno} in <{__name__}>
        Exception: A general exception occurred during the value type validation.
        ValueError: A failure occurred while searching the file. The file path does not include a file with an extension.
        Exception: Forwarding caught {type(error).__name__} at line {error.__traceback__.tb_lineno} in <{__name__}>
        Exception: A general failure occurred while while searching the file

    Returns:
        list: A list of discovered search values. Each discovered value is per element. No discovered values will return None.
        \tExample: [{'search_entry': '|Error|', 'found_entry': 'the entry found'}, {'search_entry': '|Warning|', 'found_entry': 'the entry found'}]
        Useage Keys:
            - search_entry
            - found_entry
    """
    logger = logging.getLogger(__name__)
    logger.debug(f'=' * 20 + get_function_name() + '=' * 20)
    # Custom flowchart tracking. This is ideal for large projects that move a lot.
    # For any third-party modules, set the flow before making the function call.
    logger_flowchart = logging.getLogger('flowchart')
    logger_flowchart.debug(f'Flowchart --> Function: {get_function_name()}')

    # Checks function launch variables and logs passing parameters.
    try:
        # Validates required types.
        value_type_validation(file_paths, list, __name__, get_line_number())
        value_type_validation(searching_value, [str, list], __name__, get_line_number())

        formatted_file_paths = '  - file_paths (list):' + str('\n        - ' + '\n        - '.join(map(str, file_paths)))
        if isinstance(searching_value, list):
            formatted_searching_value = '  - searching_value (list):' + str('\n        - ' + '\n        - '.join(map(str, searching_value)))
        elif isinstance(searching_value, str):
            formatted_searching_value = f'  - searching_value (str):\n        - {searching_value}'

        logger.debug(
            'Passing parameters:\n'
            f'{formatted_file_paths}\n'
            f'{formatted_searching_value}\n'
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

    logger.debug(f'Begining to search the files \"{file_paths}\" for a value \"{searching_value}\"')

    try:
        # Assigns list variable to be used in this function.
        # Required to return multiple found strings.
        grouped_found_files = []
        matched_entries = []

        # Sets count on total files being searched.
        total_files = len(file_paths)
        logger.debug('Starting to loop through file(s)')
        # Loops through each file path to add all lines into a single list.
        for index, file_path in enumerate(file_paths):
            # Checks that the passing file_path contains a file extension.
            if '.' not in file_path:
                error_args = {
                    'main_message': 'A failure occurred while searching the file. The file path does not include a file with an extension.',
                    'error_type': ValueError,
                    'expected_result': 'A file with an extension (ex: myfile.txt)',
                    'returned_result': file_path,
                    'suggested_resolution': 'Please verify you have sent a full file path and not a directory.',
                }
                error_formatter(error_args, __name__, get_line_number())
            logger.debug(f'Reading in all lines from the file \"{file_path}\"')
            # Sets the basename for cleaner logging output.
            basename_searched_file = os.path.basename(file_path)
            logger.debug(f'Looping through file \"{basename_searched_file}\" {index + 1} of {total_files}')

            # Using "with" to take care of open and closing.
            with open(file_path, 'r') as f:
                readLines = f.readlines()
                # Loops through each line.
                for line in readLines:
                    # Adds line to list.
                    grouped_found_files.append(line)

            logger.debug('Looping through all lines from the files 1 by 1')

        # Looping through all lines from the log file 1 by 1.
        for line in grouped_found_files:
            # Strips off the '\n' character.
            stripped_line = (line.strip())
            # Checks if searching_value is a str or list
            if isinstance(searching_value, str):
                # Checks if a value exists as each line is read.
                if searching_value in stripped_line:
                    logger.debug(f'Searched file value \"{searching_value}\" found. Adding file value to the returning list \"matched_entries\"')
                    # Adds found line and search value to list
                    matched_entries.append({'search_entry': searching_value, 'found_entry': stripped_line})
            elif isinstance(searching_value, list):
                # Loops through each search value
                for search_value in searching_value:
                    # Checks if a value exists as each line is read.
                    if search_value in stripped_line:
                        logger.debug(f'Searched file value \"{search_value}\" from value list \"{searching_value}\" found. Adding file value \"{stripped_line}\" to the returning list \"matched_entries\"')

                        # Adds found line and search value to list
                        matched_entries.append({'search_entry': searching_value, 'found_entry': stripped_line})

            logger.debug('Checking if the list has discovered file entry values')

        # Checking if the list has discovered values for potential cleanup.
        if matched_entries:
            # Checks if searching_value is str or list to clean up any potential duplicates
            if isinstance(searching_value, str):
                logger.debug('Searched file value has been found')
            elif isinstance(searching_value, list):
                logger.debug('Searched file values have been found')
                logger.debug(f'A list of all found search matches is listed below: {matched_entries}')
                logger.debug(f'Removing any duplicate entries that may have matched multiple times with similar search info')
                # Removes any duplicate matched values using the 2nd entry (1st element). This can happen if a search list has a similar search word that discovers the same line.
                # Example Return: [{'search_entry': '|Error|', 'found_entry': 'the entry found2'}]
                matched_entries = remove_duplicate_dict_values_in_list(matched_entries, 1)
                logger.debug(f'The adjusted match list with removed duplicates is listed below: {matched_entries}')
    except Exception as error:
        if 'Originating error on line' in str(error):
            logger.debug(f'Forwarding caught {type(error).__name__} at line {error.__traceback__.tb_lineno} in <{__name__}>')
            raise error
        else:
            error_args = {
                'main_message': 'A general failure occurred while while searching the file.',
                'error_type': Exception,
                'original_error': error,
            }
            error_formatter(error_args, __name__, error.__traceback__.tb_lineno)
    else:
        # Checking if the list has discovered log entry values.
        if matched_entries:
            logger.debug('Returning found values')
            # Returns found lines(s).
            return matched_entries
        elif not matched_entries:
            logger.debug('No searched value has have been found')
            logger.debug('Returning None')
            # Returns "None" because no strings found.
            return None


def convert_relative_to_full_path(relative_path: str) -> str:
    """
    Determine full path to file given a relative file path with compatibility with PyInstaller(compiler) built-in

    Args:
        relative_path (string): The unqualified (relative) file path that needs to converted to a qualified full path format
        \t\- Example: "\\[directory]\\[file].[extension]"

    Raises:
        TypeError: The value '{relative_path}' is not in str format.
        Exception: Forwarding caught {type(error).__name__} at line {error.__traceback__.tb_lineno} in <{__name__}>
        Exception: A general exception occurred during the value type validation.
        Exception: Forwarding caught {type(error).__name__} at line {error.__traceback__.tb_lineno} in <{__name__}>
        Exception: A general exception occurred during the relative to full path conversion.

    Returns:
        [string]: Full file path
        \t\- Example: "C:\\[root directory]\\[directory]\\[file].[extension]"
    """
    logger = logging.getLogger(__name__)
    logger.debug(f'=' * 20 + get_function_name() + '=' * 20)
    # Custom flowchart tracking. This is ideal for large projects that move a lot.
    # For any third-party modules, set the flow before making the function call.
    logger_flowchart = logging.getLogger('flowchart')
    logger_flowchart.debug(f'Flowchart --> Function: {get_function_name()}')

    # Checks function launch variables and logs passing parameters.
    try:
        # Validates required types.
        value_type_validation(relative_path, str, __name__, get_line_number())

        logger.debug(
            'Passing parameters:\n'
            f'  - relative_path(str):\n        - {relative_path}\n'
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

    try:
        if hasattr(sys, '_MEIPASS'):
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
        else:
            # When running un-compiled, use normal os calls to determine location
            base_path = os.getcwd()

        return f'{base_path}\\{relative_path}'
    except Exception as error:
        if 'Originating error on line' in str(error):
            logger.debug(f'Forwarding caught {type(error).__name__} at line {error.__traceback__.tb_lineno} in <{__name__}>')
            raise error
        else:
            error_args = {
                'main_message': 'A general exception occurred during the relative to full path conversion.',
                'error_type': Exception,
                'original_error': error,
            }
            error_formatter(error_args, __name__, error.__traceback__.tb_lineno)


def user_file_selection(prompt: str, criteria: str, root_dir: Optional[str] = None) -> str:
    """
    Provides a simple user interface that numerically lists a set of files found using user submitted criteria.  User is prompted to submit the numeric value of the file that is to be used.

    Args:
        prompt (str): Literal prompt string to present to user\r
        \tExample: "Enter the database name to import"\n
        criteria (str): Filter to apply when searching for files. Expects standard OS search criteria
        \tExample: "*.db" or "*config*"\n
        root_dir (str, optional): Manually sets the root directory to search.  Requires an absolute path format. Defaults to None.\r
        \tExample: "C:\\Directory\\Subdirectory\"\n

    Raises:
        TypeError: The value '{prompt}' is not in str format.
        TypeError: The value '{criteria}' is not in str format.
        TypeError: The value '{root_dir}' is not in str format.
        Exception: Forwarding caught {type(error).__name__} at line {error.__traceback__.tb_lineno} in <{__name__}>
        Exception: A general exception occurred during the value type validation.
        FileNotFoundError: No files were found matching the required criteria
        Exception: Forwarding caught {type(error).__name__} at line {error.__traceback__.tb_lineno} in <{__name__}>
        Exception: A general failure occurred during the user file selection.

    Returns:
        [string]: Returns the path of the file that was selected in the format provided\r
        \tExample: "test.py" or "c:\\folder\\test.py"
    """
    logger = logging.getLogger(__name__)
    logger.debug(f'=' * 20 + get_function_name() + '=' * 20)
    # Custom flowchart tracking. This is ideal for large projects that move a lot.
    # For any third-party modules, set the flow before making the function call.
    logger_flowchart = logging.getLogger('flowchart')
    logger_flowchart.debug(f'Flowchart --> Function: {get_function_name()}')

    # Checks function launch variables and logs passing parameters.
    try:
        # Validates required types.
        value_type_validation(prompt, str, __name__, get_line_number())
        value_type_validation(criteria, str, __name__, get_line_number())
        if root_dir:
            value_type_validation(root_dir, str, __name__, get_line_number())

        if root_dir:
            formatted_root_dir = f'  - relative_path (str):\n        - {root_dir}'
        else:
            formatted_root_dir = f'  - relative_path (str):\n        - None'

        logger.debug(
            'Passing parameters:\n'
            f'  - prompt (str):\n        - {prompt}\n'
            f'  - criteria (str):\n        - {criteria}\n'
            f'{formatted_root_dir}\n'
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

    try:
        # Initialize an empty list that will contain files found during search
        files = []
        # Print the prompt
        print(prompt)
        """
        # Search for files in current working directory
        for file in glob(criteria):
            # Do not match on temporary files beginning with '~'
            if search('^~', file) is None:
                # Add file to list
                files.append(file)
                print(f'  [{[i for i, x in enumerate(files) if x == file][0]}] {file}')
        """
        if root_dir:
            # Use provided root directory for search
            search_path = root_dir
        else:
            # If path not provided, use current working directory
            search_path = os.path.abspath(os.curdir)

        for file in Path(search_path).glob(criteria):
            # Add file to list
            files.append(file)
            print(f'  [{[i for i, x in enumerate(files) if x == file][0]}] {os.path.basename(file)}')

        # If no files were found matching user provided criteria,  raise exception
        if len(files) == 0:
            error_args = {
                'main_message': 'No files were found matching the required criteria',
                'error_type': FileNotFoundError,
                'expected_result': 'A matching file',
                'returned_result': 0,
                'suggested_resolution': 'Please verify you have set all required keys and try again.',
            }
            error_formatter(error_args, __name__, get_line_number())

        # Loop until valid input is provided by user
        while True:
            try:
                selection = int(input('\nSelection [#]:  '))
            except ValueError:
                print("Invalid entry")
                logger.debug("User entered non-numeric input")
                continue
            # Check user input for basic validity
            if selection < 0:
                # User is being a dick and submitted a negative number, re-prompt
                print("Invalid entry")
                logger.debug("User entered negative number input")
                continue
            elif selection not in range(len(files)):
                # Number input is greater than max selectable value, re-prompt
                print("Invalid entry")
                logger.debug("User entered number greater than returned file count")
                continue
            else:
                # Valid input provided, return absolute path of file selected
                return files[selection]
    except Exception as error:
        if 'Originating error on line' in str(error):
            logger.debug(f'Forwarding caught {type(error).__name__} at line {error.__traceback__.tb_lineno} in <{__name__}>')
            raise error
        else:
            error_args = {
                'main_message': 'A general failure occurred during the user file selection.',
                'error_type': Exception,
                'original_error': error,
            }
            error_formatter(error_args, __name__, error.__traceback__.tb_lineno)
