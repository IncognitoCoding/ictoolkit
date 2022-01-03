"""
This module is designed to assist with message encryption. The module has the ability to encrypted or unencrypted messages.
"""
# Built-in/Generic Imports
import logging
from typing import Union

# Libraries
from cryptography.fernet import Fernet, InvalidToken
import base64
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

# Own module
from ictoolkit.directors.validation_director import value_type_validation
from ictoolkit.directors.error_director import error_formatter
from ictoolkit.helpers.py_helper import get_function_name, get_line_number

__author__ = 'IncognitoCoding'
__copyright__ = 'Copyright 2021, encryption_director'
__credits__ = ['IncognitoCoding']
__license__ = 'GPL'
__version__ = '1.1'
__maintainer__ = 'IncognitoCoding'
__status__ = 'Development'


def encrypt_info(unencrypted_info: str, message_encryption_password: str, message_encryption_random_salt: Union[bytes, str]) -> bytes:
    """
    This function encrypts any message that is sent.

    Args:
        unencrypted_info (str): Unencrypted info in bytes format.
        message_encryption_password (str): The password needing to be used to encrypt the info.
        message_encryption_random_salt (bytes or str): A random salt in bytes format. If the value is sent as str format the value will be re-encoded. 
                                                                                     A string type can happen if the value is set in a YAML or configuration file and not re-encoded correctly.\n

    Raises:
        TypeError: The value '{unencrypted_info}' is not in str format.
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
        value_type_validation(unencrypted_info, str, __name__, get_line_number())
        value_type_validation(message_encryption_password, str, __name__, get_line_number())
        value_type_validation(message_encryption_random_salt, [bytes, str], __name__, get_line_number())

        logger.debug(
            'Passing parameters:\n'
            f'  - unencrypted_info (str):\n        - {str(unencrypted_info)}'
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
        # Converts unencrypted message string into bytes.
        unencrypted_info = unencrypted_info.encode()
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
        encrypted_info = f.encrypt(unencrypted_info)
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
