__author__ = "IncognitoCoding"
__copyright__ = "Copyright 2022, ictoolkit"
__credits__ = ["IncognitoCoding"]
__license__ = "MIT"
__version__ = "3.9"
__maintainer__ = "IncognitoCoding"
__status__ = "Production"

import logging

# Logging configuration
log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())

# Function & Methods
from .helpers.py_helper import get_function_name, get_line_number
from .data_structure.choice import user_choice_character_grouping
from .data_structure.common import (
    str_to_list,
    common_case_isupper,
    common_case_islower,
    dict_keys_upper,
    dict_keys_lower,
)
from .data_structure.dataclass import create_dataclass
from .data_structure.dict import string_grouper, move_dict_value

# from .exceptions import
from .data_structure.list import (
    remove_duplicate_dict_values_in_list,
    get_list_of_dicts_duplicates,
    get_list_duplicates,
)
from .data_structure.str import find_longest_common_substring, clean_non_word_characters

from .directors.email_director import create_template_email, send_email
from .directors.encryption_director import encrypt_info, decrypt_info, launch_decryptor_website
from .directors.file_director import write_file, search_file, convert_relative_to_full_path, user_file_selection
from .directors.html_director import HTMLConverter
from .directors.ini_config_director import read_ini_config
from .directors.log_director import create_logger, setup_logger_yaml
from .directors.subprocess_director import start_subprocess
from .directors.thread_director import start_function_thread
from .directors.yaml_director import read_yaml_config

# Dataclasses & NamedTuples
# --- None ---

# Exceptions
from .data_structure.exceptions import InputFailure, RequirementFailure
from .directors.email_director import CreateTemplateFailure, EmailSendFailure
from .directors.encryption_director import EncryptionFailure, DecryptionFailure, DecryptionSiteFailure
from .directors.file_director import FileWriteFailure, FileSearchFailure
from .directors.log_director import LoggerSetupFailure
from .directors.subprocess_director import SubprocessStartFailure
from .directors.thread_director import ThreadStartFailure
from .directors.yaml_director import YamlReadFailure
