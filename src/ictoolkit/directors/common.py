class InputFailure(Exception):
    """Exception raised for an input exception message."""

    __module__ = "builtins"
    pass


class RequirementFailure(Exception):
    """Exception raised for a requirement exception message."""

    __module__ = "builtins"
    pass


class CallerOverrideFailure(Exception):
    """Exception raised for a caller override exception message."""

    __module__ = "builtins"
    pass
