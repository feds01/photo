import os
from src.utils import *
from src.data import Table


def fancy_tree_display(roots, values):
    full_string, tree_symbol = "", "|_ "
    max_root = Cleaner().get_largest_element(roots)
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
        instance_leaves.update({os.path.basename(directory): Directory(directory).index_directory(count=True, file=True)})
    instance_data.pop(1)
    print("More detail about the photo directory - '" + os.path.basename(instance_data[0]) + "' :", space(1))
    print("Full directory path: ", instance_data[0])
    for i in range(1, 5):
        file_count += instance_data[i]
    print("Total files:", file_count)
    print(fancy_tree_display(list(instance_leaves.keys()), list(instance_leaves.values())),)
    print("Total directory size: " + str(instance_data[-1][0]) + " " + instance_data[-1][1])


def table_selector(max_id, prefix="~$ "):
    print("Enter the ID of the directory or enter the path of the directory to continue: ")
    dirs = []
    for i in range(1, max_id):
        dirs.append(Table().load_instance_by_id(i)[0])
    while True:
        scan_dir_input = input(prefix)
        try:
            scan_dir_input = int(scan_dir_input)
            if max_id < scan_dir_input or scan_dir_input < 0:
                print("The entered ID is too high or too low.")
            else:
                return safe_mode_selector(scan_dir_input, "path")
        except ValueError:
            try:
                if scan_dir_input[0] is ":":
                    if scan_dir_input[1:] == "paths":
                        for path in dirs:
                            print(path)
                    continue
            except IndexError:
                pass
            if scan_dir_input.isspace() or scan_dir_input == "":
                continue
            if scan_dir_input not in dirs:
                print("Entered directory path not present.")
            else:
                return safe_mode_selector(scan_dir_input, "path")


def safe_mode_selector(directory, pid):
    if pid == "path":
        pass
    else:
        directory = Table().load_instance_by_id(directory)
    while True:
        safe_scan_input = input("Scan the directory in safe mode [Y/n]? ").lower()
        if safe_scan_input == "y":
            return [directory, "--safe"]
        if safe_scan_input == "n":
            return [directory]
