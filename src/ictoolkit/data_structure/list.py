# Built-in/Generic Imports
import logging
from typing import Union, List, Any, Optional

# Libraries
from fchecker.type import type_check

# Local Functions
from ..helpers.py_helper import get_function_name
from ..helpers.sort_helper import str_int_key

# Exceptions
from fexception import FKeyError, FValueError


__author__ = "IncognitoCoding"
__copyright__ = "Copyright 2022, list"
__credits__ = ["IncognitoCoding"]
__license__ = "MIT"
__version__ = "0.5"
__maintainer__ = "IncognitoCoding"
__status__ = "Production"


def find_substring(value: str, start_match: str, end_match: str) -> Union[list, None]:
    """
    Finds a substring based on the start and end match values.

    Multiple substring detection is supported.

    Args:
        value (str):
        \t\\- The value containing substrings.
        start_match (str):
        \t\\- The start matching substring.
        end_match (str):
        \t\\- The end matching substring.

    Raises:
        FTypeError (fexception):
        \t\\- The object value '{value}' is not an instance of the required class(es) or subclass(es).
        FTypeError (fexception):
        \t\\- The object value '{start_match}' is not an instance of the required class(es) or subclass(es).
        FTypeError (fexception):
        \t\\- The object value '{end_match}' is not an instance of the required class(es) or subclass(es).

    Returns:
        Union[list, None]:
        \t\\- list:\\
        \t\t\\- A list of matching substrings.\\
        \t\\- None:\\
        \t\t\\- No matching substrings.
    """
    logger = logging.getLogger(__name__)
    logger.debug(f"=" * 20 + get_function_name() + "=" * 20)
    # Custom flowchart tracking. This is ideal for large projects that move a lot.
    # For any third-party modules, set the flow before making the function call.
    logger_flowchart = logging.getLogger("flowchart")
    logger_flowchart.debug(f"Flowchart --> Function: {get_function_name()}")

    type_check(value=value, required_type=str, tb_remove_name="find_section")
    type_check(value=start_match, required_type=str, tb_remove_name="find_section")
    type_check(value=end_match, required_type=str, tb_remove_name="find_section")

    logger.debug(
        "Passing parameters:\n"
        f"  - value (str):\n        - {value}\n"
        f"  - start_match (str):\n        - {start_match}\n"
        f"  - end_match (str):\n        - {end_match}\n"
    )

    try:
        logger.debug(f"Checking if a section is between the start ({start_match}) and end ({end_match}) characters")

        matched_substrings: list[str] = []

        # Gets the initial value section.
        start: int = value.index(start_match) + len(start_match)
        end: int = value.index(end_match, start)

        matched_substrings.append(value[start:end])

        logger.debug(f"A section was found and added to the list\n  - {value[start:end]}")
        logger.debug(f"Starting a loop to see if any other sections exist")

        # Stores the stripped value.
        stripped_value: str = value
        # Loops through until all sections are found.
        while True:
            # Stripps the ending plus 1 to remove the separator.
            stripped_value = stripped_value[end + 1 :]
            # Checks if any other groupings exist.
            if start_match in stripped_value and end_match in stripped_value:
                logger.debug("Another section was detected")
                start: int = stripped_value.index(start_match) + len(start_match)
                end: int = stripped_value.index(end_match, start)
                matched_substrings.append(stripped_value[start:end])
                logger.debug(f"An additional section was found and added to the list\n  - {stripped_value[start:end]}")
            else:
                break

        logger.debug(f"Returning {len(matched_substrings)} sections\n  - {matched_substrings}")
        return matched_substrings
    except ValueError:
        logger.debug(f"No sections exist in the value")
        # Returns none if no substring if found.
        return None


