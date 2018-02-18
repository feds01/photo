import os
from src.core.config import *


def handle_fdreq(path):
    try:
        return list(os.listdir(path))

    except Exception as e:
        if Config.get_session("verbose"):
            pass
        else:
            if e is PermissionError:
                IndexingError(path, 'permissions')

            # covers weird windows hidden folder mechanics
            if e is FileNotFoundError:
                IndexingError(path, 'un-loadable')

        return []