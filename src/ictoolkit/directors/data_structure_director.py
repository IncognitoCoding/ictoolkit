"""
This module is designed to offer data structure functions. These data structures include lists, tuples, sets, and dictionaries.
"""
# Built-in/Generic Imports
import re
import logging
from itertools import groupby
from typing import Union

# Libraries
from fchecker import type_check

# Local Functions
#   - Full path required to avoid partially initialized module error.
from ictoolkit import get_function_name

# Exceptions
from fexception import FGeneralError, FKeyError, FTypeError, FValueError

__author__ = 'IncognitoCoding'
__copyright__ = 'Copyright 2022, data_structure_director'
__credits__ = ['IncognitoCoding']
__license__ = 'MIT'
__version__ = '3.0'
__maintainer__ = 'IncognitoCoding'
__status__ = 'Production'


def remove_duplicate_dict_values_in_list(list_dictionary: list, element_number: int = None) -> list:
    """
    Removes duplicate values in a dictionary within a list and returns
    the same list minus duplicates.

    This function will convert a list of dictionaries into a list of tuples
    that contains items of the dictionary for duplicate removal.

    A list of dictionaries are sometimes needed to be sorted based off a specific
    element in the dictionary entry.

    This function offers the ability to choose which element number to use for matching
    or match the entire dictionary element.

    Args:
        list_dictionary (list):
        \t\\- A dictionary with duplicate values in a list.
        element_number (int, optional):
        \t\\- Enter the dictionary element number when matching based on a specific dictionary\\
        \t   element in the dictionary line.\\
        \t\\- Defaults to None for a full match.

    Calling Examples:\\
    \tList Dictionary Example:\\
    \t\t\\- list_dictionary = [{'search_entry': '|Error|',
    \t\t\t\t\t       'found_entry': 'the entry found'},
    \t\t\t\t\t       {'search_entry': '|Warning|',
    \t\t\t\t\t       'found_entry': 'the entry found'}]
    \tMatch Dictionary Example:\\
    \t\t\\- element_number = None
    \t\t\t\\- Match On:
    \t\t\t\t\\- ('search_entry': '|Error|', 'found_entry': 'the entry found')\\
    \t\t\t\t\\- ('search_entry': '|Warning|', 'found_entry': 'the entry found')
    \t\t\t\\- No match would occur, and both dictionary entries would return.\\
    \t\t\t\\- Return:
    \t\t\t\t\\- [{'search_entry': '|Error|', 'found_entry': 'the entry found'},
    \t\t\t\t   {'search_entry': '|Warning|', 'found_entry': 'the entry found'}]
    \t\t\\- element_number = 1
    \t\t\t\\- Match On:
    \t\t\t\t\\- ('found_entry': 'the entry found')
    \t\t\t\t\\- ('found_entry': 'the entry found')
    \t\t\t\\- A match would occur, and only one dictionary entry would return.
    \t\t\t\t\\- Return:
    \t\t\t\t\\- [{'search_entry': '|Error|', 'found_entry': 'the entry found'}]

    Raises:
        FTypeError (fexception):
        \t\\- The value '{list_dictionary}' is not in <class 'list'> format.
        FTypeError (fexception):
        \t\\- The value '{element_number}' is not in <class 'int'> format.
        FGeneralError (fexception):
        \t\\- A general failure occurred removing duplicates from the dictionary in the list.

    Returns:
        list:\\
        \t\\- A list of dictionars with duplicate values removed.
    """
    logger = logging.getLogger(__name__)
    logger.debug(f'=' * 20 + get_function_name() + '=' * 20)
    # Custom flowchart tracking. This is ideal for large projects that move a lot.
    # For any third-party modules, set the flow before making the function call.
    logger_flowchart = logging.getLogger('flowchart')
    logger_flowchart.debug(f'Flowchart --> Function: {get_function_name()}')

    try:
        type_check(list_dictionary, list)
        if element_number:
            type_check(element_number, int)
    except FTypeError:
        raise

    formatted_list_dictionary = '  - list_dictionary (list):' + str('\n        - ' + '\n        - '.join(map(str, list_dictionary)))
    if element_number:
        formatted_element_number = f'  - element_number (int):\n        - {element_number}'
    else:
        formatted_element_number = f'  - element_number (int):\n        - None'
    logger.debug(
        'Passing parameters:\n'
        f'{formatted_list_dictionary}\n '
        f'{formatted_element_number}\n'
    )

    # Holds temporary found elements for comparison.
    element_found = set()
    # Stores the revised list that does not contain any duplicates.
    revised_list = []

    try:

        # Loops through each dictionary in the list
        for dictionary_in_list in list_dictionary:
            # Checks if section number is being used for matching or a full match is being used.
            if element_number is None:
                # Used tuple because it can be hashed, which allows removal using set.
                # This will convert the dictionaries in the list to tuples that contains the dictionaries.
                # Sorted is added to help with any possible match issues wien adding/removing lots of key history.
                items_of_dictionary = tuple(sorted(dictionary_in_list.items()))
                # Checks if dictionary entry matches previous entries.
                if items_of_dictionary not in element_found:
                    # New element found and adding to set.
                    element_found.add(items_of_dictionary)

                    # Adds the full dictionary_in_list to the list because it is not a duplicate.
                    revised_list.append(dictionary_in_list)
            elif element_number:
                # Used tuple because it can be hashed, which allows removal using set.
                # This will convert the dictionaries in the list to tuples that contains the dictionaries.
                # No sort is added here because sort will break the element number order.
                items_of_dictionary = tuple(dictionary_in_list.items())
                # Checks if dictionary element section does not match previous entries.
                if items_of_dictionary[element_number] not in element_found:
                    # New element found and adding to set.
                    element_found.add(items_of_dictionary[element_number])

                    # Adds the full dictionary_in_list to the list because it is not a duplicate.
                    revised_list.append(dictionary_in_list)
    except Exception as exc:
        exc_args = {
            'main_message': 'A general failure occurred removing duplicates from the dictionary in the list.',
            'original_exception': exc,
        }
        raise FGeneralError(exc_args)
    else:
        return revised_list


