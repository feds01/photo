from SkeletonIndex import Index
import baseTools
from queue import Queue
import threading
import multiprocessing
main_list = []

__author__ = "Alexander Fedotov <alexander.fedotov.uk@gmail.com>"
__company__ = "(C) Wasabi & Co. All rights reserved."


class Thread(threading.Thread):
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue
        self.path = ""

    def run(self):
        while True:
            self.path = self.queue.get()
            print(self.path)
            main_list.append(Task.thread_task(self.path))
            self.queue.task_done()


class Task:
    def __init__(self, path):
        self.branch_list = []
        self.path = path

    def branches(self):
        self.branch_list = baseTools.Directory("").get_directory_branches(self.path)
        return self.branch_list

    @staticmethod
    def thread_task(directory):
            return Index(directory).cycle()


def main(analyze_path):
    main_list.append(Index.run_directory(analyze_path))
    queue = Queue()
    branches = Task(analyze_path).branches()
    for x in range(multiprocessing.cpu_count()):
        thread = Thread(queue)
        thread.daemon = True
        thread.start()
    for branch in branches:
        queue.put(branch)
    queue.join()
    return main_list
