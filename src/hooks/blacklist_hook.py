from src.blacklist import *

__author__ = "Alexander Fedotov <alexander.fedotov.uk@gmail.com>"
__company__ = "(C) Wasabi & Co. All rights reserved."

"""
Module name: blacklist_hook.py
Usage:
Description -

"""


def certify_index_results(results):
    directories = Utility().list_organiser(Blacklist(results, directory="").run_blacklist_check())
    for _dir in directories:
        results.remove(_dir)
    return results