def get_list_of_dicts_duplicates(key: str, list_dictionary: list, grouped: bool = False) -> Union[list, dict, None]:
    """
    Finds duplicate dictionary values in the list using the key and return the value and index points.

    Duplicates can be either un-grouped or grouped. Default is un-grouped.

    Returning both the duplicate and original list index points allows any modification or additional data search when the duplicates return.

    A key is required to find all duplicates for that key.

    Calling Examples:\\
    \tExamples:\\
    \t\t\\- key = key1
    \t\t\\- list_dictionary = [{'key1': 'ValueA'},
    \t\t\t\t\t      {'key1': 'ValueA'},
    \t\t\t\t\t      {'key1': 'ValueA'},
    \t\t\t\t\t      {'key1': 'ValueB'},
    \t\t\t\t\t      {'key1': 'ValueB'},
    \t\t\t\t\t      {'key1': 'ValueC'},
    \t\t\t\t\t      {'key1': 'ValueD'}]

    Args:
        key (str):
        \t\\- the dictionary key that needs to get all duplicate values assigned to that ke
        list_dictionary (list):
        \t\\- dictionary with duplicate values in a list
        grouped (bool):
        \t\\- enables grouping of duplicate values.\\
        \t\\- Disabled by default

    Raises:
        FTypeError (fexception):
        \t\\- The value '{key}' is not in <class 'str'> format.
        FTypeError (fexception):
        \t\\- The value '{list_dictionary}' is not in <class 'list'> format.
        FTypeError (fexception):
        \t\\- The value '{grouped}' is not in <class 'bool'> format.
        FKeyError (fexception):
        \t\\- A failure occurred getting duplicate values the list.
        FGeneralError (fexception):
        \t\\- A general failure occurred getting duplicate values from the key ({key}) in the list_dictionary.
        FGeneralError (fexception):
        \t\\- A genearl failure occurred grouping duplicate values.

    Returns:
        Union[list, dict, None]:
        \t\\- list:\\
        \t\t\\- The default return option is un-grouped duplicate values in dictionary format in a list.
        \t\\- dict:\\
        \t\t\\- Enabling grouped will return the duplicate values grouped in a dictionary with individual nested groupings.
        \t\\- None:\\
        \t\t\\- If no duplicates are detected, a value of "None" will be returned.

    Return Examples:\\
    \tUn-Grouped:\\
    \t\t\\- [{'index': 0, 'value': 'ValueA'},
    \t\t   {'index': 1, 'value': 'ValueA'},
    \t\t   {'index': 2, 'value': 'ValueA'},
    \t\t   {'index': 3, 'value': 'ValueB'},
    \t\t   {'index': 4, 'value': 'ValueB'}]
    \tGrouped:\\
    \t\t\\- {'ValueA': [{'index': 0, 'value': 'ValueA'},
    \t\t\t\t   {'index': 1, 'value': 'ValueA'},
    \t\t\t\t   {'index': 2, 'value': 'ValueA'}],
    \t\t    'ValueB': [{'index': 3, 'value': 'ValueB'},
    \t\t\t\t   {'index': 4, 'value': 'ValueB'}]}
    """
    logger = logging.getLogger(__name__)
    logger.debug(f'=' * 20 + get_function_name() + '=' * 20)
    # Custom flowchart tracking. This is ideal for large projects that move a lot.
    # For any third-party modules, set the flow before making the function call.
    logger_flowchart = logging.getLogger('flowchart')
    logger_flowchart.debug(f'Flowchart --> Function: {get_function_name()}')

    try:
        type_check(key, str)
        type_check(list_dictionary, list)
        type_check(grouped, bool)
    except FTypeError:
        raise

    formatted_list_dictionary = '  - list_dictionary (list):' + str('\n        - ' + '\n        - '.join(map(str, list_dictionary)))
    logger.debug(
        'Passing parameters:\n'
        f'  - key (int):\n        - {key}\n'
        f'{formatted_list_dictionary}\n'
        f'  - grouped (bool):\n        - {grouped}\n'
    )

    try:
        # Temporary storage for unique items.
        temp_unique_items = []
        # Stores duplicate list entries as dictionaries.
        # The key is the duplicate from the list and the value is the index.
        duplicate_list_dictionary = []
        # Gets values of the keys.
        duplicates_of_key = [a_dict[key] for a_dict in list_dictionary]

        # Loops through all values.
        for entry in duplicates_of_key:
            # Checks if the entry from the list exists in the "temp_unique_items" list. If not it gets added to the temp list.
            # If the entry exists the entry will hit the elif statement and get all index points for the duplicates.
            if entry not in temp_unique_items:
                # Adds the entry to the list.
                temp_unique_items.append(entry)
            # Checks if the duplicate entry already exists in the duplicate_list_dictionary list.
            # This has to check if the 'duplicate_list_dictionary' is empty and if the duplicate list does not contain the entry.
            # The two different "entry" searches are required in case the key is a string or an INT. A string would have a single quote and an INT would not.
            elif bool(duplicate_list_dictionary) is False or f'\'value\': {entry}' not in str(duplicate_list_dictionary) and f'\'value\': \'{entry}\'' not in str(duplicate_list_dictionary):
                # Loops through all entries in the list.
                for index, value in enumerate(duplicates_of_key):
                    # Checks if the value from the list is equal to the discovered duplicate.
                    if value == entry:
                        # Adds the duplicate entry values and index
                        # The value will be the key and the index will be the value.
                        # This will allow the ease if finding all index points for a specific value.
                        duplicate_list_dictionary.append({'index': index, 'value': value})
    except KeyError:
        exc_args = {
            'main_message': 'A failure occurred getting duplicate values the list.',
            'expected_result': f'The searching key ({key}) existing in the dictionary',
            'returned_result': f'The searching key ({key}) does not existing in the dictionary ({list_dictionary})',
            'suggested_resolution': 'Please verify you have set all required keys and try again.',
        }
        raise FKeyError(exc_args)
    except Exception as exc:
        exc_args = {
            'main_message': f'A general failure occurred getting duplicate values from the key ({key}) in the list_dictionary.',
            'original_exception': exc,
        }
        raise FGeneralError(exc_args)
    else:
        # Checks that duplicates exist.
        if duplicate_list_dictionary:
            # Checks if the user enabled grouping.
            if grouped:

                try:
                    # Stores new grouped entries
                    grouped = {}
                    # Loops through each grouped entry.
                    for entry in duplicate_list_dictionary:
                        # Gets matching entries based on the "value" key and adds them to the grouped dictionary.
                        grouped[entry['value']] = grouped.get(entry['value'], [])
                        grouped[entry['value']].append(entry)
                except Exception as exc:
                    exc_args = {
                        'main_message': 'A genearl failure occurred grouping duplicate values.',
                        'original_exception': exc,
                    }
                    raise FGeneralError(exc_args)
                else:
                    # Returns grouped duplicates.
                    return grouped
            else:
                # Returns un-grouped duplicates.
                return duplicate_list_dictionary
        else:
            return None


