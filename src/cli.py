# import time
import argparse
from src.thread_indexer import *
# from multiprocessing import freeze_support

__author__ = "Alexander Fedotov <alexander.fedotov.uk@gmail.com>"
__company__ = "(C) Wasabi & Co. All rights reserved."


CLI_INPUT_BLOCK = "~$"


class Arguments:
    pass

arguments = Arguments()
parser = argparse.ArgumentParser(description="Remove redundant photo backup's")

parser.add_argument('-p', '--path', help='specify a specific starting path, leaving blank will index the current directory.')
parser.add_argument('-t', '--thread', action='store_true', help='use threads to increase indexing speeds')
parser.add_argument('-b', '--blacklist', default=False, action='store_true', help='use the blacklist to filter out unwanted directories')
parser.add_argument('-s', '--silent', default=False, action='store_true', help="don't display mild error messages or warnings.")
parser.add_argument('--safe', action='store_true', help='inform user of any file operations')
parser.add_argument('--unsafe', action='store_true', default=False, help="don't inform user of file operations")

parser.parse_args(namespace=arguments)
if arguments.path is None:
    arguments.path = get_command_path()

# print(vars(arguments))

"""
if __name__ == '__main__':
    freeze_support()
    start = time.clock()
    print(ThreadIndex('C:\\', use_blacklist=True).run())
    print(time.clock() - start)
"""