import yaml
from src.config_manager import get_config_file_location

config_file_location = get_config_file_location(__file__)

class Config:
    def __init__(self):
        self.stream = ""
        self.raw_data = {}
        self.config_raw_data = {}
        self.key_list = []
        self.data = {}
        self.retrieve_config()

    def retrieve_config(self):
        with open(config_file_location, "r") as self.stream:
            try:
                self.raw_data = yaml.load(self.stream)
                return self.raw_data
            except Exception as exc:
                print(exc)

    def clean_raw_data(self, exception_key):
        self.key_list = sorted(list(self.raw_data))
        for key in self.key_list:
            if key == self.key_list[exception_key]:
                pass
            else:
                self.raw_data.pop(key)


    def retrieve_data(self, key):
        self.get_config_keys()
        self.clean_raw_data(self.key_list.index(key))
        for data_group_key in self.get_key_value(key):
            self.data.update({data_group_key: self.get_key_value(key)[data_group_key]})
        return self.data

    def get_specific_data(self, key, specific):
        self.retrieve_data(key)
        return self.data[specific]

    def get_config_keys(self):
        self.key_list = sorted(list(self.raw_data))
        return self.key_list

    def get_key_value(self, key):
        return self.raw_data.get(key)

    def get_specific_keys(self, key):
        self.get_config_keys()
        return self.raw_data[self.key_list[self.key_list.index(key)]].keys()
