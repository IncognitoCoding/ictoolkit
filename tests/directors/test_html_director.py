# Local Functions
from ictoolkit import HTMLConverter

# Exceptions
from fexception import FTypeError, FValueError


def test_feed():
    """
    This test currently tests encrypting a message or info.

    Raises:
        ValueError: A failure occurred in section 1.0 while testing the function 'test_feed'. The message is not in bytes format.
        ValueError: A failure occurred in section 1.1 while testing the function 'test_feed'. The message returned the wrong result.
        ValueError: A failure occurred in section 2.0 while testing the function 'test_feed'. The test did not fail when not sending a incorrect convert_option value.
        ValueError: A failure occurred in section 2.1 while testing the function 'test_feed'. The test did not fail when not sending a incorrect data value.
    """
    print("")
    print("-" * 65)
    print("-" * 65)
    print("Testing Function: feed")
    print("-" * 65)
    print("-" * 65)
    print("")

    # ############################################################
    # ######Section Test Part 1 (Successful Value Checking)#######
    # ############################################################
    # ========Tests for a successful output return.========
    parser = HTMLConverter()

    data = """
        <ol>
        <li>Coffee</li>
        <li>Tea</li>
        <li>Milk</li>
        </ol>

        <ul>
        <li>Coffee</li>
        <li>Tea</li>
        <li>Milk</li>
        </ul>
    """
    parser.feed(data, "text")
    converted_html = parser.output
    if "- Coffee" not in converted_html:
        exc_args = {
            "main_message": "A failure occurred in section 1.1 while testing the function 'test_feed'. The message returned the wrong result.",
            "expected_result": "- Coffee",
            "returned_result": converted_html,
        }
        raise FValueError(exc_args)

    # ############################################################
    # ######Section Test Part 2 (Error/Catch Value Checking)######
    # ############################################################
    # ========Tests for incorrect value checks.========
    try:
        parser = HTMLConverter()

        parser.feed(data, "image")
    except FValueError as error:
        if "The HTML output could not be converted because the conversion option is not valid" not in str(error):
            exc_args = {
                "main_message": "A failure occurred in section 2.0 while testing the function 'test_feed'. The test did not fail when not sending a incorrect convert_option value.",
                "expected_result": "A value error",
                "error": error,
            }
            raise FValueError(exc_args)

    # ========Tests for incorrect value checks.========
    try:
        parser = HTMLConverter()

        parser.feed(1, "text")
    except FTypeError as error:
        if """The object value '1' is not an instance of the required class(es) or subclass(es).""" not in str(error):
            exc_args = {
                "main_message": "A failure occurred in section 2.1 while testing the function 'test_feed'. The test did not fail when not sending a incorrect data value.",
                "expected_result": "A value error",
                "error": error,
            }
            raise FValueError(exc_args)
