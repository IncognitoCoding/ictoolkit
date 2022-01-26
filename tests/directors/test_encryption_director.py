# Local Functions
from fchecker import type_check
from ictoolkit import (encrypt_info,
                       decrypt_info)

# Exceptions
from fexception import (FTypeError,
                        FValueError)


def test_encrypt_info():
    """
    This test currently tests encrypting a message or info.

    Raises:
        ValueError: A failure occurred in section 1.0 while testing the function 'encrypt_info'. The message is not in bytes format.
    """
    print('')
    print('-' * 65)
    print('-' * 65)
    print('Testing Function: encrypt_info')
    print('-' * 65)
    print('-' * 65)
    print('')

    # ############################################################
    # ####Section Test Part 1 (Successful Encryption Checking)####
    # ############################################################
    # ========Tests for a successful encryption.========
    message_encryption_password = 'ChangePassword1'
    message_encryption_random_salt = b'ChangeME'

    # Sets the sample message.
    sample_message = 'pytest sample'
    # Converts unencrypted message string into bytes.
    encrypted_message = encrypt_info(sample_message, message_encryption_password, message_encryption_random_salt)
    # Expected Sample Return: b'gAAAAABgW0PuVC2XK6QXtpD44P2pHnvAvwSXSV0Ulj8TBzJLHfrvQZF4eFkF22TdOynRx9eMPb7n_dRULQmZWcEz-g85nXK3yg=='
    try:
        type_check(encrypted_message, bytes)
    except FTypeError as exc:
        exc_args = {
            'main_message': 'A failure occurred in section 1.0 while testing the function \'encrypt_info\'. The message is not in bytes format.',
            'original_error': exc,
        }
        raise FTypeError(exc_args)

    # ========Tests for a successful encryption.========
    message_encryption_password = 'ChangePassword1'
    message_encryption_random_salt = str(b'ChangeME')

    # Sets the sample message.
    sample_message = 'pytest sample'
    # Converts unencrypted message string into bytes.
    encrypted_message = encrypt_info(sample_message, message_encryption_password, message_encryption_random_salt)
    # Expected Sample Return: b'gAAAAABgW0PuVC2XK6QXtpD44P2pHnvAvwSXSV0Ulj8TBzJLHfrvQZF4eFkF22TdOynRx9eMPb7n_dRULQmZWcEz-g85nXK3yg=='
    try:
        type_check(encrypted_message, bytes)
    except FTypeError as exc:
        exc_args = {
            'main_message': 'A failure occurred in section 1.1 while testing the function \'encrypt_info\'. The message is not in bytes format.',
            'original_error': exc,
        }
        raise FTypeError(exc_args)


def test_decrypt_info():
    """
    This test currently tests decryptting a message or info.

    Raises:
        ValueError: A failure occurred in section 1.0 while testing the function 'decrypt_info'. The message is not in bytes format.
        ValueError: A failure occurred in section 1.1 while testing the function 'decrypt_info'. The message returned the wrong result.
    """
    print('')
    print('-' * 65)
    print('-' * 65)
    print('Testing Function: decrypt_info')
    print('-' * 65)
    print('-' * 65)
    print('')

    # ############################################################
    # ####Section Test Part 1 (Successful Decryption Checking)####
    # ############################################################
    # ========Tests for a successful decryption.========
    message_encryption_password = 'ChangePassword1'
    message_encryption_random_salt = b'ChangeME'

    # Sets the sample message.
    encoded_message = b'gAAAAABgW0PuVC2XK6QXtpD44P2pHnvAvwSXSV0Ulj8TBzJLHfrvQZF4eFkF22TdOynRx9eMPb7n_dRULQmZWcEz-g85nXK3yg=='
    decrypted_message = decrypt_info(encoded_message, message_encryption_password, message_encryption_random_salt)
    try:
        type_check(decrypted_message, str)
    except FTypeError as exc:
        exc_args = {
            'main_message': 'A failure occurred in section 1.0 while testing the function \'decrypt_info\'. The message is not in bytes format.',
            'original_error': exc,
        }
        raise FTypeError(exc_args)

    # ========Tests for a successful decryption.========
    message_encryption_password = 'ChangePassword1'
    message_encryption_random_salt = b'ChangeME'

    # Sets the sample message.
    encoded_message = b'gAAAAABgW0PuVC2XK6QXtpD44P2pHnvAvwSXSV0Ulj8TBzJLHfrvQZF4eFkF22TdOynRx9eMPb7n_dRULQmZWcEz-g85nXK3yg=='
    decrypted_message = decrypt_info(encoded_message, message_encryption_password, message_encryption_random_salt)

    # Expected Return: b'pytest sample'
    if decrypted_message != 'pytest sample':
        exc_args = {
            'main_message': 'A failure occurred in section 1.1 while testing the function \'decrypt_info\'. The message returned the wrong result.',
            'expected_result': 'b\'pytest sample\'',
            'returned_result': decrypted_message,
        }
        raise FValueError(exc_args)

    # ========Tests for a successful decryption.========
    message_encryption_password = 'ChangePassword1'
    message_encryption_random_salt = str(b'ChangeME')

    # Sets the sample message.
    encoded_message = b'gAAAAABgW0PuVC2XK6QXtpD44P2pHnvAvwSXSV0Ulj8TBzJLHfrvQZF4eFkF22TdOynRx9eMPb7n_dRULQmZWcEz-g85nXK3yg=='
    decrypted_message = decrypt_info(encoded_message, message_encryption_password, message_encryption_random_salt)

    # Expected Return: b'pytest sample'
    if decrypted_message != 'pytest sample':
        exc_args = {
            'main_message': 'A failure occurred in section 1.1 while testing the function \'decrypt_info\'. The message returned the wrong result.',
            'expected_result': 'b\'pytest sample\'',
            'returned_result': decrypted_message,
        }
        raise FValueError(exc_args)
