# Built-in/Generic Imports
import logging
from typing import Any, List, Union, Optional
from dataclasses import dataclass

# Libraries
from fchecker.type import type_check
from ictoolkit import get_function_name

# Exceptions
from .exceptions import CaptureFailure
from fexception import FCustomException, FTypeError

# Local Exceptions and Dataclasses


__author__ = "IncognitoCoding"
__copyright__ = "Copyright 2022, capture"
__credits__ = ["IncognitoCoding"]
__license__ = "MIT"
__version__ = "0.1"
__maintainer__ = "IncognitoCoding"
__status__ = "Beta"


@dataclass
class FindNStrip:
    """
    Information to find and detect a line of text.

    Only use one look-ahead or look-behind per find_n_strip.

    Args:
        group (Union[str, int, float, bool]):
        \t\\- The name of the return group key.\\
        \t\t\\- For Example: An interface with all matching settings.\\
        parent (bool):
        \t\\- Identifies if the FindNStrip group is a parent to all other\\
        \t   found group matches.
        \t\\- Any FindNStrip dataclass value with the parent set to 'False'\\
        \t   means the data belongs to a parent.
        return_key (str):
        \t\\- The name of the return dictionary key.\\
        \t\\- This key will have the value of the found and stripped line.\\
        start_remove (str, optional):
        \t\\- Remove the unused start of the line detection value.\\
        \t\\- Defaults to None.\\
        end_remove (str, optional):
        \t\\- Remove the unused end of the line detection value.\\
        \t\\- Defaults to None.\\
        regex_remove (str, optional):
        \t\\- Remove the unused line detection values.\\
        \t\\- Defaults to None.\\
        look_ahead_plus_1 (str, optional):
        \t\\- Looks + 1 index ahead of the start_remove value in the list.\\
        \t\\- Defaults to None.\\
        look_ahead_plus_2 (str, optional):
        \t\\- Looks + 2 index ahead of the start_remove value in the list.\\
        \t\\- Defaults to None.\\
        look_ahead_plus_3 (str, optional):
        \t\\- Looks + 3 index ahead of the start_remove value in the list.\\
        \t\\- Defaults to None.\\
        look_behind_minus_1 (str, optional):
        \t\\- Looks - 1 index behind of the start_remove value in the list.\\
        \t\\- Defaults to None.\\
        look_behind_minus_2 (str, optional):
        \t\\- Looks - 2 index behind of the start_remove value in the list.\\
        \t\\- Defaults to None.\\
        look_behind_minus_3 (str, optional):
        \t\\- Looks - 3 index behind of the start_remove value in the list.\\
        \t\\- Defaults to None.\\
        required (bool, optional):
        \t\\- If the FindNStrip is a required match value.\\
        \t\\- If the section has no match the section will not save.\\
        \t\\- Defaults to False.
    """

    __slots__ = (
        "group",
        "parent",
        "return_key",
        "start_remove",
        "end_remove",
        "regex_remove",
        "look_ahead_plus_1",
        "look_ahead_plus_2",
        "look_ahead_plus_3",
        "look_behind_minus_1",
        "look_behind_minus_2",
        "look_behind_minus_3",
        "required",
    )

    group: Union[str, int, float, bool]
    parent: bool
    return_key: str
    start_remove: Optional[str]
    end_remove: Optional[str]
    regex_remove: Optional[str]
    look_ahead_plus_1: Optional[str]
    look_ahead_plus_2: Optional[str]
    look_ahead_plus_3: Optional[str]
    look_behind_minus_1: Optional[str]
    look_behind_minus_2: Optional[str]
    look_behind_minus_3: Optional[str]
    required: bool

    def __init__(
        self,
        group: Union[str, int, float, bool],
        parent: bool,
        return_key: str,
        start_remove: Optional[str] = None,
        end_remove: Optional[str] = None,
        regex_remove: Optional[str] = None,
        look_ahead_plus_1: Optional[str] = None,
        look_ahead_plus_2: Optional[str] = None,
        look_ahead_plus_3: Optional[str] = None,
        look_behind_minus_1: Optional[str] = None,
        look_behind_minus_2: Optional[str] = None,
        look_behind_minus_3: Optional[str] = None,
        required: bool = False,
    ) -> None:
        super().__init__()
        object.__setattr__(self, "group", group)
        object.__setattr__(self, "parent", parent)
        object.__setattr__(self, "return_key", return_key)
        object.__setattr__(self, "start_remove", start_remove)
        object.__setattr__(self, "end_remove", end_remove)
        object.__setattr__(self, "regex_remove", regex_remove)
        object.__setattr__(self, "look_ahead_plus_1", look_ahead_plus_1)
        object.__setattr__(self, "look_ahead_plus_2", look_ahead_plus_2)
        object.__setattr__(self, "look_ahead_plus_3", look_ahead_plus_3)
        object.__setattr__(self, "look_behind_minus_1", look_behind_minus_1)
        object.__setattr__(self, "look_behind_minus_2", look_behind_minus_2)
        object.__setattr__(self, "look_behind_minus_3", look_behind_minus_3)
        object.__setattr__(self, "required", required)

        msg_override = "Invalid 'ParseRipper' dataclass argument value type."

        type_check(
            value=group,
            required_type=(int, str),
            tb_remove_name="__init__",
            msg_override=msg_override,
        )
        type_check(
            value=parent,
            required_type=bool,
            tb_remove_name="__init__",
            msg_override=msg_override,
        )
        type_check(
            value=return_key,
            required_type=str,
            tb_remove_name="__init__",
            msg_override=msg_override,
        )
        if start_remove:
            type_check(
                value=start_remove,
                required_type=str,
                tb_remove_name="__init__",
                msg_override=msg_override,
            )
        if end_remove:
            type_check(
                value=end_remove,
                required_type=str,
                tb_remove_name="__init__",
                msg_override=msg_override,
            )
        if regex_remove:
            type_check(
                value=regex_remove,
                required_type=str,
                tb_remove_name="__init__",
                msg_override=msg_override,
            )
        if look_ahead_plus_1:
            type_check(
                value=look_ahead_plus_1,
                required_type=str,
                tb_remove_name="__init__",
                msg_override=msg_override,
            )
        if look_ahead_plus_2:
            type_check(
                value=look_ahead_plus_2,
                required_type=str,
                tb_remove_name="__init__",
                msg_override=msg_override,
            )
        if look_ahead_plus_3:
            type_check(
                value=look_ahead_plus_3,
                required_type=str,
                tb_remove_name="__init__",
                msg_override=msg_override,
            )
        if look_behind_minus_1:
            type_check(
                value=look_behind_minus_1,
                required_type=str,
                tb_remove_name="__init__",
                msg_override=msg_override,
            )
        if look_behind_minus_2:
            type_check(
                value=look_behind_minus_2,
                required_type=str,
                tb_remove_name="__init__",
                msg_override=msg_override,
            )
        if look_behind_minus_3:
            type_check(
                value=look_behind_minus_3,
                required_type=str,
                tb_remove_name="__init__",
                msg_override=msg_override,
            )
        type_check(
            value=required,
            required_type=bool,
            tb_remove_name="__init__",
            msg_override=msg_override,
        )