def str_to_list(
    value: Union[str, list], sep: str, remove_whitespace: bool = True, exclude: Optional[str] = None
) -> list[Any]:
    """
    Take any string and converts it based on the separator.\\
    The difference between this function and .split() is that\\
    this function allows lists to pass through and sections of\\
    the value to be excluded.

    Ideal for converting database cells that were converted from\\
    list to str for storage. Ex: .join('my_list_values') or list_to_str(value=[1,2])

    The exclude can be beneficial when part of a string needs to be converted,\\
    but another section with a matching separator must remain intact.

    Whitespace is stripped automatically.

    Usage Notes:
    \t\\- If a list is sent the original list will forward.\\
    \t\\- If the separator never matches the entry will be considered\\
    \t   a single entry and add to the list.

    Args:
        value (Union[str, list]):
        \t\\- The string getting split.
        \t\\- A list will forward through.
        sep (str):
        \t\\- The delimiter that will split the string.
        remove_whitespace (bool, optional):
        \t\\- Removes whitespace.
        \t\\- Defaults to True.
        exclude (str, optional):
        \t\\- A character to use for excluding the string section from splitting.\\
        \t\\- Use a unique character that will never match a common string (ex: ~, [, ^, •).\\
        \t\\- NOTE:
        \t\t\\- A single exclude will exclude values after.\\
        \t\t\\- Start and end exclude will exclude a section.\\
        \t\t\\- Multiple start/end excludes are supported.

    Raises:
        FTypeError (fexception):
        \t\\- The object value '{value}' is not an instance of the required class(es) or subclass(es).
        FTypeError (fexception):
        \t\\- The object value '{sep}' is not an instance of the required class(es) or subclass(es).
        FTypeError (fexception):
        \t\\- The object value '{remove_whitespace}' is not an instance of the required class(es) or subclass(es).
        FTypeError (fexception):
        \t\\- The object value '{exclude}' is not an instance of the required class(es) or subclass(es).
        FValueError (fexception):
        \t\\- The 'exclude' value must contain only one character.

    Returns:
        list[Any]:
        \t\\- A converted string to a list or the original forwarded list.\\
        \t\\- Empty lists can pass through.
    """
    logger = logging.getLogger(__name__)
    logger.debug(f"=" * 20 + get_function_name() + "=" * 20)
    # Custom flowchart tracking. This is ideal for large projects that move a lot.
    # For any third-party modules, set the flow before making the function call.
    logger_flowchart = logging.getLogger("flowchart")
    logger_flowchart.debug(f"Flowchart --> Function: {get_function_name()}")

    type_check(value=value, required_type=(str, list), tb_remove_name="str_to_list")
    type_check(value=sep, required_type=str, tb_remove_name="str_to_list")
    type_check(value=remove_whitespace, required_type=bool, tb_remove_name="str_to_list")
    if exclude:
        type_check(value=exclude, required_type=str, tb_remove_name="str_to_list")

    if isinstance(value, str):
        formatted_value = f"  - string (str):\n        - {value}\n"
    else:
        formatted_value = "  - value (list):" + str("\n        - " + "\n        - ".join(map(str, value)))

    logger.debug(
        "Passing parameters:\n"
        f"{formatted_value}\n"
        f"  - sep (str):\n        - {sep}\n"
        f"  - remove_whitespace (bool):\n        - {remove_whitespace}\n"
        f"  - exclude (str):\n        - {exclude}\n"
    )

    if exclude:
        # Checks that only one exclude character was sent.
        if len(exclude) >= 2:
            exc_args = {
                "main_message": "The 'exclude' value must contain only one character.",
                "expected_result": "1",
                "returned_result": len(exclude),
            }
            raise FValueError(message_args=exc_args, tb_remove_name="str_to_list")

    new_list: list[str] = []
    constructed_string: str = ""
    ignore: bool = False

    if isinstance(value, str):
        logger.debug(f"Splitting all string characters\n  - Total Characters = {len(value)}")
        # Checks if an exclude is included to use a more in-depth split process.
        if exclude:
            for index, character in enumerate(value):
                # Checks if the character is excluded.
                # This will enable or disable the grouping.
                if character == exclude:
                    ignore = True if ignore == False else False
                    logger.debug(
                        f"Ignore Character: {character} at position {index}.... Previous Character is {value[index - 1]}"
                    )
                    logger.debug(f"Setting ignore to {ignore}")
                else:
                    # Adds each character to the string.
                    constructed_string += character

                if (
                    (character == sep and not ignore)
                    or (len(value) == index + 1)
                    or (not ignore and value[index + 1] == exclude)
                ):
                    # Removes whitespace.
                    if remove_whitespace:
                        logger.debug("Removing whitepsace from the constructed string")
                        constructed_string = constructed_string.strip()

                    logger.debug(f"Adding the constructed string to the list\n  - {constructed_string}")
                    # Adds the populated string to the results list.
                    new_list.append(constructed_string)
                    # Clears the values.
                    constructed_string = ""
        else:
            # Converts if the delimiter is in the value.
            if sep in str(value):
                new_list = str(value.strip()).split(sep)
            else:
                new_list.append(value.strip())
    else:
        new_list = value

    logger.debug(f"Returning the list\n  - {new_list}")
    return new_list


