import yaml
from src.config_manager import get_config_file_location
from src.core.exceptions import *

__author__ = "Alexander Fedotov <alexander.fedotov.uk@gmail.com>"
__company__ = "(C) Wasabi & Co. All rights reserved."


class _Config:
    def __init__(self):
        self._raw_data = self.retrieve_config()
        self.key_list = []
        self.data = {}

    @staticmethod
    def retrieve_config():
        try:
            return yaml.load(open(get_config_file_location(), "r"))
        except Exception as exc:
            yml_error(exc)

    def retrieve_data(self, key):
        for group_key in self.get_key_value(key):
            self.data.update({group_key: self.get_key_value(key)[group_key]})

    def get_specific_data(self, key, specific):
        self.retrieve_data(key)
        try:
            return self.data[specific]
        except Exception as exc:
            Fatal('config is unreadable', True, 'key was not found, but expected', 'key=%s' % exc)

    def get_key_value(self, key):
        return self._raw_data.get(key)

    def get_specific_keys(self, key):
        try:
            return list(self._raw_data.get(key).keys())
        except Exception as exc:
            Fatal('config is unreadable', True, 'key was not found, but expected', 'key=%s' % exc)

    def join_specific_data(self, key1, key2, key_subset):
        return self.get_key_value(key1) + self.get_specific_data(key2, key_subset)


Config = _Config()
del _Config