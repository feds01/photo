#!C:\Python\Python35-32\python.exe
import FileTransfer
import baseTools

__author__ = "Alexander Fedotov <alexander.fedotov.uk@gmail.com>"
__company__ = "(C) Wasabi & Co. All rights reserved."

photo_directory_list = []


class FileAnalysis:
    def __init__(self, path):
        self.path = path
        self.photo_model_directories = []

    def import_artifacts(self):
        pass

    def check_directory(self):
        if self.path in photo_directory_list:
            return True
        else:
            pass