def remove_duplicate_dict_values_in_list(list_dictionary: List[dict], element_number: Optional[int] = None) -> list:
    """
    Removes duplicate values in a dictionary within a list and returns
    the same list minus duplicates.

    This function will convert a list of dictionaries into a list of tuples
    that contains items of the dictionary for duplicate removal.

    A list of dictionaries are sometimes needed to be sorted based on a specific
    element in the dictionary entry.

    This function offers the ability to choose which element number to use for matching
    or match the entire dictionary element.

    Args:
        list_dictionary (List[dict]):
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
        \t\\- The object value '{list_dictionary}' is not an instance of the required class(es) or subclass(es).
        FTypeError (fexception):
        \t\\- The object value '{element_number}' is not an instance of the required class(es) or subclass(es).

    Returns:
        list:\\
        \t\\- A list of dictionars with duplicate values removed.
    """
    logger = logging.getLogger(__name__)
    logger.debug(f"=" * 20 + get_function_name() + "=" * 20)
    # Custom flowchart tracking. This is ideal for large projects that move a lot.
    # For any third-party modules, set the flow before making the function call.
    logger_flowchart = logging.getLogger("flowchart")
    logger_flowchart.debug(f"Flowchart --> Function: {get_function_name()}")

    type_check(value=list_dictionary, required_type=list, tb_remove_name="remove_duplicate_dict_values_in_list")
    if element_number:
        type_check(value=element_number, required_type=int, tb_remove_name="remove_duplicate_dict_values_in_list")

    formatted_list_dictionary = "  - list_dictionary (list):" + str(
        "\n        - " + "\n        - ".join(map(str, list_dictionary))
    )
    if element_number:
        formatted_element_number = f"  - element_number (int):\n        - {element_number}"
    else:
        formatted_element_number = f"  - element_number (int):\n        - None"
    logger.debug("Passing parameters:\n" f"{formatted_list_dictionary}\n" f"{formatted_element_number}\n")

    # Holds temporary found elements for comparison.
    element_found = set()
    # Stores the revised list that does not contain any duplicates.
    revised_list = []

    # Loops through each dictionary in the list
    for dictionary_in_list in list_dictionary:
        # Checks if section number is being used for matching or a full match is being used.
        if element_number is None:
            # Used tuple because it can be hashed, which allows removal using set.
            # This will convert the dictionaries in the list to tuples that contain the dictionaries.
            # Sorted is added to help with any possible match issues while adding/removing lots of key history.
            items_of_dictionary = tuple(sorted(dictionary_in_list.items()))
            # Checks if dictionary entry matches previous entries.
            if items_of_dictionary not in element_found:
                # New element found and adding to set.
                element_found.add(items_of_dictionary)

                # Adds the full dictionary_in_list to the list because it is not a duplicate.
                revised_list.append(dictionary_in_list)
        elif element_number:
            # Used tuple because it can be hashed, which allows removal using set.
            # This will convert the dictionaries in the list to tuples that contain the dictionaries.
            # No sort is added here because sort will break the element number order.
            items_of_dictionary = tuple(dictionary_in_list.items())
            # Checks if dictionary element section does not match previous entries.
            if items_of_dictionary[element_number] not in element_found:
                # New element found and adding to set.
                element_found.add(items_of_dictionary[element_number])

                # Adds the full dictionary_in_list to the list because it is not a duplicate.
                revised_list.append(dictionary_in_list)

    return revised_list


