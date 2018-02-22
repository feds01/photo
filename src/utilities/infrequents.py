from src.core.config import *
from src.utilities.arrays import organise_array

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