from src import utils


class Main:
    def __init__(self):
        self.cmd_path = ""

    @staticmethod
    def initial_setup():
        print("running setup for first time . . .")
        utils.File().run_setup()

    @staticmethod
    def clean_session_files():
        utils.File().clean_files(None, None, general=True)

