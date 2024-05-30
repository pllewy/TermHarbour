import unittest
import os
from static.AI_modules import extraction_01 as extraction

class ExtractionTests(unittest.TestCase):
    def setUp(self):
        self.text = "This is a test text. It contains 2 sentences."
        self.file_path_txt = "dummy_path.txt"
        self.file_path_pdf = "dummy_path.pdf"
        self.file_path_csv = "dummy_path.csv"
        self.file_path_unsupported = "dummy_path.docx"
        self.terms_pattern = ["test_text", "2_sentences"]
        self.terms_ner = ["Test_Text"]
        self.nlp = extraction.load_spacy_model("en")

    def tearDown(self):
        # Clean up created test files
        if os.path.exists(self.file_path_txt):
            os.remove(self.file_path_txt)
        if os.path.exists(self.file_path_pdf):
            os.remove(self.file_path_pdf)
        if os.path.exists(self.file_path_csv):
            os.remove(self.file_path_csv)

    def test_preprocess_text_removes_unwanted_characters(self):
        result = extraction.preprocess_text(self.text)
        self.assertEqual(result, "This is a test text It contains sentences")

    def test_read_text_from_file_handles_txt_files(self):
        with open(self.file_path_txt, 'w') as file:
            file.write(self.text)
        result = extraction.read_text_from_file(self.file_path_txt)
        self.assertEqual(result, self.text)

    def test_read_text_from_file_handles_unsupported_files(self):
        with self.assertRaises(ValueError):
            extraction.read_text_from_file(self.file_path_unsupported)

    def test_lemmatize_terms_returns_correct_lemmas(self):
        result = extraction.lemmatize_terms(self.terms_pattern, self.nlp)
        self.assertEqual(result, {"test_text": "test_text", "2_sentences": "2_sentence"})

    def test_extract_specialist_terms_with_patterns_returns_correct_terms(self):
        result = extraction.extract_specialist_terms_with_patterns(self.text, self.nlp)
        self.assertEqual(result, self.terms_pattern)

    def test_extract_ner_terms_returns_correct_terms(self):
        result = extraction.extract_ner_terms(self.text, self.nlp)
        self.assertEqual(result, self.terms_ner)

    def test_combine_term_lists_returns_combined_list(self):
        result = extraction.combine_term_lists(self.terms_pattern, self.terms_ner)
        self.assertEqual(result, self.terms_pattern + self.terms_ner)

    def test_post_process_terms_removes_single_occurrences_and_numeric_terms(self):
        terms = ["test_text", "2_sentences", "2_sentences", "400th"]
        result = extraction.post_process_terms(terms)
        self.assertEqual(result, ["2_sentences", "2_sentences"])

if __name__ == '__main__':
    unittest.main()
