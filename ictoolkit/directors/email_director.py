#!interpreter

"""
This module is designed to assist with email-related actions. The module has the ability to send emails encrypted or unencrypted.
"""
# Built-in/Generic Imports
import sys
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
__copyright__ = 'Copyright 2021, file_director'
__credits__ = ['IncognitoCoding', 'Monoloch']
__license__ = 'GPL'
__version__ = '1.1'
__maintainer__ = 'IncognitoCoding'
__status__ = 'Development'


def encrypt_info(email_settings, unencrypted_info, logger=None):
    """
    This function encrypts any message that is sent. 

    Args:
    email_settings (dict): email settings constructed within a dictionary
        {message_encryption_password (str): message encryption password,
         message_encryption_random_salt (bytes): message encryption random salt}
    unencrypted_info (bytes): unencrypted info in bytes format
    logger (logger, optional): logger. Defaults to None.

    Raises:
        ValueError: A failure occurred while encrypting the info

    Returns:
        bytes: encrypted info
    """
    # Checks if logger exists.
    if logger != None:
        logger.debug(f'Begining to encrypt the info. unencrypted_info = {unencrypted_info}')

    try:

        # Checks if logger exists.
        if logger != None:
            logger.debug('Converting the pre-defined encryption password to bytes')

        # Converting the pre-defined encryption password to bytes.
        password = email_settings.get('message_encryption_password').encode()  

        # Checks if logger exists.
        if logger != None:
            logger.debug('Setting random salt string that is (16 bytes) used to help protect from dictionary attacks')

        # Setting random salt string that is a (byte) used to help protect from dictionary attacks.
        # The salt string is randomly generated on the initial setup but static after the initial setup.
        salt = email_settings.get('message_encryption_random_salt')

        # Checks if logger exists.
        if logger != None:
            logger.debug('Deriving a cryptographic key from a password')

        # Calling function to derive a cryptographic key from a password.
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(), # An instance of HashAlgorithm
            length=32, # The desired length of the derived key in bytes. Maximum is (232 - 1)
            salt=salt, # Secure values [1] are 128-bits (16 bytes) or longer and randomly generated
            iterations=100000, # The number of iterations to perform of the hash function
            backend=default_backend() # An optional instance of PBKDF2HMACBackend
        )

        # Checks if logger exists.
        if logger != None:
            logger.debug('Returned from imported function (PBKDF2HMAC) to function (encrypt_info)')
            logger.debug('Encoding the string using the pre-defined encryption password and the cryptographic key into the binary form')

        # Encoding the string using the pre-defined encryption password and the cryptographic key into the binary form.
        key = base64.urlsafe_b64encode(kdf.derive(password))

        # Checks if logger exists.
        if logger != None:
            logger.debug('Creating a symmetric authenticated cryptography (secret key)')

        # Creating a symmetric authenticated cryptography (secret key).
        f = Fernet(key)

        # Checks if logger exists.
        if logger != None:
            logger.debug('Encrypting the info using the secret key to create a Fernet token')

        # Encrypting the info using the secret key to create a Fernet token.
        encrypted_info = f.encrypt(unencrypted_info)

    except Exception as err: 
        raise ValueError(f'A failure occurred while encrypting the info, {err}, Originating error on line {traceback.extract_stack()[-1].lineno} in <{__name__}>')

    else:
        # Checks if logger exists.
        if logger != None:
            logger.debug(f'Returning the encrypted info. encrypted_info = {encrypted_info}')

        # Returning the encrypted info.
        return encrypted_info


