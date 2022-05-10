# Built-in/Generic Imports
import traceback
import os
from datetime import datetime
from os.path import dirname as up

# Local Functions
from ictoolkit import send_email

# Exceptions
from fexception import FValueError


def test_send_email():
    """
    This tests sending an email with port 25. TLS is not tested as part of the pytest.

    Raises:
        ValueError: A failure occurred in section 1.0 while testing the function 'send_email'. The email did not send.
        ValueError: A failure occurred in section 1.1 while testing the function 'send_email'. The email did not send.
        ValueError: A failure occurred in section 2.0 while testing the function 'send_email'. The test did not fail when sending a non-dictionary parameter.
    """
    print("")
    print("-" * 65)
    print("-" * 65)
    print("Testing Function: send_email")
    print("-" * 65)
    print("-" * 65)
    print("")

    # ############################################################
    # ######Section Test Part 1 (Successful Send Checking)#######
    # ############################################################
    # ========Tests for a successful send out port 25 for non-HTTP.========
    email_settings = {
        "smtp": "mailrise.thoroughinnovations.com",
        "authentication_required": False,
        "use_tls": False,
        "username": "SMTP_username",
        "password": "SMTP_password",
        "from_email": "ictoolkit_pytest@thoroughinnovations.com",
        "to_email": "gmail@thoroughinnovations.com",
        "send_email_template": False,
        "message_encryption_password": "ChangePassword1",
        "message_encryption_random_salt": b"ChangeME",
    }

    subject = "Pytest Email from ictoolkit"
    body = "Message code below: @START-ENCRYPT@This is my original string@END-ENCRYPT@"
    template_args = ""

    try:

        # No return value. Throws an exception if the email send fails.
        send_email(email_settings, subject, body, template_args)
    except Exception as error:
        error_message = (
            "A failure occurred in section 1.0 while testing the function 'send_email'. The email did not send.\n"
            + (("-" * 150) + "\n")
            + (("-" * 65) + "Additional Information" + ("-" * 63) + "\n")
            + (("-" * 150) + "\n")
            + f"{error}\n\n"
            f"Originating error on line {traceback.extract_stack()[-1].lineno} in <{__name__}>\n"
            + (("-" * 150) + "\n") * 2
        )
        raise ValueError(error_message)

    # ========Tests for a successful send out port 25 for HTTP.========
    # Gets the parrent root directory.
    preset_root_directory = os.path.dirname(os.path.realpath(__file__))
    # Gets directory 3 levels up.
    two_levels_up_path = up(up(preset_root_directory))
    # Checks that the main root program directory has the correct save folders created.
    # Sets the template directory path.
    save_template_path = os.path.abspath(f"{two_levels_up_path}/tests/directors/email_templates")

    email_settings = {
        "smtp": "mailrise.thoroughinnovations.com",
        "authentication_required": False,
        "use_tls": False,
        "username": "SMTP_username",
        "password": "SMTP_password",
        "from_email": "ictoolkit_pytest@thoroughinnovations.com",
        "to_email": "gmail@thoroughinnovations.com",
        "send_email_template": True,
        "email_template_name": "pytest_sample.html",
        "email_template_path": save_template_path,
        "message_encryption_password": "ChangePassword1",
        "message_encryption_random_salt": b"ChangeME",
    }

    subject = "Pytest Email from ictoolkit"
    body = None
    template_args = {
        "name": "Pytest",
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "url": "http://1.1.1.1:5000/",
    }

    try:
        # No return value. Throws an exception if the email send fails.
        send_email(email_settings, subject, body, template_args)
    except Exception as error:
        error_message = (
            "A failure occurred in section 1.1 while testing the function 'send_email'. The email did not send.\n"
            + (("-" * 150) + "\n")
            + (("-" * 65) + "Additional Information" + ("-" * 63) + "\n")
            + (("-" * 150) + "\n")
            + f"{error}\n\n"
            f"Originating error on line {traceback.extract_stack()[-1].lineno} in <{__name__}>\n"
            + (("-" * 150) + "\n") * 2
        )
        raise ValueError(error_message)

    # ############################################################
    # ######Section Test Part 2 (Error/Catch Value Checking)######
    # ############################################################
    # ========Tests for an incorrectly sent email settings format.========

    try:
        send_email("INCORRECT or EMPTY DATA TEST", subject, body, template_args)
    except Exception as error:
        if (
            """The object value 'INCORRECT or EMPTY DATA TEST' is not an instance of the required class(es) or subclass(es)."""
            not in str(error)
        ):
            error_message = (
                "A failure occurred in section 2.0 while testing the function 'send_email'. The test did not fail when sending a non-dictionary parameter.\n"
                + (("-" * 150) + "\n")
                + (("-" * 65) + "Additional Information" + ("-" * 63) + "\n")
                + (("-" * 150) + "\n\n")
                + "Expected Result:\n"
                "  - non-dictionary values\n\n"
                "Returned Result:\n"
                f"  - {error}\n\n"
                f"Originating error on line {traceback.extract_stack()[-1].lineno} in <{__name__}>\n"
                + (("-" * 150) + "\n") * 2
            )
            raise ValueError(error_message)