def get_list_duplicates(duplicates: list, match_index: int = None, grouped: bool = False) -> Union[list, dict, None]:
    """
    Finds duplicate entries in the list return the value and index points.

    Duplicates can be either un-grouped or grouped. Default is un-grouped.

    Returning both the duplicate and original list index points allows any modification\\
    or additional data search when the duplicates return.

    Args:
        duplicates (list):
        \t\\- List with duplicate strings, a list with duplicate list index,\\
        \t  a list with duplicate lists, a list with duplicate tuple index, and a list with duplicate tuple lists.
        match_index (int, optional):
        \t\\- If the entries in the lists are a list the index can be set to match on a specific index in the list.\\
        \t\\- Defaults to None.
        grouped (bool):
        \t\\- Enables grouping of duplicate values.\\
        \t\\- Defaults to False.

    Calling Examples:\\
    \tExample1:
    \t\t\\- duplicates = ['ValueA',
    \t\t\t\t\t'ValueA',
    \t\t\t\t\t'ValueA',
    \t\t\t\t\t'ValueB',
    \t\t\t\t\t'ValueB',
    \t\t\t\t\t'ValueC',
    \t\t\t\t\t'ValueD']
    \tExample2:\\
    \t\t\\- duplicates = [['ValueA', 'ValueB'],
    \t\t\t\t\t['ValueA', 'ValueB'],
    \t\t\t\t\t['ValueD', 'ValueB'],
    \t\t\t\t\t['ValueB'], ['ValueB']
    \tExample3:\\
    \t\t\\- duplicates = [('ValueA', 'ValueB'),
    \t\t\t\t\t('ValueA', 'ValueB'),
    \t\t\t\t\t('ValueD', 'ValueB'),
    \t\t\t\t\t('ValueB'), ('ValueB')]

    Raises:
        FTypeError (fexception):
        \t\\- The value '{duplicates}' is not in <class 'list'> format.
        FTypeError (fexception):
        \t\\- The value '{match_index}' is not in <class 'int'> format.
        FTypeError (fexception):
        \t\\- The value '{grouped}' is not in <class 'bool'> format.
        FGeneralError: A general failure occurred getting duplicate values the list.
        FGeneralError: A general failure occurred grouping duplicate values.


    Returns:
        Union[list, dict, None]:
        \t\\- list:\\
        \t\t\\- The default return option is un-grouped duplicate values in dictionary format in a list.
        \t\\- dict:\\
        \t\t\\- Enabling grouped will return the duplicate values grouped in a dictionary with individual nested groupings.
        \t\\- None:\\
        \t\t\\- If no duplicates are detected, a value of "None" will be returned.

    Return Examples:\\
    \tUn-Grouped:\\
    \t\t\\- [{'index': 0, 'value': 'ValueA'},
    \t\t   {'index': 1, 'value': 'ValueA'},
    \t\t   {'index': 2, 'value': 'ValueA'},
    \t\t   {'index': 3, 'value': 'ValueB'},
    \t\t   {'index': 4, 'value': 'ValueB'}]
    \tGrouped:\\
    \t\t\\- {'ValueA': [{'index': 0, 'value': 'ValueA'},
    \t\t\t\t   {'index': 1, 'value': 'ValueA'},
    \t\t\t\t   {'index': 2, 'value': 'ValueA'}],
    \t\t    'ValueB': [{'index': 3, 'value': 'ValueB'},
    \t\t\t\t   {'index': 4, 'value': 'ValueB'}]}
    """
    logger = logging.getLogger(__name__)
    logger.debug(f'=' * 20 + get_function_name() + '=' * 20)
    # Custom flowchart tracking. This is ideal for large projects that move a lot.
    # For any third-party modules, set the flow before making the function call.
    logger_flowchart = logging.getLogger('flowchart')
    logger_flowchart.debug(f'Flowchart --> Function: {get_function_name()}')

    try:
        type_check(duplicates, list,)
        if match_index:
            type_check(match_index, int)
        type_check(grouped, bool)
    except FTypeError:
        raise

    formatted_duplicates = '  - duplicates (list):' + str('\n        - ' + '\n        - '.join(map(str, duplicates)))
    if match_index:
        formatted_match_index = f'  - match_index (int):\n        - {match_index}'
    else:
        formatted_match_index = f'  - match_index (int):\n        - None'
    logger.debug(
        'Passing parameters:\n'
        f'{formatted_duplicates}\n'
        f'{formatted_match_index}\n'
        f'  - grouped (bool):\n        - {grouped}\n'
    )

    try:
        # Temporary storage for unique items.
        temp_unique_items = []
        # Stores duplicate list entries as dictionaries.
        # The key is the duplicate from the list and the value is the index.
        duplicate_list_dictionary = []

        for entry in duplicates:
            # Checks if the entry in the list is another list.
            # This allows lists to be in a list and be searched.
            if isinstance(entry, list) or isinstance(entry, tuple):
                # Checks a match_index is given to match a specific index in the list entry.
                if isinstance(match_index, int):
                    # Checks if the entry from the list exists in the "temp_unique_items" list. If not it gets added to the temp list.
                    # If the entry exists the entry will hit the elif statement and get all index points for the duplicates.
                    if entry[match_index] not in temp_unique_items:
                        # Adds the entry to the list.
                        temp_unique_items.append(entry[match_index])
                    # Checks if the duplicate entry already exists in the duplicate_list_dictionary list.
                    # This has to check if the 'duplicate_list_dictionary' is empty and if the duplicate list does not contain the entry.
                    # The two different "entry" searches are required in case the key is a string or an INT. A string would have a single quote and an INT would not.
                    elif bool(duplicate_list_dictionary) is False or f'\'value\': {entry[match_index]}' not in str(duplicate_list_dictionary) and f'\'value\': \'{entry[match_index]}\'' not in str(duplicate_list_dictionary):
                        # Loops through all entries in the list.
                        for index, value in enumerate(duplicates):
                            # Checks if the value from the list is equal to the discovered duplicate.
                            if value[match_index] == entry[match_index]:
                                # Adds the duplicate entry values and index
                                # The value will be the key and the index will be the value.
                                # This will allow the ease if finding all index points for a specific value.
                                duplicate_list_dictionary.append({'index': index, 'value': value})
                # No match_index given, so the entire list entry will be used for matching, so the entry will be converted to a string.
                else:
                    # Checks if the entry from the list exists in the "temp_unique_items" list. If not it gets added to the temp list.
                    # If the entry exists the entry will hit the elif statement and get all index points for the duplicates.
                    if str(entry) not in temp_unique_items:
                        # Adds the entry to the list.
                        temp_unique_items.append(str(entry))
                    # Checks if the duplicate entry already exists in the duplicate_list_dictionary list.
                    # This has to check if the 'duplicate_list_dictionary' is empty and if the duplicate list does not contain the entry.
                    # The two different "entry" searches are required in case the key is a string or an INT. A string would have a single quote and an INT would not.
                    elif bool(duplicate_list_dictionary) is False or f'\'value\': {str(entry)}' not in str(duplicate_list_dictionary) and f'\'value\': \'{str(entry)}\'' not in str(duplicate_list_dictionary):
                        # Loops through all entries in the list.
                        for index, value in enumerate(duplicates):
                            # Checks if the value from the list is equal to the discovered duplicate.
                            if str(value) == str(entry):
                                # Adds the duplicate entry values and index
                                # The value will be the key and the index will be the value.
                                # This will allow the ease if finding all index points for a specific value.
                                duplicate_list_dictionary.append({'index': index, 'value': value})
            # Standard strings in the list.
            else:
                # Checks if the entry from the list exists in the "temp_unique_items" list. If not it gets added to the temp list.
                # If the entry exists the entry will hit the elif statement and get all index points for the duplicates.
                if entry not in temp_unique_items:
                    # Adds the entry to the list.
                    temp_unique_items.append(entry)
                # Checks if the duplicate entry already exists in the duplicate_list_dictionary list.
                # This has to check if the 'duplicate_list_dictionary' is empty and if the duplicate list does not contain the entry.
                # The two different "entry" searches are required in case the key is a string or an INT. A string would have a single quote and an INT would not.
                elif bool(duplicate_list_dictionary) is False or f'\'value\': {entry}' not in str(duplicate_list_dictionary) and f'\'value\': \'{entry}\'' not in str(duplicate_list_dictionary):
                    # Loops through all entries in the list.
                    for index, value in enumerate(duplicates):
                        # Checks if the value from the list is equal to the discovered duplicate.
                        if value == entry:
                            # Adds the duplicate entry values and index
                            # The value will be the key and the index will be the value.
                            # This will allow the ease if finding all index points for a specific value.
                            duplicate_list_dictionary.append({'index': index, 'value': value})
    except Exception as exc:
        exc_args = {
            'main_message': 'A general failure occurred getting duplicate values the list.',
            'original_exception': exc,
        }
        raise FGeneralError(exc_args)
    else:
        # Checks that duplicates exist.
        if duplicate_list_dictionary:
            # Checks if the user enabled grouping.
            if grouped:

                try:
                    # Stores new grouped entries
                    grouped = {}
                    # Loops through each grouped entry.
                    for entry in duplicate_list_dictionary:
                        # Checks if the match_index is set to match a specific list index in the list entry.
                        if isinstance(match_index, int):
                            # Checks if the values being returned are a tuple.
                            # If tuple the matched_index will be used to set the key.
                            # This is required because single value will be a string and the index will only pull the first letter.
                            # Output Example: {'index': 0, 'value': ('ValueA', 'ValueB')}
                            if isinstance(entry['value'], tuple):
                                # Gets matching entries based on the "value" key and adds them to the grouped dictionary.
                                grouped[str(entry['value'][match_index])] = grouped.get(str(entry['value'][match_index]), [])
                                grouped[str(entry['value'][match_index])].append(entry)
                            # Means only one entry exists as the value, and the value type is a string.
                            # Output Example: {'index': 3, 'value': 'ValueB'}
                            else:
                                # Gets matching entries based on the "value" key and adds them to the grouped dictionary.
                                grouped[str(entry['value'])] = grouped.get(str(entry['value']), [])
                                grouped[str(entry['value'])].append(entry)
                        # Checks if no match_index exists, which matches the entire list entry.
                        # The list entry is converted to a string for the key.
                        elif not isinstance(match_index, int):
                            # Gets matching entries based on the "value" key and adds them to the grouped dictionary.
                            grouped[str(entry['value'])] = grouped.get(str(entry['value']), [])
                            grouped[str(entry['value'])].append(entry)
                        # Standard string element in the list.
                        else:
                            # Gets matching entries based on the "value" key and adds them to the grouped dictionary.
                            grouped[entry['value']] = grouped.get(entry['value'], [])
                            grouped[entry['value']].append(entry)
                except Exception as exc:
                    exc_args = {
                        'main_message': 'A general failure occurred grouping duplicate values.',
                        'original_exception': exc,
                    }
                    raise FGeneralError(exc_args)
                else:
                    # Returns grouped duplicates.
                    return grouped
            else:
                # Returns un-grouped duplicates.
                return duplicate_list_dictionary
        else:
            return None


