import unittest
from static.AI_modules.alignment import align, align_sentences

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

    def test_align_sentences_returns_dictionary(self):
        result = align_sentences(self.source_sentence, self.target_sentence)
        self.assertIsInstance(result, dict)
        self.assertTrue("mwmf" in result)
        self.assertTrue("inter" in result)
        self.assertTrue("itermax" in result)

    def test_align_sentences_with_empty_sentences(self):
        result = align_sentences([], [])
        self.assertIsInstance(result, dict)
        self.assertTrue("mwmf" in result)
        self.assertTrue("inter" in result)
        self.assertTrue("itermax" in result)
        self.assertEqual(len(result["mwmf"]), 0)
        self.assertEqual(len(result["inter"]), 0)
        self.assertEqual(len(result["itermax"]), 0)

if __name__ == '__main__':
    unittest.main()