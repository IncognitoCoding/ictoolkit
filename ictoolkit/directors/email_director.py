#!interpreter

"""
This module is designed to assist with email-related actions. The module has the ability to send emails encrypted or unencrypted.
"""
# Built-in/Generic Imports
import os
import sys
import logging
import traceback
import smtplib
import re
from email.message import EmailMessage
from typing import Optional

# Libraries
from cryptography.fernet import Fernet, InvalidToken
import base64
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from jinja2 import Environment, PackageLoader, select_autoescape

__author__ = 'IncognitoCoding'
__copyright__ = 'Copyright 2021, email_director'
__credits__ = ['IncognitoCoding', 'Monoloch']
__license__ = 'GPL'
__version__ = '1.7'
__maintainer__ = 'IncognitoCoding'
__status__ = 'Development'


def encrypt_info(email_settings: dict, unencrypted_info: bytes) -> bytes:
    """
    This function encrypts any message that is sent.

    Args:
        email_settings (dict): Email settings constructed within a dictionary.\n
        - email_settings Key/Value:
            - message_encryption_password (str): The password needing to be used to encrypt the info.
            - message_encryption_random_salt (bytes): A random salt in bytes format.\n
        unencrypted_info (bytes): Unencrypted info in bytes format.

    Raises:
        ValueError: A failure occurred while encrypting the info.

    Returns:
        bytes: encrypted info
    """
    logger = logging.getLogger(__name__)
    logger.debug(f'=' * 20 + traceback.extract_stack(None, 2)[1][2] + '=' * 20)
    # Custom flowchart tracking. This is ideal for large projects that move a lot.
    # For any third-party modules, set the flow before making the function call.
    logger_flowchart = logging.getLogger('flowchart')
    # Deletes the flowchart log if one already exists.
    logger_flowchart.debug(f'Flowchart --> Function: {traceback.extract_stack(None, 2)[1][2]}')

    # ###############################################
    # ##############Parameter Validation#############
    # ###############################################
    #
    # Verifies the email settings are in string format.
    if not isinstance(email_settings, dict):
        error_message = (
            'The email settings are not in dictionary format.\n'
            + (('-' * 150) + '\n') + (('-' * 65) + 'Additional Information' + ('-' * 63) + '\n') + (('-' * 150) + '\n')
            + 'Expected Result:\n'
            f'  - Type = dict\n\n'
            'Returned Result:\n'
            f'  - Type = {type(email_settings)}\n\n'
            f'Originating error on line {traceback.extract_stack()[-1].lineno} in <{__name__}>\n'
            + (('-' * 150) + '\n') * 2
        )
        logger.error(error_message)
        raise TypeError(error_message)
    # Verifies the unencrypted info is in bytes format.
    if not isinstance(unencrypted_info, bytes):
        error_message = (
            'The unencrypted info is not in bytes format.\n'
            + (('-' * 150) + '\n') + (('-' * 65) + 'Additional Information' + ('-' * 63) + '\n') + (('-' * 150) + '\n')
            + 'Expected Result:\n'
            f'  - Type = bytes\n\n'
            'Returned Result:\n'
            f'  - Type = {type(unencrypted_info)}\n\n'
            f'Originating error on line {traceback.extract_stack()[-1].lineno} in <{__name__}>\n'
            + (('-' * 150) + '\n') * 2
        )
        logger.error(error_message)
        raise TypeError(error_message)
    # Checks if the message_encryption_password is being passed to the function.
    if not email_settings.get('message_encryption_password'):
        error_message = (
            'The message encryption password value is missing.\n'
            + (('-' * 150) + '\n') + (('-' * 65) + 'Additional Information' + ('-' * 63) + '\n') + (('-' * 150) + '\n')
            + 'Expected Result:\n'
            f'  - A message encryption password\n\n'
            'Returned Result:\n'
            f'  - message_encryption_password = None\n\n'
            'Suggested Resolution:\n'
            '   - Please verify you have set the correct key value in the email_settings dictionary.\n\n'
            f'Originating error on line {traceback.extract_stack()[-1].lineno} in <{__name__}>\n'
            + (('-' * 150) + '\n') * 2
        )
        logger.error(error_message)
        raise TypeError(error_message)
    # Checks if the message_encryption_random_salt is being passed to the function.
    if not email_settings.get('message_encryption_random_salt'):
        error_message = (
            'The message encryption random salt value is missing.\n'
            + (('-' * 150) + '\n') + (('-' * 65) + 'Additional Information' + ('-' * 63) + '\n') + (('-' * 150) + '\n')
            + 'Expected Result:\n'
            f'  - A message encryption random salt\n\n'
            'Returned Result:\n'
            f'  - message_encryption_random_salt = None\n\n'
            'Suggested Resolution:\n'
            '   - Please verify you have set the correct key value in the email_settings dictionary.\n\n'
            f'Originating error on line {traceback.extract_stack()[-1].lineno} in <{__name__}>\n'
            + (('-' * 150) + '\n') * 2
        )
        logger.error(error_message)
        raise TypeError(error_message)

    # ###############################################
    # ########Parameter Debug Format/Write###########
    # ###############################################
    #
    # Requires pre-logger formatting because the logger can not use one line if/else or join without excluding sections of the the output.
    formatted_email_settings = '  - email_settings (dict):\n        - ' + '\n        - '.join(': '.join((key, str(val))) for (key, val) in email_settings.items())
    logger.debug(
        'Passing parameters:\n'
        f'{formatted_email_settings}\n'
        f'  - unencrypted_info (bytes:\n        - {unencrypted_info}\n'
    )

    # ###############################################
    # #############Primary Function Code#############
    # ###############################################
    #
    logger.debug(f'Starting to encrypt the info')
    try:
        logger.debug('Converting the pre-defined encryption password to bytes')
        # Converting the pre-defined encryption password to bytes.
        password = email_settings.get('message_encryption_password').encode()

        logger.debug('Setting random salt string that is (16 bytes) used to help protect from dictionary attacks')
        # Setting random salt string that is a (byte) used to help protect from dictionary attacks.
        # The salt string is randomly generated on the initial setup but static after the initial setup.
        salt = email_settings.get('message_encryption_random_salt')

        logger.debug('Deriving a cryptographic key from a password')
        # Calling function to derive a cryptographic key from a password.
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),  # An instance of HashAlgorithm
            length=32,  # The desired length of the derived key in bytes. Maximum is (232 - 1)
            salt=salt,  # Secure values [1] are 128-bits (16 bytes) or longer and randomly generated
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
        error_message = (
            f'A failure occurred while encrypting the info.\n\n'
            + (('-' * 150) + '\n') + (('-' * 65) + 'Additional Information' + ('-' * 63) + '\n') + (('-' * 150) + '\n')
            + f'{error}\n\n'
            f'Originating error on line {traceback.extract_stack()[-1].lineno} in <{__name__}>\n'
            + (('-' * 150) + '\n') * 2
        )
        logger.error(error_message)
        raise ValueError(error_message)
    else:
        logger.debug(f'Returning the encrypted info. encrypted_info = {encrypted_info}')
        # Returning the encrypted info.
        return encrypted_info


