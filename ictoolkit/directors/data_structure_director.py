#!interpreter

"""
This module is designed to offer data structure functions. These data structures include lists, tuples, sets, and dictionaries.
"""
# Built-in/Generic Imports
import os
import logging
import traceback
from itertools import groupby

__author__ = 'IncognitoCoding'
__copyright__ = 'Copyright 2021, data_structure_director'
__credits__ = ['IncognitoCoding']
__license__ = 'GPL'
__version__ = '1.4'
__maintainer__ = 'IncognitoCoding'
__status__ = 'Development'


def remove_duplicate_dict_values_in_list(list_dictionary, element_number=None):
    """
    Removes duplicate values in a dictionary within a list and returns the same list minus duplicates.
    
    This function will convert a list of dictionaries into a list of tuples that contains items of the dictionary for duplicate removal.

    A list of dictionaries are sometimes needed to be sorted based off a specific element in the dictionary entry. This function offers the ability to choose which element number to use for matching
    or match the entire dictionary element.
    - Element Number Example: [{'search_entry': '|Error|', 'found_entry': 'the entry found'}, {'search_entry': '|Warning|', 'found_entry': 'the entry found'}]
        - Element Number 'None' would check match on ('search_entry': '|Error|', 'found_entry': 'the entry found') & ('search_entry': '|Warning|', 'found_entry': 'the entry found')
            - No match would occur, and both entries would dictionary entries would return.
                - Return: [{'search_entry': '|Error|', 'found_entry': 'the entry found'}, {'search_entry': '|Warning|', 'found_entry': 'the entry found'}]
        - Element Number 1 would check match on ('found_entry': 'the entry found') & ('found_entry': 'the entry found')
            - A match would occur, and only one dictionary entry would return.
                - Return: [{'search_entry': '|Error|', 'found_entry': 'the entry found'}]

    Raises:
        ValueError: A failure occurred removing duplicates from the dictionary in the list.

    Args:
        list_dictionary (list): A dictionary with duplicate values in a list.
        element_number (int or None): Enter the dictionary element number when matching based on a specific dictionary element in the dictionary line. Enter None when a full match is needed.
            
    Returns:
        list: A list of dictionars with duplicate values removed.
    """
    try:

        # Holds temporoary found elements for comparison.
        element_found = set()
        # Stores the revised list that does not contain any duplicates.
        revised_list = []

        # Loops through each dictionary in the list
        for dictionary_in_list in list_dictionary:
            # Checks if section number is being used for matching or a full match is being used.
            if element_number == None:
                # Used tuple because it can be hased, which allows removal using set.
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
                # Used tuple because it can be hased, which allows removal using set.
                # This will convert the dictionaries in the list to tuples that contains the dictionaries.
                # No sort is added here because sort will break the element number order.
                items_of_dictionary = tuple(dictionary_in_list.items())
                # Checks if dictionary element section does not match previous entries.
                if items_of_dictionary[element_number] not in element_found:
                    # New element found and adding to set.
                    element_found.add(items_of_dictionary[element_number])

                    # Adds the full dictionary_in_list to the list because it is not a duplicate.
                    revised_list.append(dictionary_in_list)
    except Exception as err: 
        error_message = (
            f'A failure occurred removing duplicates from the dictionary in the list.\n\n' +
            (('-' * 150) + '\n') + (('-' * 65) + 'Additional Information' + ('-' * 63) + '\n') + (('-' * 150) + '\n') +
            f'{err}\n\n'
            f'Originating error on line {traceback.extract_stack()[-1].lineno} in <{__name__}>\n' +
            (('-' * 150) + '\n') * 2 
        )   
        raise ValueError(error_message)
    else:
        return revised_list


