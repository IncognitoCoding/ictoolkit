"""
This module is designed to assist with email-related actions. The module has the ability to send emails encrypted or unencrypted.
"""
# Built-in/Generic Imports
import os
import sys
import logging
import smtplib
import re
from email.message import EmailMessage
import mimetypes
from typing import Optional

# Libraries
from jinja2 import Environment, PackageLoader, select_autoescape
from fchecker import type_check

# Local Functions
from ..directors.encryption_director import encrypt_info
from ..helpers.py_helper import get_function_name

# Exceptions
from ..directors.encryption_director import EncryptionFailure
from fexception import FGeneralError, FTypeError, FCustomException

__author__ = 'IncognitoCoding'
__copyright__ = 'Copyright 2022, email_director'
__credits__ = ['IncognitoCoding', 'Monoloch']
__license__ = 'MIT'
__version__ = '3.2'
__maintainer__ = 'IncognitoCoding'
__status__ = 'Production'


class CreateTemplateFailure(Exception):
    """Exception raised for the template creation failure."""
    __module__ = 'builtins'
    pass


class EmailSendFailure(Exception):
    """Exception raised for an email send failure."""
    __module__ = 'builtins'
    pass


def create_template_email(email_template_name: str, email_template_path: str, **template_args: Optional[dict]) -> str:
    """
    Uses the jinja2 module to create a template with users passing email template arguments.

    Args:
        email_template_name (str):
        \t\\- The name of the template.
        email_template_path (str):
        \t\\- The full path to the templates directory.
        **template_args(dict, optional):
        \t\\- The template arguments are used to populate the HTML template variables. Defaults to None.

    Raises:
        FTypeError (fexception):
        \t\\- The value '{email_template_name}' is not in <class 'str'> format.
        FTypeError (fexception):
        \t\\- The value '{email_template_path}' is not in <class 'str'> format.
        FTypeError (fexception):
        \t\\- The value '{template_args}' is not in <class 'dict'> format.
        CreateTemplateFailure:
        \t\\- The email HTML template path does not exist.
        FGeneralError (fexception):
        \t\\- A general exception occurred while rendering the HTML template.

    Returns:
        str:
        \t\\- A formatted HTML email template with all the arguments updated.
    """
    logger = logging.getLogger(__name__)
    logger.debug(f'=' * 20 + get_function_name() + '=' * 20)
    # Custom flowchart tracking. This is ideal for large projects that move a lot.
    # For any third-party modules, set the flow before making the function call.
    logger_flowchart = logging.getLogger('flowchart')
    logger_flowchart.debug(f'Flowchart --> Function: {get_function_name()}')

    try:
        type_check(email_template_name, str)
        type_check(email_template_path, str)
        if template_args:
            type_check(template_args, dict)
    except FTypeError:
        raise

    if template_args:
        formatted_template_args = ('  - template_args (dict):\n        - '
                                   + '\n        - '.join(': '.join((key, str(val))) for (key, val) in template_args.items()))
    else:
        formatted_template_args = '  - template_args (dict):\n        - None'

    logger.debug(
        'Passing parameters:\n'
        f'  - email_template_name (str):\n        - {email_template_name}\n'
        f'  - email_template_path (str):\n        - {email_template_path}\n'
        f'{formatted_template_args}\n'
    )

    # Checks if the email_template_path exists.
    if not os.path.exists(email_template_path):
        exc_args = {
            'main_message': 'The email HTML template path does not exist.',
            'custom_type': CreateTemplateFailure,
            'expected_result': 'A valid email template path.',
            'returned_result': email_template_path,
            'suggested_resolution': 'Please verify you have set the correct path and try again.',
        }
        raise CreateTemplateFailure(FCustomException(exc_args))

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
    except Exception as exc:
        exc_args = {
            'main_message': 'A general exception occurred while rendering the HTML template.',
            'original_exception': exc,
        }
        raise FGeneralError(exc_args)
    else:
        return template.render(**template_args)


