__author__ = "Alexander Fedotov <alexander.fedotov.uk@gmail.com>"
__company__ = "(C) Wasabi & Co. All rights reserved."

"""
Module name: exceptions.py
Usage:
Description -

"""


class Fatal(Exception):
    def __init__(self, message):
        print(message)
        pass


class BlacklistEntryError(Exception):
    def __init__(self, err):
        self.error = err
        self.print_message()
        pass

    def print_message(self):
        if self.error == "present":
            print("blacklist: given directory is present, cannot add entry.")
        if self.error == "not-present":
            print("blacklist: given directory is not present, cannot remove entry.")


class IndexingError(Exception):
    def __init__(self, directory):
        print("permissions: could not list directory -", directory)
        pass


class ByteOverflow(Exception):
    def __init__(self):
        print("while converting bytes to units, the byte count overflowed 1024**5.")
        pass

"""
class Config(BaseException):
    def __init__(self, error_code, old_definition):
        self.error_code = error_code
        self.old_definition = old_definition
        self.correct_value = "\\"

    def IncorrectVariableValue(self):
            print("Config was not compiled correctly.")
            print("Error Code: " + self.error_code)
            print("variable definition " ,self.old_definition, " -> ", self.correct_value)
"""