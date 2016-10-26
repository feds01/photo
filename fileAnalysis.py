#!C:\Python\Python35-32\python.exe
from baseTools import *
import time
__author__ = "Alexander Fedotov <alexander.fedotov.uk@gmail.com>"
__company__ = "(C) Wasabi & Co. All rights reserved."


class Data:
    def __init__(self, path, pipefile):
        self.path = path
        self.destination_file = ""
        self.directory_data = Directory(Directory(str(self.path)).get_directory_size(1)).get_appropriate_units()
        self.analysis_path = Directory(path)
        self.counter_data = []
        self.packaged_data = {}
        self.temp_data_on_indexing = []
        self.extension_keys = []
        self.fetch_data_destination_path(pipefile)

    def fetch_data_destination_path(self, key):
        self.destination_file = Config().get_specific_data("data", key)
        self.destination_file = os.path.join(Directory(__file__).get_current_directory(), self.destination_file)
        return self.destination_file

    def create_data_on_directory(self):
        self.directory_data.append(self.analysis_path.index_photo_directory())
        self.extension_keys = Config().get_specific_keys("file_extensions")
        for specific_key in self.extension_keys:
            for extension in Config().get_specific_data("file_extensions", specific_key):
                if Directory(self.path).index_directory(count=True, file_c=True) == 0:
                    self.directory_data.insert(6, 0)
                if extension == ".jpg":
                    self.directory_data.append(self.analysis_path.find_specific_file(extension))
                else:
                    self.counter_data.append(self.analysis_path.find_specific_file(extension))
        self.directory_data.insert(6, sum(self.counter_data))
        return self.directory_data

    def create_data_on_photo_directories(self):
        for photo_directory in self.path:
            self.packaged_data.update({self.path.index(photo_directory)+1: photo_directory})

    def export_data_on_directory(self):
        self.packaged_data.update({self.path: self.create_data_on_directory()})
        File().write(self.packaged_data, self.destination_file)

    def export_data_on_multiple_directories(self):
        self.packaged_data = {}
        for directory in self.path:
            self.packaged_data.update({directory: Data(directory).create_data_on_directory()})
        File().write(self.packaged_data, self.destination_file)

    def export_data_on_photo_directory(self):
        self.create_data_on_photo_directories()
        File().write(self.packaged_data, self.destination_file)

Data(['C:\\Users','E:\\Photo\\Sandbox','E:\\Software','E:\\','C:\\temp','F:\\type','Z:\\Launcher'], "table_data").export_data_on_photo_directory()
