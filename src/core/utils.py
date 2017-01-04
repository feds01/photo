import os
import ast
import shutil
from src.core.exceptions import *
from src.core.config_extractor import Config

__author__ = "Alexander Fedotov <alexander.fedotov.uk@gmail.com>"
__company__ = "(C) Wasabi & Co. All rights reserved."

"""
Module name: utils.py
Usage:
Description -

"""


def print_space(n):
    return n * "\n"


def get_largest_element(_list):
    return len(max(_list, key=len))


def find_element(_list, case):
        for element in _list:
                if case in element or case is element:
                    return int(_list.index(element))
                else:
                    pass


def extension_swapper(file, ext, remove_dot=False):
    if remove_dot:
        return file[:-4] + ext
    else:
        return file[:-3] + ext


def border_size_by_data_length(data, use_str=False):
        if use_str:
            return len(str(data)) + 2
        if data >= 4:
            return data + 1
        else: return 4


def int_list_to_str(int_list):
        str_list = []
        for i in int_list:
            str_list.append(str(i))
        return str_list


def get_command_path():
        return os.getcwd()


def get_directory_separator():
        if os.pathsep == ";":
            return "\\"
        else:
            return "/"


def handle_get_content(path, silent_mode=False):
    try:
        content = os.listdir(path)
    except PermissionError:
        if silent_mode:
            pass
        else:
            IndexingError(path, 'permissions')
        return ""
    return content


def _validate_content_load(content):
    if content is "":
        return ""
    else:
        pass


class Utility:
    def __init__(self):
        self.final_list = []
        self.input_list = []
        self.construct = []
        self.path_construct_list = []
        self.char_size = 0
        self.overflow_chars = 0
        self.block_pos = 0
        self.old_block = ""
        self.cur_block = ""
        self.slicing = False

    def list_organiser(self, _list):
        self.input_list = [x for x in _list if x]
        for element in self.input_list:
            if type(element) == list:
                self.final_list.extend(element)
            else:
                self.final_list.append(element)
        return self.final_list

    def join_lists(self, *lists):
        if len(lists) == 1:
            return lists[0]
        else:
            for element_list in lists:
                self.final_list.extend(element_list)
            return self.final_list

    def shorten_path(self, path, char_size=30, count_separator_char=False):
        self.char_size = char_size
        self.overflow_chars = len(path) - (self.char_size + 1)
        self.construct, self.input_list = path.split(os.sep), path.split(os.sep)
        if count_separator_char:
            for _ in self.input_list[:-1]:
                self.overflow_chars += 1
        if len(path) >= self.char_size:
            self.input_list.pop(-1)
            self.final_list.append({self.input_list[-1]: len(self.input_list[-1])})
            if int(self.final_list[0][self.input_list[-1]]) < self.overflow_chars:
                self.input_list.pop(-1)
                self.overflow_chars -= int(self.final_list[0][self.construct[-2]])
                for component in reversed(self.input_list):
                    if len(component) >= self.overflow_chars:
                        self.final_list.append({component: len(component)})
                        self.overflow_chars -= len(component)
                        if self.overflow_chars <= 0:
                            break
                    if len(component) < self.overflow_chars:
                        self.final_list.append({component: len(component)})
                        self.overflow_chars -= len(component)
                        continue
            self.input_list = list()
            for key in list(reversed(self.final_list)):
                self.input_list.append(list(key.keys()))
            self.input_list = self.list_organiser(self.input_list)[-len(self.input_list):]
            self.path_construct_list.append(self.construct.index(self.input_list[0]))
            for element in self.input_list:
                self.construct.remove(element)
            self.construct.insert(int(self.path_construct_list[0]), "...")
            while len("".join(self.construct)) + int(len(self.construct))-1 > char_size:
                self.overflow_chars = len("".join(self.construct)) + int(len(self.construct)) - 1
                if self.overflow_chars-3 <= char_size:
                    self.block_pos = (find_element(list(self.construct), "...")) - 1
                    if len(self.construct[self.block_pos]) is 3:
                        self.slicing = True
                        self.cur_block = self.construct[self.block_pos][0] + "..."
                        break
                    if self.overflow_chars - 2 == char_size + 1:
                        self.cur_block = str("".join(list(self.construct[self.block_pos])[:2])) + "..."
                    continue
                if self.overflow_chars > char_size:
                    self.construct.pop(self.construct.index("...")-1)
                else:
                    self.slicing = True
                    break
            if self.slicing:
                self.construct.pop(self.block_pos), self.construct.pop(self.construct.index("..."))
                self.construct.insert(self.block_pos, self.cur_block)
            self.old_block = self.construct[0] + get_directory_separator()
            for block in self.construct[1:]:
                self.old_block = os.path.join(self.old_block, block)
            return self.old_block
        else:
            return path


