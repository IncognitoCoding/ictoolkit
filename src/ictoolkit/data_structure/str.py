# Built-in/Generic Imports
import re
import logging
from typing import Union
from warnings import warn

# Libraries
from fchecker.type import type_check

# Local Functions
from ..helpers.py_helper import get_function_name

# Local Exceptions:
from .exceptions import RemoveSectionFailure

# Exceptions
from fexception import FValueError, FCustomException


__author__ = "IncognitoCoding"
__copyright__ = "Copyright 2022, str"
__credits__ = ["IncognitoCoding"]
__license__ = "MIT"
__version__ = "0.5"
__maintainer__ = "IncognitoCoding"
__status__ = "Production"


def list_to_str(value: Union[str, list], sep: str = " ") -> str:
    """
    Take any list and converts the list to a string.\\

    Usage Notes:
    \t\\- If str is sent the original str will forward.\\

    Args:
        value (Union[str, list]):
        \t\\- The list getting converted.
        \t\\- A str will forward through.
        sep (str, optional):
        \t\\- The delimiter that will separate each list entry.
        \t\\- Blanks are supported.
        \t\\- Defaults to a single blank space.

    Raises:
        FTypeError (fexception):
        \t\\- The object value '{value}' is not an instance of the required class(es) or subclass(es).

    Returns:
        str:
        \t\\- A converted list to a string or the original forwarded list.
    """
    logger = logging.getLogger(__name__)
    logger.debug(f"=" * 20 + get_function_name() + "=" * 20)
    # Custom flowchart tracking. This is ideal for large projects that move a lot.
    # For any third-party modules, set the flow before making the function call.
    logger_flowchart = logging.getLogger("flowchart")
    logger_flowchart.debug(f"Flowchart --> Function: {get_function_name()}")

    type_check(value=value, required_type=(str, list), tb_remove_name="list_to_str")

    if isinstance(value, str):
        formatted_value = f"  - string (str):\n        - {value}\n"
    else:
        formatted_value = "  - value (list):" + str("\n        - " + "\n        - ".join(map(str, value)))
    logger.debug("Passing parameters:\n" f"{formatted_value}\n")

    if isinstance(value, list):
        new_list = sep.join(map(str, value))
    else:
        new_list = value

    return new_list


def find_longest_common_substring(string1: str, string2: str) -> Union[str, None]:
    """
    This function finds the longest substring between two different strings.

    Args:
        string1 (string):
        \t\\- string to compare against string2
        string2 (string):
        \t\\- string to compare against string1

    Raises:
        FTypeError (fexception):
        \t\\- The object value '{string1}' is not an instance of the required class(es) or subclass(es).
        FTypeError (fexception):
        \t\\- The object value '{string2}'' is not an instance of the required class(es) or subclass(es).

    Returns:
        str:\\
        \t\\- returns the string up to the point the characters no longer match.
    """
    logger = logging.getLogger(__name__)
    logger.debug(f"=" * 20 + get_function_name() + "=" * 20)
    # Custom flowchart tracking. This is ideal for large projects that move a lot.
    # For any third-party modules, set the flow before making the function call.
    logger_flowchart = logging.getLogger("flowchart")
    logger_flowchart.debug(f"Flowchart --> Function: {get_function_name()}")

    type_check(value=string1, required_type=str, tb_remove_name="find_longest_common_substring")
    type_check(value=string2, required_type=str, tb_remove_name="find_longest_common_substring")

    logger.debug(
        "Passing parameters:\n"
        f"  - string1 (str):\n        - {string1}\n"
        f"  - string2 (str):\n        - {string2}\n"
    )

    def _iter():
        for a, b in zip(string1, string2):
            if a == b:
                yield a
            else:
                return

    substring = None
    if "".join(_iter()):
        substring = "".join(_iter())

    return substring


