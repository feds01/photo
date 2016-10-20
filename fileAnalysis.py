#!C:\Python\Python35-32\python.exe
from baseTools import Directory, Cleaner

__author__ = "Alexander Fedotov <alexander.fedotov.uk@gmail.com>"
__company__ = "(C) Wasabi & Co. All rights reserved."


class Data:
    def __init__(self, path):
        self.path = path
        self.directory_data = list()
        self.directory_byte_size = int(Directory(self.path).get_directory_size(1))

    def create_data_on_directory(self):
        self.directory_data = Directory(self.directory_byte_size).get_appropriate_units()
        self.directory_data.append(Directory(self.path).index_photo_directory())
        # print(type(self.directory_data))
        return self.directory_data


print(Data("E:\\Photo\\TestFolder").create_data_on_directory())

