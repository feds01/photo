import subprocess

from src.core.config import *
from src.core.config import Config
from src.core.exceptions import Fatal, config_warning
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


def open_file(path):
    subprocess.Popen(['C:\\Windows\\explorer.exe', path], shell=True)


def is_child(child, directory, symlinks=False):
    directory = os.path.abspath(directory)
    child = os.path.abspath(child)
    if not symlinks and os.path.islink(child):
        return False
    return os.path.commonprefix([child, directory]) == directory


def check_process_count(v=True, return_pnum=False):
    _raw_value = os.cpu_count() * Config.get('thread.instance_multiplier')

    if _raw_value <= 0:
        Fatal('process count cannot be %s' % _raw_value,
              'incorrect config magic process number of %s' % _raw_value,
              'instance_multiplier=%s' % (_raw_value / os.cpu_count())).stop()
    elif _raw_value >= 32:
        if not v:
            config_warning('magic process number is extremely large.')
        else:
            pass

    if type(_raw_value) != int:
        try:
            if round(_raw_value, 0) == _raw_value:
                _raw_value = int(_raw_value)
            else:
                Fatal('process count cannot be float.', 'incorrect config magic process number of %s' %
                  (_raw_value / os.cpu_count())).stop()
        except TypeError as error:
            Fatal('process count cannot be float.', 'incorrect config magic process number of %s' %
                  _raw_value, 'incorrect type: %s' % type(_raw_value), '%s' % error).stop()
            if not v:
                config_warning('magic process instance multiplier number was processed as float.')

    return _raw_value if return_pnum else True