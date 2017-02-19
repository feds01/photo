import time
import subprocess
from src.thread_indexer import *

__author__ = "Alexander Fedotov <alexander.fedotov.uk@gmail.com>"
__company__ = "(C) Wasabi & Co. All rights reserved."

"""
Module name: cli_helpers.py
Usage:
Description -

"""


def load_file_info(path):
    size = get_appropriate_units(Directory(path).get_file_size())
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


def loader(data):
    instance_leaves = {}
    file_count = 0
    for directory in data[1]:
        instance_leaves.update({os.path.basename(directory): Directory(directory).index_directory(count=True, file=True)})
    data.pop(1)
    print("More detail about the photo directory - '" + os.path.basename(data[0]) + "' :\n")
    print("Full directory path: ", data[0])
    for i in range(1, 5):
        file_count += data[i]
    print("Total files:", file_count)
    print(fancy_tree_display(list(instance_leaves.keys()), list(instance_leaves.values())))
    print("Total directory size: " + str(data[-1][0]) + " " + data[-1][1])


def open_file(file):
    subprocess.Popen(['C:\\Windows\\explorer.exe', file], shell=True)


def prompt_user(message, excepted_input):
    user_input = ''
    while user_input not in excepted_input:
        user_input = input(message).lower()
    return user_input


def select_files(files):
    files = sorted(files.values())
    blocked_files = []
    for file in files:
        current_file = True
        while current_file:
            delete_confirmation = input("Are you sure you want to delete '" + file + "' [Y/n]?").lower()
            if delete_confirmation == "y":
                current_file = False
            elif delete_confirmation == "n":
                    blocked_files.append(file)
                    print("canceled deletion")
                    current_file = False
            elif delete_confirmation.isspace() or delete_confirmation == "":
                pass
            elif delete_confirmation == ":open":
                open_file(file)
            elif delete_confirmation == ":info":
                load_file_info(file)
            elif delete_confirmation == ":stop":
                return "stop"
    for file in blocked_files:
        files.remove(file)
    return files