# Built-in/Generic Imports
import logging
from itertools import groupby
from typing import Union, Any
from collections import OrderedDict

# Libraries
from fchecker.type import type_check

# Local Functions
from ..data_structure.common import common_case_isupper, common_case_islower, dict_keys_upper, dict_keys_lower
from ..helpers.py_helper import get_function_name
from ..helpers.sort_helper import str_int_key

# Exceptions
from fexception import FGeneralError, FTypeError


__author__ = "IncognitoCoding"
__copyright__ = "Copyright 2022, dict"
__credits__ = ["IncognitoCoding"]
__license__ = "MIT"
__version__ = "0.3"
__maintainer__ = "IncognitoCoding"
__status__ = "Production"


def string_grouper(
    list_of_strings: list[str],
    grouping_option: int,
    grouping_value: Union[str, int, None] = None,
    case_insensitive: bool = False,
) -> dict[str, list[str]]:
    """
    String grouper will group a list of strings using three different options.

    Each option provides a different type of results but covers any type of desired grouping.

    Args:
        list_of_strings (list[str]):
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
        \t\\- All dictionary keys will return with the common case.\\
        \t\\- For example, lower and upper would be grouped into the same grouping.\\
        \t\\- Disabled by default.

    Raises:
        FTypeError (fexception):
        \t\\- The object value '{list_of_strings}' is not an instance of the required class(es) or subclass(es).
        FTypeError (fexception):
        \t\\- The object value '{grouping_value}' is not an instance of the required class(es) or subclass(es).
        FTypeError (fexception):
        \t\\- The object value '{grouping_option}' is not an instance of the required class(es) or subclass(es).
        FTypeError (fexception):
        \t\\- The object value '{case_insensitive}' is not an instance of the required class(es) or subclass(es).
        FTypeError (fexception):
        \t\\- The grouping_value sent for the grouping is not a string.
        FTypeError (fexception):
        \t\\- The grouping_value sent for the grouping is not a int.
        FGeneralError (fexception):
        \t\\- A general failure occurred while grouping the strings.

    Returns:
        dict[str, list[str]]:\\
        \t\\- A list of grouped strings.

    Return Example:\\
    \t\\- {'JJ-MDF-9200-1_2': ['JJ-MDF-9200-1_2'],\\
    \t    'KV-IDF': ['kv-IDF1-9200-1_2', 'KV-IDF2-9200-1_2'],\\
    \t    'KV-MDF': ['KV-MDF-9200-1_2', 'KV-MDF1-9200-1_2'],\\
    \t    'KZV-MDF1-9200-1_2': ['KZV-MDF1-9200-1_2'],\\
    \t    'TI-IDF': ['TI-IDF1-9200-1_2', 'TI-IDF2-9200-1_2']}
    """
    logger = logging.getLogger(__name__)
    logger.debug(f"=" * 20 + get_function_name() + "=" * 20)
    # Custom flowchart tracking. This is ideal for large projects that move a lot.
    # For any third-party modules, set the flow before making the function call.
    logger_flowchart = logging.getLogger("flowchart")
    logger_flowchart.debug(f"Flowchart --> Function: {get_function_name()}")

    try:
        type_check(value=list_of_strings, required_type=list)
        if grouping_value:
            type_check(value=grouping_value, required_type=(str, int))
        type_check(value=grouping_option, required_type=int)
        type_check(value=case_insensitive, required_type=bool)
    except FTypeError:
        raise

    formatted_list_of_strings = "  - list_of_strings (list):" + str(
        "\n        - " + "\n        - ".join(map(str, list_of_strings))
    )
    if grouping_value:
        formatted_grouping_value = f"  - grouping_value (str or int or None):\n        - {grouping_value}"
    else:
        formatted_grouping_value = f"  - grouping_value (str or int or None):\n        - None"

    logger.debug(
        "Passing parameters:\n"
        f"{formatted_list_of_strings}\n"
        f"{formatted_grouping_value}\n"
        f"  - grouping_option (int):\n        - {grouping_option}\n"
        f"  - case_insensitive (bool):\n        - {case_insensitive}\n"
    )

    logger.debug(f"Starting string grouping with the following list of strings: {list_of_strings}")

    try:
        # Checks if any "None" entries exist.
        if None in list_of_strings:
            logger.debug(f'The list of strings contains "None" string entries. The "None" entries have been removed')
            # Removes any "None" entries from the list.
            list_of_strings = list(filter(None, list_of_strings))
        # Make sure that the list is greater than or equal to 2.
        if len(list_of_strings) >= 2:
            # Holds grouped values from the list.
            grouping: dict[str, list[str]] = {}

            # Sorts with case-insensitive.
            if case_insensitive:
                list_of_strings = sorted(list_of_strings, key=lambda s: s.casefold())
            else:
                list_of_strings = sorted(list_of_strings)

            # Groups based on the user's group option.
            if grouping_option == 1:
                # This section will group based on a character. If the string is "Testing-1" and the matching character was -, the grouping values would match on "Testing".
                # Checks that the grouping_value is a string.
                if isinstance(grouping_value, str):
                    # Loops through a list of strings and splits based on the split number. The split number will create a grouping, and provide the split output for each grouping.
                    if case_insensitive:
                        if common_case_isupper(list_of_strings=list_of_strings):
                            for j, i in groupby(
                                list_of_strings, lambda a_string: a_string.upper().split(grouping_value)[0]
                            ):
                                # Appends the grouping from groupby to the list in in dictionary format.
                                grouping.update({j: list(i)})
                        elif common_case_islower(list_of_strings=list_of_strings):
                            for j, i in groupby(
                                list_of_strings, lambda a_string: a_string.lower().split(grouping_value)[0]
                            ):
                                # Appends the grouping from groupby to the list in in dictionary format.
                                grouping.update({j: list(i)})
                    else:
                        for j, i in groupby(list_of_strings, lambda a_string: a_string.split(grouping_value)[0]):
                            # Appends the grouping from groupby to the list in in dictionary format.
                            grouping.update({j: list(i)})
                else:
                    exc_args = {
                        "main_message": "The grouping_value sent for the grouping is not a string.",
                        "expected_result": """<class 'str'>""",
                        "returned_result": type(grouping_value),
                    }
                    raise FTypeError(exc_args)
            elif grouping_option == 2:
                # This section groups based on a character number. If the string is "Testing" and the number was 3, the grouping values would match on "Tes".
                # Checks that the grouping_value is a number.
                if isinstance(grouping_value, int):
                    group_number: int = grouping_value
                    # Loops through a list of strings and splits based on the split number. The split number will create a grouping, and provide the split output for each grouping.
                    if case_insensitive:
                        if common_case_isupper(list_of_strings=list_of_strings):
                            for j, i in groupby(
                                list_of_strings,
                                lambda a_string: [
                                    str(a_string[index : index + group_number]).upper()
                                    for index in range(0, len(a_string), group_number)
                                ][0],
                            ):
                                # Appends the grouping from groupby to the list in in dictionary format.
                                grouping.update({j: list(i)})
                        elif common_case_islower(list_of_strings=list_of_strings):
                            for j, i in groupby(
                                list_of_strings,
                                lambda a_string: [
                                    str(a_string[index : index + group_number]).lower()
                                    for index in range(0, len(a_string), group_number)
                                ][0],
                            ):
                                # Appends the grouping from groupby to the list in in dictionary format.
                                grouping.update({j: list(i)})
                    else:
                        for j, i in groupby(
                            list_of_strings,
                            lambda a_string: [
                                str(a_string[index : index + group_number])
                                for index in range(0, len(a_string), group_number)
                            ][0],
                        ):
                            # Appends the grouping from groupby to the list in in dictionary format.
                            grouping.update({j: list(i)})
                else:
                    exc_args = {
                        "main_message": "The grouping_value sent for the grouping is not a int.",
                        "expected_result": """<class 'int'>""",
                        "returned_result": type(grouping_value),
                    }
                    raise FTypeError(exc_args)
            elif grouping_option == 3:
                # This comparison can have some complex checks because it has to check previous entries and make choices based on previous and current groupings.
                # The section of code is split into two different loops. The primary loop goes through each string. The sub-string loops and checks character by character
                # between the previous string and current string.
                # All processing is done with the mindset that the current entry is always compared with the previous entry. The comparison is based on alphabetical order.
                # Loops through all raw string imports to compare.
                for raw_string_loop_tracker, string in enumerate(list_of_strings):
                    # Checks if the length of the raw string is equal to the raw_string_loop_tracker + 1. This allows a clean exit without the list going out of the index.
                    if len(list_of_strings) != raw_string_loop_tracker + 1:
                        logger.debug(f'Comparing "{string}" with "{list_of_strings[raw_string_loop_tracker + 1]}"')
                        # Loops through each character in the main string entry.
                        for character_loop_tracker, character in enumerate(string):
                            logger.debug(f"Checking character position {character_loop_tracker}")

                            # Checks if case adjustment needs to be applied.
                            next_raw_value: str
                            if case_insensitive:
                                character = character.casefold()
                                next_raw_value = list_of_strings[raw_string_loop_tracker + 1][
                                    character_loop_tracker
                                ].casefold()
                            else:
                                next_raw_value = list_of_strings[raw_string_loop_tracker + 1][character_loop_tracker]

                            # Checks if the character from the main entry matches the character in the next raw string in the list.
                            # + 1 so the first string entry will compare with this starting entry.
                            if character == next_raw_value:
                                logger.debug(f"Match at character position {character_loop_tracker}")
                            # No match
                            elif character != next_raw_value:
                                logger.debug(f"No Match at character position {character_loop_tracker}")

                                # Case insensitive is supported in this function. Two different variables
                                # needs set to check character matches and set values.
                                # Used for comparing characters. Character get starts at 1, so need to -1.
                                match_characters_check: str
                                if case_insensitive:
                                    match_characters_check = string[0:character_loop_tracker].casefold()
                                else:
                                    match_characters_check = string[0:character_loop_tracker]

                                # Sets the match characters.
                                match_characters_set = string[0:character_loop_tracker]

                                logger.debug(f"Matched characters = {match_characters_check}")
                                if match_characters_set:
                                    # Checks if no groupings have been added.
                                    if not grouping:
                                        # Adds the initial grouping.
                                        grouping.update(
                                            {
                                                match_characters_set: [
                                                    string,
                                                    list_of_strings[raw_string_loop_tracker + 1],
                                                ]
                                            }
                                        )
                                    else:
                                        # Case insensitive is supported in this function. Two different variables
                                        # needs set to check character matches and set values.
                                        # Used for comparing characters. The character starts at 1, so needs to be -1.
                                        previous_group_key_check: str
                                        if case_insensitive:
                                            previous_group_key_check = list(grouping.keys())[-1].casefold()
                                        else:
                                            previous_group_key_check = list(grouping.keys())[-1]

                                        # Gets the previous grouping identifier key.
                                        previous_group_key_set: str = list(grouping.keys())[-1]
                                        # Gets the previous grouping value.
                                        previous_group_values: list[str] = list(grouping.values())[-1]

                                        # Checks if the previous grouping identifier is the same, so the string can be joined into the same group entry.
                                        if match_characters_check == previous_group_key_check:
                                            logger.debug(
                                                f"Previous grouping matches. {previous_group_key_check} = {match_characters_check}"
                                            )

                                            previous_group_values.append(list_of_strings[raw_string_loop_tracker + 1])
                                            grouping[previous_group_key_set] = previous_group_values
                                        else:
                                            # Checks if a single string entry. This is required because a single string entry will have the same group_identifier name as the string until the next entry is matched.
                                            if len(previous_group_values) == 1:
                                                logger.debug(
                                                    f'Previous grouping is a single entry and has matching characters. "{match_characters_check}" in "{previous_group_key_check}"'
                                                )
                                                # Checks if the current match_characters are in the previous_group_keys name.
                                                # Note: The previous_group_keys name will be the full name of the string, so the match has to be the other way for detection.
                                                if match_characters_check in previous_group_key_check:
                                                    logger.debug("Merging previous entry with the current entry")

                                                    # Removes the previous group entry because it will not be merged with the current string group.
                                                    grouping.pop(previous_group_key_set)

                                                    # grouping.remove(grouping[-1])
                                                    # Adds the new grouping to the list with the previous group added as well.
                                                    grouping.update(
                                                        {
                                                            match_characters_set: [
                                                                "".join(previous_group_values),
                                                                list_of_strings[raw_string_loop_tracker + 1],
                                                            ],
                                                        }
                                                    )
                                                else:
                                                    logger.debug(
                                                        f"Previous grouping do not match. {previous_group_key_check} != {match_characters_check}"
                                                    )
                                                    # Adds the new grouping to the list.
                                                    grouping.update(
                                                        {
                                                            match_characters_set: [
                                                                list_of_strings[raw_string_loop_tracker + 1]
                                                            ],
                                                        }
                                                    )
                                            # Compares the previous group to the match to make sure the groupings are the same. The previous_grouping_identifier could contain more characters than the current match, so this flow is required.
                                            elif str(previous_group_key_check) in str(match_characters_check):
                                                logger.debug(
                                                    f'Previous grouping has multiple strings grouped and the group_identifier has the same characters as the match group. "{match_characters_check}" in "{previous_group_key_check}"'
                                                )

                                                previous_group_values.append(
                                                    list_of_strings[raw_string_loop_tracker + 1]
                                                )
                                                grouping[previous_group_key_set] = previous_group_values
                                            else:
                                                logger.debug(
                                                    f"Previous grouping do not match. {previous_group_key_check} != {match_characters_check}"
                                                )
                                                # No match occurred with the previous entry, which means this entry is completely new, so the "group_identifier" will be the name of the string. This will adjust if the next string has a match.
                                                # Note: If no match is made the group_identifier will always be the name of the string because it had nothing to compare itself against.
                                                # Adds the new grouping to the list.
                                                grouping.update(
                                                    {
                                                        list_of_strings[raw_string_loop_tracker + 1]: [
                                                            list_of_strings[raw_string_loop_tracker + 1]
                                                        ],
                                                    }
                                                )
                                else:
                                    logger.debug("No Matching Characters Found")

                                    # Checks if entries have been added to the list. No entries mean the starting entry needs to be added.
                                    if not grouping:
                                        # Adds the starting entry and the next entry because neither of these entries matched on startup.
                                        grouping.update({string: [string]})
                                        grouping.update(
                                            {
                                                list_of_strings[raw_string_loop_tracker + 1]: [
                                                    list_of_strings[raw_string_loop_tracker + 1]
                                                ],
                                            }
                                        )
                                    else:
                                        # Note: If no match is made the group_identifier will always be the name of the string because it had nothing to compare itself against.
                                        # Adds the new grouping to the list.
                                        grouping.update(
                                            {
                                                list_of_strings[raw_string_loop_tracker + 1]: [
                                                    list_of_strings[raw_string_loop_tracker + 1]
                                                ],
                                            }
                                        )
                                # Breaks the lop because no additional characters match.
                                break

                            # Checks if the main string is shorter than the main string. This means no match occurred, so the group_identifier for this entry is main entry.
                            if character_loop_tracker == len(string) - 1:
                                logger.debug("Compare string is longer than the main string")
                                grouping.update({string: [string]})
                                grouping.update(
                                    {
                                        list_of_strings[raw_string_loop_tracker + 1]: [
                                            list_of_strings[raw_string_loop_tracker + 1]
                                        ],
                                    }
                                )

            # Sorts the group keys, and values list.
            # Sorts with case-insensitive.
            if case_insensitive:
                sorted_grouping = {
                    key: sorted(grouping[key], key=lambda s: s.casefold())
                    for key in sorted(grouping, key=lambda s: s.casefold())
                }
                # Adjustes keys based on the common case.
                if common_case_isupper(list_of_strings=list_of_strings):
                    sorted_grouping = dict_keys_upper(sorted_grouping)
                elif common_case_islower(list_of_strings=list_of_strings):
                    sorted_grouping = dict_keys_lower(sorted_grouping)
            # Sorts with case-sensitive.
            else:
                sorted_grouping = {key: sorted(grouping[key]) for key in sorted(grouping)}

            # Returns the list of dictionaries.
            return sorted_grouping
        else:
            # Only one entry was sent. Returning the single entry.
            return {list_of_strings[0]: [list_of_strings[0]]}
    except FTypeError as exc:  # pragma: no cover
        raise
    except Exception as exc:  # pragma: no cover
        exc_args = {
            "main_message": "A general failure occurred while grouping the strings.",
            "original_exception": exc,
        }
        raise FGeneralError(exc_args)


