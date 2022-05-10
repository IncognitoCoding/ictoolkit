"""
This script is used to test the subprocess_director module using pytest.
"""
# Local Functions
from ictoolkit import start_subprocess

# Exceptions
from fexception import FValueError


def test_start_subprocess():
    """
    Tests starting a subprocess.

    Raises:
        ValueError: A failure occurred in section 1.0 while testing the function 'start_subprocess'. The subprocess did not return any output.
    """
    print("")
    print("-" * 65)
    print("-" * 65)
    print("Testing Function: start_subprocess")
    print("-" * 65)
    print("-" * 65)
    print("")

    # ############################################################
    # ######Section Test Part 1 (Successful Value Checking)#######
    # ############################################################
    # ========Tests for a successful output return.========
    # Sample sub processing args
    processing_args = ["ipconfig", "/all"]

    output = start_subprocess(processing_args)

    # Expected Return: ['', 'Windows IP Configuration', '', '   Host Name . . . . . . . . . . . . : Test-PC-1', '   Primary Dns Suffix  . . . . . . . : test.site.org', ' ...............---> continued']
    if not output.stdout:
        exc_args = {
            "main_message": "A failure occurred in section 1.0 while testing the function 'start_subprocess'. The subprocess did not return any output.",
        }
        raise FValueError(exc_args)
