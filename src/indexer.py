#!C:\Python\Python35-32\python.exe
# import time
from src.data import Data
from src.hooks.blacklist_hook import *



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
    def __init__(self, *args, path, thread_method=False, silent=False, use_blacklist=False, max_instances=-1):
        self.silent_mode = silent
        self.thread_method = thread_method
        self.path = path
        self.use_blacklist = use_blacklist
        self.max_instances = max_instances
        self.photo_model_directories = []
        self.first_layer_nodes = []
        self.directory_index_data = []
        self.directories, self.directory_leaves = [], []
        if self.thread_method:
            self.big_job_data = args[0]
        else:
            self.big_job_data = {}

    @staticmethod
    def validate_directory_structure(path, max_instances=-1, silent_mode=False):
        return Directory(path).index_photo_directory(max_instances=max_instances, silent_mode=silent_mode)

    def analyze_directories(self):
        self.photo_model_directories.append(self.validate_directory_structure(self.directories, self.max_instances, silent_mode=self.silent_mode))

    def directory_filter(self):
        for directory in self.directory_leaves:
            self.directories.remove(directory)

    @staticmethod
    def run_directory(path):
        if Directory(path).index_directory(count=True) < 3:
            pass
        if Index.validate_directory_structure(path):
            return path

    def find_leaves(self):
        for directory in self.directories:
            if len(Directory.get_directory_branches(directory, handle_get_content(directory, silent_mode=self.silent_mode))) < 3:
                self.directory_leaves.append(directory)
        return self.directory_leaves

    def apply_filter(self, return_results=False):
        if self.use_blacklist:
            self.directories = certify_index_results(self.directories, helpers=self.big_job_data)

        self.find_leaves(), self.directory_filter()
        if return_results:
            return self.directories

    def node_count_check(self):
        if len(self.directories) is 0:
            if not self.silent_mode:
                print("error: given directory is a leaf.")
            return []

    def run_directory_index(self, _return=False):
        if not self.thread_method:
            self.first_layer_nodes = Directory.get_directory_branches(self.path, os.listdir(self.path))
        else:
            self.first_layer_nodes = [self.path]
        self.directories = []
        for node in self.first_layer_nodes:
            self.directory_index_data = Directory(node).index_directory()
            if len(self.directory_index_data) >= 2048:
                self.big_job_data.update({node: self.directory_index_data})
            else:
                pass
            self.directories.append(self.directory_index_data)
        self.directories.append(self.first_layer_nodes)
        self.directories = Utility().list_organiser(self.directories)
        if _return:
            return [self.directories, self.big_job_data]

    def run(self, pipe=False):
        # start = time.clock()
        if not Directory(self.path).check_directory():
            raise Fatal("fatal: directory does not exist")
        self.run_directory_index()
        self.node_count_check()
        self.apply_filter(), self.analyze_directories()
        self.photo_model_directories = Utility().list_organiser(self.photo_model_directories)
        if pipe:
            Data(self.photo_model_directories).export_data_on_directories()
        else:
            # print(time.clock() - start)
            return self.photo_model_directories

# print(Index(path="C:\\", use_blacklist=True, silent=True).run())