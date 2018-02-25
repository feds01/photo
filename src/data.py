#!C:\Python\Python36\python.exe
# import time
from src.core.core import *
from prettytable import PrettyTable

from src.utilities.session import close_session
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
        self.file = File(Config.join('application_root', 'session'))
        self.dirapi = Directory(path)

        # just in case only one directory was passed for processing
        if type(self.path) != list:
            self.path = [self.path]

    def load(self):
        data = self.file.read_json()
        data.update({"directories": {}})

        return data

    def datafy(self, path):
        self.dirapi.set_path(path)

        data = {}
        file_list = {}
        file_count = 0
        data.update({'path': path})

        for specific_key in sorted(Config.get("file_extensions")):
            for extension in Config.get("file_extensions." + specific_key):
                files = find_specific_file(extension, index(path, file=True), case_sensitive=False)
                file_list.update({extension: {"amount": len(files), "files": files}})
                file_count += len(files)

            data.update({'file_list': file_list})
            data.update({'file_count': file_count})

        data.update({'photo': sorted(self.dirapi.index_photo_directory(return_folders=True).values())})
        data.update({'size': sizeof_fmt(directory_size(path))})

        return data

    def export(self):
        loaded_data = self.load()
        counter = 1

        for directory in self.path:
            loaded_data["directories"].update({counter: self.datafy(directory)})
            counter += 1
        # check if any directories were found, if none found, then exit
        if len(loaded_data["directories"]) == 0:
            print('zero instances of photo directories found.')
            close_session()
        else:
            self.file.write_json(loaded_data, indent=None)


class Table:
    def __init__(self, max_size=30):
        self.path_size = max_size
        self.file = File(Config.join('application_root', 'session'))
        self.readable_size = []

        # data import
        self.import_data = self.file.read_json()
        self.import_data.update({"table": []})
        self.row_count = int(len(self.import_data['directories']))

        if Config.get("table_records") != -1:
            for i in range(self.row_count):
                if not i + 1 <= Config.get("table_records"):
                    dict(self.import_data).pop(i)

        # table init and settings
        self.table = PrettyTable()
        self.table.border = False
        self.table.field_names = ["id", "path", "crt", "dng", "tif", "jpg"]
        self.table.align = "l"
        self.border_symbol = "-"

    def __str__(self):
        return str(self.table)

    def get(self, req):
        specific_data = []
        for data in list(self.import_data["directories"].values()):
            specific_data.append(global_get(data, req))

        return specific_data

    def make_row(self, key):
        row = [key]

        if self.path_size <= len(list(self.import_data["directories"][f"{key}"].get('path'))):
            row.append(shorten(self.import_data["directories"][f"{key}"].get('path')))
        else:
            row.append(self.import_data["directories"][f"{key}"].get('path'))
        data = self.import_data["directories"][f"{key}"].get('file_list')
        for item in data.values():
            row.append(item["amount"])

        size_data = self.import_data["directories"][f"{key}"].get('size')
        readable_size = []

        if size_data[0] == 0:
            readable_size.append("0Kb")
        else:
            # array position 1 stores the human readable value
            readable_size.append(size_data[1])

        self.readable_size.extend(readable_size)

        return row

    def from_id(self, _id):
        if self.import_data == {}:
            super(self.__init__)

        try:
            return self.import_data["directories"].get(f"{_id}")
        except KeyError:
            raise Fatal('System tried to load a non-existent part of the results table',
                        'id=%s' % _id,
                        'data=%s' % self.import_data["directories"]).stop()

    @staticmethod
    def __calculate_border_size(data, use_string=False):
        return data + 1 if data >= 4 else len(str(data)) + 2 if use_string else 4

    def border(self):
        borders = []
        border_data = []

        for item in self.import_data["directories"]["1"].get('file_list').items():
            border_data.append(self.__calculate_border_size(
                largest_element(to_string([x for x in list(self.get("file_list.'%s'.amount" % item[0]))]))))

        for i in border_data:
            borders.append(self.border_symbol * int(i))

        for i in reversed(range(self.path_size - 4)):
            if largest_element(self.get('path')) + i < self.path_size:
                self.path_size -= i
                break

        row = [self.__calculate_border_size(Config.get("table_records"), True) * self.border_symbol,
               (self.path_size + 1) * self.border_symbol]

        row.extend(borders)
        self.table.add_row(row)

    def make_table(self):
        rows = []

        for i in range(1, self.row_count + 1):
            rows.append(self.make_row(i))

        self.border()
        [self.table.add_row(row) for row in rows]

        # save to session file
        self.import_data.update({"table": rows})
        self.file.write_json(self.import_data, indent=None)

        self.readable_size.insert(0, self.border_symbol * self.__calculate_border_size(
            largest_element(self.readable_size)))
        self.table.add_column("size", self.readable_size, align="r")