def get_list_of_dicts_duplicates(key, list_dictionary, grouped=False):
    """
    Finds duplicate dictionary values in the list using the key and return the value and index points. Duplicates can be either un-grouped or grouped. Default is ungrouped. 
    Returning both the duplicate and original list index points allows any modification or additional data search when the duplicates return.

    A key is required to find all duplicates for that key.

    Calling Example List of Dictionaries: [{'key1': 'ValueA'}, {'key1': 'ValueA'}, {'key1': 'ValueA'}, {'key1': 'ValueB'}, {'key1': 'ValueB'}, {'key1': 'ValueC'}, {'key1': 'ValueD'}]

    Args:
        key (str): the dictionary key that needs to get all duplicate values assigned to that ke
        list_dictionary (list): dictionary with duplicate values in a list
        grouped (bool): enables grouping of duplicate values. Disabled by default

    Raises:
        ValueError: A failure occurred getting duplicate values the list.
        ValueError: A failure occurred getting duplicate values from the key ({key}) in the list_dictionary.
        ValueError: A failure occurred grouping duplicate values.

    Returns:
        list: the default return option is un-grouped duplicate values in dictionary format in a list
        dict: enabling grouped will return the duplicate values grouped in a dictionary with individual nested groupings
        None: if no duplicates are detected, a value of "None" will be returned

        Return Example (Un-Grouped): [{'index': 0, 'value': 'ValueA'}, {'index': 1, 'value': 'ValueA'}, {'index': 2, 'value': 'ValueA'}, {'index': 3, 'value': 'ValueB'}, {'index': 4, 'value': 'ValueB'}]
        Return Example (Grouped): {'ValueA': [{'index': 0, 'value': 'ValueA'}, {'index': 1, 'value': 'ValueA'}, {'index': 2, 'value': 'ValueA'}], 'ValueB': [{'index': 3, 'value': 'ValueB'}, {'index': 4, 'value': 'ValueB'}]}
    """
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
            elif bool(duplicate_list_dictionary) == False or f'\'value\': {entry}' not in str(duplicate_list_dictionary) and f'\'value\': \'{entry}\'' not in str(duplicate_list_dictionary):
                # Loops through all entries in the list.
                for index, value in enumerate(duplicates_of_key):
                    # Checks if the value from the list is equal to the discovered duplicate.
                    if value == entry:
                        # Adds the duplicate entry values and index
                        # The value will be the key and the index will be the value.
                        # This will allow the ease if finding all index points for a specific value.
                        duplicate_list_dictionary.append({'index': index, 'value': value})
    except KeyError:
        error_message = (
            'A failure occurred getting duplicate values the list.\n' +
            (('-' * 150) + '\n') + (('-' * 65) + 'Additional Information' + ('-' * 63) + '\n') + (('-' * 150) + '\n') +
            'Expected Result:\n'
            f'  - The searching key ({key}) existing in the dictionary\n\n'
            'Returned Result:\n'
            f'  - The searching key ({key}) does not existing in the dictionary ({list_dictionary})\n\n'
            f'Originating error on line {traceback.extract_stack()[-1].lineno} in <{__name__}>\n' +
            (('-' * 150) + '\n') * 2 
        )
        raise ValueError(error_message)
    except Exception as err: 
        error_message = (
            f'A failure occurred getting duplicate values from the key ({key}) in the list_dictionary.\n' +
            (('-' * 150) + '\n') + (('-' * 65) + 'Additional Information' + ('-' * 63) + '\n') + (('-' * 150) + '\n') +
            f'{err}\n\n'
            f'Originating error on line {traceback.extract_stack()[-1].lineno} in <{__name__}>\n' +
            (('-' * 150) + '\n') * 2 
        )
        raise ValueError(error_message)
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
                except Exception as err: 
                    error_message = (
                        f'A failure occurred grouping duplicate values.\n' +
                        (('-' * 150) + '\n') + (('-' * 65) + 'Additional Information' + ('-' * 63) + '\n') + (('-' * 150) + '\n') +
                        f'{err}\n\n'
                        f'Originating error on line {traceback.extract_stack()[-1].lineno} in <{__name__}>\n' +
                        (('-' * 150) + '\n') * 2 
                    )
                    raise ValueError(error_message)
                else:
                    # Returns grouped duplicates.
                    return grouped
            else:
                # Returns un-grouped duplicates.
                return duplicate_list_dictionary
        else:
            return None


