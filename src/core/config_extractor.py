import yaml
from src.core.exceptions import *
from src.utilities.shorts import global_get
from src.config_manager import get_config_file_location

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

    def join_specific_data(self, key1, key2):
        return self.get(key1) + self.get(key2)

    def get(self, req):
        return global_get(self._raw_data, req)


Config = _Config()
del _Config