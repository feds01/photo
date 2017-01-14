# import time
from src.indexer import *
from src.core.utils import *
from numpy import array_split
from src.blacklist import Blacklist
from multiprocessing import Pool, freeze_support

__author__ = "Alexander Fedotov <alexander.fedotov.uk@gmail.com>"
__company__ = "(C) Wasabi & Co. All rights reserved."

"""
Module name: thread_indexer.py
Usage: cli.py
Description -

"""


class ThreadIndex:
    def __init__(self, path, use_blacklist=False, silent=False, max_instances=-1):
        self.PROCESS_COUNT = os.cpu_count() * Config.get_specific_data('thread', 'instance_multiplier')
        self.JOB_QUEUE = []
        self.result = []
        self.nodes = []
        self.chunks = []
        self.photo_directories = []
        self.artifact_location = {}
        self.path = path
        self.use_blacklist = use_blacklist
        self.silent = silent
        self.max_instances = max_instances

    def get_nodes(self):
        self.nodes = Directory.get_branches(self.path, silent=self.silent)
        if self.use_blacklist:
            self.nodes = Blacklist(helpers=self.artifact_location).check_entry_existence(self.nodes)
        self.photo_directories.append(self.validate_directory_structure(paths=self.nodes))

    def form_job_queue(self):
        self.JOB_QUEUE = []
        for item in self.nodes:
            self.JOB_QUEUE.append(item)

    def form_filter_job_queue(self):
        self.JOB_QUEUE = []
        for block in self.chunks:
            self.JOB_QUEUE.append(list(block))

    def index_node(self, node):  # This is a target function!
        instance = Index(self.artifact_location, path=node, thread_method=True, silent=self.silent, use_blacklist=self.use_blacklist)
        instance.run_directory_index()
        return instance.directories

    def apply_filter(self, directories):  # this is also a target function
        instance = Index(path='', silent=self.silent)
        instance.directories = directories
        instance.apply_filter()
        return instance.directories

    def validate_directory_structure(self, paths):
        return Directory(paths).index_photo_directory(silent_mode=self.silent, max_instances=self.max_instances)

    def split_workload(self, results):
        return array_split(results, self.PROCESS_COUNT)

    def run_apply_filter(self):
        self.chunks = self.split_workload(self.result)
        self.form_filter_job_queue()
        pool = Pool(self.PROCESS_COUNT)
        self.result = pool.map(self.apply_filter, self.JOB_QUEUE)
        self.result = Utility().list_organiser(self.result)
        pool.close(), pool.join()

    def run_directory_index(self):
        if self.use_blacklist:
            self.artifact_location.update({"artifact-loc": os.path.join(Config.get_key_value("application_root"),
                                                                        Config.get_specific_data('blacklist',
                                                                                                 'location'))})
        self.get_nodes()
        self.form_job_queue()
        pool = Pool(self.PROCESS_COUNT)
        self.result = pool.map(self.index_node, self.JOB_QUEUE)
        self.result = Utility().list_organiser(self.result)
        pool.close(), pool.join()

    def safe_process_count(self):
        if type(self.PROCESS_COUNT) != int:
            try:
                if round(self.PROCESS_COUNT, 0) == self.PROCESS_COUNT:
                    self.PROCESS_COUNT = int(self.PROCESS_COUNT)
                    if not self.silent:
                        config_warning('magic process number was processed as float.')
                    pass
                else:
                    Fatal('process count cannot be float.', True, 'incorrect config magic process number of %s' %
                          (self.PROCESS_COUNT / os.cpu_count()))
            except TypeError as error:
                Fatal('process count cannot be float.', True, 'incorrect config magic process number of %s' %
                      self.PROCESS_COUNT, 'incorrect type: %s' % type(self.PROCESS_COUNT), '%s' % error)

    def run(self, pipe=False):
        if not Directory(self.path).check_directory():
            raise Fatal("directory does not exist", False, 'directory=%s' % self.path)
        self.safe_process_count()
        self.run_directory_index()
        self.run_apply_filter()
        self.photo_directories.append(self.validate_directory_structure(self.result))
        self.photo_directories = Utility().list_organiser(self.photo_directories)
        if pipe:
            Data(self.photo_directories).export_data_on_directories()
        else:
            return self.photo_directories


if __name__ == '__main__':
    freeze_support()
    # start = time.clock()
    # print(ThreadIndex('C:\\', use_blacklist=True).run())
    # print(time.clock() - start)