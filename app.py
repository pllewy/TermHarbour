from flask import Flask, render_template, request
import os

from static.alignment import align, align_sentences
from static.extraction_01 import read_text_from_file, post_process_terms
from static.upload import save_file, get_glossary_names
from static.extraction_01 import read_text_from_file, post_process_terms, preprocess_text, load_spacy_model, extract_specialist_terms_with_patterns, combine_term_lists, extract_ner_terms

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def main_page():
    if request.method == 'POST':
        source_text = request.form['source_text']
        target_text = request.form['target_text']
        source_language = request.form['source_language']
        target_language = request.form['target_language']

        print(source_text, target_text, source_language, target_language)
        aligned = align_sentences(source_text, target_text, print_input=True, print_output=True)

        return render_template('main_page.html',
                               source_text=source_text, source_language=source_language,
                               target_text=target_text, target_language=target_language)
    else:
        return render_template('main_page.html',
                               source_text="", source_language="en",
                               target_text="", target_language="es")


@app.route('/dictionary')
def dictionary():
    return ('<div>Dictionary tab.</div>'
            '<a href="/" >Press here to go back to main menu</>')


@app.route('/glossary')
def glossary():
    file_contents = []

    database_dir = './glossaries'

    # Iterate over all files in the database directory
    for filename in os.listdir(database_dir):
        # Check if the file is a regular file
        if os.path.isfile(os.path.join(database_dir, filename)) and filename.endswith('.txt'):
            with open(os.path.join(database_dir, filename), 'r') as file:
                # Read the file line by line
                lines = file.readlines()

                # Split the lines and remove any leading or trailing whitespace
                lines = [line.strip() for line in lines]

                # Append the file contents to the list
                file_contents.append((filename, lines))

    return render_template('glossaries.html', file_contents=file_contents)


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        source_lang = 'en'  # input("Enter the source language (en, pl, es): ")
        target_lang = 'pl'  # input("Enter the target language (en, pl, es): ")

        # STEP 1: Extract the data from the request
        language = request.form['language']
        domain = request.form['domain']
        source_file = request.files['file']

        if source_file.filename == '':
            return 'No selected file', 400
        print(language, domain)

        save_path = save_file(request.files['file'])
        save_path_2 = save_file(request.files['target_file'])

        # STEP 2: Process the data
        file_path = save_path
        file_path_2 = save_path_2

        nlp = load_spacy_model(source_lang)
        text = read_text_from_file(file_path)
        text_preprocessed = preprocess_text(text)
        terms_ner = extract_ner_terms(text, nlp)
        terms_pattern = extract_specialist_terms_with_patterns(text_preprocessed, nlp)
        post_process_terms(terms_pattern)
        final_terms = combine_term_lists(terms_pattern, terms_ner)

        text2 = read_text_from_file(file_path_2)

        extracted_terms2 = extract_and_translate_terms_with_patterns(text2, source_lang, target_lang)
        terms2 = post_process_terms(extracted_terms2)

        # STEP 3: Align the terms
        alignment = align(final_terms, terms2)

        terms_dict = {
            'source_terms': final_terms,
            'target_terms': terms2,
            'alignment': alignment
        }

        return terms_dict, 200

    # If the request method is GET, return the upload page with the list of glossaries
    glossary_files = get_glossary_names()

    return render_template('upload.html', glossary_files=glossary_files)


if __name__ == '__main__':
    app.run(debug=True)
