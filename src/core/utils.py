import os
from src.core.exceptions import *

__author__ = "Alexander Fedotov <alexander.fedotov.uk@gmail.com>"
__company__ = "(C) Wasabi & Co. All rights reserved."

"""
Module name: utils.py
Usage:
Description -

"""

file_sizes = {0: "bytes", 1: "Kb", 2: "Mb", 3: "Gb", 4: "Tb"}


def get_scan_type(var):
    return 'thread' if var else 'normal'

def get_largest_element(arr):
    return len(max(arr, key=len))


def find_element(arr, case):
        for element in arr:
                if case in element or case == element:
                    return int(arr.index(element))
                else:
                    continue


def extension_swapper(file, ext, remove_dot=False):
    if remove_dot:
        return file[:-4] + ext
    else:
        return file[:-3] + ext


def generate_border(data, use_str=False):
        if use_str:
            return len(str(data)) + 2
        if data >= 4:
            return data + 1
        else:
            return 4


def convert_list(int_list):
        str_list = []
        for i in int_list:
            str_list.append(str(i))
        return str_list


def get_command_path():
        return os.getcwd()


def get_directory_separator():
        return os.sep


def get_appropriate_units(size):
    _size = size
    byte_exponent = 1024
    if size == 0:
        return [size, "bytes", 1]
    else:
        for i in range(20):
            if size / byte_exponent >= 1:
                size /= byte_exponent
                continue
            elif size / byte_exponent < 1 and i == 0:
                return [size, file_sizes[0], 1]
            elif size / byte_exponent < 1:
                try:
                    return [round(_size / byte_exponent ** i, 2), file_sizes[i], byte_exponent ** i]
                except KeyError:
                    return [round(_size / byte_exponent **i, 2), i, byte_exponent**i]


def handle_get_content(path, silent_mode=False):
    try:
        content = os.listdir(path)
    except PermissionError:
        if silent_mode:
            pass
        else:
            IndexingError(path, 'permissions')
        return ""
    return content


class Utility:
    def __init__(self):
        self.final_list = []
        self.input_list = []
        self.construct = []
        self.path_construct_list = []
        self.block_pos = 0
        self.old_block = ""
        self.cur_block = ""
        self.slicing = False

    def list_organiser(self, _list):
        self.input_list = [x for x in _list if x]
        for element in self.input_list:
            if type(element) == list:
                self.final_list.extend(element)
            else:
                self.final_list.append(element)
        return self.final_list

    def join_lists(self, *lists):
        if len(lists) == 1:
            return lists[0]
        else:
            for element_list in lists:
                self.final_list.extend(element_list)
            return self.final_list

    def shorten_path(self, path, max_chars=30, count_separator_char=False):
        overflow_chars = len(path) - (max_chars + 1)
        self.construct, self.input_list = path.split(os.sep), path.split(os.sep)
        if count_separator_char:
            for _ in self.input_list[:-1]:
                overflow_chars += 1
        if len(path) >= max_chars:
            self.input_list.pop(-1)
            self.final_list.append({self.input_list[-1]: len(self.input_list[-1])})
            if int(self.final_list[0][self.input_list[-1]]) < overflow_chars:
                self.input_list.pop(-1)
                overflow_chars -= int(self.final_list[0][self.construct[-2]])
                for component in reversed(self.input_list):
                    if len(component) >= overflow_chars:
                        self.final_list.append({component: len(component)})
                        overflow_chars -= len(component)
                        if overflow_chars <= 0:
                            break
                    if len(component) < overflow_chars:
                        self.final_list.append({component: len(component)})
                        overflow_chars -= len(component)
                        continue
            self.input_list = list()
            for key in list(reversed(self.final_list)):
                self.input_list.append(list(key.keys()))
            self.input_list = self.list_organiser(self.input_list)[-len(self.input_list):]
            self.path_construct_list.append(self.construct.index(self.input_list[0]))
            for element in self.input_list:
                self.construct.remove(element)
            self.construct.insert(int(self.path_construct_list[0]), "...")
            while len("".join(self.construct)) + int(len(self.construct))-1 > max_chars:
                overflow_chars = len("".join(self.construct)) + int(len(self.construct)) - 1
                if overflow_chars-3 <= max_chars:
                    self.block_pos = (find_element(list(self.construct), "...")) - 1
                    if len(self.construct[self.block_pos]) is 3:
                        self.slicing = True
                        self.cur_block = self.construct[self.block_pos][0] + "..."
                        break
                    if overflow_chars - 2 <= max_chars + 1:
                        self.cur_block = str("".join(list(self.construct[self.block_pos])[:2])) + "..."
                if overflow_chars > max_chars:
                    self.construct.pop(self.construct.index("...")-1)
                else:
                    self.slicing = True
                    break
            if self.slicing:
                self.construct.pop(self.block_pos), self.construct.pop(self.construct.index("..."))
                self.construct.insert(self.block_pos, self.cur_block)
            self.old_block = self.construct[0] + get_directory_separator()
            for block in self.construct[1:]:
                self.old_block = os.path.join(self.old_block, block)
            return self.old_block
        else:
            return path