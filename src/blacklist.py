from src.core.fileio import *
from src.utilities.infrequents import is_child
from src.utilities.arrays import organise_array

__author__ = "Alexander Fedotov <alexander.fedotov.uk@gmail.com>"
__company__ = "(C) Wasabi & Co. All rights reserved."


class _Blacklist:
    def __init__(self):
        self.data = {}
        self.file = File(file=Config.join('application_root', 'blacklist.location'))

        self.read()

    def read(self):
        self.data = self.file.read_json()

    def get_blacklist(self):
        return self.data["entries"]

    def is_entry(self, entries, inverted=False):
        entries = organise_array([entries])
        verify_list = list(filter(lambda e: e in self.data['entries'], entries))

        if not inverted:
            # entries which came out clean
            return list(filter(lambda e: e not in verify_list, entries))
        else:
            # entries which are flagged as being in the blacklist
            return verify_list

    def of_entry(self, entries, inverted=False):
        entries = organise_array([entries])
        verify_list = []
        for item in self.data["entries"]:
            if inverted:
                verify_list.extend(list(filter(lambda e: is_child(item, e), entries)))
            else:
                verify_list.extend(list(filter(lambda e: is_child(e, item), entries)))

        return verify_list

    def check(self, directory, child=False):
        if child:
            return bool(self.of_entry(directory))
        else:
            return bool(self.is_entry(directory, inverted=True))

    def update(self):
        self.file.write_json(self.data)

    def add_completed(self, path, update=False):
        if path not in self.data['completed']:
            self.data['completed'].append(path)

        if update:
            self.update()

    def is_completed(self, path):
        return path in self.data["completed"]


Blacklist = _Blacklist()
del _Blacklist
