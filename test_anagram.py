import unittest
from anagram import is_anagram


class TestLog(unittest.TestCase):
    def is_anagram(self):
        # Test Cases as per documentation
        self.assertEqual(is_anagram('', ''), True)
        self.assertEqual(is_anagram('A', 'A'), True)
        self.assertEqual(is_anagram('A', 'B'), False)
        self.assertEqual(is_anagram('ab', 'ba'), True)
        self.assertEqual(is_anagram('AB', 'ab'), True)
