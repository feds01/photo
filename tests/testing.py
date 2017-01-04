import unittest
from src.data import Data
from src.thread_indexer import *

__author__ = "Alexander Fedotov <alexander.fedotov.uk@gmail.com>"
__company__ = "(C) Wasabi & Co. All rights reserved."

"""
Module name: testing.py
Usage:
Description -

"""


class IndexWithNormalMethod(unittest.TestCase):

    def test_index_method(self):
        self.assertEqual(Index(path="E:\\Photo\\").run(pipe=False), ["E:\\Photo\\sandbox"])

    def test_index_thread_method(self):
        self.assertEqual(run("E:\\Photo"), ["E:\\Photo\\sandbox"])

    def test_index_with_fake_dir(self):
        self.assertRaises(Fatal, lambda: Index(path="F:\\Photo\\").run(pipe=False))


class DataMethod(unittest.TestCase):
    def setUp(self):
        self.start = time.time()
        Data(["E:\\Files\\Ana Felix Snow Queen", "E:\\Photo\\sandbox"]).export_data_on_directories()
        self.end = time.time() - self.start
        self.file_location = os.path.join(Config.get_key_value("application_root"), "temp\\size_data.txt")
        self.expected_result = {1: ['E:\\Files\\Ana Felix Snow Queen', ['E:\\Files\\Ana Felix Snow Queen\\_GOOD', 'E:\\Files\\Ana Felix Snow Queen\\all', 'E:\\Files\\Ana Felix Snow Queen\\crt'], 0, 75, 38, 754, [7.08, 'Gb', 1073741824]], 2: ['E:\\Photo\\sandbox', ['E:\\Photo\\sandbox\\all', 'E:\\Photo\\sandbox\\crt', 'E:\\Photo\\sandbox\\good'], 1, 0, 0, 2, [0.0, 'bytes', 1]]}

    def test_time_on_creation(self):
        if self.end < 1:
            self.assertEqual(1, 1)
        else:
            self.assertEqual(1, 0)

    def test_correct_data(self):
        Data(["E:\\Files\\Ana Felix Snow Queen", "E:\\Photo\\sandbox"]).export_data_on_directories()
        self.assertEqual(File(self.file_location).read("_dict"), self.expected_result)


class IndexItemSize(unittest.TestCase):

    def test_zero_bytes(self):
        results = Directory(0).get_appropriate_units()
        self.assertEqual(str(results[0]) + results[1], "0bytes")

    def test_kilobyte(self):
        results = Directory(1024).get_appropriate_units()
        self.assertEqual(str(int(results[0])) + results[1], "1Kb")

    def test_negative_byte(self):
        results = Directory(-1).get_appropriate_units()
        self.assertEqual(str(results[0]) + results[1], "-1bytes")

    def test_overflow_byte(self):
        self.assertRaises(ByteOverflow, lambda:  Directory(3871283728371238172382).get_appropriate_units())

if __name__ == "__main__":
    unittest.main()