class Directory:
    def __init__(self, item):
        self.directory_object = item
        self.byte_exponent_count = 1024
        self.directory_size = 0
        self.byte_size = self.directory_object
        self.directory_list = []
        self.file_extension_list = []
        self.directories = []
        self.file_sizes = {0: "bytes", 1: "Kb", 2: "Mb", 3: "Gb", 4: "Tb"}
        self.drive_letter = ""
        self.directory = ""
        self.path = ""

    def index_directory(self, count=False, file=False):
            directory_count, file_count = 0, 0
            file_list = []
            for directory, directories, files in os.walk(self.directory_object):
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

    def index_with_blacklist(self, helpers):
        # a smarter method to filter with blacklists, modifies what
        # os.walk visits by removing from dirs necessary entries
        if helpers:
            artifact_location = dict(helpers).get('artifact-loc')
        else:
            artifact_location = os.path.join(Config.get_key_value('application_root'),
                                             Config.get_specific_data('blacklist', 'location'))

        self.drive_letter = self.get_directory_drive(self.directory_object)
        self.directory_list = File(artifact_location).read(specific='list')

        for entry in self.directory_list:
            if self.get_directory_drive(entry) != self.drive_letter:
                self.directory_list.remove(entry)
            else:
                continue
        if self.directory_object in self.directory_list:
            return []
        for root, dirs, files in os.walk(self.directory_object, topdown=True):
            del files
            if len(self.directory_list) is 0:
                pass
            else:
                for directory in dirs:
                    if os.path.join(root, directory) in self.directory_list:
                        self.directory_list.remove(os.path.join(root, directory))
                        dirs.remove(directory)
                        continue
            for directory in dirs:
                self.directories.append(os.path.join(root, directory))
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
        folder_keys = Config.get_specific_keys("folders")
        all_keys = []
        self.directory_object = Utility().list_organiser([self.directory_object])
        self.directories = []
        for basename_key in folder_keys:
            all_keys.append(Config.get_specific_data("folders", basename_key))
        all_keys = Utility().list_organiser(all_keys)

        def method(path):
            directories = []
            content = handle_get_content(path, silent_mode=silent_mode)
            _validate_content_load(content)
            for basename in all_keys:
                    if basename in content:
                        directories.append(os.path.join(path, basename))
                    else:
                        pass
            return directories
        if return_folders:
            return method(self.directory_object[0])
        if len(self.directory_object) == 1:
            result = method(self.directory_object[0])
            if len(result) == 3:
                return self.directory_object[0]
        else:
            for directory in self.directory_object:
                result = method(directory)
                if len(self.directories) == max_instances:
                    return self.directories
                if len(result) == 3:
                    self.directories.append(directory)
                else:
                    pass
            return self.directories

    def check_directory(self):
        if os.path.exists(self.directory_object):
            return True
        else:
            return False

    def check_file(self):
        if os.path.isfile(self.directory_object):
            return True
        else:
            return False

    @staticmethod
    def get_branches(path):
        path_list = handle_get_content(path)
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
        return os.path.splitdrive(path)[0][0]

    def get_parent_directory(self):
        self.path = os.path.split(self.directory_object)[0]
        return self.path

    def get_directory_size(self, unit=1):
        if not Directory(self.directory_object).check_directory():
            return 0
        for directory, directories, files in os.walk(self.directory_object):
            for file in files:
                self.path = os.path.join(directory, file)
                self.directory_size += os.path.getsize(self.path)
        return self.directory_size / unit

    def get_appropriate_units(self):
        if self.directory_object == 0:
            return [self.directory_object, "bytes", 1]
        if self.directory_object/1024**5 > 1:
            raise ByteOverflow
        else:
            for i in range(5):
                if self.byte_size / self.byte_exponent_count >= 1:
                    self.byte_size /= self.byte_exponent_count
                    continue
                if self.byte_size / self.byte_exponent_count < 1 and i == 0:
                    return [self.directory_object, self.file_sizes[0], 1]
                if self.byte_size / self.byte_exponent_count < 1:
                    return [round(self.directory_object / self.byte_exponent_count ** i, 2), self.file_sizes[i], self.byte_exponent_count ** i]

    def get_file_size(self, unit=1):
        return os.path.getsize(self.directory_object) / unit

    def get_artifact_file_location(self, filename):
        self.directory = Directory(self.directory_object).get_parent_directory()
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
        self.application_root = Config.get_key_value("application_root")
        self.application_directories = sorted(Config.get_specific_data("application_directories","dirs"))
        self.temp_files = Config.get_specific_data("application_directories", "temp")
        self.artifact_files = Config.get_specific_data("application_directories", "artifact")
        self.file = file
        self.data = ""

    def setup_directories(self):
        for directory in self.application_directories:
            try:
                os.mkdir(os.path.join(self.application_root, directory))
            except FileExistsError:
                pass

    def setup_files(self):
        for application_dir in self.application_directories:
            if application_dir == "temp":
                for _file in self.temp_files:
                    self.file = os.path.join(self.application_root, application_dir, _file)
                    self.create()
            else:
                for _file in self.artifact_files:
                    self.file = os.path.join(self.application_root, application_dir, _file)
                    self.create()

    def clean_files(self, file, specific, general=False):
        file_list = Utility().join_lists(self.artifact_files, self.temp_files)
        if file in file_list:
            with open(os.path.join(specific, file), "w") as f:
                f.flush(), f.truncate(), f.close()
        if general:
            for directory in self.application_directories:
                if directory == self.application_directories[1]:
                    pass
                else:
                    shutil.rmtree(os.path.join(self.application_root, directory))

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
                if specific in ["_dict", "list"]:
                    return ast.literal_eval(self.data)
                else:
                    return self.data

    def remove(self):
        os.remove(self.file)

    def create(self):
        with open(self.file, "w") as f:
            f.close()

    def run_setup(self):
        self.setup_directories()
        self.setup_files()