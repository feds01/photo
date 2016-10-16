#!C:\Python\Python35-32\python.exe
import os

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
        self.directory_count = 0
        self.directory_list = []
        self.directories = []
        self.folder_name = ""
        self.directoryLeaves = []

    @staticmethod
    def checkDirectory(path):
        if os.path.exists(path):
            return True
        else:
            return False

    def directory(self, path, count=False):
        if Index.checkDirectory(path):
            for directory, directories, files in os.walk(path):
                for sub_directory in directories:
                    self.directory_count += 1
                    self.directory_list.append(os.path.join(directory, sub_directory))
            if count:
                return self.directory_count
            if not count:
                return self.directory_list
        else:
            return 0

    @staticmethod
    def certifyDirectorySkeleton(path, specific_basename):
        for folder_name in Basename.get_basename(specific_basename):
            if Index.checkDirectory(os.path.join(path, folder_name)):
                return True
            else:
                pass

    def analyzeDirectorySkeleton(self):
        for directory in self.directories:
                    if self.certifyDirectorySkeleton(directory, "all"):
                        if self.certifyDirectorySkeleton(directory, "good"):
                            if self.certifyDirectorySkeleton(directory, "crt"):
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

    def __directoryListFilter(self):
        for directory in self.directories:
            if directory in self.directoryLeaves:
                self.directories.remove(directory)
            if Index.directory(self, directory, count=True) <= 3:
                try:
                    self.directories.remove(directory)
                except ValueError:
                    pass

    def runParentDirectory(self):
        if self.directories is None:
            return None
        else:
            if self.certifyDirectorySkeleton(self.path, "all"):
                if self.certifyDirectorySkeleton(self.path, "good"):
                    if self.certifyDirectorySkeleton(self.path, "crt"):
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
        if Index("").directory(path, count=True) < 3:
            return None
        else:
            if Index("").certifyDirectorySkeleton(path, "all"):
                if Index("").certifyDirectorySkeleton(path, "good"):
                    if Index("").certifyDirectorySkeleton(path, "crt"):
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
        self.directories = Index.directory(self, self.path, count=False)
        self.__directoryListFilter()
        self.analyzeDirectorySkeleton()
        self.runParentDirectory()
        if self.photo_model_directories is None:
            return None
        else:
            return self.photo_model_directories
