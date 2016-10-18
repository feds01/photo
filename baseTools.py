import os

__author__ = "Alexander Fedotov <alexander.fedotov.uk@gmail.com>"
__company__ = "(C) Wasabi & Co. All rights reserved."


class Cleaner:
    def __init__(self):
        self.final_list = []

    def list_organiser(self, path_list):
        path_list = [x for x in path_list if x]
        for element in path_list:
            if type(element) == list:
                self.final_list.extend(self.list_organiser(element))
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


class Directory:
    def __init__(self, operation_input):
        self.operation_input = operation_input
        self.path = ""

    def get_current_directory(self):
        self.path = os.path.split(self.operation_input)[0]
        return self.path

    def checkDirectory(self):
        if os.path.exists(self.operation_input):
            return True
        else:
            return False