def move_dict_value(
    my_dict: dict[Any, Any],
    src_key: Union[str, int, float, bool],
    dest_key: Union[str, int, float, bool],
    value: Any,
    sort: bool = True,
) -> dict[Union[str, int, float, bool], Any]:
    """
    This function moves dictionary values from one key to another key.

    Sorting will perform on values types (str) or (int). String numbers are supported.

    Single source grouping value entries will get removed.

    Args:
        my_dict (dict[Any, Any]):
        \t\\- The dictionary needing the value moved.
        src_key (Union[str, int, float, bool]):
        \t\\- The source dictionary key for the value being moved.
        dest_key (Union[str, int, float, bool]):
        \t\\- The destination dictionary key for the value being moved.\\
        \t\\- Supports existing or new keys. A new key will make a new entry.
        value (Any):
        \t\\- The value needing moved.
        sort (bool, optional):
        \t\\- Sorts the destination dictionary values.\\
        \t\\- Defaults to True.

    Raises:
        FGeneralError:
        \t\\- A general failure occurred while moving dictionary values.

    Returns:
        dict[Union[str, int, float, bool], Any]:
        \t\\- A revised dictionary with the moved value.
    """
    logger = logging.getLogger(__name__)
    logger.debug(f"=" * 20 + get_function_name() + "=" * 20)
    # Custom flowchart tracking. This is ideal for large projects that move a lot.
    # For any third-party modules, set the flow before making the function call.
    logger_flowchart = logging.getLogger("flowchart")
    logger_flowchart.debug(f"Flowchart --> Function: {get_function_name()}")

    try:
        type_check(value=my_dict, required_type=dict)
        type_check(value=src_key, required_type=(str, int, float, bool))
        type_check(value=dest_key, required_type=(str, int, float, bool))
        type_check(value=sort, required_type=bool)
    except FTypeError:
        raise

    formatted_my_dict = "  - my_dict (dict):\n        - " + "\n        - ".join(
        ": ".join((str(key), str(val))) for (key, val) in my_dict.items()
    )
    logger.debug(
        "Passing parameters:\n"
        f"{formatted_my_dict}\n"
        f"  - src_key (Union[str, int, float, bool]):\n        - {src_key}\n"
        f"  - dest_key (Union[str, int, float, bool]):\n        - {dest_key}\n"
        f"  - sort (bool):\n        - {sort}\n"
    )

    try:
        src_list: list = []
        dest_list: list = []

        if isinstance(my_dict[src_key], list):
            for item in my_dict[src_key]:
                src_list.append(item)
        elif isinstance(my_dict[src_key], (str, int, float, bool)):
            src_list.append(my_dict[src_key])

        # Checks if the destination key exists.
        if any(dest_key == key for key in list(my_dict.keys())):
            if isinstance(my_dict[dest_key], list):
                for item in my_dict[dest_key]:
                    dest_list.append(item)
            elif isinstance(my_dict[dest_key], (str, int, float, bool)):
                dest_list.append(my_dict[dest_key])

        # Removs the value from the source list if the list is not empty.
        if len(src_list) >= 1:
            src_list.remove(value)

        # Adds the value to the destination list.
        dest_list.append(value)
        if sort:
            if dest_list:
                # Checks to determine the type of sort that can be performed.
                # List sort is supported on int/str or int only.
                int_only: bool = True
                int_str_only: bool = True
                for value in dest_list:
                    # Checks if any values are not int.
                    if not isinstance(value, int):
                        int_only = False
                    # Checks if a value is int only.
                    if isinstance(value, int):
                        int_str_only = False
                    # Checks if any values are not int or str.
                    if not "str" in str(type(value)) and not "int" in str(type(value)):
                        int_str_only = False

                # Sorts if the values approved.
                if int_str_only:
                    dest_list.sort(key=str_int_key)
                elif int_only:
                    dest_list.sort(key=int)

        # Removes the source dictionary entry if the list is empty.
        if len(src_list) == 0:
            my_dict.pop(src_key)

        # Updates the source dictionary value if the list is not empty.
        if len(src_list) >= 1:
            my_dict[src_key] = src_list

        # Updates the destination dictionary value.
        my_dict[dest_key] = dest_list

        # Final sort based on the keys.
        if sort:
            my_dict = OrderedDict(sorted(my_dict.items()))
    except Exception as exc:  # pragma: no cover
        exc_args = {
            "main_message": "A general failure occurred while moving dictionary values.",
            "original_exception": exc,
        }
        raise FGeneralError(exc_args)
    else:
        return my_dict
