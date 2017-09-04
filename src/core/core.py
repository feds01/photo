import re
from src.core.fileio import *
from src.core.config_extractor import *
from src.utilities.simple import organise_list


def _validate_content_load(content):
    if content is "":
        return ""
    else:
        pass


class Directory:
    def __init__(self, item):
        self.directory = item
        self.directory_size = 0
        self.byte_size = self.directory
        self.directory_list = []
        self.file_extension_list = []
        self.directories = []
        self.drive_letter = ""
        self.path = ""

    def index_directory(self, count=False, file=False):
            directory_count, file_count = 0, 0
            file_list = []
            for directory, directories, files in os.walk(self.directory):
                for sub_directory in directories:
                    directory_count += 1
                    self.directory_list.append(os.path.join(directory, sub_directory))
                if file:
                    for _file in files:
                        file_list.append(os.path.join(directory, _file))
                        file_count += 1
                else:
                    pass
            if file and count:
                return file_count
            if count:
                return directory_count
            if file:
                return file_list
            else:
                return self.directory_list

    def index_with_blacklist(self):
        # a smarter method to filter with blacklists, modifies what
        # os.walk visits by removing from dirs necessary entries

        artifact_location = Config.join_specific_data('application_root', 'blacklist.location')
        self.drive_letter = self.get_directory_drive(self.directory)
        blacklist = File(artifact_location).read(specific='list')
        for entry in blacklist:
            if self.get_directory_drive(entry) != self.drive_letter:
                blacklist.remove(entry)
            else:
                continue
        for root, dirs, files in os.walk(self.directory, topdown=True):
            del files
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

    def find_specific_file(self, extension, files, case_sensitive=True):
        self.file_extension_list = []
        extensions = extension.split()
        if not case_sensitive:
            if extension.islower():
                extensions.append(extension.upper())
            else:
                extensions.append(extension.lower())
        for file in files:
            for extension in extensions:
                if file.endswith(extension):
                    self.file_extension_list.append(file)
                else:
                    pass
        return self.file_extension_list

    def index_photo_directory(self, return_folders=False, silent_mode=False, max_instances=-1):
        crt_pattern  = re.compile(Config.get('folders.crt.pattern'))
        all_pattern  = re.compile(Config.get('folders.all.pattern'))
        good_pattern = re.compile(Config.get('folders.good.pattern'))
        self.directory = organise_list([self.directory])
        self.directories = []

        def method(path):
            directories = {}
            content = handle_get_content(path, silent_mode=silent_mode)
            _validate_content_load(content)

            def _find_item(directory):
                if crt_pattern.fullmatch(directory):
                    return directory
                if all_pattern.fullmatch(directory):
                    return directory
                if good_pattern.fullmatch(directory):
                    return directory
                else:
                    return False

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
                if len(self.directories) == max_instances:
                    return self.directories
                if len(result) == 3:
                    self.directories.append(directory)
                else:
                    pass
            return self.directories

    def check_directory(self):
        return os.path.exists(self.directory)

    @staticmethod
    def get_branches(path, silent=False):
        path_list = handle_get_content(path, silent)
        _validate_content_load(path_list)
        branch_directories = []
        for directory in path_list:
            if check_file(os.path.join(path, directory)):
                pass
            else:
                branch_directories.append(os.path.join(path, directory))

        return branch_directories

    @staticmethod
    def get_directory_drive(path):
        return os.path.splitdrive(path)[0]

    def standardise_drive(self):
        drive = self.get_directory_drive(self.directory).capitalize()
        return drive + os.path.splitdrive(self.directory)[1]

    def get_parent_directory(self):
        return os.path.split(self.directory)[0]

    def get_directory_size(self, unit=1):
        if not self.check_directory():
            return 0
        self.directory = self.index_directory(file=True)
        for file in self.directory:
            self.directory_size += os.path.getsize(file)
        return self.directory_size / unit

    def get_file_size(self, unit=1):
        return os.path.getsize(self.directory) / unit

    def get_artifact_file_location(self, filename):
        self.directory = self.get_parent_directory()
        if self.directory.endswith("src"):
            self.directories = Directory(os.path.split(self.directory)[0]).index_directory(file=True)
        else:
            self.directories = Directory(self.directory).index_directory(file=True)
        # TODO: remove code in main build, just for finder to run quicker on this method
        for file in list(self.directories):
            if ".git" in file:
                self.directories.remove(file)
            if ".idea" in file:
                self.directories.remove(file)
            else:
                continue

        for file in list(self.directories):
            if os.path.split(file)[1] == filename:
                return file
            else:
                pass
