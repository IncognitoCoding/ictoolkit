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
import mimetypes
from typing import Optional

# Libraries
from cryptography.fernet import Fernet, InvalidToken
import base64
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from jinja2 import Environment, PackageLoader, select_autoescape

# Own module
from ictoolkit.directors.validation_director import value_type_validation
from ictoolkit.directors.error_director import error_formatter
from ictoolkit.helpers.py_helper import get_function_name, get_line_number

__author__ = 'IncognitoCoding'
__copyright__ = 'Copyright 2021, email_director'
__credits__ = ['IncognitoCoding', 'Monoloch']
__license__ = 'GPL'
__version__ = '1.8'
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
    logger.debug(f'=' * 20 + get_function_name() + '=' * 20)
    # Custom flowchart tracking. This is ideal for large projects that move a lot.
    # For any third-party modules, set the flow before making the function call.
    logger_flowchart = logging.getLogger('flowchart')
    # Deletes the flowchart log if one already exists.
    logger_flowchart.debug(f'Flowchart --> Function: {get_function_name()}')

    # Checks function launch variables and logs passing parameters.
    try:
        # Validates required types.
        value_type_validation(email_settings, dict, __name__, get_line_number())
        value_type_validation(unencrypted_info, bytes, __name__, get_line_number())
        value_type_validation(email_settings.get('message_encryption_password'), str, __name__, get_line_number())
        value_type_validation(email_settings.get('message_encryption_random_salt'), bytes, __name__, get_line_number())

        # Requires pre-logger formatting because the logger can not use one line if/else or join without excluding sections of the the output.
        formatted_email_settings = '  - email_settings (dict):\n        - ' + '\n        - '.join(': '.join((key, str(val))) for (key, val) in email_settings.items())
        formatted_message_encryption_password = '  - message_encryption_password (str):\n        - ' + email_settings.get('message_encryption_password')
        formatted_message_encryption_random_salt = '  - message_encryption_random_salt (bytes):\n        - ' + email_settings.get('message_encryption_random_salt')

        logger.debug(
            'Passing parameters:\n'
            f'{formatted_email_settings}\n'
            f'{formatted_message_encryption_password}\n'
            f'{formatted_message_encryption_random_salt}\n'
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
    logger.debug(f'=' * 20 + get_function_name() + '=' * 20)
    # Custom flowchart tracking. This is ideal for large projects that move a lot.
    # For any third-party modules, set the flow before making the function call.
    logger_flowchart = logging.getLogger('flowchart')
    # Deletes the flowchart log if one already exists.
    logger_flowchart.debug(f'Flowchart --> Function: {get_function_name()}')

    # Checks function launch variables and logs passing parameters.
    try:
        # Validates required types.
        value_type_validation(email_settings, dict, __name__, get_line_number())
        value_type_validation(encrypted_info, bytes, __name__, get_line_number())
        value_type_validation(email_settings.get('message_encryption_password'), str, __name__, get_line_number())
        value_type_validation(email_settings.get('message_encryption_random_salt'), bytes, __name__, get_line_number())

        # Requires pre-logger formatting because the logger can not use one line if/else or join without excluding sections of the the output.
        formatted_email_settings = '  - email_settings (dict):\n        - ' + '\n        - '.join(': '.join((key, str(val))) for (key, val) in email_settings.items())
        formatted_message_encryption_password = '  - message_encryption_password (str):\n        - ' + email_settings.get('message_encryption_password')
        formatted_message_encryption_random_salt = '  - message_encryption_random_salt (bytes):\n        - ' + email_settings.get('message_encryption_random_salt')

        logger.debug(
            'Passing parameters:\n'
            f'{formatted_email_settings}\n'
            f'{formatted_message_encryption_password}\n'
            f'{formatted_message_encryption_random_salt}\n'
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
    logger.debug(f'=' * 20 + get_function_name() + '=' * 20)
    # Custom flowchart tracking. This is ideal for large projects that move a lot.
    # For any third-party modules, set the flow before making the function call.
    logger_flowchart = logging.getLogger('flowchart')
    # Deletes the flowchart log if one already exists.
    logger_flowchart.debug(f'Flowchart --> Function: {get_function_name()}')

    # Checks function launch variables and logs passing parameters.
    try:
        # Validates required types.
        value_type_validation(email_template_name, str, __name__, get_line_number())
        value_type_validation(email_template_path, str, __name__, get_line_number())
        if template_args:
            value_type_validation(template_args, dict, __name__, get_line_number())

        # Requires pre-logger formatting because the logger can not use one line if/else or join without excluding sections of the the output.
        if template_args:
            formatted_template_args = '  - template_args (dict):\n        - ' + '\n        - '.join(': '.join((key, str(val))) for (key, val) in template_args.items())
        else:
            formatted_template_args = '  - template_args (dict):\n        - None'

        logger.debug(
            'Passing parameters:\n'
            f'  - email_template_name (str):\n        - {email_template_name}\n'
            f'  - email_template_path (str):\n        - {email_template_path}\n'
            f'{formatted_template_args}\n'
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

    # Checks if the email_template_path exists.
    if not os.path.exists(email_template_path):
        error_args = {
            'main_message': 'The email HTML template path does not exist.',
            'error_type': ValueError,
            'expected_result': 'a valid email template path',
            'returned_result': email_template_path,
            'suggested_resolution': 'Please verify you have set the correct path and try again.',
        }
        error_formatter(error_args, __name__, get_line_number())

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
        if 'Originating error on line' in str(error):
            logger.debug(f'Forwarding caught {type(error).__name__} at line {error.__traceback__.tb_lineno} in <{__name__}>')
            raise error
        else:
            error_args = {
                'main_message': 'A general exception occurred while rendering the HTML template..',
                'error_type': Exception,
                'original_error': error,
            }
            error_formatter(error_args, __name__, error.__traceback__.tb_lineno)


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
            - attachment_path (str, optional): Allows sending an email attachment. Defaults to None.
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
    logger.debug(f'=' * 20 + get_function_name() + '=' * 20)
    # Custom flowchart tracking. This is ideal for large projects that move a lot.
    # For any third-party modules, set the flow before making the function call.
    logger_flowchart = logging.getLogger('flowchart')
    # Deletes the flowchart log if one already exists.
    logger_flowchart.debug(f'Flowchart --> Function: {get_function_name()}')

    # Checks function launch variables and logs passing parameters.
    try:
        # Validates required types.
        value_type_validation(email_settings, dict, __name__, get_line_number())
        value_type_validation(subject, str, __name__, get_line_number())
        if body:
            value_type_validation(body, str, __name__, get_line_number())
        value_type_validation(email_settings.get('message_encryption_random_salt'), bytes, __name__, get_line_number())
        if template_args:
            value_type_validation(template_args, dict, __name__, get_line_number())

        # Requires pre-logger formatting because the logger can not use one line if/else or join without excluding sections of the the output.
        formatted_email_settings = '  - email_settings (dict):\n        - ' + '\n        - '.join(': '.join((key, str(val))) for (key, val) in email_settings.items())
        if body:
            formatted_body = f'- email_template_name (str):\n        - {body}'
        else:
            formatted_body = f'- email_template_name (str):\n        - None'
        if template_args:
            formatted_template_args = '  - template_args (dict):\n        - ' + '\n        - '.join(': '.join((key, str(val))) for (key, val) in template_args.items())
        else:
            formatted_template_args = '  - template_args (dict):\n        - None'

        logger.debug(
            'Passing parameters:\n'
            f'{formatted_email_settings}\n'
            f'  - subject (str):\n        - {subject}\n'
            f'{formatted_body}\n'
            f'{formatted_template_args}\n'
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

    logger.debug(f'Starting to send an email message')

    try:
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
            error_args = {
                'main_message': 'An error occurred while sending the email. No body or template was sent.',
                'error_type': ValueError,
                'suggested_resolution': 'Ensure the body or template is being passed to the email_director module functions.',
            }
            error_formatter(error_args, __name__, get_line_number())

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
    except Exception as error:
        if 'Originating error on line' in str(error):
            logger.debug(f'Forwarding caught {type(error).__name__} at line {error.__traceback__.tb_lineno} in <{__name__}>')
            raise error
        else:
            error_args = {
                'main_message': 'A general exception occurred while creating the email message body.',
                'error_type': Exception,
                'original_error': error,
            }
            error_formatter(error_args, __name__, error.__traceback__.tb_lineno)

    try:
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
        # Attaches file if a path is sent.
        if email_settings.get('attachment_path'):
            # Checks that the attachment file exists.
            attachment_path = os.path.abspath(email_settings.get('attachment_path'))
            # Checks if the save_log_path exists and if not it will be created.
            if not os.path.exists(attachment_path):
                error_args = {
                    'main_message': 'The attachment path for the email message does not exist.',
                    'error_type': ValueError,
                    'expected_result': 'a valid email attachment path',
                    'returned_result': attachment_path,
                    'suggested_resolution': 'Please verify you have set the correct path and try again.',
                }
                error_formatter(error_args, __name__, get_line_number())
            # Gets the mime type to determine the type of message being sent.
            mime_type, _ = mimetypes.guess_type(attachment_path)
            # Gets the MIME type and subtype.
            mime_type, mime_subtype = mime_type.split('/', 1)
            # Attaches the attachment to the message.
            with open(attachment_path, 'rb') as ap:
                message.add_attachment(ap.read(), maintype=mime_type, subtype=mime_subtype, filename=os.path.basename(attachment_path))
    except Exception as error:
        if 'Originating error on line' in str(error):
            logger.debug(f'Forwarding caught {type(error).__name__} at line {error.__traceback__.tb_lineno} in <{__name__}>')
            raise error
        else:
            error_args = {
                'main_message': 'A general exception occurred while preparing the email message structure.',
                'error_type': Exception,
                'original_error': error,
            }
            error_formatter(error_args, __name__, error.__traceback__.tb_lineno)

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
            except Exception as error:
                error_args = {
                    'main_message': 'Failed to initialize SMTP connection using TLS.',
                    'error_type': Exception,
                    'original_error': error,
                }
                error_formatter(error_args, __name__, error.__traceback__.tb_lineno)
        else:
            logger.debug('Opening connection to SMTP server on port 25')
            smtp_Object = smtplib.SMTP(email_settings.get('smtp'), 25)
    except Exception as error:
        if 'Originating error on line' in str(error):
            logger.debug(f'Forwarding caught {type(error).__name__} at line {error.__traceback__.tb_lineno} in <{__name__}>')
            raise error
        else:
            if (
                "target machine actively refused it" in str(error)
                or "connected party did not properly respond after a period of time" in str(error)
                or "getaddrinfo failed" in str(error)
            ): 
                error_args = {
                    'main_message': 'Failed to send the email message. Connection to SMTP server failed.',
                    'error_type': ValueError,
                    'suggested_resolution': 'Ensure the server address and TLS options are set correctly.',
                }
                error_formatter(error_args, __name__, error.__traceback__.tb_lineno)
            elif 'Connection unexpectedly closed' in str(error):
                error_args = {
                    'main_message': 'Failed to send the email message. Connection to SMTP server failed.',
                    'error_type': ValueError,
                    'suggested_resolution': 'Ensure SMTP is reachable.',
                }
                error_formatter(error_args, __name__, error.__traceback__.tb_lineno)
            else:
                error_args = {
                    'main_message': 'A general exception occurred while sending the email message.',
                    'error_type': Exception,
                    'original_error': error,
                }
                error_formatter(error_args, __name__, error.__traceback__.tb_lineno)

    # Sends email.
    try:
        # If authentication required, log in to mail server with credentials.
        if email_settings.get('authentication_required') is True:
            logger.debug('SMTP server authentication required, logging into server')
            smtp_Object.login(email_settings.get('username'), email_settings.get('password'))
            logger.debug('Sending the email')

        smtp_Object.sendmail(email_settings.get('from_email'), email_settings.get('to_email'), message.as_string())
    except Exception as error:
        if 'Originating error on line' in str(error):
            logger.debug(f'Forwarding caught {type(error).__name__} at line {error.__traceback__.tb_lineno} in <{__name__}>')
            raise error
        else:
            error_args = {
                'main_message': 'A general exception occurred while creating the email message body.',
                'error_type': Exception,
                'original_error': error,
            }
            error_formatter(error_args, __name__, error.__traceback__.tb_lineno)

            if "SMTP AUTH extension not supported" in str(error):
                error_args = {
                    'main_message': 'SMTP authentication is set to required but it is not supported by the server.',
                    'error_type': Exception,
                    'suggested_resolution': 'Try changing the INI [email] AuthenticationRequired value to False',
                }
            elif "Client host rejected: Access denied" in str(error):
                error_args = {
                    'main_message': 'The SMTP server rejected the connection.',
                    'error_type': Exception,
                    'suggested_resolution': 'Authentication may be required, ensure the INI [email] AuthenticationRequired is set correctly',

                }
            elif "authentication failed" in str(error):
                error_args = {
                    'main_message': 'SMTP server authentication failed.',
                    'error_type': Exception,
                    'suggested_resolution': 'Ensure the INI [email] Username and Password are set correctly.',
                }
            elif " Authentication Required. Learn more at\n5.7.0  HTMLs://support.google.com" in str(error):
                error_args = {
                    'main_message': 'Incorrect username and/or password or authentication_required is not enabled or Less Secure Apps needs enabled in your gmail settings.',
                    'error_type': Exception,
                }
            elif "Authentication Required" in str(error):
                error_args = {
                    'main_message': 'Incorrect username and/or password or the authentication_required setting is not enabled.',
                    'error_type': Exception,
                }
            else:
                error_args = {
                    'main_message': 'A general exception occurred while sending the email.',
                    'error_type': Exception,
                    'original_error': error,
                }
            error_formatter(error_args, __name__, error.__traceback__.tb_lineno)

    finally:

        try:
            logger.debug(f'Terminating SMTP object')
            # Terminating SMTP object.
            smtp_Object.quit()
        except Exception as error:
            if 'Originating error on line' in str(error):
                logger.debug(f'Forwarding caught {type(error).__name__} at line {error.__traceback__.tb_lineno} in <{__name__}>')
                raise error
            else:
                if 'Failed to send message' in str(error):
                    error_args = {
                        'main_message': 'Failed to send message. SMTP terminatation error occurred.',
                        'error_type': Exception,
                        'original_error': error,
                    }
                else:
                    error_args = {
                        'main_message': 'A general exception occurred while terminating the SMTP object.',
                        'error_type': Exception,
                        'original_error': error,
                    }
                error_formatter(error_args, __name__, error.__traceback__.tb_lineno)
