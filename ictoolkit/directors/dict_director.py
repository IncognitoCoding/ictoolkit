#!interpreter

"""
This module is designed to offer the ability to modify dictionaries.
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
