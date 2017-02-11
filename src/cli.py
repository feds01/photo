import argparse
from src.thread_indexer import *
from multiprocessing import freeze_support
# from multiprocessing import freeze_support

__author__ = "Alexander Fedotov <alexander.fedotov.uk@gmail.com>"
__company__ = "(C) Wasabi & Co. All rights reserved."


CLI_INPUT_BLOCK = "~$"


class Arguments:
    path = ''
    safe = ''
    blacklist = ''
    silent = ''
    thread = ''
    pass

arguments = Arguments()
parser = argparse.ArgumentParser(description="Remove redundant photo backup's")

parser.add_argument('-p', '--path', help='specify a specific starting path, leaving blank will index the current directory.')
parser.add_argument('-t', '--thread', default=False, action='store_true', help='use threads to increase indexing speeds')
parser.add_argument('-b', '--blacklist', default=False, action='store_true', help='use the blacklist to filter out unwanted directories')
parser.add_argument('-s', '--silent', default=False, action='store_true', help="don't display mild error messages or warnings.")
parser.add_argument('--safe', default=True, action='store_true', help='inform user of any file operations')


parser.parse_args(namespace=arguments)

if arguments.path == '':
    arguments.path = get_command_path()

if not Directory(arguments.path).check_directory():
    Fatal("directory does not exist", True, 'directory=%s' % arguments.path)
else:
    if __name__ == '__main__':
        freeze_support()
        arguments.path = Directory(arguments.path).standardise_drive()
        if arguments.thread:
            print(ThreadIndex(path=arguments.path, use_blacklist=arguments.blacklist, silent=arguments.silent).run())
        else:
            print(Index(path=arguments.path, use_blacklist=arguments.blacklist, silent=arguments.silent).run())