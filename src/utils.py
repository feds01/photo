import os
import yaml
import shutil
__author__ = "Alexander Fedotov <alexander.fedotov.uk@gmail.com>"
__company__ = "(C) Wasabi & Co. All rights reserved."


class Cleaner:
    def __init__(self):
        self.final_list = []
        self.input_list = []
        self.construct = []
        self.path_construct_list = []
        self.char_size = 0
        self.overflow_chars = 0
        self.old_block = ""
        self.cur_block = ""

    @staticmethod
    def get_largest_element(data):
        return len(max(data, key=len))

    @staticmethod
    def border_size_by_data_length(data, use_str=False):
        # TODO: improve function
        if use_str:
            return len(str(data)) + 2
        else:
            if data >= 4:
                return data + 1
            else:
                return 4

    @staticmethod
    def int_list_to_str(int_list):
        str_list = []
        for i in int_list:
            str_list.append(str(i))
        return str_list

    def list_organiser(self, path_list):
        self.input_list = [x for x in path_list if x]
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
        if len(path) > self.char_size:
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
            self.old_block = self.construct[0] + Directory.get_directory_separator()
            for block in self.construct[1:]:
                self.old_block = os.path.join(self.old_block, block)
            return self.old_block
        else:
            return path


class Directory:
    def __init__(self, main_input):
        self.main_input = main_input
        self.byte_exponent_count = 1024
        self.directory_size = 0
        self.byte_size = self.main_input
        self.directory_count = 0
        self.file_count = 0
        self.directory_list = []
        self.file_list = []
        self.file_extension_list = []
        self.file_sizes = {0: "bytes", 1: "Kb", 2: "Mb", 3: "Gb", 4: "Tb"}
        self.directories = []
        self.directory = ""
        self.path = ""

    def index_directory(self, count=False, file_c=False):
        if Directory(self.main_input).check_directory():
            for directory, directories, files in os.walk(self.main_input):
                for sub_directory in directories:
                    self.directory_count += 1
                    self.directory_list.append(os.path.join(directory, sub_directory))
                if file_c:
                    for file in files:
                        self.file_list.append(os.path.join(directory, file))
                        self.file_count += 1
                else:
                    pass
            if count:
                return self.directory_count
            if file_c:
                return self.file_list
            if file_c and count:
                return self.file_count
            if not count:
                return self.directory_list
        else:
            return 0

    def find_specific_file(self, extension, file_list):
        self.file_extension_list = []
        for file in file_list:
            if file.endswith(extension):
                self.file_extension_list.append(file)
            else:
                pass
        if not self.file_extension_list:
            return []
        else:
            return self.file_extension_list

    def index_photo_directory(self):
        self.folder_keys = Config().get_specific_keys("folders")
        self.directories_for_analysis = Cleaner().list_organiser([self.main_input])
        self.directories = []

        def method(path):
            directories = []
            for config_key in self.folder_keys:
                for basename in Config().get_specific_data("folders", config_key):
                    if basename in os.listdir(path):
                        directories.append(os.path.join(path, basename))
                    else:
                        pass
            return directories
        if len(self.directories_for_analysis) == 1:
            return method(self.directories_for_analysis[0])
        else:
            for directory in self.directories_for_analysis:
                if len(method(directory)) == 3:
                    self.directories.append(directory)
                else:
                    pass
            return self.directories

    def check_directory(self):
        if os.path.exists(str(self.main_input)):
            return True
        else:
            return False

    def check_file(self):
        if os.path.isfile(self.main_input):
            return True
        else:
            return False

    @staticmethod
    def get_directory_branches(path):
        branch_directories = []
        for directory in os.listdir(str(path)):
            if Directory(directory).check_file():
                pass
            else:
                branch_directories.append(os.path.join(path, directory))
        return branch_directories

    def get_current_directory(self):
        self.path = os.path.split(self.main_input)[0]
        return self.path

    def get_directory_size(self, unit):
        if not Directory(self.main_input).check_directory():
            return 0
        for directory, directories, files in os.walk(self.main_input):
            for file in files:
                self.path = os.path.join(directory, file)
                self.directory_size += os.path.getsize(self.path)
        return self.directory_size / unit

    def get_appropriate_units(self):
        if self.main_input == 0:
            return [self.main_input, "bytes", 1]
        else:
            for i in range(5):
                if self.byte_size / self.byte_exponent_count >= 1:
                    self.byte_size /= self.byte_exponent_count
                    continue
                if self.byte_size / self.byte_exponent_count < 1 and i == 0:
                    return [self.main_input, self.file_sizes[0], 1]
                if self.byte_size / self.byte_exponent_count < 1:
                    return [round(self.main_input / self.byte_exponent_count**i, 2), self.file_sizes[i], self.byte_exponent_count**i]

    def get_file_size(self, unit):
        return os.path.getsize(self.main_input) / unit

    def get_config_file_location(self):
        self.directory = Directory(self.main_input).get_current_directory()
        if self.directory.endswith("src"):
            self.directories = Directory(os.path.split(self.directory)[0]) .index_directory(file_c=True)
        else:
            self.directories = Directory(self.directory).index_directory(file_c=True)
        #TODO: remove code in main build, just for python to run quicker on this method
        for file in list(self.directories):
            if ".git" in file:
                self.directories.remove(file)
            if ".idea" in file:
                self.directories.remove(file)
            else:
                continue

        for file in list(self.directories):
            if os.path.split(file)[1] == "config.yml":
                return file
            else:
                pass

    @staticmethod
    def get_command_path():
        return os.getcwd()

    @staticmethod
    def get_directory_separator():
        if os.pathsep == ";":
            return "\\"
        else:
            return "/"


