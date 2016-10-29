#!C:\Python\Python35-32\python.exe
import os
from utils import Directory
from data import Data


__author__ = "Alexander Fedotov <alexander.fedotov.uk@gmail.com>"
__company__ = "(C) Wasabi & Co. All rights reserved."


class Index:
    def __init__(self, path, thread_method=False):
        self.photo_model_directories = []
        self.thread_method = thread_method
        self.path = path
        self.directories = []
        self.directoryLeaves = []

    @staticmethod
    def certify_directory(path):
        photo_sub_directories = Directory(path).index_photo_directory()
        return photo_sub_directories

    def analyze_directories(self):
        for directory in self.directories:
            if self.certify_directory(directory) is []:
                pass
            if self.certify_directory(directory):
                self.photo_model_directories.append(directory)

    def directory_filter(self):
        for directory in self.directoryLeaves:
            if Directory(directory).index_directory(count=True) <= 3:
                try:
                    self.directories.remove(directory)
                except ValueError:
                    pass
            else:
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
            if not dirs:
                self.directoryLeaves.append(root)
        return self.directoryLeaves

    def cycle(self, pipe=False):
        if not Directory(self.path).check_directory():
            print("fatal: entered directory does not exist")
            exit()
        self.directories = Directory(self.path).index_directory()
        if not self.thread_method:
            self.directories.append(Directory(self.path).get_current_directory())
            pass
        self.find_leaves(self.path)
        self.directory_filter()
        self.analyze_directories()
        if self.photo_model_directories is []:
            return []
        else:
            if pipe:
                Data(self.photo_model_directories, "table_data").export_data_on_photo_directory()
            else:
                return self.photo_model_directories