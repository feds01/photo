#!C:\Python\Python35-32\python.exe
from baseTools import Directory, Cleaner
import os
import shutil


class File:
    def __init__(self):
        self.necessary_directories = ["temp", "artifact"]
        self.necessary_files_temp = ["photo_directories_data.txt", "removed_files_data.txt", "table_data.txt",
                                     "size_data.txt"]
        self.necessary_files_artifact = ["blacklist.txt", "completed_directories.txt"]
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

    def clean_files(self, file, specific, all=False):
        file_list = Cleaner().join_lists(self.necessary_files_artifact, self.necessary_files_temp)
        if file in file_list:
            with open(os.path.join(specific, file), "w") as f:
                f.flush(), f.truncate(), f.close()
        if all:
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