def string_grouper(list_of_strings: list, grouping_value: Union[str, int, None], grouping_option: int, case_insensitive: bool = False) -> list:
    """
    String grouper will group a list of strings using three different options.

    Each option provides a different type of results, but covers any type of desired grouping.

    Args:
        list_of_strings (list):
        \t\\- A grouping of strings that need to get grouped.
        grouping_value (Union[str, int, None]):
        \t\\- A group value based on a character or positions.\\
        \t\t\\- Group Option 1 Example:\\
        \t\t\t\\- grouping_value = '-'\\
        \t\t\t\t\\- Result:
        \t\t\t\t\t\\- If the string is "Testing-1", the grouping\\
        \t\t\t\t\t   values would match on "Testing".\\
        \t\t\\- Group Option 2 Example:\\
        \t\t\t\\- grouping_value = 2\\
        \t\t\t\t\\- Result:\\
        \t\t\t\t\t\\- If the string is "Testing-1", the grouping\\
        \t\t\t\t\t   values would match on "Te".\\
        \t\t\\- Group Option 3 Example:\\
        \t\t\t\\- No value is required. Send None or a random\\
        \t\t\t  character as the parameter value.\\
        grouping_option (int):
        \t\\- A grouping option.
        \t\t\\- Option 1:
        \t\t\t\\- Similar Separator\\
        \t\t\t\t\\- Using this option will use the "grouping_value"\\
        \t\t\t\t   to group all like entries in the list together.\\
        \t\t\\- Option 2:
        \t\t\t\\- Character Position Number\\
        \t\t\t\t\\- Using this option will group all like entries in the\\
        \t\t\t\t   list together based on the number of character\\
        \t\t\t\t   positions entered.\\
        \t\t\\- Option 3:
        \t\t\t\\- Common String\\
        \t\t\t\t\\- Using this option will group all common strings in\\
        \t\t\t\t   the list together based on the last matching character.\\
        \t\t\t\t\t\\- Note1: The group_identifier may not be the same number\\
        \t\t\t\t\t\t       of characters based on the importing list.\\
        \t\t\t\t\t\\- Note2: Currently option3 does not support case\\
        \t\t\t\t\t\t       insensitive matching.
        case_insensitive (bool):
        \t\\- Enables case insensitive matching.\\
        \t\\- For example, lower and upper would be grouped into the same grouping.\\
        \t\\- Disabled by default.

    Raises:
        FTypeError (fexception):
        \t\\- The value '{list_of_strings}' is not in <class 'list'> format.
        FTypeError (fexception):
        \t\\- The value '{grouping_value}' is not in [<class 'str'>, <class 'int'>] format.
        FTypeError (fexception):
        \t\\- The value '{grouping_option' is not in <class 'int'> format.
        FTypeError (fexception):
        \t\\- The value '{case_insensitive}' is not in <class 'bool'> format.
        FTypeError (fexception):
        \t\\- The grouping_value sent for the grouping is not a string.
        FTypeError (fexception):
        \t\\- The grouping_value sent for the grouping is not a int.
        FGeneralError (fexception):
        \t\\- A general failure occurred while grouping the strings.

    Returns:
        list:\\
        \t\\- A list of grouped strings.

    Return Example:\\
    \t\\- [{'group_identifier': 'BA', 'grouping': ['BA-IDF1', 'BA-IDF2', 'BA-IDF3', 'BA-MDF']},\\
    \t   {'group_identifier': 'CB', 'grouping': ['CB-IDF0', 'CB-IDF1', 'CB-MDF']},\\
    \t   {'group_identifier': 'CE', 'grouping': ['CE-BUSLABOFF', 'CE-IDF-Band']},\\
    \t   {'group_identifier': 'CI', 'grouping': ['CI-MDF1']},\\
    \t   {'group_identifier': 'DH', 'grouping': ['DH-IDF1', 'DH-IDF2', 'DH-MDF']},\\
    \t   {'group_identifier': 'GH', 'grouping': ['GH-IDF0-RM113', 'GH-IDF1-RM161', 'GH-MDF-RM113']}]
    """
    logger = logging.getLogger(__name__)
    logger.debug(f'=' * 20 + get_function_name() + '=' * 20)
    # Custom flowchart tracking. This is ideal for large projects that move a lot.
    # For any third-party modules, set the flow before making the function call.
    logger_flowchart = logging.getLogger('flowchart')
    logger_flowchart.debug(f'Flowchart --> Function: {get_function_name()}')

    try:
        type_check(list_of_strings, list)
        if grouping_value:
            type_check(grouping_value, [str, int])
        type_check(grouping_option, int)
        type_check(case_insensitive, bool)
    except FTypeError:
        raise

    formatted_list_of_strings = '  - list_of_strings (list):' + str('\n        - ' + '\n        - '.join(map(str, list_of_strings)))
    if grouping_value:
        formatted_grouping_value = f'  - grouping_value (str or int or None):\n        - {grouping_value}'
    else:
        formatted_grouping_value = f'  - grouping_value (str or int or None):\n        - None'

    logger.debug(
        'Passing parameters:\n'
        f'{formatted_list_of_strings}\n'
        f'{formatted_grouping_value}\n'
        f'  - grouping_option (int):\n        - {grouping_option}\n'
        f'  - case_insensitive (bool):\n        - {case_insensitive}\n'
    )

    logger.debug(f'Starting string grouping with the following list of strings: {list_of_strings}')

    try:
        # Checks if any "None" entries exist.
        if None in list_of_strings:
            logger.debug(f'The list of strings contains \"None\" string entries. The \"None\" entries have been removed')
            # Removes any "None" entries from the list.
            list_of_strings = list(filter(None, list_of_strings))
        # Make sure that the list is greater than or equal to 2.
        if len(list_of_strings) >= 2:
            # Holds grouped values from the list.
            grouping = []
            case_lower = None
            case_upper = None
            # Checks if the sort should be based on case.
            # Currently option 3 does not support case insensitive matching. This only allows option 1 and 2.
            if case_insensitive and grouping_option != 3:
                upper_count = 0
                lower_count = 0
                # Loops through every string in the list to check for common case (ex: A or a) to determine sort.
                for string in list_of_strings:
                    # Checks case and increases count.
                    if string.isupper():
                        upper_count += 1
                    elif string.islower():
                        lower_count += 1
                # Checks the difference between the upper and lower count to determine the sort based on the common case. Tie goes to Upper.
                if upper_count > lower_count:
                    list_of_strings = sorted(list_of_strings, key=str.upper)
                    case_upper = True
                elif lower_count > upper_count:
                    list_of_strings = sorted(list_of_strings, key=str.lower)
                    case_lower = True
                elif upper_count == lower_count:
                    list_of_strings = sorted(list_of_strings, key=str.upper)
                    case_upper = True
                else:
                    list_of_strings.sort()
            else:
                list_of_strings.sort()

            # Groups based on the users group option.
            if grouping_option == 1:
                # This section groups based on a character. If the string is "Testing-1" and the matching character was -, the grouping values would match on "Testing".
                # Checks that the grouping_value is a string.
                if isinstance(grouping_value, str):
                    # Loops through a list of strings and splits based on the split number. The split number will create a grouping, and provide the split output for each grouping.
                    if case_upper:
                        for j, i in groupby(list_of_strings, lambda a_string: a_string.upper().split(grouping_value)[0]):
                            # Appends the grouping from groupby to the list in in dictionary format.
                            grouping.append({'group_identifier': j, 'grouping': list(i)})
                    elif case_lower:
                        for j, i in groupby(list_of_strings, lambda a_string: a_string.lower().split(grouping_value)[0]):
                            # Appends the grouping from groupby to the list in in dictionary format.
                            grouping.append({'group_identifier': j, 'grouping': list(i)})
                    else:
                        for j, i in groupby(list_of_strings, lambda a_string: a_string.split(grouping_value)[0]):
                            # Appends the grouping from groupby to the list in in dictionary format.
                            grouping.append({'group_identifier': j, 'grouping': list(i)})
                else:
                    exc_args = {
                        'main_message': 'The grouping_value sent for the grouping is not a string.',
                        'expected_result': """<class 'str'>""",
                        'returned_result': type(grouping_value),
                    }
                    raise FTypeError(exc_args)
            elif grouping_option == 2:
                # This section groups based on a character number. If the string is "Testing" and the number was 3, the grouping values would match on "Tes".
                # Checks that the grouping_value is a number.
                if isinstance(grouping_value, int):
                    if case_upper:
                        # Loops through a list of strings and splits based on the split number. The split number will create a grouping, and provide the split output for each grouping.
                        for j, i in groupby(list_of_strings, lambda a_string: [a_string[index: index + grouping_value].upper() for index in range(0, len(a_string), grouping_value)][0]):
                            # Appends the grouping from groupby to the list in in dictionary format.
                            grouping.append({'group_identifier': j, 'grouping': list(i)})
                    elif case_lower:
                        # Loops through a list of strings and splits based on the split number. The split number will create a grouping, and provide the split output for each grouping.
                        for j, i in groupby(list_of_strings, lambda a_string: [a_string[index: index + grouping_value].lower() for index in range(0, len(a_string), grouping_value)][0]):
                            # Appends the grouping from groupby to the list in in dictionary format.
                            grouping.append({'group_identifier': j, 'grouping': list(i)})
                    else:
                        # Loops through a list of strings and splits based on the split number. The split number will create a grouping, and provide the split output for each grouping.
                        for j, i in groupby(list_of_strings, lambda a_string: [a_string[index: index + grouping_value] for index in range(0, len(a_string), grouping_value)][0]):
                            # Appends the grouping from groupby to the list in in dictionary format.
                            grouping.append({'group_identifier': j, 'grouping': list(i)})
                else:
                    exc_args = {
                        'main_message': 'The grouping_value sent for the grouping is not a int.',
                        'expected_result': """<class 'int'>""",
                        'returned_result': type(grouping_value),
                    }
                    raise FTypeError(exc_args)
            elif grouping_option == 3:
                # This compare can have some complex checks because it has to check previous entries and make choices based on previous and current groupings.
                # The section of code is split by two different loops. The primary loop goes through each string. The sub-string loops and checks character by character between the previous string and current string.
                # All processing is done with the mindset that the current entry is always compared with the previous entry. The compare is based on alphabetical order.
                # Loops through all raw string imports to compare.
                for raw_string_loop_tracker, string in enumerate(list_of_strings):
                    # Checks if the length of the raw string is equal to the raw_string_loop_tracker + 1. This allows a clean exit without the list going out of index.
                    if len(list_of_strings) != raw_string_loop_tracker + 1:
                        logger.debug(f'Comparing \"{string}\" with \"{list_of_strings[raw_string_loop_tracker + 1]}\"')
                        # Loops through each character in the main string entry.
                        for character_loop_tracker, character in enumerate(string):
                            logger.debug(f'Checking character position {character_loop_tracker}')
                            # Checks if the character from the main entry matches the character in the next raw string in the list.
                            # + 1 so the first string entry will compare with this starting entry.
                            if character == list_of_strings[raw_string_loop_tracker + 1][character_loop_tracker]:
                                logger.debug(f'Match at character position {character_loop_tracker}')
                            # No match
                            elif character != list_of_strings[raw_string_loop_tracker + 1][character_loop_tracker]:
                                logger.debug(f'No Match at character position {character_loop_tracker}')
                                # Gets matching characters. Character get starts at 1, so need to -1.
                                match_characters = string[0:character_loop_tracker]
                                logger.debug(f'Matched characters = {match_characters}')
                                if match_characters:
                                    # Checks if no groupings have been added.
                                    if not grouping:
                                        # Adds the initial grouping.
                                        grouping.append({'group_identifier': match_characters, 'grouping': [string, list_of_strings[raw_string_loop_tracker + 1]]})
                                    else:
                                        # Gets the previous grouping identifier.
                                        previous_group_identifier = grouping[-1].get('group_identifier')
                                        # Checks if the previous grouping identifier is the same, so the string can be joined into the same group entry.
                                        if match_characters == previous_group_identifier:
                                            logger.debug(f'Previous grouping matches. {previous_group_identifier} = {match_characters}')
                                            # Inserts the compared string to the previous grouping because it has the same matching group identifier.
                                            grouping[-1].get('grouping').insert(len(grouping) + 1, list_of_strings[raw_string_loop_tracker + 1])
                                        else:
                                            # Checks if a single string entry. This is required because a single string entry will have the same group_identifier name as the string until the next entry is matched.
                                            if len(grouping[-1].get('grouping')) == 1:
                                                logger.debug(f'Previous grouping is a single entry and has matching characters. \"{match_characters}\" in \"{previous_group_identifier}\"')
                                                # Checks if the current match_characters are in the previous_group_identifiers name.
                                                # Note: The previous_group_identifiers name will be the full name of the string, so the match has to be the other way for detection.
                                                if match_characters in previous_group_identifier:
                                                    logger.debug('Merging previous entry with the current entry')
                                                    # Remove previous entry and insert the grouping from the previous entry with the current string group.
                                                    #
                                                    #
                                                    # Gets the previous grouping string. Removes the list brackets and quotes.
                                                    previous_group_string = str(grouping[-1].get('grouping')).strip('][').strip("'")

                                                    # Removes the previous group entry because it will not be merged with the current string group.
                                                    grouping.remove(grouping[-1])
                                                    # Adds the new grouping to the list with the previous group added as well.
                                                    grouping.append({'group_identifier': match_characters, 'grouping': [previous_group_string, list_of_strings[raw_string_loop_tracker + 1]]})
                                                else:
                                                    logger.debug(f'Previous grouping do not match. {previous_group_identifier} != {match_characters}')
                                                    # Adds the new grouping to the list.
                                                    grouping.append({'group_identifier': match_characters, 'grouping': [list_of_strings[raw_string_loop_tracker + 1]]})
                                            # Compares the previous group to the match to make sure the groupings are the same. The previous_grouping_identifier could contain more characters than the current match, so this flow is required.
                                            elif previous_group_identifier in match_characters:
                                                logger.debug(f'Previous grouping has multiple strings grouped and the group_identifier has the same characters as the match group. \"{match_characters}\" in \"{previous_group_identifier}\"')
                                                # Inserts the compared string to the previous grouping because it has the same matching group identifier.
                                                grouping[-1].get('grouping').insert(len(grouping) + 1, list_of_strings[raw_string_loop_tracker + 1])
                                            else:
                                                logger.debug(f'Previous grouping do not match. {previous_group_identifier} != {match_characters}')
                                                # No match occurred with the previous entry, which means this entry is a completely new entry, so the "group_identifier" will be the name of the string. This will adjust if the next string has a match.
                                                # Note: If no match is made the group_identifier will always be the name of the string because it had nothing to compare itself against.
                                                # Adds the new grouping to the list.
                                                grouping.append({'group_identifier': list_of_strings[raw_string_loop_tracker + 1], 'grouping': [list_of_strings[raw_string_loop_tracker + 1]]})
                                else:
                                    logger.debug('No Matching Characters Found')

                                    # Checks if entries have been added to the list. No entries means the starting entry needs added.
                                    if not grouping:
                                        # Adds the starting entry and the next entry because neither of these entries matched on startup.
                                        grouping.append({'group_identifier': string, 'grouping': [string]})
                                        grouping.append({'group_identifier': list_of_strings[raw_string_loop_tracker + 1], 'grouping': [list_of_strings[raw_string_loop_tracker + 1]]})
                                    else:
                                        # Note: If no match is made the group_identifier will always be the name of the string because it had nothing to compare itself against.
                                        # Adds the new grouping to the list.
                                        grouping.append({'group_identifier': list_of_strings[raw_string_loop_tracker + 1], 'grouping': [list_of_strings[raw_string_loop_tracker + 1]]})

                                # Breaks the lop because no additional characters match.
                                break

                            # Checks if the main string is shorter than the main string. This means no match occurred, so the group_identifier for this entry is main entry.
                            if character_loop_tracker == len(string) - 1:
                                logger.debug('Compare string is longer than the main string')
                                grouping.append({'group_identifier': string, 'grouping': [string]})
                                grouping.append({'group_identifier': list_of_strings[raw_string_loop_tracker + 1], 'grouping': [list_of_strings[raw_string_loop_tracker + 1]]})

            # Returns the list of dictionaries.
            # Return Example: grouping = [{'group_identifier': 'JJ-MDF-9200-1_2', 'grouping': ['JJ-MDF-9200-1_2']},
            #                             {'group_identifier': 'KV-IDF', 'grouping': ['KV-IDF1-9200-1_2', 'KV-IDF2-9200-1_2']},
            #                             {'group_identifier': 'KV-MDF', 'grouping': ['KV-MDF-9200-1_2', 'KV-MDF1-9200-1_2']},
            #                             {'group_identifier': 'KZV-MDF1-9200-1_2', 'grouping': ['KZV-MDF1-9200-1_2']},
            #                             {'group_identifier': 'TI-IDF', 'grouping': ['TI-IDF1-9200-1_2', 'TI-IDF2-9200-1_2']}]
            return grouping
        else:
            return None
    except FTypeError as exc:
        raise
    except Exception as exc:
        exc_args = {
            'main_message': 'A general failure occurred while grouping the strings.',
            'original_exception': exc,
        }
        raise FGeneralError(exc_args)


