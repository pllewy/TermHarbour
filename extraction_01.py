from translate import Translator
import spacy
from spacy.matcher import Matcher
import PyPDF2
import re

def load_spacy_model(language_code):
    if language_code == 'en':
        return spacy.load("en_core_web_sm")
    elif language_code == 'pl':
        return spacy.load("pl_core_news_sm")
    elif language_code == 'es':
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

    return text

def lemmatize_terms(terms, nlp):
    lemmatized_terms = {}
    for term in terms:
        doc = nlp(term)
        lemmatized_terms[term] = ' '.join([token.lemma_ for token in doc])
    return lemmatized_terms


def translate_terms(terms, target_lang):
    translator = Translator(to_lang=target_lang)
    translated_terms = {}

    for term in terms:
        translation = translator.translate(term)
        translated_terms[term] = translation

    return translated_terms

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
    else:
        raise ValueError("Unsupported file format")

def extract_specialist_terms_with_patterns(text, nlp):
    
    text = preprocess_text(text)
    doc = nlp(text)
    specialist_terms = []

    # Initialize Matcher with the current spaCy model's vocabulary
    matcher = Matcher(nlp.vocab)

    # Define patterns
    patterns = [
        # Pattern 1: adjective
        #[{"POS": "ADJ", "IS_PUNCT": False}],
        # Pattern 2: adjective or noun followed by noun
        [{"POS": {"IN": ["ADJ", "NOUN"]}, "OP": "*", "IS_PUNCT": False}, 
         {"POS": "NOUN"}],
        # Pattern 3: adjective or noun followed by adposition, optional determiner, adjective or noun, and noun  
        [{"POS": {"IN": ["ADJ", "NOUN"]}, "OP": "+", "IS_PUNCT": False}, 
         {"POS": "ADP", "IS_PUNCT": False},
         {"POS": "DET", "OP": "?", "IS_PUNCT": False},
         {"POS": {"IN": ["ADJ", "NOUN"]}, "OP": "*", "IS_PUNCT": False},
         {"POS": "NOUN"}],
        # Pattern 4: adjective or noun followed by zero or more adjectives, Nouns, determiners, or adpositions, and adjective or noun  
        [{"POS": {"IN": ["ADJ", "NOUN"]}, "IS_PUNCT": False},  
         {"POS": {"IN": ["ADJ", "NOUN", "DET", "ADP"]}, "OP": "*", "IS_PUNCT": False},
         {"POS": {"IN": ["ADJ", "NOUN"]}, "IS_PUNCT": False}], 
        #[{"ENT_TYPE": {"IN": ["ORG", "PERSON", "GPE", "EVENT", "WORK_OF_ART"]}}],  # Pattern 5: named entities of specified types
        #[{"ENT_TYPE": {"IN": ["ORG", "PERSON", "GPE", "EVENT", "WORK_OF_ART"]}, "OP": "+"}] # Pattern 6: named entities of specified types added together
    ]
#
    for pattern in patterns:
        matcher.add("SPECIALIST_TERM", [pattern])

    matches = matcher(doc)

    for match_id, start, end in matches:
        span = doc[start:end]
        lemmatized_term = ' '.join([token.lemma_ for token in span])
        specialist_terms.append(lemmatized_term.lower().replace(' ','_'))

    return specialist_terms

def extract_and_translate_terms_with_patterns(text, source_lang, target_lang):
    nlp_source = load_spacy_model(source_lang)
    
    # Extract terms using the pattern-based extractor
    terms = extract_specialist_terms_with_patterns(text, nlp_source)
    
    # Lemmatize the extracted terms using the source language model
    #lemmatized_terms = lemmatize_terms(terms, nlp_source)

    # Translate lemmatized terms into the target language
    #translated_terms = translate_terms(lemmatized_terms.values(), target_lang)

    return terms #, lemmatized_terms #, translated_terms

def post_process_terms(terms):
    #terms = [term for term in terms if 3 <= len(term.split('_')) <= 10]  # Filter by length
    terms = [term for term in terms if terms.count(term) > 1]  # Keep terms that appear more than once
    terms = [term for term in terms if not re.match(r'^\d+[a-z]*$', term)]  # Ignore terms like "d4", "400th"
    
    return terms
#
# file_path = 'health.pdf'
# source_lang = 'en' #input("Enter the source language (en, pl, es): ")
# target_lang = 'pl' #input("Enter the target language (en, pl, es): ")
#
# text = read_text_from_file(file_path)
#
# extracted_terms = extract_and_translate_terms_with_patterns(text, source_lang, target_lang)
# terms = post_process_terms(extracted_terms)
# print("Extracted Terms:", terms)
# #print("Translated Terms:", translated_terms)