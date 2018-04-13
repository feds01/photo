import pprint
import sys
import traceback

__author__ = "Alexander Fedotov <alexander.fedotov.uk@gmail.com>"
__company__ = "(C) Wasabi & Co. All rights reserved."


def exception_handler(e, value, tb):
    if e == KeyboardInterrupt:
        pass

    if debug:
        print(''.join(traceback.format_exception(type, value, tb)))


debug = True  # temporary value, only available on main thread
sys.excepthook = exception_handler


class Fatal(Exception):
    def __init__(self, message, *other):
        self.message = message

        print('fatal: %s' % self.message)

        for information in other:
            if type(information) == dict:
                self.pretty_print(information)
            else:
                print(information)

    def get_message(self):
        return self.message

    @staticmethod
    def pretty_print(dictionary):
        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(dictionary)

    @staticmethod
    def stop():
        exit()


class IndexingError(Exception):
    def __init__(self, directory, reason):
        if reason == "permissions":
            print("permissions: could not scan %s directory - passing." % directory)

        elif reason == "leaf":
            print('error: given directory(%s) is a leaf' % directory)


def do_warning(prefix, message, *other):
    print(f"{prefix}: {message}")

    for item in other:
        print(item)


if debug:
    do_warning('src.core.exceptions', "debug value is enabled!")