def decrypt_info(email_settings: dict, encrypted_info: bytes) -> bytes:
    """
    This function decrypts any message that is sent.

    Args:
        email_settings (dict): email settings constructed within a dictionary\n
        - email_settings Key/Value:
            - message_encryption_password (str): The password needing to be used to encrypt the info.
            - message_encryption_random_salt (bytes): A random salt in bytes format.\n
        encrypted_info (bytes): Encrypted message in bytes format. Re-encoding may be required.

    Raises:
        ValueError: A failure occurred while decrypting the info.
        ValueError: An invalid Key failure occurred while decrypting the info.

    Returns:
        bytes: Decrypted info.
    """
    logger = logging.getLogger(__name__)
    logger.debug(f'=' * 20 + traceback.extract_stack(None, 2)[1][2] + '=' * 20)
    # Custom flowchart tracking. This is ideal for large projects that move a lot.
    # For any third-party modules, set the flow before making the function call.
    logger_flowchart = logging.getLogger('flowchart')
    # Deletes the flowchart log if one already exists.
    logger_flowchart.debug(f'Flowchart --> Function: {traceback.extract_stack(None, 2)[1][2]}')

    # ###############################################
    # ##############Parameter Validation#############
    # ###############################################
    #
    # Verifies the email settings are in string format.
    if not isinstance(email_settings, dict):
        error_message = (
            'The email settings are not in dictionary format.\n'
            + (('-' * 150) + '\n') + (('-' * 65) + 'Additional Information' + ('-' * 63) + '\n') + (('-' * 150) + '\n')
            + 'Expected Result:\n'
            f'  - Type = dict\n\n'
            'Returned Result:\n'
            f'  - Type = {type(email_settings)}\n\n'
            f'Originating error on line {traceback.extract_stack()[-1].lineno} in <{__name__}>\n'
            + (('-' * 150) + '\n') * 2
        )
        logger.error(error_message)
        raise TypeError(error_message)
    # Verifies the encrypted info is in bytes format.
    if not isinstance(encrypted_info, bytes):
        error_message = (
            'The encrypted info is not in bytes format.\n'
            + (('-' * 150) + '\n') + (('-' * 65) + 'Additional Information' + ('-' * 63) + '\n') + (('-' * 150) + '\n')
            + 'Expected Result:\n'
            f'  - Type = bytes\n\n'
            'Returned Result:\n'
            f'  - Type = {type(encrypted_info)}\n\n'
            f'Originating error on line {traceback.extract_stack()[-1].lineno} in <{__name__}>\n'
            + (('-' * 150) + '\n') * 2
        )
        logger.error(error_message)
        raise TypeError(error_message)
    # Checks if the message_encryption_password is being passed to the function.
    if not email_settings.get('message_encryption_password'):
        error_message = (
            'The message encryption password value is missing.\n'
            + (('-' * 150) + '\n') + (('-' * 65) + 'Additional Information' + ('-' * 63) + '\n') + (('-' * 150) + '\n')
            + 'Expected Result:\n'
            f'  - A message encryption password\n\n'
            'Returned Result:\n'
            f'  - message_encryption_password = None\n\n'
            'Suggested Resolution:\n'
            '   - Please verify you have set the correct key value in the email_settings dictionary.\n\n'
            f'Originating error on line {traceback.extract_stack()[-1].lineno} in <{__name__}>\n'
            + (('-' * 150) + '\n') * 2
        )
        logger.error(error_message)
        raise TypeError(error_message)
    # Checks if the message_encryption_random_salt is being passed to the function.
    if not email_settings.get('message_encryption_random_salt'):
        error_message = (
            'The message encryption random salt value is missing.\n'
            + (('-' * 150) + '\n') + (('-' * 65) + 'Additional Information' + ('-' * 63) + '\n') + (('-' * 150) + '\n')
            + 'Expected Result:\n'
            f'  - A message encryption random salt\n\n'
            'Returned Result:\n'
            f'  - message_encryption_random_salt = None\n\n'
            'Suggested Resolution:\n'
            '   - Please verify you have set the correct key value in the email_settings dictionary.\n\n'
            f'Originating error on line {traceback.extract_stack()[-1].lineno} in <{__name__}>\n'
            + (('-' * 150) + '\n') * 2
        )
        logger.error(error_message)
        raise TypeError(error_message)

    # ###############################################
    # ########Parameter Debug Format/Write###########
    # ###############################################
    #
    # Requires pre-logger formatting because the logger can not use one line if/else or join without excluding sections of the the output.
    formatted_email_settings = '  - email_settings (dict):\n        - ' + '\n        - '.join(': '.join((key, str(val))) for (key, val) in email_settings.items())
    logger.debug(
        'Passing parameters:\n'
        f'{formatted_email_settings}\n'
        f'  - encrypted_info (bytes:\n        - {encrypted_info}\n'
    )

    # ###############################################
    # #############Primary Function Code#############
    # ###############################################
    #
    logger.debug(f'Starting to decrypt the info')
    try:
        # Converting the pre-defined encryption password to bytes.
        password = email_settings.get('message_encryption_password').encode()

        logger.debug('Setting random salt string that is (16 bytes) used to help protect from dictionary attacks')
        # Setting random salt string that is a (byte) used to help protect from dictionary attacks.
        # The salt string is randomly generated on the initial setup but static after the initial setup.
        salt = email_settings.get('message_encryption_random_salt')

        # Calling function to derive a cryptographic key from a password
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),  # An instance of HashAlgorithm
            length=32,  # The desired length of the derived key in bytes. Maximum is (232 - 1)
            salt=salt,  # Secure values [1] are 128-bits (16 bytes) or longer and randomly generated
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
        error_message = (
            f'A failure occurred while decrypting the info.\n\n'
            + (('-' * 150) + '\n') + (('-' * 65) + 'Additional Information' + ('-' * 63) + '\n') + (('-' * 150) + '\n')
            + f'{error}\n\n'
            f'Originating error on line {traceback.extract_stack()[-1].lineno} in <{__name__}>\n'
            + (('-' * 150) + '\n') * 2
        )
        logger.error(error_message)
        raise ValueError(error_message)
    else:

        try:
            logger.debug('Decrypting the info using the secret key to create a Fernet token.')
            # Decrypting the info using the secret key to create a Fernet token.
            decrypted_info = f.decrypt(encrypted_info)

            logger.debug(f'Returning the decrypted info. decrypted_info = {decrypted_info}')
            # Returning the decrypted info
            return decrypted_info
        except InvalidToken as err:
            error_message = (
                f'An invalid Key failure occurred while decrypting the info.\n\n'
                + (('-' * 150) + '\n') + (('-' * 65) + 'Additional Information' + ('-' * 63) + '\n') + (('-' * 150) + '\n')
                + f'{err}\n\n'
                f'Originating error on line {traceback.extract_stack()[-1].lineno} in <{__name__}>\n'
                + (('-' * 150) + '\n') * 2
            )
            logger.error(error_message)
            raise ValueError(error_message)


