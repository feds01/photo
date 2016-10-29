#!C:\Python\Python35-32\python.exe
from utils import *
from tabulate import tabulate
import time
__author__ = "Alexander Fedotov <alexander.fedotov.uk@gmail.com>"
__company__ = "(C) Wasabi & Co. All rights reserved."


class Data:
    def __init__(self, path, pipe, pipe_file=""):
        self.pipe_file = pipe_file
        self.path = path
        self.destination_file = ""
        self.directory_data = Directory(Directory(str(self.path)).get_directory_size(1)).get_appropriate_units()
        self.analysis_path = Directory(path)
        self.counter_data = []
        self.packaged_data = {}
        self.temp_data_on_indexing = []
        self.extension_keys = []
        self.fetch_data_destination_path(pipe)

    def fetch_data_from_external_source(self):
        return File().read(self.pipe_file, "")

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
            self.packaged_data.update({self.path.index(photo_directory)+1: [photo_directory, Cleaner().directory_path_shorten(photo_directory), Directory((Directory(photo_directory)).get_directory_size(1)).get_appropriate_units()]})

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

class Table:
    def __init__(self, max_rows=5, pretty=False, detailed=False, path_char_size=30):
        self.max_rows = int(max_rows)
        self.data_packets = 0
        self.pretty = pretty
        self.detailed = detailed
        self.path_size = path_char_size
        self.table_import_data = {}
        self.headers = ["ID", "Directory-Path", "Size"]
        self.size_data = []
        self.all_columns = []
        self.column = []
        self.file_origin = ""


    def get_data_file_location(self, key):
        self.file_origin = Config().get_specific_data("data", key)
        self.file_origin = os.path.join(Directory(__file__).get_current_directory(), self.file_origin)
        return self.file_origin

    def import_table_data(self):
        self.table_import_data = File().read(self.get_data_file_location("table_data"), "_dict")
        self.data_packets = len(self.table_import_data.keys())
        for i in range(len(self.table_import_data.keys())):
            if (i) in range(self.max_rows):
                pass
            else:
                self.table_import_data.pop(i+1)
        return self.table_import_data

    def convert_import_data_to_column_data(self, key):
        self.column = []
        self.column.append(key)
        if self.path_size <= len(list(self.table_import_data[key][0])):
            self.column.append(self.table_import_data[key][1])
        else:
            self.column.append(self.table_import_data[key][0])
        self.size_data = self.table_import_data[key][2]
        if self.size_data[0] == 0:
            self.column.append("0Kb")
        else:
            if type(self.size_data[0]) == float:
                self.size_data[0] = str(self.size_data[0])
            self.column.append("".join(self.size_data[:2]))
        return self.column

    def create_final_column_data(self):
        self.import_table_data()
        for i in range(self.data_packets):
            self.all_columns.append(self.convert_import_data_to_column_data(i+1))
        return self.all_columns

    def make_table(self):
        self.create_final_column_data()
        print(tabulate(self.all_columns, self.headers))
        print()
        print("Enter ID of directory to initiate cleansing process")

