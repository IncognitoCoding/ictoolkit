#!interpreter

"""
This module is designed to assist with email-related actions. The module has the ability to send emails encrypted or unencrypted.
"""
# Built-in/Generic Imports
import sys
import logging
import traceback
import smtplib
from email.message import EmailMessage
from datetime import datetime
from email.mime.multipart import MIMEMultipart

# Libraries
import cryptography
from cryptography.fernet import Fernet
import base64
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

__author__ = 'IncognitoCoding'
__copyright__ = 'Copyright 2021, email_director'
__credits__ = ['IncognitoCoding', 'Monoloch']
__license__ = 'GPL'
__version__ = '1.3'
__maintainer__ = 'IncognitoCoding'
__status__ = 'Development'


def encrypt_info(email_settings, unencrypted_info):
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

    logger.debug(f'Begining to encrypt the info. unencrypted_info = {unencrypted_info}')
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
            algorithm=hashes.SHA256(), # An instance of HashAlgorithm
            length=32, # The desired length of the derived key in bytes. Maximum is (232 - 1)
            salt=salt, # Secure values [1] are 128-bits (16 bytes) or longer and randomly generated
            iterations=100000, # The number of iterations to perform of the hash function
            backend=default_backend() # An optional instance of PBKDF2HMACBackend
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
    except Exception as err: 
        error_message = (
            f'A failure occurred while encrypting the info.\n\n' +
            (('-' * 150) + '\n') + (('-' * 65) + 'Additional Information' + ('-' * 63) + '\n') + (('-' * 150) + '\n') +
            f'{err}\n\n'
            f'Originating error on line {traceback.extract_stack()[-1].lineno} in <{__name__}>\n' +
            (('-' * 150) + '\n') * 2 
        )   
        logger.error(error_message) 
        raise ValueError(error_message)
    else:
        logger.debug(f'Returning the encrypted info. encrypted_info = {encrypted_info}')
        # Returning the encrypted info.
        return encrypted_info


def decrypt_info(email_settings, encrypted_info):
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

    try:
        logger.debug(f'Begining to decrypt the info. uencrypted_info = {encrypted_info}')
        # Converting the pre-defined encryption password to bytes.
        password = email_settings.get('message_encryption_password').encode() 

        logger.debug('Setting random salt string that is (16 bytes) used to help protect from dictionary attacks')
        # Setting random salt string that is a (byte) used to help protect from dictionary attacks.
        # The salt string is randomly generated on the initial setup but static after the initial setup.
        salt = email_settings.get('message_encryption_random_salt')

        # Calling function to derive a cryptographic key from a password
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(), # An instance of HashAlgorithm
            length=32, # The desired length of the derived key in bytes. Maximum is (232 - 1)
            salt=salt, # Secure values [1] are 128-bits (16 bytes) or longer and randomly generated
            iterations=100000, # The number of iterations to perform of the hash function
            backend=default_backend() # An optional instance of PBKDF2HMACBackend
        )

        logger.debug('Returned from imported function (PBKDF2HMAC) to function (encrypt_info)')
        logger.debug('Encoding the string using the pre-defined encryption password and the cryptographic key into the binary form')
        # Encoding the string using the pre-defined encryption password and the cryptographic key into the binary form.
        key = base64.urlsafe_b64encode(kdf.derive(password))

        # Creating a symmetric authenticated cryptography (secret key)
        f = Fernet(key)
    except Exception as err: 
        error_message = (
            f'A failure occurred while decrypting the info.\n\n' +
            (('-' * 150) + '\n') + (('-' * 65) + 'Additional Information' + ('-' * 63) + '\n') + (('-' * 150) + '\n') +
            f'{err}\n\n'
            f'Originating error on line {traceback.extract_stack()[-1].lineno} in <{__name__}>\n' +
            (('-' * 150) + '\n') * 2 
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
                f'An invalid Key failure occurred while decrypting the info.\n\n' +
                (('-' * 150) + '\n') + (('-' * 65) + 'Additional Information' + ('-' * 63) + '\n') + (('-' * 150) + '\n') +
                f'{err}\n\n'
                f'Originating error on line {traceback.extract_stack()[-1].lineno} in <{__name__}>\n' +
                (('-' * 150) + '\n') * 2 
            )   
            logger.error(error_message) 
            raise ValueError(error_message)


