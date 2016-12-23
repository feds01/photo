# import time
from numpy import array_split
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
PROCESS_COUNT = os.cpu_count() * 6
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


def form_filter_job_queue(directory_blocks, silent_mode):
    global JOB_QUEUE
    JOB_QUEUE = []
    for block in directory_blocks:
        JOB_QUEUE.append([list(block), silent_mode])
    return JOB_QUEUE


def filter_wrapper(*args):
    return apply_filter(args[0][0], args[0][1])


def index_wrapper(*args):
    return index_branch(args[0][0], args[0][1], args[0][2])


def index_branch(branch, helpers, use_blacklist=False):  # This is a target function!
    if use_blacklist:
        instance = Index(helpers, path=branch, thread_method=True, use_blacklist=use_blacklist)
    else:
        instance = Index(path=branch, thread_method=True)
    instance.run_directory_index(), instance.blacklist_filter()
    return instance.directories


def apply_filter(directories, silent):  # this is also a target function
    instance = Index(path='', use_blacklist=False, silent=silent)
    instance.directories = directories
    instance.apply_filter()
    return instance.directories


def validate_directory_structure(paths, silent=False, max_instances=-1):
    return Directory(paths).index_photo_directory(silent_mode=silent, max_instances=max_instances)


def split_workload(results):
    return array_split(results, PROCESS_COUNT)


def run_apply_filter(results, silent=False):
    global JOB_QUEUE, PROCESS_COUNT, result
    freeze_support()
    chunks = split_workload(results)
    JOB_QUEUE = form_filter_job_queue(chunks, silent)
    pool = Pool(PROCESS_COUNT)
    result = pool.map(filter_wrapper, JOB_QUEUE)
    result = Utility().list_organiser(result)
    pool.close(), pool.join()
    return result


def run_directory_index(root, use_blacklist=False):
    global artifact_location, JOB_QUEUE, PROCESS_COUNT, result
    freeze_support()
    if use_blacklist:
        artifact_location.update({"artifact-loc": str(Directory(__file__).get_artifact_file_location(filename="blacklist.txt"))})
    nodes = get_nodes(root)
    JOB_QUEUE = form_job_queue(nodes, artifact_location, use_blacklist)
    pool = Pool(PROCESS_COUNT)
    result = pool.map(index_wrapper, JOB_QUEUE)
    result = Utility().list_organiser(result)
    pool.close(), pool.join()
    return result


def run(path, silent=False, max_instances=-1, use_blacklist=False):
    global result
    result = run_directory_index(path, use_blacklist)
    result = run_apply_filter(result, silent)
    photo_directories = validate_directory_structure(result, silent, max_instances)
    return photo_directories

if __name__ == '__main__':
    freeze_support()
    # start = time.clock()
   # print(run('C:\\', use_blacklist=True))
    #print(time.clock() - start)