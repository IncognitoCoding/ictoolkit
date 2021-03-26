#!interpreter

"""
This module is designed to assist with file-related actions.
"""
# Built-in/Generic Imports
import os
import pathlib
import logging
import traceback

# Own modules
from ictoolkit.directors.dict_director import remove_duplicate_dict_values_in_list

__author__ = 'IncognitoCoding'
__copyright__ = 'Copyright 2021, file_director'
__credits__ = ['IncognitoCoding']
__license__ = 'GPL'
__version__ = '1.0'
__maintainer__ = 'IncognitoCoding'
__status__ = 'Development'


def write_file(file_path, write_value, logger=None):
    """
    Writes a value to the file.

    Args:
        file_path (str): the file path being written into
        write_value (str): the value being written into the file
        logger (logger, optional): logger. Defaults to None.

    Raises:
        ValueError: A failure occurred while writing the file
        ValueError: Writing file value <Value Being Written> to file <File Path Being Written> did not complete. The value does not exist after being written
    """

    # Checks if logger exists.
    if logger != None:
        logger.debug(f'Begining to write the value to the file. write_value = {write_value}')

    try:
        
        # Checks if logger exists.
        if logger != None:
            # Writing the value to the file.
            logger.debug('Writing the value to the file')

        # Using "with" to take care of open and closing.
        with open (file_path, 'a+') as f:
            f.writelines(write_value + "\n")

    except Exception as err: 
        raise ValueError(f'A failure occurred while writing the file., {err}, Originating error on line {traceback.extract_stack()[-1].lineno} in <{__name__}>')

    else:

        # Checks if logger exists.
        if logger != None:
            # Checking if the file entry written to the file.
            # Calling Example: search_file(<log file>, <search string>, <configured logger>)
            return_Search = search_file(file_path, write_value, logger)
        else:
             # Checking if the file entry written to the file.
            # Calling Example: search_file(<log file>, <search string>, <configured logger>)
            return_Search = search_file(file_path, write_value)

        # Validates file entry wrote.
        if return_Search == None: 
            raise ValueError(f'Writing file value \"{write_value}\" to file \"{file_path}\" did not complete. The value does not exist after being written, Originating error on line {traceback.extract_stack()[-1].lineno} in <{__name__}>')


def file_exist_check(file_path, file_description, logger=None):
    """
    Validates the file exists.

    Args:
        file_path (str): the file path being checked
        file_description (str): name of the file being checked
        logger (logger, optional): logger. Defaults to None.

    Raises:
        ValueError: Log file does not exist
    """

    # Checks if logger exists.
    if logger != None:
        logger.debug(f'Begining to check the file path for {file_description}')

    # Checks if the file does not exist
    file = pathlib.Path(file_path)
    if not file.exists ():
        raise ValueError(f'{file_description} log file does not exist, Originating error on line {traceback.extract_stack()[-1].lineno} in <{__name__}>')
    else:
        # Checks if logger exists.
        if logger != None:
            logger.debug(f'{file_description} log file exists')


