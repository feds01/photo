import signal
from src.indexer import *
from numpy import array_split
from multiprocessing import Pool
from src.thread.manager import Process
from src.thread.protection import check_process_count

__author__ = "Alexander Fedotov <alexander.fedotov.uk@gmail.com>"
__company__ = "(C) Wasabi & Co. All rights reserved."

"""
Module name: thread_indexer.py
Usage: cli.py
Description -

"""
pool: str


class ThreadIndex:
    def __init__(self, path, use_blacklist=False, silent=False, max_instances=-1, no_check=False):
        self.PROCESS_COUNT = check_process_count(True, True)
        self.JOB_QUEUE = []
        self.result = []
        self.nodes = []
        self.chunks = []
        self.photo_directories = []
        self.path = path
        self.use_blacklist = use_blacklist
        self.silent = silent
        self.max_instances = max_instances
        self.no_check = no_check

    def get_nodes(self):
        self.nodes = Directory.get_branches(self.path, silent=self.silent)
        if self.use_blacklist:
            self.nodes = Blacklist.check_entry_existence(self.nodes)
        self.photo_directories.append(self.validate_directory_structure(paths=self.nodes))
        self._node_filter()

    def _node_filter(self):
        for node in self.nodes:
            # background check, user doesn't need to know second time
            if handle_get_content(node, silent_mode=True) == '':
                self.nodes.remove(node)
            else:
                pass

    def launch_process_pool(self):
        global pool

        try:
            with Pool(self.PROCESS_COUNT) as pool:
                if not self.no_check:
                    for _process in pool._pool[:]:
                        if not Process.register(_process.pid, 'thread'):
                            Fatal('Process authentication error', True,
                                  'there was a problem authorising a process launch')

                self.run_directory_index()
                self.run_apply_filter()

        except KeyboardInterrupt:
            signal.signal(signal.SIGINT, signal.SIG_IGN)

        finally:
            pool.close(), pool.join()

    def form_job_queue(self):
        self.JOB_QUEUE = []
        for item in self.nodes:
            self.JOB_QUEUE.append(item)

    def form_filter_job_queue(self):
        self.JOB_QUEUE = []
        for block in self.chunks:
            self.JOB_QUEUE.append(list(block))

    def index_node(self, node):  # This is a target function!
        if Config.get('debug'):
            sys.excepthook = exception_handler

        try:
            instance = Index(path=node, thread_method=True, silent=self.silent, use_blacklist=self.use_blacklist)
            instance.run_directory_index()
            return instance.directories
        except KeyboardInterrupt:
            signal.signal(signal.SIGINT, signal.SIG_IGN)

    def apply_filter(self, directories):  # this is also a target function
        try:
            instance = Index(path='', silent=self.silent)
            instance.directories = directories
            instance.apply_filter()
            return instance.directories

        except KeyboardInterrupt:
            signal.signal(signal.SIGINT, signal.SIG_IGN)

    def validate_directory_structure(self, paths):
        return Directory(paths).index_photo_directory(silent_mode=self.silent, max_instances=self.max_instances)

    def split_workload(self, results):
        return array_split(results, self.PROCESS_COUNT)

    def run_apply_filter(self):
        global pool
        try:
            self.chunks = self.split_workload(self.result)
            self.form_filter_job_queue()
            self.result = organise_list(pool.map(self.apply_filter, self.JOB_QUEUE))
            if not self.no_check:
                Process.get_frame()

        finally:
            if not self.no_check:
                Process.truncate(os.getpid())

    def run_directory_index(self):
        global pool
        self.get_nodes()
        self.form_job_queue()
        self.result = organise_list(pool.map(self.index_node, self.JOB_QUEUE))

    def run(self, pipe=True):
        check_directory(self.path)
        self.launch_process_pool()
        self.photo_directories.append(self.validate_directory_structure(self.result))
        self.photo_directories = organise_list(self.photo_directories)
        if pipe:
            Data(self.photo_directories).export()
        else:
            return self.photo_directories