class Config:
    config_file_location =  Directory(__file__).get_config_file_location()
    #TODO: move everything from 'Config()' to config.py
    def __init__(self):
        self.stream = ""
        self.raw_data = {}
        self.config_raw_data = {}
        self.key_list = []
        self.data = {}
        self.retrieve_config()

    def retrieve_config(self):
        with open(self.config_file_location, "r") as self.stream:
            try:
                self.raw_data = yaml.load(self.stream)
                return self.raw_data
            except Exception as exc:
                print(exc)

    def clean_raw_data(self, exception_key):
        self.key_list = sorted(list(self.raw_data))
        for key in self.key_list:
            if key == self.key_list[exception_key]:
                pass
            else:
                self.raw_data.pop(key)

    def retrieve_data(self, key):
        self.get_config_keys()
        self.clean_raw_data(self.key_list.index(key))
        for data_group_key in self.raw_data[self.key_list[self.key_list.index(key)]]:
            self.data.update({data_group_key: self.raw_data[self.key_list[self.key_list.index(key)]][data_group_key]})
        return self.data

    def get_specific_data(self, key, specific):
        self.retrieve_data(key)
        return self.data[specific]

    def get_config_keys(self):
        self.key_list = sorted(list(self.raw_data))
        return self.key_list

    def get_specific_keys(self, key):
        self.get_config_keys()
        return self.raw_data[self.key_list[self.key_list.index(key)]].keys()



class File:
    def __init__(self):
        # TODO: move all stuff to YAML config file in artifacts
        self.necessary_directories = ["temp", "artifact"]
        self.necessary_files_temp = ["photo_directories_data.txt", "removed_files_data.txt", "table_data.txt",
                                     "size_data.txt"]
        self.necessary_files_artifact = ["blacklist.txt", "completed_directories.txt", "config.txt"]
        self.current_directory = Directory(__file__).get_current_directory()
        self.file = ""
        self.data = ""

    def setup_directories(self):
        for directory in self.necessary_directories:
            if os.path.exists(directory):
                pass
            else:
                os.mkdir(os.path.join(self.current_directory, directory))

    def setup_files(self):
        for file in self.necessary_files_temp:
            with open(os.path.join(self.necessary_directories[0], file), "w") as f:
                f.close()
        for file in self.necessary_files_artifact:
            with open(os.path.join(self.necessary_directories[1], file), "w") as f:
                f.close()

    def clean_files(self, file, specific, general=False):
        file_list = Cleaner().join_lists(self.necessary_files_artifact, self.necessary_files_temp)
        if file in file_list:
            with open(os.path.join(specific, file), "w") as f:
                f.flush(), f.truncate(), f.close()
        if general:
            for directory in self.necessary_directories:
                if directory == self.necessary_directories[1]:
                    pass
                else:
                    shutil.rmtree(os.path.join(self.current_directory, directory))

    def write(self, data, file):
        self.data = str(data)
        self.file = file
        if not Directory(self.file).check_directory():
            return 0
        else:
            with open(self.file, "w") as f:
                f.write(self.data), f.close()

    def read(self, file, specific):
        self.file = file
        if not Directory(self.file).check_file():
            return None
        else:
            if specific == "_dict":
                with open(file, "r") as f:
                    self.data = eval(f.read())
                    f.close()
                    return self.data
            else:
                with open(self.file, "r") as f:
                    self.data = f.read()
                    f.close()
                    return self.data

    def run_setup(self):
        self.setup_directories()
        self.setup_files()

