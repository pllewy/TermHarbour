# Author: Maurycy Oprus

import static.extraction_01 as extraction
from lbl2vec import Lbl2Vec, Lbl2TransformerVec
from gensim.models.doc2vec import TaggedDocument


def clean_text(file_path):

    text = extraction.read_text_from_file(file_path)
    extracted_terms = extraction.preprocess_text(text)

    print(extracted_terms.lower())
    return extracted_terms.lower()


def text_categorization(category, language, text):
    if category == 'medicine':
        if language == 'english':
            # learning input: https://github.com/sebischair/Medical-Abstracts-TC-Corpus
            model = Lbl2Vec.load('models/Lbl2Vec/Lbl2Vec_med_simple_2')
    elif category == 'art':
        if language == 'english':
            # learning input: https://www.kaggle.com/datasets/mannacharya/aeon-essays-dataset
            model = Lbl2Vec.load('models/Lbl2Vec/Lbl2Vec_art_simple')
    elif category == 'news':
        if language == 'english':
            # learning input: https://www.kaggle.com/datasets/sunilthite/text-document-classification-dataset
            model = Lbl2Vec.load('models/Lbl2Vec/Lbl2Vec_broad_simple')
    elif category == "environment":
        if language == 'english':
            # learning input: https://www.kaggle.com/datasets/beridzeg45/guardian-environment-related-news
            model = Lbl2Vec.load(
                'models/Lbl2Vec/Lbl2Vec_environment_simple')

    # print(model.predict_new_docs(documents=[text]))
    print(model.predict_new_docs(tagged_docs=[TaggedDocument(text.split(" "), ['0'])]).iloc[0])
    cat_values = model.predict_new_docs(tagged_docs=[TaggedDocument(text.split(" "), ['0'])]).iloc[0]

    threshold = cat_values['highest_similarity_score'] * 0.8

    top_categories = []
    for label, score in cat_values.items():
        if label not in ["doc_key", "most_similar_label", "highest_similarity_score"]:
            if score > threshold:
                top_categories.append((label, score))

    # Sorting in descending order
    top_categories = sorted(top_categories, key=lambda x: x[1], reverse=True)

    if len(top_categories) > 4:
        top_categories = top_categories[:4]

    return [category for category, score in top_categories]


if __name__ == "__main__":
    # text_categorization(
    #     'medicine',
    #     'en',
    #     txt_1
    # )

    print(
        text_categorization(
            'medicine',
            'en',
            clean_text('C:/Users/Mauri/Desktop/main_repo/TermHarbour/input_files/health.pdf')
        )
    )
