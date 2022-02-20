"""
This script is used to test the dict_director module using pytest.
"""
# Built-in/Generic Imports
from dataclasses import asdict
import pytest

# Local Functions
from ictoolkit import (create_dataclass,
                       remove_duplicate_dict_values_in_list,
                       get_list_of_dicts_duplicates,
                       get_list_duplicates,
                       string_grouper,
                       find_longest_common_substring,
                       clean_non_word_characters)

# Exceptions
from fexception import FValueError


def test_create_dataclass():
    """
    This tests creating a dataclass.

    Raises:
    """
    print('')
    print('-' * 65)
    print('-' * 65)
    print('Testing Function: create_dataclass')
    print('-' * 65)
    print('-' * 65)
    print('')

    # ############################################################
    # ######Section Test Part 1 (Successful Value Checking)#######
    # ############################################################
    # =====================================================
    # ========Tests for a successful output return.========
    # =====================================================
    # Creating the dictionary
    a_dict = {'name': "Bob",
              'room_number': 1223,
              'teaching_subject': "Python"}
    new_dataclass = create_dataclass('MyTestClass', a_dict)
    assert """<class 'types.MyTestClass'>""" == str(type(new_dataclass))
    assert """MyTestClass(name='Bob', room_number=1223, teaching_subject='Python')""" == str(new_dataclass)
    assert """{'name': 'Bob', 'room_number': 1223, 'teaching_subject': 'Python'}""" == str(asdict(new_dataclass))
    assert 'Bob' == str(new_dataclass.name)
    assert 1223 == int(new_dataclass.room_number)
    assert 'Python' == str(new_dataclass.teaching_subject)

    # Tests changing dataclass value.
    new_dataclass.name = 'John'
    assert 'John' == str(new_dataclass.name)

    # =====================================================
    # ========Tests for a successful output return.========
    # =====================================================
    # Creating the dictionary
    a_dict = [{'name': "Bob", 'room_number': 1223, 'teaching_subject': "Python"},
              {'name': "Tim", 'room_number': 1333, 'teaching_subject': "Python2"}]

    new_dataclass = create_dataclass('MyTestClass', a_dict)
    assert """<class 'list'>""" == str(type(new_dataclass))
    assert """<class 'types.MyTestClass'>""" == str(type(new_dataclass[0]))
    assert """{'name': 'Bob', 'room_number': 1223, 'teaching_subject': 'Python'}""" == str(asdict(new_dataclass[0]))
    assert """{'name': 'Tim', 'room_number': 1333, 'teaching_subject': 'Python2'}""" == str(asdict(new_dataclass[1]))

    # ############################################################
    # ######Section Test Part 2 (Error/Catch Value Checking)######
    # ############################################################
    # =====================================================
    # ======Tests for an incorrectly sent list format.=====
    # =====================================================
    with pytest.raises(Exception) as excinfo:
        a_dict = [{'name': "Bob", 'room_number': 1223, 'teaching_subject': "Python"},
                  {'name': "Tim", 'teaching_subject': "Python2"}]
        new_dataclass = create_dataclass('MyTestClass', a_dict)
    assert """MyTestClass got an unexpected keyward argument 'room_number'""" in str(excinfo.value)


