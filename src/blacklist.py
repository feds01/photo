from src.core.utils import *

__author__ = "Alexander Fedotov <alexander.fedotov.uk@gmail.com>"
__company__ = "(C) Wasabi & Co. All rights reserved."


def is_child(child, directory, symlinks=False):
    directory = os.path.abspath(directory)
    child = os.path.abspath(child)
    if not symlinks and os.path.islink(child):
        return False
    return os.path.commonprefix([child, directory]) == directory


class Blacklist:
    def __init__(self, directory="", use_filter=False, *dirs):
        self.dirs = list(*dirs)
        self.use_filter = use_filter
        self.directory = directory
        self.disk = ""
        self.new_black_list = []
        self.black_list = []
        self.bad_entries, self.bad_child_entries = [], []
        self.child_list, self.root_list = [], []
        self.file_location = Directory(__file__).get_artifact_file_location("blacklist.txt")

    def read_blacklist(self):
        self.black_list = File(self.file_location).read(specific="")
        return self.black_list

    def get_child_entries(self):
        self.child_list = []
        self.black_list = self.read_blacklist()
        for entry in list(self.black_list):
            if is_child(entry, self.directory):
                self.child_list.append(entry)
            else:
                pass

    def get_root_entries(self):
        self.root_list = []
        self.black_list = self.read_blacklist()
        if os.path.split(self.directory)[1] == "":
            return []

        for entry in list(self.black_list):
            if is_child(self.directory, entry):
                self.root_list.append(entry)
            else:
                pass

    def check_entry_duplication(self):
        self.black_list = self.read_blacklist()
        if self.directory in self.black_list:
            return True

    def check_entry_recursive_duplication(self):
        self.black_list = self.read_blacklist()
        for entry in self.black_list:
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
        if directory in self.black_list:
            return True
        else:
            return False

    def add_entry(self):
        self.black_list = []
        self.black_list = self.read_blacklist()
        self.black_list.append(self.directory)
        self.new_black_list = self.black_list
        File(self.file_location).write(self.new_black_list)

    def remove_entry(self, roots=False, children=False):
        cycle_done = False
        self.bad_entries = []
        self.black_list = self.read_blacklist()
        if roots and children:
            cycle_done = True
            self.get_child_entries(), self.get_root_entries()
        if roots and not cycle_done:
            self.get_root_entries()
        if children and not cycle_done:
            self.get_child_entries()
        if self.directory in self.black_list:
            self.black_list.remove(self.directory)
        self.bad_entries = Utility().join_lists(self.child_list, self.root_list)
        for entry in self.bad_entries:
            self.black_list.remove(entry)
        self.purge_artifact(), File(self.file_location).write(self.black_list)

    def run_blacklist_check(self):
        self.black_list = self.read_blacklist()
        if self.use_filter:
            self.entry_filter_by_volume()
        self.bad_entries = []
        for directory in self.dirs:
            if self.check_entry_existence(directory):
                self.bad_entries.append(directory)
            else:
                pass
        for entry in self.bad_entries:
            self.bad_child_entries.append(Directory(entry).index_directory())

        return Utility().join_lists(self.bad_entries, self.bad_child_entries)

    def purge_artifact(self):
        File(self.file_location).remove(), File(self.file_location).create()

    def entry_filter_by_volume(self):
        self.disk = os.path.splitdrive(self.directory)
        for entry in self.black_list:
            if os.path.splitdrive(entry) != self.disk:
                self.black_list.remove(entry)
            else:
                pass