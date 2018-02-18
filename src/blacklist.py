from src.core.fileio import *
from src.core.exceptions import *
from src.utilities.arrays import organise_array

__author__ = "Alexander Fedotov <alexander.fedotov.uk@gmail.com>"
__company__ = "(C) Wasabi & Co. All rights reserved."

def is_child(child, directory, symlinks=False):
    directory = os.path.abspath(directory)
    child = os.path.abspath(child)
    if not symlinks and os.path.islink(child):
        return False
    return os.path.commonprefix([child, directory]) == directory


class _Blacklist:
    _REMOVE = 0x00
    _INSERT = 0x01
    _PURGE = 0x02

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

    def update_blacklist(self, instruction, array):
        current_data = self.file.read_json()
        current_data["entries"] = []

        array = organise_array([array])
        if instruction == self._INSERT:
            self.blacklist.extend(array)
        elif instruction == self._REMOVE:
            for entry in array:
                self.blacklist.remove(entry)
        elif instruction == self._PURGE:
            self.blacklist = []

        for entry in self.blacklist:
            current_data["entries"].append(entry)

        self.file.write_json(current_data)

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

    def add_entry(self, entry):
        if entry in self.blacklist:
            raise BlacklistEntryError('present')
        if len(self.of_entry(entry)) > 0:
                raise BlacklistEntryError('present')
        else:
            self.update_blacklist(self._INSERT, entry)

    def remove_entry(self, entry, by_child=False):
        if entry not in self.blacklist and not by_child:
            return BlacklistEntryError('not-present')
        if entry in self.blacklist:
            self.bad_entries.append(entry)
        else:
            for item in self.blacklist:
                if is_child(item, entry):
                    self.bad_entries.append(item)
                else:
                    pass

        self.update_blacklist(self._REMOVE, self.bad_entries)

    def check(self, directory, child=False):
        self.read_blacklist()

        if child:
            return bool(self.of_entry(directory))
        else:
            return bool(self.is_entry(directory, inverted=True))


Blacklist = _Blacklist()
del _Blacklist