def search_file(file_path, searching_value, logger=None):
    """
    Searches the file for a value. The search can look for multiple values when the searching value arguments are passed as a list. A single-string search is supported as well.

    Args:
        file_path (str): the file path being checked
        searching_value (str or list): search value that is looked for within the file. The entry can be a single string or a list to search
        logger (logger, optional): logger. Defaults to None.

    Raises:
        ValueError: A failure occurred while searching the file

    Returns:
        list: a dictionary in a list
        
        Useage Keys:
            - search_entry
            - found_entry
            
        Return Example: Return Example: [{'search_entry': '|Error|', 'found_entry': 'the entry found'}, {'search_entry': '|Warning|', 'found_entry': 'the entry found'}]
    """
    # Checks if logger exists.
    if logger != None:
        logger.debug(f'Begining to search the file \"{file_path}\" for a value \"{searching_value}\"')

    try:

        # Stores the search entry and found info.
        # Required to return multiple found strings.
        matched_entries = []

        # Checks if logger exists.
        if logger != None:
            logger.debug('Reading in all lines from the file')

        # Using "with" to take care of open and closing.
        with open (file_path, 'r') as f:
            lines = f.readlines()
        
        # Checks if logger exists.
        if logger != None:
            logger.debug('Looping through all lines from the file 1 by 1')

        # Looping through all lines from the log file 1 by 1.
        for line in lines:
            
            # Strips off the '\n' character.
            stripped_line = (line.strip())

            # Checks if searching_value is a str or list
            if isinstance(searching_value, str):

                # Checks if a value exists as each line is read.
                if searching_value in stripped_line:
                    
                    # Checks if logger exists.
                    if logger != None:
                        logger.debug(f'Searched file value \"{searching_value}\" found. Adding file value to the returning list \"matched_entries\"')

                    # Adds found line and search value to list
                    matched_entries.append({'search_entry': searching_value, 'found_entry': stripped_line})

            elif isinstance(searching_value, list):

                # Loops through each search value
                for search_value in searching_value:

                    # Checks if a value exists as each line is read.
                    if search_value in stripped_line:
                        
                        # Checks if logger exists.
                        if logger != None:
                            logger.debug(f'Searched file value \"{search_value}\" from value list \"{searching_value}\" found. Adding file value \"{stripped_line}\" to the returning list \"matched_entries\"')

                        # Adds found line and search value to list
                        matched_entries.append({'search_entry': searching_value, 'found_entry': stripped_line})

        # Checks if logger exists.
        if logger != None:
            logger.debug('Checking if the list \"matched_entries\" has matched values')

        # Checking if the listy has discovered values for potential cleanup.
        if matched_entries:

            # Checks if searching_value is str or list to clean up any potential duplicates
            if isinstance(searching_value, list):
                
                # Checks if logger exists.
                if logger != None:
                    logger.debug(f'A list of all found search matches is listed below: {matched_entries}')
                    logger.debug(f'Removing any duplicate entries that may have matched multiple times with similar search info')

                # Removes any duplicate matched values using the 2nd entry (1st element). This can happen if a search list has a similar search word that discovers the same line.
                # Example Return: [{'search_entry': '|Error|', 'found_entry': 'the entry found2'}]
                matched_entries = remove_duplicate_dict_values_in_list(matched_entries, 1) 

                # Checks if logger exists.
                if logger != None:
                    logger.debug(f'The adjusted match list with removed duplicates is listed below: {matched_entries}')

    except Exception as err: 
        raise ValueError(f'A failure occurred while searching the file., {err}, Originating error on line {traceback.extract_stack()[-1].lineno} in <{__name__}>')

    else:
        
        # Checking if the list has discovered log entry values.
        if matched_entries:
            
            # Checks if logger exists.
            if logger != None:
                logger.debug('Returning found values')

            # Returns found lines(s).
            return matched_entries

        elif not matched_entries:

            # Checks if logger exists.
            if logger != None:
                logger.debug('No searched value has have been found')
                logger.debug('Returning None')
                
            # Returns "None" because no strings found.
            return None


