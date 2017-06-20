import time
import unittest
from src.thread_indexer import *

__author__ = "Alexander Fedotov <alexander.fedotov.uk@gmail.com>"
__company__ = "(C) Wasabi & Co. All rights reserved."


class IndexWithNormalMethod(unittest.TestCase):

    def test_method(self):
        self.assertEqual(Index(path="C:\\Temp").run(pipe=False), ["C:\\Temp\\test"])

    def test_fake_dir(self):
        self.assertRaises(Fatal, lambda: Index(path="E:\\Photo\\").run(pipe=False))

    def test_blacklisted_dir(self):
        self.assertRaises(Fatal, lambda: Index(path='C:\\Windows').run(pipe=False))


class IndexWithThreadMethod(unittest.TestCase):

    def test_method(self):
        self.assertEqual(ThreadIndex("C:\\Temp", no_check=True).run(), ["C:\\Temp\\test"])

    def test_fake_dir(self):
        self.assertRaises(Fatal, lambda: ThreadIndex(path="E:\\Photo\\").run(pipe=False))

    def test_blacklisted_dir(self):
        self.assertRaises(Fatal, lambda: ThreadIndex(path='C:\\Windows').run(pipe=False))


'''
class DataMethod(unittest.TestCase):
    def setUp(self):
        self.start = time.time()
        Data(["C:\\Temp\\"]).export_data_on_directories()
        self.end = time.time() - self.start
        self.file_location = Config.join_specific_data("application_root", "application_directories", 'size_data')
        self.expected_result = {1: ['E:\\Files\\Ana Felix Snow Queen', ['E:\\Files\\Ana Felix Snow Queen\\_GOOD', 'E:\\Files\\Ana Felix Snow Queen\\all', 'E:\\Files\\Ana Felix Snow Queen\\crt'], 0, 75, 38, 754, [7.08, 'Gb', 1073741824]], 2: ['E:\\Photo\\sandbox', ['E:\\Photo\\sandbox\\all', 'E:\\Photo\\sandbox\\crt', 'E:\\Photo\\sandbox\\good'], 1, 0, 0, 2, [0.0, 'bytes', 1]]}

    def test_time_on_creation(self):
        if self.end < 1:
            self.assertEqual(1, 1)
        else:
            self.assertEqual(1, 0)

    def test_correct_data(self):
        Data(["C:\\Files\\Ana Felix Snow Queen", "E:\\Photo\\sandbox"]).export_data_on_directories()
        self.assertEqual(File(self.file_location).read("dict"), self.expected_result)
'''

class IndexItemSize(unittest.TestCase):

    def test_zero_bytes(self):
        results = get_appropriate_units(0)
        self.assertEqual(str(results[0]) + results[1], "0bytes")

    def test_kilobyte(self):
        results = get_appropriate_units(1024)
        self.assertEqual(str(int(results[0])) + results[1], "1Kb")

    def test_negative_byte(self):
        results = get_appropriate_units(-1)
        self.assertEqual(str(results[0]) + results[1], "-1bytes")

if __name__ == "__main__":
    unittest.main()