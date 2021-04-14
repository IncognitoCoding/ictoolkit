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


def get_list_of_dicts_duplicates(key, list_dictionary):
    
    """
    Finds duplicate dictionary values in the list using the key and return the value and index points as a list with each duplicate in dictionary format.

    A key is required to find all duplicates for that key.

    The duplicate value will be the key, and the index point the duplicate gets found lists as the value. 

    Calling Example List of Dictionaries: [{'key1': 'ValueA'}, {'key1': 'ValueA'}, {'key1': 'ValueA'}, {'key1': 'ValueB'}, {'key1': 'ValueB'}]

    Args:
        key (str): the dictionary key that needs to get all duplicate values assigned to that ke
        list_dictionary (list): dictionary with duplicate values in a list

    Returns:
        list: duplicate values in dictionary format in a list

        Return Example: [{'ValueA': 0}, {'ValueA': 1}, {'ValueA': 2}, {'ValueB': 3}, {'ValueB': 4}]
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
            elif bool(duplicate_list_dictionary) == False or 'None' in str([a_dict.get(entry) for a_dict in duplicate_list_dictionary]):
                
                # Loops through all entries in the list.
                for index, value in enumerate(duplicates_of_key):
                    # Checks if the value from the list is equal to the discovered duplicate.
                    if value == entry:
                        
                        # Adds the duplicate entry values and index
                        # The value will be the key and the index will be the value.
                        # This will allow the ease if finding all index points for a specific value.
                        duplicate_list_dictionary.append({value: index})

    except Exception as err: 
        raise ValueError(f'A failure occurred getting duplicate values from the key ({key}) in the list_dictionary, {err}, Originating error on line {traceback.extract_stack()[-1].lineno} in <{__name__}>')

    else:

        return duplicate_list_dictionary


def get_list_duplicates(duplicates):
    """
    Finds all duplicate entries in a list and returns the value and index points as a list with each duplicate in dictionary format.

    The duplicate value will be the key, and the index point the duplicate gets found adds as the value. 

    Calling Example List: ['ValueA', 'ValueA', 'ValueA', 'ValueB', 'ValueB']

    Returns:
        list: duplicate values in dictionary format in a list

        Return Example: [{'ValueA': 0}, {'ValueA': 1}, {'ValueA': 2}, {'ValueB': 3}, {'ValueB': 4}]
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
            elif bool(duplicate_list_dictionary) == False or 'None' in str([a_dict.get(entry) for a_dict in duplicate_list_dictionary]):

                # Loops through all entries in the list.
                for index, value in enumerate(duplicates):
                    # Checks if the value from the list is equal to the discovered duplicate.
                    if value == entry:
                        
                        # Adds the duplicate entry values and index
                        # The value will be the key and the index will be the value.
                        # This will allow the ease if finding all index points for a specific value.
                        duplicate_list_dictionary.append({value: index})

    except Exception as err: 
        raise ValueError(f'A failure occurred getting duplicate values the list, {err}, Originating error on line {traceback.extract_stack()[-1].lineno} in <{__name__}>')

    else:
        
        return duplicate_list_dictionary
