import re


def num_string_converter(text: str):
    """Converts string numbers to numbers and returns normal text."""
    return int(text) if text.isdigit() else text


def str_int_key(text: str):
    """Converts string or string with numbers to a list to be used with as a sort key"""
    return [num_string_converter(c) for c in re.split("(\\d+)", text)]