def send_email(email_settings: dict, subject: str, body: str = None, template_args: dict = None) -> None:
    """
    This function offers many customized options when sending an email.

    Email can be sent with port 25 or using TLS.

    Email sections can be sent encrypted or unencrypted.

    Emails can be sent using one of two options:
    \tNon-HTML:
    \t\t\\- These messages are basic non HTML emails. Multiple lines are supported.
    \tHTML:
    \t\t\\- These messages use HTML templates that can have variables in the HTML template get populated with data.\\
    \t\t\\- HTML will be preferred if both are configured.\\
    \t\t\\- Templates and variables require structure from HTMLs://jinja.palletsprojects.com.\\
    \t\t\\- When using HTML, the jinja module is used in conjunction with some added features and simplified use from this function.

    Email Encryption:
    \t String encryption can be added to any string in an email with the email_settings variables setup and\\
    \t the string section identified as needing to be encrypted.

    \t Any string section starting with @START-ENCRYPT@ and ending with @END-ENCRYPT@ will have that code section\\
    \t get encrypted and supported for the body or **template_args parameters.

    \t Encryption Requirements:
    \t\t\\- The encrypt_info function is required when enabling message encryption.\\
    \t\t\\- The decrypt_info function is required when decrypting the message.\\
    \t\t\t\\- This function can be used outside the main program.\\
    \t\t\t\\- The decrypt_info can be a small separate program or a website using flask.\\
    \t\t\\- To create a random "salt" use this command "print("urandom16 Key:", os.urandom(16))"\\

    \t Format Example:
    \t\t\\- The encrypted message will be in bytes format. Formatting needs in the template or body of the message.\\
    \t\t\t\\- Example1:
    \t\t\t\t\\- <p>     Decryption Code:@START-ENCRYPT@This is my original string@END-ENCRYPT@</p>\\
    \t\t\t\\- Example2:
    \t\t\t\t\\- @START-ENCRYPT@This is my original string@END-ENCRYPT@\\

    Args:
        email_settings (dict):
        \t\\- Email settings constructed within a dictionary\\
        subject (str):
        \t\\- Email subject information\\
        body (str, optional):
        \t\\- The email body is for raw non-HTML email messages.\\
        \t\\- Adding a message to this body will override any template options and use\\
        \t   a basic non-HTML email message.\\
        \t\\- Defaults to None.\\
        template_args(dict, optional):
        \t\\- The template arguments are used to populate the HTML template variables.\\
        \t\\- Defaults to None.\\
        \t\t\\- Example (url is the passing parameter):\\
        \t\t\t\\- <p><a href="{{ url }}">Decrypt</a></p>\\

    Arg Keys:
        email_settings Keys:\\
        \t\\- smtp (str):\\
        \t\t\\- SMTP server.\\
        \t\\- authentication_required (bool):\\
        \t\t\\- Enables authentication.\\
        \t\\- use_tls (str):\\
        \t\t\\- Enables TLS.
        \t\\- username (str):\\
        \t\t\\- Username for email authentication.\\
        \t\\- password (str):\\
        \t\t\\- Password for email authentication.\\
        \t\\- from_email (str):\\
        \t\t\\- From email address.\\
        \t\\- to_email (str):\\
        \t\t\\- To email address.\\
        \t\\- attachment_path (str, optional):\\
        \t\t\\- Allows sending an email attachment.\\
        \t\t\\- Defaults to None.\\
        \t\\- send_email_template (bool, optional):\\
        \t\t\\- Allows sending an email with an HTML template.\\
        \t\t\\- Defaults to False.\\
        \t\\- email_template_name (str, optional):\\
        \t\t\\- The template name.\\
        \t\t\\- Defaults to None.\\
        \t\\- email_template_path (str, optional):\\
        \t\t\\- The template folder path.\\
        \t\t\\- This directory will hold all HTML templates.\\
        \t\t\\- This path is commonly the directory of the main program.\\
        \t\t\\- Defaults to None.\\
        \t\\- message_encryption_password (str, optional):\\
        \t\t\\- Encryption password if encryption is enabled.\\
        \t\t\\- Set to None if no encryption.\\
        \t\\- message_encryption_random_salt (bytes, optional):\\
        \t\t\\- Random salt in bytes format.\\
        \t\t\\- Set to None if no encryption.

    Raises:
        FTypeError (fexception):
        \t\\- The value '{email_settings}' is not in <class 'dict'> format.
        FTypeError (fexception):
        \t\\- The value '{subject}' is not in <class 'str'> format.
        FTypeError (fexception):
        \t\\- The value '{body}' is not in <class 'str'> format.
        FTypeError (fexception):
        \t\\- The value '{template_args}' is not in <class 'dict'> format.
        EmailSendFailure:
        \t\\- An error occurred while sending the email.
        CreateTemplateFailure:
        \t\\- The email HTML template path does not exist.
        EncryptionFailure:
        \t\\- A failure occurred while encrypting the message.
        FGeneralError (fexception):
        \t\\- A general exception occurred while creating the email message body.
        EmailSendFailure:
        \t\\- The attachment path for the email message does not exist.
        FGeneralError (fexception):
        \t\\- A general exception occurred while preparing the email message structure.
        EmailSendFailure:
        \t\\- Failed to initialize SMTP connection using TLS.
        EmailSendFailure:
        \t\\- Failed to send the email message. Connection to SMTP server failed.
        EmailSendFailure:
        \t\\- Failed to reach the SMTP server.
        FGeneralError (fexception):
        \t\\- A general exception occurred while sending the email message.
        EmailSendFailure:
        \t\\- SMTP authentication is set to required but it is not supported by the server.
        EmailSendFailure:
        \t\\- The SMTP server rejected the connection.
        EmailSendFailure:
        \t\\- SMTP server authentication failed.
        EmailSendFailure:
        \t\\- Incorrect username and/or password or authentication_required is not enabled\\
        \t  or Less Secure Apps needs enabled in your gmail settings.
        EmailSendFailure:
        \t\\- Incorrect username and/or password or the authentication_required setting is not enabled.
        FGeneralError (fexception):
        \t\\- A general exception occurred while sending the email.
        EmailSendFailure:
        \t\\- Failed to send message. SMTP terminatation error occurred.
        FGeneralError (fexception):
        \t\\- A general exception occurred while terminating the SMTP object.
    """
    logger = logging.getLogger(__name__)
    logger.debug(f'=' * 20 + get_function_name() + '=' * 20)
    # Custom flowchart tracking. This is ideal for large projects that move a lot.
    # For any third-party modules, set the flow before making the function call.
    logger_flowchart = logging.getLogger('flowchart')
    logger_flowchart.debug(f'Flowchart --> Function: {get_function_name()}')

    try:
        type_check(email_settings, dict)
        type_check(subject, str)
        if body:
            type_check(body, str)
        if template_args:
            type_check(template_args, dict)
    except FTypeError:
        raise

    formatted_email_settings = ('  - email_settings (dict):\n        - '
                                + '\n        - '.join(': '.join((key, str(val))) for (key, val) in email_settings.items()))
    if body:
        formatted_body = f'- email_template_name (str):\n        - {body}'
    else:
        formatted_body = f'- email_template_name (str):\n        - None'
    if template_args:
        formatted_template_args = ('  - template_args (dict):\n        - '
                                   + '\n        - '.join(': '.join((key, str(val))) for (key, val) in template_args.items()))
    else:
        formatted_template_args = '  - template_args (dict):\n        - None'

    logger.debug(
        'Passing parameters:\n'
        f'{formatted_email_settings}\n'
        f'  - subject (str):\n        - {subject}\n'
        f'{formatted_body}\n'
        f'{formatted_template_args}\n'
    )

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
            exc_args = {
                'main_message': 'An error occurred while sending the email.',
                'custom_type': EmailSendFailure,
                'expected_result': 'Body or HTML Template',
                'returned_result': 'No body or template was sent.',
                'suggested_resolution': 'Ensure the body or template is being passed to the email_director module functions.',
            }
            raise EmailSendFailure(FCustomException(exc_args))
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
                password = email_settings.get('message_encryption_password')
                salt = email_settings.get('message_encryption_random_salt')
                # Calls function to sends unencrypted message for encryption.
                # Return Example: <encrypted message>
                encrypted_info = encrypt_info(unencrypted_string, password, salt)
                # Removes the encryption string identifiers and sets encryption on the string.
                updating_body.append(email_line.replace('@START-ENCRYPT@', '').replace('@END-ENCRYPT@', '').replace(unencrypted_string, str(encrypted_info)))
            else:
                # Adds the non-encrypted line to the list.
                updating_body.append(email_line)

        logger.debug(f'Setting the updated email body')
        # Converts the list back into a string with new lines for each entry.
        updated_body = "\n".join(updating_body)
    except CreateTemplateFailure:
        raise
    except EmailSendFailure:
        raise
    except EncryptionFailure:
        raise
    except Exception as exc:
        exc_args = {
            'main_message': 'A general exception occurred while creating the email message body.',
            'original_exception': exc,
        }
        raise FGeneralError(exc_args)

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
            if not os.path.exists(attachment_path):
                exc_args = {
                    'main_message': 'The attachment path for the email message does not exist.',
                    'custom_type': EmailSendFailure,
                    'expected_result': 'A valid email attachment path.',
                    'returned_result': attachment_path,
                    'suggested_resolution': 'Please verify you have set the correct path and try again.',
                }
                raise EmailSendFailure(FCustomException(exc_args))
            # Gets the mime type to determine the type of message being sent.
            mime_type, _ = mimetypes.guess_type(attachment_path)
            # Gets the MIME type and subtype.
            mime_type, mime_subtype = mime_type.split('/', 1)
            # Attaches the attachment to the message.
            with open(attachment_path, 'rb') as ap:
                message.add_attachment(ap.read(), maintype=mime_type, subtype=mime_subtype, filename=os.path.basename(attachment_path))
    except EmailSendFailure:
        raise
    except Exception as exc:
        exc_args = {
            'main_message': 'A general exception occurred while preparing the email message structure.',
            'original_exception': exc,
        }
        raise FGeneralError(exc_args)

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
            except Exception as exc:
                exc_args = {
                    'main_message': 'Failed to initialize SMTP connection using TLS.',
                    'custom_type': EmailSendFailure,
                    'original_exception': exc
                }
                raise EmailSendFailure(FCustomException(exc_args))
        else:
            logger.debug('Opening connection to SMTP server on port 25')
            smtp_Object = smtplib.SMTP(email_settings.get('smtp'), 25)
    except EmailSendFailure:
        raise
    except Exception as exc:
        if (
            "target machine actively refused it" in str(exc)
            or "connected party did not properly respond after a period of time" in str(exc)
            or "getaddrinfo failed" in str(exc)
        ):
            exc_args = {
                'main_message': 'Failed to send the email message. Connection to SMTP server failed.',
                'custom_type': EmailSendFailure,
                'suggested_resolution': 'Ensure the server address and TLS options are set correctly.',
                'original_exception': exc
            }
            raise EmailSendFailure(FCustomException(exc_args))
        elif 'Connection unexpectedly closed' in str(exc):
            exc_args = {
                'main_message': 'Failed to reach the SMTP server.',
                'custom_type': EmailSendFailure,
                'suggested_resolution': 'Ensure SMTP is reachable.',
                'original_exception': exc
            }
            raise EmailSendFailure(FCustomException(exc_args))
        else:
            exc_args = {
                'main_message': 'A general exception occurred while sending the email message.',
                'original_exception': exc,
            }
            raise FGeneralError(exc_args)

    # Sends email.
    try:
        # If authentication required, log in to mail server with credentials.
        if email_settings.get('authentication_required') is True:
            logger.debug('SMTP server authentication required, logging into server')
            smtp_Object.login(email_settings.get('username'), email_settings.get('password'))
            logger.debug('Sending the email')

        smtp_Object.sendmail(email_settings.get('from_email'), email_settings.get('to_email'), str(message).encode('utf-8').strip())
    except Exception as exc:
        if "SMTP AUTH extension not supported" in str(exc):
            exc_args = {
                'main_message': 'SMTP authentication is set to required but it is not supported by the server.',
                'custom_type': EmailSendFailure,
                'suggested_resolution': 'Try changing the INI [email] AuthenticationRequired value to False',
                'original_exception': exc
            }
        elif "Client host rejected: Access denied" in str(exc):
            exc_args = {
                'main_message': 'The SMTP server rejected the connection.',
                'custom_type': EmailSendFailure,
                'suggested_resolution': 'Authentication may be required, ensure the INI [email] AuthenticationRequired is set correctly.',
                'original_exception': exc
            }
        elif "authentication failed" in str(exc):
            exc_args = {
                'main_message': 'SMTP server authentication failed.',
                'custom_type': EmailSendFailure,
                'suggested_resolution': 'Ensure the INI [email] Username and Password are set correctly.',
                'original_exception': exc
            }
        elif " Authentication Required. Learn more at\n5.7.0  HTMLs://support.google.com" in str(exc):
            exc_args = {
                'main_message': 'Incorrect username and/or password or authentication_required is not enabled or Less Secure Apps needs enabled in your gmail settings.',
                'custom_type': EmailSendFailure,
                'original_exception': exc
            }
        elif "Authentication Required" in str(exc):
            exc_args = {
                'main_message': 'Incorrect username and/or password or the authentication_required setting is not enabled.',
                'custom_type': EmailSendFailure,
                'original_exception': exc
            }
        else:
            exc_args = {
                'main_message': 'A general exception occurred while sending the email.',
                'original_exception': exc,
            }
            raise FGeneralError(exc_args)

        raise EmailSendFailure(FCustomException(exc_args))

    finally:

        try:
            logger.debug(f'Terminating SMTP object')
            # Terminating SMTP object.
            smtp_Object.quit()
        except Exception as exc:
            if 'Failed to send message' in str(exc):
                exc_args = {
                    'main_message': 'Failed to send message. SMTP terminatation error occurred.',
                    'custom_type': EmailSendFailure,
                    'original_exception': exc
                }
                raise EmailSendFailure(FCustomException(exc_args))
            else:
                exc_args = {
                    'main_message': 'A general exception occurred while terminating the SMTP object.',
                    'original_exception': exc,
                }
                raise FGeneralError(exc_args)
