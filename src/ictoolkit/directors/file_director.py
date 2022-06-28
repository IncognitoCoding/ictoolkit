"""
This module is designed to assist with file-related actions.
"""
# Built-in/Generic Imports
import os
import sys
import logging
from pathlib import Path
from typing import Any, Union, Optional, Dict

# Libraries
from fchecker.type import type_check
from fchecker.file import file_check

# Local Functions
from ..data_structure.list import remove_duplicate_dict_values_in_list
from ..helpers.py_helper import get_function_name

# Exceptions
from fexception import FCustomException, FFileNotFoundError

__author__ = "IncognitoCoding"
__copyright__ = "Copyright 2022, file_director"
__credits__ = ["IncognitoCoding"]
__license__ = "MIT"
__version__ = "3.7"
__maintainer__ = "IncognitoCoding"
__status__ = "Production"


class FileWriteFailure(Exception):
    """Exception raised for file write failures."""

    __module__ = "builtins"
    pass


class FileSearchFailure(Exception):
    """Exception raised for file search failures."""

    __module__ = "builtins"
    pass


def write_file(file_path: str, write_value: str) -> None:
    """
    Writes a value to the file.

    Write validation is performed after the write. Supports writes with
    new lines (\\n).

    Args:
        file_path (str):
        \t\\- The file path being written into.
        write_value (str):
        \t\\- The value being written into the file.

    Raises:
        FTypeError (fexception):
        \t\\- The object value '{file_path}' is not an instance of the required class(es) or subclass(es).
        FTypeError (fexception):
        \t\\- The object value '{write_value}' is not an instance of the required class(es) or subclass(es).
        FileWriteFailure:
        \t\\- The file failed to write.
        FFileNotFoundError (fexception):
        \t\\- The file does not exist in the validating file path ({file_path}).
        FileWriteFailure:
        \t\\- Writing file value ({write_value}) to file ({file_path}) did not complete.
    """
    logger = logging.getLogger(__name__)
    logger.debug(f"=" * 20 + get_function_name() + "=" * 20)
    # Custom flowchart tracking. This is ideal for large projects that move a lot.
    # For any third-party modules, set the flow before making the function call.
    logger_flowchart = logging.getLogger("flowchart")
    logger_flowchart.debug(f"Flowchart --> Function: {get_function_name()}")

    type_check(value=file_path, required_type=str, tb_remove_name="write_file")
    type_check(value=write_value, required_type=str, tb_remove_name="write_file")

    logger.debug(
        "Passing parameters:\n"
        f"  - file_path (str):\n        - {file_path}\n"
        f"  - write_value (str):\n        - {write_value}\n"
    )

    try:
        logger.debug(f"Begining to write the value to the file. write_value = {write_value}")
        logger.debug("Writing the value to the file")
        # Using "with" to take care of open and closing.
        with open(file_path, "a") as f:
            if "\n" in write_value:
                f.writelines(write_value + "\n")
            else:
                f.write(write_value + "\n")
    except Exception as exc:  # pragma: no cover
        exc_args = {
            "main_message": "The file failed to write.",
            "custom_type": FileWriteFailure,
            "original_exception": exc,
        }
        raise FileWriteFailure(FCustomException(message_args=exc_args, tb_remove_name="write_file"))
    else:
        try:
            return_search: Union[list[Any], None] = None
            # Checks if a file that was written had new lines, so each line can get checked
            # individually.
            if "\n" in write_value:
                split_new_line_write_value = write_value.split("\n")
                for line in split_new_line_write_value:
                    return_search = search_file(file_path, line)
                    if not return_search:
                        break
            else:
                # Checking if the file entry is written to the file.
                # Calling Example: search_file(<log file>, <search string>, <configured logger>)
                return_search = search_file(file_path, write_value)
        except FFileNotFoundError:
            raise
        else:
            # Validates file entry wrote.
            if return_search is None:
                exc_args = {
                    "main_message": f"Writing file value ({write_value}) to file ({file_path}) did not complete.",
                    "custom_type": FileWriteFailure,
                    "returned_result": " No return search value were returned.",
                }
                raise FileWriteFailure(FCustomException(message_args=exc_args, tb_remove_name="write_file"))


