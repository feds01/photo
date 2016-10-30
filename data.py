#!C:\Python\Python35-32\python.exe
from utils import *
from tabulate import tabulate
import time
__author__ = "Alexander Fedotov <alexander.fedotov.uk@gmail.com>"
__company__ = "(C) Wasabi & Co. All rights reserved."


class Data:
    def __init__(self, path, pipe_file=""):
        self.path = path
        self.pipe_file = pipe_file
        self.destination_file = ""
        self.directory_data = []
        self.analysis_path = Directory(path)
        self.counter_data = []
        self.file_list = []
        self.packaged_data = {}
        self.final_data = {}
        self.extension_keys = []

    def fetch_data_destination_path(self, key):
        self.destination_file = Config().get_specific_data("data", key)
        self.destination_file = os.path.join(Directory(__file__).get_current_directory(), self.destination_file)
        return self.destination_file

    def create_data_on_directory(self):
        self.directory_data.append(self.path)
        self.directory_data.append(self.analysis_path.index_photo_directory())
        self.extension_keys = Config().get_specific_keys("file_extensions")
        self.file_list = Directory(self.path).index_directory(file_c=True)
        for specific_key in sorted(self.extension_keys):
            for extension in Config().get_specific_data("file_extensions", specific_key):
                if Directory(self.path).index_directory(count=True, file_c=True) == 0:
                    self.directory_data.insert(6, 0)
                if extension == ".jpg":
                    self.counter_data.append(self.analysis_path.find_specific_file(extension, self.file_list))
                else:
                    self.counter_data.append(self.analysis_path.find_specific_file(extension, self.file_list))
        for specific_files_list in self.counter_data:
            self.directory_data.append(len(specific_files_list))
        self.directory_data.append(Directory(Directory(str(self.path)).get_directory_size(1)).get_appropriate_units())
        return self.directory_data

    def export_data_on_directories(self):
        self.fetch_data_destination_path(self.pipe_file)
        self.packaged_data = {}
        for directory in self.path:
            self.packaged_data.update({self.path.index(directory)+1: Data(directory).create_data_on_directory()})
        File().write(self.packaged_data, self.destination_file)


class Table:
    def __init__(self, max_rows=5, pretty=False, detailed=False, path_char_size=30):
        self.max_rows = int(max_rows)
        self.data_packets = 0
        self.pretty = pretty
        self.detailed = detailed
        self.path_size = path_char_size
        self.table_import_data = {}
        self.headers = ["ID", "Directory-Path", "crt", "dng", "raw", "jpg", "Size"]
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
            if i in range(self.max_rows):
                pass
            else:
                self.table_import_data.pop(i+1)
        return self.table_import_data

    def convert_import_data_to_column_data(self, key):
        self.column = []
        self.column.append(key)
        if self.path_size <= len(list(self.table_import_data[key][0])):
            self.column.append(Cleaner().directory_path_shorten(self.table_import_data[key][0]))
        else:
            self.column.append(self.table_import_data[key][0])
        for sub_key in range(2, 6):
            self.column.append(self.table_import_data[key][sub_key])
        self.size_data = self.table_import_data[key][-1]
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

Data(["E:\\Photo\\Sandbox"], "table_data").export_data_on_directories()
Table().make_table()