def get_list_of_dicts_duplicates(
    key: str, list_dictionary: List[dict], grouped: bool = False
) -> Union[list, dict, None]:
    """
    This function finds duplicate dictionary values in the list using the key and return the value and index points.

    Duplicates can be either un-grouped or grouped. Default is un-grouped.

    Returning both the duplicate and original list index points allows any modification or additional data search when the duplicates return.

    A key is required to find all duplicates for that key.

    Args:
        key (str):
        \t\\- the dictionary key that needs to get all duplicate values assigned to that ke
        list_dictionary (List[dict]):
        \t\\- dictionary with duplicate values in a list
        grouped (bool):
        \t\\- enables grouping of duplicate values.\\
        \t\\- Disabled by default

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

    Raises:
        FTypeError (fexception):
        \t\\- The object value '{key}' is not an instance of the required class(es) or subclass(es).
        FTypeError (fexception):
        \t\\- The object value '{list_dictionary}' is not an instance of the required class(es) or subclass(es).
        FTypeError (fexception):
        \t\\- The object value '{grouped}' is not an instance of the required class(es) or subclass(es).
        FKeyError (fexception):
        \t\\- A failure occurred getting duplicate values the list.

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
    logger.debug(f"=" * 20 + get_function_name() + "=" * 20)
    # Custom flowchart tracking. This is ideal for large projects that move a lot.
    # For any third-party modules, set the flow before making the function call.
    logger_flowchart = logging.getLogger("flowchart")
    logger_flowchart.debug(f"Flowchart --> Function: {get_function_name()}")

    type_check(value=key, required_type=str, tb_remove_name="get_list_of_dicts_duplicates")
    type_check(value=list_dictionary, required_type=list, tb_remove_name="get_list_of_dicts_duplicates")
    type_check(value=grouped, required_type=bool, tb_remove_name="get_list_of_dicts_duplicates")

    formatted_list_dictionary = "  - list_dictionary (list):" + str(
        "\n        - " + "\n        - ".join(map(str, list_dictionary))
    )
    logger.debug(
        "Passing parameters:\n"
        f"  - key (int):\n        - {key}\n"
        f"{formatted_list_dictionary}\n"
        f"  - grouped (bool):\n        - {grouped}\n"
    )

    try:
        # Temporary storage for unique items.
        temp_unique_items = []
        # Stores duplicate list entries as dictionaries.
        # The key is the duplicate from the list and the value is the index.
        duplicate_list_dictionary = []
        # Gets values of the keys.
        duplicates_of_key = [my_dict[key] for my_dict in list_dictionary]

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
            elif (
                bool(duplicate_list_dictionary) is False
                or f"'value': {entry}" not in str(duplicate_list_dictionary)
                and f"'value': '{entry}'" not in str(duplicate_list_dictionary)
            ):
                # Loops through all entries in the list.
                for index, value in enumerate(duplicates_of_key):
                    # Checks if the value from the list is equal to the discovered duplicate.
                    if value == entry:
                        # Adds the duplicate entry values and index
                        # The value will be the key and the index will be the value.
                        # This will allow the ease if finding all index points for a specific value.
                        duplicate_list_dictionary.append({"index": index, "value": value})
    except KeyError:  # pragma: no cover
        exc_args = {
            "main_message": "A failure occurred getting duplicate values the list.",
            "expected_result": f"The searching key ({key}) existing in the dictionary",
            "returned_result": f"The searching key ({key}) does not existing in the dictionary ({list_dictionary})",
            "suggested_resolution": "Please verify you have set all required keys and try again.",
        }
        raise FKeyError(message_args=exc_args, tb_remove_name="get_list_of_dicts_duplicates")
    else:
        # Checks that duplicates exist.
        if duplicate_list_dictionary:
            # Checks if the user enabled grouping.
            if grouped:
                # Stores new grouped entries
                grouped_entries: dict[str, list[Any]] = {}
                # Loops through each grouped entry.
                for entry in duplicate_list_dictionary:
                    # Gets matching entries based on the "value" key and adds them to the grouped dictionary.
                    grouped_entries[entry["value"]] = grouped_entries.get(entry["value"], [])
                    grouped_entries[entry["value"]].append(entry)

                # Returns grouped duplicates.
                return grouped_entries
            else:
                # Returns un-grouped duplicates.
                return duplicate_list_dictionary
        else:
            return None


def get_list_duplicates(
    duplicates: list, match_index: Optional[int] = None, grouped: bool = False
) -> Union[list, dict, None]:
    """
    Finds duplicate entries in the list and return the value and index points.

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

    Calling Examples:
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
        \t\\- The object value '{duplicates}' is not an instance of the required class(es) or subclass(es).
        FTypeError (fexception):
        \t\\- The object value '{match_index}' is not an instance of the required class(es) or subclass(es).
        FTypeError (fexception):
        \t\\- The object value '{grouped}' is not an instance of the required class(es) or subclass(es).

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
    logger.debug(f"=" * 20 + get_function_name() + "=" * 20)
    # Custom flowchart tracking. This is ideal for large projects that move a lot.
    # For any third-party modules, set the flow before making the function call.
    logger_flowchart = logging.getLogger("flowchart")
    logger_flowchart.debug(f"Flowchart --> Function: {get_function_name()}")

    type_check(value=duplicates, required_type=list, tb_remove_name="get_list_duplicates")
    if match_index:
        type_check(value=match_index, required_type=int, tb_remove_name="get_list_duplicates")
    type_check(value=grouped, required_type=bool, tb_remove_name="get_list_duplicates")

    formatted_duplicates = "  - duplicates (list):" + str("\n        - " + "\n        - ".join(map(str, duplicates)))
    if match_index:
        formatted_match_index = f"  - match_index (int):\n        - {match_index}"
    else:
        formatted_match_index = f"  - match_index (int):\n        - None"
    logger.debug(
        "Passing parameters:\n"
        f"{formatted_duplicates}\n"
        f"{formatted_match_index}\n"
        f"  - grouped (bool):\n        - {grouped}\n"
    )

    # Temporary storage for unique items.
    temp_unique_items = []
    # Stores duplicate list entries as dictionaries.
    # The key is the duplicate from the list and the value is the index.
    duplicate_list_dictionary = []

    for entry in duplicates:
        # Checks if the entry in the list is another list.
        # This allows lists to be in a list and be searched.
        if isinstance(entry, list) or isinstance(entry, tuple):
            # Checks that a match_index is given to match a specific index in the list entry.
            if isinstance(match_index, int):
                # Checks if the entry from the list exists in the "temp_unique_items" list. If not it gets added to the temp list.
                # If the entry exists the entry will hit the elif statement and get all index points for the duplicates.
                if entry[match_index] not in temp_unique_items:
                    # Adds the entry to the list.
                    temp_unique_items.append(entry[match_index])
                # Checks if the duplicate entry already exists in the duplicate_list_dictionary list.
                # This has to check if the 'duplicate_list_dictionary' is empty and if the duplicate list does not contain the entry.
                # The two different "entry" searches are required in case the key is a string or an INT. A string would have a single quote and an INT would not.
                elif (
                    bool(duplicate_list_dictionary) is False
                    or f"'value': {entry[match_index]}" not in str(duplicate_list_dictionary)
                    and f"'value': '{entry[match_index]}'" not in str(duplicate_list_dictionary)
                ):
                    # Loops through all entries in the list.
                    for index, value in enumerate(duplicates):
                        # Checks if the value from the list is equal to the discovered duplicate.
                        if value[match_index] == entry[match_index]:
                            # Adds the duplicate entry values and index
                            # The value will be the key and the index will be the value.
                            # This will allow the ease if finding all index points for a specific value.
                            duplicate_list_dictionary.append({"index": index, "value": value})
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
                elif (
                    bool(duplicate_list_dictionary) is False
                    or f"'value': {str(entry)}" not in str(duplicate_list_dictionary)
                    and f"'value': '{str(entry)}'" not in str(duplicate_list_dictionary)
                ):
                    # Loops through all entries in the list.
                    for index, value in enumerate(duplicates):
                        # Checks if the value from the list is equal to the discovered duplicate.
                        if str(value) == str(entry):
                            # Adds the duplicate entry values and index
                            # The value will be the key and the index will be the value.
                            # This will allow the ease if finding all index points for a specific value.
                            duplicate_list_dictionary.append({"index": index, "value": value})
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
            elif (
                bool(duplicate_list_dictionary) is False
                or f"'value': {entry}" not in str(duplicate_list_dictionary)
                and f"'value': '{entry}'" not in str(duplicate_list_dictionary)
            ):
                # Loops through all entries in the list.
                for index, value in enumerate(duplicates):
                    # Checks if the value from the list is equal to the discovered duplicate.
                    if value == entry:
                        # Adds the duplicate entry values and index
                        # The value will be the key and the index will be the value.
                        # This will allow the ease if finding all index points for a specific value.
                        duplicate_list_dictionary.append({"index": index, "value": value})

    # Checks that duplicates exist.
    if duplicate_list_dictionary:
        # Checks if the user enabled grouping.
        if grouped:
            # Stores new grouped entries
            grouped_entries: dict[str, list[Any]] = {}
            # Loops through each grouped entry.
            for entry in duplicate_list_dictionary:
                # Checks if the match_index is set to match a specific list index in the list entry.
                if isinstance(match_index, int):
                    # Checks if the values being returned are a tuple.
                    # If tuple the matched_index will be used to set the key.
                    # This is required because single value will be a string and the index will only pull the first letter.
                    # Output Example: {'index': 0, 'value': ('ValueA', 'ValueB')}
                    if isinstance(entry["value"], tuple):
                        # Gets matching entries based on the "value" key and adds them to the grouped dictionary.
                        grouped_entries[str(entry["value"][match_index])] = grouped_entries.get(
                            str(entry["value"][match_index]), []
                        )
                        grouped_entries[str(entry["value"][match_index])].append(entry)
                    # Means only one entry exists as the value, and the value type is a string.
                    # Output Example: {'index': 3, 'value': 'ValueB'}
                    else:
                        # Gets matching entries based on the "value" key and adds them to the grouped dictionary.
                        grouped_entries[str(entry["value"])] = grouped_entries.get(str(entry["value"]), [])
                        grouped_entries[str(entry["value"])].append(entry)
                # Checks if no match_index exists, which matches the entire list entry.
                # The list entry is converted to a string for the key.
                elif not isinstance(match_index, int):
                    # Gets matching entries based on the "value" key and adds them to the grouped dictionary.
                    grouped_entries[str(entry["value"])] = grouped_entries.get(str(entry["value"]), [])
                    grouped_entries[str(entry["value"])].append(entry)
                # Standard string element in the list.
                else:
                    # Gets matching entries based on the "value" key and adds them to the grouped dictionary.
                    grouped_entries[entry["value"]] = grouped_entries.get(entry["value"], [])
                    grouped_entries[entry["value"]].append(entry)

            # Returns grouped duplicates.
            return grouped_entries
        else:
            # Returns un-grouped duplicates.
            return duplicate_list_dictionary
    else:
        return None


