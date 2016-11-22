#!C:\Python\Python35-32\python.exe
from prettytable import PrettyTable
from src.utils import *
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
        self.extension_keys = []

    def fetch_data_destination_path(self, key):
        self.destination_file = Config().get_specific_data("data", key)
        self.destination_file = os.path.join(Directory(__file__).get_current_directory(), self.destination_file)
        return self.destination_file

    def create_data_on_directory(self, given_path):
        self.directory_data.append(given_path)
        self.analysis_path = Directory(given_path)
        self.file_list = Directory(given_path).index_directory(file=True)
        if self.file_list == []:
            self.directory_data.append([0, 0, 0, 0])
            self.directory_data = Cleaner().list_organiser(self.directory_data)
        else:
            self.extension_keys = Config().get_specific_keys("file_extensions")
            for specific_key in sorted(self.extension_keys):
                for extension in Config().get_specific_data("file_extensions", specific_key):
                    if extension == ".jpg":
                        self.counter_data.append(self.analysis_path.find_specific_file(extension, self.file_list))
                    else:
                        self.counter_data.append(self.analysis_path.find_specific_file(extension, self.file_list))
            for specific_files_list in self.counter_data:
                self.directory_data.append(len(specific_files_list))
        self.directory_data.insert(1, self.analysis_path.index_photo_directory())
        self.directory_data.append(Directory(Directory(given_path).get_directory_size(1)).get_appropriate_units())
        return self.directory_data

    def export_data_on_directories(self):
        start = time.clock()
        self.fetch_data_destination_path(self.pipe_file)
        self.packaged_data = {}
        for directory in self.path:
            self.packaged_data.update({self.path.index(directory)+1: self.create_data_on_directory(directory)})
        File().write(self.packaged_data, self.destination_file)
        return time.clock() - start


class Table:
    def __init__(self, path, max_index_sets=5, pretty=NotImplemented, detailed=NotImplemented, path_char_size=30):
        self.path = path
        self.max_rows = int(max_index_sets)
        self.data_packets = 0
        self.path_size = path_char_size
        self.table_import_data = {}
        self.headers = ["ID", "Directory-Path", "crt", "dng", "tif", "jpg"]
        self.table = PrettyTable()
        self.size_data = []
        self.border_data = []
        self.size_data_final = []
        self.all_rows = []
        self.row = []
        self.application_root, self.file_origin = "", ""
        self.border_symbol = "-"

    def get_data_file_location(self, key):
        self.file_origin = Config().get_specific_data("data", key)
        self.application_root = Config().get_key_value("application_root")
        self.file_origin = os.path.join(self.application_root, self.file_origin)
        return self.file_origin

    def import_table_data(self):
        self.table_import_data = File().read(self.get_data_file_location("size_data"), "_dict")
        self.data_packets = len(self.table_import_data.keys())
        for i in range(self.data_packets):
            if i in range(self.max_rows):
                pass
            else:
                self.table_import_data.pop(i+1)
        return self.table_import_data

    def get_specific_data_from_import(self, sub_key):
        specific_data = []
        for key in range(1, self.data_packets):
            specific_data.append(self.table_import_data[key][sub_key])
        return specific_data

    def make_row_data(self, key):
        self.row = []
        self.row.append(key)
        if self.path_size <= len(list(self.table_import_data[key][0])):
            self.row.append(Cleaner().shorten_path(self.table_import_data[key][0]))
        else:
            self.row.append(self.table_import_data[key][0])
        for sub_key in range(2, 6):
            self.row.append(self.table_import_data[key][sub_key])
        self.size_data = self.table_import_data[key][-1]
        if self.size_data[0] == 0:
            self.size_data_final.append("0Kb")
        else:
            if type(self.size_data[0]) == float:
                self.size_data[0] = str(self.size_data[0])
            self.size_data_final.append("".join(self.size_data[:2]))
        return self.row

    def make_border(self):
        borders = []
        for i in range(2, 6):
            i = Cleaner.int_list_to_str(self.get_specific_data_from_import(i))
            self.border_data.append(Cleaner.border_size_by_data_length(Cleaner.get_largest_element(i)))
        for i in self.border_data:
            borders.append(self.border_symbol * int(i))
        self.row = [Cleaner.border_size_by_data_length(self.max_rows, True)* self.border_symbol, (self.path_size+1)* self.border_symbol]
        self.row.extend(borders)
        self.table.add_row(self.row)
        del self.row

    def converge_row_data(self):
        self.import_table_data()
        for i in range(self.data_packets):
            self.all_rows.append(self.make_row_data(i + 1))
        return self.all_rows

    def define_table(self):
        self.table.border = False
        self.table.field_names = self.headers
        self.table.align = "l"

    def make_table(self):
        self.define_table()
        self.converge_row_data()
        print("Indexing Results of '" + self.path + "' . . .")
        self.make_border()
        for row in self.all_rows:
            self.table.add_row(row)
        self.size_data_final.insert(0, self.border_symbol*Cleaner.border_size_by_data_length(Cleaner.get_largest_element(self.size_data_final)))
        self.table.add_column("size", self.size_data_final, align="r")
        print(self.table)
        print()
        print("Enter ID of directory to initiate cleansing process")

Table("E:\\").make_table()