def test_remove_duplicate_dict_values_in_list():
    """
    This tests removing duplicate dictionary values in a list.

    Raises:
        ValueError: A failure occurred in section 1.0 while testing the function 'remove_duplicate_dict_values_in_list' using a full check.
        ValueError: A failure occurred in section 1.1 while testing the function 'remove_duplicate_dict_values_in_list' using an index.
    """
    print('')
    print('-' * 65)
    print('-' * 65)
    print('Testing Function: remove_duplicate_dict_values_in_list')
    print('-' * 65)
    print('-' * 65)
    print('')

    # ############################################################
    # ######Section Test Part 1 (Successful Value Checking)#######
    # ############################################################
    # ========Tests for a successful output return.========
    # Sets sample list
    sample_list_dictionary = list([{'search_entry': '|Error|', 'found_entry': 'the entry found'}, {'search_entry': '|Warning|', 'found_entry': 'the entry found'}])
    # Tests removing duplicate dictionary entries.
    check_all = remove_duplicate_dict_values_in_list(sample_list_dictionary)
    # Return length should equal 2.
    # Expected Return: [{'search_entry': '|Error|', 'found_entry': 'the entry found'}, {'search_entry': '|Warning|', 'found_entry': 'the entry found'}]
    if len(check_all) != 2:
        exc_args = {
            'main_message': 'A failure occurred in section 1.0 while testing the function \'remove_duplicate_dict_values_in_list\' using a full check.',
            'expected_result': 2,
            'returned_result': len(check_all),
        }
        raise FValueError(exc_args)

    # ========Tests for a successful output return.========
    # Tests removing duplicates from index 1 of each dictionary entry.
    check_index = remove_duplicate_dict_values_in_list(sample_list_dictionary, 1)
    # Return length should equal 1.
    # Expected Return: [{'search_entry': '|Error|', 'found_entry': 'the entry found'}]
    if len(check_index) != 1:
        exc_args = {
            'main_message': 'A failure occurred in section 1.1 while testing the function \'remove_duplicate_dict_values_in_list\' using an index.',
            'expected_result': 1,
            'returned_result': len(check_index),
        }
        raise FValueError(exc_args)


def test_get_list_of_dicts_duplicates():
    """
    Tests getting a list of dictionary duplicates.

    Raises:
        ValueError: A failure occurred in section 1.0 while testing the function 'get_list_of_dicts_duplicates'.
        ValueError: A failure occurred in section 1.1 while testing the function 'get_list_of_dicts_duplicates'.
    """
    print('')
    print('-' * 65)
    print('-' * 65)
    print('Testing Function: get_list_of_dicts_duplicates')
    print('-' * 65)
    print('-' * 65)
    print('')

    # ############################################################
    # ######Section Test Part 1 (Successful Value Checking)#######
    # ############################################################
    # ========Tests for a successful output return.========
    # Sets sample list
    sample_list_dictionary = [{'key1': 'ValueA'}, {'key1': 'ValueA'}, {'key1': 'ValueA'}, {'key1': 'ValueB'}, {'key1': 'ValueB'}]
    # Tests finding duplicate values for key (key1).
    check_all = get_list_of_dicts_duplicates('key1', sample_list_dictionary)
    # Return length should equal 5.
    # Expected Return: [{'index': 0, 'value': 'ValueA'}, {'index': 1, 'value': 'ValueA'}, {'index': 2, 'value': 'ValueA'}, {'index': 3, 'value': 'ValueB'}, {'index': 4, 'value': 'ValueB'}]
    if len(check_all) != 5:
        exc_args = {
            'main_message': 'A failure occurred in section 1.0 while testing the function \'get_list_of_dicts_duplicates\'.',
            'expected_result': 5,
            'returned_result': len(check_all),
        }
        raise FValueError(exc_args)

    # ========Tests for a successful output return.========
    # Tests finding duplicate values for key (key1).
    check_all = get_list_of_dicts_duplicates('key1', sample_list_dictionary, True)
    # Return length should equal 2.
    # Expected Return: {'ValueA': [{'index': 0, 'value': 'ValueA'}, {'index': 1, 'value': 'ValueA'}, {'index': 2, 'value': 'ValueA'}], 'ValueB': [{'index': 3, 'value': 'ValueB'}, {'index': 4, 'value': 'ValueB'}]}
    if len(check_all) != 2:
        exc_args = {
            'main_message': 'A failure occurred in section 1.1 while testing the function \'get_list_of_dicts_duplicates\'.',
            'expected_result': 2,
            'returned_result': len(check_all),
        }
        raise FValueError(exc_args)


