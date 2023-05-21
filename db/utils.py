"""
Module with utilities for db folder.
Includes:
    - Costume Exception classes
"""


class ConfigFormatError(Exception):
    """
    Class representing an error in the format of the config file for the database.
    """

    def __init__(self, section, filename):
        self.section = section
        self.filename = filename

    def __str__(self) -> str:
        return f"Section {self.section} not found in the {self.filename} file"


class ConfigEmptyError(Exception):
    """
    Class representing an error in the format of the config file for the database.
    """

    def __str__(self) -> str:
        return "This Config has no parameters"
