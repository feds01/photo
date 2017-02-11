import os
from src.core.exceptions import *

__author__ = "Alexander Fedotov <alexander.fedotov.uk@gmail.com>"
__company__ = "(C) Wasabi & Co. All rights reserved."

"""
Module name: utils.py
Usage:
Description -

"""


def print_space(n):
    return n * "\n"


def get_largest_element(_list):
    return len(max(_list, key=len))


def find_element(_list, case):
        for element in _list:
                if case in element or case == element:
                    return int(_list.index(element))
                else:
                    continue


def extension_swapper(file, ext, remove_dot=False):
    if remove_dot:
        return file[:-4] + ext
    else:
        return file[:-3] + ext


def border_size_by_data_length(data, use_str=False):
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
        self.char_size = 0
        self.overflow_chars = 0
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

    def shorten_path(self, path, char_size=30, count_separator_char=False):
        self.char_size = char_size
        self.overflow_chars = len(path) - (self.char_size + 1)
        self.construct, self.input_list = path.split(os.sep), path.split(os.sep)
        if count_separator_char:
            for _ in self.input_list[:-1]:
                self.overflow_chars += 1
        if len(path) >= self.char_size:
            self.input_list.pop(-1)
            self.final_list.append({self.input_list[-1]: len(self.input_list[-1])})
            if int(self.final_list[0][self.input_list[-1]]) < self.overflow_chars:
                self.input_list.pop(-1)
                self.overflow_chars -= int(self.final_list[0][self.construct[-2]])
                for component in reversed(self.input_list):
                    if len(component) >= self.overflow_chars:
                        self.final_list.append({component: len(component)})
                        self.overflow_chars -= len(component)
                        if self.overflow_chars <= 0:
                            break
                    if len(component) < self.overflow_chars:
                        self.final_list.append({component: len(component)})
                        self.overflow_chars -= len(component)
                        continue
            self.input_list = list()
            for key in list(reversed(self.final_list)):
                self.input_list.append(list(key.keys()))
            self.input_list = self.list_organiser(self.input_list)[-len(self.input_list):]
            self.path_construct_list.append(self.construct.index(self.input_list[0]))
            for element in self.input_list:
                self.construct.remove(element)
            self.construct.insert(int(self.path_construct_list[0]), "...")
            while len("".join(self.construct)) + int(len(self.construct))-1 > char_size:
                self.overflow_chars = len("".join(self.construct)) + int(len(self.construct)) - 1
                if self.overflow_chars-3 <= char_size:
                    self.block_pos = (find_element(list(self.construct), "...")) - 1
                    if len(self.construct[self.block_pos]) is 3:
                        self.slicing = True
                        self.cur_block = self.construct[self.block_pos][0] + "..."
                        break
                    if self.overflow_chars - 2 == char_size + 1:
                        self.cur_block = str("".join(list(self.construct[self.block_pos])[:2])) + "..."
                    continue
                if self.overflow_chars > char_size:
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