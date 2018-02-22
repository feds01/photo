from src.core.config import *
from src.utilities.arrays import organise_array

__author__ = "Alexander Fedotov <alexander.fedotov.uk@gmail.com>"
__company__ = "(C) Wasabi & Co. All rights reserved."


# specific function for listing a directories contents
def handle_fdreq(path):
    try:
        return [x.name for x in os.scandir(path)]

    except Exception as e:
        if not Config.get_session("verbose"):
            if e is PermissionError:
                IndexingError(path, 'permissions')

            # covers weird windows hidden folder mechanics
            if e is FileNotFoundError:
                IndexingError(path, 'un-loadable')

        return []


# convert base-names to paths
def to_path(root, arr):
        return map(lambda x: os.path.join(root, x), arr)


def to_structure(root, structure):
    make_list = []

    for item in structure:
        sub = os.path.join(root, item)
        if not os.path.exists(sub):
            make_list.append(sub)

        if type(structure.get(item)) == dict:
            make_list.extend(to_structure(os.path.join(root, item), structure.get(item)))

        if type(structure.get(item)) == list:
            items = organise_array(structure.get(item))
            for node in items:
                if type(node) == dict:
                    make_list.extend(to_structure(os.path.join(root, item), node))
                else:
                    make_list.append(os.path.join(root, item, node))
        else:
            if structure.get(item) != "":
                make_list.append(os.path.join(root, item, structure.get(item)))

    return make_list