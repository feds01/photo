#!C:\Python\Python35-32\python.exe
from baseTools import Directory, Cleaner
import os
import yaml
import shutil



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
        self.data = data
        self.file = file
        if not Directory(self.file).check_directory():
            return None
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


class Config:
    def __init__(self):
        self.stream = ""
        self.raw_data = {}
        self.key_list = []
        self.basename_data = {}
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

    def retrieve_basename_data(self):
        self.key_list = sorted(list(self.retrieve_config()))
        self.raw_data = self.retrieve_config()
        self.clean_raw_data(1)
        for directory_name_data in self.raw_data[self.key_list[1]]:
            self.basename_data.update({directory_name_data: self.raw_data[self.key_list[1]][directory_name_data]})
        return self.basename_data

    def retrieve_blacklist_data(self):
        pass

print(Config().retrieve_basename_data())