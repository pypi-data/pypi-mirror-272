import unittest
from pylib.core import average

class TestCore(unittest.TestCase):
    def test_average(self):
        self.assertEqual(average([10, 20, 30]), 20)
        self.assertEqual(average([]), 0)

if __name__ == '__main__':
    unittest.main()
