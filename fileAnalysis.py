#!C:\Python\Python35-32\python.exe
from baseTools import *
import time
__author__ = "Alexander Fedotov <alexander.fedotov.uk@gmail.com>"
__company__ = "(C) Wasabi & Co. All rights reserved."


class Data:
    def __init__(self, path):
        self.path = path
        self.destination_file = ""
        self.directory_data = Directory(Directory(self.path).get_directory_size(1)).get_appropriate_units()
        self.analysis_path = Directory(path)
        self.counter_data = []
        self.packaged_data = {}
        self.temp_data_on_indexing = []
        self.extension_keys = []
        self.fetch_data_destination_path()

    def fetch_data_destination_path(self):
        self.destination_file = Config().get_specific_data("data", "index_data")
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

    def export_data_on_directory(self):
        start = time.clock()
        self.packaged_data.update({self.path: self.create_data_on_directory()})
        File().write(self.packaged_data, self.destination_file)
        return time.clock() - start

    def temp_data(self):
        for i in range(50):
            data = self.export_data_on_directory()
            print(i)
            print(self.packaged_data)
            print(data)
            self.temp_data_on_indexing.append(data)
        return self.temp_data_on_indexing
