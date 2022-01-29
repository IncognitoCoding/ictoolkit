__author__ = 'IncognitoCoding'
__copyright__ = 'Copyright 2022, ictoolkit'
__credits__ = ['IncognitoCoding']
__license__ = 'MIT'
__version__ = '3.2'
__maintainer__ = 'IncognitoCoding'
__status__ = 'Production'

import logging

# Logging configuration
log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())

# Function & Methods
from .helpers.py_helper import (get_function_name,
                                get_line_number)
from .directors.data_structure_director import (remove_duplicate_dict_values_in_list,
                                                get_list_of_dicts_duplicates,
                                                get_list_duplicates,
                                                string_grouper,
                                                find_longest_common_substring,
                                                user_choice_character_grouping,
                                                clean_non_word_characters)
from .directors.email_director import (create_template_email,
                                       send_email)
from .directors.encryption_director import (encrypt_info,
                                            decrypt_info,
                                            launch_decryptor_website)
from .directors.file_director import (write_file,
                                      search_file,
                                      search_multiple_files,
                                      convert_relative_to_full_path,
                                      user_file_selection)
from .directors.html_director import HTMLConverter
from .directors.ini_config_director import (read_ini_config,
                                            get_ini_config)
from .directors.log_director import (create_logger,
                                     setup_logger_yaml)
from .directors.subprocess_director import start_subprocess
from .directors.thread_director import start_function_thread
from .directors.yaml_director import read_yaml_config

# Dataclasses & NamedTuples
# --- None ---

# Exceptions
from .directors.email_director import (CreateTemplateFailure,
                                       EmailSendFailure)
from .directors.encryption_director import (EncryptionFailure,
                                            DecryptionFailure,
                                            DecryptionSiteFailure)
from .directors.file_director import (FileWriteFailure,
                                      FileSearchFailure)
from .directors.log_director import LoggerSetupFailure
from .directors.subprocess_director import SubprocessStartFailure
from .directors.thread_director import ThreadStartFailure
from .directors.yaml_director import YamlReadFailure
