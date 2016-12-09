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
    def __init__(self, directory=""):
        self.directory = directory
        self.new_black_list = []
        self.old_black_list = []
        self.black_list = []
        self.file_location = Directory(__file__).get_artifact_file_location("blacklist.txt")

    def read_blacklist(self, specific=None):
        self.black_list = File(self.file_location).read(specific="")
        if specific:
            if specific in self.black_list:
                return True
            else:
                return False
        else:
            return self.black_list

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

    def create_instance(self):
        self.old_black_list = []
        self.old_black_list = self.read_blacklist()
        self.old_black_list.append(self.directory)
        self.new_black_list = self.old_black_list
        File(self.file_location).write(self.new_black_list)

    def remove_entry(self, roots=False, children=False):
        cycle_done = False
        self.black_list = self.read_blacklist()
        if roots and children:
            cycle_done = True
            for entry in list(self.black_list):
                if is_child(self.directory, entry) or is_child(entry, self.directory):
                    self.black_list.remove(entry)

        if roots and not cycle_done:
            for entry in list(self.black_list):
                if is_child(self.directory, entry):
                    self.black_list.remove(entry)

        if children and not cycle_done:
            for entry in list(self.black_list):
                if is_child(entry, self.black_list):
                    self.black_list.remove(entry)

        if self.directory in self.black_list:
            self.black_list.remove(self.directory)

        self.purge_artifact(), File(self.file_location).write(self.black_list)

    def purge_artifact(self):
        File(self.file_location).remove(), File(self.file_location).create()
