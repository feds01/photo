import re
from src.core.fileio import *
from src.blacklist import Blacklist
from src.utilities.arrays import organise_array
from src.utilities.infrequents import handle_fdreq, to_path

__author__ = "Alexander Fedotov <alexander.fedotov.uk@gmail.com>"
__company__ = "(C) Wasabi & Co. All rights reserved."


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

        files = Directory(path).index(file=True)

        for file in files:
            size += file_size(file)

        return size / unit


def get_drive(path):
        return os.path.splitdrive(path)[0]


def standardise_drive(path):
        drive = get_drive(path).capitalize()

        return drive + os.path.splitdrive(path)[1]


# similar to handle_fdreq(), however this will return only directories, and the actual path's rather than basename
def get_branches(path):
    try:
        return list(map(lambda x: x.path ,filter(lambda x: x.is_dir(), [x for x in os.scandir(path)])))

    except Exception as e:
        if not Config.get_session("verbose"):
            if e is PermissionError:
                IndexingError(path, 'permissions')

            # covers weird windows hidden folder mechanics
            if e is FileNotFoundError:
                IndexingError(path, 'un-loadable')

        return []


def index(path, count=False, file=False):
        file_list = []
        directories = []

        for root, dirs, files in os.walk(path):
            directories.extend(to_path(root, dirs))
            file_list.extend(to_path(root, files))

        if file and count:
            return len(file_list)
        if count:
            return len(directories)

        return file_list if file else directories

class Directory:
    def __init__(self, path):
        self.path = path
        self.directories = []

    def set_path(self, path):
        self.__init__(path)

    def index(self, count=False, file=False):
        file_list = []

        for root, dirs, files in os.walk(self.path):
            self.directories.extend(to_path(root, dirs))
            file_list.extend(to_path(root, files))

        if file and count:
            return len(file_list)
        if count:
            return len(self.directories)

        return file_list if file else self.directories

    def index_directory(self):
        for root, dirs, files in os.walk(self.path):
            del files

            if len(dirs) == 0 and root != self.path:
                self.directories.remove(root)

            else:
                self.directories.extend(to_path(root, dirs))

        return self.directories

    def index_with_blacklist(self):
        # a smarter method to filter with blacklists, modifies what
        # os.walk visits by removing from dirs necessary entries
        blacklist = Blacklist.blacklist

        drive_letter = get_drive(self.path)

        for entry in blacklist:
            if get_drive(entry) != drive_letter:
                blacklist.remove(entry)

        for root, dirs, files in os.walk(self.path, topdown=True):
            del files

            # DO NOT TOUCH 'IS' '==' does not work!
            if blacklist is []:
                for directory in dirs:
                    self.directories.append(directory)
            else:
                # remove directory from the directory list if the length of dirs is 0
                # check if the current 'root' is not actual directory entry point
                if len(dirs) == 0 and root != self.path:
                    self.directories.remove(root)

                for directory in to_path(root, dirs):
                    if directory in blacklist:
                        blacklist.remove(directory)
                        dirs.remove(os.path.split(directory)[1])

                    else:
                        self.directories.append(directory)

        return self.directories

    def index_photo_directory(self, return_folders=False):
        # the patterns are loaded from the config.yml file and complied,
        # further on they are used to quickly identify matching folder names
        # rather than relying on hard coded folder example names
        crt  = re.compile(Config.get('folders.crt.pattern'))
        all  = re.compile(Config.get('folders.all.pattern'))
        good = re.compile(Config.get('folders.good.pattern'))
        self.path = organise_array([self.path])
        self.directories = []

        def method(path):
            directories = {}
            content = handle_fdreq(path)

            def _find_item(directory, path):
                if crt.fullmatch(directory):
                    return {"crt": path}
                if all.fullmatch(directory):
                    return {"all": path}
                if good.fullmatch(directory):
                    return {"good": path}
                else:
                    return False

            if len(content) == 0:
                return directories

            for item in content:
                check = _find_item(item, os.path.join(path, item))

                if bool(check):
                    # we always know that certain keys will be present
                    directories.update(check)

                if len(directories.keys()) == 3:
                    break

            return directories

        if return_folders:
            try:
                return method(self.path[0])

            except IndexError:
                return method(self.path)

        if len(self.path) == 1:
            result = list(method(self.path[0]).values())
            if len(result) == 3:
                return self.path[0]
            else:
                pass
        else:
            for directory in self.path:
                result = list(method(directory).values())
                if len(self.directories) == Config.get("table_records"):
                    return self.directories
                if len(result) == 3:
                    self.directories.append(directory)
                else:
                    pass
            return self.directories

