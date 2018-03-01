import subprocess

from src.core.config import *
from src.core.config import Config
from src.core.exceptions import Fatal
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


def check_process_count(v=True, ret=False):
    process_count = os.cpu_count() * Config.get('thread.instance_multiplier')

    if process_count <= 0:
        Fatal('process count cannot be %s' % process_count,
              'incorrect config magic process number of %s' % process_count,
              'instance_multiplier=%s' % (process_count / os.cpu_count())).stop()
    elif process_count >= 32:
        if not v:
            do_warning('thread', 'magic process number is extremely large.', 'count=%s' % process_count)

    if type(process_count) != int:
        try:
            if round(process_count, 0) == process_count:
                process_count = int(process_count)
            else:
                Fatal('process count cannot be float.', 'incorrect config magic process number of %s' %
                      (process_count / os.cpu_count())).stop()
        except TypeError as error:
            Fatal('process count cannot be float.', 'incorrect config magic process number of %s' %
                  process_count, 'incorrect type: %s' % type(process_count), '%s' % error).stop()
        if not v:
            do_warning('thread', 'magic process instance multiplier number was processed as float.')

    return process_count if ret else True
