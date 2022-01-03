"""
This module is designed to assist with message encryption. The module has the ability to encrypt or decrypt messages.

Required Companion Modules:
    - pip install cryptography
    - pip install flask
    - pip install waitress
"""
# Built-in/Generic Imports
import logging
import pathlib
import os
from typing import Union

# Libraries
from cryptography.fernet import Fernet, InvalidToken
import base64
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from flask import Flask, render_template, request
from waitress import serve

# Own module
from ictoolkit.directors.validation_director import value_type_validation
from ictoolkit.directors.error_director import error_formatter
from ictoolkit.directors.file_director import file_exist_check
from ictoolkit.helpers.py_helper import get_function_name, get_line_number

__author__ = 'IncognitoCoding'
__copyright__ = 'Copyright 2021, encryption_director'
__credits__ = ['IncognitoCoding']
__license__ = 'GPL'
__version__ = '1.2'
__maintainer__ = 'IncognitoCoding'
__status__ = 'Development'


def encrypt_info(decrypted_info: str, message_encryption_password: str, message_encryption_random_salt: Union[bytes, str]) -> bytes:
    """
    This function encrypts any message that is sent.

    Args:
        decrypted_info (str): decrypted info in bytes format.
        message_encryption_password (str): The password needing to be used to encrypt the info.
        message_encryption_random_salt (bytes or str): A random salt in bytes format. If the value is sent as str format the value will be re-encoded.
                                                                                     A string type can happen if the value is set in a YAML or configuration file and not re-encoded correctly.\n

    Raises:
        TypeError: The value '{decrypted_info}' is not in str format.
        TypeError: The value '{message_encryption_password}' is not in str format.
        TypeError: The value '{message_encryption_random_salt}' is not in bytes format.
        Exception: Forwarding caught {type(error).__name__} at line {error.__traceback__.tb_lineno} in <{__name__}>
        Exception: A general exception occurred during the value type validation.
        Exception: Forwarding caught {type(error).__name__} at line {error.__traceback__.tb_lineno} in <{__name__}>
        Exception: A general exception occurred while encrypting the info.

    Returns:
        bytes: encrypted info
    """
    logger = logging.getLogger(__name__)
    logger.debug(f'=' * 20 + get_function_name() + '=' * 20)
    # Custom flowchart tracking. This is ideal for large projects that move a lot.
    # For any third-party modules, set the flow before making the function call.
    logger_flowchart = logging.getLogger('flowchart')
    logger_flowchart.debug(f'Flowchart --> Function: {get_function_name()}')

    # Checks function launch variables and logs passing parameters.
    try:
        # Validates required types.
        value_type_validation(decrypted_info, str, __name__, get_line_number())
        value_type_validation(message_encryption_password, str, __name__, get_line_number())
        value_type_validation(message_encryption_random_salt, [bytes, str], __name__, get_line_number())

        logger.debug(
            'Passing parameters:\n'
            f'  - decrypted_info (str):\n        - {str(decrypted_info)}'
            f'  - message_encryption_password (str):\n        - {message_encryption_password}'
            f'  - message_encryption_random_salt (bytes, str):\n        - {str(message_encryption_random_salt)}'
        )
    except Exception as error:
        if 'Originating error on line' in str(error):
            logger.debug(f'Forwarding caught {type(error).__name__} at line {error.__traceback__.tb_lineno} in <{__name__}>')
            raise error
        else:
            error_args = {
                'main_message': 'A general exception occurred during the value type validation.',
                'error_type': Exception,
                'original_error': error,
            }
            error_formatter(error_args, __name__, error.__traceback__.tb_lineno)

    logger.debug(f'Starting to encrypt the info')
    try:
        logger.debug('Converting the pre-defined encryption password to bytes')
        # Converts decrypted message string into bytes.
        decrypted_info = decrypted_info.encode()
        # Converting the pre-defined encryption password to bytes.
        password = message_encryption_password.encode()

        # Checks if incoming salt is in str format, so the salt can be re-encoded.
        if isinstance(message_encryption_random_salt, str):
            if message_encryption_random_salt[:2] == "b'":
                # Strips the bytes section off the input.
                # Removes first 2 characters.
                unconverted_message_encryption_random_salt = message_encryption_random_salt[2:]
                # Removes last character.
                unconverted_message_encryption_random_salt = unconverted_message_encryption_random_salt[:-1]
                # Re-encodes the info.
                message_encryption_random_salt = unconverted_message_encryption_random_salt.encode().decode('unicode_escape').encode("raw_unicode_escape")

        logger.debug('Deriving a cryptographic key from a password')
        # Calling function to derive a cryptographic key from a password.
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),  # An instance of HashAlgorithm
            length=32,  # The desired length of the derived key in bytes. Maximum is (232 - 1)
            salt=message_encryption_random_salt,  # Secure values [1] are 128-bits (16 bytes) or longer and randomly generated
            iterations=100000,  # The number of iterations to perform of the hash function
            backend=default_backend()  # An optional instance of PBKDF2HMACBackend
        )

        logger.debug('Returned from imported function (PBKDF2HMAC) to function (encrypt_info)')
        logger.debug('Encoding the string using the pre-defined encryption password and the cryptographic key into the binary form')
        # Encoding the string using the pre-defined encryption password and the cryptographic key into the binary form.
        key = base64.urlsafe_b64encode(kdf.derive(password))

        logger.debug('Creating a symmetric authenticated cryptography (secret key)')
        # Creating a symmetric authenticated cryptography (secret key).
        f = Fernet(key)

        logger.debug('Encrypting the info using the secret key to create a Fernet token')
        # Encrypting the info using the secret key to create a Fernet token.
        encrypted_info = f.encrypt(decrypted_info)
    except Exception as error:
        if 'Originating error on line' in str(error):
            logger.debug(f'Forwarding caught {type(error).__name__} at line {error.__traceback__.tb_lineno} in <{__name__}>')
            raise error
        else:
            error_args = {
                'main_message': 'A general exception occurred while encrypting the info.',
                'error_type': Exception,
                'original_error': error,
            }
            error_formatter(error_args, __name__, error.__traceback__.tb_lineno)
    else:
        logger.debug(f'Returning the encrypted info. encrypted_info = {encrypted_info}')
        # Returning the encrypted info.
        return encrypted_info


