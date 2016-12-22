# import time
import multiprocessing
from src.indexer import Index
from src.hooks.blacklist_hook import *
from multiprocessing import Pool, freeze_support

__author__ = "Alexander Fedotov <alexander.fedotov.uk@gmail.com>"
__company__ = "(C) Wasabi & Co. All rights reserved."

"""
Module name: thread_indexer.py
Usage:
Description -

"""
# Variables for multiprocessing
JOB_QUEUE = []
artifact_location = {}

# variable not implemented yet
PROCESS_COUNT = multiprocessing.cpu_count()
# final result variable
result = []


def get_nodes(root, use_blacklist=False):
    global artifact_location
    root_branches = Directory.get_directory_branches(root, os.listdir(root))
    if use_blacklist:
        root_branches = Blacklist(helpers=artifact_location).check_entry_existence(root_branches)
    return root_branches


def form_job_queue(nodes, helpers, use_blacklist):
    for item in nodes:
        if not use_blacklist:
            helpers = {}
        JOB_QUEUE.append([item, helpers, use_blacklist])
    return JOB_QUEUE


def index_wrapper(*args):
    return index_branch(args[0][0], args[0][1], args[0][2])


def index_branch(branch, helpers, use_blacklist=False):  # This is a target function!
    if use_blacklist:
        instance = Index(helpers, path=branch, thread_method=True, use_blacklist=use_blacklist)
    else:
        instance = Index(path=branch, thread_method=True)
    instance.run_directory_index()
    return instance.apply_filter(return_results=True)


def run_directory_index(root, max_instances=-1, use_blacklist=False):
    del max_instances
    global artifact_location, JOB_QUEUE, PROCESS_COUNT, result
    freeze_support()
    if use_blacklist:
        artifact_location.update({"artifact-loc": str(Directory(__file__).get_artifact_file_location(call="mod-launch", filename="blacklist.txt"))})
    nodes = get_nodes(root)
    JOB_QUEUE = form_job_queue(nodes, artifact_location, use_blacklist)
    pool = Pool(6)  # TODO: replace with PROCESS_COUNT
    result = pool.map(index_wrapper, JOB_QUEUE)
    pool.close(), pool.join()
    return Utility().list_organiser(result)


if __name__ == '__main__':
    pass
    # start = time.clock()
    # run_directory_index("C:\\", use_blacklist=True)
    # print(time.clock() - start)

"""
def main(analyze_path):
    queue = Queue()
    branches = Task(analyze_path).branches()
    main_list.append(Index.run_directory(Directory(analyze_path).get_current_directory()))
    for x in range(multiprocessing.cpu_count()):
        thread = Thread(queue)
        thread.daemon = True
        thread.start()
    for branch in branches:
        main_list.append(Index.run_directory(branch))
        queue.put(branch)
    queue.join()
    return Utility().list_organiser(main_list)
"""