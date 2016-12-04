from src.utils import *
from src.config_extractor import *

__author__ = "Alexander Fedotov <alexander.fedotov.uk@gmail.com>"
__company__ = "(C) Wasabi & Co. All rights reserved."


class Analyse:
    def __init__(self, directory):
        self.directory = directory
        self.directory_subs = Directory(self.directory).index_photo_directory(return_folders=True)
        self.directory_folders = []
        self.all_folder_names, self.crt_folder_names = [], []
        self.subdirectory_sorter()
        self.all_folder_files, self.good_folder_files, self.crt_folder_files = [], [], []

    def subdirectory_sorter(self):
            self.crt_folder_names = Config().get_specific_data("folders", "crt_folder_name")
            self.all_folder_names = Config().get_specific_data("folders", "all_folder_name")
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



Analyse("E:\\Files\\Ana Felix Snow Queen")
Analyse("E:\\Files\\Ana Felix Forest First")