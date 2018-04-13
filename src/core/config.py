import os

from yaml import load, dump, YAMLError
from src.core.exceptions import *
from src.utilities.shorts import global_get

__author__ = "Alexander Fedotov <alexander.fedotov.uk@gmail.com>"
__company__ = "(C) Wasabi & Co. All rights reserved."


class _Config:
    def __init__(self):
        self.data = self.retrieve_config()
        self.session = {}

    @staticmethod
    def retrieve_config():
        root = os.path.abspath(os.path.join(os.path.split(__file__)[0], "..\\..\\"))
        file = ""

        data = {
            'application_root': root,
            'folders': {
                'good': {'pattern': '(_|)[gG][oO]{2}[dD]'},
                'all':  {'pattern': '(_|)[aA][lL]{2}'},
                'crt':  {'pattern': '(_|)[dDcC][nNrR][gGtT]'}
            },
            'blacklist': {
                'enabled': False,
                'location': 'artifact\\blacklist.json'
            },
            'session': 'temp\\session.json',
            'thread': {
                'instance_multiplier': 1
            },
            'table_records': -1,
            'path_length': 30,
            'file_extensions': {'crt': ['.CR2', '.dng', '.tif'], 'good': ['.jpg']},
            'debug': True,
            'log_file': os.path.join(root, '\\temp\\photo.log')
        }

        try:
            file = os.path.join(root, "artifact\\config.yml")
            data = load(open(file, "r"))

        except FileNotFoundError:
            # alert the user there was a problem whilst trying to find config
            do_warning('config', f"missing configuration file")
            print("generating new file . . .", end="")

            with open(file, "w") as f:
                dump(data, f, indent=4)
                f.close()

            print("Success!\n")

        except YAMLError as e:
            Fatal('config file is unreadable.', 'Here is trace:\n\n%s' % e).stop()

        finally:
            # qualitative configuration checks, use global get to ensure that key actually exists)
            if global_get(data, "application_root")[-1:] != os.path.sep:
                data.update({"application_root": data.get("application_root") + os.sep})

            return data

    def join(self, key1, key2):
        return self.get(key1) + self.get(key2)

    def get(self, req):
        return global_get(self.data, req)

    def init_session(self, config):
        self.session = config

    def set_session(self, key, value):
        self.session.update({key: value})

    def get_session(self, key):
        return self.session.get(key)


Config = _Config()
del _Config