def search_file(
    file_path: Union[str, list[str]],
    searching_value: Union[str, list[Union[str, int]]],
    include_next_line_value: Optional[Union[str, list[Union[str, int]]]] = None,
) -> Union[list[Any], None]:
    """
    Searches single or multiple files for a value.

    The search can look for multiple values when the searching value arguments are passed as a list.

    A single-string search is supported as well.

    Args:
        file_path (Union[str, list[str]]):
        \t\\- A list of file path being checked.
        searching_value (Union[str, list[Union[str, int]]]):
        \t\\- search value that is looked for within the file.\\
        \t\\- The entry can be a single string or a list to search\\
        include_next_line_value (Union[str, list[Union[str, int]]], optional):
        \t\\- Includes any next line containing a character or characters that match.\\
        \t\\- Ideal when logs add new line information and the output needs returned.\\
        \t\\- The next line value check can be a single string or a list to search.

    Raises:
        FTypeError (fexception):
        \t\\- The object value '{file_path}' is not an instance of the required class(es) or subclass(es).
        FTypeError (fexception):
        \t\\- The object value '{searching_value}' is not an instance of the required class(es) or subclass(es).
        FFileNotFoundError (fexception):
        \t\\- The file does not exist in the validating file path ({file_path}).
        FileSearchFailure (fexception):
        \t\\- A failure occurred while searching the file. The file path does not include a file with an extension.

    Returns:
        Union[list, None]:
        \t\\- list:\\
        \t\t\\- A list of discovered search values.
        \t\t\\- Each discovered value is per element.
        \t\\- None:\\
        \t\t\\- No discovered values will return None.

    Return Examples:
    \t\\- [{'search_entry': '|Error|', 'found_entry': 'the entry found'},
    \t   {'search_entry': '|Warning|', 'found_entry': 'the entry found'}]

    Return Usage Keys:
    \t\\- search_entry\\
    \t\\- found_entry
    """
    logger = logging.getLogger(__name__)
    logger.debug(f"=" * 20 + get_function_name() + "=" * 20)
    # Custom flowchart tracking. This is ideal for large projects that move a lot.
    # For any third-party modules, set the flow before making the function call.
    logger_flowchart = logging.getLogger("flowchart")
    logger_flowchart.debug(f"Flowchart --> Function: {get_function_name()}")

    type_check(value=file_path, required_type=(str, list), tb_remove_name="search_file")
    type_check(value=searching_value, required_type=(str, list), tb_remove_name="search_file")

    if isinstance(file_path, list):
        formatted_file_path = "  - file_path (list):" + str("\n        - " + "\n        - ".join(map(str, file_path)))
    elif isinstance(file_path, str):
        formatted_file_path = f"  - file_path (str):\n        - {file_path}"
    if isinstance(searching_value, list):
        formatted_searching_value = "  - searching_value (list):" + str(
            "\n        - " + "\n        - ".join(map(str, searching_value))
        )
    elif isinstance(searching_value, str):
        formatted_searching_value = f"  - searching_value (str):\n        - {searching_value}"
    logger.debug("Passing parameters:\n" f"{formatted_file_path}\n" f"{formatted_searching_value}\n")

    # Assigns list variable to be used in this function.
    # Required to return multiple found strings.
    matched_entries: list[dict[str, Union[str, list[Union[str, int]]]]] = []
    grouped_found_file_lines: list[str] = []

    if isinstance(file_path, list):
        # Sets count on total files being searched.
        total_files = len(file_path)
        logger.debug("Starting to loop through file(s)")
        logger.debug(f'Begining to search the files "{file_path}" for a value "{searching_value}"')
        # Loops through each file path to add all lines into a single list.
        for index, file_path in enumerate(file_path):
            # Checks that the passing file_path contains a file extension.
            if "." not in file_path:
                exc_args = {
                    "main_message": "A failure occurred while searching the file. The file path does not include a file with an extension.",
                    "custom_type": FileSearchFailure,
                    "expected_result": "A file with an extension (ex: myfile.txt)",
                    "returned_result": file_path,
                    "suggested_resolution": "Please verify you have sent a full file path and not a directory.",
                }
                raise FileSearchFailure(FCustomException(message_args=exc_args, tb_remove_name="search_file"))

            logger.debug(f'Reading in all lines from the file "{file_path}"')
            # Sets the basename for cleaner logging output.
            basename_searched_file = os.path.basename(file_path)
            logger.debug(f'Looping through file "{basename_searched_file}" {index + 1} of {total_files}')

            try:
                file_check(file_path)
            except FFileNotFoundError:
                raise

            # Using "with" to take care of open and closing.
            with open(file_path, "r") as f:
                readLines = f.readlines()
                # Loops through each line.
                for line in readLines:
                    # Adds a line to the list.
                    grouped_found_file_lines.append(line)

            logger.debug("Looping through all lines from the files 1 by 1")
    else:
        # Using "with" to take care of open and closing.
        with open(file_path, "r") as f:
            readLines = f.readlines()
            # Loops through each line.
            for line in readLines:
                # Adds a line to the list.
                grouped_found_file_lines.append(line)

    # Looping through all lines from the log file(s) line list 1 by 1.
    for index, line in enumerate(grouped_found_file_lines):
        # Strips off the '\n' character.
        stripped_line: str = str(line).strip()
        # Checks if searching_value is a str or list
        if isinstance(searching_value, str):
            # Checks if a value exists as each line is read.
            if searching_value in stripped_line:
                logger.debug(
                    f'Searched file value "{searching_value}" found. Adding file value to the returning list "matched_entries"'
                )
                # Checks if the next line needs to be included in the search.
                if include_next_line_value:
                    multi_line_builder: list = []
                    line_tracker: int = index
                    while True:
                        # Adds found line and search value to list
                        multi_line_builder.append(grouped_found_file_lines[line_tracker].strip())

                        line_tracker += 1

                        # Checks if the end of the file lines.
                        if line_tracker >= len(grouped_found_file_lines):
                            break
                        # Checks if the next line value filters do not match to break the loop.
                        if isinstance(include_next_line_value, str):
                            if include_next_line_value not in str(grouped_found_file_lines[line_tracker]):
                                break
                        if isinstance(include_next_line_value, list):
                            found: bool = True
                            for next_line_value in include_next_line_value:
                                if str(next_line_value) in str(grouped_found_file_lines[line_tracker]):
                                    found = True
                                    break
                                else:
                                    found = False
                            if found is False:
                                break
                    matched_entries.append(
                        {"search_entry": searching_value, "found_entry": str("\n".join(multi_line_builder))}
                    )
                else:
                    # Adds found line and search value to list
                    matched_entries.append({"search_entry": searching_value, "found_entry": stripped_line})
        elif isinstance(searching_value, list):
            # Loops through each search value
            for search_value in searching_value:
                # Checks if a value exists as each line is read.
                if str(search_value) in str(stripped_line):
                    logger.debug(
                        f'Searched file value "{search_value}" from value list "{searching_value}" found. Adding file value "{stripped_line}" to the returning list "matched_entries"'
                    )
                    # Checks if the next line needs to be included in the search.
                    if include_next_line_value:
                        multi_line_builder: list = []
                        line_tracker: int = index
                        while True:
                            # Adds found line and search value to list
                            multi_line_builder.append(grouped_found_file_lines[line_tracker].strip())

                            line_tracker += 1

                            # Checks if the next line value filters do not match to break loop.
                            if isinstance(include_next_line_value, str):
                                if include_next_line_value not in str(grouped_found_file_lines[line_tracker]):
                                    break
                            if isinstance(include_next_line_value, list):
                                found: bool = True
                                for next_line_value in include_next_line_value:
                                    if str(next_line_value) in str(grouped_found_file_lines[line_tracker]):
                                        found = True
                                        break
                                    else:
                                        found = False
                                if found is False:
                                    break
                        matched_entries.append(
                            {"search_entry": searching_value, "found_entry": str("\n".join(multi_line_builder))}
                        )
                    else:
                        # Adds found line and search value to list
                        matched_entries.append({"search_entry": searching_value, "found_entry": stripped_line})

    # Checking if the list has discovered values for potential cleanup.
    if matched_entries:
        # Checks if searching_value is str or list to clean up any potential duplicates
        if isinstance(searching_value, str):
            logger.debug("Searched file value has been found")
        elif isinstance(searching_value, list):
            logger.debug("Searched file values have been found")
            logger.debug(f"A list of all found search matches is listed below: {matched_entries}")
            logger.debug(
                f"Removing any duplicate entries that may have matched multiple times with similar search info"
            )
            # Removes any duplicate matched values using the 2nd entry (1st element). This can happen if a search list has a similar search word that discovers the same line.
            # Example Return: [{'search_entry': '|Error|', 'found_entry': 'the entry found2'}]
            matched_entries = remove_duplicate_dict_values_in_list(matched_entries, 1)
            logger.debug(f"The adjusted match list with removed duplicates is listed below: {matched_entries}")

    # Checking if the list has discovered log entry values.
    if matched_entries:
        logger.debug("Returning found values")
        # Returns found lines(s).
        return matched_entries
    elif not matched_entries:
        logger.debug("No searched value has have been found")
        logger.debug("Returning None")
        # Returns "None" because no strings found.
        return None


