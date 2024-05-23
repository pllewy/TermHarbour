from flask import Flask, render_template, request
import os

from extraction_01 import read_text_from_file, post_process_terms, preprocess_text, load_spacy_model, extract_specialist_terms_with_patterns, combine_term_lists, extract_ner_terms

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def main_page():
    if request.method == 'POST':
        text = request.form['text']
        source_language = request.form['source']
        target_language = request.form['target']
        return render_template('main_page.html', x=[1, 2, 3, 4], text=text, source_language=source_language,
                               target_language=target_language)
    else:
        return render_template('main_page.html', x=[1, 2, 3, 4], text="", source_language="", target_language="")


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
        language = request.form['language']
        domain = request.form['domain']
        source_file = request.files['file']

        if source_file.filename == '':
            return 'No selected file', 400
        print(language, domain)

        save_path = os.path.join('.', 'input_files', source_file.filename)
        source_file.save(save_path)

        file_path = save_path
        source_lang = 'en'  # input("Enter the source language (en, pl, es): ")
        target_lang = 'pl'  # input("Enter the target language (en, pl, es): ")

        nlp = load_spacy_model(source_lang)
        text = read_text_from_file(file_path)
        text_preprocessed = preprocess_text(text)
        terms_ner = extract_ner_terms(text, nlp)
        terms_pattern = extract_specialist_terms_with_patterns(text_preprocessed, nlp)
        post_process_terms(terms_pattern)
        final_terms = combine_term_lists(terms_pattern, terms_ner)

        terms_dict = {}
        terms_dict['content'] = final_terms

        return terms_dict, 200

    glossary_files = []

    database_dir = './glossaries'

    for filename in os.listdir(database_dir):
        if os.path.isfile(os.path.join(database_dir, filename)):
            with open(os.path.join(database_dir, filename), 'r') as file:
                # Append the file contents to the list
                glossary_files.append(filename)

    file_contents = "Hello world"

    return render_template('upload.html', file_contents=file_contents, glossary_files=glossary_files)


@app.route('/test')
def test():
    
    file_path = 'health.pdf'
    source_lang = 'en'  # input("Enter the source language (en, pl, es): ")
    target_lang = 'pl'  # input("Enter the target language (en, pl, es): ")
    
    nlp = load_spacy_model(source_lang)
    text = read_text_from_file(file_path)
    text = read_text_from_file(file_path)
    text_preprocessed = preprocess_text(text)
    terms_ner = extract_ner_terms(text, nlp)
    terms_pattern = extract_specialist_terms_with_patterns(text_preprocessed, nlp)
    post_process_terms(terms_pattern)
    final_terms = combine_term_lists(terms_pattern, terms_ner)

    glossary_files = os.listdir('./glossaries')

    return render_template('test.html', glossary_files=glossary_files, test_text=final_terms)


if __name__ == '__main__':
    app.run(debug=True)