def sort_list(my_list: list[Any]) -> list[Any]:
    """
    Mixed types (ex: int, str) can not be sorted together by default.

    This function sorts a list of any value based on the string equivalent.

    Strings and Integers will sort nicely. Other values like\\
    Bool will sort alphabetically.

    Examples:
    \t\\- 1 = "1"\\
    \t\\- True = "True"\\
    \t\\- Bool = "Bool"

    Args:
        my_list (list[Any]):
        \t\\- The list needing sorted.

    Raises:
        FTypeError (fexception):
        \t\\- The object value '{my_list}' is not an instance of the required class(es) or subclass(es).

    Returns:
        list[Any]:
        \t\\- A sorted list based on the string equivalent.
    """
    logger = logging.getLogger(__name__)
    logger.debug(f"=" * 20 + get_function_name() + "=" * 20)
    # Custom flowchart tracking. This is ideal for large projects that move a lot.
    # For any third-party modules, set the flow before making the function call.
    logger_flowchart = logging.getLogger("flowchart")
    logger_flowchart.debug(f"Flowchart --> Function: {get_function_name()}")

    type_check(value=my_list, required_type=list, tb_remove_name="sort_list")

    formatted_my_list = "  - my_list (list):" + str("\n        - " + "\n        - ".join(map(str, my_list)))

    logger.debug("Passing parameters:\n" f"{formatted_my_list}\n")

    # Stores the original type, so it can be converted back.
    orig_type: dict[Any, Any] = {}
    converted_list: list[str] = []

    # Checks if the values are all int or a mix.
    all_int = all(str(value).isdigit() for value in my_list)

    if all_int:
        my_list.sort()
        sorted_list = my_list
    else:
        contains_int: bool = False
        contains_str: bool = False
        # Gets the original type and sets the converted list.
        for value in my_list:
            orig_type.update({str(value): type(value)})

            # Tracks value type for sorting.
            if isinstance(value, int):
                contains_int = True
            elif isinstance(value, str):
                contains_str = True

            converted_list.append(str(value))

        # Converts the int, int/str or str list.
        # Checks which type to cut down on processing time.
        if contains_int and not contains_str:
            converted_list.sort(key=int)
        elif contains_int and contains_str:
            converted_list.sort(key=str_int_key)
        else:
            converted_list.sort()

        # Re-converts the values back to the original type.
        sorted_list: list[Any] = []
        for value in converted_list:
            # Checks if the value was a list to reconstruct the list.
            if "<class 'list'>" in str(orig_type[value]):
                # Uses eval to convert the str[list] back to the original list.
                sorted_list.append(eval(value))
            else:
                # Looks up original type in the dictionary and adds the value
                # with the original type to the sorted list.
                sorted_list.append(orig_type[value](value))

    return sorted_list