def test_get_list_duplicates():
    """
    Tests getting a list of duplicates.

    Raises:
        ValueError: A failure occurred in section 1.0 while testing the function 'get_list_duplicates'.
        ValueError: A failure occurred in section 1.1 while testing the function 'get_list_duplicates'.
        ValueError: A failure occurred in section 1.2 while testing the function 'get_list_duplicates'.
    """
    print('')
    print('-' * 65)
    print('-' * 65)
    print('Testing Function: get_list_duplicates')
    print('-' * 65)
    print('-' * 65)
    print('')

    # ############################################################
    # ######Section Test Part 1 (Successful Value Checking)#######
    # ############################################################
    # ========Tests for a successful output return.========
    # Sets sample list
    sample_list = ['ValueA', 'ValueA', 'ValueA', 'ValueB', 'ValueB']
    # Tests finding duplicate values in the list.
    check_all = get_list_duplicates(sample_list)
    # Return length should equal 5.
    # Expected Return: [{'index': 0, 'value': 'ValueA'}, {'index': 1, 'value': 'ValueA'}, {'index': 2, 'value': 'ValueA'}, {'index': 3, 'value': 'ValueB'}, {'index': 4, 'value': 'ValueB'}]
    if len(check_all) != 5:
        exc_args = {
            'main_message': 'A failure occurred in section 1.0 while testing the function \'get_list_duplicates\'.',
            'expected_result': 5,
            'returned_result': len(check_all),
        }
        raise FValueError(exc_args)

    # ========Tests for a successful output return.========
    # Sets sample list
    sample_list = [['ValueA', 'ValueB'], ['ValueA', 'ValueB'], ['ValueD', 'ValueB'], ['ValueB'], ['ValueB']]
    # Tests finding duplicate values in the list.
    check_all = get_list_duplicates(sample_list, None, True)
    # Return length should equal 2.
    # Expected Return: {'ValueA': [{'index': 0, 'value': 'ValueA'}, {'index': 1, 'value': 'ValueA'}, {'index': 2, 'value': 'ValueA'}], 'ValueB': [{'index': 3, 'value': 'ValueB'}, {'index': 4, 'value': 'ValueB'}]}
    if len(check_all) != 2:
        exc_args = {
            'main_message': 'A failure occurred in section 1.1 while testing the function \'get_list_duplicates\'.',
            'expected_result': 2,
            'returned_result': len(check_all),
        }
        raise FValueError(exc_args)

    # ========Tests for a successful output return.========
    # Sets sample list
    sample_list = [['ValueA', 'ValueB'], ['ValueA', 'ValueB'], ['ValueD', 'ValueB'], ['ValueB'], ['ValueB']]
    # Tests finding duplicate values in the list.
    check_all = get_list_duplicates(sample_list, 0, True)
    # Return length should equal 2.
    # Expected Return: {'ValueA': [{'index': 0, 'value': 'ValueA'}, {'index': 1, 'value': 'ValueA'}, {'index': 2, 'value': 'ValueA'}], 'ValueB': [{'index': 3, 'value': 'ValueB'}, {'index': 4, 'value': 'ValueB'}]}
    if len(check_all) != 2:
        exc_args = {
            'main_message': 'A failure occurred in section 1.2 while testing the function \'get_list_duplicates\'.',
            'expected_result': 2,
            'returned_result': len(check_all),
        }
        raise FValueError(exc_args)


