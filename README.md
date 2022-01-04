# ictoolkit
 
ictoolkit is designed to be the swiss army knife of programming methods. This package is ever-growing and includes many useful methods. Some methods are not complex but often used, so they help keep the main code less congested and provide error catching. Available methods will be listed below, but further details will be listed within each functions docstring.

The requirements.txt file includes all required packages for all modules. If you only use a few modules from ictoolkit, it is worth running your code against the module to see which ones are missing.

## Package Highlights:
* A growing list of useful methods to help assist with general programming.
* Some methods accept an optional logger parameter to assist with additional troubleshooting.
* All methods have error catching built into them.

## Package/Method/Function Info:
* Package: directors
  - Method: data_structure_director
    - Function: remove_duplicate_dict_values_in_list
      - Removes duplicate values in a dictionary within a list and returns the same list minus duplicates.
    - Function: get_list_of_dicts_duplicates
      - Finds duplicate dictionary values in the list using the key and return the value and index points.
    - Function: get_list_duplicates
      - Finds duplicate entries in the list return the value and index points.
    - Function: string_grouper
      - String grouper will group a list of strings using three different options.
    - Function: find_longest_common_substring
      - This function finds the longest substring between two different strings.  
    - Function: user_choice_character_grouping
      - This function will remove any non-word hex characters from any passing string.  
  - Method: email_director
    - Function: create_template_email
      -  Uses the jinja2 module to create a template with users passing email template arguments.
    - Function: send_email
      - This function offers many customized options when sending an email. Email can be sent with port 25 or using TLS. Email messages can be sent encrypted or unencrypted.
  - Method: encryption_director
    - Function: encrypt_info
      - This function encrypts any message that is sent.
    - Function: decrypt_info
      - This function decrypts any message that is sent.
    - Function: launch_decryptor_website
      -  Creates the decryptor website to decrypt messages.
  - Method: error_director
    - Function: error_formatter
      - An error formatter to create consistent error output.   
  - Method: file_director
    - Function: write_file
      - Writes a value to the file.
    - Function: file_exist_check
      - Validates the file exists.
    - Function: search_file
      - Searches the file for a value.
    - Function: search_multiple_files
      - Searches multiple files for a value.
    - Function: convert_relative_to_full_path
      - Determines a full file path to file given a relative file path compatible with PyInstaller(compiler) built-in.
    - Function: user_file_selection
      - Provides a simple user interface that numerically lists a set of files found using user submitted criteria.
  - Method: html_director
    - Class: HTMLConverter
      - Converts html to a different output format. For example: html --> text.   
  - Method: ini_config_director
    - Function: read_ini_config
      - Reads configuration ini file data and returns the returns the read configuration.
    - Function: get_ini_config
      - Gets the ini configuration section key based on the read configuration and the section.
  - Method: log_director
    - Function: create_logger
      - Creates a logger based on specific parameters. The logger is passed back and can be used throughout the program.
    - Function: setup_logger_yaml
      - This function sets up a logger for the program using a YAML file. Default file log handler paths are supported when using this function.
  - Method: subprocess_director
    - Function: start_subprocess
      - This function runs a subprocess when called and returns the output in an easy-to-reference attribute style dictionary similar to the original subprocess output return.
  - Method: thread_director
    - Function: start_function_thread
      - This function is used to start any other function inside it's own thread. This is ideal if you need to have part of the program sleep and another part of the program always active (ex: Web Interface = Always Active & Log Checking = 10 Minute Sleep)
  - Method: validation_director
    - Function: value_type_validation
      - A simple type validation validation check. 
  - Method: yaml_director
    - Function: read_yaml_config
      - Reads configuration yaml file data and returns the returns the read configuration.
    - Function: yaml_value_validation
      - YAML value validations are performed within this function. Any validation that does not pass will throw a message statement, and the program will exit.
