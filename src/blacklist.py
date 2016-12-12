from src.core.utils import *

__author__ = "Alexander Fedotov <alexander.fedotov.uk@gmail.com>"
__company__ = "(C) Wasabi & Co. All rights reserved."

"""
Module name: blacklist.py
Usage: blacklist_hook.py, cli.py
Description -

This module is used to manage and access the blacklist. The class 'Blacklist' is
used for checking and filtering the directory indexing results of indexer.py. If
any of the results are children of an entry in the blacklist or are any entry in
the blacklist, they are filtered out by blacklist_hook.py. The filtering of blacklist
entries is also available for performance. The function "entry_filter_by_volume()"
will filter any entries which do not have the same volume label as the index results.
Also the entered directory to be scanned is also checked through the blacklist. The
class also contains functions which are periodically run by 'blacklist_hook.py' to keep
the blacklist clean. Remove child entries or root entries or duplicate entries are performed
by the function 'redundancy_check()'. This module also contains the function 'is_child()'
which returns if an a given directory is a child directory of another given directory.
The function also has support for symbolic links.

is_child():
:argument child     (the expected child directory)                                       [default= ""   (necessary)]
:argument directory (the parent directory)                                               [default= ""   (necessary)]
:argument symlinks  (use symlinks to check if :arg child is a child of :arg directory)   [default= False           ]

Note: Linux and Windows filesystems work
:returns directory= "/home/docs/"      child="/home/docs/html/apple/", is_child(child, directory) -> True
:returns directory= "/home/docs/"      child="/home/docs/",            is_child(child, directory) -> True
:returns directory= "/home/docs/html/" child="/home/docs/",            is_child(child, directory) -> False


Blacklist():
:exception if :arg directory is a child of a blacklist entry or another blacklist entry
:raises BlacklistEntryError

:exception if :arg directory is not present and is trying to be removed.
:raises BlacklistEntryError

:argument dirs       (a list of directories to run through run_blacklist_check())        [default= []            ]
:argument directory  (check, remove or add an entry to the blacklist)                    [default= "" (necessary)]
:argument use_filter (uses entry_filter_by_volume() to filter  blacklist entries)        [default= False         ]

:returns blacklist= ["C:\\Users"]
         results=   ["C:\\Users\\Default", "C:\\photos\\projects"]
         Blacklist(results, "", use_filter=False).run_blacklist_check() -> ["C:\\Users\\Default"]
         Note: the function does not return the new result list, but only the results which
               need to be removed.

:returns blacklist= ["C:\\Users"]
         Blacklist(directory="C:\\Windows").add_entry() -> blacklist= ["C:\\Users", "C:\\Windows"]

:returns blacklist= ["C:\\Users\\Default", "C:\\photos\\projects"]
         Blacklist(directory="C:\\photos\\projects").remove_entry() -> blacklist= ["C:\\Users\\Default"]
"""


def is_child(child, directory, symlinks=False):
    directory = os.path.abspath(directory)
    child = os.path.abspath(child)
    if not symlinks and os.path.islink(child):
        return False
    return os.path.commonprefix([child, directory]) == directory


class Blacklist:
    def __init__(self, *dirs, directory="", use_filter=False):
        self.dirs = list(*dirs)
        self.use_filter = use_filter
        self.directory = directory
        self.disk = ""
        self.new_blacklist = []
        self.blacklist = []
        self.bad_entries, self.bad_child_entries = [], []
        self.child_list, self.root_list = [], []
        self.file_location = Directory(__file__).get_artifact_file_location("blacklist.txt")

    def read_blacklist(self):
        self.blacklist = File(self.file_location).read(specific="")
        return self.blacklist

    def get_child_entries(self):
        self.child_list = []
        self.blacklist = self.read_blacklist()
        for entry in list(self.blacklist):
            if is_child(entry, self.directory):
                self.child_list.append(entry)
            else:
                pass

    def get_root_entries(self):
        self.root_list = []
        self.blacklist = self.read_blacklist()
        if os.path.split(self.directory)[1] == "":
            return []

        for entry in list(self.blacklist):
            if is_child(self.directory, entry):
                self.root_list.append(entry)
            else:
                pass

    def check_entry_duplication(self):
        self.blacklist = self.read_blacklist()
        if self.directory in self.blacklist:
            return True

    def check_entry_recursive_duplication(self):
        self.blacklist = self.read_blacklist()
        for entry in self.blacklist:
            if is_child(entry, self.directory) or is_child(self.directory, entry):
                return True
            else:
                pass

    def redundancy_check(self):
        if self.check_entry_duplication() or self.check_entry_recursive_duplication():
            self.remove_entry(roots=True, children=True)
        else:
            pass

    def check_entry_existence(self, directory):
        if directory in self.blacklist:
            return True
        else:
            return False

    def add_entry(self):
        self.blacklist = []
        self.blacklist = self.read_blacklist()
        if self.directory in self.blacklist:
            raise BlacklistEntryError("present")
        for entry in self.blacklist:
            if is_child(self.directory, entry):
                raise BlacklistEntryError("present")

        self.blacklist.append(self.directory)
        self.new_blacklist = self.blacklist
        File(self.file_location).write(self.new_blacklist)

    def remove_entry(self, roots=False, children=False):
        cycle_done = False
        self.bad_entries = []
        self.blacklist = self.read_blacklist()
        if self.directory not in self.blacklist:
            raise BlacklistEntryError("not-present")
        else:
            if roots and children:
                cycle_done = True
                self.get_child_entries(), self.get_root_entries()
            if roots and not cycle_done:
                self.get_root_entries()
            if children and not cycle_done:
                self.get_child_entries()
            if self.directory in self.blacklist:
                self.blacklist.remove(self.directory)
            self.bad_entries = Utility().join_lists(self.child_list, self.root_list)
            for entry in self.bad_entries:
                self.blacklist.remove(entry)
            self.purge_artifact(), File(self.file_location).write(self.blacklist)

    def run_blacklist_check(self):
        self.blacklist = self.read_blacklist()
        if self.use_filter:
            self.entry_filter_by_volume()
        self.bad_entries = []
        for directory in self.dirs:
            if self.check_entry_existence(directory):
                self.bad_entries.append(directory)
                self.bad_entries.append(Directory(directory).index_directory())

        return Utility().join_lists(self.bad_entries, self.bad_child_entries)

    def purge_artifact(self):
        File(self.file_location).remove(), File(self.file_location).create()

    def entry_filter_by_volume(self):
        self.disk = os.path.splitdrive(self.directory)
        for entry in self.blacklist:
            if os.path.splitdrive(entry) != self.disk:
                self.blacklist.remove(entry)
            else:
                pass