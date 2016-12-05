import unittest
import src.thread_indexer
from src.exceptions import *
from src.data import Data
from src.index import Index


class IndexWithNormalMethod(unittest.TestCase):

    def test_index_method(self):
        self.assertEqual(Index("E:\\Photo\\").cycle(pipe=False), ["E:\\Photo\\sandbox", "E:\\Photo\\temp\\test"])

    def test_index_thread_method(self):
        self.assertEqual(src.thread_indexer.main("E:\\Photo"), ["E:\\Photo\\sandbox", "E:\\Photo\\temp\\test"])

    def test_index_with_fake_dir(self):
        self.assertRaises(Fatal, lambda: Index("F:\\Photo\\").cycle(pipe=False))


class DataMethod(unittest.TestCase):

    def test_time_on_creation(self):
        if Data(["E:\\Files\\Ana Felix Snow Queen", "E:\\Photo\\sandbox", "E:\\Photo\\temp\\test"]).export_data_on_directories() < 1:
            self.assertEqual(1, 1)
        else:
            self.assertEqual(1, 0)

if __name__ == "__main__":
    unittest.main()