def test_string_grouper():
    """
    Tests grouping strings.

    Raises:
        ValueError: A failure occurred in section 1.0 while testing the function 'string_grouper'.
        ValueError: A failure occurred in section 1.1 while testing the function 'string_grouper'. The first entries in the list do not match.
        ValueError: A failure occurred in section 2.0 while testing the function 'string_grouper'.
        ValueError: A failure occurred in section 2.1 while testing the function 'string_grouper'. The first entries in the list do not match.
        ValueError: A failure occurred in section 3.0 while testing the function 'string_grouper'.
        ValueError: A failure occurred in section 3.1 while testing the function 'string_grouper'. The first entries in the list do not match.
        ValueError: A failure occurred in section 4.0 while testing the function 'string_grouper'.
        ValueError: A failure occurred in section 4.1 while testing the function 'string_grouper'. The first entries in the list do not match.
        ValueError: A failure occurred in section 5.0 while testing the function 'string_grouper'.
        ValueError: A failure occurred in section 5.1 while testing the function 'string_grouper'. The first entries in the list do not match.
        ValueError: A failure occurred in section 6.0 while testing the function 'string_grouper'.
        ValueError: A failure occurred in section 6.1 while testing the function 'string_grouper'. The first entries in the list do not match.
        ValueError: A failure occurred in section 7.0 while testing the function 'string_grouper'. The test did not fail when sending a non-list of strings.
        ValueError: A failure occurred in section 7.1 while testing the function 'string_grouper'. The test did not fail when sending a non-string.
        ValueError: A failure occurred in section 7.2 while testing the function 'string_grouper'. The test did not fail when sending a non-int.
    """
    print('')
    print('-' * 65)
    print('-' * 65)
    print('Testing Function: string_grouper')
    print('-' * 65)
    print('-' * 65)
    print('')

    # List of sample switch names for multiple sites. Case insensitve testing.
    list_of_strings = [
        "JJ-MDF-9200-1_2",
        "KV-MDF-9200-1_2",
        "KV-MDF1-9200-1_2",
        "KZV-MDF1-9200-1_2",
        "kv-IDF1-9200-1_2",
        "KV-IDF2-9200-1_2",
        "TI-IDF1-9200-1_2",
        "TI-IDF2-9200-1_2",
    ]

    # ############################################################
    # ######Section Test Part 1 (Successful Value Checking)#######
    # ############################################################
    # ========Tests for a successful output return for case insensitive.========
    # Tests finding duplicate values in the list.
    group_check = string_grouper(list_of_strings, '-', 1, True)

    # Return length should equal 5.
    # Expected Return: [{'group_identifier': 'JJ', 'grouping': ['JJ-MDF-9200-1_2']},
    #                   {'group_identifier': 'KV', 'grouping': ['kv-IDF1-9200-1_2, 'KV-IDF2-9200-1_2', 'KV-MDF-9200-1_2', 'KV-MDF1-9200-1_2']},
    #                   {'group_identifier': 'KZV', 'grouping': ['KZV-MDF1-9200-1_2']},
    #                   {'group_identifier': 'TI', 'grouping': ['TI-IDF1-9200-1_2', 'TI-IDF2-9200-1_2']}]
    if len(group_check) != 4:
        exc_args = {
            'main_message': 'A failure occurred in section 1.0 while testing the function \'string_grouper\'.',
            'expected_result': 4,
            'returned_result': len(group_check),
        }
        raise FValueError(exc_args)

    # Gets first list return values from the two dictionary entries.
    group_identifier = group_check[0].get('group_identifier')
    grouping = group_check[0].get('grouping')
    # Checks if the values are not equal to the expected return output.
    if (
        group_identifier != 'JJ'
        or grouping != ['JJ-MDF-9200-1_2']
    ):
        exc_args = {
            'main_message': 'A failure occurred in section 1.1 while testing the function \'string_grouper\'s. The first entries in the list do not match.',
            'expected_result': 'group_identifier != JJ -- or --  grouping != [\'JJ-MDF-9200-1_2\']',
            'returned_result': f'roup_identifier != {group_identifier} -- or -- grouping != {grouping}',
        }
        raise FValueError(exc_args)

    # ############################################################
    # ######Section Test Part 2 (Successful Value Checking)#######
    # ############################################################
    # ========Tests for a successful output return for case insensitive.========
    # Tests finding duplicate values in the list.
    group_check = string_grouper(list_of_strings, 2, 2, True)

    # Return length should equal 4.
    # Expected Return: [{'group_identifier': 'JJ', 'grouping': ['JJ-MDF-9200-1_2']},
    #                   {'group_identifier': 'KV', 'grouping': ['kv-IDF1-9200-1_2', 'KV-IDF2-9200-1_2', 'KV-MDF-9200-1_2', 'KV-MDF1-9200-1_2']},
    #                   {'group_identifier': 'KZV', 'grouping': ['KZV-MDF1-9200-1_2']},
    #                   {'group_identifier': 'TI', 'grouping': ['TI-IDF1-9200-1_2', 'TI-IDF2-9200-1_2']}]
    if len(group_check) != 4:
        exc_args = {
            'main_message': 'A failure occurred in section 2.0 while testing the function \'string_grouper\'.',
            'expected_result': 4,
            'returned_result': len(group_check),
        }
        raise FValueError(exc_args)

    # Gets first list return values from the two dictionary entries.
    group_identifier = group_check[0].get('group_identifier')
    grouping = group_check[0].get('grouping')
    # Checks if the values are not equal to the expected return output.
    if (
        group_identifier != 'JJ'
        or grouping != ['JJ-MDF-9200-1_2']
    ):
        exc_args = {
            'main_message': 'A failure occurred in section 2.1 while testing the function \'string_grouper\'s. The first entries in the list do not match.',
            'expected_result': 'group_identifier != JJ -- or --  grouping != [\'JJ-MDF-9200-1_2\']',
            'returned_result': f'roup_identifier != {group_identifier} -- or -- grouping != {grouping}',
        }
        raise FValueError(exc_args)

    # ############################################################
    # ######Section Test Part 3 (Successful Value Checking)#######
    # ############################################################
    # ========Tests for a successful output return.========
    # Currently option 3 does not support case insensitive. Leaving test to add once option 3 is setup.
    # Tests finding duplicate values in the list.
    group_check = string_grouper(list_of_strings, None, 3)

    # Return length should equal 5.
    # Expected Return: [{'group_identifier': 'JJ-MDF-9200-1_2', 'grouping': ['JJ-MDF-9200-1_2']},
    #                   {'group_identifier': 'KV-IDF', 'grouping': ['KV-IDF1-9200-1_2', 'KV-IDF2-9200-1_2']},
    #                   {'group_identifier': 'KV-MDF', 'grouping': ['KV-MDF-9200-1_2', 'KV-MDF1-9200-1_2']},
    #                   {'group_identifier': 'KZV-MDF1-9200-1_2', 'grouping': ['KZV-MDF1-9200-1_2']},
    #                   {'group_identifier': 'TI-IDF', 'grouping': ['TI-IDF1-9200-1_2', 'TI-IDF2-9200-1_2']}]
    if len(group_check) != 5:
        exc_args = {
            'main_message': 'A failure occurred in section 3.0 while testing the function \'string_grouper\'.',
            'expected_result': 5,
            'returned_result': len(group_check),
        }
        raise FValueError(exc_args)

    # Gets first list return values from the two dictionary entries.
    group_identifier = group_check[0].get('group_identifier')
    grouping = group_check[0].get('grouping')
    # Checks if the values are not equal to the expected return output.
    if (
        group_identifier != 'JJ-MDF-9200-1_2'
        or grouping != ['JJ-MDF-9200-1_2']
    ):
        exc_args = {
            'main_message': 'A failure occurred in section 3.1 while testing the function \'string_grouper\'s. The first entries in the list do not match.',
            'expected_result': 'group_identifier != JJ-MDF-9200-1_2 -- or --  grouping != [\'JJ-MDF-9200-1_2\']',
            'returned_result': f'roup_identifier != {group_identifier} -- or -- grouping != {grouping}',
        }
        raise FValueError(exc_args)

    # List of sample switch names for multiple sites. All upper testing.
    list_of_strings = [
        "JJ-MDF-9200-1_2",
        "KV-MDF-9200-1_2",
        "KV-MDF1-9200-1_2",
        "KZV-MDF1-9200-1_2",
        "KV-IDF1-9200-1_2",
        "KV-IDF2-9200-1_2",
        "TI-IDF1-9200-1_2",
        "TI-IDF2-9200-1_2",
    ]

    # ############################################################
    # ######Section Test Part 4 (Successful Value Checking)#######
    # ############################################################
    # ========Tests for a successful output return.========
    # Tests finding duplicate values in the list.
    group_check = string_grouper(list_of_strings, '-', 1)

    # Return length should equal 4.
    # Expected Return: [{'group_identifier': 'JJ', 'grouping': ['JJ-MDF-9200-1_2']},
    #                   {'group_identifier': 'KV', 'grouping': ['KV-IDF1-9200-1_2', 'KV-IDF2-9200-1_2', 'KV-MDF-9200-1_2', 'KV-MDF1-9200-1_2']},
    #                   {'group_identifier': 'KZV', 'grouping': ['KZV-MDF1-9200-1_2']},
    #                   {'group_identifier': 'TI', 'grouping': ['TI-IDF1-9200-1_2', 'TI-IDF2-9200-1_2']}]
    if len(group_check) != 4:
        exc_args = {
            'main_message': 'A failure occurred in section 4.0 while testing the function \'string_grouper\'.',
            'expected_result': 4,
            'returned_result': len(group_check),
        }
        raise FValueError(exc_args)

    # Gets first list return values from the two dictionary entries.
    group_identifier = group_check[0].get('group_identifier')
    grouping = group_check[0].get('grouping')
    # Checks if the values are not equal to the expected return output.
    if (
        group_identifier != 'JJ'
        or grouping != ['JJ-MDF-9200-1_2']
    ):
        exc_args = {
            'main_message': 'A failure occurred in section 4.1 while testing the function \'string_grouper\'s. The first entries in the list do not match.',
            'expected_result': 'group_identifier != JJ -- or --  grouping != [\'JJ-MDF-9200-1_2\']',
            'returned_result': f'roup_identifier != {group_identifier} -- or -- grouping != {grouping}',
        }
        raise FValueError(exc_args)

    # ############################################################
    # ######Section Test Part 5 (Successful Value Checking)#######
    # ############################################################
    # ========Tests for a successful output return.========
    # Tests finding duplicate values in the list.
    group_check = string_grouper(list_of_strings, 2, 2)

    # Return length should equal 4.
    # Expected Return: [{'group_identifier': 'JJ', 'grouping': ['JJ-MDF-9200-1_2']},
    #                   {'group_identifier': 'KV', 'grouping': ['KV-IDF1-9200-1_2', 'KV-IDF2-9200-1_2', 'KV-MDF-9200-1_2', 'KV-MDF1-9200-1_2']},
    #                   {'group_identifier': 'KZV', 'grouping': ['KZV-MDF1-9200-1_2']},
    #                   {'group_identifier': 'TI', 'grouping': ['TI-IDF1-9200-1_2', 'TI-IDF2-9200-1_2']}]
    if len(group_check) != 4:
        exc_args = {
            'main_message': 'A failure occurred in section 5.0 while testing the function \'string_grouper\'.',
            'expected_result': 4,
            'returned_result': len(group_check),
        }
        raise FValueError(exc_args)

    # Gets first list return values from the two dictionary entries.
    group_identifier = group_check[0].get('group_identifier')
    grouping = group_check[0].get('grouping')
    # Checks if the values are not equal to the expected return output.
    if (
        group_identifier != 'JJ'
        or grouping != ['JJ-MDF-9200-1_2']
    ):
        exc_args = {
            'main_message': 'A failure occurred in section 5.1 while testing the function \'string_grouper\'s. The first entries in the list do not match.',
            'expected_result': 'group_identifier != JJ -- or --  grouping != [\'JJ-MDF-9200-1_2\']',
            'returned_result': f'roup_identifier != {group_identifier} -- or -- grouping != {grouping}',
        }
        raise FValueError(exc_args)

    # ############################################################
    # ######Section Test Part 6 (Successful Value Checking)#######
    # ############################################################
    # ========Tests for a successful output return.========
    # Tests finding duplicate values in the list.
    group_check = string_grouper(list_of_strings, None, 3)

    # Return length should equal 5.
    # Expected Return: [{'group_identifier': 'JJ-MDF-9200-1_2', 'grouping': ['JJ-MDF-9200-1_2']},
    #                   {'group_identifier': 'KV-IDF', 'grouping': ['KV-IDF1-9200-1_2', 'KV-IDF2-9200-1_2']},
    #                   {'group_identifier': 'KV-MDF', 'grouping': ['KV-MDF-9200-1_2', 'KV-MDF1-9200-1_2']},
    #                   {'group_identifier': 'KZV-MDF1-9200-1_2', 'grouping': ['KZV-MDF1-9200-1_2']},
    #                   {'group_identifier': 'TI-IDF', 'grouping': ['TI-IDF1-9200-1_2', 'TI-IDF2-9200-1_2']}]
    if len(group_check) != 5:
        exc_args = {
            'main_message': 'A failure occurred in section 6.0 while testing the function \'string_grouper\'.',
            'expected_result': 5,
            'returned_result': len(group_check),
        }
        raise FValueError(exc_args)

    # Gets first list return values from the two dictionary entries.
    group_identifier = group_check[0].get('group_identifier')
    grouping = group_check[0].get('grouping')
    # Checks if the values are not equal to the expected return output.
    if (
        group_identifier != 'JJ-MDF-9200-1_2'
        or grouping != ['JJ-MDF-9200-1_2']
    ):
        exc_args = {
            'main_message': 'A failure occurred in section 6.1 while testing the function \'string_grouper\'s. The first entries in the list do not match.',
            'expected_result': 'group_identifier != JJ-MDF-9200-1_2 -- or --  grouping != [\'JJ-MDF-9200-1_2\']',
            'returned_result': f'roup_identifier != {group_identifier} -- or -- grouping != {grouping}',
        }
        raise FValueError(exc_args)

    # ############################################################
    # ######Section Test Part 7 (Error/Catch Value Checking)######
    # ############################################################
    # ========Tests for an incorrectly sent list format.========
    try:
        # Tests finding duplicate values in the list.
        group_check = string_grouper('INCORRECT or EMPTY DATA TEST', '-', 1)
    except Exception as error:
        if """The value 'INCORRECT or EMPTY DATA TEST' is not in <class 'list'> format""" not in str(error):
            exc_args = {
                'main_message': 'A failure occurred in section 7.0 while testing the function \'string_grouper\'. The test did not fail when sending a non-list of strings.',
                'expected_result': 'non-list error',
                'returned_result': error,
            }
            raise FValueError(exc_args)

    # ========Tests for an incorrectly sent string format.========
    # Tests finding duplicate values in the list.
    try:
        group_check = string_grouper(['ONE ENTRY1', 'ONE ENTRY2'], 3, 1)
    except Exception as error:
        if 'The grouping_value sent for the grouping is not a string' not in str(error):
            exc_args = {
                'main_message': 'A failure occurred in section 7.2 while testing the function \'string_grouper\'. The test did not fail when sending a non-string.',
                'expected_result': 'non-string error',
                'returned_result': error,
            }
            raise FValueError(exc_args)

    # ========Tests for an incorrectly sent int format.========
    # Tests finding duplicate values in the list.
    try:
        group_check = string_grouper(['ONE ENTRY1', 'ONE ENTRY2'], 'T', 2)
    except Exception as error:
        if 'The grouping_value sent for the grouping is not a int' not in str(error):
            exc_args = {
                'main_message': 'A failure occurred in section 7.3 while testing the function \'string_grouper\'. The test did not fail when sending a non-int.',
                'expected_result': 'non-int error',
                'returned_result': error,
            }
            raise FValueError(exc_args)