def create_template_email(email_template_name: str, email_template_path: str, **template_args: Optional[dict]) -> str:
    """
    Uses the jinja2 module to create a template with users passing email template arguments.

    Args:
        email_template_name (str): The name of the template.
        email_template_path (str): The full path to the templates directory.
        **template_args(dict, optional): The template arguments are used to populate the HTML template variables. Defaults to None.

    Returns:
        str: A formatted HTML email template with all the arguments updated.
    """
    logger = logging.getLogger(__name__)
    logger.debug(f'=' * 20 + traceback.extract_stack(None, 2)[1][2] + '=' * 20)
    # Custom flowchart tracking. This is ideal for large projects that move a lot.
    # For any third-party modules, set the flow before making the function call.
    logger_flowchart = logging.getLogger('flowchart')
    # Deletes the flowchart log if one already exists.
    logger_flowchart.debug(f'Flowchart --> Function: {traceback.extract_stack(None, 2)[1][2]}')

    # ###############################################
    # ##############Parameter Validation#############
    # ###############################################
    #
    # Verifies the template name is in string format.
    if not isinstance(email_template_name, str):
        error_message = (
            'The template name is not in string format.\n'
            + (('-' * 150) + '\n') + (('-' * 65) + 'Additional Information' + ('-' * 63) + '\n') + (('-' * 150) + '\n')
            + 'Expected Result:\n'
            f'  - Type = str\n\n'
            'Returned Result:\n'
            f'  - Type = {type(email_template_name)}\n\n'
            f'Originating error on line {traceback.extract_stack()[-1].lineno} in <{__name__}>\n'
            + (('-' * 150) + '\n') * 2
        )
        logger.error(error_message)
        raise TypeError(error_message)
    # Checks if the email_template_path exists.
    if not os.path.exists(email_template_path):
        error_message = (
            'The email HTML template path does not exist.\n'
            + (('-' * 150) + '\n') + (('-' * 65) + 'Additional Information' + ('-' * 63) + '\n') + (('-' * 150) + '\n')
            + 'Expected Result:\n'
            f'  - a valid email template path\n\n'
            'Returned Result:\n'
            f'  - email_template_path = {email_template_path}\n\n'
            'Suggested Resolution:\n'
            '   - Please verify you have set the correct path and try again.\n\n'
            f'Originating error on line {traceback.extract_stack()[-1].lineno} in <{__name__}>\n'
            + (('-' * 150) + '\n') * 2
        )
        print(error_message)
        raise ValueError(error_message)

    # ###############################################
    # ########Parameter Debug Format/Write###########
    # ###############################################
    #
    if template_args:
        # Requires pre-logger formatting because the logger can not use one line if/else or join without excluding sections of the the output.
        formatted_template_args = '  - template_args (dict):\n        - ' + '\n        - '.join(': '.join((key, str(val))) for (key, val) in template_args.items())
    else:
        formatted_template_args = '  - template_args (dict):\n        - None\n'
    logger.debug(
        'Passing parameters:\n'
        f'  - email_template_name (str):\n        - {email_template_name}\n'
        f'  - email_template_path (str):\n        - {email_template_path}\n'
        f'{formatted_template_args}\n'
    )

    # ###############################################
    # #############Primary Function Code#############
    # ###############################################
    #
    try:
        # Gets the main program module name.
        # Output Example: C:\Repositories\smtpredirect\smtpredirect\smtpredirect.py
        main_module_file_path = os.path.realpath(sys.argv[0]) if sys.argv[0] else None
        # Gets the main program base name.
        # Output Example: smtpredirect.py
        module_base_name = os.path.basename(main_module_file_path)
        # Gets the main program name.
        # Output Example: smtpredirect
        module_name = os.path.splitext(module_base_name)[0]

        env = Environment(
            loader=PackageLoader(module_name, email_template_path),
            autoescape=select_autoescape(['html', 'xml'])
        )
        template = env.get_template(email_template_name)

        # Returns
        return template.render(**template_args)
    except Exception as error:
        error_message = (
            f'A error occurred while rendering the HTML template.\n\n'
            + (('-' * 150) + '\n') + (('-' * 65) + 'Additional Information' + ('-' * 63) + '\n') + (('-' * 150) + '\n')
            + f'{error}\n\n'
            f'Originating error on line {error.__traceback__.tb_lineno} in <{__name__}>\n'
            + (('-' * 150) + '\n') * 2
        )
        logger.error(error_message)
        raise ValueError(error_message)