def find_longest_common_substring(string1: str, string2: str) -> str:
    """
    This function finds the longest substring between two different strings.

    Args:
        string1 (string):
        \t\\- string to compare against string2
        string2 (string):
        \t\\- string to compare against string1

    Raises:
        FTypeError (fexception):
        \t\\- The value '{string1}' is not in <class 'str'> format.
        FTypeError (fexception):
        \t\\- The value '{string2}' is not in <class 'str'> format.
        FGeneralError (fexception):
        \t\\- A general exception occurred interating the two strings.

    Returns:
        str:\\
        \t\\- returns the string up to the point the characters no longer match.
    """
    logger = logging.getLogger(__name__)
    logger.debug(f'=' * 20 + get_function_name() + '=' * 20)
    # Custom flowchart tracking. This is ideal for large projects that move a lot.
    # For any third-party modules, set the flow before making the function call.
    logger_flowchart = logging.getLogger('flowchart')
    logger_flowchart.debug(f'Flowchart --> Function: {get_function_name()}')

    try:
        type_check(string1, str)
        type_check(string2, str)
    except FTypeError:
        raise

    logger.debug(
        'Passing parameters:\n'
        f'  - string1 (str):\n        - {string1}\n'
        f'  - string2 (str):\n        - {string2}\n'
    )

    def _iter():
        for a, b in zip(string1, string2):
            if a == b:
                yield a
            else:
                return

    try:
        if ''.join(_iter()):
            substring = ''.join(_iter())
        else:
            substring = None
    except Exception as exc:
        exc_args = {
            'main_message': 'A general exception occurred interating the two strings.',
            'original_exception': exc,
        }
        raise FGeneralError(exc_args)
    else:
        return substring