def test_find_longest_common_substring():
    """
    Tests finding a common grouping substring.

    Raises:
        ValueError: A failure occurred in section 1.0 while testing the function \'find_longest_common_substring\'. The test did return the correct common substring.
        ValueError: A failure occurred in section 2.0 while testing the function \'find_longest_common_substring\'. The test did not fail when sending a non-string parameter.
    """
    print('')
    print('-' * 65)
    print('-' * 65)
    print('Testing Function: find_longest_common_substring')
    print('-' * 65)
    print('-' * 65)
    print('')

    # ############################################################
    # ######Section Test Part 1 (Successful Value Checking)#######
    # ############################################################
    # ========Tests for a successful output return.========
    common_substring = find_longest_common_substring('mysamplechangeshere', 'mysampleneverchanges')
    # Checks if the return substring is not equal the expected result.
    if not common_substring == 'mysample':
        exc_args = {
            'main_message': 'A failure occurred in section 1.0 while testing the function \'find_longest_common_substring\'. The test did return the correct common substring.',
            'expected_result': 'mysample',
            'returned_result': common_substring,
        }
        raise FValueError(exc_args)

    # ############################################################
    # ######Section Test Part 2 (Error/Catch Value Checking)######
    # ############################################################
    # ========Tests for an incorrectly sent config format.========
    try:

        common_substring = find_longest_common_substring('mysamplechangeshere', ['INCORRECT or EMPTY DATA TEST'])
    except Exception as error:
        if """The value '['INCORRECT or EMPTY DATA TEST']' is not in <class 'str'> format.""" not in str(error):
            exc_args = {
                'main_message': 'A failure occurred in section 2.0 while testing the function \'find_longest_common_substring\'. The test did not fail when sending a non-string parameter.',
                'expected_result': 'non-string parameter error',
                'returned_result': error,
            }
            raise FValueError(exc_args)


