#!interpreter

"""
This module is designed to offer data structure functions. These data structures include lists, tuples, sets, and dictionaries.
"""
# Built-in/Generic Imports
import os
import logging
import traceback

__author__ = 'IncognitoCoding'
__copyright__ = 'Copyright 2021, data_structure_director'
__credits__ = ['IncognitoCoding']
__license__ = 'GPL'
__version__ = '1.3'
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