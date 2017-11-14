from src.core.core import *
from src.utilities.manipulation import sizeof_fmt, swap_extension

__author__ = "Alexander Fedotov <alexander.fedotov.uk@gmail.com>"
__company__ = "(C) Wasabi & Co. All rights reserved."

"""
Module name: cleaner.py
Usage:
Description -

"""


class Analyse:
    def __init__(self, directory):
        self.directory = directory
        self.directories = {}
        self.report = {}
        self.files = []
        self.organise_nodes()

    def organise_nodes(self):
            directories = Directory(self.directory).index_photo_directory(return_folders=True)
            keys = list(directories.keys())
            for key in keys:
                if re.fullmatch(Config.get("folders.crt.pattern"), key):
                    self.directories.update({'crt': directories.get(key)})
                if re.fullmatch(Config.get("folders.all.pattern"), key):
                    self.directories.update({'all': directories.get(key)})
                else:
                    self.directories.update({'good': directories.get(key)})

    def find_files(self):
        all_files = Directory(self.directories.get('all')).index_directory(file=True)
        good_files = Directory(self.directories.get('good')).index_directory(file=True)
        for file in all_files:
            if file not in good_files:
                self.files.append(file)
            else:
                pass

    def find_crt_files(self):
        crt_files = Directory(self.directories.get('crt')).index_directory(file=True)
        crt_extensions = Config.get("file_extensions.crt")
        for file in self.files:
            crt_version = []
            for extension in crt_extensions:
                crt_version.append(swap_extension(self.path_converter(file), extension, remove_dot=True))
            for crt_file in crt_version:
                if crt_file in crt_files:
                    self.report.update({file: crt_file})

    def path_converter(self, path):
            return os.path.join(self.directories.get('crt'), os.path.basename(path))

    def run_analysis(self):
        self.find_files()
        self.find_crt_files()
        return self.report


class Delete:
    def __init__(self, delete, silent=False):
        self.silent = silent
        self.delete_list = delete
        self.total_size = 0
        self.file_path = ""

    def calculate_size(self):
        for file in self.delete_list:
            self.total_size += Directory(file).get_file_size()

    def delete_file(self):
        file_size = Directory(self.file_path).get_file_size()
        if not self.silent:
            file_info = sizeof_fmt(file_size)
            print(f"deleting: {os.path.basename(self.file_path)} size: {str(file_info[1])}")
        try:
            os.remove(self.file_path)
        except Exception as e:
            Fatal(f"could not remove file {self.file_path}", False, 'error=%s' % e)
            self.total_size -= file_size

    def deletion_manager(self):
        self.calculate_size()
        for file in self.delete_list:
            self.file_path = file
            self.delete_file()
        self.total_size = sizeof_fmt(self.total_size)
        print(f"saved: {self.total_size[1]} of disk space with operation.")
        return True