def send_email(email_settings: dict, subject: str, body: Optional[str] = None, template_args: Optional[dict] = None) -> None:
    """
    This function offers many customized options when sending an email. Email can be sent with port 25 or using TLS. Email sections can be sent encrypted or unencrypted.

    Emails can be sent using two options (You must use one or the other for an email to send.).
        - Non-HTML:
            - These messages are basic non HTML emails. Multiple lines are supported.
        - HTML:
            - These messages use HTML templates that can have variables in the HTML template get populated with data. HTML will be preferred if both are configured. Templates and variables
              require structure from HTMLs://jinja.palletsprojects.com. When using HTML, the jinja module is used in conjunction with some added features and simplified use from this function.

    String encryption can be added to any string in an email with the email_settings variables setup and the string section identified as needing to be encrypted.
    Any string section starting with @START-ENCRYPT@ and ending with @END-ENCRYPT@ will have that code section get encrypted and supported for the body or **template_args parameters.
    The encrypted message will be in bytes format. Formatting needs in the template or body of the message.
        - String Encryption Example1: <p>     Decryption Code:@START-ENCRYPT@This is my original string@END-ENCRYPT@</p>
        - String Encryption Example2: @START-ENCRYPT@This is my original string@END-ENCRYPT@

    Function parameters require the email settings to be sent in a dictionary format.
    Encryption Requirements:
        - The encrypt_info function is required when enabling message encryption.
        - The decrypt_info function is required when decrypting the message.
            - This function can be used outside the main program. The decrypt_info can be a small separate program or a website using flask.
        - To create a random "salt" use this command "print("urandom16 Key:", os.urandom(16))"

    Args:
        email_settings (dict): Email settings constructed within a dictionary\n
        - email_setting Keys/Values:\n
            - smtp (str): SMTP server.
            - authentication_required (bool): Enables authentication.
            - use_tls (str): Enables TLS.
            - username (str): Username for email authentication.
            - password (str): Password for email authentication.
            - from_email (str): From email address.
            - to_email (str): To email address.
            - send_email_template (bool, optional): Allows sending an email with an HTML template. Defaults to False.
            - email_template_name (str, optional): The template name. Defaults to None.
            - email_template_path (str, optional): The template folder path. This directory will hold all HTML templates. This path is commonly the directory of the main program. Defaults to None.
            - message_encryption_password (str, optional): Encryption password if encryption is enabled. Set to None if no encryption.
            - message_encryption_random_salt (bytes, optional): Random salt in bytes format. Set to None if no encryption.\n
        subject (str): Email subject information
        body (str, optional): The email body is for raw non-HTML email messages. Adding a message to this body will override any template options and use a basic non-HTML email message. Defaults to None.
        template_args(dict, optional): The template arguments are used to populate the HTML template variables. Defaults to None.
            \\- Example (url is the passing parameter):
                \\- <p><a href="{{ url }}">Decrypt</a></p>

    Raises:
        ValueError: Failed to send the email message. No email encryption option was selected
        ValueError: Failed to initialize SMTP connection using TLS.
        ValueError: Failed to send the email message. Connection to SMTP server failed.
        ValueError: Failed to send the email message. SMTP send error occurred.
        ValueError: Failed to send message. SMTP terminatation error occurred.
    """
    logger = logging.getLogger(__name__)
    logger.debug(f'=' * 20 + traceback.extract_stack(None, 2)[1][2] + '=' * 20)
    # Custom flowchart tracking. This is ideal for large projects that move a lot.
    # For any third-party modules, set the flow before making the function call.
    logger_flowchart = logging.getLogger('flowchart')
    # Deletes the flowchart log if one already exists.
    logger_flowchart.debug(f'Flowchart --> Function: {traceback.extract_stack(None, 2)[1][2]}')

    # ###############################################
    # ##############Parameter Validation#############
    # ###############################################
    #
    # Verifies the email settings are in dictionary format.
    if not isinstance(email_settings, dict):
        error_message = (
            'The email settings are not in dictionary format.\n'
            + (('-' * 150) + '\n') + (('-' * 65) + 'Additional Information' + ('-' * 63) + '\n') + (('-' * 150) + '\n')
            + 'Expected Result:\n'
            f'  - Type = dict\n\n'
            'Returned Result:\n'
            f'  - Type = {type(email_settings)}\n\n'
            f'Originating error on line {traceback.extract_stack()[-1].lineno} in <{__name__}>\n'
            + (('-' * 150) + '\n') * 2
        )
        logger.error(error_message)
        raise TypeError(error_message)
    # Verifies the template name is in string format.
    if not isinstance(subject, str):
        error_message = (
            'The subject is not in string format.\n'
            + (('-' * 150) + '\n') + (('-' * 65) + 'Additional Information' + ('-' * 63) + '\n') + (('-' * 150) + '\n')
            + 'Expected Result:\n'
            f'  - Type = str\n\n'
            'Returned Result:\n'
            f'  - Type = {type(subject)}\n\n'
            f'Originating error on line {traceback.extract_stack()[-1].lineno} in <{__name__}>\n'
            + (('-' * 150) + '\n') * 2
        )
        logger.error(error_message)
        raise TypeError(error_message)
    # Verifies the template name is in string format.
    if (
        not isinstance(body, str)
        and body is not None
    ):
        error_message = (
            'The body is not in string format or not set to None.\n'
            + (('-' * 150) + '\n') + (('-' * 65) + 'Additional Information' + ('-' * 63) + '\n') + (('-' * 150) + '\n')
            + 'Expected Result:\n'
            f'  - Type = str or None\n\n'
            'Returned Result:\n'
            f'  - Type = {type(body)}\n\n'
            f'Originating error on line {traceback.extract_stack()[-1].lineno} in <{__name__}>\n'
            + (('-' * 150) + '\n') * 2
        )
        logger.error(error_message)
        raise TypeError(error_message)

    # ###############################################
    # ########Parameter Debug Format/Write###########
    # ###############################################
    #
    # Requires pre-logger formatting because the logger can not use one line if/else or join without excluding sections of the the output.
    formatted_email_settings = '  - email_settings (dict):\n        - ' + '\n        - '.join(': '.join((key, str(val))) for (key, val) in email_settings.items())
    if body:
        f'  - body (str):\n        - {body}\n'
    else:
        f'  - body (str):\n        - None\n'
    if template_args:
        # Requires pre-logger formatting because the logger can not use one line if/else or join without excluding sections of the the output.
        formatted_template_args = '  - template_args (dict):\n        - ' + '\n        - '.join(': '.join((key, str(val))) for (key, val) in template_args.items())
    else:
        formatted_template_args = '  - template_args (dict):\n        - None\n'
    logger.debug(
        'Passing parameters:\n'
        f'{formatted_email_settings}\n'
        f'  - subject(str):\n        - {subject}\n'
        f'{body}\n'
        f'{formatted_template_args}\n'
    )

    # ###############################################
    # #############Primary Function Code#############
    # ###############################################
    #
    try:
        logger.debug(f'Starting to send an email message')
        logger.debug(f'Checking if the email is sending non-HTML or HTML')
        # Gets send_email_template option.
        send_email_template = email_settings.get('send_email_template')
        # Checks if the email is template or non-HTML.
        if (
            send_email_template is True
            and template_args
        ):
            logger.debug(f'Sending HTML templated email')
            email_template_name = email_settings.get('email_template_name')
            email_template_path = email_settings.get('email_template_path')

            # Creates the email template.
            email_body = create_template_email(email_template_name, email_template_path, **template_args)
        elif body:
            logger.debug(f'Sending non-HTML email')
            email_body = body
        else:
            error_message = (
                f'An error occurred while sending the email. No body or template was sent.\n\n'
                + (('-' * 150) + '\n') + (('-' * 65) + 'Additional Information' + ('-' * 63) + '\n') + (('-' * 150) + '\n')
                + 'Suggested Resolution:\n'
                '  - Ensure the body or template is being passed to the email_director module functions.\n\n'
                f'Originating error on line {traceback.extract_stack()[-1].lineno} in <{__name__}>\n'
                + (('-' * 150) + '\n') * 2
            )
            logger.error(error_message)
            raise ValueError(error_message)

        # Holds the updating email body lines.
        updating_body = []
        # Checks the email for any encryption identifiers.
        # Splits the email into individual lines that can be looped through.
        adjusted_body = email_body.split('\n')
        logger.debug(f'Looping through each line of the email to check for any encryption identifiers')
        for email_line in adjusted_body:
            # Checks if the body contains any encryption identifiers.
            if (
                '@START-ENCRYPT@' in email_line
                and '@END-ENCRYPT@' in email_line
            ):
                logger.debug(f'Encryption identifiers found. Encrypting this section of the output.')
                # Original String: <p>     Decryption Code: @START-ENCRYPT@This is my original string@END-ENCRYPT@</p>
                # Matched String: This is my original string
                unencrypted_string = (re.search('@START-ENCRYPT@(.*)@END-ENCRYPT@', email_line)).group(1)
                logger.debug('Converting unencrypted message string into bytes')
                # Converts unencrypted message string into bytes.
                encoded_message = unencrypted_string.encode()
                # Calls function to sends unencrypted message for encryption.
                # Return Example: <encrypted message>
                encrypted_info = encrypt_info(email_settings, encoded_message)
                # Removes the encryption string identifiers and sets encryption on the string.
                updating_body.append(email_line.replace('@START-ENCRYPT@', '').replace('@END-ENCRYPT@', '').replace(unencrypted_string, str(encrypted_info)))
            else:
                # Adds the non-encrypted line to the list.
                updating_body.append(email_line)

        logger.debug(f'Setting the updated email body')
        # Converts the list back into a string with new lines for each entry.
        updated_body = "\n".join(updating_body)
    except TypeError as error:
        error_message = (f'{error}Additional traceback reverse path line: {error.__traceback__.tb_lineno} in <{__name__}>\n')
        logger.debug(f'Forwarding caught ValueError at line {error.__traceback__.tb_lineno} in <{__name__}>')
        raise ValueError(error_message)
    except ValueError as error:
        error_message = (f'{error}Additional traceback reverse path line: {error.__traceback__.tb_lineno} in <{__name__}>\n')
        logger.debug(f'Forwarding caught ValueError at line {error.__traceback__.tb_lineno} in <{__name__}>')
        raise ValueError(error_message)
    except Exception as error:
        error_message = (
            f'An error occurred while sending the email.\n\n'
            + (('-' * 150) + '\n') + (('-' * 65) + 'Additional Information' + ('-' * 63) + '\n') + (('-' * 150) + '\n')
            + f'{error}\n\n'
            f'Originating error on line {error.__traceback__.tb_lineno} in <{__name__}>\n'
            + (('-' * 150) + '\n') * 2
        )
        logger.error(error_message)
        raise ValueError(error_message)

    logger.debug('Preparing the email message structure')
    # Preparing email message structure.
    message = EmailMessage()
    message['Subject'] = subject
    message['From'] = email_settings.get('from_email')
    message['To'] = [email_settings.get('to_email')]
    # Sets header based on HTML or text be passed to the function.
    if (
        send_email_template is True
        and template_args
    ):
        # Sets header for text and html. Required to allow html template.
        message.add_header('Content-Type', 'text/html')
    elif body:
        # Sets header for text only. Required to allow new lines.
        message.add_header('Content-Type', 'text')

    logger.debug('Setting payload to HTML')
    # Setting email body payload.
    message.set_payload(updated_body)

    try:
        logger.debug('Setting up SMTP object')
        # Setting up SMTP object.
        if email_settings.get('use_tls') is True:
            logger.debug('Opening connection to SMTP server on port 587 for TLS')
            smtp_Object = smtplib.SMTP(email_settings.get('smtp'), 587)

            try:
                smtp_Object.ehlo()
                logger.debug('Sending StartTLS message')
                smtp_Object.starttls()
            except Exception as err:
                error_message = (
                    f'Failed to initialize SMTP connection using TLS.\n\n'
                    + (('-' * 150) + '\n') + (('-' * 65) + 'Additional Information' + ('-' * 63) + '\n') + (('-' * 150) + '\n')
                    + f'{err}\n\n'
                    f'Originating error on line {traceback.extract_stack()[-1].lineno} in <{__name__}>\n'
                    + (('-' * 150) + '\n') * 2
                )
                logger.error(error_message)
                raise ValueError(error_message)
        else:
            logger.debug('Opening connection to SMTP server on port 25')
            smtp_Object = smtplib.SMTP(email_settings.get('smtp'), 25)
    except Exception as err:
        if (
            "target machine actively refused it" in str(err)
            or "connected party did not properly respond after a period of time" in str(err)
        ):
            error_message = (
                'Failed to send the email message. Connection to SMTP server failed.\n\n'
                + (('-' * 150) + '\n') + (('-' * 65) + 'Additional Information' + ('-' * 63) + '\n') + (('-' * 150) + '\n')
                + 'Suggested Resolution:\n'
                '  - Ensure the server address and TLS options are set correctly.\n\n'
                f'Originating error on line {traceback.extract_stack()[-1].lineno} in <{__name__}>\n'
                + (('-' * 150) + '\n') * 2
            )
            logger.error(error_message)
            raise ValueError(error_message)

    # Sends email.
    try:
        # If authentication required, log in to mail server with credentials.
        if email_settings.get('authentication_required') is True:
            logger.debug('SMTP server authentication required, logging into server')
            smtp_Object.login(email_settings.get('username'), email_settings.get('password'))
            logger.debug('Sending the email')

        smtp_Object.sendmail(email_settings.get('from_email'), email_settings.get('to_email'), message.as_string())
    except Exception as err:
        if "SMTP AUTH extension not supported" in str(err):
            err = "SMTP authentication is set to required but it is not supported by the server. Try changing the INI [email] AuthenticationRequired value to False"
        elif "Client host rejected: Access denied" in str(err):
            err = "The SMTP server rejected the connection.  Authentication may be required, ensure the INI [email] AuthenticationRequired is set correctly"
        elif "authentication failed" in str(err):
            err = "SMTP server authentication failed. Ensure the INI [email] Username and Password are set correctly"
        elif " Authentication Required. Learn more at\n5.7.0  HTMLs://support.google.com" in str(err):
            err = "Incorrect username and/or password or authentication_required is not enabled or Less Secure Apps needs enabled in your gmail settings"
        elif "Authentication Required" in str(err):
            err = "Incorrect username and/or password or the authentication_required setting is not enabled"
        error_message = (
            f'Failed to send the email message. SMTP send error occurred.\n\n'
            + (('-' * 150) + '\n') + (('-' * 65) + 'Additional Information' + ('-' * 63) + '\n') + (('-' * 150) + '\n')
            + f'{err}\n\n'
            f'Originating error on line {traceback.extract_stack()[-1].lineno} in <{__name__}>\n'
            + (('-' * 150) + '\n') * 2
        )
        logger.error(error_message)
        raise ValueError(error_message)

    finally:

        try:
            logger.debug(f'Terminating SMTP object')
            # Terminating SMTP object.
            smtp_Object.quit()
        except Exception as error:
            error_message = (
                f'Failed to send message. SMTP terminatation error occurred.\n\n'
                + (('-' * 150) + '\n') + (('-' * 65) + 'Additional Information' + ('-' * 63) + '\n') + (('-' * 150) + '\n')
                + f'{error}\n\n'
                f'Originating error on line {traceback.extract_stack()[-1].lineno} in <{__name__}>\n'
                + (('-' * 150) + '\n') * 2
            )
            logger.error(error_message)
            raise ValueError(error_message)
