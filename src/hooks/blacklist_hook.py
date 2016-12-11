from src.blacklist import *

__author__ = "Alexander Fedotov <alexander.fedotov.uk@gmail.com>"
__company__ = "(C) Wasabi & Co. All rights reserved."


def certify_index_results(results):
    directories = Blacklist(results).run_blacklist_check()
    for _dir in directories:
        results.remove(_dir)
    return results
