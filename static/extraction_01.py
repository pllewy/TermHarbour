from translate import Translator
import spacy
from spacy.matcher import Matcher
import PyPDF2
import re
import csv
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
from nltk import sent_tokenize

def load_spacy_model(language_code):
    if language_code == 'en' or language_code == 'english':
        return spacy.load("en_core_web_sm")
    elif language_code == 'pl' or language_code == 'polish':
        return spacy.load("pl_core_news_sm")
    elif language_code == 'es' or language_code == 'spanish':
        return spacy.load("es_core_news_sm")
    else:
        raise ValueError("Unsupported language code")

def preprocess_text(text):
    # Replace newline characters with a space
    text = text.replace('\n', ' ')
    
    # Remove references like [1], [2-4], [5,6], etc.
    text = re.sub(r'\[\d+–\d+\]|\[\d+(,\d+)*\]', '', text)
    
    # Remove any standalone numbers (e.g., dates, page numbers)
    text = re.sub(r'\b\d+\b', '', text)
    
    # Remove hyperlinks
    text = re.sub(r'http[s]?://\S+', '', text)
    
    # Remove special characters
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    
    # Normalize spaces to a single space
    text = re.sub(r'\s+', ' ', text).strip()
    
    # Remove non ascii
    text = re.sub(r'[^\x00-\x7F]+', ' ', text)
    
    # Remove words that contain any digits
    text = re.sub(r'\b\w*\d\w*\b', '', text)
    
    return text

def read_text_from_file(file_path):
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
    lemmatized_terms = {}
    for term in terms:
        doc = nlp(term)
        lemmatized_terms[term] = ' '.join([token.lemma_ for token in doc])
    return lemmatized_terms


def extract_specialist_terms_with_patterns(text, nlp):
    doc = nlp(text)
    specialist_terms = []

    matcher = Matcher(nlp.vocab)
    patterns = [
        # Pattern 1: adjective or noun followed by noun
        [{"POS": {"IN": ["ADJ", "NOUN"]}, "OP": "*", "IS_PUNCT": False},
         {"POS": "NOUN"}],
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
        term = ' '.join([token.lemma_ for token in span]).lower()
        specialist_terms.append(term.replace(' ', '_'))

    return specialist_terms

def extract_ner_terms(text, nlp):
    ner_terms = []
    doc = nlp(text)
    ner_terms = [ent.text.replace(' ','_') for ent in doc.ents if ent.label_ in ["ORG", "PERSON", "GPE", "EVENT", "WORK_OF_ART"]]
    return ner_terms

def combine_term_lists(terms_pattern, terms_ner):
    final_terms = []
    
    final_terms = terms_pattern + terms_ner

    return final_terms

def post_process_terms(terms):
    terms = [term for term in terms if terms.count(term) > 1]  # Keep terms that appear more than once
    terms = [term for term in terms if not re.match(r'^\d+[a-z]*$', term)]  # Ignore terms like "d4", "400th"

    return terms