@dataclass
class ParseRipper:
    """
    Args:
        start_detect (str):
        \t\\- Loop start detection.
        end_detect (Union[list, str], optional):
        \t\\- Loop end detection.\\
        \t\\- A list can be sent to end at mid-points. Mid-point\\
        \t   breaks will return to the next line to continue processing\\
        \t   until the first entry in the list is found.\\
        \t\\- The list will process in order. The first entry is the main\\
        \t   loop stop point. All entries after are mid-point end detection.
        \t\\- Leave None to break after the detected line.\\
        \t\\- Defaults to None.\\
        find_n_strips (list[FindNStrip]):
        \t\\- A list of dataclass entries to find and detect a line of text.
        exclude_values (list, optional):
        \t\\- A list of parsed values to exclude.\\
        \t\\- Defaults to None.\\
    """

    __slots__ = (
        "start_detect",
        "end_detect",
        "find_n_strips",
        "exclude_values",
    )

    start_detect: str
    end_detect: Optional[Union[list, str]]
    find_n_strips: List[FindNStrip]
    exclude_values: Optional[list]

    def __init__(
        self,
        start_detect: str,
        end_detect: Optional[Union[list, str]] = None,
        find_n_strips: List[FindNStrip] = [],
        exclude_values: Optional[list] = [],
    ) -> None:
        super().__init__()
        object.__setattr__(self, "start_detect", start_detect)
        object.__setattr__(self, "end_detect", end_detect)
        object.__setattr__(self, "find_n_strips", find_n_strips)
        object.__setattr__(self, "exclude_values", exclude_values)

        msg_override = "Invalid 'ParseRipper' dataclass argument value type."

        type_check(
            value=start_detect,
            required_type=str,
            tb_remove_name="__init__",
            msg_override=msg_override,
        )
        if end_detect:
            type_check(
                value=end_detect,
                required_type=(list, str),
                tb_remove_name="__init__",
                msg_override=msg_override,
            )
        type_check(
            value=find_n_strips,
            required_type=list,
            tb_remove_name="__init__",
            msg_override=msg_override,
        )
        if len(find_n_strips) >= 0:
            type_check(
                value=find_n_strips[0],
                required_type=FindNStrip,
                tb_remove_name="__init__",
                msg_override=msg_override,
            )
        if exclude_values:
            type_check(
                value=exclude_values,
                required_type=list,
                tb_remove_name="__init__",
                msg_override=msg_override,
            )


