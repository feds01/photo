import os
from src.core.exceptions import *

def handle_fdreq(path, silent_mode=False):
    try:
        return list(os.listdir(path))

    except Exception as e:
        if silent_mode:
            pass
        else:
            if e is PermissionError:
                IndexingError(path, 'permissions')

            # covers weird windows hidden folder mechanics
            if e is FileNotFoundError:
                IndexingError(path, 'un-loadable')

        return []