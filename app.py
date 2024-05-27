from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text

from static.alignment import align, align_sentences
from static.upload import save_file, get_glossary_names
from static.extraction_01 import (read_text_from_file, post_process_terms, preprocess_text, load_spacy_model,
                                  extract_specialist_terms_with_patterns,  combine_term_lists, extract_ner_terms)
# from static.classification import text_categorization
import os
import warnings
warnings.filterwarnings("ignore", category=FutureWarning, module='huggingface_hub')

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'glossary.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


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


# @app.route('/glossary')
# def glossary():
#     file_contents = []
#
#     database_dir = './glossaries'
#
#     # Iterate over all files in the database directory
#     for filename in os.listdir(database_dir):
#         # Check if the file is a regular file
#         if os.path.isfile(os.path.join(database_dir, filename)) and filename.endswith('.txt'):
#             with open(os.path.join(database_dir, filename), 'r') as file:
#                 # Read the file line by line
#                 lines = file.readlines()
#
#                 # Split the lines and remove any leading or trailing whitespace
#                 lines = [line.strip() for line in lines]
#
#                 # Append the file contents to the list
#                 file_contents.append((filename, lines))
#
#     return render_template('glossaries.html', file_contents=file_contents)


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
        terms_pattern = post_process_terms(terms_pattern)
        final_terms = combine_term_lists(terms_pattern, terms_ner)


        nlp_2 = load_spacy_model(target_lang)
        text2 = read_text_from_file(file_path_2)
        text_preprocessed_2 = preprocess_text(text2)
        terms_ner_2 = extract_ner_terms(text2, nlp)
        terms_pattern_2 = extract_specialist_terms_with_patterns(text_preprocessed_2, nlp_2)
        terms_pattern_2 = post_process_terms(terms_pattern_2)
        final_terms_2 = combine_term_lists(terms_pattern_2, terms_ner_2)

        # STEP 3: Align the terms
        alignment = align(final_terms, final_terms_2)

        terms_dict = {
            'source_terms': final_terms,
            'target_terms': final_terms_2,
            'alignment': alignment
        }

        return terms_dict, 200

    # If the request method is GET, return the upload page with the list of glossaries
    glossary_files = get_glossary_names()

    return render_template('upload.html', glossary_files=glossary_files)

class Glossary(db.Model):
    __tablename__ = 'medicine'  # Default table

    id = db.Column(db.Integer, primary_key=True)
    english = db.Column(db.String(80), nullable=False)
    spanish = db.Column(db.String(80), nullable=False)
    polish = db.Column(db.String(80), nullable=False)


@app.route('/glossary')
def glossary():
    table_name = request.args.get('table', 'medicine')
    records = db.session.execute(text(f'SELECT * FROM {table_name}')).fetchall()
    return render_template('glossary.html', records=records, table=table_name)


@app.route('/add', methods=['POST'])
def add_record():
    table_name = request.form['table']
    english = request.form['english']
    spanish = request.form['spanish']
    polish = request.form['polish']
    db.session.execute(
        text(f'INSERT INTO {table_name} (english, spanish, polish) VALUES (:english, :spanish, :polish)'),
        {'english': english, 'spanish': spanish, 'polish': polish})
    db.session.commit()
    return redirect(url_for('glossary', table=table_name))


@app.route('/edit/<int:id>', methods=['POST'])
def edit_record(id):
    table_name = request.form['table']
    english = request.form['english']
    spanish = request.form['spanish']
    polish = request.form['polish']
    db.session.execute(
        text(f'UPDATE {table_name} SET english = :english, spanish = :spanish, polish = :polish WHERE id = :id'),
        {'english': english, 'spanish': spanish, 'polish': polish, 'id': id})
    db.session.commit()
    return redirect(url_for('glossary', table=table_name))


@app.route('/delete/<int:id>', methods=['POST'])
def delete_record(id):
    table_name = request.form['table']
    db.session.execute(text(f'DELETE FROM {table_name} WHERE id = :id'), {'id': id})
    db.session.commit()
    return jsonify({'result': 'success'})


@app.route('/initialize')
def initialize():
    with app.app_context():
        db.create_all()
        db.session.commit()
    return "Database initialized!"


if __name__ == '__main__':
    app.run(debug=True)