def capture_file_sections(
    my_list: list[str], strip: ParseRipper
) -> Union[
    list[
        dict[
            Union[str, int, float, bool],
            Union[list[dict[Union[str, int, float, bool], Union[str, None]]], None],
        ]
    ],
    None,
]:
    """
    Captures sections out of any file based on specifically selected dataclass values.

    Multiple grouping is possible with dictionary returns.

    A future release may include the ability to convert the dictionary to dataclass variables.

    Args:
        my_list (list[str]):
        \t\\- A list of values or sentences.
        strip (ParseRipper):
        \t\\- A ParseRipper dataclass with parsing information.

    Raises:
        FTypeError (fexception):
        \t\\- The object value '{my_list}' is not an instance of the required class(es) or subclass(es).
        FTypeError (fexception):
        \t\\- The object value '{strip}' is not an instance of the required class(es) or subclass(es).
        CaptureFailure:
        \t\\- No processing_group was found.
        CaptureFailure:
        \t\\- Unexpected queued key count.

    Returns:
        Union[list[dict[Union[str, int, float, bool], Union[list[dict[Union[str, int, float, bool], Union[str, None]]], None]]], None]:
        \t\\- A list of dictionary groupings.

    Return Example:
    \t\\- parsed_data[0] = {'mygroup1': [{'name': 'Tom'},\\
    \t\t\t\t\t\t\t     {'job': 'mechanic'},\\
    \t\t\t\t\t\t\t     {'shift': '1st'}]}
    """
    # ##############################################################################
    # ########################REMOVE ME AFTER TESTING###############################
    # ##############################################################################
    import sys

    logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    logger = logging.getLogger(__name__)
    # ##############################################################################
    # ##############################################################################

    logger.debug(f"=" * 20 + get_function_name() + "=" * 20)
    # Custom flowchart tracking. This is ideal for large projects that move a lot.
    # For any third-party modules, set the flow before making the function call.
    logger_flowchart = logging.getLogger("flowchart")
    logger_flowchart.debug(f"Flowchart --> Function: {get_function_name()}")

    type_check(
        value=my_list, required_type=list, tb_remove_name="capture_file_sections"
    )
    type_check(
        value=strip, required_type=ParseRipper, tb_remove_name="capture_file_sections"
    )

    formatted_my_list = "  - config (list):" + str(
        "\n        - " + "\n        - ".join(map(str, my_list))
    )
    logger.debug(
        "Passing parameters:\n"
        f"{formatted_my_list}\n"
        f"  - strip (ParseRipper):\n        - {strip}\n"
    )

    # Holds all section_groups.
    all_section_groups: list[
        dict[
            Union[str, int, float, bool],
            Union[list[dict[Union[str, int, float, bool], Union[str, None]]], None],
        ]
    ] = []

    # Stores if the match was a parent line.
    parent_found: bool = False

    # Loops through each line.
    for line_index, line_entry in enumerate(my_list):
        # Checks for a matching start detection line.
        if strip.start_detect in line_entry:
            loop_counter: int = line_index

            # Stores the user-defined processing group.
            processing_group: Union[str, int, float, bool, None] = None
            # Holds queued line captures during the main loop.
            queued_line: dict[Union[str, int, float, bool], list[dict[str, str]]] = {}
            # Holds all grouped section data before an end_detect.
            section_group: dict[
                Union[str, int, float, bool],
                Union[list[dict[Union[str, int, float, bool], Union[str, None]]], None],
            ] = {}

            logger.debug(
                f"A start_detection value ({strip.start_detect}) matched a line_entry ({line_entry}). Starting an infinite loop"
            )
            # Loops until the end_detect value is discovered.
            while True:
                # Tracks excluded match results, for breaking the loop.
                exclude_match: bool = False

                subloop1_ahead_plus_1_line: Union[str, None] = None
                subloop1_ahead_plus_2_line: Union[str, None] = None
                subloop1_ahead_plus_3_line: Union[str, None] = None
                subloop1_behind_minus_1_line: Union[str, None] = None
                subloop1_behind_minus_2_line: Union[str, None] = None
                subloop1_behind_minus_3_line: Union[str, None] = None

                subloop1_line: str = str(my_list[loop_counter])
                if loop_counter + 1 <= len(my_list) - 1:
                    subloop1_ahead_plus_1_line = str(my_list[loop_counter + 1])
                if loop_counter + 2 <= len(my_list) - 1:
                    subloop1_ahead_plus_2_line = str(my_list[loop_counter + 2])
                if loop_counter + 3 <= len(my_list) - 1:
                    subloop1_ahead_plus_3_line = str(my_list[loop_counter + 3])
                if loop_counter - 1 >= 0:
                    subloop1_behind_minus_1_line = str(my_list[loop_counter - 1])
                if loop_counter - 2 >= 0:
                    subloop1_behind_minus_2_line = str(my_list[loop_counter - 2])
                if loop_counter - 3 >= 0:
                    subloop1_behind_minus_3_line = str(my_list[loop_counter - 3])

                # Starts to use the FindNStrip search to find a matching line.
                for find in strip.find_n_strips:
                    # Sets the processing group.
                    # The group needs set at the top in case no match keys need populated.
                    processing_group = find.group

                    # ################################################
                    # ############Extened Approval Check##############
                    # ################################################
                    # The approval check is disabled by default.
                    # Each look-ahead or look-behind is checked to see if a check is required.
                    # No checks will set the approval check to True.
                    # Only one look-ahead or look-behind can be used per find_n_strip.
                    extended_approval_check: bool = False
                    if (subloop1_ahead_plus_1_line and find.look_ahead_plus_1) and (
                        find.look_ahead_plus_1 in subloop1_ahead_plus_1_line
                    ):
                        logger.debug(
                            f"A look_ahead_plus_1 value ({find.look_ahead_plus_1}) matched a line_entry ({subloop1_ahead_plus_1_line}). "
                            "Setting the extended_approval_check to True"
                        )
                        extended_approval_check = True
                    elif (subloop1_ahead_plus_2_line and find.look_ahead_plus_2) and (
                        find.look_ahead_plus_2 in subloop1_ahead_plus_2_line
                    ):
                        logger.debug(
                            f"A look_ahead_plus_2 value ({find.look_ahead_plus_2}) matched a line_entry ({subloop1_ahead_plus_2_line}). "
                            f"Setting the extended_approval_check to True"
                        )
                        extended_approval_check = True
                    elif (subloop1_ahead_plus_3_line and find.look_ahead_plus_3) and (
                        find.look_ahead_plus_3 in subloop1_ahead_plus_3_line
                    ):
                        logger.debug(
                            f"A look_ahead_plus_3 value ({find.look_ahead_plus_3}) matched a line_entry ({subloop1_ahead_plus_3_line}). "
                            "Setting the extended_approval_check to True"
                        )
                        extended_approval_check = True
                    elif (
                        subloop1_behind_minus_1_line and find.look_behind_minus_1
                    ) and (find.look_behind_minus_1 in subloop1_behind_minus_1_line):
                        logger.debug(
                            f"A look_behind_minus_1 value ({find.look_behind_minus_1}) matched a line_entry ({subloop1_behind_minus_1_line}). "
                            "Setting the extended_approval_check to True"
                        )
                        extended_approval_check = True
                    elif (
                        subloop1_behind_minus_2_line and find.look_behind_minus_2
                    ) and (find.look_behind_minus_2 in subloop1_behind_minus_2_line):
                        logger.debug(
                            f"A look_behind_minus_2 value ({find.look_behind_minus_2}) matched a line_entry ({subloop1_behind_minus_2_line}). "
                            "Setting the extended_approval_check to True"
                        )
                        extended_approval_check = True
                    elif (
                        subloop1_behind_minus_3_line and find.look_behind_minus_3
                    ) and (find.look_behind_minus_3 in subloop1_behind_minus_3_line):
                        logger.debug(
                            f"A look_behind_minus_3 value ({find.look_behind_minus_3}) matched a line_entry ({subloop1_behind_minus_3_line}). "
                            "Setting the extended_approval_check to True"
                        )
                        extended_approval_check = True
                    # Final check if no look-ahead or look-behinds are being used.
                    elif (
                        not find.look_ahead_plus_1
                        and not find.look_ahead_plus_2
                        and not find.look_ahead_plus_3
                        and not find.look_behind_minus_1
                        and not find.look_behind_minus_2
                        and not find.look_behind_minus_3
                    ):
                        logger.debug(
                            f"No look-ahead or look-behind values are being checked. Setting the extended_approval_check to True"
                        )
                        extended_approval_check = True

                    # Checks if any combination of start_remove or end_remove matches and if the extended_approval_check passed.
                    if (
                        (
                            (find.start_remove and find.start_remove in subloop1_line)
                            and (find.end_remove and find.end_remove in subloop1_line)
                        )
                        or (
                            find.start_remove
                            and find.start_remove in subloop1_line
                            and (not find.end_remove)
                        )
                        or (
                            not find.start_remove
                            and (find.end_remove and find.end_remove in subloop1_line)
                        )
                    ) and extended_approval_check:

                        logger.debug(
                            f"A find_n_strip value ({find}) matched a line_entry ({line_entry}). Starting to parse based on "
                            f"start_remove ({find.start_remove}) and end_remove ({find.end_remove}) values"
                        )
                        replaced: Union[str, None] = None
                        if find.start_remove and find.end_remove:
                            # Replace Example:
                            #   Original:                 <host-name>A-NOC</host-name>
                            #   Replaced: A-NOC
                            replaced = (
                                subloop1_line.strip()
                                .replace(find.start_remove, "")
                                .replace(find.end_remove, "")
                            )
                            logger.debug(
                                f"'{strip.start_detect}' found, and removing the '{find.start_remove}' and '{find.end_remove}' string. Set Value (str):"
                                f"\n    - Original Parse: {subloop1_line}\n    - Replaced Parse: {replaced}"
                            )
                        elif find.start_remove and not find.end_remove:
                            # Replace Example:
                            #   Original:                 <host-name>A-NOC</host-name>
                            #   Replaced: A-NOC
                            replaced = subloop1_line.strip().replace(
                                find.start_remove, ""
                            )
                            logger.debug(
                                f"'{strip.start_detect}' found, and removing the '{find.start_remove}' and '{find.end_remove}' string. Set Value (str):"
                                f"\n    - Original Parse: {subloop1_line}\n    - Replaced Parse: {replaced}"
                            )
                        elif not find.start_remove and find.end_remove:
                            # Replace Example:
                            #   Original:                 <host-name>A-NOC</host-name>
                            #   Replaced: A-NOC
                            replaced = subloop1_line.strip().replace(
                                find.end_remove, ""
                            )
                            logger.debug(
                                f"'{strip.start_detect}' found, and removing the '{find.start_remove}' and '{find.end_remove}' string. Set Value (str):"
                                f"\n    - Original Parse: {subloop1_line}\n    - Replaced Parse: {replaced}"
                            )
                        else:
                            # Replace Example:
                            #   Original:                 <host-name>A-NOC</host-name>
                            #   Replaced: <host-name>A-NOC</host-name>
                            replaced = subloop1_line.strip()
                            logger.debug(
                                f"'{strip.start_detect}' found, and removing the '{find.start_remove}' and '{find.end_remove}' string. Set Value (str):"
                                f"\n    - Original Parse: {subloop1_line}\n    - Replaced Parse: {replaced}"
                            )

                        # Checks if a replace value exists.
                        if replaced:
                            # Checks if any excluded values exist.
                            if strip.exclude_values:
                                exclude_match = any(
                                    exclude
                                    for exclude in strip.exclude_values
                                    if exclude == replaced
                                )
                            if not exclude_match:
                                if processing_group:
                                    queued_line = {
                                        processing_group: [{find.return_key: replaced}]
                                    }
                                    # Checks if the matching line is a parent line.
                                    if find.parent:
                                        parent_found = True
                                else:
                                    exc_args: dict = {
                                        "main_message": "No processing_group was found.",
                                        "custom_type": CaptureFailure,
                                        "expected_result": "A processing group value",
                                        "returned_result": None,
                                    }
                                    raise CaptureFailure(
                                        FCustomException(
                                            message_args=exc_args,
                                            tb_remove_name="capture_file_sections",
                                        )
                                    )
                            break

                break_flag: bool = False
                loop_counter += 1
                # Checks if an end detection line exists.
                # This section will pre-set any empty keys with None and set the break_flag.
                if strip.end_detect:
                    end_detect: list = []
                    # Checks if the end_detect is a list with mid-breaks or a single main break.
                    if isinstance(strip.end_detect, list):
                        end_detect = strip.end_detect
                    else:
                        end_detect.append(strip.end_detect)

                    # Checks if a detection line exists.
                    if end_detect and len(end_detect) >= 1:
                        main_break: bool = False

                        # Reverses the list, so all mid-breaks are checked first.
                        end_detect = end_detect.copy()
                        end_detect.reverse()
                        for end_index, end_value in enumerate(end_detect):
                            if end_value in subloop1_line:
                                # Sets the main breakpoint if the first index is the breakpoint.
                                # All other breaks are mid-breaks and will continue in the main loop.
                                if end_index == len(end_detect) - 1:
                                    logger.debug(
                                        f"A end_detection value ({end_value}) matched a line_entry ({line_entry}). "
                                        "Performing some post-detection tasks to format the data for saving"
                                    )
                                    # Checks if any section data was found.
                                    if section_group:
                                        required_keys: list = []
                                        # Loops through all required section searches.
                                        for find in strip.find_n_strips:
                                            # Checks if the section line is a requirement.
                                            if find.required:
                                                required_keys.append(find.return_key)

                                        list_of_keys: list = []
                                        # Gets all section keys.
                                        for section in section_group.values():
                                            for value in section:
                                                for key in value.keys():
                                                    list_of_keys.append(key)
                                        # Converts the list of keys to a tuple.
                                        section_keys: tuple = tuple(list_of_keys)

                                        valid: bool = False
                                        if required_keys:
                                            # Loops through required and section keys to check if the captures section is valid.
                                            for required_key in required_keys:
                                                for section_key in section_keys:
                                                    if required_key == section_key:
                                                        valid = True
                                                        break
                                        else:
                                            valid = True

                                        # Checks if the section data has all required field data before returning data.
                                        # This is ideal for matches that may not contain specific information in other sections.
                                        if valid:
                                            # Adds any fields that were never found.
                                            for find in strip.find_n_strips:
                                                key_set: bool = False
                                                for section_key in section_keys:
                                                    if find.return_key == section_key:
                                                        key_set = True

                                                # Checks if the find_n_strip key exists in the section.
                                                # If not the key will be written with None. This keeps all returns consistent.
                                                if not key_set:
                                                    # Merges the no match key into the existing section_keys.
                                                    if processing_group:
                                                        merge_value = create_or_merge_dict_value(
                                                            my_dict=section_group,
                                                            key=processing_group,
                                                            merge_value={
                                                                find.return_key: None
                                                            },
                                                        )
                                                        section_group = merge_value
                                                    else:
                                                        exc_args: dict = {
                                                            "main_message": "No processing_group was found.",
                                                            "custom_type": CaptureFailure,
                                                            "expected_result": "A processing group value",
                                                            "returned_result": None,
                                                        }
                                                        raise CaptureFailure(
                                                            FCustomException(
                                                                message_args=exc_args,
                                                                tb_remove_name="capture_file_sections",
                                                            )
                                                        )

                                    # Sets the main break flag.
                                    main_break = True
                                    break

                        # Checks if the main brake is set.
                        if main_break:
                            break_flag = True
                    # Breaks if no match, but the end of the list is reached.
                    elif loop_counter == len(my_list):
                        logger.debug(
                            "Breaking because no matching end_detect and the end of the list is reached"
                        )
                        break_flag = True
                # Breaks if no match, but the end of the list is reached.
                elif loop_counter == len(my_list):
                    logger.debug(
                        "Breaking because no set end_detection and the end of the list is reached"
                    )
                    break_flag = True

                # This section uses the parent group, queued_line, and break_flag to help determine when
                # the section_group needs to be added to the main group and cleared for the next section.
                # Note: The last looped group section will need to be processed at the very end.
                # NOTE:
                #   - The break_flag catches the last section_group.
                if parent_found and queued_line or break_flag:
                    # The last entry may not have a queued_line if nothing matches, but it will have data still in the section_group that needs to be written.
                    if not break_flag:
                        logger.debug(
                            f"A queued_line from {processing_group} is ready for processing: {queued_line}"
                        )

                    # Looks for an existing section_group value to add the previous section to the main list.
                    if section_group:
                        logger.debug(
                            f"An existing section value is detected: {section_group}. Adding the value to the all_section_groups list."
                        )
                        # Adds the section group to the main global section_group for all sections.
                        all_section_groups.append(section_group)

                    # Sets/Overrides the previous section_group with the current section value.
                    section_group = queued_line  # type: ignore

                    # Clears the queued_line, processing_group, and parent flag.
                    queued_line = {}
                    processing_group = ""
                    parent_found = False
                elif queued_line:
                    logger.debug(
                        f"A queued_line from {processing_group} is appending to an existing dictionary: {queued_line}"
                    )

                    # Looks for an existing section_group value.
                    if section_group:
                        logger.debug(
                            f"An existing section value is detected: {section_group}"
                        )
                        # Gets the name of the user defined grouped key.
                        queued_key = list(queued_line.keys())
                        if len(queued_key) == 1:
                            key = queued_key[0]
                        else:
                            exc_args: dict = {
                                "main_message": "Unexpected queued key count.",
                                "custom_type": CaptureFailure,
                                "expected_result": 1,
                                "returned_result": len(queued_key),
                            }
                            raise CaptureFailure(
                                FCustomException(
                                    message_args=exc_args,
                                    tb_remove_name="capture_file_sections",
                                )
                            )

                        queued_value = list(queued_line.values())
                        # Converts a single value from a list to a single value.
                        if len(queued_value) == 1:
                            values = queued_value[0]
                        else:
                            values = queued_value

                        # Merges the queued_line with the current section_group.
                        merge_value = create_or_merge_dict_value(
                            my_dict=section_group, key=key, merge_value=values
                        )
                        # Sets the merged values to the section_group. The next parent writes or break_flag will write the section_group to the main list.
                        section_group = merge_value

                    # Clears the queued_line and processing_group.
                    queued_line = {}
                    processing_group = ""

                if break_flag:
                    break

    if all_section_groups:
        formatted_all_section_groups = "  - parsed_data (list):" + str(
            "\n        - " + "\n        - ".join(map(str, all_section_groups))
        )
        logger.debug(
            f"Data parsing completed, and the dictionary formatted data will return: \n{formatted_all_section_groups}"
        )
        return all_section_groups
    else:
        logger.debug("No data matched. Returning None")
        return None


