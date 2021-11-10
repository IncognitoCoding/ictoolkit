#!interpreter

"""
This module is designed to assist with file-related actions.
"""
# Built-in/Generic Imports
import os
import sys
import logging
import pathlib
import traceback
from pathlib import Path

# Own modules
from ictoolkit.directors.dict_director import remove_duplicate_dict_values_in_list

__author__ = 'IncognitoCoding'
__copyright__ = 'Copyright 2021, file_director'
__credits__ = ['IncognitoCoding']
__license__ = 'GPL'
__version__ = '1.1'
__maintainer__ = 'IncognitoCoding'
__status__ = 'Development'


def write_file(file_path, write_value):
    """
    Writes a value to the file.

    Args:
        file_path (str): The file path being written into.
        write_value (str): The value being written into the file.

    Raises:
        ValueError: A failure occurred while writing the file
        ValueError: Writing file value <Value Being Written> to file <File Path Being Written> did not complete. The value does not exist after being written
    """
    logger = logging.getLogger(__name__)

    logger.debug(f'Begining to write the value to the file. write_value = {write_value}')
    try:
        logger.debug('Writing the value to the file')
        # Using "with" to take care of open and closing.
        with open(file_path, 'a+') as f:
            f.writelines(write_value + "\n")
    except Exception as err:
        error_message = (
            f'A failure occurred while writing the file.\n\n' +
            (('-' * 150) + '\n') + (('-' * 65) + 'Additional Information' + ('-' * 63) + '\n') + (('-' * 150) + '\n') +
            f'{err}\n\n'
            f'Originating error on line {traceback.extract_stack()[-1].lineno} in <{__name__}>\n' +
            (('-' * 150) + '\n') * 2
        )
        logger.error(error_message)
        raise ValueError(error_message)

    else:
        # Checking if the file entry written to the file.
        # Calling Example: search_file(<log file>, <search string>, <configured logger>)
        return_search = search_file(file_path, write_value)
        # Validates file entry wrote.
        if return_search is None:
            error_message = (
                f'Writing file value \"{write_value}\" to file \"{file_path}\" did not complete.\n' +
                (('-' * 150) + '\n') + (('-' * 65) + 'Additional Information' + ('-' * 63) + '\n') + (('-' * 150) + '\n') +
                'Expected Result:\n'
                '  - Return search value. != 2\n\n'
                'Returned Result:\n'
                f'  - No return search value was returned.\n\n'
                f'Originating error on line {traceback.extract_stack()[-1].lineno} in <{__name__}>\n' +
                (('-' * 150) + '\n') * 2
            )
            logger.error(error_message)
            raise ValueError(error_message)


def file_exist_check(file_path, file_description):
    """
    Validates the file exists.

    Args:
        file_path (str): The file path being checked.
        file_description (str): Name of the file being checked.

    Raises:
        ValueError: Log file does not exist.
    """
    logger = logging.getLogger(__name__)

    logger.debug(f'Begining to check the file path for {file_description}')
    # Checks if the file does not exist
    file = pathlib.Path(file_path)
    if not file.exists():
        error_message = (
            f'{file_description} log file does not exist.\n\n' +
            (('-' * 150) + '\n') + (('-' * 65) + 'Additional Information' + ('-' * 63) + '\n') + (('-' * 150) + '\n') +
            'Suggested Resolution:\n'
            '  - Ensure the file path is the correct path to your file.\n\n'
            f'Originating error on line {traceback.extract_stack()[-1].lineno} in <{__name__}>\n' +
            (('-' * 150) + '\n') * 2
        )
        logger.error(error_message)
        raise ValueError(error_message)
    else:
        logger.debug(f'{file_description} log file exists')


