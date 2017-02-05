from src.core.utils import *

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
        self.all_files = []
        self.good_files = []
        self.crt_extensions = Config.get_specific_data("file_extensions", "crt")
        self.organise_nodes()

    def organise_nodes(self):
            directories = Directory(self.directory).index_photo_directory(return_folders=True)
            keys = list(directories.keys())
            for key in keys:
                if key in Config.get_specific_data("folders", "crt_folder_name"):
                    self.directories.update({'crt': directories.get(key)})
                if key in Config.get_specific_data("folders", "all_folder_name"):
                    self.directories.update({'all': directories.get(key)})
                else:
                    self.directories.update({'good': directories.get(key)})

    def find_files(self):
        self.all_files = Directory(self.directories.get('all')).index_directory(file=True)
        self.good_files = Directory(self.directories.get('good')).index_directory(file=True)
        for file in self.all_files:
            if file not in self.good_files:
                self.files.append(file)
            else:
                pass

    def find_crt_files(self):
        crt_files = Directory(self.directories.get('crt')).index_directory(file=True)
        for file in self.files:
            crt_version = []
            for extension in self.crt_extensions:
                crt_version.append(extension_swapper(self.path_converter(file), extension, remove_dot=True))
            for version in crt_version:
                if version in crt_files:
                    self.report.update({file: version})
                else:
                    continue

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
        self.saved_space = ""
        self.file_path = ""
        self.file_info = ""
        self.file_name = ""

    def calculate(self):
        for file in self.delete_list:
            self.total_size += Directory(file).get_file_size()

    def delete_file(self):
        file_size = Directory(self.file_path).get_file_size()
        if not self.silent:
            self.file_info = Directory(file_size).get_appropriate_units()
            print("deleting: " + self.file_name, "size:", str(self.file_info[0]) + self.file_info[1])
        try:
            os.remove(self.file_path)
        except Exception as e:
            Fatal("could not remove file %s" % self.file_path, False, 'error=%s' % e)
            self.total_size -= file_size

    def deletion_manager(self):
        self.calculate()
        for file in self.delete_list:
            self.file_path = file
            self.file_name = os.path.basename(self.file_path)
            self.delete_file()
        self.total_size = Directory(self.total_size).get_appropriate_units()
        self.saved_space = '%s%s' % (self.total_size[0], self.total_size[1])
        return "saved: %s of disk space with operation." % self.saved_space
