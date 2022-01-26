import time
import traceback

# Imports from one directory above and in another folder. Required when running a manual test because a manual test does not jump cleanly to folders above. Pytest does not require a custom set sys.path.
# The '..' represent levels of directories above.
import os
import sys
lib_path = os.path.abspath(os.path.join(__file__, '..', '..', '..'))
sys.path.append(lib_path)

from directors.data_structure_director import user_choice_character_grouping


def test_user_choice_character_grouping():
    """
    This function tests the user_choice_character_grouping.

    Raises:
        ValueError: 
    """
    print('')
    print('-' * 65)
    print('-' * 65)
    print('Testing Function: create_ip_network_design_spreadsheet')
    print('-' * 65)
    print('-' * 65)
    print('')
    #############################################################
	#######Section Test Part 1 (Successful Value Checking)#######
	#############################################################
	#========Tests for a successful output return.========
    sample_list = [
        'TI-MyTest1',
        'TI-MyTest2',
        'KV-MyTest1',
        'KV-MyTest2',
        'WZ-MyTest1'
    ]
    print('Manual run instructions')
    print('')
    print('Select \'Yes\' to continue, Character Position Number, Enter 2 for the character position')
    grouped_characters = user_choice_character_grouping(sample_list)
    # Gets each grouped identifier.
    group_identifiers = [x.get('group_identifier') for x in grouped_characters]
    if '[\'KV\', \'TI\', \'WZ\']' != str(group_identifiers):
        error_message = (
            'A failure occurred in section 1.0 while testing the function \'user_choice_character_grouping\'. Incorrectly returned grouping returned.\n' +
            (('-' * 150) + '\n') + (('-' * 65) + 'Additional Information' + ('-' * 63) + '\n') + (('-' * 150) + '\n') +
            'Expected Result:\n'
            '  - group_identifiers == [\'KV\', \'TI\', \'WZ\']\n\n'
            'Returned Result:\n'
            f'  - group_identifiers == {group_identifiers}\n\n'''
            f'Originating error on line {traceback.extract_stack()[-1].lineno} in <{__name__}>\n' +
            (('-' * 150) + '\n') * 2 
        )
        raise ValueError(error_message)

    #############################################################
	#######Section Test Part 2 (Error/Catch Value Checking)######
	#############################################################
	#========Tests for an incorrectly sent config format.========
    print('!' * 150)
    print('The next test will show the error message because this is not a pytest. If you do not see \'ValueError\' it means the test passed. The test is running in 10 seconds')
    print('!' * 150)
    time.sleep(10)
    try:

        grouped_characters = user_choice_character_grouping('INCORRECT or EMPTY DATA TEST')
    except Exception as error:
        if 'The sent list_of_strings are not in list format' not in str(error):
            error_message = (
                'A failure occurred in section 2.0 while testing the function \'user_choice_character_grouping\'. The test did not fail when sending a non-list parameter.\n' +
                (('-' * 150) + '\n') + (('-' * 65) + 'Additional Information' + ('-' * 63) + '\n') + (('-' * 150) + '\n\n') +
                'Expected Result:\n'
                '  - non-list parameter error\n\n'
                'Returned Result:\n'
                f'  - {error}\n\n'
                f'Originating error on line {traceback.extract_stack()[-1].lineno} in <{__name__}>\n' +
                (('-' * 150) + '\n') * 2 
            )
            raise ValueError(error_message)


test_user_choice_character_grouping()