def search_file(file_path, searching_value, logger=None):
    """
    Searches the file for a value. The search can look for multiple values when the searching value arguments are passed as a list. A single-string search is supported as well.

    Args:
        file_path (str): the file path being checked
        searching_value (str or list): search value that is looked for within the file. The entry can be a single string or a list to search

    Raises:
        ValueError: A failure occurred while searching the file

    Returns:
        list: a dictionary in a list

        Usage Keys:
            - search_entry
            - found_entry

        Return Example: Return Example: [{'search_entry': '|Error|', 'found_entry': 'the entry found'}, {'search_entry': '|Warning|', 'found_entry': 'the entry found'}]
    """
    logger = logging.getLogger(__name__)

    logger.debug(f'Begining to search the file \"{file_path}\" for a value \"{searching_value}\"')
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

        # Checking if the listy has discovered values for potential cleanup.
        if matched_entries:
            # Checks if searching_value is str or list to clean up any potential duplicates
            if isinstance(searching_value, list):

                logger.debug(f'A list of all found search matches is listed below: {matched_entries}')
                logger.debug(f'Removing any duplicate entries that may have matched multiple times with similar search info')
                # Removes any duplicate matched values using the 2nd entry (1st element). This can happen if a search list has a similar search word that discovers the same line.
                # Example Return: [{'search_entry': '|Error|', 'found_entry': 'the entry found2'}]
                matched_entries = remove_duplicate_dict_values_in_list(matched_entries, 1)

                logger.debug(f'The adjusted match list with removed duplicates is listed below: {matched_entries}')
    except Exception as err:
        error_message = (
            f'A failure occurred while searching the file.\n\n' +
            (('-' * 150) + '\n') + (('-' * 65) + 'Additional Information' + ('-' * 63) + '\n') + (('-' * 150) + '\n') +
            f'{err}\n\n'
            f'Originating error on line {traceback.extract_stack()[-1].lineno} in <{__name__}>\n' +
            (('-' * 150) + '\n') * 2
        )
        logger.error(error_message)
        raise ValueError(error_message)
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


def search_multiple_files(file_paths, searching_value):
    """
    Searches multiple files for a value. Requires the file_path to be sent as a list. The search can look for multiple values when the searching value arguments are passed as a list.
    A single-string search is supported as well.

    Args:
        file_path (str): the file path being checked
        searching_value (str or list): search value that is looked for within the file. The entry can be a single string or a list to search

    Raises:
        ValueError: A failure occurred while searching the file

    Returns:
        list: A list of discovered search values. Each discovered value is per element. No discovered values will return None.

        Useage Keys:
            - search_entry
            - found_entry

        Return Example: Return Example: [{'search_entry': '|Error|', 'found_entry': 'the entry found'}, {'search_entry': '|Warning|', 'found_entry': 'the entry found'}]
    """
    logger = logging.getLogger(__name__)

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

        # Checking if the listy has discovered values for potential cleanup.
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
    except Exception as err:
        error_message = (
            f'A failure occurred while searching the file.\n\n' +
            (('-' * 150) + '\n') + (('-' * 65) + 'Additional Information' + ('-' * 63) + '\n') + (('-' * 150) + '\n') +
            f'{err}\n\n'
            f'Originating error on line {traceback.extract_stack()[-1].lineno} in <{__name__}>\n' +
            (('-' * 150) + '\n') * 2
        )
        logger.error(error_message)
        raise ValueError(error_message)
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


