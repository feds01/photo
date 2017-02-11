import argparse
from src.cli_helpers import *
from src.thread_indexer import *
from multiprocessing import freeze_support

__author__ = "Alexander Fedotov <alexander.fedotov.uk@gmail.com>"
__company__ = "(C) Wasabi & Co. All rights reserved."


CLI_INPUT_BLOCK = "~$ "

class Arguments:
    path = ''
    safe = ''
    blacklist = ''
    silent = ''
    thread = ''
    pass


def prepare(directory):
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
            ThreadIndex(path=arguments.path, use_blacklist=arguments.blacklist, silent=arguments.silent).run(pipe=True)
        else:
            Index(path=arguments.path, use_blacklist=arguments.blacklist, silent=arguments.silent).run(pipe=True)
        Table().make_table()
        print()
        print("Enter ID of directory or enter path of directory to continue")
        dirs = []
        max_id = len(
            File(Config.join_specific_data('application_root', 'application_directories', 'table_data')).read('_dict'))
        for i in range(1, max_id+1):
            dirs.append(Table().load_instance_by_id(i)[0])
        while True:
            directory_input = input(CLI_INPUT_BLOCK)
            try:
                directory_input = int(directory_input)
                if max_id < directory_input or directory_input < 0:
                    print("The entered ID is too high or too low.")
                else:
                    print('loading - %s' % dirs[directory_input-1])
                    loader(Table().load_instance_by_id(directory_input))
                    if confirm_selection():
                        prepare(Table().load_instance_by_id(directory_input)[0])
                    else:
                        print()
                        continue
            except ValueError:
                try:
                    if directory_input[0] is ":":
                        if directory_input[1:] == "paths":
                            for path in dirs:
                                print(path)
                        continue
                except IndexError:
                    pass
                if directory_input.isspace() or directory_input == "":
                    continue
                if directory_input not in dirs:
                    print("Entered directory path not present.")
                else:
                    print('loading - %s' % directory_input)
                    loader(Table().load_instance_by_id(directory_input))
                    if confirm_selection():
                        prepare(directory_input)
                    else:
                        continue
