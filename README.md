# ictoolkit
 
ictoolkit is designed to be the swiss army knife of programming methods. This package is ever-growing and includes many useful techniques. Some modules are not complex but are often used, so they help keep the main code less congested and provide error catching. Available methods will be listed below, but further details will be listed within each function's docstring.

The setup.cfg file includes all required packages for all modules. Some needed packages may not be necessary, depending on the modules used.

## Future Update Notes:
Functions and classes under the "directors" directory will be moved to a different directory/structure within ictoolkit in the future. These functions and classes will be set up similar to the data_structure directory. For now, import using "from ictoolkit import [function or class]". The process will prevent no breaks once the functions and classes are moved.

## Package Highlights:
* A growing list of useful methods to help assist with general programming.

## Package/Module/Method/Function Info:
* Directory/Modules: data_structure
  - Module: choice.py
    - Function: user_choice_character_grouping
      - Groups a list of characters based on the user's choices.
  - Module: common.py
    - Function: common_case_isupper
      - Checks if the common case of the strings in the list is upper case.
    - Function: common_case_islower
      - Checks if the common case of the strings in the list is lower case.
  - Module: dataclass.py
    - Function: create_dataclass
      - Create a dynamic dataclass from a dictionary or a dynamic dataclass list from a list of dictionaries.
  - Module: dict.py
    - Function: dict_keys_upper
      - Converts all dictionary keys to upper case.
    - Function: dict_keys_lower
      - Converts all dictionary keys to lower case.
    - Function: sort_dict
      - Sorts a dictionary based on the sort options.
    - Function: string_grouper
      - String grouper will group a list of strings using three different options.
    - Funtion: move_dict_value
      - This function moves dictionary values from one key to another key.
  - Module: exceptions.py
    - Class: InputFailure(Exception)
      - Exception raised for an input exception message.
    - Class: RequirementFailure(Exception)
      - Exception raised for a requirement exception message.
    - Class: RemoveSectionFailure(Exception)
      - Exception raised for a removal section exception message.
    - Class: DictStructureFailure(Exception)
      - Exception raised for a dictionary structure exception message.
  - Module: int.py
    - Function: char_count
      - Counts the characters in value and returns the count of a specific character.
  - Module: list.py
    - Function: find_substring
      - Finds a substring based on the start and end match values.
    - Function: str_to_list
      - Take any string and converts it based on the separator. The difference between this function and .split() is that this function allows lists to pass through and sections of the value to be excluded. Source list values will pass through.
    - Function: remove_duplicate_dict_values_in_list
      - Removes duplicate values in a dictionary within a list and returns the same list minus duplicates.
    - Function: get_list_of_dicts_duplicates
      - This function finds duplicate dictionary values in the list using the key and return the value and index points.
    - Function: get_list_duplicates
      - Finds duplicate entries in the list and return the value and index points.
    - Function: sort_list
      - Sorts a list. Mixed types (ex: int, str) can not be sorted together by default. This function sorts a list of any value based on the string equivalent.
  - Module: str.py
    - Function: list_to_str
      - Take any list and converts the list to a string. Source string values will pass through.
    - Function: find_longest_common_substring
      - This function finds the longest substring between two different strings.
    - Function: clean_non_word_characters
      - This function will remove any non-word hex characters from any passing string.
    - Function: remove_section
      - Offers the ability to remove a section of a string using removal value(s).
* Directory/Modules: directors
  - Module: email_director.py
    - Class: CreateTemplateFailure(Exception)
      - Exception raised for the template creation failure.
    - Class: EmailSendFailure(Exception)
      - Exception raised for an email send failure.
    - Function: create_template_email
      - Uses the jinja2 module to create a template with users passing email template arguments.
    - Function: send_email
      - This function offers many customized options when sending an email.
  - Module: encryption_director.py
    - Class: EncryptionFailure(Exception)
      - Exception raised for an encryption failure.
    - Class: DecryptionFailure(Exception)
      - Exception raised for a decryption failure.
    - Class: DecryptionSiteFailure(Exception)
      - Exception raised for a decryption site failure.
    - Function: encrypt_info
      - This function encrypts any message that is sent.
    - Function: decrypt_info
      - This function decrypts any message that is sent.
    - Function: launch_decryptor_website
      - Creates the decryptor website to decrypt messages.
  - Module: file_director.py
    - Class: FileWriteFailure(Exception)
      - Exception raised for file write failures.
    - Class: FileSearchFailure(Exception)
      - Exception raised for file search failures.
    - Function: write_file
      - Writes a value to the file.
    - Function: search_file
      - Searches single or multiple files for a value.
    - Function: convert_relative_to_full_path
      - Determines a full file path to file given a relative file path compatible with PyInstaller(compiler) built-in.
    - Function: user_file_selection
      - Provides a simple user interface that numerically lists a set of files found using user submitted criteria.
  - Module: html_director.py
    - Class: HTMLConverter(HTMLParser)
      - Converts HTML to another format.
      - See "Method" docstrings for more details.
  - Module: ini_config_director.py
    - Function: read_ini_config
      - Reads configuration INI file data and returns the read configuration.
  - Module: log_director.py
    - Class: LoggerSetupFailure(Exception)
      - Exception raised for a logger setup failure.
    - Function: create_logger
      - This function creates a logger based on specific parameters.
    - Function: setup_logger_yaml
      - This function sets up a logger for the program using a YAML file.
  - Module: subprocess_director.py
    - Class: SubprocessStartFailure(Exception)
      - Exception raised for the subprocess start failure.
    - Class: AttributeDictionary(dict)
      - This class helps convert an object in a dictionary to dict.key opposed to using dict['key'].
    - Function: start_subprocess
      - This function runs a subprocess when called and returns the output in an easy-to-reference attribute style dictionary similar to the original subprocess output return.
  - Module: thread_director.py
    - Class: ThreadStartFailure(Exception)
      - Exception raised for the thread start failure.
    - Function: start_function_thread
      - This function is used to start any other function inside its thread.
  - Module: yaml_director.py
    - Class: YamlReadFailure(Exception)
      - Exception raised for the thread start failure.
    - Function: read_yaml_config
      - Reads configuration YAML file data and returns the read configuration.
