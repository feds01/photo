__author__ = "Alexander Fedotov <alexander.fedotov.uk@gmail.com>"
__company__ = "(C) Wasabi & Co. All rights reserved."


class Cleaner:
    def __init__(self, operation):
        self.final_list = []
        self.operation = operation

    def __clean(self):
        del self.final_list
        del self.operation
        self.__init__(None)

    def list_organiser(self, path_list):
        path_list = [x for x in path_list if x]
        for element in path_list:
            if type(element) == list:
                self.final_list.extend(self.list_organiser(element))
            else:
                self.final_list.append(element)
        return self.final_list
