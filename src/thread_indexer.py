import signal
from src.indexer import *
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


class ThreadIndex:
    def __init__(self, path, use_blacklist=False, silent=False, max_instances=-1, check=True):
        self.index = Index("", silent=silent, use_blacklist=use_blacklist, max_instances=max_instances)
        self.PROCESS_COUNT = check_process_count(True, True)

        self.result = []
        self.nodes = []
        self.dirs = []

        self.path = path
        self.use_blacklist = use_blacklist
        self.silent_mode = silent
        self.max_instances = max_instances
        self.check = check

    def get_nodes(self):
        self.nodes = Directory.get_branches(self.path, silent=self.silent_mode)

        if self.use_blacklist:
            # this filters the first level directories and checks if they are blacklisted.
            self.nodes = Blacklist.check_entry_existence(self.nodes)

        self.dirs.append(self.index.validate(self.nodes))

        for node in self.nodes:
            if handle_fdreq(node, silent_mode=self.silent_mode) == "":
                self.nodes.remove(node)

    def worker(self, node):
        if Config.get('debug'):
            sys.excepthook = exception_handler

        __index_object = self.index

        try:
            if self.check:
                Process.get_frame()

            __index_object.path = node
            __index_object.run_directory_index()
            __index_object.apply_filter()

            return __index_object.directories

        except KeyboardInterrupt:
            signal.signal(signal.SIGINT, signal.SIG_IGN)

    def launch_process_pool(self):
        global pool

        try:
            with Pool(self.PROCESS_COUNT) as pool:
                if self.check:
                    for _process in pool._pool[:]:
                        if not Process.register(_process.pid, 'thread'):
                            Fatal('Process authentication error', True,
                                  'there was a problem authorising a process launch')

                self.result = organise_array(pool.map(self.worker, self.nodes))
        except KeyboardInterrupt:
            signal.signal(signal.SIGINT, signal.SIG_IGN)

        finally:
            pool.close(), pool.join()
            self.dirs.append(self.index.validate(self.result))
            self.dirs = organise_array(self.dirs)

    def run(self, pipe=True):
        check_directory(self.path)
        self.get_nodes()
        self.launch_process_pool()

        if pipe:
            Data(self.dirs).export()
        else:
            return self.dirs