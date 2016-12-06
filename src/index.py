#!C:\Python\Python35-32\python.exe
import os
# import time
from src.core.exceptions import *
from src.core.utils import Directory, Utility
from src.data import Data

__author__ = "Alexander Fedotov <alexander.fedotov.uk@gmail.com>"
__company__ = "(C) Wasabi & Co. All rights reserved."


class Index:
    def __init__(self, path, thread_method=False):
        self.photo_model_directories = []
        self.thread_method = thread_method
        self.path = path
        self.directories = []
        self.directory_leaves = []

    @staticmethod
    def certify_directory(path):
        return Directory(path).index_photo_directory()

    def analyze_directories(self):
        self.photo_model_directories.append(self.certify_directory(self.directories))

    def directory_filter(self):
        for directory in self.directory_leaves:
            self.directories.remove(directory)

    @staticmethod
    def run_directory(path):
        if Directory(path).index_directory(count=True) < 3:
            pass
        if Index.certify_directory(path) is []:
            pass
        if Index.certify_directory(path):
            return path

    def find_leaves(self, path):
        for root, dirs, files in os.walk(path):
            if not dirs or len(dirs) < 3:
                self.directory_leaves.append(root)
        if self.thread_method:
            if path in self.directory_leaves:
                self.directory_leaves.remove(path)
            else:
                pass
        return self.directory_leaves

    def cycle(self, pipe=False):
        # start = time.clock()
        if not Directory(self.path).check_directory():
            raise Fatal("fatal: directory does not exist")
        if self.thread_method:
            if len(Directory.get_directory_branches(self.path, os.listdir(self.path))) == 0:
                return []
        if not self.thread_method:
            self.directories.append(Directory(self.path).get_current_directory())
        self.directories = Directory(self.path).index_directory()
        self.find_leaves(self.path)
        self.directory_filter()
        self.analyze_directories()
        if self.photo_model_directories is []:
            return []
        else:
            self.photo_model_directories = Utility().list_organiser(self.photo_model_directories)
            if pipe:
                Data(self.photo_model_directories).export_data_on_directories()
            else:
                # print(time.clock() - start)
                return self.photo_model_directories