def user_choice_character_grouping(list_of_strings: list) -> list:
    """
    Groups a list of characters based on the users choices.

    This is a user interaction function.

    The user can group based on a similar character or character position.

    Args:
        list_of_strings (list):
        \t\\- A list of strings that need to get grouped.

    Raises:
        FTypeError (fexception):
        \t\\- The value '{list_of_strings}' is not in <class 'list'> format.
        FGeneralError (fexception):
        \t\\- A general exception occurred when getting the user choice character grouping.

    Returns:
        list:\\
        \t\\- A list of grouped characters.
    """
    logger = logging.getLogger(__name__)
    logger.debug(f'=' * 20 + get_function_name() + '=' * 20)
    # Custom flowchart tracking. This is ideal for large projects that move a lot.
    # For any third-party modules, set the flow before making the function call.
    logger_flowchart = logging.getLogger('flowchart')
    logger_flowchart.debug(f'Flowchart --> Function: {get_function_name()}')

    try:
        type_check(list_of_strings, list)
    except FTypeError:
        raise

    formatted_list_of_strings = '  - list_of_strings (list):' + str('\n        - ' + '\n        - '.join(map(str, list_of_strings)))
    logger.debug(
        'Passing parameters:\n'
        f'{formatted_list_of_strings}\n'
    )

    logger.debug(f'Passing parameters [list_of_strings] (list):' + '\n    - ' + '\n    - '.join(map(str, list_of_strings)))

    # Sets grouping value to None to prevent any reference errors on a retry.
    groupings = None

    try:
        while True:
            # ############################################################
            # ###########Requests Options and Gets Groupings##############
            # ############################################################
            print('')
            print('A hostname comparison is about to take place to group devices based on similar naming into the IP Network Design spreadsheets. Please continue to select how many character positions you would like to search.')
            continue_choice = input('Are you ready to continue? \n \n1 - Yes \n2 - No \n \nEnter Selection Number: ')
            # Adds console blank lines.
            print('')
            print('')
            if int(continue_choice) == 1:
                character_choice = input('Do you wish to group based on a character position number or a similar separator? \n \n1 - Similar Separator \n2 - Character Position Number  \n \nEnter Select Number: ')
                if int(character_choice) == 1:
                    character_separater = str(input('Enter the similar separater character: '))
                    # Adds console blank lines.
                    print('')
                    print('')
                    # Checks the the user entered a number.
                    if isinstance(character_separater, str):
                        # Calls function to group the list of strings.
                        groupings = string_grouper(list_of_strings, character_separater, 1, True)
                    else:
                        print('Error: You did not enter a string. Please retry again.')
                        print('')
                        print('')
                        # Continues to top of loop to prompt user again
                elif int(character_choice) == 2:
                    character_search_number = input('Enter the character position grouping number: ')
                    # Adds console blank lines.
                    print('')
                    print('')
                    # Checks the the user entered a number.
                    if character_search_number.isdigit():
                        # Converts string to int.
                        character_search_number = int(character_search_number)
                        # Calls function to group the list of strings.
                        groupings = string_grouper(list_of_strings, character_search_number, 2, True)
                    else:
                        print('Error: You did not enter a number. Please retry again.')
                        print('')
                        print('')
                        # Continues to top of loop to prompt user again
            elif int(continue_choice) == 2:
                print('You choose not to continue the hostname comparison. Exiting....')
                exit()

            # ############################################################
            # #################Offers Grouping Overview###################
            # ############################################################
            # Checks if groupings exist before continuing.
            # No grouping means the user choose to retry.
            if groupings:
                character_grouping_overview = input('Would you like to see the new names before continuing? \n \n1 - Yes \n2 - No  \n \nEnter Select Number: ')
                if int(character_grouping_overview) == 1:
                    print('The grouping output will show the grouping identifier and the grouped devices. The grouping identifier will be used for the IP Network Design spreadsheet.')
                    print('')
                    print('')
                    # Loops through output to show the user the results
                    for grouping in groupings:
                        # Sets variables for easier usage.
                        group_identifier = grouping.get('group_identifier')
                        grouping = grouping.get('grouping')
                        print(f'Grouping Identifier = {group_identifier} >>>>> Grouping = {grouping}')

                    print('')
                    print('')
                    grouping_acceptance = input('Are you satisfied with the new names that will use for the IP Network Design spreadsheet? \n \n1 - Yes \n2 - No \n3 - Quit  \n \nEnter Select Number: ')
                    print('')
                    print('')
                    if int(grouping_acceptance) == 1:
                        # Returns the groupings
                        return groupings
                    elif int(grouping_acceptance) == 2:
                        print('User choose to retry character group position')
                        # Continues to top of loop to prompt user again
                    elif int(grouping_acceptance) == 3:
                        print('You choose to quit. Exiting....')
                        exit()
                elif int(character_grouping_overview) == 2:
                    # Returns the groupings
                    return groupings
    except Exception as exc:
        exc_args = {
            'main_message': 'A general exception occurred when getting the user choice character grouping.',
            'original_exception': exc,
        }
        raise FGeneralError(exc_args)


