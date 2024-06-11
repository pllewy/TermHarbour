import unittest
from static.AI_modules.alignment import align

class TestAlignment(unittest.TestCase):
    def setUp(self):
        self.source_sentence = ["This", "is", "a", "test"]
        self.target_sentence = ["This", "is", "also", "a", "test"]

    def test_align_with_default_method(self):
        result = align(self.source_sentence, self.target_sentence)
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 4)

    def test_align_with_non_default_method(self):
        result = align(self.source_sentence, self.target_sentence, alignment_method="inter")
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 4)

    def test_align_with_empty_sentences(self):
        result = align([], [])
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 0)

if __name__ == '__main__':
    unittest.main()