def create_or_merge_dict_value(
    my_dict: Union[dict[Union[str, int, float, bool], Any], None],
    key: Union[str, int, float, bool],
    merge_value: Any,
) -> dict[Union[str, int, float, bool], Any]:
    """
    Creates a new dictionary from a key and merge_value, adds a key and merge_value, or merges\\ 
    any existing values with a matching key will get merged. The merge will be converted to a list.

    Args:
        my_dict (Union[dict[str, Any], None]):
        \t\\- An existing dictionary.\\
        \t\\- If one is not provided a new dictionary will get created with the key and merge_value.
        key (Union[str, int, float, bool]):
        \t\\- The key to create or merge.
        merge_value (Any):
        \t\\- The value to create or merge.\\
        \t\\- None is supported.

    Raises:
        FTypeError (fexception):
        \t\\- The object value '{my_dict}' is not an instance of the required class(es) or subclass(es).
        FTypeError (fexception):
        \t\\- The object value '{key}' is not an instance of the required class(es) or subclass(es).
        FTypeError (fexception):
        \t\\- The object value '{merge_value}' is not an instance of the required class(es) or subclass(es).
        FTypeError (fexception):
        \t\\- Type is not supported

    Returns:
        dict[Union[str, int, float, bool], Any]:
        \t\\- The created or merged dictionary value.
    
    Return Example:
    \t\\- my_dict = {'mygroup': [{'name': 'Tom'},
    \t\t\t\t\t\t{'job': "mechanic"},
    \t\t\t\t\t\t{'shift': "1st"},
    \t\t\t\t\t\t{'phone': None}]}
    """
    logger = logging.getLogger(__name__)
    logger.debug(f"=" * 20 + get_function_name() + "=" * 20)
    # Custom flowchart tracking. This is ideal for large projects that move a lot.
    # For any third-party modules, set the flow before making the function call.
    logger_flowchart = logging.getLogger("flowchart")
    logger_flowchart.debug(f"Flowchart --> Function: {get_function_name()}")

    if my_dict:
        type_check(
            value=my_dict,
            required_type=dict,
            tb_remove_name="create_or_merge_dict_value",
        )
    type_check(
        value=key,
        required_type=(str, int, float, bool),
        tb_remove_name="create_or_merge_dict_value",
    )

    if my_dict:
        formatted_my_dict = "  - my_dict (dict):\n        - " + "\n        - ".join(
            ": ".join((str(key), str(val))) for (key, val) in my_dict.items()
        )
    else:
        formatted_my_dict = f"  - my_dict (dict):\n        - None\n"
    logger.debug(
        "Passing parameters:\n"
        f"{formatted_my_dict}\n"
        f"  - key (Union[str, int, float, bool]):\n        - {key}\n"
        f"  - merge_value (Any):\n        - {merge_value}\n"
    )

    # Creates a new dictionary or merges values with existing values
    if my_dict:
        logger.debug("An existing dictionary exists. Checking for any matching keys")
        if my_dict.get(key) == None:
            my_dict.update({key: merge_value})
            logger.debug(
                f"No matching key exists. Added the key ({key}) and value ({merge_value}) to the dictionary"
                f"\n  - my_dict = {my_dict}"
            )
        else:
            updated_value: list = []
            current_value: Union[list[str], str, dict, None] = my_dict.get(key)
            if current_value:
                if isinstance(current_value, str):
                    updated_value = [current_value, merge_value]
                    logger.debug(
                        f"The current value is a string. Added the merge_value ({merge_value}) to a "
                        f"list with the current value ({current_value}).\n  - updated_value = {updated_value}"
                    )
                elif isinstance(current_value, list):
                    # Checks if the merge value is a list to append.
                    if isinstance(merge_value, list):
                        # Joins two lists together.
                        updated_value = current_value + merge_value
                    else:
                        # Sets the current value to the list.
                        updated_value = current_value
                        # Adds any other type to the existing list.
                        updated_value.append(merge_value)  # type: ignore
                    logger.debug(
                        f"The current value is a list. Joined the merge value ({merge_value}) to a "
                        f"the current value ({current_value}).\n  - updated_value = {updated_value}"
                    )
                else:
                    exc_args = {
                        "main_message": "Type is not supported",
                        "expected_result": "str, list",
                        "returned_result": type(current_value),
                        "suggested_resolution": "Please report this section to the developer to add support.",
                    }
                    raise FTypeError(
                        message_args=exc_args, tb_remove_name="str_to_list"
                    )

            my_dict.update({key: updated_value})
            logger.debug(
                f"Added the updated merged value ({updated_value}) to the return list as a dictionary"
                f"\n  - my_dict = {my_dict}"
            )
    else:
        my_dict = {}
        my_dict.update({key: merge_value})
        logger.debug(
            f"No dictionary exists. Creating a new dictionary with the key ({key}) and value ({merge_value})"
            f"\n  - my_dict = {my_dict}"
        )

    logger.debug(f"Returning the dictionary new or merged dictionary ({my_dict})")
    return my_dict
