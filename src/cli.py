# setup to extent to system paths
import sys, os
import argparse

sys.path.extend(os.pardir)
from src.cli_helpers import *
from src.cleaner import *
from src.data import Table
from src.thread_indexer import *
from src.thread.manager import Process
from multiprocessing import freeze_support

__author__ = "Alexander Fedotov <alexander.fedotov.uk@gmail.com>"
__company__ = "(C) Wasabi & Co. All rights reserved."


CLI_INPUT_BLOCK = "~$ "
finished_jobs = 0
blacklist_default = Config.get('blacklist.enabled')
dirs = []
max_id = 0


class Arguments:
    path = ''
    safe = True
    blacklist = blacklist_default
    silent = False
    thread = False
    pass


def run_scan():
    if arguments.thread:
        ThreadIndex(path=arguments.path, use_blacklist=arguments.blacklist, silent=arguments.silent).run()
    else:
        Index(path=arguments.path, use_blacklist=arguments.blacklist, silent=arguments.silent).run()

    Table().make_table()


def load_table():
    global max_id, dirs
    dirs = []
    max_id = len(File(Config.join_specific_data('application_root', 'application_directories.table_data')).read('dict'))
    for i in range(1, max_id + 1):
        dirs.append(Table().load_instance_by_id(i).get('path'))


def refresh():
    if finished_jobs > 0:
        return True, run_scan() if bool(prompt_user('Refresh index results? [Y/n] ', ['y', 'n']) == 'y') else False
    else:
        return False


def prepare(directory):
    files = Analyse(directory).run_analysis()
    return Delete(select_files(files), arguments.silent).deletion_manager()


def setup():
    arguments.path = Directory(arguments.path).standardise_drive()

arguments = Arguments()
parser = argparse.ArgumentParser(description="Remove redundant photo backup's")

parser.add_argument('-p', '--path', help='specify a specific starting path, leaving blank will index the current directory.')
parser.add_argument('-t', '--thread', default=False, action='store_true', help='use threads to increase indexing speeds')
parser.add_argument('-b', '--blacklist', default=blacklist_default, action='store_true', help='use the blacklist to filter out unwanted directories')
parser.add_argument('-s', '--silent', default=False, action='store_true', help="don't display mild error messages or warnings.")
parser.add_argument('--safe', default=True, action='store_true', help='inform user of any file operations')
parser.parse_args(namespace=arguments)

if __name__ == '__main__':
        if arguments.path == '':
            arguments.path = get_command_path()

        if not Directory(arguments.path).check_directory():
            Fatal("directory does not exist", True, 'directory=%s' % arguments.path)

        if arguments.blacklist and not blacklist_default:
            if not arguments.silent:
                config_warning('blacklist is not enabled in config, but is being used.')

        if arguments.thread:
            Process.register(os.getpid(), 'parent')
            check_process_count(silent=arguments.silent, return_pnum=True)
        # environment setup
        print('beginning scan of %s ' % arguments.path)
        freeze_support(), setup()
        # actual scan function calls
        run_scan()
        # user interface
        print("Enter ID of directory or enter path of directory to continue")
        while True:
            directory_input = input(CLI_INPUT_BLOCK)
            try:
                load_table()
                directory_input = int(directory_input)
                if max_id < directory_input or directory_input < 0:
                    print("The entered ID is too high or too low.")
                else:
                    print('loading - %s' % dirs[directory_input-1])
                    loader(Table().load_instance_by_id(directory_input))
                    if bool(prompt_user('Are you sure you want to continue? [Y/n] ', ['y', 'n']) == 'y'):
                        if prepare(Table().load_instance_by_id(directory_input).get('path')):
                            print()
                    else:
                        print()
                        continue
            except ValueError:
                load_table()
                try:
                    if directory_input[0] is ":":
                        print()
                        if directory_input[1:] == "paths":
                            if refresh():
                                finished_jobs -= 1
                                load_table()
                            for path in dirs:
                                print(path)
                        if directory_input[1:] == 'exit':
                            exit()
                        if directory_input[1:] == 'table':
                            if refresh():
                                finished_jobs -= 1
                                load_table()
                            Table().make_table()
                        print()
                        continue
                except IndexError:
                    pass
                if directory_input.isspace() or directory_input == "":
                    continue
                if directory_input not in dirs:
                    print("Entered directory path not present.")
                else:
                    print('loading - %s' % directory_input)
                    loader(Table().load_instance_by_id(dirs.index(directory_input)+1))
                    if bool(prompt_user('Are you sure you want to continue? [Y/n] ', ['y', 'n']) == 'y'):
                        if prepare(directory_input):
                            finished_jobs += 1
                    else:
                        print()
                        continue
