#!C:\Python\Python36\python.exe
from src.core.core import *
from prettytable import PrettyTable

from src.utilities.shorts import *
from src.utilities.arrays import organise_array
from src.utilities.session import close_session
from src.utilities.manipulation import to_string, largest_element, sizeof_fmt

__author__ = "Alexander Fedotov <alexander.fedotov.uk@gmail.com>"
__company__ = "(C) Wasabi & Co. All rights reserved."


class Data:
    def __init__(self, path):
        self.path = path
        self.file = File(Config.join('application_root', 'session'))
        self.dirapi = Directory(path)

        # just in case only one directory was passed for processing
        if type(self.path) != list:
            self.path = [self.path]

    def datafy(self, path):
        self.dirapi.set_path(path)

        data = {'path': path}
        file_list = {}
        file_count = 0

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
        loaded_data = {"directories": {}}
        counter = 1

        for directory in self.path:
            loaded_data["directories"].update({counter: self.datafy(directory)})
            counter += 1
        # check if any directories were found, if none found, then exit
        if len(loaded_data["directories"]) == 0:
            print('zero instances of photo directories found.')
            close_session()
        else:
            data = self.file.read_json()
            data.update(loaded_data)

            self.file.write_json(data, indent=None)


class Table:
    def __init__(self, max_size=30):
        self.max_size = max_size
        self.file = File(Config.join('application_root', 'session'))

        # data import
        self.import_data = self.file.read_json()

        # data truncation
        self.row_count = int(len(self.import_data['directories']))

        if Config.get("table_records") != -1:
            for i in range(self.row_count):
                if not i + 1 <= Config.get("table_records"):
                    dict(self.import_data).pop(i)

        # table init and settings
        self.table = PrettyTable()
        self.table.border = False
        self.border_symbol = "-"

        # we can easily add the id column, padding of 2 from actual digit
        border = self.border_length(str(self.row_count), padding=2) * self.border_symbol

        self.table.add_column('id', organise_array([border, list(range(1, self.row_count + 1))]), align='l')

    def __str__(self):
        return str(self.table)

    def get(self, req):
        specific_data = []
        for data in list(self.import_data["directories"].values()):
            specific_data.append(global_get(data, req))

        return specific_data

    def from_id(self, _id):
        if self.import_data == {}:
            super(self.__init__)

        try:
            return self.import_data["directories"].get(f"{_id}")
        except KeyError:
            raise Fatal('System tried to load a non-existent part of the results table',
                        'id=%s' % _id,
                        'data=%s' % self.import_data["directories"]).stop()

    def make_table(self):
        data_queries = {
            'path': 'path',
            'crt': "file_list.'.CR2'.amount",
            'dng': "file_list.'.dng'.amount",
            'tif': "file_list.'.jpg'.amount",
            'size': 'size'
        }

        for query in data_queries.keys():
            results = [x for x in self.get(data_queries.get(query))]

            if query == "path":
                results = [shorten(x, self.max_size) for x in results]

            if query == "size":
                results = [x[1] for x in results]
                border = self.border_length(largest_element(results), padding=1) * self.border_symbol

                self.table.add_column(query, organise_array([border, results]), align='r')
                continue
            else:
                results = to_string(results)
            border = self.border_length(largest_element(results)) * self.border_symbol

            self.table.add_column(query, organise_array([border, results]), align='l')

    @staticmethod
    def border_length(item, padding=3):
        # get the item size, works with string only
        # add the amount of padding
        # this is for making the table look and feel well spaced
        return len(item) + padding