import time
import unittest
from src.thread_indexer import *
from src.utilities.manipulation import sizeof_fmt
__author__ = "Alexander Fedotov <alexander.fedotov.uk@gmail.com>"
__company__ = "(C) Wasabi & Co. All rights reserved."

root:     str = os.path.split(__file__)[0]
main_dir: str = ''
test_dir: str = ''
dirs:    list = ['crt', 'good', 'all']


def setup():
    global root, main_dir, test_dir, dirs

    main_dir = os.path.join(root, 'output')
    test_dir = os.path.join(main_dir, 'test_0')
    try:
        os.mkdir(main_dir)
        os.mkdir(test_dir)

        for d in dirs:
            os.mkdir(os.path.join(test_dir, d))

    except FileExistsError:
        return


class IndexWithNormalMethod(unittest.TestCase):

    def setUp(self):
        setup()

    def test_method(self):
        self.assertEqual(Index(path=main_dir).run(pipe=False), [test_dir])

    def test_fake_dir(self):
        self.assertRaises(Fatal, lambda: Index(path="E:\\Photo\\").run(pipe=False))

    def test_blacklisted_dir(self):
        self.assertRaises(Fatal, lambda: Index(path='C:\\Windows').run(pipe=False))


class IndexWithThreadMethod(unittest.TestCase):

    def setUp(self):
        setup()

    def test_method(self):
        self.assertEqual(ThreadIndex(main_dir, no_check=True).run(pipe=False),  [test_dir])

    def test_fake_dir(self):
        self.assertRaises(Fatal, lambda: ThreadIndex(path="E:\\Photo\\").run(pipe=False))

    def test_blacklisted_dir(self):
        self.assertRaises(Fatal, lambda: ThreadIndex(path='C:\\Windows').run(pipe=False))


class DataMethod(unittest.TestCase):
    def setUp(self):
        self.start = time.time()
        Data(test_dir).export()
        self.end = time.time() - self.start
        self.file_location = Config.join_specific_data("application_root", "application_directories.size_data")
        self.expected_result = {1: {'path': '', 'file_list': {'.CR2': (0, []), '.dng': (0, []), '.tif': (0, []), '.jpg': (0, [])}, 'photo': [], 'size': [0, '0bytes']}}

    def test_time_on_creation(self):
        if self.end < 1:
            self.assertEqual(1, 1)
        else:
            self.assertEqual(1, 0)

    def test_correct_data(self):
        Data(test_dir).export()
        self.assertEqual(File(self.file_location).read("dict"), self.expected_result)

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