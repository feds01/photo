#!C:\Python\Python35-32\python.exe
from src.data import Data
from src.hooks.checks import *
from src.utilities.arrays import organise_array

__author__ = "Alexander Fedotov <alexander.fedotov.uk@gmail.com>"
__company__ = "(C) Wasabi & Co. All rights reserved."

"""
Module name: indexer.py
Usage: cli.py, thread_indexer.py
Description -

This module is used to index a directory recursively and find a specific directory
structure with specific sub-folder names at the first recursion depth. The module
runs an index and outputs the results in a form of a list which it can pipe to the
"data.py" module. The argument "path" must be passed to the method as this is the
starting point of the index. Furthermore arguments such as "use_blacklist", "max_instances"
can be specified to limit the index results or filter the indexing results. The
argument "thread_index" is used by the module "thread_indexer.py" which enables
support for the required method.

Index():

:exception if :arg "path" is not a real directory
:raises Fatal(), stops application as the exception was caught too deep. A check was passed in "cli.py" and is
        not passed in this module.

:argument path           (index start point)                                             [default= "" (necessary)]
:argument use_blacklist  (filters folder scan with black_list)                           [default= False         ]
:argument thread_method  (enable support for thread_method)                              [default= False         ]
:argument max_instances  (indexes until the scan finds the maximum amount of instances)  [default= -1 (no limit) ]

:returns list with results i.e; Index("F:\\").run_index() -> ["F:\\Model\\Aria\\", "F:\\photos\\James_sept"]
"""


class Index:
    def __init__(self, path, thread_method=False, silent=False, use_blacklist=False, max_instances=-1):
        self.silent_mode = silent
        self.thread_method = thread_method
        self.path = path
        self.use_blacklist = use_blacklist
        self.max_instances = max_instances
        self.photo_directories = []
        self.directories, self.directory_leaves = [], []

    def validate_directory_structure(self, paths):
        return Directory(paths).index_photo_directory(max_instances=self.max_instances,
                                                      silent_mode=self.silent_mode)

    def analyze_directories(self):
        self.photo_directories.append(
            self.validate_directory_structure(self.directories))

    def directory_filter(self):
        for directory in self.directory_leaves:
            self.directories.remove(directory)

    @staticmethod
    def run_directory(path):
        if Directory(path).index_directory(count=True) < 3:
            pass
        if Index(path="").validate_directory_structure(paths=path):
            return path

    def find_leaves(self):
        for directory in self.directories:
            branches = Directory.get_branches(directory, silent=self.silent_mode)
            if len(branches) < 3:
                self.directory_leaves.append(directory)
        return self.directory_leaves

    def apply_filter(self, return_results=False):
        self.find_leaves(), self.directory_filter()
        if return_results:
            return self.directories

    def run_directory_index(self):
        if len(Directory.get_branches(self.path, silent=self.silent_mode)) == 0:
            node_error(self.path, self.silent_mode)

        if self.use_blacklist:
            self.directories = Directory(self.path).index_with_blacklist()
        else:
            self.directories = Directory(self.path).index_directory()

    def run(self, pipe=True):
        check_directory(self.path)
        self.run_directory_index()
        self.apply_filter()
        self.analyze_directories()
        self.photo_directories = organise_array(self.photo_directories)
        if pipe:
            Data(self.photo_directories).export()
        else:
            return self.photo_directories