def convert_relative_to_full_path(relative_path: str) -> str:
    """
    Determines a full file path to file given a relative file path compatible\\
    with PyInstaller(compiler) built-in.

    Args:
        relative_path (str):
        \t\\- The unqualified (relative) file path that needs to converted to\\
        \t  a qualified full path format

    Calling Example:
    \t\\- relative_path = "\\[directory]\\[file].[extension]"

    Raises:
        FTypeError (fexception):
        \t\\- The object value '{relative_path}' is not an instance of the required class(es) or subclass(es).

    Returns:
        str:
        \t\\- Full file path.

    Return Example:\\
    \t\\- "C:\\[root directory]\\[directory]\\[file].[extension]"
    """
    logger = logging.getLogger(__name__)
    logger.debug(f"=" * 20 + get_function_name() + "=" * 20)
    # Custom flowchart tracking. This is ideal for large projects that move a lot.
    # For any third-party modules, set the flow before making the function call.
    logger_flowchart = logging.getLogger("flowchart")
    logger_flowchart.debug(f"Flowchart --> Function: {get_function_name()}")

    type_check(value=relative_path, required_type=str, tb_remove_name="convert_relative_to_full_path")

    logger.debug("Passing parameters:\n" f"  - relative_path(str):\n        - {relative_path}\n")

    if hasattr(sys, "_MEIPASS"):
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS  # type: ignore
    else:
        # When running un-compiled, use normal os calls to determine location
        base_path = os.getcwd()

    return f"{base_path}\\{relative_path}"


