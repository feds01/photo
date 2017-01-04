import time
from numpy import array_split
from src.indexer import Index
from src.blacklist import Blacklist
from src.core.utils import *
from multiprocessing import Pool, freeze_support

__author__ = "Alexander Fedotov <alexander.fedotov.uk@gmail.com>"
__company__ = "(C) Wasabi & Co. All rights reserved."

"""
Module name: thread_indexer.py
Usage: cli.py
Description -

"""
# Variables for scanning options
max_instance_count = -1
use_blacklist = False
silent = False

# Variables for multiprocessing
JOB_QUEUE = []
photo_directories = []
artifact_location = {}

PROCESS_COUNT = os.cpu_count() * Config.get_specific_data('thread', 'instance_multiplier')
result = []
# final result variable


def get_nodes(root):
    global artifact_location, photo_directories
    branches = Directory.get_branches(root)
    if use_blacklist:
        branches = Blacklist(helpers=artifact_location).check_entry_existence(branches)
    photo_directories.append(validate_directory_structure(paths=branches))
    return branches


def form_job_queue(nodes, helpers):
    for item in nodes:
        if not use_blacklist:
            helpers = {}
        JOB_QUEUE.append([item, helpers, use_blacklist])
    return JOB_QUEUE


def form_filter_job_queue(directory_blocks):
    global JOB_QUEUE
    JOB_QUEUE = []
    for block in directory_blocks:
        JOB_QUEUE.append([list(block)])
    return JOB_QUEUE


def filter_wrapper(*args):
    return apply_filter(args[0][0])


def index_wrapper(*args):
    return index_branch(args[0][0], args[0][1])


def index_branch(branch, helpers):  # This is a target function!
    if use_blacklist:
        instance = Index(helpers, path=branch, thread_method=True, use_blacklist=use_blacklist)
    else:
        instance = Index(path=branch, thread_method=True)
    instance.run_directory_index()
    return instance.directories


def apply_filter(directories):  # this is also a target function
    instance = Index(path='', silent=silent)
    instance.directories = directories
    instance.apply_filter()
    return instance.directories


def validate_directory_structure(paths):
    return Directory(paths).index_photo_directory(silent_mode=silent, max_instances=max_instance_count)


def split_workload(results):
    return array_split(results, PROCESS_COUNT)


def run_apply_filter(results):
    global JOB_QUEUE, PROCESS_COUNT, result
    chunks = split_workload(results)
    JOB_QUEUE = form_filter_job_queue(chunks)
    pool = Pool(PROCESS_COUNT)
    result = pool.map(filter_wrapper, JOB_QUEUE)
    result = Utility().list_organiser(result)
    pool.close(), pool.join()
    return result


def run_directory_index(root):
    global artifact_location, JOB_QUEUE, PROCESS_COUNT, result
    freeze_support()
    if use_blacklist:
        artifact_location.update({"artifact-loc": str(Directory(__file__).get_artifact_file_location(filename="blacklist.txt"))})
    nodes = get_nodes(root=root)
    JOB_QUEUE = form_job_queue(nodes, artifact_location)
    pool = Pool(PROCESS_COUNT)
    result = pool.map(index_wrapper, JOB_QUEUE)
    result = Utility().list_organiser(result)
    pool.close(), pool.join()
    return result


def run(path, silent_mode=False, max_instances=-1, blacklist=False):
    global result, photo_directories, silent, use_blacklist, max_instance_count
    silent = silent_mode
    use_blacklist = blacklist
    max_instance_count = max_instances
    result = run_directory_index(path)
    result = run_apply_filter(result)
    photo_directories.append(validate_directory_structure(result))
    return Utility().list_organiser(photo_directories)

if __name__ == '__main__':
    freeze_support()
    # start = time.clock()
    # print(run('C:\\', blacklist=True))
    # print(time.clock() - start)