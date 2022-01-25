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
from fchecker import type_check, file_check
from ictoolkit.helpers.py_helper import get_function_name

# Exceptions
from fexception import FGeneralError, FTypeError, FCustomException, FFileNotFoundError


__author__ = 'IncognitoCoding'
__copyright__ = 'Copyright 2022, encryption_director'
__credits__ = ['IncognitoCoding']
__license__ = 'GPL'
__version__ = '2.1'
__maintainer__ = 'IncognitoCoding'
__status__ = 'Production'


class EncryptionFailure(Exception):
    """
    Exception raised for a encryption failure.

    Args:
        exc_message:\\
        \t\\- The failure reason.
    """
    __module__ = 'builtins'

    exc_message: str

    def __init__(self, exc_message: str) -> None:
        self.exc_message = exc_message


class DecryptionFailure(Exception):
    """
    Exception raised for a decryption failure.

    Args:
        exc_message:\\
        \t\\- The failure reason.
    """
    __module__ = 'builtins'

    exc_message: str

    def __init__(self, exc_message: str) -> None:
        self.exc_message = exc_message


class DecryptionSiteFailure(Exception):
    """
    Exception raised for a decryption site failure.

    Args:
        exc_message:\\
        \t\\- The failure reason.
    """
    __module__ = 'builtins'

    exc_message: str

    def __init__(self, exc_message: str) -> None:
        self.exc_message = exc_message


def encrypt_info(decrypted_info: str, message_encryption_password: str, message_encryption_random_salt: Union[bytes, str]) -> bytes:
    """
    This function encrypts any message that is sent.

    Args:
        decrypted_info (str):
        \t\\- decrypted info in bytes format.
        message_encryption_password (str):
        \t\\- The password needing to be used to encrypt the info.
        message_encryption_random_salt (Union[bytes, str]):
        \t\\- A random salt in bytes format.\\
        \t\\- If the value is sent as str format the value will be re-encoded.\\
        \t\\- A string type can pass if the value is set in a YAML or configuration file and not re-encoded correctly.

    Raises:
        FTypeError (fexception):
        \t\\- The value '{decrypted_info}' is not in <class 'str'> format.
        FTypeError (fexception):
        \t\\- The value '{message_encryption_password}' is not in <class 'str'> format.
        FTypeError (fexception):
        \t\\- The value '{message_encryption_random_salt}' is not in [<class 'bytes'>, <class 'str'>] format.
        EncryptionFailure:
        \t\\- A failure occurred while encrypting the message.

    Returns:
        bytes:\\
        \t\\- encrypted info
    """
    logger = logging.getLogger(__name__)
    logger.debug(f'=' * 20 + get_function_name() + '=' * 20)
    # Custom flowchart tracking. This is ideal for large projects that move a lot.
    # For any third-party modules, set the flow before making the function call.
    logger_flowchart = logging.getLogger('flowchart')
    logger_flowchart.debug(f'Flowchart --> Function: {get_function_name()}')

    try:
        type_check(decrypted_info, str)
        type_check(message_encryption_password, str)
        type_check(message_encryption_random_salt, [bytes, str])
    except FTypeError:
        raise

    logger.debug(
        'Passing parameters:\n'
        f'  - decrypted_info (str):\n        - {str(decrypted_info)}\n'
        f'  - message_encryption_password (str):\n        - {message_encryption_password}\n'
        f'  - message_encryption_random_salt (bytes, str):\n        - {str(message_encryption_random_salt)}\n'
    )

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
    except Exception as exc:
        exc_args = {
            'main_message': 'A failure occurred while encrypting the message.',
            'custom_type': EncryptionFailure,
            'original_exception': exc
        }
        raise EncryptionFailure(FCustomException(exc_args))
    else:
        logger.debug(f'Returning the encrypted info. encrypted_info = {encrypted_info}')
        # Returning the encrypted info.
        return encrypted_info


def decrypt_info(encrypted_info: Union[bytes, str], message_encryption_password: str, message_encryption_random_salt: Union[bytes, str]) -> bytes:
    """
    This function decrypts any message that is sent.

    Args:
        encrypted_info (Union[bytes, str]):
        \t\\- Encrypted message in bytes format. If the value is sent as str format the value will be re-encoded.\\
        \t\\- A string type can happen if the value is set in a YAML or configuration file and not re-encoded correctly.\\
        message_encryption_password (str):
        \t\\- The password needing to be used to encrypt the info.\\
        message_encryption_random_salt (Union[bytes, str]):
        \t\\- A random salt in bytes format. If the value is sent as str format the value will be re-encoded.\\
        \t\\- A string type can happen if the value is set in a YAML or configuration file and not re-encoded correctly.

    Raises:
        FTypeError (fexception):
        \t\\- The value '{encrypted_info}' is not in [<class 'bytes'>, <class 'str'>] format.
        FTypeError (fexception):
        \t\\- The value '{message_encryption_password}' is not in <class 'str'> format.
        FTypeError (fexception):
        \t\\- The value '{message_encryption_random_salt}' is not in [<class 'bytes'>, <class 'str'>] format.
        DecryptionFailure:
        \t\\- A failure occurred while decrypting the message.
        DecryptionFailure:
        \t\\- An invalid Key failure occurred while decrypting the info.
        FGeneralError (fexception):
        \t\\- A general exception occurred while decrypting the info.

    Returns:
        bytes:
        \t\\- Decrypted info.
    """
    logger = logging.getLogger(__name__)
    logger.debug(f'=' * 20 + get_function_name() + '=' * 20)
    # Custom flowchart tracking. This is ideal for large projects that move a lot.
    # For any third-party modules, set the flow before making the function call.
    logger_flowchart = logging.getLogger('flowchart')
    logger_flowchart.debug(f'Flowchart --> Function: {get_function_name()}')

    try:
        type_check(encrypted_info, [bytes, str])
        type_check(message_encryption_password, str)
        type_check(message_encryption_random_salt, [bytes, str])
    except FTypeError:
        raise

    logger.debug(
        'Passing parameters:\n'
        f'  - encrypted_info (bytes, str):\n        - {str(encrypted_info)}\n'
        f'  - message_encryption_password (str):\n        - {message_encryption_password}\n'
        f'  - message_encryption_random_salt (bytes, str):\n        - {str(message_encryption_random_salt)}\n'
    )

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
    except Exception as exc:
        exc_args = {
            'main_message': 'A failure occurred while decrypting the message.',
            'custom_type': DecryptionFailure,
            'original_exception': exc
        }
        raise DecryptionFailure(FCustomException(exc_args))
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
        except InvalidToken as exc:
            exc_args = {
                'main_message': 'An invalid Key failure occurred while decrypting the info.',
                'custom_type': DecryptionFailure,
                'original_exception': exc
            }
            raise DecryptionFailure(FCustomException(exc_args))
        except Exception as exc:
            exc_args = {
                'main_message': 'A general exception occurred while decrypting the info.',
                'original_exception': exc,
            }
            raise FGeneralError(exc_args)


