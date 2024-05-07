import unittest
from krux.values import *


class TestValues(unittest.TestCase):
    def test_none_min_max(self):
        self.assertEqual(none_min(1, 2), 1)
        self.assertEqual(none_min(1, None), 1)
        self.assertEqual(none_min(None, 2), 2)
        self.assertEqual(none_min(None, None), None)

        self.assertEqual(none_max(1, 2), 2)
        self.assertEqual(none_max(1, None), 1)
        self.assertEqual(none_max(None, 2), 2)
        self.assertEqual(none_max(None, None), None)


if __name__ == '__main__':
    unittest.main()
