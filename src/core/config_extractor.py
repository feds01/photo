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

    def join_specific_data(self, key1, key2):
        return self.get(key1) + self.get(key2)

    def get(self, req):
        keys = req.split('.')
        data = self._raw_data
        for key in keys:
            if key in data.keys():
                data = data.get(key)
                continue
            else:
                Fatal('config is unreadable', True, 'key was not found, but expected', 'key=%s' % req)
        try:
            return data.keys()
        except Exception:
            return data


Config = _Config()
del _Config