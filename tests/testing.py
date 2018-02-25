import time
import unittest
from src.indexing import *
from src.utilities.manipulation import sizeof_fmt
from src.utilities.infrequents import to_structure
from src.utilities.session import open_session

__author__ = "Alexander Fedotov <alexander.fedotov.uk@gmail.com>"
__company__ = "(C) Wasabi & Co. All rights reserved."

main_root: str = os.path.abspath(os.path.join(os.path.split(__file__)[0], "..\\"))
root:      str = os.path.split(__file__)[0]
main_dir:  str = ''
test_dir: str  = ''

dirs:      list = ['crt', 'good', 'all']
make_dirs: dict = {"test_0": "", "test_1" : dirs, "test_3" : [{"nested": dirs}, dirs]}


def setup():
    global root, main_dir, dirs, make_dirs

    main_dir = os.path.join(root, 'output')

    try:
        if not os.path.exists(main_dir):
            os.mkdir(main_dir)

        for item in to_structure(main_dir, make_dirs):
            if not os.path.exists(item):
                os.mkdir(item)

    except PermissionError as e:
        print("Could not perform setup! :( permissions")
        print(e)


class ProgramConfiguration(unittest.TestCase):
    def test_extraction(self):
        self.assertEqual(type(Config.get("table_records")), int)

    def test_extraction1(self):
        self.assertEqual(Config.get("application_root"), main_root + "\\")

    def test_incorrect_key(self):
        self.assertRaises(Fatal, lambda: Config.get("non-present-key"))

    def test_join(self):
        temp_folder = os.path.join(main_root, "temp\\session.json")
        self.assertEqual(Config.join("application_root", "session"), temp_folder)


class IndexWithNormalMethod(unittest.TestCase):
    def setUp(self):
        setup()
        Config.init_session({'thread': False, 'blacklist': True, 'verbose': True})

    def test_method(self):
        self.assertEqual(len(Index(path=main_dir).run(pipe=False)), 3)

    def test_method_with_nested_directory(self):
        result = Index(path=os.path.join(main_dir, "test_3"), ).run(pipe=False)
        self.assertEqual(len(result), 2)

    def test_fake_dir(self):
        self.assertRaises(Fatal, lambda: Index(path="E:\\Photo\\").run(pipe=False))

    def test_blacklisted_dir(self):
        self.assertRaises(Fatal, lambda: Index(path='C:\\Windows').run(pipe=False))


class IndexWithThreadMethod(unittest.TestCase):
    def setUp(self):
        setup()
        open_session()
        Config.set_session("thread", True)

    def test_method(self):
        result = ThreadIndex(path=os.path.join(main_dir)).run(pipe=False)

        self.assertEqual(len(result), 3)

    def test_method_with_nested_directory(self):
        result = ThreadIndex(path=os.path.join(main_dir, "test_3")).run(pipe=False)

        self.assertEqual(len(result), 2)

    def test_fake_dir(self):
        self.assertRaises(Fatal, lambda: ThreadIndex(path="E:\\Photo\\").run(pipe=False))

    def test_blacklisted_dir(self):
        self.assertRaises(Fatal, lambda: ThreadIndex(path='C:\\Windows').run(pipe=False))


class DataMethod(unittest.TestCase):
    def setUp(self):
        open_session()
        test_dir = os.path.join(main_dir, "test_0")

        self.start = time.time()
        Data(test_dir).export()
        self.end = time.time() - self.start
        self.file_location = Config.join("application_root", "session")
        self.expected_result = {'directories': {'1': {'path': '', 'file_count': 0, 'file_list': {'.CR2': {'amount': 0, 'files': []}, '.dng': {'amount': 0, 'files': []}, '.tif': {'amount': 0, 'files': []}, '.jpg': {'amount': 0, 'files': []}}, 'photo': [], 'size': [0, '0Kb']}}}

    def test_time_on_creation(self):
        if self.end < 1:
            self.assertEqual(1, 1)
        else:
            self.assertEqual(1, 0)

    def test_correct_data(self):
        Data(test_dir).export()
        data = File(self.file_location).read_json()

        try:
            data.pop("session")
            data.pop("table")
        except KeyError:
            pass

        self.assertEqual(data, self.expected_result)


class IndexItemSize(unittest.TestCase):

    def test_zero_bytes(self):
        results = sizeof_fmt(0)
        self.assertEqual(results[1], "0Kb")

    def test_kilobyte(self):
        results = sizeof_fmt(1024)
        self.assertEqual(results[1], "1.0Kb")

    def test_negative_byte(self):
        results = sizeof_fmt(-1)
        self.assertEqual(results[1], "0Kb")


if __name__ == "__main__":
    unittest.main()