def decrypt_info(email_settings, encrypted_info, logger=None):
    """
    This function decrypts any message that is sent. 

    Args:
        email_settings (dict): email settings constructed within a dictionary
            {message_encryption_password (str): message encryption password,
             message_encryption_random_salt (bytes): message encryption random salt}
        encrypted_info ([type]): encrypted message in bytes format. Re-encoding may be required.
        logger (logger, optional): logger. Defaults to None.

    Raises:
        ValueError: A failure occurred while decrypting the info
        ValueError: Invalid Key

    Returns:
        bytes: decrypted info
    """

    try:

        # Checks if logger exists.
        if logger != None:
            logger.debug(f'Begining to decrypt the info. uencrypted_info = {encrypted_info}')
            
        # Converting the pre-defined encryption password to bytes.
        password = email_settings.get('message_encryption_password').encode() 

        # Checks if logger exists.
        if logger != None:
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

        # Checks if logger exists.
        if logger != None:
            logger.debug('Returned from imported function (PBKDF2HMAC) to function (encrypt_info)')
            logger.debug('Encoding the string using the pre-defined encryption password and the cryptographic key into the binary form')

        # Encoding the string using the pre-defined encryption password and the cryptographic key into the binary form.
        key = base64.urlsafe_b64encode(kdf.derive(password))

        # Creating a symmetric authenticated cryptography (secret key)
        f = Fernet(key)

    except Exception as err: 
        raise ValueError(f'A failure occurred while decrypting the info, {err}, Originating error on line {traceback.extract_stack()[-1].lineno} in <{__name__}>')

    else:

        try:

            # Checks if logger exists.
            if logger != None:
                logger.debug('Decrypting the info using the secret key to create a Fernet token')

            # Decrypting the info using the secret key to create a Fernet token.
            decrypted_info = f.decrypt(encrypted_info)

            # Checks if logger exists.
            if logger != None:
                logger.debug(f'Returning the decrypted info. decrypted_info = {decrypted_info}')
                
            # Returning the decrypted info
            return decrypted_info

        except InvalidToken as e:
            raise ValueError(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}|Error|Invalid Key. The info did not unencrypt. {e}, Error on line {traceback.extract_stack()[-1].lineno} in <{__name__}>')


