import re
from src.core.fileio import *
from src.blacklist import Blacklist
from src.core.config import *
from src.utilities.arrays import organise_array
from src.utilities.infrequents import handle_fdreq


def check_directory(directory):
    return os.path.exists(directory)


def find_specific_file(extension, files, case_sensitive=True):
    extension_list = []
    extensions = extension.split()

    if not case_sensitive:
        if extension.islower():
            extensions.append(extension.upper())
        else:
            extensions.append(extension.lower())

    for file in files:
        for extension in extensions:
            if file.endswith(extension):
                extension_list.append(file)

    return extension_list


def directory_size(path, unit=1):
        size = 0

        if not check_directory(path):
            return 0

        files = Directory(path).index_directory(file=True)

        for file in files:
            size += file_size(file)

        return size / unit


def get_drive(path):
        return os.path.splitdrive(path)[0]


def standardise_drive(path):
        drive = get_drive(path).capitalize()

        return drive + os.path.splitdrive(path.directory)[1]


class Directory:
    def __init__(self, item):
        self.directory = item
        self.byte_size = self.directory
        self.directory_list = []
        self.directories = []
        self.path = ""

    def set_path(self, path):
        self.__init__(path)

    def index_directory(self, count=False, file=False):
            file_list = []

            for directory, directories, files in os.walk(self.directory):
                for sub_directory in directories:
                    self.directory_list.append(os.path.join(directory, sub_directory))

                if file:
                    for _file in files:
                        file_list.append(os.path.join(directory, _file))
                else:
                    pass

            if file and count:
                return len(file_list)
            if count:
                return len(self.directory_list)

            return file_list if file else self.directory_list

    def index_with_blacklist(self):
        # a smarter method to filter with blacklists, modifies what
        # os.walk visits by removing from dirs necessary entries
        blacklist = Blacklist.blacklist

        drive_letter = get_drive(self.directory)

        for entry in blacklist:
            if get_drive(entry) != drive_letter:
                blacklist.remove(entry)
            else:
                continue

        for root, dirs, files in os.walk(self.directory, topdown=True):
            del files

            # DO NOT TOUCH 'IS' '==' does not work!
            if blacklist is []:
                for directory in dirs:
                    self.directories.append(os.path.join(directory))
            else:
                remove = []
                for directory in dirs:
                    directory = os.path.join(root, directory)
                    if directory in blacklist:
                        blacklist.remove(directory)
                        remove.append(os.path.split(directory)[1])

                    else:
                        self.directories.append(directory)
                        continue
                if len(remove) > 0:
                    for removable in remove:
                        dirs.remove(removable)
                else:
                    continue
        return self.directories

    def index_photo_directory(self, return_folders=False):
        # the patterns are loaded from the config.yml file and complied,
        # further on they are used to quickly identify matching folder names
        # rather than relying on hard coded folder example names
        crt_pattern  = re.compile(Config.get('folders.crt.pattern'))
        all_pattern  = re.compile(Config.get('folders.all.pattern'))
        good_pattern = re.compile(Config.get('folders.good.pattern'))
        self.directory = organise_array([self.directory])
        self.directories = []

        def method(path):
            directories = {}
            content = handle_fdreq(path)

            def _find_item(directory):
                if crt_pattern.fullmatch(directory):
                    return directory
                if all_pattern.fullmatch(directory):
                    return directory
                if good_pattern.fullmatch(directory):
                    return directory
                else:
                    return False

            if len(content) == 0:
                return directories

            for item in content:
                check = _find_item(item)
                if bool(check):
                    directories.update({check: os.path.join(path, check)})

                if len(directories.keys()) == 3:
                    break

                else:
                    continue

            return directories

        if return_folders:
            try:
                return method(self.directory[0])

            except IndexError:
                return method(self.directory)

        if len(self.directory) == 1:
            result = list(method(self.directory[0]).values())
            if len(result) == 3:
                return self.directory[0]
            else:
                pass
        else:
            for directory in self.directory:
                result = list(method(directory).values())
                if len(self.directories) == Config.get("table_records"):
                    return self.directories
                if len(result) == 3:
                    self.directories.append(directory)
                else:
                    pass
            return self.directories

    @staticmethod
    def get_branches(path):
        path_list = handle_fdreq(path)

        branch_directories = []
        for directory in path_list:
            if check_file(os.path.join(path, directory)):
                pass
            else:
                branch_directories.append(os.path.join(path, directory))

        return branch_directories

    def get_directory_size(self, unit=1):
        size = 0

        if not check_directory(self.path):
            return 0

        self.directory = self.index_directory(file=True)

        for file in self.directory:
            size += file_size(file)

        return size / unit

