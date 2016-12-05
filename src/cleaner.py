from src.utils import *
from src.config_extractor import *

__author__ = "Alexander Fedotov <alexander.fedotov.uk@gmail.com>"
__company__ = "(C) Wasabi & Co. All rights reserved."


class Analyse:
    def __init__(self, directory, safe=False):
        self.directory = directory
        self.safe = safe
        self.files = []
        self.constructed_report = {}
        self.crt_file_version = []
        self.crt_path_files = []
        self.directory_folders = []
        self.all_folder_files, self.good_folder_files, self.crt_folder_files = [], [], []
        self.crt_folder_names = Config().get_specific_data("folders", "crt_folder_name")
        self.all_folder_names = Config().get_specific_data("folders", "all_folder_name")
        self.crt_extensions = Config().get_specific_data("file_extensions", "crt")
        self.directory_subs = Directory(self.directory).index_photo_directory(return_folders=True)
        self.subdirectory_sorter()

    def subdirectory_sorter(self):
            # TODO: clean-up
            for directory in self.directory_subs:
                for folder_name in self.crt_folder_names:
                    if os.path.basename(directory) == folder_name:
                        self.directory_folders.append(directory)
                        self.directory_subs.remove(directory)
            for directory in self.directory_subs:
                for folder_name in self.all_folder_names:
                    if os.path.basename(directory) == folder_name:
                        self.directory_folders.append(directory)
                        self.directory_subs.remove(directory)
            self.directory_folders = Utility().join_lists(self.directory_folders, self.directory_subs)
            del self.directory_subs

    def file_finder(self):
        self.all_folder_files = Directory(self.directory_folders[1]).index_directory(file=True)
        self.good_folder_files = Directory(self.directory_folders[2]).index_directory(file=True)
        for file in self.all_folder_files:
            if file not in self.good_folder_files:
                self.files.append(file)
            else:
                pass

    def path_converter(self, path):
            return os.path.join(self.directory_folders[0], os.path.basename(path))

    def crt_file_finder(self):
        self.crt_folder_files = Directory(self.directory_folders[0]).index_directory(file=True)
        for file in self.files:
            self.crt_file_version = []
            for extension in self.crt_extensions:
                self.crt_file_version.append(Utility().extension_swapper(self.path_converter(file), extension, remove_dot=True))
            for version in self.crt_file_version:
                if version in self.crt_folder_files:
                    self.constructed_report.update({file: version})
                else:
                    pass

    def run_analysis(self):
        self.file_finder()
        self.crt_file_finder()
        return self.constructed_report

print(Analyse("E:\\Files\\Ana Felix Snow Queen\\").run_analysis())
print(Analyse("E:\\Files\\Ana Felix Forest First\\").run_analysis())