def clean_non_word_characters(string: str) -> str:
    """
    This function will remove any non-word hex characters from any passing string.

    Strings without non-word hex will be passed through without any errors.

    Args:
        string (str):
        \t\\- A string with non-word hex characters.

    Raises:
        FTypeError (fexception):
        \t\\- The object value '{string}' is not an instance of the required class(es) or subclass(es).
        FValueError (fexception):
        \t\\- The string ({string}) with non-word characters did not clean.

    Returns:
        str:\\
        \t\\- A cleaned string with valid only words.
    """
    logger = logging.getLogger(__name__)
    logger.debug(f"=" * 20 + get_function_name() + "=" * 20)
    # Custom flowchart tracking. This is ideal for large projects that move a lot.
    # For any third-party modules, set the flow before making the function call.
    logger_flowchart = logging.getLogger("flowchart")
    logger_flowchart.debug(f"Flowchart --> Function: {get_function_name()}")

    type_check(value=string, required_type=str, tb_remove_name="clean_non_word_characters")

    logger.debug("Passing parameters:\n" f"  - string (str):\n        - {string}\n")

    # Some Python returned information will return with trailing hex characters (non-words). These are unescaped control characters, which is what Python displays using hexadecimal notation.
    # This expression will remove the hex characters. It can be written with either [^\x20-\x7e] or [^ -~].*
    # Note: When viewing non-word characters it can very from console or logging. You may see output similar BT-NNAK\x06 or BT-NNAK♠ or BT-NNAK\u00006 or BT-NNAK.
    # Example1:
    #   - Input: BT-NNAK\x06
    #   - Output: BT-NNAK
    cleaned_string = re.sub(r"[^ -~].*", "", string)
    encoded_string = cleaned_string.encode("ascii", "ignore")
    if "\\x" in str(encoded_string):  # pragma: no cover
        exc_args = {
            "main_message": f"The string ({string}) with non-word characters did not clean.",
            "expected_result": "The string should not have contained any hex characters.",
            "returned_result": encoded_string,
        }
        raise FValueError(message_args=exc_args, tb_remove_name="clean_non_word_characters")
    else:
        # Checks if the lengths are different from the parameter string and cleaned string to know if the string contained non-word values.
        if len(string) > len(cleaned_string):
            logger.debug(
                f"The string was cleaned of all non-word characters. Set Value (str):\n    - Original Value: {string}\n    - Cleaned Value: {cleaned_string}"
            )
        else:
            logger.debug(f"The string did not contain any non-word characters. No change required.")
        return cleaned_string


