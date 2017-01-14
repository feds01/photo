__author__ = "Alexander Fedotov <alexander.fedotov.uk@gmail.com>"
__company__ = "(C) Wasabi & Co. All rights reserved."

"""
Module name: exceptions.py
Usage:
Description -

"""


class Fatal(Exception):
    def __init__(self, message, stop=False, *other):
        print('fatal: %s' % message)
        self.line = 0
        for information in other:
            print([hex(self.line) + ':'][0], information)
            self.line += 1
        if stop:
            exit()


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
    def __init__(self, directory, reason):
        if reason == "permissions":
            print("permissions: could not scan %s directory - passing." % directory)

        elif reason == "leaf":
            print('error: given directory(%s) is a leaf' % directory)


class ByteOverflow(Exception):
    def __init__(self):
        print("while converting bytes to units, the byte count overflowed 1024**5.")
        pass


def config_warning(message):
    print('config: %s' % message)


def node_error(silent, directory):
    if silent:
        pass
    else:
        IndexingError(directory, "leaf")


def yml_error(error):
    Fatal('While loading Config file something went wrong.\nHere is trace:\n', error)
    exit()