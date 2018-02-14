#!C:\Python\Python36\python.exe
# import time
from src.core.core import *
from prettytable import PrettyTable
from src.utilities.shorts import *
from src.utilities.manipulation import to_string, largest_element, sizeof_fmt

__author__ = "Alexander Fedotov <alexander.fedotov.uk@gmail.com>"
__company__ = "(C) Wasabi & Co. All rights reserved."

"""
Module name: data.py
Usage:
Description -

"""


class Data:
    def __init__(self, path):
        self.path = path
        self.destination_file = ""
        self.directory_data = {}
        self.packaged_data = {}
        self.counter_data = []
        self.file_list = []

    def fetch_data_destination_path(self):
        self.destination_file = Config.join_specific_data('application_root', 'application_directories.size_data')
        return self.destination_file

    def datafy(self, path):
        self.directory_data, self.file_list, data = {}, [], {}
        self.directory_data.update({'path': path})

        analysis_path = Directory(path)
        self.file_list = Directory(path).index_directory(file=True)

        extension_keys = Config.get("file_extensions")

        for specific_key in sorted(extension_keys):
            for extension in Config.get("file_extensions." + specific_key):
                files = analysis_path.find_specific_file(extension, self.file_list, case_sensitive=False)
                data.update({extension: (len(files), files)})

            self.directory_data.update({'file_list': data})

        self.directory_data.update({'photo': sorted(analysis_path.index_photo_directory(return_folders=True).values())})
        self.directory_data.update({'size': sizeof_fmt(Directory(path).get_directory_size())})

        return self.directory_data

    def export(self):
        self.fetch_data_destination_path()
        self.packaged_data = {}

        if type(self.path) != list:
            self.path = [self.path]

        for directory in self.path:
            self.packaged_data.update({self.path.index(directory) + 1: self.datafy(directory)})
        # check if any directories were found, if none found, then exit
        if self.packaged_data == {}:

            print('zero instances of photo directories found.')
            File(self.destination_file).clean()
            exit()
        else:
            File(self.destination_file).write(self.packaged_data)


class Table:
    def __init__(self, max_instances=5, max_size=30):
        self.max_rows = max_instances
        self.data_packets = 0
        self.path_size = max_size
        self.file_location = Config.join_specific_data('application_root', 'application_directories.size_data')
        self.import_data = File(self.file_location).read("dict")
        self.readable_size = []
        self.all_rows = []
        self.row = []
        self.destination_file = ''

        # data import
        self.data_packets = int(len(self.import_data.keys()))
        for i in range(self.data_packets):
            if not i + 1 <= self.max_rows:
                dict(self.import_data).pop(i)

        # table init and settings
        self.table = PrettyTable()
        self.table.border = False
        self.table.field_names = ["ID", "Path", "crt", "dng", "tif", "jpg"]
        self.table.align = "l"
        self.border_symbol = "-"

    def __str__(self):
        return str(self.table)

    def get(self, req):
        specific_data = []
        for data in list(self.import_data.values()):
            specific_data.append(global_get(data, req))

        return specific_data

    def make_row(self, key):
        self.row = [key]
        if self.path_size <= len(list(self.import_data[key].get('path'))):
            self.row.append(shorten(self.import_data[key].get('path')))
        else:
            self.row.append(self.import_data[key].get('path'))
        data = self.import_data[key].get('file_list')
        for item in data.values():
            self.row.append(item[0])

        size_data = self.import_data[key].get('size')
        readable_size = []

        if size_data[0] == 0:
            readable_size.append("0Kb")
        else:
            # array position 1 stores the human readable value
            readable_size.append(size_data[1])

        self.readable_size.extend(readable_size)
        return self.row

    def from_id(self, _id):
        if self.import_data == {}:
            super(self.__init__)

        try:
            return self.import_data.get(_id)
        except KeyError:
            raise Fatal('System tried to load a non-existent part of the results table', True,
                        'id=%s' % _id,
                        'data=%s' % self.import_data)

    @staticmethod
    def __calculate_border_size(data, use_string=False):
        return data + 1 if data >= 4 else len(str(data)) + 2 if use_string else 4

    def border(self):
        borders = []
        border_data = []

        for item in self.import_data[1].get('file_list').items():
            border_data.append(self.__calculate_border_size(
                largest_element(to_string([x[0] for x in self.get("file_list.'%s'" % item[0])]))))

        for i in border_data:
            borders.append(self.border_symbol * int(i))

        for i in reversed(range(self.path_size - 4)):
            if largest_element(self.get('path')) + i < self.path_size:
                self.path_size -= i
                break

        self.row = [self.__calculate_border_size(self.max_rows, True) * self.border_symbol,
                    (self.path_size + 1) * self.border_symbol]
        self.row.extend(borders)
        self.table.add_row(self.row)

        del self.row

    def make_table(self):
        for i in range(1, self.data_packets + 1):
            self.all_rows.append(self.make_row(i))

        self.border()
        [self.table.add_row(row) for row in self.all_rows]

        self.readable_size.insert(0, self.border_symbol * self.__calculate_border_size(
            largest_element(self.readable_size)))
        self.table.add_column("size", self.readable_size, align="r")
