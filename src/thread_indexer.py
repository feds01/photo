import multiprocessing
from queue import Queue
from src.blacklist import *
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
    root_branches = Blacklist(helpers=Blacklist().read_blacklist()).check_entry_existence(root_branches)

    return root_branches







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