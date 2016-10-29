from index import Index
from baseTools import Directory, Cleaner
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
        self.process = ""

    def run(self):
        while True:
            self.process = self.queue.get()
            main_list.append(Task.thread_task(self.process))
            self.queue.task_done()


class Task:
    def __init__(self, path):
        self.branch_list = []
        self.path = path

    def branches(self):
        self.branch_list = Directory("").get_directory_branches(self.path)
        return self.branch_list

    @staticmethod
    def thread_task(directory):
            return Index(directory, thread_method=True).cycle()


def main(analyze_path):
    queue = Queue()
    branches = Task(analyze_path).branches()
    main_list.append(Index("").run_directory(Directory(analyze_path).get_current_directory()))
    for x in range(multiprocessing.cpu_count()):
        thread = Thread(queue)
        thread.daemon = True
        thread.start()
    for branch in branches:
        main_list.append(Index("").run_directory(branch))
        queue.put(branch)
    queue.join()
    return Cleaner().list_organiser(main_list)

print(main("E:\\Photo"))