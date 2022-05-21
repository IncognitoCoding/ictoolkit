from ..data_structure.choice import user_choice_character_grouping
from ..data_structure.common import (
    str_to_list,
    common_case_isupper,
    common_case_islower,
    dict_keys_upper,
    dict_keys_lower,
)
from ..data_structure.dataclass import create_dataclass
from ..data_structure.dict import string_grouper, move_dict_value

from .exceptions import InputFailure, RequirementFailure, RemoveSectionFailure
from ..data_structure.list import (
    remove_duplicate_dict_values_in_list,
    get_list_of_dicts_duplicates,
    get_list_duplicates,
)
from ..data_structure.str import find_longest_common_substring, clean_non_word_characters, remove_section
