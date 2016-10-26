#!C:\Python\Python35-32\python.exe
import os
from baseTools import Directory, Config


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

    def analyze_directory_skeleton(self):
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

    def cycle(self):
        self.directories = Directory(self.path).index_directory()
        if not self.thread_method:
            self.directories.append(Directory(self.path).get_current_directory())
        self.find_leaves(self.path)
        self.directory_filter()
        self.analyze_directory_skeleton()
        if self.photo_model_directories is []:
            return []
        else:
            return self.photo_model_directories