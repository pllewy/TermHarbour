# Author: Maurycy Oprus

import static.AI_modules.extraction_01 as extraction
from lbl2vec import Lbl2Vec
from gensim.models.doc2vec import TaggedDocument

def clean_text(file_path):
    """
    Reads text from a file, preprocesses it and returns the cleaned text.

    Args:
        file_path (str): The path to the file to be read.

    Returns:
        str: The cleaned text.
    """
    text = extraction.read_text_from_file(file_path)
    extracted_terms = extraction.preprocess_text(text)

    print(extracted_terms.lower())
    return extracted_terms.lower()


def text_categorization(category, language, text):
    """
    Categorizes a given text based on the specified category and language.

    Args:
        category (str): The category to be used for categorization.
        language (str): The language of the text.
        text (str): The text to be categorized.

    Returns:
        list: A list of top categories for the text.
    """
    if category == 'medicine':
        if language == 'english':
            model = Lbl2Vec.load('models/Lbl2Vec/Lbl2Vec_med_simple_2')
    elif category == 'art':
        if language == 'english':
            model = Lbl2Vec.load('models/Lbl2Vec/Lbl2Vec_art_simple')
    elif category == 'news':
        if language == 'english':
            model = Lbl2Vec.load('models/Lbl2Vec/Lbl2Vec_broad_simple')
    elif category == "environment":
        if language == 'english':
            model = Lbl2Vec.load('models/Lbl2Vec/Lbl2Vec_environment_simple')

    cat_values = model.predict_new_docs(tagged_docs=[TaggedDocument(text.split(" "), ['0'])]).iloc[0]

    threshold = cat_values['highest_similarity_score'] * 0.8

    top_categories = []
    for label, score in cat_values.items():
        if label not in ["doc_key", "most_similar_label", "highest_similarity_score"]:
            if score > threshold:
                top_categories.append((label, score))

    top_categories = sorted(top_categories, key=lambda x: x[1], reverse=True)

    if len(top_categories) > 4:
        top_categories = top_categories[:4]

    return [category for category, score in top_categories]


if __name__ == "__main__":
    print(
        text_categorization(
            'medicine',
            'en',
            clean_text('C:/Users/Mauri/Desktop/main_repo/TermHarbour/input_files/health.pdf')
        )
    )