def clean_non_word_characters(string: str) -> str:
    """
    This function will remove any non-word hex characters from any passing string.

    Strings without non-word hex will be passed through without any errors.

    Args:
        string (str):
        \t\\- A string with non-word hex characters.

    Raises:
        FTypeError (fexception):
        \t\\- The value '{string}' is not in <class 'str'> format.
        FValueError (fexception):
        \t\\- The string ({string}) with non-word characters did not clean.

    Returns:
        str:\\
        \t\\- A cleaned string with valid only words.
    """
    logger = logging.getLogger(__name__)
    logger.debug(f'=' * 20 + get_function_name() + '=' * 20)
    # Custom flowchart tracking. This is ideal for large projects that move a lot.
    # For any third-party modules, set the flow before making the function call.
    logger_flowchart = logging.getLogger('flowchart')
    logger_flowchart.debug(f'Flowchart --> Function: {get_function_name()}')

    try:
        type_check(string, str)
    except FTypeError:
        raise

    logger.debug(
        'Passing parameters:\n'
        f'  - string (str):\n        - {string}\n'
    )

    # Some Python returned information will return with trailing hex characters (non-words). These are unescaped control characters, which is what Python displays using hexadecimal notation.
    # This expression will remove the hex characters. It can be written with either [^\x20-\x7e] or [^ -~].*
    # Note: When viewing non-word characters it can very from console or logging. You may see output similar BTW-N5K\x06 or BTW-N5K♠ or BTW-N5K\u00006 or BTW-N5K.
    # Example1:
    #   - Input: BTW-N5K\x06
    #   - Output: BTW-N5K
    cleaned_string = re.sub(r'[^ -~].*', '', string)
    encoded_string = cleaned_string.encode('ascii', 'ignore')
    if '\\x' in str(encoded_string):
        exc_args = {
            'main_message': f'The string ({string}) with non-word characters did not clean.',
            'expected_result': 'The string should not have contained any hex characters.',
            'returned_result': encoded_string,
        }
        raise FValueError(exc_args)
    else:
        # Checks if the lengths are different from the parameter string and cleaned string to know if the string contained non-word values.
        if len(string) > len(cleaned_string):
            logger.debug(f'The string was cleaned of all non-word characters. Set Value (str):\n    - Original Value: {string}\n    - Cleaned Value: {cleaned_string}')
        else:
            logger.debug(f'The string did not contain any non-word characters. No change required.')
        return cleaned_string
