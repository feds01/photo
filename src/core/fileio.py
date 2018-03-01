import json
from src.core.config import *

__author__ = "Alexander Fedotov <alexander.fedotov.uk@gmail.com>"
__company__ = "(C) Wasabi & Co. All rights reserved."


def check_file(path):
    return os.path.isfile(path)


def file_size(file, unit=1):
        return os.path.getsize(file) / unit


def get_filename(path, rp=False):
    split_path = os.path.split(path)
    return split_path if rp else split_path[1]


class File:
    def __init__(self, file=""):
        self.file = file

    def set_file(self, file):
        self.__init__(file)

    def write_json(self, data, indent=4):
        with open(self.file, "w") as f:
            json.dump(data, f, indent=indent)
            f.close()

    def read_json(self):
        if not check_file(self.file):
            do_warning('file', "given file does not exist", 'file=%s' % self.file)
            return {}

        with open(self.file, "r") as f:
            data = json.load(f)
            f.close()

        return {} if data is None else data
