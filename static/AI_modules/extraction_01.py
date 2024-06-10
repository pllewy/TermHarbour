# Author: Sebastian Piotrowski

from translate import Translator
import spacy
from spacy.matcher import Matcher
import PyPDF2
import re
import csv
from collections import Counter

from static.timer import measure_time


def load_spacy_model(language_code):
    """
    Loads a Spacy model based on the provided language code.

    Args:
        language_code (str): The language code for the Spacy model to be loaded.

    Returns:
        spacy.lang: The loaded Spacy model.
    """
    if language_code == 'en' or language_code == 'english':
        return spacy.load("en_core_web_lg")
    elif language_code == 'pl' or language_code == 'polish':
        return spacy.load("pl_core_news_lg")
    elif language_code == 'es' or language_code == 'spanish':
        return spacy.load("es_core_news_lg")
    else:
        raise ValueError("Unsupported language code")


def preprocess_text(text):
    """
    Preprocesses the provided text by removing newline characters, references, standalone numbers, hyperlinks, special characters, non-ascii characters, and words containing digits.

    Args:
        text (str): The text to be preprocessed.

    Returns:
        str: The preprocessed text.
    """

    # Replace newline characters with a space
    text = text.replace('\n', ' ')

    # # remove commas - TODO new, check if it is necessary
    # text = text.replace(',', '')
    # text = text.replace('.', '')

    # Remove references like [1], [2-4], [5,6], etc.
    text = re.sub(r'\[\d+–\d+\]|\[\d+(,\d+)*\]', '', text)

    # Remove any standalone numbers (e.g., dates, page numbers)
    text = re.sub(r'\b\d+\b', '', text)

    # Remove hyperlinks
    text = re.sub(r'http[s]?://\S+', '', text)

    # Remove special characters except Polish and Spanish letters
    text = re.sub(r'[^a-zA-Z0-9\sąćęłńóśźżĄĆĘŁŃÓŚŹŻáéíóúüñÁÉÍÓÚÜÑ]', '', text)

    # Normalize spaces to a single space
    text = re.sub(r'\s+', ' ', text).strip()

    # Remove words that contain any digits
    text = re.sub(r'\b\w*\d\w*\b', '', text)

    return text


@measure_time
def read_text_from_file(file_path):
    """
    Reads text from a file based on its file type.

    Args:
        file_path (str): The path to the file to be read.

    Returns:
        str: The text read from the file.
    """
    if file_path.endswith('.txt'):
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    elif file_path.endswith('.pdf'):
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ''
            for page_num in range(len(pdf_reader.pages)):
                text += pdf_reader.pages[page_num].extract_text()
            return text
    elif file_path.endswith('.csv'):
        with open(file_path, 'r', newline='', encoding='utf-8') as file:
            text = file.read()
            reader = csv.reader(file)
            try:
                next(reader)  # Skip header if it exists
            except StopIteration:
                pass  # Do nothing if there are no more lines
            for row in reader:
                text += row[0] + ' '  # assuming the text is in the first column
            return text
    else:
        raise ValueError("Unsupported file format")


def lemmatize_terms(terms, nlp):
    """
    Lemmatizes the provided terms using the provided Spacy model.

    Args:
        terms (list): The terms to be lemmatized.
        nlp (spacy.lang): The Spacy model to be used for lemmatization.

    Returns:
        dict: A dictionary mapping the original terms to their lemmatized forms.
    """
    lemmatized_terms = {}
    for term in terms:
        doc = nlp(term)
        lemmatized_terms[term] = ' '.join([token.lemma_ for token in doc])
    return lemmatized_terms


def extract_specialist_terms_with_patterns(text, nlp):
    """
    Extracts specialist terms from the provided text using the provided Spacy model and predefined patterns.

    Args:
        text (str): The text from which to extract specialist terms.
        nlp (spacy.lang): The Spacy model to be used for extraction.

    Returns:
        list: A list of extracted specialist terms.
    """
    specialist_terms = []
    max_length = nlp.max_length  # Get the maximum length allowed by spaCy
    for i in range(0, len(text), max_length):
        chunk = text[i:i + max_length]
        doc = nlp(chunk)
        matcher = Matcher(nlp.vocab)
        patterns = [
            # Pattern 1: adjective or noun followed by noun
            [{"POS": {"IN": ["ADJ", "NOUN"]}, "OP": "*", "IS_PUNCT": False}, {"POS": "NOUN"}],
            # Pattern 2: adjective or noun followed by adposition, optional determiner, adjective or noun, and noun
            [{"POS": {"IN": ["ADJ", "NOUN"]}, "OP": "+", "IS_PUNCT": False},
             {"POS": "ADP", "IS_PUNCT": False}, {"POS": "DET", "OP": "?", "IS_PUNCT": False},
             {"POS": {"IN": ["ADJ", "NOUN"]}, "OP": "*", "IS_PUNCT": False}, {"POS": "NOUN"}],
            # Pattern 3: adjective or noun followed by zero or more adjectives, nouns, determiners, or adpositions, and adjective or noun
            [{"POS": {"IN": ["ADJ", "NOUN"]}, "IS_PUNCT": False},
             {"POS": {"IN": ["ADJ", "NOUN", "DET", "ADP"]}, "OP": "*", "IS_PUNCT": False},
             {"POS": {"IN": ["ADJ", "NOUN"]}, "IS_PUNCT": False}]
        ]

        for pattern in patterns:
            matcher.add("SPECIALIST_TERM", [pattern])

        matches = matcher(doc)

        for match_id, start, end in matches:
            span = doc[start:end]
            term = ' '.join([token.text for token in span]).lower()
            # part_of_speech = ' '.join([token.pos_ for token in span])
            # print(term, part_of_speech)
            specialist_terms.append(term.replace(' ', '_'))

    return specialist_terms



def extract_ner_terms(text, nlp):
    """
    Extracts named entity recognition (NER) terms from the provided text using the provided Spacy model.

    Args:
        text (str): The text from which to extract NER terms.
        nlp (spacy.lang): The Spacy model to be used for extraction.

    Returns:
        list: A list of extracted NER terms.
    """
    ner_terms = []
    max_length = nlp.max_length  # Get the maximum length allowed by spaCy
    for i in range(0, len(text), max_length):
        chunk = text[i:i + max_length]
        doc = nlp(chunk)
        ner_terms.extend([ent.text.replace(' ', '_') for ent in doc.ents if ent.label_ in ["ORG", "PERSON", "GPE", "EVENT", "WORK_OF_ART"]])
    return ner_terms


def combine_term_lists(terms_pattern, terms_ner):
    """
    Combines two lists of terms into one.

    Args:
        terms_pattern (list): The first list of terms.
        terms_ner (list): The second list of terms.

    Returns:
        list: The combined list of terms.
    """
    final_terms = []

    final_terms = terms_pattern + terms_ner

    return final_terms


def post_process_terms(terms):
    """
    Post-processes a list of terms by keeping only those that appear more than once and do not match a certain pattern.

    Args:
        terms (list): The list of terms to be post-processed.

    Returns:
        list: The post-processed list of terms.
    """
    term_counts = Counter(terms)
    processed_terms = [term for term in term_counts if term_counts[term] > 0 and not re.match(r'^\d+[a-z]*$', term)]
    return processed_terms
