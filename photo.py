import argparse
import SkeletonIndex
import threadScan
import fileAnalysis
import FileTransfer


class Main:
    def __init__(self):
        self.cmd_path = ""

    @staticmethod
    def initial_setup():
        print("running setup for first time . . .")
        FileTransfer.File().run_setup()

    @staticmethod
    def clean_session_files():
        FileTransfer.File().clean_files(None, None, all=True)