def get_list_duplicates(duplicates, match_index=None, grouped=False):
    """
    Finds duplicate entries in the list return the value and index points. Duplicates can be either un-grouped or grouped. Default is ungrouped. 
    Returning both the duplicate and original list index points allows any modification or additional data search when the duplicates return.

    Calling Example List1: ['ValueA', 'ValueA', 'ValueA', 'ValueB', 'ValueB', 'ValueC', 'ValueD']
    Calling Example List2: [['ValueA', 'ValueB'], ['ValueA', 'ValueB'], ['ValueD', 'ValueB'], ['ValueB'], ['ValueB']
    Calling Example List3: [('ValueA', 'ValueB'), ('ValueA', 'ValueB'), ('ValueD', 'ValueB'), ('ValueB'), ('ValueB')]

    Args:
        duplicates (list): list with duplicate strings, a list with duplicate list index, a list with duplicate lists, a list with duplicate tuple index, and a list with duplicate tuple lists
        match_index (int): if the entries in the lists are a list the index can be set to match on a specific index in the list.
        grouped (bool): enables grouping of duplicate values. Disabled by default

    Raises:
        ValueError: A failure occurred getting duplicate values the list.
        ValueError: A failure occurred grouping duplicate values.

    Returns:
        list: the default return option is un-grouped duplicate values in dictionary format in a list
        dict: enabling grouped will return the duplicate values grouped in a dictionary with individual nested groupings
        None: if no duplicates are detected, a value of "None" will be returned

        Return Example (Un-Grouped): [{'index': 0, 'value': 'ValueA'}, {'index': 1, 'value': 'ValueA'}, {'index': 2, 'value': 'ValueA'}, {'index': 3, 'value': 'ValueB'}, {'index': 4, 'value': 'ValueB'}]
        Return Example (Grouped): {'ValueA': [{'index': 0, 'value': 'ValueA'}, {'index': 1, 'value': 'ValueA'}, {'index': 2, 'value': 'ValueA'}], 'ValueB': [{'index': 3, 'value': 'ValueB'}, {'index': 4, 'value': 'ValueB'}]}
    """  
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
                    elif bool(duplicate_list_dictionary) == False or f'\'value\': {entry[match_index]}' not in str(duplicate_list_dictionary) and f'\'value\': \'{entry[match_index]}\'' not in str(duplicate_list_dictionary):
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
                    elif bool(duplicate_list_dictionary) == False or f'\'value\': {str(entry)}' not in str(duplicate_list_dictionary) and f'\'value\': \'{str(entry)}\'' not in str(duplicate_list_dictionary):
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
                elif bool(duplicate_list_dictionary) == False or f'\'value\': {entry}' not in str(duplicate_list_dictionary) and f'\'value\': \'{entry}\'' not in str(duplicate_list_dictionary):
                    # Loops through all entries in the list.
                    for index, value in enumerate(duplicates):
                        # Checks if the value from the list is equal to the discovered duplicate.
                        if value == entry:
                            # Adds the duplicate entry values and index
                            # The value will be the key and the index will be the value.
                            # This will allow the ease if finding all index points for a specific value.
                            duplicate_list_dictionary.append({'index': index, 'value': value})

    except Exception as err: 
        error_message = (
            f'A failure occurred getting duplicate values the list.\n' +
            (('-' * 150) + '\n') + (('-' * 65) + 'Additional Information' + ('-' * 63) + '\n') + (('-' * 150) + '\n') +
            f'{err}\n\n'
            f'Originating error on line {traceback.extract_stack()[-1].lineno} in <{__name__}>\n' +
            (('-' * 150) + '\n') * 2 
        )
        raise ValueError(error_message)
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
                except Exception as err: 
                    error_message = (
                        f'A failure occurred grouping duplicate values.\n' +
                        (('-' * 150) + '\n') + (('-' * 65) + 'Additional Information' + ('-' * 63) + '\n') + (('-' * 150) + '\n') +
                        f'{err}\n\n'
                        f'Originating error on line {traceback.extract_stack()[-1].lineno} in <{__name__}>\n' +
                        (('-' * 150) + '\n') * 2 
                    )
                    raise ValueError(error_message)
                else:
                    # Returns grouped duplicates.
                    return grouped
            else:
                # Returns un-grouped duplicates.
                return duplicate_list_dictionary
        else:
            return None


