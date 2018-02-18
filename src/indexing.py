#!C:\Python\Python35-32\python.exe
import signal
from multiprocessing import Pool

from src.data import Data
from src.core.core import *
from src.thread.manager import Process
from src.utilities.arrays import organise_array
from src.thread.protection import check_process_count

__author__ = "Alexander Fedotov <alexander.fedotov.uk@gmail.com>"
__company__ = "(C) Wasabi & Co. All rights reserved."


def check_directory(path):
    if not Directory(path).check_directory():
        raise Fatal("directory does not exist", False, 'directory= %s' % path)

    if Blacklist.check(path, child=True):
        raise Fatal("directory is blacklisted.", False, 'directory=%s' % path)


class Index:
    def __init__(self, path=""):
        if path != "":
            self.path = path
        else:
            self.path = Config.get_session("path")

        self.directories = []
        self.dirapi = Directory(self.path)

    def validate(self, paths):
        return Directory(paths).index_photo_directory()

    def apply_filter(self, return_results=False):
        for directory in self.directories:
            branches = self.dirapi.get_branches(directory)
            if len(branches) < 3:
                self.directories.remove(directory)

        self.directories = self.validate(self.directories)

        if return_results:
            return self.directories

    def index(self):
        if len(self.dirapi.get_branches(self.path)) == 0:
            if not Config.get_session("verbose"):
                IndexingError(self.path, "leaf")

        self.dirapi.set_path(self.path)

        if Config.get_session("blacklist"):
            self.directories = self.dirapi.index_with_blacklist()
        else:
            self.directories = self.dirapi.index_directory()

    def run(self, pipe=True):
        check_directory(self.path)

        self.index(), self.apply_filter()

        if pipe:
            Data(self.directories).export()
        else:
            return self.directories


class ThreadIndex:
    def __init__(self, path="", check=True):
        if path != "":
            self.path = path
        else:
            self.path = Config.get_session("path")

        self.index = Index("")
        self.PROCESS_COUNT = check_process_count(v=True, return_pnum=True)

        self.result = []
        self.nodes = []
        self.dirs = [] # directories which match the specifications

        self.check = check

    def get_nodes(self):
        self.nodes = Directory.get_branches(self.path)

        if Config.get_session("blacklist"):
            # this filters the first level directories and checks if they are blacklisted.
            self.nodes = Blacklist.is_entry(self.nodes)

        # check if any of the nodes match the specifications
        self.dirs = self.index.validate(self.nodes)

        for node in self.nodes:
            if handle_fdreq(node) == "":
                self.nodes.remove(node)

    def worker(self, node):
        if Config.get('debug'):
            sys.excepthook = exception_handler

        __index_object = self.index

        try:
            if self.check:
                Process.get_frame()

            __index_object.path = node
            __index_object.index()

            return __index_object.apply_filter(return_results=True)

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
            self.dirs.append(self.result)
            self.dirs = organise_array(self.dirs)

    def run(self, pipe=True):
        check_directory(self.path)

        self.get_nodes()
        self.launch_process_pool()

        if pipe:
            Data(self.dirs).export()
        else:
            return self.dirs