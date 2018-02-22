import sys
import traceback
from src.utilities.manipulation import query_user

__author__ = "Alexander Fedotov <alexander.fedotov.uk@gmail.com>"
__company__ = "(C) Wasabi & Co. All rights reserved."

debug = True  # temporary value


def exception_handler(type, value, tb):
    if type == KeyboardInterrupt:
        pass

    if debug:
        print(''.join(traceback.format_exception(type, value, tb)))

sys.excepthook = exception_handler


class simple_error(Exception):
    def __init__(self, message, try_recovery, info):
        print('error: %s' % message)
        self.info = info

        if try_recovery:
            self.recovery()
        else:
            pass

    def recovery(self):
        e_description = self.info.get('e_type').split('.')

        if e_description[0] == 'file':
            print('file operation on object - %s' % self.info.get('object'))

        elif e_description[0] == 'process':
            if e_description[1] == 'kb_error':
                return bool(query_user('Perform a re-scan? [y/n]', ('y', 'n')) == 'y')


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


def config_warning(message):
    print('config: %s' % message)

def yml_error(error):
    Fatal('config file is unreadable.', 'Here is trace:\n\n%s' % error).stop()