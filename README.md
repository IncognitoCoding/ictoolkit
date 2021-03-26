# ictoolkit
 
ictoolkit is designed to be the swiss army knife of programming methods. This package is ever-growing and includes many useful methods. Some methods are not complex but often used, so they help keep the main code less congested and provide error catching. Available methods will be listed below, but further details will be listed within each functions docstring.

## Package Highlights:
* A growing list of useful methods to help assist with general programming.
* Some methods accept an optional logger parameter to assist with additional troubleshooting.
* All methods have error catching built into them.

## Package/Method/Function Info:
* Package: directors
  - Method: dict_director
    - Function: remove_duplicate_dict_values_in_list
      - Removes duplicate values in a dictionary within a list and returns the same list minus duplicates.
  - Method: email_director
    - Function: send_email
      - This function offers many customized options when sending an email. Email can be sent with port 25 or using TLS. Email messages can be sent encrypted or unencrypted.
    - Function: encrypt_info
      - This function encrypts any message that is sent.
    - Function: decrypt_info
      - This function decrypts any message that is sent.
  - Method: file_director
    - Function: write_file
      - Writes a value to the file.
    - Function: file_exist_check
      - Validates the file exists.
    - Function: search_file
      - Searches the file for a value. The search can look for multiple values when the searching value arguments are passed as a list. A single-string search is supported as well.
    - Function: search_multiple_files
      - Searches multiple files for a value. Requires the file_path to be sent as a list. The search can look for multiple values when the searching value arguments are passed as a list. A single-string search is supported as well.
    - Function: check_file_threshold_size
      - Checks threshold on the log file. If the threshold is exceeded, the log file will be cleared.
  - Method: ini_config_director
    - Function: read_ini_config
      - Reads configuration ini file data and returns the returns the read configuration.
    - Function: get_ini_config
      - Gets the ini configuration section key based on the read configuration and the section.
  - Method: log_director
    - Function: create_logger
      - Creates a logger based on specific parameters. The logger is passed back and can be used throughout the program.
  - Method: subprocess_director
    - Function: start_subprocess
      - This function runs a subprocess when called and returns the output in an easy-to-reference attribute style dictionary similar to the original subprocess output return.
  - Method: thread_director
    - Function: start_function_thread
      - This function is used to start any other function inside it's own thread. This is ideal if you need to have part of the program sleep and another part of the program always active (ex: Web Interface = Always Active & Log Checking = 10 Minute Sleep)
  - Method: yaml_director
    - Function: read_yaml_config
      - Reads configuration yaml file data and returns the returns the read configuration.
    - Function: yaml_value_validation
      - YAML value validations are performed within this function. Any validation that does not pass will throw a message statement, and the program will exit.
