import yaml
from src.config_manager import get_config_file_location

__author__ = "Alexander Fedotov <alexander.fedotov.uk@gmail.com>"
__company__ = "(C) Wasabi & Co. All rights reserved."


class _Config:
    def __init__(self):
        self._raw_data = self.retrieve_config()
        self.config_raw_data = {}
        self.key_list = []
        self.data = {}

    @staticmethod
    def retrieve_config():
        try:
            return yaml.load(open(get_config_file_location(), "r"))
        except Exception as exc:
            print(exc)

    def retrieve_data(self, key):
        for data_group_key in self.get_key_value(key):
            self.data.update({data_group_key: self.get_key_value(key)[data_group_key]})
        return self.data

    def get_specific_data(self, key, specific):
        self.retrieve_data(key)
        return self.data[specific]

    def get_key_value(self, key):
        return self._raw_data.get(key)

    def get_specific_keys(self, key):
        return list(self._raw_data.get(key).keys())


Config = _Config()
del _Config