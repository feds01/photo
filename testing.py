import unittest
from src.exceptions import *
from src.index import Index


class IndexWithNormalMethod(unittest.TestCase):

    def test_index_method(self):
        self.assertEqual(Index("E:\\Photo\\").cycle(pipe=False), ["E:\\Photo\\sandbox", "E:\\Photo\\temp\\test"])

    def test_index_with_fake_dir(self):
        self.assertRaises(Fatal, lambda: Index("F:\\Photo\\").cycle(pipe=False))


if __name__ == "__main__":
    unittest.main()