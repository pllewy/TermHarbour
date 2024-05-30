import unittest
from static.AI_modules import classification

class MockLbl2Vec:
    def load(self, *args, **kwargs):
        return self

    def predict_new_docs(self, *args, **kwargs):
        return {"highest_similarity_score": 1, "label1": 0.9, "label2": 0.8, "label3": 0.7, "label4": 0.6, "label5": 0.5, "doc_key": "0", "most_similar_label": "label1"}

class TestClassification(unittest.TestCase):
    def setUp(self):
        self.text = "This is a test text"
        self.category = "medicine"
        self.language = "english"
        self.original_lbl2vec = classification.Lbl2Vec
        classification.Lbl2Vec = MockLbl2Vec

    def tearDown(self):
        classification.Lbl2Vec = self.original_lbl2vec

    def test_text_categorization_returns_expected_result(self):
        result = classification.text_categorization(self.category, self.language, self.text)
        self.assertEqual(result, ["label1", "label2", "label3", "label4"])

    def test_text_categorization_with_low_scores_returns_empty_list(self):
        original_predict_new_docs = MockLbl2Vec.predict_new_docs
        MockLbl2Vec.predict_new_docs = lambda self, *args, **kwargs: {"highest_similarity_score": 1, "label1": 0.1, "label2": 0.2, "label3": 0.3, "label4": 0.4, "label5": 0.5, "doc_key": "0", "most_similar_label": "label5"}
        result = classification.text_categorization(self.category, self.language, self.text)
        MockLbl2Vec.predict_new_docs = original_predict_new_docs
        self.assertEqual(result, [])

if __name__ == '__main__':
    unittest.main()
