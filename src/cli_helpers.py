import time
from src.core.utils import *
from src.data import Table

__author__ = "Alexander Fedotov <alexander.fedotov.uk@gmail.com>"
__company__ = "(C) Wasabi & Co. All rights reserved."

"""
Module name: cli_helpers.py
Usage:
Description -

"""


def load_file_info(path):
    size = Directory(Directory(path).get_file_size()).get_appropriate_units()
    change_date = time.ctime(os.path.getctime(path))
    print("size:", str(size[0]) + size[1], " last modification:", change_date)


def fancy_tree_display(roots, values):
    full_string, tree_symbol = "", "|_ "
    max_root = get_largest_element(roots)
    for i in range(len(roots)):
        align = ""
        if len(roots[i]) < 5:
            align = " " * (max_root - len(roots[i]))
        full_string += tree_symbol + roots[i] + align + ": " + str(values[i]) + "\n"
    return full_string


def table_instance_display(instance_data):
    instance_leaves = {}
    file_count = 0
    for directory in instance_data[1]:
        instance_leaves.update({os.path.basename(directory): Directory(directory).index_directory(count=True,
                                                                                                  file=True)})
    instance_data.pop(1)
    print("More detail about the photo directory - '" + os.path.basename(instance_data[0]) + "' :", print_space(1))
    print("Full directory path: ", instance_data[0])
    for i in range(1, 5):
        file_count += instance_data[i]
    print("Total files:", file_count)
    print(fancy_tree_display(list(instance_leaves.keys()), list(instance_leaves.values())))
    print("Total directory size: " + str(instance_data[-1][0]) + " " + instance_data[-1][1])


def confirm_selection():
    confirmation = ''
    while confirmation not in ['y', 'n']:
        confirmation = input('Are you sure you want to continue? [Y/n] ').lower()
    if confirmation == 'y':
        return True
    else:
        return False


def loader(data):
    table_instance_display(data)


def select_files(files):
    crt_files = sorted(files.values())
    cancel_delete_files = []
    for file in crt_files:
        current_file = True
        while current_file:
            confirm_delete_input = input("Are you sure you want to delete '" + file + "' [Y/n]?").lower()
            if confirm_delete_input == "y":
                current_file = False
            elif confirm_delete_input == "n":
                    cancel_delete_files.append(file)
                    print("canceled deletion")
                    current_file = False
            elif confirm_delete_input.isspace() or confirm_delete_input == "":
                pass
            elif confirm_delete_input == ":open":
                command = "explorer.exe " + file
                os.popen(command)
            elif confirm_delete_input == ":info":
                load_file_info(file)
            elif confirm_delete_input == ":stop":
                return "stop"
    for file in cancel_delete_files:
        crt_files.pop(crt_files.index(file))
    return crt_files