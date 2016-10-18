import os

__author__ = "Alexander Fedotov <alexander.fedotov.uk@gmail.com>"
__company__ = "(C) Wasabi & Co. All rights reserved."


class Cleaner:
    def __init__(self):
        self.final_list = []

    def list_organiser(self, path_list):
        path_list = [x for x in path_list if x]
        for element in path_list:
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
    def __init__(self, operation_input):
        self.operation_input = operation_input
        self.directory_size = 0
        self.directory_count = 0
        self.directory_list = []
        self.path = ""

    def index_directory(self, count=False):
        if Directory(self.operation_input).check_directory():
            for directory, directories, files in os.walk(self.operation_input):
                for sub_directory in directories:
                    self.directory_count += 1
                    self.directory_list.append(os.path.join(directory, sub_directory))
            if count:
                return self.directory_count
            if not count:
                return self.directory_list
        else:
            return 0

    def get_current_directory(self):
        self.path = os.path.split(self.operation_input)[0]
        return self.path

    def check_directory(self):
        if os.path.exists(self.operation_input):
            return True
        else:
            return False

    def get_directory_size(self, unit):
        for dirpath, dirnames, filenames in os.walk(self.operation_input):
            for file in filenames:
                self.path = os.path.join(dirpath, file)
                self.directory_size += os.path.getsize(self.path)
        return self.directory_size / unit

    def get_file_size(self, unit):
        return os.path.getsize(self.operation_input) / unit

    @staticmethod
    def get_command_path():
        return os.getcwd()
