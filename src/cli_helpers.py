import os
from src.utils import *
from src.data import Table


def fancy_tree_display(roots, values):
    full_string, tree_symbol = "", "|_ "
    max_root = Cleaner().get_largest_element(roots)
    for i in range(len(roots)):
        align = ""
        if len(roots[i]) < 4:
            align = " " * (max_root - len(roots[i]))
        full_string += tree_symbol + roots[i] + align + ": " + str(values[i]) + "\n"
    return full_string


def table_instance_display(instance_data):
    instance_leaves = {}
    file_count = 0
    print(instance_data[1])
    for directory in instance_data[1]:
        instance_leaves.update({os.path.basename(directory): Directory(directory).index_directory(count=True, file=True)})
    instance_data.pop(1)
    print("More detail about the photo directory - \'", os.path.basename(instance_data[0]), "\' :", space(1))
    print("Full directory path: ", instance_data[0])
    for i in range(1, 5):
        file_count += instance_data[i]
    print("Total files:", file_count)

"""
self.instance = self.table_import_data.get(_id)
self.instance.pop(1)
print("More detail about the photo directory - \'", os.path.basename(self.instance[0]), "\' :", space(1))
print("Full directory path: ", self.instance[0])
for i in range(1, 5):
    self.file_count += self.instance[i]
print("Total files:", self.file_count)
print(fancy_tree_display(["crt", "good", "all"], [3, 6, 2]))
print("Total size: ", self.instance[5][0] + self.instance[5][1])
"""
table_instance_display(Table().load_instance_by_id(1))