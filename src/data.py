#!C:\Python\Python36\python.exe
from prettytable import PrettyTable

from src.core.core import *
from src.utilities.shorts import *
from src.utilities.manipulation import sizeof_fmt
from src.utilities.arrays import organise_array, largest_element, to_string

__author__ = "Alexander Fedotov <alexander.fedotov.uk@gmail.com>"
__company__ = "(C) Wasabi & Co. All rights reserved."


class Table:
    def __init__(self):
        self.file = File(Config.join('application_root', 'session'))
        self.data = {}
        self.row_count = 0

        # table init and settings
        self.border_symbol = "-"
        self.table = PrettyTable()

        self.import_data()

    def __str__(self):
        return str(self.table)

    def create_data(self, directories, ret=False):
        # reset directories data just in case
        self.data['directories'] = {}

        if type(directories) == str:
            directories = [directories]

        for pos, directory in enumerate(directories):
            self.data["directories"].update({str(pos + 1): self.instantiate(directory)})

        self.truncate_data(), self.export_data()

        if ret:
            return self.data["directories"]

    def truncate_data(self):
        # data truncation
        self.row_count = int(len(self.data['directories']))

        if Config.get("table_records") != -1:
            for i in range(self.row_count):
                if not i + 1 <= Config.get("table_records"):
                    self.data["directories"].pop(i)

    def get(self, req):
        specific_data = []
        for data in list(self.data["directories"].values()):
            specific_data.append(global_get(data, req))

        return specific_data

    def from_id(self, _id):
        if self.data == {}:
            super(self.__init__)

        try:
            return self.data["directories"].get(f"{_id}")
        except KeyError:
            raise Fatal('System tried to load a non-existent part of the results table',
                        'id=%s' % _id,
                        'data=%s' % self.data["directories"]).stop()

    def init_table(self):
        self.table = PrettyTable()
        self.table.border = False

    def make_table(self):
        # re-initialise the variable
        self.init_table()

        data_queries = {
            'path': 'path',
            'crt': "file_list.'.CR2'.amount",
            'dng': "file_list.'.dng'.amount",
            'tif': "file_list.'.tif'.amount",
            'jpg': "file_list.'.jpg'.amount",
            'size': 'size',
            'indexed': 'path'
        }

        # we can easily add the id column, padding of 2 from actual digit
        border = self.border_length(str(self.row_count), padding=2) * self.border_symbol

        self.table.add_column('id', organise_array([border, list(range(1, self.row_count + 1))]), align='l')

        for query in data_queries.keys():
            results = [x for x in self.get(data_queries.get(query))]

            if query == "path":
                results = [shorten(x, Config.get("path_length")) for x in results]

            elif query == "size":
                results = [x[1] for x in results]

            elif query == "indexed":
                results = [Blacklist.is_completed(x) for x in results]

            results = to_string(results)
            border = self.border_length(largest_element(results)) * self.border_symbol

            self.table.add_column(query, organise_array([border, results]), align='l')

    def import_data(self):
        self.data = self.file.read_json()

    def export_data(self):
        self.file.write_json(self.data, indent=None)

    @staticmethod
    def border_length(item, padding=3):
        # get the item size, works with string only
        # add the amount of padding
        # this is for making the table look and feel well spaced
        return len(item) + padding

    @staticmethod
    def instantiate(path):
        directory = Directory(path)

        data = {'path': path}
        file_stats = {}
        file_count = 0

        for specific_key in sorted(Config.get("file_extensions")):
            for extension in Config.get("file_extensions." + specific_key):
                files = list(filter(lambda x: x[-4:] in [extension, extension.upper()], index(path, file=True)))

                file_stats.update({extension: {"amount": len(files)}})
                file_count += len(files)

            data.update({'file_list': file_stats, 'file_count': file_count})

        data.update({'photo': sorted(directory.index_photo_directory(return_folders=True).values())})
        data.update({'size': sizeof_fmt(directory_size(path))})

        return data