def check_file_threshold_size(file_path, size_max_file_size, logger=None):
    """
    Checks threshold on the log file. If the threshold is exceeded, the log file will be cleared.

    Args:
        file_path (str): the file path being checked
        size_max_file_size (int): the max size of the file being checked

    Raises:
        ValueError: Failure occured while clearing log file
        ValueError: Log file size is <File Size> bytes after clearing. Failed to clear log
        ValueError: <File Path> file does not exist., <General Error>
    """
    logger = logging.getLogger(__name__)

    logger.debug(f'Begining to check if the log file {file_path} has reached {size_max_file_size} bytes')
    # Checks if file exists before starting.
    # Log files may not exist on the initial start.
    file = pathlib.Path(file_path)
    if file.exists():
        # Gets log file size.
        size_file_path = os.path.getsize(file_path)
        # Checks if the log file is greater than the threshold.
        if size_file_path > size_max_file_size:
            logger.debug(f'Log file size is {size_file_path} bytes and over threashold of {size_max_file_size} bytes')
            logger.info('Clearing the log file because it is over the file size threshold')
            # Clears older entries in the log file.
            try:
                # Clears log file.
                f = open(file_path, "w")
                f.close()
            except Exception as err:
                error_message = (
                    f'Failure occured while clearing log file.\n\n' +
                    (('-' * 150) + '\n') + (('-' * 65) + 'Additional Information' + ('-' * 63) + '\n') + (('-' * 150) + '\n') +
                    f'{err}\n\n'
                    f'Originating error on line {traceback.extract_stack()[-1].lineno} in <{__name__}>\n' +
                    (('-' * 150) + '\n') * 2
                )
                logger.error(error_message)
                raise ValueError(error_message)

            # Gets log file size again.
            size_file_path = os.path.getsize(file_path)
            # Checks if log file cleared.
            if size_file_path > size_max_file_size:
                error_message = (
                    f'Log file size is {size_file_path} bytes after clearing. Failed to clear log.\n\n' +
                    (('-' * 150) + '\n') + (('-' * 65) + 'Additional Information' + ('-' * 63) + '\n') + (('-' * 150) + '\n') +
                    'Suggested Resolution:\n'
                    '  - Check permissions.\n\n'
                    f'Originating error on line {traceback.extract_stack()[-1].lineno} in <{__name__}>\n' +
                    (('-' * 150) + '\n') * 2
                )
                logger.error(error_message)
                raise ValueError(error_message)
            else:
                logger.info('Log file cleared successfully')
        else:
            logger.debug(f'Log file size is {size_file_path} bytes and under threshold of {size_max_file_size} bytes. No action required.')
    else:
        error_message = (
            f'{file_path} file does not exist.\n\n' +
            (('-' * 150) + '\n') + (('-' * 65) + 'Additional Information' + ('-' * 63) + '\n') + (('-' * 150) + '\n') +
            'Suggested Resolution:\n'
            '  - Ensure the file path is the correct path to your file.\n\n'
            f'Originating error on line {traceback.extract_stack()[-1].lineno} in <{__name__}>\n' +
            (('-' * 150) + '\n') * 2
        )
        logger.error(error_message)
        raise ValueError(error_message)


def convert_relative_to_full_path(relative_path: str) -> str:
    """ Determine full path to file given a relative file path with compatibility with PyInstaller(compiler) built-in

    Args:
        relative_path (string): The unqualified (relative) file path that needs to converted to a qualified full path format
            - Example: "\\[directory]\\[file].[extension]"

    Returns:
        [string]: Full file path
            - Example: "C:\\[root directory]\\[directory]\\[file].[extension]"
    """
    if hasattr(sys, '_MEIPASS'):
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    else:
        # When running uncompiled, use normal os calls to determine location
        base_path = os.getcwd()

    return f'{base_path}\\{relative_path}'


