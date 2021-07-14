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
        # Test for some Errors
        self.assertRaises(is_anagram(1, 2), TypeError)
        self.assertRaises(is_anagram([1, "a"], ("b", 5, 9)), TypeError)
        self.assertRaises(is_anagram(), TypeError)
