import sys
import traceback

__author__ = "Alexander Fedotov <alexander.fedotov.uk@gmail.com>"
__company__ = "(C) Wasabi & Co. All rights reserved."

debug = True  # temporary value


def exception_handler(e, value, tb):
    if e == KeyboardInterrupt:
        pass

    if debug:
        print(''.join(traceback.format_exception(type, value, tb)))


sys.excepthook = exception_handler


class Fatal(Exception):
    def __init__(self, message, *other):
        self.message = message

        print('fatal: %s' % self.message)

        self.line = 0
        for information in other:
            print([hex(self.line) + ':'][0], information)
            self.line += 1

    def get_message(self):
        return self.message

    def stop(self):
        exit()


class IndexingError(Exception):
    def __init__(self, directory, reason):
        if reason == "permissions":
            print("permissions: could not scan %s directory - passing." % directory)

        elif reason == "leaf":
            print('error: given directory(%s) is a leaf' % directory)


def config_warning(message):
    print('config: %s' % message)


def yml_error(error):
    Fatal('config file is unreadable.', 'Here is trace:\n\n%s' % error).stop()


if debug:
    config_warning("debug value is enabled!")