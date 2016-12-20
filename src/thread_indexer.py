import multiprocessing
from queue import Queue
from src.hooks.blacklist_hook import *
from src.core.utils import *
from src.indexer import Index


__author__ = "Alexander Fedotov <alexander.fedotov.uk@gmail.com>"
__company__ = "(C) Wasabi & Co. All rights reserved."

"""
Module name: thread_indexer.py
Usage:
Description -

"""

main_list = []


def blacklist_check_nodes(root):
    root_branches = Directory.get_directory_branches(root,os.listdir(root))
    root_branches = Blacklist().check_entry_existence(root_branches)
    return root_branches


def index_branch(branch, use_blacklist=True): # This is a target function!
    instance = Index(branch, thread_method=True, use_blacklist=use_blacklist)
    instance.run_directory_index()
    return instance.apply_filter(return_results=True)


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