def remove_section(orig_value: str, removal_values: Union[str, tuple[str, ...]], sep: str, percent: int = 100) -> str:
    """
    Offers the ability to remove a section of a string using removal value(s).

    Advantages:
    \t\\- Supports sending a "tuple" of values to check against the orig_value for removal.\\
    \t\\- Supports percent match removal values. If a value does not have a full match\\
    \t   it can run through the percent matcher, which checks for common characters (start to end).\\
    \t\\- The sep for the orig_value will work with the removal_value in the removal_values list.\\
    \t\t\\- This is great when stripping subdomains, folders, or websites.

    
    How Removal Works:
    \t\\- Any value that does not match the delimiter, will skip.\\
    \t\\- The removal_values will sort in reverse order, so sub-domains are checked\\
    \t    before the parent domain. Parent domains would strip and leave the\\
    \t    sub-domain on the name without the reverse sort.

    Args:
        orig_value (str):
        \t\\- The orig_value that needs a domain removed.
        removal_values (Union[str, Tuple[str, ...]]):
        \t\\- A single removal value or a tuple of values used for match removal.\\
        \t\\- These values can range from single strings, statements, domains\\
        \t   folders, websites, etc.
        sep (str):
        \t\\- The delimiter needed to separate the orig_value and get specific sections.\\
        \t\\- The same delimiter can be used to split the removal value(s) for comparison.\\
        \t\\- An empty string is not supported, but blank spaces are.\\
        \t\\- If your string needs no delimiter, use one of Python's built-ins.
        percent (int):
        \t\\- How much match percentage is required (1-100).
        \t\\- If a full removal value does not match a percent match will attempt.\\
        \t\\- If no percent match occurs, a warning message will flag.
        \t\\- Percent matching calculations >= 99 will add additional compute time.\\
        \t\\- Defaults to 100.

    Raises:
        FTypeError (fexception):
        \t\\- The object value '{orig_value}' is not an instance of the required class(es) or subclass(es).
        FTypeError (fexception):
        \t\\- The object value '{removal_values}' is not an instance of the required class(es) or subclass(es).
        FTypeError (fexception):
        \t\\- The removal_values arg requires a tuple of strings.
        RemoveSectionFailure:
        \t\\- Unexpected stripped_orig_value value of None.

    Returns:
        str:\\
        \t\\- A orig_value with a stripped removal value.
    """
    logger = logging.getLogger(__name__)
    logger.debug(f"=" * 20 + get_function_name() + "=" * 20)
    # Custom flowchart tracking. This is ideal for large projects that move a lot.
    # For any third-party modules, set the flow before making the function call.
    logger_flowchart = logging.getLogger("flowchart")
    logger_flowchart.info(f"Flowchart --> Function: {get_function_name()}")

    type_check(value=orig_value, required_type=str, tb_remove_name="remove_section")
    type_check(value=removal_values, required_type=(str, tuple), tb_remove_name="remove_section")
    if isinstance(removal_values, tuple):
        for value in removal_values:
            type_check(
                value=value,
                required_type=str,
                tb_remove_name="remove_section",
                msg_override="Invalid tuple value type. The removal_values arg requires a tuple of strings.",
            )
    type_check(value=sep, required_type=str, tb_remove_name="remove_section")
    type_check(value=percent, required_type=int, tb_remove_name="remove_section")

    formatted_removal_values = "  - removal_values (list):" + str(
        "\n        - " + "\n        - ".join(map(str, removal_values))
    )
    logger.debug(
        "Passing parameters:\n"
        f"  - orig_value (str):\n        - {orig_value}\n"
        f"{formatted_removal_values}\n"
        f"  - sep (str):\n        - {sep}\n"
        f"  - percent (int):\n        - {percent}\n"
    )

    stripped_orig_value: Union[str, None] = None
    adjusted_removal_values: list[str] = []

    # Checks if string or tuple to set the adjusted_removal_value list.
    if isinstance(removal_values, tuple):
        if sep in str(removal_values):
            # Sorts the removal list to have the sub-domains/sub-directories/etc. sorted before the parent.
            # Sort Example:
            # Original: ['sample.org', 'home.sample.org', 'redcolor.org', 'home.redcolor.org', 'sim.redcolor.org', 'amp.redcolor.org']
            # Sorted: ['home.sample.org', 'sample.org', 'sim.redcolor.org', 'home.redcolor.org', 'amp.redcolor.org', 'redcolor.org']
            adjusted_removal_values = sorted(removal_values, key=lambda x: list(reversed(x.split(sep))), reverse=True)
        else:
            # No separator in the removal values.
            adjusted_removal_values = sorted(removal_values)
    else:
        # String value. Adding to the removal list.
        adjusted_removal_values.append(removal_values)

    # Checks if the orig_value contains a sep.
    if sep in orig_value:
        for removal_value in adjusted_removal_values:
            if removal_value in orig_value:
                stripped_orig_value = orig_value.split(sep=f"{sep}{removal_value}")[0]
                logger.debug(
                    f"Removed the removal_value from the orig_value'"
                    f"\n  - original = {orig_value}"
                    f"\n  - stripped = {stripped_orig_value}"
                )
                break

        # Checks if percent matching is enabled.
        # If the removal_value list does not match the original orig_value will return with the extension.
        if int(percent) <= 99 and None is stripped_orig_value:
            logger.debug(
                "No removal_value was found in the orig_value. Performing a percent check in case the orig_value was cut off because of length"
            )
            last_section_match: bool = False
            # Attempt to match based on value matches. Some values may not always match a complete removal
            # value but can match a percent value.
            for removal_value_index, removal_value in enumerate(adjusted_removal_values):
                # Splits the orig_value and removal_value at the 'sep' to form
                # sections. Sections can be the orig_value, subdomain, domain subfolder, folder, etc.
                split_orig_value: list[str] = orig_value.split(sep)
                split_removal_value: list[str] = removal_value.split(sep)
                logger.debug(
                    f"The orig_value and potential removal_value({removal_value_index + 1} of {len(adjusted_removal_values)}) match are split"
                    f"\n  - split_orig_value = {split_orig_value}"
                    f"\n  - split_removal_value = {split_removal_value}"
                )

                # Loops through each removal_value entry to check if percent ending matches.
                section_match: list[str] = []
                for orig_value_section_index, orig_value_section in enumerate(split_orig_value):
                    # Compares the split removal_value section against all split orig_value sections for any matches.
                    match = [
                        removal_value_section
                        for removal_value_section in split_removal_value
                        if removal_value_section.startswith(orig_value_section)
                    ]

                    # Adds amatches to the list.
                    if len(match) == 1:
                        if match[0] == orig_value_section:
                            logger.debug(
                                f"A full match was found at split section {orig_value_section_index + 1} of {len(split_orig_value)}"
                                f"\n  - full = {orig_value_section}"
                            )
                        else:
                            logger.debug(
                                f"A percent match was found between the orig_value and removal_value was found at split section "
                                f"{orig_value_section_index + 1} of {len(split_orig_value)}"
                                f"\n  - partial = {orig_value_section}\n  - full = {match[0]}"
                            )

                        # Adds the orig_value section.
                        section_match.append(orig_value_section)

                        # Check if the match was on the last element of the split orig_value list.
                        if orig_value_section == split_orig_value[-1]:
                            logger.debug("The final sections matched. The percent match has been satisfied")
                            last_section_match = True

                # Breaks because the percent match is complete.
                if last_section_match:
                    # Checks which stat section matches the orig_value. The section that matches is the section that will
                    # strip anything after.
                    for section in section_match:
                        if section in orig_value:
                            logger.debug(
                                f"The section ({section}) was found in the orig_value ({orig_value}).\n"
                                "Checking if the section_match has a high enough match percentage to split"
                            )

                            # Checks if the percent section match is within the allowed percentage range of the removal value.
                            if len(sep.join(section_match)) / len(removal_value) >= float(percent) / 100.0:
                                # Strips the removal_value based on the first entry in the section match list.
                                # Two entries will exist in the list.
                                stripped_orig_value = orig_value.split(sep=f"{sep}{section}")[0]
                                logger.debug(
                                    f"The orig_value ({orig_value}) match is high enough for removal"
                                    f"\n  - split percentage match = {len(sep.join(section_match)) / len(removal_value)}"
                                    f"\n  - required percentage match = {float(percent) / 100.0}"
                                )
                                logger.debug(
                                    f"Removing the percent removal_value from the orig_value starting at section '{section}'"
                                    f"\n  - original = {orig_value}"
                                    f"\n  - stripped = {stripped_orig_value}"
                                )
                                break
                            else:
                                logger.debug(
                                    f"The removal value ({removal_value}) contains {len(removal_value)} characters and the "
                                    f"orig_value section split delimiter ({sep.join(section_match)}) contains {len(sep.join(section_match))}"
                                )
                                logger.debug(
                                    f"The orig_value ({orig_value}) did not have a section removed because the percentage match was not high enough"
                                    f"\n  - split percentage match = {len(sep.join(section_match)) / len(removal_value)}"
                                    f"\n  - required percentage match = {float(percent) / 100.0}"
                                )

                                break
                    # Checks if the split did not take place because of a percentage check.
                    if not stripped_orig_value:
                        # Sets the original orig_value.
                        stripped_orig_value = orig_value

                    break

            if not last_section_match:
                warning_msg = (
                    f"The processing orig_value ({orig_value}) contains a '{sep}' but has no removal_value(s) match"
                    "\n  - removal_values = " + ", ".join(adjusted_removal_values) + "\n  - Action:"
                    "\n    - Please verify you have all potential matching removal_value(s)."
                    "\n    - If some orig_value entries have the potential to not match, please verify the orig_value "
                    "is a value needing to be stripped."
                )
                logger.warning(warning_msg)
                warn(warning_msg)

                # Sets the original orig_value.
                stripped_orig_value = orig_value
        elif int(percent) == 100 and None is stripped_orig_value:
            # Sets the original orig_value.
            stripped_orig_value = orig_value
    else:
        # Sets the stripped orig_value.
        stripped_orig_value = orig_value

    if stripped_orig_value:
        # Returns a stripped removal_value or the original orig_value depending on a match.
        return stripped_orig_value
    else:  # pragma: no cover
        exc_args: dict = {
            "main_message": "Unexpected stripped_orig_value value of None.",
            "custom_type": RemoveSectionFailure,
            "expected_result": "A string value",
            "returned_result": None,
        }
        raise RemoveSectionFailure(FCustomException(message_args=exc_args, tb_remove_name="remove_section"))
