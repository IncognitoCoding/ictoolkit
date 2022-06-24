# Built-in/Generic Imports
import re
import logging

# Libraries
from fchecker.type import type_check

# Local Functions
from .dict import string_grouper, move_dict_value
from ..helpers.py_helper import get_function_name

# Exceptions
from fexception import FTypeError


__author__ = "IncognitoCoding"
__copyright__ = "Copyright 2022, choice"
__credits__ = ["IncognitoCoding"]
__license__ = "MIT"
__version__ = "0.7"
__maintainer__ = "IncognitoCoding"
__status__ = "Production"


def user_choice_character_grouping(list_of_strings: list) -> dict[str, list[str]]:
    """
    Groups a list of characters based on the user's choices.

    This is a user interaction function.

    The user can group based on a similar character or character position.

    Args:
        list_of_strings (list):
        \t\\- A list of strings that need to get grouped.

    Raises:
        FTypeError (fexception):
        \t\\- The object value '{list_of_strings}' is not an instance of the required class(es) or subclass(es).
        FValueError (fexception):
        \t\\- The string grouper key is not the correct type.

    Returns:
        dict[str, list[str]]:\\
        \t\\- A dictionary of grouped characters.
    """
    logger = logging.getLogger(__name__)
    logger.debug(f"=" * 20 + get_function_name() + "=" * 20)
    # Custom flowchart tracking. This is ideal for large projects that move a lot.
    # For any third-party modules, set the flow before making the function call.
    logger_flowchart = logging.getLogger("flowchart")
    logger_flowchart.debug(f"Flowchart --> Function: {get_function_name()}")

    type_check(value=list_of_strings, required_type=list, tb_remove_name="user_choice_character_grouping")

    formatted_list_of_strings = "  - list_of_strings (list):" + str(
        "\n        - " + "\n        - ".join(map(str, list_of_strings))
    )
    logger.debug("Passing parameters:\n" f"{formatted_list_of_strings}\n")

    # Sets grouping value to None to prevent any reference errors on a retry.
    groupings: dict[str, list[str]] = {}

    try:
        while True:
            # ############################################################
            # ###########Requests Options and Gets Groupings##############
            # ############################################################
            print(
                "\nA hostname comparison is about to take place to group devices based on similar naming into the IP Network Design spreadsheets. "
                "Please continue to select how many character positions you would like to search.\n\n"
            )
            while True:
                choice = input("Are you ready to continue? \n \n1 - Yes \n2 - No \n \nEnter Selection Number: ")
                # Force the input to match the number 1 - 2.
                if re.match(r"[1-2]", choice):
                    continue_choice = int(choice)
                    break

            if int(continue_choice) == 1:
                while True:
                    choice = input(
                        "\nDo you wish to group based on a character position number or a similar separator? \n \n1 - Similar Separator \n2 - Character Position Number  \n \nEnter Select Number: "
                    )
                    # Force the input to match the number 1 - 2.
                    if re.match(r"[1-2]", choice):
                        character_choice = int(choice)
                        break
                if int(character_choice) == 1:
                    while True:
                        choice = str(input("Enter the similar separater character: "))
                        if isinstance(choice, str) and choice != "":
                            choice_character_separater = choice
                            break
                    # Checks the the user entered a number.
                    if isinstance(choice_character_separater, str):
                        # Calls function to group the list of strings.
                        groupings = string_grouper(
                            list_of_strings=list_of_strings,
                            grouping_option=1,
                            grouping_value=choice_character_separater,
                            case_insensitive=True,
                        )
                    else:
                        print("\nError: You did not enter a string. Please retry again.\n\n")
                        # Continues to top of loop to prompt user again
                elif int(character_choice) == 2:
                    while True:
                        choice = input("Enter the character position grouping number: ")
                        if choice.isdigit():
                            character_search_number_choice = choice
                            break
                    # Checks the the user entered a number.
                    if character_search_number_choice.isdigit():
                        # Converts string to int.
                        character_search_number_choice = int(character_search_number_choice)
                        # Calls function to group the list of strings.
                        groupings = string_grouper(
                            list_of_strings=list_of_strings,
                            grouping_option=2,
                            grouping_value=character_search_number_choice,
                            case_insensitive=True,
                        )
                    else:
                        print("\nError: You did not enter a number. Please retry again.\n\n")
                        # Continues to top of loop to prompt user again
            elif int(continue_choice) == 2:
                print("You choose not to continue the hostname comparison. Exiting....")
                exit()

            # ############################################################
            # #################Offers Grouping Overview###################
            # ############################################################
            # Checks if groupings exist before continuing.
            # No grouping means the user chooses to retry.
            if groupings:
                print("\nThe grouping output will show the grouping identifier key and the grouped devices.\n")
                # Loops through the output to show the user the results
                for key, group in groupings.items():
                    # Sets variables for easier usage.
                    print(f"Grouping Key = {key} >>>>> Grouping = {group}")

                while True:
                    choice = input(
                        "\nAre you satisfied with the grouped names? \n \n1 - Yes - Continue\n2 - No - Edit\n3 - Quit  \n \nEnter Select Number: "
                    )
                    # Force the input to match the number 1 - 2.
                    if re.match(r"[1-2]", choice):
                        grouping_acceptance_choice = int(choice)
                        break
                print("\n")
                if int(grouping_acceptance_choice) == 1:
                    # Returns the groupings
                    return groupings
                elif int(grouping_acceptance_choice) == 2:
                    done_editing_choice: int = 0
                    # Loops until customer is done with changes.
                    while True:
                        logger.debug("User choose to retry character group position")
                        # Gets the string value to move.
                        while True:
                            while True:
                                choice = input(
                                    "Please enter the name of the string value you want to move (wildcard: *): "
                                )
                                if isinstance(choice, str) and choice != "":
                                    dest_group_value_choice: str = choice
                                    break

                            # Single key/value variables.
                            src_group_key: str = ""
                            single_match_value: bool = False
                            # Wildcard key/value variables.
                            wildcard_key_value: dict[str, list[str]] = {}

                            # Strips any character after the wildcard character.
                            if "*" in dest_group_value_choice[-1:] and "*" not in dest_group_value_choice[:1]:
                                if "*" != dest_group_value_choice.split()[-1]:
                                    # Removes any characters after the end wildcard character.
                                    dest_group_value_choice = dest_group_value_choice.split("*")[0] + "*"
                            elif "*" not in dest_group_value_choice[-1:] and "*" in dest_group_value_choice[:1]:
                                if "*" != dest_group_value_choice.split()[:1]:
                                    # Removes any characters after the start wildcard character.
                                    dest_group_value_choice = "*" + dest_group_value_choice.split("*")[1]
                            elif "*" in dest_group_value_choice[-1:] and "*" in dest_group_value_choice[:1]:
                                if "*" != dest_group_value_choice.split()[:1]:
                                    # Removes any characters after the start wildcard character.
                                    dest_group_value_choice = "*" + dest_group_value_choice.split("*")[1] + "*"

                            wildcard_value: list[str] = []
                            # Checks if the string value exists.
                            for key, group in groupings.items():
                                # Checks if the string value exists.
                                if "*" in dest_group_value_choice[-1:] and "*" not in dest_group_value_choice[:1]:
                                    wildcard_value = [
                                        value
                                        for value in group
                                        if value.startswith(dest_group_value_choice.replace("*", ""))
                                    ]

                                    if len(wildcard_value) >= 1:
                                        if isinstance(key, str):
                                            wildcard_key_value.update({key: wildcard_value})
                                        else:
                                            exc_args = {
                                                "main_message": "The string grouper key is not the correct type.",
                                                "expected_result": "<class 'str'>",
                                                "returned_result": f"{type(key)}",
                                            }
                                            raise FTypeError(exc_args)
                                elif "*" not in dest_group_value_choice[-1:] and "*" in dest_group_value_choice[:1]:
                                    wildcard_value = [
                                        value
                                        for value in group
                                        if value.endswith(dest_group_value_choice.replace("*", ""))
                                    ]

                                    if len(wildcard_value) >= 1:
                                        if isinstance(key, str):
                                            wildcard_key_value.update({key: wildcard_value})
                                        else:
                                            exc_args = {
                                                "main_message": "The string grouper key is not the correct type.",
                                                "expected_result": "<class 'str'>",
                                                "returned_result": f"{type(key)}",
                                            }
                                            raise FTypeError(exc_args)
                                elif "*" in dest_group_value_choice[-1:] and "*" in dest_group_value_choice[:1]:
                                    wildcard_value = [
                                        value for value in group if dest_group_value_choice.replace("*", "") in value
                                    ]

                                    if len(wildcard_value) >= 1:
                                        if isinstance(key, str):
                                            wildcard_key_value.update({key: wildcard_value})
                                        else:
                                            exc_args = {
                                                "main_message": "The string grouper key is not the correct type.",
                                                "expected_result": "<class 'str'>",
                                                "returned_result": f"{type(key)}",
                                            }
                                            raise FTypeError(exc_args)
                                else:
                                    single_match_value = any(dest_group_value_choice == value for value in group)
                                if single_match_value:
                                    # Sets the name of the source group.
                                    if isinstance(key, str):
                                        src_group_key = key
                                    else:
                                        exc_args = {
                                            "main_message": "The string grouper key is not the correct type.",
                                            "expected_result": "<class 'str'>",
                                            "returned_result": f"{type(key)}",
                                        }
                                        raise FTypeError(exc_args)
                                    break

                            if single_match_value or len(wildcard_key_value) >= 1:
                                break
                            else:
                                if "*" in dest_group_value_choice:
                                    print(
                                        f"\nThe wildcard string value you entered '{dest_group_value_choice}' does not match any value in the existing groups. Please try again.\n"
                                    )
                                else:
                                    print(
                                        f"\nThe string value you entered '{dest_group_value_choice}' does not match any value in the existing groups. Please try again.\n"
                                    )

                        existing_dest_group: bool = False
                        existing_dest_values: list[str] = []
                        # Gets the string value to move.
                        while True:
                            while True:
                                choice = input(
                                    f"Please enter the group key to move the string value(s) '{dest_group_value_choice}': "
                                )
                                if isinstance(choice, str) and choice != "":
                                    dest_group_key_choice = choice
                                    break

                            single_match_value: bool = False
                            # Checks if the string value exists.
                            for key, group in groupings.items():
                                # Checks if the string value exists.
                                if dest_group_key_choice == key:
                                    # Verifies the moving values are not part of the same
                                    # destination group.
                                    for current_group_value in groupings[key]:
                                        # Checks current values against the users choice.
                                        if "*" in dest_group_value_choice:
                                            if len(wildcard_key_value) >= 1:
                                                # Loops through wildcard groupings (One per matching key).
                                                for key, group in wildcard_key_value.items():
                                                    # Loops through each entry in the matching wildcard key based group.
                                                    for dest_group_value in group:
                                                        if current_group_value == dest_group_value:
                                                            print(
                                                                f"\nThe current group value '{current_group_value}' matches one of the destination "
                                                                f"moving values '{groupings[key]}'. Skipping this value"
                                                            )
                                                            # Adds values to the list to be existed during the move.
                                                            existing_dest_values.append(current_group_value)
                                        else:
                                            if current_group_value == dest_group_value_choice:
                                                print(
                                                    f"\nThe current group value '{current_group_value}' matches the destination "
                                                    f"moving value '{dest_group_value_choice}'. Skipping the group edit"
                                                )
                                                existing_dest_group = True
                                                break
                                        if existing_dest_group:
                                            break

                                    if existing_dest_group:
                                        break
                                    else:
                                        single_match_value = True
                                if single_match_value:
                                    break
                            if existing_dest_group or single_match_value:
                                break
                            else:
                                continue_choice: int = 0
                                while True:
                                    choice = input(
                                        f"\nThe string value you entered '{dest_group_key_choice}' does not match any existing group keys. Do you want to continue with this new key?\n\n"
                                        "1 - Yes \n"
                                        "2 - No \n \nEnter Selection Number: "
                                    )
                                    # Force the input to match the number 1 - 2.
                                    if re.match(r"[1-2]", choice):
                                        continue_choice = int(choice)
                                        break
                                if continue_choice == 1:
                                    break

                        if existing_dest_group:
                            print("\nBelow are your current grouping edits:")
                            # Loops through the output to show the user the results
                            for key, group in groupings.items():
                                # Sets variables for easier usage.
                                print(f"Grouping Key = {key} >>>>> Grouping = {group}")
                        else:
                            # Moves the dictionary value based on the destination group value.
                            if "*" in dest_group_value_choice:
                                if len(wildcard_key_value) >= 1:
                                    for key, group in wildcard_key_value.items():
                                        for entry in group:
                                            # Checks if the entry is an existing entry.
                                            existing_dest_group = any(
                                                value for value in existing_dest_values if entry == value
                                            )
                                            # Moves if the value is not an existing value.
                                            if not existing_dest_group:
                                                groupings = move_dict_value(
                                                    my_dict=groupings,
                                                    src_key=key,
                                                    dest_key=dest_group_key_choice,
                                                    value=entry,
                                                )  # type: ignore
                            else:
                                # Moves the dictionary values based on the user's input.
                                groupings = move_dict_value(
                                    my_dict=groupings,
                                    src_key=src_group_key,
                                    dest_key=dest_group_key_choice,
                                    value=dest_group_value_choice,
                                )  # type: ignore

                            print("\nBelow are your revised edits:")
                            # Loops through the output to show the user the results
                            for key, group in groupings.items():
                                # Sets variables for easier usage.
                                print(f"Grouping Key = {key} >>>>> Grouping = {group}")

                        while True:
                            choice = input(
                                "\nAre you done making group value edits?\n\n"
                                "1 - Yes \n"
                                "2 - No \n \nEnter Selection Number: "
                            )
                            # Force the input to match the number 1 - 2.
                            if re.match(r"[1-2]", choice):
                                done_editing_choice = int(choice)
                                break
                        # Checks if the user is done making edits.
                        if done_editing_choice == 1:
                            # Returns the groupings
                            return groupings
                    # Continues to top of loop to prompt user again
                elif int(grouping_acceptance_choice) == 3:
                    print("\nYou choose to quit. Exiting....")
                    exit()
    # Catches ctrl + c
    except KeyboardInterrupt:
        print("Keyboard interruption. Exiting...")
        exit()
    # Catches ctrl + z
    # Input box failure (ex: ctrl + z) will throw this exception.
    except EOFError:
        print("Keyboard interruption. Exiting...")
        exit()