def search_multiple_files(file_paths, searching_value, logger=None):
    """
    Searches multiple files for a value. Requires the file_path to be sent as a list. The search can look for multiple values when the searching value arguments are passed as a list. 
    A single-string search is supported as well.

    Args:
        file_path (str): the file path being checked
        searching_value (str or list): search value that is looked for within the file. The entry can be a single string or a list to search
        logger (logger, optional): logger. Defaults to None.

    Raises:
        ValueError: A failure occurred while searching the file

    Returns:
        list: A list of discovered search values. Each discovered value is per element. No discovered values will return None.

        Useage Keys:
            - search_entry
            - found_entry

        Return Example: Return Example: [{'search_entry': '|Error|', 'found_entry': 'the entry found'}, {'search_entry': '|Warning|', 'found_entry': 'the entry found'}]
    """

    # Checks if logger exists.
    if logger != None:
        logger.debug(f'Begining to search the files \"{file_paths}\" for a value \"{searching_value}\"')

    try:
        
        # Assigns list variable to be used in this function.
        # Required to return multiple found strings.
        grouped_found_files = []
        matched_entries = []
        
        # Sets count on total files being searched.
        total_files = len(file_paths)

        # Checks if logger exists.
        if logger != None:
            logger.debug('Starting to loop through file(s)')

        # Loops through each file path to add all lines into a single list.
        for index, file_path in enumerate(file_paths):
            
            # Checks if logger exists.
            if logger != None:
                logger.debug(f'Reading in all lines from the file \"{file_path}\"')

            # Sets the basename for cleaner logging output.
            basename_searched_file = os.path.basename(file_path)

            # Checks if logger exists.
            if logger != None:
                logger.debug(f'Looping through file \"{basename_searched_file}\" {index + 1} of {total_files}')

            # Using "with" to take care of open and closing.
            with open (file_path, 'r') as f:

                readLines = f.readlines()
                
                # Loops through each line.
                for line in readLines:
                    
                    # Adds line to list.
                    grouped_found_files.append(line)
        
        # Checks if logger exists.
        if logger != None:
            logger.debug('Looping through all lines from the files 1 by 1')

        # Looping through all lines from the log file 1 by 1.
        for line in grouped_found_files:
            
            # Strips off the '\n' character.
            stripped_line = (line.strip())
            
            # Checks if searching_value is a str or list
            if isinstance(searching_value, str):
                
                # Checks if a value exists as each line is read.
                if searching_value in stripped_line:
                    
                    # Checks if logger exists.
                    if logger != None:
                        logger.debug(f'Searched file value \"{searching_value}\" found. Adding file value to the returning list \"matched_entries\"')

                    # Adds found line and search value to list
                    matched_entries.append({'search_entry': searching_value, 'found_entry': stripped_line})

            elif isinstance(searching_value, list):

                # Loops through each search value
                for search_value in searching_value:

                    # Checks if a value exists as each line is read.
                    if search_value in stripped_line:
                        
                        # Checks if logger exists.
                        if logger != None:
                            logger.debug(f'Searched file value \"{search_value}\" from value list \"{searching_value}\" found. Adding file value \"{stripped_line}\" to the returning list \"matched_entries\"')

                        # Adds found line and search value to list
                        matched_entries.append({'search_entry': searching_value, 'found_entry': stripped_line})

        # Checks if logger exists.
        if logger != None:
            logger.debug('Checking if the list has discovered file entry values')
        
        # Checking if the listy has discovered values for potential cleanup.
        if matched_entries:
            
            # Checks if searching_value is str or list to clean up any potential duplicates
            if isinstance(searching_value, str):
                
                # Checks if logger exists.
                if logger != None:
                    logger.debug('Searched file value has been found')

            elif isinstance(searching_value, list):
                
                # Checks if logger exists.
                if logger != None:
                    logger.debug('Searched file values have been found')
                    logger.debug(f'A list of all found search matches is listed below: {matched_entries}')
                    logger.debug(f'Removing any duplicate entries that may have matched multiple times with similar search info')

                # Removes any duplicate matched values using the 2nd entry (1st element). This can happen if a search list has a similar search word that discovers the same line.
                # Example Return: [{'search_entry': '|Error|', 'found_entry': 'the entry found2'}]
                matched_entries = remove_duplicate_dict_values_in_list(matched_entries, 1) 

                # Checks if logger exists.
                if logger != None:
                    logger.debug(f'The adjusted match list with removed duplicates is listed below: {matched_entries}')
            
    except Exception as err: 
        raise ValueError(f'A failure occurred while searching the file., {err}, Originating error on line {traceback.extract_stack()[-1].lineno} in <{__name__}>')

    else:
        
        # Checking if the list has discovered log entry values.
        if matched_entries:
            
            # Checks if logger exists.
            if logger != None:
                logger.debug('Returning found values')
 
            # Returns found lines(s).
            return matched_entries

        elif not matched_entries:
            
            # Checks if logger exists.
            if logger != None:
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
        logger (logger, optional): logger. Defaults to None.

    Raises:
        ValueError: Failure occured while clearing log file
        ValueError: Log file size is <File Size> bytes after clearing. Failed to clear log
        ValueError: <File Path> file does not exist., <General Error>
    """

    # Checks if logger exists.
    if logger != None:
        logger.debug(f'Begining to check if the log file {file_path} has reached {size_max_file_size} bytes')

    # Checks if file exists before starting.
    # Log files may not exist on the initial start.
    file = pathlib.Path(file_path)
    if file.exists ():
        
        # Gets log file size.
        size_file_path = os.path.getsize(file_path)
    
        # Checks if the log file is greater than the threshold.
        if size_file_path > size_max_file_size:
            
            # Checks if logger exists.
            if logger != None:
                logger.debug(f'Log file size is {size_file_path} bytes and over threashold of {size_max_file_size} bytes')
                logger.info('Clearing the log file because it is over the file size threshold')

            # Clears older entries in the log file.
            try:
                # Clears log file.
                f = open(file_path,"w")
                f.close()
            except Exception as err:
                raise ValueError(f'Failure occured while clearing log file., {err}, Originating error on line {traceback.extract_stack()[-1].lineno} in <{__name__}>')

            # Gets log file size again.
            size_file_path = os.path.getsize(file_path)
            
            # Checks if log file cleared.
            if size_file_path > size_max_file_size:
                raise ValueError(f'Log file size is {size_file_path} bytes after clearing. Failed to clear log., {err}, Originating error on line {traceback.extract_stack()[-1].lineno} in <{__name__}>')

            else:
                # Checks if logger exists.
                if logger != None:
                    logger.info('Log file cleared successfully')

        else:
            # Checks if logger exists.
            if logger != None:
                logger.debug(f'Log file size is {size_file_path} bytes and under threshold of {size_max_file_size} bytes. No action required.')

    else:
        raise ValueError(f'{file_path} file does not exist., {err}, Originating error on line {traceback.extract_stack()[-1].lineno} in <{__name__}>')
