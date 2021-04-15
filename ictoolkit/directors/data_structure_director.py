#!interpreter

"""
This module is designed to offer data structure functions. These data structures include lists, tuples, sets, and dictionaries.
"""
# Built-in/Generic Imports
import os
import logging
import traceback

__author__ = 'IncognitoCoding'
__copyright__ = 'Copyright 2021, dict_director'
__credits__ = ['IncognitoCoding']
__license__ = 'GPL'
__version__ = '1.0'
__maintainer__ = 'IncognitoCoding'
__status__ = 'Development'


def remove_duplicate_dict_values_in_list(list_dictionary, element_number=None):
    """
    Removes duplicate values in a dictionary within a list and returns the same list minus duplicates.
    
    This function will convert a list of dictionaries into a list of tuples that contains items of the dictionary for duplicate removal.

    Dictionaries in a list are sometimes needed to be sorted based off a specific element in the dictionary entry. This function offers the ability to choose which element number to use for matching
    or match the entire dictionary element.

    Args:
        list_dictionary (list): dictionary with duplicate values in a list
        element_number (int or None): enter the dictionary element number when matching based on a specific dictionary element in the dictionary line. Enter None when a full match is needed.
            
            Element Number Example: [{'search_entry': '|Error|', 'found_entry': 'the entry found'}, {'search_entry': '|Warning|', 'found_entry': 'the entry found'}]
                - Element Number 'None' would check match on ('search_entry': '|Error|', 'found_entry': 'the entry found') & ('search_entry': '|Warning|', 'found_entry': 'the entry found')
                    - No match would occur, and both entries would dictionary entries would return.
                        - Return: [{'search_entry': '|Error|', 'found_entry': 'the entry found'}, {'search_entry': '|Warning|', 'found_entry': 'the entry found'}]
                - Element Number 1 would check match on ('found_entry': 'the entry found') & ('found_entry': 'the entry found')
                    - A match would occur, and only one dictionary entry would return.
                        - Return: [{'search_entry': '|Error|', 'found_entry': 'the entry found'}]
    Returns:
        list: dictionaries in a list with duplicate values removed
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
        raise ValueError(f'A failure occurred removing duplicates from the dictionary in the list, {err}, Originating error on line {traceback.extract_stack()[-1].lineno} in <{__name__}>')

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

    except KeyError as err:
        raise ValueError(f'A failure occurred getting duplicate values the list, The searching key ({key}) does not exist in the dictionary, Originating error on line {traceback.extract_stack()[-1].lineno} in <{__name__}>')
    except Exception as err: 
        raise ValueError(f'A failure occurred getting duplicate values from the key ({key}) in the list_dictionary, {err}, Originating error on line {traceback.extract_stack()[-1].lineno} in <{__name__}>')
    
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
                    raise ValueError(f'A failure occurred grouping duplicate values, {err}, Originating error on line {traceback.extract_stack()[-1].lineno} in <{__name__}>')
                
                else:

                    # Returns grouped duplicates.
                    return grouped

            else:

                # Returns un-grouped duplicates.
                return duplicate_list_dictionary

        else:
            return None


def get_list_duplicates(duplicates, grouped=False):
    """
    Finds duplicate entries in the list return the value and index points. Duplicates can be either un-grouped or grouped. Default is ungrouped. 
    Returning both the duplicate and original list index points allows any modification or additional data search when the duplicates return.

    Calling Example List: ['ValueA', 'ValueA', 'ValueA', 'ValueB', 'ValueB', 'ValueC', 'ValueD']

    Args:
        duplicates (list): list with duplicates
        grouped (bool): enables grouping of duplicate values. Disabled by default

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
        raise ValueError(f'A failure occurred getting duplicate values the list, {err}, Originating error on line {traceback.extract_stack()[-1].lineno} in <{__name__}>')

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
                    raise ValueError(f'A failure occurred grouping duplicate values, {err}, Originating error on line {traceback.extract_stack()[-1].lineno} in <{__name__}>')
                
                else:

                    # Returns grouped duplicates.
                    return grouped

            else:

                # Returns un-grouped duplicates.
                return duplicate_list_dictionary
        
        else:
            return None
