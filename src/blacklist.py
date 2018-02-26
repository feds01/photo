from src.core.fileio import *
from src.utilities.infrequents import is_child
from src.utilities.arrays import organise_array


__author__ = "Alexander Fedotov <alexander.fedotov.uk@gmail.com>"
__company__ = "(C) Wasabi & Co. All rights reserved."


class _Blacklist:
    def __init__(self):
        self.blacklist = []
        self.bad_entries = []
        self.file_location = Config.join('application_root', 'blacklist.location')
        self.file = File(file=self.file_location)

        self.read_blacklist()

    def read_blacklist(self):
        current_data = self.file.read_json()

        for entry in current_data["entries"]:
            self.blacklist.append(entry)

        if self.blacklist is None:
            if os.path.exists(self.file_location):
                self.read_blacklist()
            else:
                self.file.create(), self.file.write_json('{"entries": []}')
                # open the file and write the initial blacklist

    def is_entry(self, entries, inverted=False):
        entries = organise_array([entries])
        verify_list = []
        for entry in entries:
            if entry in self.blacklist:
                verify_list.append(entry)
            else:
                pass
        if not inverted:
            # entries which came out clean
            for entry in verify_list:
                entries.remove(entry)
            return entries
        else:
            # entries which are flagged as being in the blacklist
            return verify_list

    def of_entry(self, entries, inverted=False):
        entries = organise_array([entries])
        verify_list = []
        for item in self.blacklist:
            for entry in entries:
                if inverted:
                    # is a blacklist entry a child of a given directory
                    if is_child(item, entry):
                        verify_list.append(item)

                if not inverted:
                    # is a given directory a child of a blacklist entry
                    if is_child(entry, item):
                        verify_list.append(item)

        return verify_list

    def check(self, directory, child=False):
        self.read_blacklist()

        if child:
            return bool(self.of_entry(directory))
        else:
            return bool(self.is_entry(directory, inverted=True))


Blacklist = _Blacklist()
del _Blacklist