def test_clean_non_word_characters():
    """
    Tests cleaning non-word characters.

    Raises:
        ValueError: A failure occurred in section 1.0 while testing the function \'clean_non_word_characters\'. The test did return the correct cleaned substring.
        ValueError: A failure occurred in section 2.0 while testing the function \'clean_non_word_characters\'. The test did not fail when sending a non-string parameter.
    """
    print('')
    print('-' * 65)
    print('-' * 65)
    print('Testing Function: clean_non_word_characters')
    print('-' * 65)
    print('-' * 65)
    print('')

    # ############################################################
    # ######Section Test Part 1 (Successful Value Checking)#######
    # ############################################################
    # ========Tests for a successful output return.========
    cleaned_string = clean_non_word_characters('BTW-N5K\x06')
    # Checks if the return substring is not equal the expected result.
    if not cleaned_string == 'BTW-N5K':
        exc_args = {
            'main_message': 'A failure occurred in section 1.0 while testing the function \'clean_non_word_characters\'. The test did return the correct cleaned substring.',
            'expected_result': 'BTW-N5K',
            'returned_result': cleaned_string,
        }
        raise FValueError(exc_args)

    # ############################################################
    # ######Section Test Part 2 (Error/Catch Value Checking)######
    # ############################################################
    # ========Tests for an incorrectly sent config format.========
    try:

        cleaned_string = clean_non_word_characters(['INCORRECT or EMPTY DATA TEST'])
    except Exception as error:
        if """The value '['INCORRECT or EMPTY DATA TEST']' is not in <class 'str'> format.""" not in str(error):
            exc_args = {
                'main_message': 'A failure occurred in section 2.0 while testing the function \'clean_non_word_characters\'. The test did not fail when sending a non-string parameter.',
                'expected_result': 'non-string parameter error',
                'returned_result': error,
            }
            raise FValueError(exc_args)
