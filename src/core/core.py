import ast
from src.core.utils import *
from src.core.config_extractor import *


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
        folder_keys = Config.get("folders")
        all_keys = []
        self.directory = Utility().list_organiser([self.directory])
        self.directories = []
        for basename_key in folder_keys:
            all_keys.append(Config.get("folders." + basename_key))
        all_keys = Utility().list_organiser(all_keys)

        def method(path):
            directories = {}
            content = handle_get_content(path, silent_mode=silent_mode)
            _validate_content_load(content)
            for basename in all_keys:
                    if basename in content:
                        directories.update({basename: os.path.join(path, basename)})
                    else:
                        pass
            return directories
        if return_folders:
            return method(self.directory[0])

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

    def check_file(self):
        return os.path.isfile(self.directory)

    @staticmethod
    def get_branches(path, silent=False):
        path_list = handle_get_content(path, silent)
        _validate_content_load(path_list)
        branch_directories = []
        for directory in path_list:
            if Directory(os.path.join(path, directory)).check_file():
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


class File:
    def __init__(self, file):
        self.application_root = Config.get("application_root")
        self.application_dirs = Config.get("application_directories.dirs")
        self.files = Config.get("application_directories.temp")
        self.file = file
        self.data = ""

    def setup_directories(self):
        for directory in self.application_dirs:
            try:
                os.mkdir(os.path.join(self.application_root, directory))
            except FileExistsError:
                pass

    def setup_files(self):
        for application_dir in self.application_dirs:
            if application_dir == "temp":
                for _file in self.files:
                    self.file = os.path.join(self.application_root, application_dir, _file)
                    self.create()
        self.file = Config.join_specific_data('application_root', 'blacklist.location')
        self.create()

    def clean_files(self):
        for file in self.files:
            with open(os.path.join(self.application_root, 'temp', file), "w") as f:
                f.flush(), f.truncate(), f.close()

    def write(self, data):
        if not Directory(self.file).check_file():
            return 0
        else:
            with open(self.file, "w") as f:
                f.write(str(data)), f.close()

    def read(self, specific):
        if not Directory(self.file).check_file():
            return None
        else:
            with open(self.file, "r") as f:
                try:
                    self.data = f.read()
                except SyntaxError:
                    if specific is "list":
                        return []
                    else:
                        return {}
                finally:
                    f.close()
                if specific in ["dict", "list"]:
                    return ast.literal_eval(self.data)
                else:
                    return self.data

    def remove(self):
        os.remove(self.file)

    def create(self):
        open(self.file, mode='w')