def launch_decryptor_website(encryption_password: str, random_salt: Union[bytes, str], decryptor_template_path: str = None, port: int = None) -> None:
    """
    Creates the decryptor website to decrypt messages.

    The html file in the templates path must be called decryptor.html, but the file can be edited.

    Args:
        encryption_password (str):
        \t\\- Password used to encrypt the info.
        random_salt (Union[bytes, str]):
        \t\\- Random salt string used to encrypt the info. If the value is sent as str format the value will be re-encoded.\\
        \t\\- A string type can happen if the value is set in a YAML or configuration file and not re-encoded correctly.\\
        decryptor_template_path (str, optional):
        \t\\- The full path to the decryptor template directory.\\
        \t\\- Default creates/uses a template folder in the programs main program path.
        port (int, optional):
        \t\\- A port number to access the decrytor site. Defaults to port 5000.

    Raises:
        FTypeError (fexception):
        \t\\- The value '{encryption_password}' is not in <class 'str'> format.
        FTypeError (fexception):
        \t\\- The value '{random_salt}' is not in [<class 'bytes'>, <class 'str'>] format.
        FTypeError (fexception):
        \t\\- The value '{decryptor_template_path}' is not in <class 'str'> format.
        FTypeError (fexception):
        \t\\- The value '{port}' is not in <class 'int'> format.
        DecryptionSiteFailure:
        \t\\- The decryption website failed to start.
    """
    logger = logging.getLogger(__name__)
    logger.debug(f'=' * 20 + get_function_name() + '=' * 20)
    # Custom flowchart tracking. This is ideal for large projects that move a lot.
    # For any third-party modules, set the flow before making the function call.
    logger_flowchart = logging.getLogger('flowchart')
    logger_flowchart.debug(f'Flowchart --> Function: {get_function_name()}')

    try:
        type_check(encryption_password, str)
        type_check(random_salt, [bytes, str])
        if decryptor_template_path:
            type_check(decryptor_template_path, str)
        if port:
            type_check(port, int)
    except FTypeError:
        raise

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
        f'  - encryption_password (str):\n        - {encryption_password}\n'
        f'  - random_salt (bytes, str):\n        - {str(random_salt)}\n'
        f'{formatted_decryptor_template_path}\n'
        f'{formatted_port}\n'
    )

    try:
        if decryptor_template_path is None:
            # Gets the main program root directory.
            main_script_path = pathlib.Path.cwd()
            decryptor_template_path = os.path.abspath(f'{main_script_path}/templates')
            # Checks if the decryptor_template_path exists and if not it will be created.
            if not os.path.exists(decryptor_template_path):
                os.makedirs(decryptor_template_path)
            logger.debug(f'No template path was sent. Using the default path.\n  - {decryptor_template_path}')
        else:
            logger.debug(f'Template path was sent. Using the template path.\n  - {decryptor_template_path}')
        decryptor_template_file_path = os.path.abspath(f'{decryptor_template_path}/decrypt.html')
        file_check(decryptor_template_file_path, 'decrypt.html')

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
            except Exception as exc:
                if 'An invalid Key failure occurred while decrypting the info' in str(exc):
                    decrypted_message = f'The submitted encrypted message does not have a matching key or salt to decrypt. The info did not decrypt.'
                else:
                    decrypted_message = exc
            # Returns values to web.
            return render_template('decrypt.html', decrypted_message=decrypted_message)

        logger.debug('Sending the decrypted message to the webpage')
        if port:
            serve(http_info_decryptor, host="0.0.0.0", port=port)
        else:
            serve(http_info_decryptor, host="0.0.0.0", port=5000)
    except FFileNotFoundError:
        raise
    except Exception as exc:
        exc_args = {
            'main_message': 'The decryption website failed to start.',
            'custom_type': DecryptionSiteFailure,
            'original_exception': exc
        }
        raise DecryptionSiteFailure(FCustomException(exc_args))
