import time
from src.core.utils import *
from src.data import Table

__author__ = "Alexander Fedotov <alexander.fedotov.uk@gmail.com>"
__company__ = "(C) Wasabi & Co. All rights reserved."


def load_file_info(path):
    size = Directory(Directory(path).get_file_size(1)).get_appropriate_units()
    change_date = time.ctime(os.path.getctime(path))
    print("size:", str(size[0]) + size[1], " last modification:", change_date)


def fancy_tree_display(roots, values):
    full_string, tree_symbol = "", "|_ "
    max_root = Utility().get_largest_element(roots)
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
    for i in range(1, max_id+1):
        dirs.append(Table().load_instance_by_id(i)[0])
    while True:
        scan_dir_input = input(prefix)
        try:
            scan_dir_input = int(scan_dir_input)
            if max_id < scan_dir_input or scan_dir_input < 0:
                print("The entered ID is too high or too low.")
            else:
                print(dirs[scan_dir_input-1])
                return safe_mode_prompt(scan_dir_input, "")
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
                return safe_mode_prompt(scan_dir_input, "path")


def enable_safe_mode():
    while True:
        enable_safe = input("enable 'safe-mode' [Y/n]? ").lower()
        if enable_safe == "y":
            write_confirmation = {"safe-mode": True}
            scan_vars_file = os.path.join(Config().get_key_value("application_root"), "temp\\scan_vars.txt")
            old = dict(File(scan_vars_file).read("_dict"))
            try:
                old.pop("safe-mode")
                old.update(write_confirmation)
            except KeyError:
                old.update(write_confirmation)
            File(scan_vars_file).write(old)
            return "safe"
        if enable_safe == "n":
            return "unsafe"
        else:
            pass


def confirm_disable_safe_mode():
    while True:
        confirm_disable = input("Are you sure you want to proceed without 'safe-mode' enabled [Y/n]?").lower()
        if confirm_disable == "y":
            return "unsafe"
        if confirm_disable == "n":
            return enable_safe_mode()
        if confirm_disable == ":info":
            artifact_location = os.path.join(Config().get_key_value("application_root"), "artifact\\cli_entries\\safe_mode.txt")
            print(File(artifact_location).read(specific=""))
        else:
            pass


def safe_mode_prompt(directory, pid):
    if pid == "path":
        pass
    else:
        directory = Table().load_instance_by_id(directory)
    return [directory, confirm_disable_safe_mode()]


def safe_mode_file_deletion(files):
    crt_files = sorted(files.values())
    delete_list = []
    for file in crt_files:
        current_file = True
        while current_file:
            confirm_delete_input = input("Are you sure you want to delete '" + file + "' [Y/n]?").lower()
            if confirm_delete_input == "y":
                delete_list.append(file)
                current_file = False
            elif confirm_delete_input == "n":
                for path in files.keys():
                    if files.get(path) == file:
                        files.pop(path)
                        print("canceled deletion")
                        break
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
    return delete_list
