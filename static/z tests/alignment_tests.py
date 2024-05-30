import unittest
from unittest.mock import patch
from static.AI_modules.alignment import align, align_sentences

class TestAlignment(unittest.TestCase):
    def setUp(self):
        self.source_sentence = ["This", "is", "a", "test"]
        self.target_sentence = ["This", "is", "also", "a", "test"]

    @patch('static.AI_modules.alignment.SentenceAligner')
    def alignment_returns_expected_result(self, mock_aligner):
        mock_aligner.return_value.get_word_aligns.return_value = {"itermax": [(0, 0), (1, 1), (2, 2), (3, 3)]}
        result = align(self.source_sentence, self.target_sentence)
        self.assertEqual(result, [["This", "This"], ["is", "is"], ["a", "also"], ["test", "test"]])

    @patch('static.AI_modules.alignment.SentenceAligner')
    def alignment_with_empty_sentences_returns_empty_list(self, mock_aligner):
        mock_aligner.return_value.get_word_aligns.return_value = {"itermax": []}
        result = align([], [])
        self.assertEqual(result, [])

    @patch('static.AI_modules.alignment.SentenceAligner')
    def align_sentences_returns_expected_result(self, mock_aligner):
        mock_aligner.return_value.get_word_aligns.return_value = {"mwmf": [(0, 0), (1, 1)], "inter": [(2, 2)], "itermax": [(3, 3)]}
        result = align_sentences(self.source_sentence, self.target_sentence)
        self.assertEqual(result, {"mwmf": [(0, 0), (1, 1)], "inter": [(2, 2)], "itermax": [(3, 3)]})

    @patch('static.AI_modules.alignment.SentenceAligner')
    def align_sentences_with_empty_sentences_returns_empty_dict(self, mock_aligner):
        mock_aligner.return_value.get_word_aligns.return_value = {"mwmf": [], "inter": [], "itermax": []}
        result = align_sentences([], [])
        self.assertEqual(result, {"mwmf": [], "inter": [], "itermax": []})

if __name__ == '__main__':
    unittest.main()