def decrypt_info(encrypted_info: Union[bytes, str], message_encryption_password: str, message_encryption_random_salt: Union[bytes, str]) -> bytes:
    """
    This function decrypts any message that is sent.

    Args:
        encrypted_info (bytes or str): Encrypted message in bytes format. If the value is sent as str format the value will be re-encoded.
                                                       A string type can happen if the value is set in a YAML or configuration file and not re-encoded correctly.\n
        message_encryption_password (str): The password needing to be used to encrypt the info.
        message_encryption_random_salt (bytes or str): A random salt in bytes format. If the value is sent as str format the value will be re-encoded.
                                                                                     A string type can happen if the value is set in a YAML or configuration file and not re-encoded correctly.\n

    Raises:
        TypeError: The value '{encrypted_info}' is not in bytes format.
        TypeError: The value '{message_encryption_password}' is not in str format.
        TypeError: The value '{message_encryption_random_salt}' is not in bytes format.
        Exception: Forwarding caught {type(error).__name__} at line {error.__traceback__.tb_lineno} in <{__name__}>
        Exception: A general exception occurred during the value type validation.
        Exception: Forwarding caught {type(error).__name__} at line {error.__traceback__.tb_lineno} in <{__name__}>
        Exception: A general exception occurred while decrypting the info.
        Exception: An invalid Key failure occurred while decrypting the info.
        Exception: Forwarding caught {type(error).__name__} at line {error.__traceback__.tb_lineno} in <{__name__}>
        Exception: A general exception occurred while decrypting the info.

    Returns:
        bytes: Decrypted info.
    """
    logger = logging.getLogger(__name__)
    logger.debug(f'=' * 20 + get_function_name() + '=' * 20)
    # Custom flowchart tracking. This is ideal for large projects that move a lot.
    # For any third-party modules, set the flow before making the function call.
    logger_flowchart = logging.getLogger('flowchart')
    logger_flowchart.debug(f'Flowchart --> Function: {get_function_name()}')

    # Checks function launch variables and logs passing parameters.
    try:
        # Validates required types.
        value_type_validation(encrypted_info, [bytes, str], __name__, get_line_number())
        value_type_validation(message_encryption_password, str, __name__, get_line_number())
        value_type_validation(message_encryption_random_salt, [bytes, str], __name__, get_line_number())

        logger.debug(
            'Passing parameters:\n'
            f'  - encrypted_info (bytes, str):\n        - {str(encrypted_info)}'
            f'  - message_encryption_password (str):\n        - {message_encryption_password}'
            f'  - message_encryption_random_salt (bytes, str):\n        - {str(message_encryption_random_salt)}'
        )
    except Exception as error:
        if 'Originating error on line' in str(error):
            logger.debug(f'Forwarding caught {type(error).__name__} at line {error.__traceback__.tb_lineno} in <{__name__}>')
            raise error
        else:
            error_args = {
                'main_message': 'A general exception occurred during the value type validation.',
                'error_type': Exception,
                'original_error': error,
            }
            error_formatter(error_args, __name__, error.__traceback__.tb_lineno)

    logger.debug(f'Starting to decrypt the info')
    try:
        # Converting the pre-defined encryption password to bytes.
        password = message_encryption_password.encode()

        logger.debug('Setting random salt string that is (16 bytes) used to help protect from dictionary attacks')

        # Checks if incoming salt is in str format, so the salt can be re-encoded.
        if isinstance(message_encryption_random_salt, str):
            if message_encryption_random_salt[:2] == "b'":
                # Strips the bytes section off the input.
                # Removes first 2 characters.
                unconverted_message_encryption_random_salt = message_encryption_random_salt[2:]
                # Removes last character.
                unconverted_message_encryption_random_salt = unconverted_message_encryption_random_salt[:-1]
                # Re-encodes the info.
                message_encryption_random_salt = unconverted_message_encryption_random_salt.encode().decode('unicode_escape').encode("raw_unicode_escape")

        # Checks if incoming salt is in str format, so the salt can be re-encoded.
        if isinstance(encrypted_info, str):
            if encrypted_info[:2] == "b'":
                # Strips the bytes section off the input.
                # Removes first 2 characters.
                unconverted_encrypted_info = encrypted_info[2:]
                # Removes last character.
                unconverted_encrypted_info = unconverted_encrypted_info[:-1]
                # Re-encodes the info.
                encrypted_info = unconverted_encrypted_info.encode().decode('unicode_escape').encode("raw_unicode_escape")

        # Calling function to derive a cryptographic key from a password
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),  # An instance of HashAlgorithm
            length=32,  # The desired length of the derived key in bytes. Maximum is (232 - 1)
            salt=message_encryption_random_salt,  # Secure values [1] are 128-bits (16 bytes) or longer and randomly generated
            iterations=100000,  # The number of iterations to perform of the hash function
            backend=default_backend()  # An optional instance of PBKDF2HMACBackend
        )

        logger.debug('Returned from imported function (PBKDF2HMAC) to function (encrypt_info)')
        logger.debug('Encoding the string using the pre-defined encryption password and the cryptographic key into the binary form')
        # Encoding the string using the pre-defined encryption password and the cryptographic key into the binary form.
        key = base64.urlsafe_b64encode(kdf.derive(password))

        # Creating a symmetric authenticated cryptography (secret key)
        f = Fernet(key)
    except Exception as error:
        if 'Originating error on line' in str(error):
            logger.debug(f'Forwarding caught {type(error).__name__} at line {error.__traceback__.tb_lineno} in <{__name__}>')
            raise error
        else:
            error_args = {
                'main_message': 'A general exception occurred while decrypting the info.',
                'error_type': Exception,
                'original_error': error,
            }
            error_formatter(error_args, __name__, error.__traceback__.tb_lineno)
    else:

        try:
            logger.debug('Decrypting the info using the secret key to create a Fernet token.')
            # Decrypting the info using the secret key to create a Fernet token.
            decrypted_info = f.decrypt(encrypted_info)
            # Converts bytes to Unicode string.
            decrypted_info = decrypted_info.decode()
            logger.debug(f'Returning the decrypted info. decrypted_info = {decrypted_info}')
            # Returning the decrypted info
            return decrypted_info
        except InvalidToken as error:
            error_args = {
                'main_message': 'An invalid Key failure occurred while decrypting the info.',
                'error_type': InvalidToken,
                'original_error': error,
            }
            error_formatter(error_args, __name__, error.__traceback__.tb_lineno)
        except Exception as error:
            if 'Originating error on line' in str(error):
                logger.debug(f'Forwarding caught {type(error).__name__} at line {error.__traceback__.tb_lineno} in <{__name__}>')
                raise error
            else:
                error_args = {
                    'main_message': 'A general exception occurred while decrypting the info.',
                    'error_type': Exception,
                    'original_error': error,
                }
                error_formatter(error_args, __name__, error.__traceback__.tb_lineno)


