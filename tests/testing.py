import time
import unittest
from src.indexing import *
from src.utilities.manipulation import sizeof_fmt
__author__ = "Alexander Fedotov <alexander.fedotov.uk@gmail.com>"
__company__ = "(C) Wasabi & Co. All rights reserved."

root:      str = os.path.split(__file__)[0]
main_dir:  str = ''
test_dir:  str = ''
make_dirs: list = ["test_0", "test_1"]
dirs:      list = ['crt', 'good', 'all']


def setup():
    global root, main_dir, test_dir, dirs, make_dirs

    main_dir = os.path.join(root, 'output')
    test_dir = os.path.join(main_dir, 'test_0')

    try:
        os.mkdir(main_dir)

        for i in make_dirs:
            os.mkdir(os.path.join(main_dir, i))

        for d in dirs:
            os.mkdir(os.path.join(test_dir, d))

    except FileExistsError:
        return


class IndexWithNormalMethod(unittest.TestCase):
    def setUp(self):
        Config.init_session({'thread': True, 'blacklist': True, 'verbose': True})
        setup()

    def test_method(self):
        self.assertEqual(Index(path=main_dir).run(pipe=False), [test_dir])

    def test_fake_dir(self):
        self.assertRaises(Fatal, lambda: Index(path="E:\\Photo\\").run(pipe=False))

    def test_blacklisted_dir(self):
        self.assertRaises(Fatal, lambda: Index(path='C:\\Windows').run(pipe=False))


class IndexWithThreadMethod(unittest.TestCase):

    def setUp(self):
        Config.init_session({'thread': True, 'blacklist': True, 'verbose': True})
        setup()

    def test_method(self):
        self.assertEqual(ThreadIndex(main_dir, check=False).run(pipe=False), [test_dir])

    def test_fake_dir(self):
        self.assertRaises(Fatal, lambda: ThreadIndex(path="E:\\Photo\\").run(pipe=False))

    def test_blacklisted_dir(self):
        self.assertRaises(Fatal, lambda: ThreadIndex(path='C:\\Windows').run(pipe=False))


class DataMethod(unittest.TestCase):
    def setUp(self):
        self.start = time.time()
        Data(test_dir).export()
        self.end = time.time() - self.start
        self.file_location = Config.join("application_root", "application_directories.session")
        self.expected_result = {'directories': {'1': {'path': '', 'file_list': {'.CR2': {'amount': 0, 'files': []}, '.dng': {'amount': 0, 'files': []}, '.tif': {'amount': 0, 'files': []}, '.jpg': {'amount': 0, 'files': []}}, 'photo': [], 'size': [0, '0bytes']}}}

    def test_time_on_creation(self):
        if self.end < 1:
            self.assertEqual(1, 1)
        else:
            self.assertEqual(1, 0)

    def test_correct_data(self):
        Data(test_dir).export()
        data = File(self.file_location).read_json()
        data.pop("table")

        self.assertEqual(data, self.expected_result)

class IndexItemSize(unittest.TestCase):

    def test_zero_bytes(self):
        results = sizeof_fmt(0)
        self.assertEqual(results[1], "0bytes")

    def test_kilobyte(self):
        results = sizeof_fmt(1024)
        self.assertEqual(results[1], "1.0Kb")

    def test_negative_byte(self):
        results = sizeof_fmt(-1)
        self.assertEqual(results[1], "0bytes")

if __name__ == "__main__":
    unittest.main()