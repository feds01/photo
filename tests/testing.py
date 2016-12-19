import unittest
import src.thread_indexer
from src.core.utils import *
from src.data import Data
from src.indexer import Index

__author__ = "Alexander Fedotov <alexander.fedotov.uk@gmail.com>"
__company__ = "(C) Wasabi & Co. All rights reserved."

"""
Module name: testing.py
Usage:
Description -

"""


class IndexWithNormalMethod(unittest.TestCase):

    def test_index_method(self):
        self.assertEqual(Index("G:\\Photo\\").run_index(pipe=False), ["G:\\Photo\\sandbox"])

    """
    def test_index_thread_method(self):
        self.assertEqual(src.thread_indexer.main("E:\\Photo"), ["E:\\Photo\\sandbox", "E:\\Photo\\temp\\test"])
    """

    def test_index_with_fake_dir(self):
        self.assertRaises(Fatal, lambda: Index("F:\\Photo\\").run_index(pipe=False))


class DataMethod(unittest.TestCase):
    def setUp(self):
        self.file_location = os.path.join(Config().get_key_value("application_root"), "temp\\size_data.txt")
        self.expected_result = {1: ['G:\\Files\\Ana Felix Snow Queen', ['G:\\Files\\Ana Felix Snow Queen\\_GOOD', 'G:\\Files\\Ana Felix Snow Queen\\all', 'G:\\Files\\Ana Felix Snow Queen\\crt'], 0, 75, 38, 754, [7.08, 'Gb', 1073741824]], 2: ['G:\\Photo\\sandbox', ['G:\\Photo\\sandbox\\all', 'G:\\Photo\\sandbox\\crt', 'G:\\Photo\\sandbox\\good'], 1, 0, 0, 2, [0.0, 'bytes', 1]]}

    def test_time_on_creation(self):
        if Data(["G:\\Files\\Ana Felix Snow Queen", "G:\\Photo\\sandbox"]).export_data_on_directories() < 1:
            self.assertEqual(1, 1)
        else:
            self.assertEqual(1, 0)

    def test_correct_data(self):
        Data(["G:\\Files\\Ana Felix Snow Queen", "G:\\Photo\\sandbox"]).export_data_on_directories()
        self.assertEqual(File(self.file_location).read("_dict"), self.expected_result)

class IndexItemSize(unittest.TestCase):

    def test_zero_bytes(self):
        result = Directory(0).get_appropriate_units()
        self.assertEqual(str(result[0]) + result[1], "0bytes")

    def test_kilobyte(self):
        result = Directory(1024).get_appropriate_units()
        self.assertEqual(str(int(result[0])) + result[1], "1Kb")

    def test_negative_byte(self):
        result = Directory(-1).get_appropriate_units()
        self.assertEqual(str(result[0]) + result[1], "-1bytes")

    def test_overflow_byte(self):
        self.assertRaises(ByteOverflow, lambda:  Directory(3871283728371238172382).get_appropriate_units())

if __name__ == "__main__":
    unittest.main()