def user_file_selection(prompt: str, criteria: str, root_dir: Optional[str] = None) -> str:
    """
    Provides a simple user interface that numerically lists a set of files\\
    found using user submitted criteria.

    The user is prompted to submit the numeric value of the file that is to be used.

    Args:
        prompt (str):
        \t\\- Literal prompt string to present to the user.\\
        criteria (str):
        \t\\- Filter to apply when searching for files.\\
        \t\\- Expects standard OS search criteria\\
        root_dir (str, optional):
        \t\\- Manually sets the root directory to search.\\
        \t\\- Requires an absolute path format.\\
        \t\\- Defaults to None.

    Calling Examples:
    \t\\- prompt = "Enter the database name to import"\\
    \t\\- criteria = "*.db" or "*config*"\\
    \t\\- root_dir = "C:\\Directory\\Subdirectory\"

    Raises:
        FTypeError (fexception):
        \t\\- The object value '{prompt}' is not an instance of the required class(es) or subclass(es).
        FTypeError (fexception):
        \t\\- The object value '{criteria}' is not an instance of the required class(es) or subclass(es).
        FTypeError (fexception):
        \t\\- The object value '{root_dir}' is not an instance of the required class(es) or subclass(es).
        FFileNotFoundError (fexception):
        \t\\- No files were found matching the required criteria.

    Returns:
        str:
        \t\\- Returns the path of the file that was selected in the format provided

    Return Example:\\
    \t\\- "test.py" or "c:\\folder\\test.py"
    """
    logger = logging.getLogger(__name__)
    logger.debug(f"=" * 20 + get_function_name() + "=" * 20)
    # Custom flowchart tracking. This is ideal for large projects that move a lot.
    # For any third-party modules, set the flow before making the function call.
    logger_flowchart = logging.getLogger("flowchart")
    logger_flowchart.debug(f"Flowchart --> Function: {get_function_name()}")

    type_check(value=prompt, required_type=str, tb_remove_name="user_file_selection")
    type_check(value=criteria, required_type=str, tb_remove_name="user_file_selection")
    if root_dir:
        type_check(value=root_dir, required_type=str, tb_remove_name="user_file_selection")

    if root_dir:
        formatted_root_dir = f"  - relative_path (str):\n        - {root_dir}"
    else:
        formatted_root_dir = f"  - relative_path (str):\n        - None"
    logger.debug(
        "Passing parameters:\n"
        f"  - prompt (str):\n        - {prompt}\n"
        f"  - criteria (str):\n        - {criteria}\n"
        f"{formatted_root_dir}\n"
    )

    # Initialize an empty list that will contain files found during search
    files = []
    # Print the prompt
    print(prompt)
    """
    # Search for files in the current working directory
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
        print(f"  [{[i for i, x in enumerate(files) if x == file][0]}] {os.path.basename(file)}")

    # If no files were found matching user provided criteria, raise exception
    if len(files) == 0:
        exc_args = {
            "main_message": "No files were found matching the required criteria.",
            "expected_result": "A matching file.",
            "returned_result": 0,
        }
        raise FFileNotFoundError(message_args=exc_args, tb_remove_name="user_file_selection")

    # Loop until valid input is provided by user
    while True:
        try:
            selection = int(input("\nSelection [#]:  "))
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
