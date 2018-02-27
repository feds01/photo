import sys, os
import argparse

sys.path.append(os.path.abspath(os.path.split(__file__)[0] + "\\..\\"))

from src.cleaner import *
from src.data import Table
from src.indexing import *
from multiprocessing import freeze_support
from src.utilities.codes import *
from src.utilities.session import close_session, open_session

__author__ = "Alexander Fedotov <alexander.fedotov.uk@gmail.com>"
__company__ = "(C) Wasabi & Co. All rights reserved."


def do_index():
    if Config.get_session("thread"):
        result = ThreadIndex().run()
    else:
        result = Index().run()

    if len(result) == 0:
        print(f'zero instances of photo directories found under {Config.get_session("path")}')
        close_session()
    else:
        Data(result).export()


def main():
    # run scan
    do_index()
    table = Table()

    print("\nuse 'exit' to stop and exit the program\nuse 'refresh' to refresh index results\n")
    table.make_table()
    print(str(table))
    print("\nEnter id of directory to instantiate file structure analysis")

    options = list(range(1, table.row_count + 1))
    options.extend(["exit", "refresh"])

    finished_directories = []

    # main loop
    while True:
        option = query_user("id: ", options, on_error="The entered id is too high or too low.")

        if option == "refresh":
            do_index()
            print(f'\n{str(table)}\n')

        elif option == "exit":
            close_session(finished_directories)
        else:
            path = table.from_id(option).get("path")

            print(f"\nselected directory {path}")
            confirm = query_user("are you sure you want to continue [y/N] ?", ["y", "n"], on_error="wow")

            if confirm == "y":
                result = Delete(analyse(path)).deletion_manager()

                if result == DELETE_SUCCESS:
                    finished_directories.append(path)

                if result == DELETE_ABORT:
                    print("Aborted current operation")

            print()


parser = argparse.ArgumentParser(description="Remove redundant photo backup's")

parser.add_argument('-p', '--path',
                    help='specify a specific starting path, leaving blank will index the current directory.')
parser.add_argument('-t', '--thread', default=False, action='store_true',
                    help='use threads to increase indexing speeds')
parser.add_argument('-b', '--blacklist', default=Config.get('blacklist.enabled'), action='store_true',
                    help='use the blacklist to filter out unwanted directories')
parser.add_argument('-v', '--verbose', default=False, action='store_true',
                    help="don't display mild error messages or warnings.")


if __name__ == '__main__':
    args = {}
    args.update(vars(parser.parse_args()))

    Config.init_session(args)

    # perform checks on arguments
    if Config.get_session("path") is None:
        Config.set_session("path", standardise_drive(os.getcwd()))

    if Config.get_session("blacklist") and not Config.get('blacklist.enabled'):
        if not Config.get_session("verbose"):
            config_warning('blacklist is not enabled in config, but is being used.')

    if Config.get_session("thread"):
        check_process_count(v=Config.get_session("verbose"), ret=True)
    # environment setup
    print(f'Scanning {Config.get_session("path")} . . .\n')
    freeze_support()

    Config.set_session("path", standardise_drive(Config.get_session("path")))
    # actual scan function calls
    open_session(), main()
