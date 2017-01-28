from src.core.utils import *

__author__ = "Alexander Fedotov <alexander.fedotov.uk@gmail.com>"
__company__ = "(C) Wasabi & Co. All rights reserved."

"""
Module name: blacklist.py
Usage: thread_indexer.py, cli.py
Description -

This module is used to manage and access the blacklist. The class 'Blacklist' is
used for checking and filtering the directory indexing results of indexer.py and
thread_indexer.py. The filtering of blacklist entries is available for performance.
Functions such as check_entry_existence() and check_child_entry() are used to verify
that if a given directory is or is under the blacklist. The modification of the blacklist
can also be done here. The function add_entry() will add an entry to the blacklist, the
function remove_entry() will remove an entry from a blacklist. Also the entered directory
to be scanned is also checked through the blacklist. This module also contains the function
'is_child()' which returns if an a given directory  is a child directory of another given
directory. The function also has support for symbolic links.

is_child():
:argument child     (the expected child directory)                                       [default= ""   (necessary)]
:argument directory (the parent directory)                                               [default= ""   (necessary)]
:argument symlinks  (use symlinks to check if :arg child is a child of :arg directory)   [default= False           ]

Note: Linux and Windows filesystems work
:returns directory= "/home/docs/"      child="/home/docs/html/apple/", is_child(child, directory) -> True
:returns directory= "/home/docs/"      child="/home/docs/",            is_child(child, directory) -> True
:returns directory= "/home/docs/html/" child="/home/docs/",            is_child(child, directory) -> False


_Blacklist():
:exception if :arg, entry is a child of a blacklist entry or another blacklist entry
:raises BlacklistEntryError

:exception if :arg, entry is not present and is trying to be removed.
:raises BlacklistEntryError


:returns blacklist= ["C:\\Users"]
         results=   ["C:\\Users\\Default", "C:\\photos\\projects"]
         Blacklist(results, "", use_filter=False).run_blacklist_check() -> ["C:\\Users\\Default"]
         Note: the function does not return the new result list, but only the results which
               need to be removed.

:returns blacklist= ["C:\\Users"]
         Blacklist.add_entry("C:\\Windows") -> blacklist= ["C:\\Users", "C:\\Windows"]

:returns blacklist= ["C:\\Users\\Default", "C:\\photos\\projects"]
         Blacklist.remove_entry("C:\\photos\\projects") -> blacklist= ["C:\\Users\\Default"]
"""


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
        self.file_location = Config.join_specific_data('application_root', 'blacklist', 'location')
        self.read_blacklist()

    def read_blacklist(self):
        self.blacklist = File(file=self.file_location).read(specific="list")

    def update_blacklist(self, instruction, *array):
        array = Utility().list_organiser([array])
        if instruction == self._INSERT:
            self.blacklist.extend(array)
        elif instruction == self._REMOVE:
            for entry in array:
                self.blacklist.remove(entry)
        elif instruction == self._PURGE:
            self.blacklist = []

        File(self.file_location).write(self.blacklist)

    def check_entry_existence(self, entries, inverted=False):
        entries = Utility().list_organiser([entries])
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

    def check_child_entry(self, entries, inverted=False):
        entries = Utility().list_organiser([entries])
        verify_list = []
        for item in self.blacklist:
            for entry in entries:
                if inverted:
                    # is a blacklist entry a child of a given directory
                    if is_child(item, entry):
                        verify_list.append(item)
                    else:
                        continue
                if not inverted:
                    # is a given directory a child of a blacklist entry
                    if is_child(entry, item):
                        verify_list.append(item)
                    else:
                        continue
        return verify_list

    def add_entry(self, entry):
        if entry in self.blacklist:
            raise BlacklistEntryError('present')
        if len(self.check_child_entry(entry)) > 0:
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

Blacklist = _Blacklist()
del _Blacklist