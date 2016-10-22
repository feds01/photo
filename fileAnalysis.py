#!C:\Python\Python35-32\python.exe
from baseTools import *

__author__ = "Alexander Fedotov <alexander.fedotov.uk@gmail.com>"
__company__ = "(C) Wasabi & Co. All rights reserved."


class Data:
    def __init__(self, path):
        self.path = path
        self.destination_directory = os.path.join(Directory(__file__).get_current_directory(), "temp")
        self.destination_file = os.path.join(self.destination_directory, "photo_directories_data.txt")
        self.directory_data = list()
        self.analysis_path = Directory(self.path)
        self.counter_data = []
        self.packaged_data = {}
        self.directory_byte_size = int(Directory(self.path).get_directory_size(1))

    def create_data_on_directory(self):
        self.directory_data = Directory(self.directory_byte_size).get_appropriate_units()
        self.directory_data.append(self.analysis_path.index_photo_directory())
        for specific_key in Config().get_specific_keys("file_extensions"):
            for extension in Config().get_specific_data("file_extensions", specific_key):
                if extension == ".jpg":
                    self.directory_data.append(self.analysis_path.find_specific_file(extension))
                else:
                    self.counter_data.append(self.analysis_path.find_specific_file(extension))
        self.directory_data.insert(6, sum(self.counter_data))
        return self.directory_data

    def export_data_on_directory(self):
        self.packaged_data.update({self.path: self.create_data_on_directory()})
        File().write(self.packaged_data, self.destination_file)


Data("E:\\Photo\\TestFolder").export_data_on_directory()