def user_file_selection(prompt: str, criteria: str, root_dir=None) -> str:
    """ Provides a simple user interface that numerically lists a set of files found using user submitted criteria.  User is prompted to submit the numeric value of the file that is to be used.

    Args:
        prompt (str): Literal prompt string to present to user\r
        \tExample: "Enter the database name to import"\n
        criteria (str): Filter to apply when searching for files. Expects standard OS search criteria
        \tExample: "*.db" or "*config*"\n
        root_dir (str): Manually sets the root directory to search.  Requires an absolute path format.\r
        \tExample: "C:\\Directory\\Subdirectory\"\n

    Raises:
        TypeError: prompt is not a string
        TypeError: criteria is not a string
        TypeError: root_dir is not a string
        FileNotFound: No files were found given the search criteria

    Returns:
        [string]: Returns the path of the file that was selected in the format provided\r
        \tExample: "test.py" or "c:\\folder\\test.py"

    """
    logger = logging.getLogger(__name__)
    logger.info(f'=' * 20 + traceback.extract_stack(None, 2)[1][2] + '=' * 20)
    # Custom flowchart tracking. This is ideal for large projects that move a lot.
    # For any third-party modules, set the flow before making the function call.
    logger_flowchart = logging.getLogger('flowchart')
    logger_flowchart.info(f'Flowchart --> Function: {traceback.extract_stack(None, 2)[1][2]}')

    logger.debug(f'Passing parameters [prompt] (str):\n    - {prompt}')
    logger.debug(f'Passing parameters [criteria] (str):\n    - {criteria}')
    logger.debug(f'Passing parameters [path_format] (str):\n    - {root_dir}')

    # Verify the provided criteria is in string format
    if not isinstance(prompt, str):
        error_message = (
            'The provided prompt is not in string format.\n' +
            (('-' * 150) + '\n') + (('-' * 65) + 'Additional Information' + ('-' * 63) + '\n') + (('-' * 150) + '\n') +
            'Expected Result:\n'
            f'  - Type = str\n\n'
            'Returned Result:\n'
            f'  - Type = {type(prompt)}\n\n'
            f'Originating error on line {traceback.extract_stack()[-1].lineno} in <{__name__}>\n' +
            (('-' * 150) + '\n') * 2
        )
        logger.error(error_message)
        raise TypeError(error_message)

    # Verify the provided criteria is in string format
    if not isinstance(criteria, str):
        error_message = (
            'The provided criteria is not in string format.\n' +
            (('-' * 150) + '\n') + (('-' * 65) + 'Additional Information' + ('-' * 63) + '\n') + (('-' * 150) + '\n') +
            'Expected Result:\n'
            f'  - Type = str\n\n'
            'Returned Result:\n'
            f'  - Type = {type(criteria)}\n\n'
            f'Originating error on line {traceback.extract_stack()[-1].lineno} in <{__name__}>\n' +
            (('-' * 150) + '\n') * 2
        )
        logger.error(error_message)
        raise TypeError(error_message)

    # Verify the provided path_format is in string format when not None
    if root_dir is not None and not isinstance(root_dir, str):
        error_message = (
            'The provided root_dir is not in string format.\n' +
            (('-' * 150) + '\n') + (('-' * 65) + 'Additional Information' + ('-' * 63) + '\n') + (('-' * 150) + '\n') +
            'Expected Result:\n'
            f'  - Type = str\n\n'
            'Returned Result:\n'
            f'  - Type = {type(root_dir)}\n\n'
            f'Originating error on line {traceback.extract_stack()[-1].lineno} in <{__name__}>\n' +
            (('-' * 150) + '\n') * 2
        )
        logger.error(error_message)
        raise TypeError(error_message)

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
        # User indicated that the required file was not in the list
        error_message = (
            'No files were found matching the required criteria\n' +
            (('-' * 150) + '\n') + (('-' * 65) + 'Additional Information' + ('-' * 63) + '\n') + (('-' * 150) + '\n') +
            f'Provided criteria: {criteria}\n'
            f'Directory: {search_path}\n'
            f'Originating error on line {traceback.extract_stack()[-1].lineno} in <{__name__}>\n' +
            (('-' * 150) + '\n') * 2
        )
        logger.debug(error_message)
        # Raise exception and let calling module determine how to handle
        raise FileNotFoundError(error_message)

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


print(user_file_selection("Get them DBs:", "*.db", "C:\\Cloud\\NextCloud\\Programming\\Python\\Scripts\\Team\\icsqltools\\icsqltools\\tests\\sql"))
