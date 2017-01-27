import time
from src.thread_indexer import *
from multiprocessing import freeze_support

__author__ = "Alexander Fedotov <alexander.fedotov.uk@gmail.com>"
__company__ = "(C) Wasabi & Co. All rights reserved."


CLI_INPUT_BLOCK = "~$"

if __name__ == '__main__':
    freeze_support()
    start = time.clock()
    print(ThreadIndex('C:\\', use_blacklist=True).run())
    print(time.clock() - start)