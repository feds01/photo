import os
import yaml
import shutil

__author__ = "Alexander Fedotov <alexander.fedotov.uk@gmail.com>"
__company__ = "(C) Wasabi & Co. All rights reserved."


class Cleaner:
    def __init__(self):
        self.final_list = []
        self.input_list = []

    def list_organiser(self, path_list):
        self.input_list = [x for x in path_list if x]
        for element in self.input_list:
            if type(element) == list:
                self.final_list.extend(self.list_organiser(element))
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

    def find_specific_file(self, extension):
        for root, dirs, files in os.walk(self.main_input):
            for file in files:
                if file.endswith(extension):
                    self.file_list.append(os.path.join(root, file))
        if not self.file_list:
            return 0
        else:
            return self.file_list

    def index_photo_directory(self):
        for config_key in Config().get_specific_keys("folders"):
            for basename in Config().get_specific_data("folders", config_key):
                if os.path.join(self.main_input, basename) in self.get_directory_branches(self.main_input):
                    self.directories.append(os.path.join(self.main_input, basename))
                else:
                    pass

        return self.directories

    def check_directory(self):
        if os.path.exists(self.main_input):
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
        for directory in os.listdir(path):
            if Directory(directory).check_file():
                pass
            else:
                branch_directories.append(os.path.join(path, directory))
        return branch_directories

    def get_current_directory(self):
        self.path = os.path.split(self.main_input)[0]
        return self.path

    def get_directory_size(self, unit):
        for directory, directories, files in os.walk(self.main_input):
            for file in files:
                self.path = os.path.join(directory, file)
                self.directory_size += os.path.getsize(self.path)
        return self.directory_size / unit

    def get_appropriate_units(self):
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
        self.directories = list(Directory(self.directory).index_directory(file_c=True))
        for file in self.directories:
            if os.path.split(file)[1] == "config.yml":
                return file
            else:
                pass

    @staticmethod
    def get_command_path():
        return os.getcwd()


class Config:
    def __init__(self):
        self.stream = ""
        self.raw_data = {}
        self.key_list = []
        self.data = {}
        self.config_file_location = ""

    def retrieve_config(self):
        with open(Directory(__file__).get_config_file_location(), "r") as self.stream:
            try:
                return yaml.load(self.stream)
            except Exception as exc:
                print(exc)

    def clean_raw_data(self, exception_key):
        self.key_list = sorted(list(self.retrieve_config()))
        for key in self.key_list:
            if key == self.key_list[exception_key]:
                pass
            else:
                self.raw_data.pop(key)

    def retrieve_data(self, key):
        self.get_config_keys()
        self.raw_data = self.retrieve_config()
        self.clean_raw_data(self.key_list.index(key))
        for data_group_key in self.raw_data[self.key_list[self.key_list.index(key)]]:
            self.data.update({data_group_key: self.raw_data[self.key_list[self.key_list.index(key)]][data_group_key]})
        return self.data

    def get_specific_data(self, key, specific):
        self.retrieve_data(key)
        return self.data[specific]

    def get_config_keys(self):
        self.key_list = sorted(list(self.retrieve_config()))
        return self.key_list

    def get_specific_keys(self, key):
        self.get_config_keys()
        return self.retrieve_config()[self.key_list[self.key_list.index(key)]].keys()


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
        if not Directory(self.file).check_directory():
            return None
        else:
            if specific == "dict":
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
