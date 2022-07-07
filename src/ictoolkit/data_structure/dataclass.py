# Built-in/Generic Imports
import logging
from typing import Union, List, Any, Optional
from dataclasses import dataclass, make_dataclass, fields, field

# Libraries
from fchecker.type import type_check

# Local Functions
from ..helpers.py_helper import get_function_name

# Exceptions
from fexception import FCustomException
from .exceptions import RequirementFailure


__author__ = "IncognitoCoding"
__copyright__ = "Copyright 2022, dataclass"
__credits__ = ["IncognitoCoding"]
__license__ = "MIT"
__version__ = "0.2"
__maintainer__ = "IncognitoCoding"
__status__ = "Production"


def create_dataclass(
    dataclass_name: str,
    my_dict: Union[dict, List[dict]],
    req_keys: Optional[set] = None,
    tb_remove_name: Optional[str] = None,
) -> Union[List[dataclass], dataclass]:
    """
    Create a dynamic dataclass from a dictionary or a dynamic dataclass list from a list of dictionaries.

    All args are set to None by default.

    Use the req_keys to force requirements.

    A list of dictionaries will have the keys compared with each other to ensure all arguments are populated the same.

    The dynamic dataclass will have a type return from the main (ex: <class '__main__.MyTestClass'>).

    Args:
        dataclass_name (str):
        \t\\- The name of the dataclass.
        my_dict (Union[dict, List[dict]]):
        \t\\- The dictionary converting to a dataclass.
        \t\\- A list of dictionaries converting to a list of dataclasses.
        req_keys (set, optional):
        \t\\- A set of required dictionary keys.
        \t\\- Defaults to None.
        tb_remove_name (str, optional):\\
        \t\\- Caller function name or any other function in the\\
        \t   traceback chain.\\
        \t\\- Removes all traceback before and at this function.\\
        \t\\- Defaults to None.

    Raises:
        FTypeError (fexception):
        \t\\- The object value '{dataclass_name}' is not an instance of the required class(es) or subclass(es).
        FTypeError (fexception):
        \t\\- The object value '{my_dict}' is not an instance of the required class(es) or subclass(es).
        InputFailure:
        \t\\- dict format is the required input to set the caller override option.
        InputFailure:
        \t\\- Incorrect caller_overide keys.

    Return:
        Union[List[Type[<User Defined Dataclass>]], Type[<User Defined Dataclass>]]\\
        \t\\- The users defined dataclass values.\\
        \t\\- A list of the users defined dataclass values.
    """
    logger = logging.getLogger(__name__)
    logger.debug(f"=" * 20 + get_function_name() + "=" * 20)
    # Custom flowchart tracking. This is ideal for large projects that move a lot.
    # For any third-party modules, set the flow before making the function call.
    logger_flowchart = logging.getLogger("flowchart")
    logger_flowchart.debug(f"Flowchart --> Function: {get_function_name()}")

    type_check(value=dataclass_name, required_type=str, tb_remove_name="create_dataclass")
    type_check(value=my_dict, required_type=(list, dict), tb_remove_name="create_dataclass")
    if req_keys:
        type_check(value=req_keys, required_type=set, tb_remove_name="create_dataclass")

    formatted_my_dict: Union[str, None] = None
    if isinstance(my_dict, list):
        formatted_my_dict = "  - my_dict (list):" + str("\n        - " + "\n        - ".join(map(str, my_dict)))
    if isinstance(my_dict, dict):
        formatted_my_dict = "  - my_dict (dict):\n        - " + "\n        - ".join(
            ": ".join((key, str(val))) for (key, val) in my_dict.items()
        )
    if req_keys:
        formatted_req_keys = f"  - req_keys (set):\n        - {req_keys}"
    else:
        formatted_req_keys = f"  - req_keys (set):\n        - None"
    logger.debug(
        "Passing parameters:\n"
        f"  - dataclass_name (str):\n        - {dataclass_name}\n"
        f"{formatted_my_dict}\n"
        f"{formatted_req_keys}\n"
    )

    # Sets the processing_dicts based on a single dict or List[dict].
    processing_dicts: list = []
    if isinstance(my_dict, dict):
        # Adds one entry.
        processing_dicts.append(my_dict)
    if isinstance(my_dict, list):
        # Converts all List[dict] to new list.
        processing_dicts = my_dict

    populated_dataclasses: list = []
    for index, entry in enumerate(processing_dicts):
        existing_fields: list = []
        for key, value in entry.items():
            arg_name: str = key
            entry_type: type = type(value)
            # Creates fields to send when making the dynamic dataclass.
            existing_fields.append((arg_name, entry_type, field(init=False, repr=False)))

        # Creates the dataclass.
        # Args are set to None to initial the dataclass before writing.
        # Any required args need to be validated before write.
        new_dataclass = make_dataclass(dataclass_name, existing_fields)
        # Set the dynamic dataclass name to __main__ function.
        # This could be set to the calling func if needed.
        # This converts the dynamic dataclass type ('type') to the actual
        # path to this function.
        # Requires for some usages such as dill pickling.
        #   - Bug: https://bugs.python.org/issue35510
        new_dataclass.__module__ = "__main__"
        # Initiates the dynamic dataclass.
        initiated_dynamic_dataclass = new_dataclass()
        # Populates the dataclass with the dictionary values.
        for key, value in entry.items():
            arg_name: str = key
            value: Any = value
            # Sets the dictionary key as the type and value as value.
            setattr(initiated_dynamic_dataclass, arg_name, value)

        # Sets required fields.
        required_field_names: Union[set[str], None] = None
        if index == 0:
            if req_keys:
                required_field_names = req_keys
            else:
                # No req_keys. Setting to the current dataclass keys, so the compare passes.
                required_field_names = {field.name for field in fields(initiated_dynamic_dataclass)}
        elif index != 0:
            # Gets previous current dataclass fields.
            required_field_names = {field.name for field in fields(populated_dataclasses[index - 1])}

        # Compares required and current field names.
        # Gets current dataclass fields.
        current_field_names = {field.name for field in fields(initiated_dynamic_dataclass)}
        if isinstance(required_field_names, set) and isinstance(current_field_names, set):
            if required_field_names != current_field_names:
                # Gets the difference between the field names.
                # Original Example: {'name', 'teaching_subject'}
                # Replaced: 'name', 'teaching_subject'
                diff_names: str = (
                    str(required_field_names.difference(current_field_names)).replace("{", "").replace("}", "")
                )
                # Checks for an empty set.
                # An empty set means the table_columns contains more entries than the required.
                if diff_names == str(set()):
                    diff_names: str = (
                        str(current_field_names.difference(required_field_names)).replace("{", "").replace("}", "")
                    )

                exc_args = {
                    "main_message": f"{dataclass_name} got an unexpected keyword argument.",
                    "custom_type": RequirementFailure,
                    "expected_result": str(sorted(required_field_names)).replace("[", "").replace("]", ""),
                    "returned_result": str(sorted(current_field_names)).replace("[", "").replace("]", ""),
                    "suggested_resolution": [
                        "Verify the passing dictionary does not require specific keys.",
                        "Make sure your list of dictionaries contains the same keys per entry.",
                    ],
                }
                raise RequirementFailure(
                    FCustomException(message_args=exc_args, tb_limit=None, tb_remove_name=tb_remove_name)
                )

        populated_dataclasses.append(initiated_dynamic_dataclass)

    # Checks the input type for the return.
    if isinstance(my_dict, dict):
        # One dict sent in, one dataclass returned.
        return populated_dataclasses[0]
    elif isinstance(my_dict, list):
        return populated_dataclasses