def send_email(email_settings, subject, body_info):
    """
    This function offers many customized options when sending an email. Email can be sent with port 25 or using TLS. Email messages can be sent encrypted or unencrypted.

    Function parameters require the email settings to be sent in a dictionary format.

    The encrypt_info function is required when enabling message encryption. 

    To create a random "salt" use this command "print("urandom16 Key:", os.urandom(16))"

    Args:
        email_settings (dict): email settings constructed within a dictionary\n
        - email_setting Keys/Values:\n
            - smtp (str): SMTP server.
            - authentication_required (bool): Enables authentication.
            - use_tls (str): Enables TLS.
            - username (str): Username for email authentication.
            - password (str): Password for email authentication.
            - from_email (str): From email address.
            - to_email (str): To email address.
            - send_message_encrypted (bool): If message should be encrypted.
            - message_encryption_password (str): Encryption password if encryption is enabled. Set to None if no encryption.
            - message_encryption_random_salt (bytes): Random salt in bytes format. Set to None if no encryption.\n
        subject (str): email subject information
        body_info (str): email body information

    Raises:
        ValueError: Failed to send the email message. No email encryption option was selected
        ValueError: Failed to initialize SMTP connection using TLS.
        ValueError: Failed to send the email message. Connection to SMTP server failed.
        ValueError: Failed to send the email message. SMTP send error occurred.
        ValueError: Failed to send message. SMTP terminatation error occurred.
    """
    logger = logging.getLogger(__name__)

    logger.debug(f'Begining to send an email message. body_info = {body_info}')

    # Gets encryption option.
    send_message_encrypted = email_settings.get('send_message_encrypted')
    # Sets email encryption to false if no value is sent.
    if send_message_encrypted == None:
        send_message_encrypted = False

    # Checking if the user wants to send encrypted or unencrypted.
    # Decrypting has to be done with f.decrypt(<encrypted message>) using the salt and password used to encrypt the message.
    if send_message_encrypted == True:
        logger.debug('Preparing to send the issue message encrypted')
        logger.debug('Converting unencrypted message string into bytes')
        # Converts unencrypted message string into bytes.
        encoded_message = body_info.encode()
        # Calls function to sends unencrypted message for encryption.
        # Return Example: <encrypted message>
        encrypted_info = encrypt_info(email_settings, encoded_message)

        logger.debug('Preparing HTML body message')
        # Preparing HTML body message.
        # Note: the encrypted message will be in bytes, containing characters that will be strip when sending the message. Single quotes need manually added to the message.
        html = """\
        <html>
        <head></head>
        <body>
            <p><br>
            """ + subject + """ was sent at """ + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + """.<br />
            <br />
            Message code below:<br />
            <br />
            """ + f'{encrypted_info}' """
            
            </p>
        </body>
        </html>
        """
    elif send_message_encrypted == False:
        logger.debug('Preparing to send the issue message unencrypted')
        logger.debug('Preparing HTML body message')
        # Preparing HTML body message.
        # Sends message unencrypted.
        html = """\
        <html>
        <head></head>
        <body>
            <p><br>
            """ + subject + """ was sent at """ + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + """.<br />
            <br />
            Message Below:<br />
            <br />
            """ + body_info + """
            
            </p>
        </body>
        </html>
        """
    else:
        error_message = (
            'Failed to send the email message. No email encryption option was selected.\n' +
            (('-' * 150) + '\n') + (('-' * 65) + 'Additional Information' + ('-' * 63) + '\n') + (('-' * 150) + '\n') +
            'Expected Result:\n'
            '  - key value for send_message_encrypted = True or False\n\n'
            'Returned Result:\n'
            f'  - key value for send_message_encrypted = {send_message_encrypted}\n\n'
            f'Originating error on line {traceback.extract_stack()[-1].lineno} in <{__name__}>\n' +
            (('-' * 150) + '\n') * 2 
        )
        logger.error(error_message)
        raise ValueError(error_message)

    logger.debug('Preparing email message structure')
    # Preparing email message structure.
    message = EmailMessage()
    message['Subject'] = subject
    message['From'] = email_settings.get('from_email')
    message['To'] = [email_settings.get('to_email')]
    # Sets header.
    message.add_header('Content-Type','text/html')

    logger.debug('Setting payload to HTML')
    # Setting payload to HTML.
    message.set_payload(html) 

    try:
        logger.debug('Setting up SMTP object')
        # Setting up SMTP object.
        if email_settings.get('use_tls') == True:
            logger.debug('Opening connection to SMTP server on port 587 for TLS')
            smtp_Object = smtplib.SMTP(email_settings.get('smtp'), 587)

            try:
                smtp_Object.ehlo()
                logger.debug('Sending StartTLS message')
                smtp_Object.starttls()
            except Exception as err:
                error_message = (
                    f'Failed to initialize SMTP connection using TLS.\n\n' +
                    (('-' * 150) + '\n') + (('-' * 65) + 'Additional Information' + ('-' * 63) + '\n') + (('-' * 150) + '\n') +
                    f'{err}\n\n'
                    f'Originating error on line {traceback.extract_stack()[-1].lineno} in <{__name__}>\n' +
                    (('-' * 150) + '\n') * 2 
                )   
                logger.error(error_message) 
                raise ValueError(error_message)
        else:
            logger.debug('Opening connection to SMTP server on port 25')
            smtp_Object = smtplib.SMTP(email_settings.get('smtp'), 25)
    except Exception as err:
        if (
            "target machine actively refused it" in str(err) or
            "connected party did not properly respond after a period of time" in str(err)
        ):
            error_message = (
                'Failed to send the email message. Connection to SMTP server failed.\n\n' +
                (('-' * 150) + '\n') + (('-' * 65) + 'Additional Information' + ('-' * 63) + '\n') + (('-' * 150) + '\n') +
                'Suggested Resolution:\n'
                '  - Ensure the server address and TLS options are set correctly.\n\n'
                f'Originating error on line {traceback.extract_stack()[-1].lineno} in <{__name__}>\n' +
                (('-' * 150) + '\n') * 2 
            )   
            logger.error(error_message) 
            raise ValueError(error_message)
        
    # Sends email.
    try:
        #If authentication required, log in to mail server with credentials.
        if email_settings.get('authentication_required') == True:
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
        elif " Authentication Required. Learn more at\n5.7.0  https://support.google.com" in str(err):
            err = "Incorrect username and/or password or authentication_required is not enabled or Less Secure Apps needs enabled in your gmail settings"
        elif "Authentication Required" in str(err):
            err = "Incorrect username and/or password or the authentication_required setting is not enabled"
        error_message = (
            f'Failed to send the email message. SMTP send error occurred.\n\n' +
            (('-' * 150) + '\n') + (('-' * 65) + 'Additional Information' + ('-' * 63) + '\n') + (('-' * 150) + '\n') +
            f'{err}\n\n'
            f'Originating error on line {traceback.extract_stack()[-1].lineno} in <{__name__}>\n' +
            (('-' * 150) + '\n') * 2 
        )   
        logger.error(error_message) 
        raise ValueError(error_message)

    finally:

        try:
            logger.debug(f'Terminating SMTP object')
            # Terminating SMTP object.
            smtp_Object.quit()
        except Exception as err: 
            error_message = (
                f'Failed to send message. SMTP terminatation error occurred.\n\n' +
                (('-' * 150) + '\n') + (('-' * 65) + 'Additional Information' + ('-' * 63) + '\n') + (('-' * 150) + '\n') +
                f'{err}\n\n'
                f'Originating error on line {traceback.extract_stack()[-1].lineno} in <{__name__}>\n' +
                (('-' * 150) + '\n') * 2 
            )   
            logger.error(error_message) 
            raise ValueError(error_message)