def send_email(email_settings, subject, body_info, logger=None):
    """
    This function offers many customized options when sending an email. Email can be sent with port 25 or using TLS. Email messages can be sent encrypted or unencrypted.

    Function parameters require the email settings to be sent in a dictionary format.

    The encrypt_info function is required when enabling message encryption. 

    To create a random "salt" use this command "print("urandom16 Key:", os.urandom(16))"

    Args:
        email_settings (dict): email settings constructed within a dictionary
            {smtp (str): SMTP server,
             authentication_required (bool): enable authentication,
             use_tls (str): enable tls, 
             username (str): username, 
             password (str): password,
             from_email (str): from email address,
             to_email (str): to email address
             send_message_encrypted (bool): enable message encryption,
             message_encryption_password (str): message encryption password,
             message_encryption_random_salt (bytes): message encryption random salt}
        subject (str): email subject information
        body_info (str): email body information
        logger (logger, optional): logger. Defaults to None.

    Raises:
        ValueError: Failed to send message. No email encryption option is selected in the user settings section
        Exception: Failed to initialize SMTP connection using TLS
        ValueError: Failed to send message
        ValueError: Failed to send message. SMTP send error occurred
        ValueError: Failed to send message. SMTP terminatation error occurred
    """
    # Checks if logger exists.
    if logger != None:
        logger.debug(f'Begining to send an email message. body_info = {body_info}')

    # Checking if the user wants to send encrypted or unencrypted.
    # Decrypting has to be done with f.decrypt(<encrypted message>) using the salt and password used to encrypt the message.
    if email_settings.get('send_message_encrypted') == True:
        
        # Checks if logger exists.
        if logger != None:
            logger.debug('Preparing to send the issue message encrypted')
            logger.debug('Converting unencrypted message string into bytes')

        # Converts unencrypted message string into bytes.
        encoded_message = body_info.encode()

        # Calls function to sends unencrypted message for encryption.
        # Calling Example: encrypt_info(<dictionary: including encryption password and random salt>, <encoded message>, <configured logger>)
        # Return Example: <encrypted message>
        encrypted_info = encrypt_info(email_settings, encoded_message, logger)

        # Checks if logger exists.
        if logger != None:
            logger.debug('Preparing HTML body message')

        # Preparing HTML body message.
        # Note: the encrypted message will be in bytes, containing characters that will be strip when sending the message. Single quotes need manually added to the message.
        html = """\
        <html>
        <head></head>
        <body>
            <p><br>
            """ + subject + """ at """ + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + """.<br />
            <br />
            Message code below:<br />
            <br />
            """ + f'{encrypted_info}' """
            
            </p>
        </body>
        </html>
        """

    elif email_settings.get('send_message_encrypted') == False:
        
        # Checks if logger exists.
        if logger != None:
            logger.debug('Preparing to send the issue message unencrypted')
            logger.debug('Preparing HTML body message')

        # Preparing HTML body message.
        # Sends message unencrypted.
        html = """\
        <html>
        <head></head>
        <body>
            <p><br>
            """ + subject + """ at """ + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + """.<br />
            <br />
            Message Below:<br />
            <br />
            """ + body_info + """
            
            </p>
        </body>
        </html>
        """
    else:
        raise ValueError(f'Failed to send message. No email encryption option is selected in the user settings section, Originating error on line {traceback.extract_stack()[-1].lineno} in <{__name__}>')

    # Checks if logger exists.
    if logger != None:
        logger.debug('Preparing email message structure')

    # Preparing email message structure.
    message = EmailMessage()
    message['Subject'] = subject
    message['From'] = email_settings.get('from_email')
    message['To'] = [email_settings.get('to_email')]
    # Sets header.
    message.add_header('Content-Type','text/html')

    # Checks if logger exists.
    if logger != None:
        logger.debug('Setting payload to HTML')

    # Setting payload to HTML.
    message.set_payload(html) 

    try:

        # Checks if logger exists.
        if logger != None:
            logger.debug('Setting up SMTP object')

        # Setting up SMTP object.
        if email_settings.get('use_tls') == True:

            # Checks if logger exists.
            if logger != None:
                logger.debug('Opening connection to SMTP server on port 587 for TLS')

            smtp_Object = smtplib.SMTP(email_settings.get('smtp'), 587)

            try:

                smtp_Object.ehlo()

                # Checks if logger exists.
                if logger != None:
                    logger.debug('Sending StartTLS message')

                smtp_Object.starttls()
            except Exception as err:
                raise Exception (f'Failed to initialize SMTP connection using TLS.  {err} Originating error on line {traceback.extract_stack()[-1].lineno} in <{__name__}>')

        else:

            # Checks if logger exists.
            if logger != None:
                logger.debug('Opening connection to SMTP server on port 25')

            smtp_Object = smtplib.SMTP(email_settings.get('smtp'), 25)

    except Exception as err:
        if "target machine actively refused it" in str(err) or "connected party did not properly respond after a period of time" in str(err):
            err = "Connection to SMTP server failed. Ensure the server address and TLS options are set correctly"
        raise ValueError(f'Failed to send message. {err}, Originating error on line {traceback.extract_stack()[-1].lineno} in <{__name__}>')
        
    # Sends email.
    try:

        #If authentication required, log in to mail server with credentials.
        if email_settings.get('authentication_required') == True:

            # Checks if logger exists.
            if logger != None:
                logger.debug('SMTP server authentication required, logging into server')

            smtp_Object.login(email_settings.get('username'), email_settings.get('password'))
        
        # Checks if logger exists.
        if logger != None:
            logger.debug('Sending the email')

        smtp_Object.sendmail(email_settings.get('from_email'), email_settings.get('to_email'), message.as_string())

    except Exception as err:
        if "SMTP AUTH extension not supported" in str(err):
            err = "SMTP authentication is set to required but it is not supported by the server. Try changing the INI [email] AuthenticationRequired value to False"
        elif "Client host rejected: Access denied" in str(err):
            err = "The SMTP server rejected the connection.  Authentication may be required, ensure the INI [email] AuthenticationRequired is set correctly"
        elif "authentication failed" in str(err):
            err = "SMTP server authentication failed. Ensure the INI [email] Username and Password are set correctly"
        raise ValueError(f'Failed to send message. SMTP send error occurred. {err}, Originating error on line {traceback.extract_stack()[-1].lineno} in <{__name__}>')

    finally:

        try:

            # Checks if logger exists.
            if logger != None:
                logger.debug(f'Terminating SMTP object')
                
            # Terminating SMTP object.
            smtp_Object.quit()

        except Exception as err: 
            raise ValueError(f'Failed to send message. SMTP terminatation error occurred. {err}, Originating error on line {traceback.extract_stack()[-1].lineno} in <{__name__}>')
            