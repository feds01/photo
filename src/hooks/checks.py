from src.core.core import *
from src.hooks.blacklist_query import *


def check_directory(path):
    if not Directory(path).check_directory():
        raise Fatal("directory does not exist", False, 'directory= %s' % path)
    if run_blacklist_check(path, child=True):
        raise Fatal("directory is blacklisted.", False, 'directory=%s' % path)
    else:
        return