def string_grouper(list_of_strings, grouping_value, grouping_option):   
    """
    String grouper will group a list of strings using three different options. Each option provides a different type of results, but covers any type of desired grouping.

    Args:
        list_of_strings (list): A grouping of strings that need to get grouped.
        grouping_value (str or int): A group value based on a character or positions.\\
            \- Group Option 1 Example: grouping_value = -. If the string is "Testing-1", the grouping values would match on "Testing".\\
            \- Group Option 2 Example: grouping_value = 2. Result: If the string is "Testing-1", the grouping values would match on "Te".\\
            \- Group Option 3 Example: No value is required. Send None or a random character as the parameter value.\\
        grouping_option (int): A grouping option.
            \- Option 1:
                \- Similar Separator\\
                    \- Using this option will use the "grouping_value" to group all like entries in the list together.\\
            \- Option 2:
                \- Character Position Number\\
                    \- Using this option will group all like entries in the list together based on the number of character positions entered.\\
            \- Option 3:
                \- Common String\\
                    \- Using this option will group all common strings in the list together based on the last matching character.\\
                        \- Note: The group_identifier may not be the same number of characters based on the importing list.\\

    Raises:
        ValueError: The value sent for the grouping is not a string.
        ValueError: The value sent for the grouping is not a number.
    
    Returns:
        list: A list of grouped strings.
            \- Return Output: [{'group_identifier': 'BA', 'grouping': ['BA-IDF1', 'BA-IDF2', 'BA-IDF3', 'BA-MDF']}, {'group_identifier': 'CB', 'grouping': ['CB-IDF0', 'CB-IDF1', 'CB-MDF']}, 
                                         \{'group_identifier': 'CE', 'grouping': ['CE-BUSLABOFF', 'CE-IDF-Band']}, {'group_identifier': 'CI', 'grouping': ['CI-MDF1']},\ 
                                         \{'group_identifier': 'DH', 'grouping': ['DH-IDF1', 'DH-IDF2', 'DH-MDF']}, {'group_identifier': 'GH', 'grouping': ['GH-IDF0-RM113', 'GH-IDF1-RM161', 'GH-MDF-RM113']}]
    """  
    logger = logging.getLogger(__name__)

    logger.debug(f'Starting string grouping with the following list of strings: {list_of_strings}')
    # Validates the sent strings are in a list.
    if isinstance(list_of_strings, list):
        # Checks if any "None" entries exist.
        if None in list_of_strings:
            logger.debug(f'The list of strings contains \"None\" string entries. The \"None\" entries have been removed')
            # Removes any "None" entries from the list.
            list_of_strings = list(filter(None, list_of_strings))
        # Make sure that the list is greater than or equal to 2.
        if len(list_of_strings) >= 2:
            # Holds grouped values from the list.
            grouping = []
            # Sort the list.
            # This is essential for grouping.
            list_of_strings.sort()

            # Groups based on the users group option.
            if grouping_option == 1:
                # This section groups based on a character. If the string is "Testing-1" and the matching character was -, the grouping values would match on "Testing".
                # Checks that the grouping_value is a string.
                if isinstance(grouping_value, str):
                    # Loops through a list of strings and splits based on the split number. The split number will create a grouping, and provide the split output for each grouping.
                    for j, i in groupby(list_of_strings, lambda a_string: a_string.split(grouping_value)[0]):
                        # Appends the grouping from groupby to the list in in dictionary format.
                        grouping.append({'group_identifier': j, 'grouping': list(i)})
                else:
                    error_message = (
                        f'The grouping_value sent for the grouping is not a string.\n' +
                        (('-' * 150) + '\n') + (('-' * 65) + 'Additional Information' + ('-' * 63) + '\n') + (('-' * 150) + '\n') +
                        'Expected Result:\n'
                        '  - string\n\n'
                        'Returned Result:\n'
                        f'  - grouping_value = {grouping_value}\n\n'
                        f'Originating error on line {traceback.extract_stack()[-1].lineno} in <{__name__}>\n' +
                        (('-' * 150) + '\n') * 2 
                    )
                    logger.error(error_message)
                    raise ValueError(error_message)
            elif grouping_option == 2:
                # This section groups based on a character number. If the string is "Testing" and the number was 3, the grouping values would match on "Tes".
                # Checks that the grouping_value is a number.
                if isinstance(grouping_value, int):
                    # Loops through a list of strings and splits based on the split number. The split number will create a grouping, and provide the split output for each grouping.
                    for j, i in groupby(list_of_strings, lambda a_string: [a_string[index : index + grouping_value] for index in range(0, len(a_string), grouping_value)][0]):
                        # Appends the grouping from groupby to the list in in dictionary format.
                        grouping.append({'group_identifier': j, 'grouping': list(i)})
                else:
                    error_message = (
                        f'The grouping_value sent for the grouping is not a int.\n' +
                        (('-' * 150) + '\n') + (('-' * 65) + 'Additional Information' + ('-' * 63) + '\n') + (('-' * 150) + '\n') +
                        'Expected Result:\n'
                        '  - int\n\n'
                        'Returned Result:\n'
                        f'  - grouping_value = {grouping_value}\n\n'
                        f'Originating error on line {traceback.extract_stack()[-1].lineno} in <{__name__}>\n' +
                        (('-' * 150) + '\n') * 2 
                    )
                    logger.error(error_message)
                    raise ValueError(error_message)
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
    else:
        list_of_strings = type(list_of_strings)
        error_message = (
            'The sent strings is not in list format.\n' +
            (('-' * 150) + '\n') + (('-' * 65) + 'Additional Information' + ('-' * 63) + '\n') + (('-' * 150) + '\n') +
            'Expected Result:\n'
            f'  - list_of_strings = list\n\n'
            'Returned Result:\n'
            f'  - list_of_strings = {list_of_strings}\n\n'
            f'Originating error on line {traceback.extract_stack()[-1].lineno} in <{__name__}>\n' +
            (('-' * 150) + '\n') * 2 
        )
        logger.error(error_message)
        raise ValueError(error_message)