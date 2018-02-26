#!C:\Python\Python35-32\python.exe
import signal
from src.data import Data
from src.core.core import *
from numpy import array_split
from multiprocessing import Pool
from src.utilities.arrays import organise_array
from src.utilities.infrequents import check_process_count

__author__ = "Alexander Fedotov <alexander.fedotov.uk@gmail.com>"
__company__ = "(C) Wasabi & Co. All rights reserved."


def _check_path(path):
    if not check_directory(path):
        raise Fatal("directory does not exist", 'directory= %s' % path)

    if Blacklist.check(path, child=True):
        raise Fatal("directory is blacklisted.", 'directory=%s' % path)


class Index:
    def __init__(self, path=""):
        if path != "":
            self.path = path
        else:
            self.path = Config.get_session("path")

        self.directories = []
        self.dirapi = Directory(self.path)

    def set_path(self, path):
        self.__init__(path)

    @staticmethod
    def validate(paths):
        return Directory(paths).index_photo_directory()

    def apply_filter(self, ret=False):
        self.directories = organise_array([self.validate(self.directories)])

        if ret:
            return self.directories

    def index(self, ret=False):
        if len(get_branches(self.path)) == 0:
            if not Config.get_session("verbose"):
                IndexingError(self.path, "leaf")

        self.dirapi.set_path(self.path)

        if Config.get_session("blacklist"):
            self.directories = self.dirapi.index_with_blacklist()
        else:
            self.directories = self.dirapi.index_directory()

        if ret:
            return self.directories

    def run(self, pipe=True):
        _check_path(self.path)

        self.index(), self.apply_filter()

        # check if actual path is an applicable directory, if so append to list
        if Index.validate(self.path):
            self.directories.append(self.path)

        if pipe:
            Data(self.directories).export()
        else:
            return self.directories


class ThreadIndex:
    def __init__(self, path=""):
        if path != "":
            self.path = path
        else:
            self.path = Config.get_session("path")

        # append session settings temp/session.json for sharing across workers
        self.file = File(Config.join("application_root", "session"))
        self.index = Index(path)
        self.PROCESS_COUNT = check_process_count(v=True, ret=True)
        self.workers = []

        self.directories = []  # directories which match the specifications

    def get_nodes(self):
        self.directories = [list(x) for x in array_split(self.index.index(ret=True), self.PROCESS_COUNT)]

    def worker(self, arr):
        # worker config session init
        Config.init_session(self.file.read_json().get("session"))

        if Config.get('debug'):
            sys.excepthook = exception_handler

        try:
            return Index.validate(arr)

        except KeyboardInterrupt:
            signal.signal(signal.SIGINT, signal.SIG_IGN)

    def launch_process_pool(self):
        result = []

        try:
            with Pool(self.PROCESS_COUNT) as pool:
                result = organise_array(pool.map(self.worker, self.directories))

                pool.close(), pool.join()

        except KeyboardInterrupt:
            signal.signal(signal.SIGINT, signal.SIG_IGN)

        finally:
            self.directories = organise_array(result)

    def run(self, pipe=True):
        _check_path(self.path)

        self.get_nodes()
        # split workload into sections
        self.launch_process_pool()

        if Index.validate(self.path):
            self.directories.append(self.path)

        if pipe:
            Data(self.directories).export()
        else:
            return self.directories