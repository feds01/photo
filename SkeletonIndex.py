#!C:\Python\Python35-32\python.exe
import os
from baseTools import Directory

__author__ = "Alexander Fedotov <alexander.fedotov.uk@gmail.com>"
__company__ = "(C) Wasabi & Co. All rights reserved."


class Basename:
        good_basename = ["_Good", "_GOOD", "Good", "GOOD", "good"]
        all_basename = ["_all", "_ALL", "all", "All", "ALL"]
        crt_basename = ["_DNG", "DNG", "crt", "_CRT", "Crt", "CRT"]

        @staticmethod
        def get_basename(specific):
            if specific == "good":
                return Basename.good_basename
            elif specific == "crt":
                return Basename.good_basename
            elif specific == "all":
                return Basename.good_basename


class Index:
    def __init__(self, path):
        self.photo_model_directories = []
        self.path = path
        self.directories = []
        self.folder_name = ""
        self.directoryLeaves = []

    @staticmethod
    def certify_directory_skeleton(path, specific_basename):
        for folder_name in Basename.get_basename(specific_basename):
            if Directory(os.path.join(path, folder_name)).check_directory():
                return True
            else:
                pass

    def analyze_directory_skeleton(self):
        for directory in self.directories:
                    if self.certify_directory_skeleton(directory, "all"):
                        if self.certify_directory_skeleton(directory, "good"):
                            if self.certify_directory_skeleton(directory, "crt"):
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
            if self.certify_directory_skeleton(self.path, "all"):
                if self.certify_directory_skeleton(self.path, "good"):
                    if self.certify_directory_skeleton(self.path, "crt"):
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
            if Index("").certify_directory_skeleton(path, "all"):
                if Index("").certify_directory_skeleton(path, "good"):
                    if Index("").certify_directory_skeleton(path, "crt"):
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