def launch_decryptor_website(encryption_password: str, random_salt: Union[bytes, str], decryptor_template_path: str = None, port: int = None) -> None:
    """
    Starts the decryptor website. The html file in the templates path must be called decryptor.html, but the file can be edited.

    Args:
        encryption_password (str): Password used to encrypt the info.
        random_salt (bytes or str): Random salt string used to encrypt the info. If the value is sent as str format the value will be re-encoded.
                                                  A string type can happen if the value is set in a YAML or configuration file and not re-encoded correctly.
        decryptor_template_path (str): The full path to the decryptor template directory. Defaults to None. Default templates folder path is the programs main program path.
        port (int): A port number to access the decrytor site. Defaults to port 5000.

    Raises:
        TypeError: The value '{encrypted_info}' is not in bytes format.
        TypeError: The value '{message_encryption_password}' is not in str format.
        TypeError: The value '{message_encryption_random_salt}' is not in bytes format.
        Exception: Forwarding caught {type(error).__name__} at line {error.__traceback__.tb_lineno} in <{__name__}>
        Exception: A general exception occurred during the value type validation.
    """
    logger = logging.getLogger(__name__)
    logger.debug(f'=' * 20 + get_function_name() + '=' * 20)
    # Custom flowchart tracking. This is ideal for large projects that move a lot.
    # For any third-party modules, set the flow before making the function call.
    logger_flowchart = logging.getLogger('flowchart')
    logger_flowchart.debug(f'Flowchart --> Function: {get_function_name()}')

    # Checks function launch variables and logs passing parameters.
    try:
        # Validates required types.
        value_type_validation(encryption_password, str, __name__, get_line_number())
        value_type_validation(random_salt, [bytes, str], __name__, get_line_number())
        if decryptor_template_path:
            value_type_validation(decryptor_template_path, str, __name__, get_line_number())
        if port:
            value_type_validation(port, int, __name__, get_line_number())

        if decryptor_template_path:
            formatted_decryptor_template_path = f'  - decryptor_template_path (str):\n        - {decryptor_template_path}'
        else:
            formatted_decryptor_template_path = f'  - decryptor_template_path (str):\n        - None'
        if port:
            formatted_port = f'  - port (int):\n        - {port}'
        else:
            formatted_port = f'  - port (int):\n        - None'

        logger.debug(
            'Passing parameters:\n'
            f'  - encryption_password (str):\n        - {encryption_password}'
            f'  - random_salt (bytes, str):\n        - {str(random_salt)}'
            f'{formatted_decryptor_template_path}'
            f'{formatted_port}'
        )
    except Exception as error:
        if 'Originating error on line' in str(error):
            logger.debug(f'Forwarding caught {type(error).__name__} at line {error.__traceback__.tb_lineno} in <{__name__}>')
            raise error
        else:
            error_args = {
                'main_message': 'A general exception occurred during the value type validation.',
                'error_type': Exception,
                'original_error': error,
            }
            error_formatter(error_args, __name__, error.__traceback__.tb_lineno)

    try:
        if decryptor_template_path is None:
            # Gets the main program root directory.
            main_script_path = pathlib.Path.cwd()

            # Checks that the main root program directory has the correct save folders created.
            # Sets the template directory save path. Checks if the path includes the templates folder or not.
            if 'templates' in str(main_script_path):
                decryptor_template_path = os.path.abspath(main_script_path)
            else:
                decryptor_template_path = os.path.abspath(f'{main_script_path}/templates')
            # Checks if the decryptor_template_path exists and if not it will be created.
            if not os.path.exists(decryptor_template_path):
                os.makedirs(decryptor_template_path)
            logger.debug(f'No template path was sent. Using the default path.\n  - {decryptor_template_path}')
        else:
            logger.debug(f'Template path was sent. Using the template path.\n  - {decryptor_template_path}')
        decryptor_template_file_path = os.path.abspath(f'{decryptor_template_path}/decrypt.html')
        file_exist_check(decryptor_template_file_path, 'decrypt.html')

        # Creates Flask instance with a specified template folder path.
        http_info_decryptor = Flask(__name__, template_folder=decryptor_template_path)

        # Checks if incoming salt is in str format, so the salt can be re-encoded.
        if isinstance(random_salt, str):
            if random_salt[:2] == "b'":
                # Strips the bytes section off the input.
                # Removes first 2 characters.
                unconverted_random_salt = random_salt[2:]
                # Removes last character.
                unconverted_random_salt = unconverted_random_salt[:-1]
                # Re-encodes the info.
                random_salt = unconverted_random_salt.encode().decode('unicode_escape').encode("raw_unicode_escape")

        @http_info_decryptor.route('/')
        def decryptor_form():
            return render_template('decrypt.html')

        @http_info_decryptor.route('/', methods=['POST'])
        def decryptor_form_post():
            # Requests input.
            encrypted_info = request.form['text']
            logger.debug(f'The user submitted encrypted_info through the website.\n  - {encrypted_info}')
            try:
                # Calling function to decrypt the encrypted info.
                decrypted_message = decrypt_info(encrypted_info, encryption_password, random_salt)
                logger.debug(f'The encrypted message has been decrypted.\n  - {decrypted_message}')
            except Exception as error:
                if 'An invalid Key failure occurred while decrypting the info' in str(error):
                    decrypted_message = f'The submitted encrypted message does not have a matching key or salt to decrypt. The info did not decrypt.'
                else:
                    decrypted_message = error
            # Returns values to web.
            return render_template('decrypt.html', decrypted_message=decrypted_message)

        logger.debug('Sending the decrypted message to the webpage')
        if port:
            serve(http_info_decryptor, host="0.0.0.0", port=port)
        else:
            serve(http_info_decryptor, host="0.0.0.0", port=5000)
    except Exception as error:
        if 'Originating error on line' in str(error):
            logger.debug(f'Forwarding caught {type(error).__name__} at line {error.__traceback__.tb_lineno} in <{__name__}>')
            raise error
        else:
            error_args = {
                'main_message': 'A general exception occurred while decrypting the info through the website.',
                'error_type': Exception,
                'original_error': error,
            }
            error_formatter(error_args, __name__, error.__traceback__.tb_lineno)
