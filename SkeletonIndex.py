#!C:\Python\Python35-32\python.exe
import os
from baseTools import Directory
from FileTransfer import Config

__author__ = "Alexander Fedotov <alexander.fedotov.uk@gmail.com>"
__company__ = "(C) Wasabi & Co. All rights reserved."


class Basename:
        def __init__(self):
            self.basename_data = {}

        def import_basename(self):
            self.basename_data = Config().retrieve_basename_data()
            return self.basename_data

        def get_basename(self, specific):
            self.import_basename()
            if specific == "good_folder_name":
                return self.basename_data[specific]
            elif specific == "crt_folder_name":
                return self.basename_data[specific]
            elif specific == "all_folder_name":
                return self.basename_data[specific]


class Index:
    def __init__(self, path):
        self.photo_model_directories = []
        self.path = path
        self.directories = []
        self.folder_name = ""
        self.directoryLeaves = []

    @staticmethod
    def certify_directory_skeleton(path, specific_basename):
        for folder_name in Basename().get_basename(specific_basename):
            if Directory(os.path.join(path, folder_name)).check_directory():
                return True
            else:
                pass

    def analyze_directory_skeleton(self):
        for directory in self.directories:
                    if self.certify_directory_skeleton(directory, "all_folder_name"):
                        if self.certify_directory_skeleton(directory, "good_folder_name"):
                            if self.certify_directory_skeleton(directory, "crt_folder_name"):
                                if directory in self.photo_model_directories:
                                    pass
                                else:
                                    self.photo_model_directories.append(directory)
                                    print("found! " + directory)
                            else:
                                pass
                        else:
                            pass
                    else:
                        pass

    def __directory_filter(self):
        for directory in self.directories:
            if directory in self.directoryLeaves:
                self.directories.remove(directory)
            if Directory(directory).index_directory(count=True) <= 3:
                try:
                    self.directories.remove(directory)
                except ValueError:
                    pass

    def run_parent_directory(self):
        if self.directories is None:
            return None
        else:
            if self.certify_directory_skeleton(self.path, "all_folder_name"):
                if self.certify_directory_skeleton(self.path, "good_folder_name"):
                    if self.certify_directory_skeleton(self.path, "crt_folder_name"):
                        if self.path in self.photo_model_directories:
                            pass
                        else:
                            self.photo_model_directories.append(self.path)
                            print("found! " + self.path)
                    else:
                        pass
                else:
                    pass
            else:
                pass

    @staticmethod
    def run_directory(path):
        if Directory(path).index_directory(count=True) < 3:
            return None
        else:
            if Index("").certify_directory_skeleton(path, "all_folder_name"):
                if Index("").certify_directory_skeleton(path, "good_folder_name"):
                    if Index("").certify_directory_skeleton(path, "crt_folder_name"):
                            print("found! " + path)
                            return path
                    else:
                        pass
                else:
                    pass
            else:
                pass

    def __find_leaves(self, path):
        for root, dirs, files in os.walk(path):
            if not dirs:
                self.directoryLeaves.append(root)

    @staticmethod
    def find_branches(path):
        branch_directories = []
        for directory in os.listdir(path):
            branch_directories.append(os.path.join(path, directory))
        return branch_directories

    def cycle(self):
        self.__find_leaves(self.path)
        self.directories = Directory(self.path).index_directory(count=False)
        self.__directory_filter()
        self.analyze_directory_skeleton()
        self.run_parent_directory()
        if self.photo_model_directories is None:
            return None
        else:
            return self.photo_model_directories

Index("E:\\").cycle()