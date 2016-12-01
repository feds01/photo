from src.utils import *


class Blacklist:
    def __init__(self, directory, *args):
        self.black_list_type = list(*args)
        self.directory = directory
        self.black_list = []
        self.file_location = Directory(__file__).get_artifact_file_location("blacklist.txt")
        self.black_list_instance = {}
        self.symbol = ""

    def package_directory(self):
        self.black_list_instance = {}
        self.black_list_instance.update({self.directory: self.black_list_type})

    def create_instance(self):
        self.package_directory()
        with open(self.file_location, "r") as file:
            if not file.readlines():
                pass
            else:
                self.symbol = "\n"
            file.close()
        with open(self.file_location, "a") as file:
            file.write(self.symbol + str(self.black_list_instance)), file.close()

