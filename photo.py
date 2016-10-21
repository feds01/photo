import argparse
import SkeletonIndex
import threadScan
import fileAnalysis
import baseTools


class Main:
    def __init__(self):
        self.cmd_path = ""

    @staticmethod
    def initial_setup():
        print("running setup for first time . . .")
        baseTools.File().run_setup()

    @staticmethod
    def clean_session_files():
        baseTools.File().clean_files(None, None, general=True)

