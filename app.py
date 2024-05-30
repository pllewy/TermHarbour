import sqlite3

from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text

from static.alignment import align, align_sentences
from static.upload import save_file, get_glossary_names
from static.extraction_01 import (read_text_from_file, post_process_terms, preprocess_text, load_spacy_model,
                                  extract_specialist_terms_with_patterns,  combine_term_lists, extract_ner_terms)
from static.classification import text_categorization
import os
import warnings
warnings.filterwarnings("ignore", category=FutureWarning, module='huggingface_hub')

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'glossary.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Glossary(db.Model):
    __tablename__ = 'medicine'
    english = db.Column(db.String(80), primary_key=True)
    spanish = db.Column(db.String(80), nullable=True)
    polish = db.Column(db.String(80), nullable=True)
    categories = db.Column(db.String(255), nullable=True)


@app.route('/', methods=['GET', 'POST'])
def main_page():
    if request.method == 'POST':
        source_text = request.form['source_text']
        target_text = request.form['target_text']
        source_language = request.form['source_language']
        target_language = request.form['target_language']

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


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        source_lang = 'english'
        target_lang = request.form.get('language')

        # language = request.form['language']
        domain = request.form.get('domain')
        source_file = request.files['file']
        target_file = request.files.get('target_file')

        if not source_file or source_file.filename == '':
            return jsonify({'error': 'No source file selected'}), 400

        if not target_file or target_file.filename == '':
            return jsonify({'error': 'No target file selected'}), 400


        save_path = save_file(request.files['file'])
        save_path_2 = save_file(request.files['target_file'])

        file_path = save_path
        file_path_2 = save_path_2

        nlp = load_spacy_model(source_lang)
        text = read_text_from_file(file_path)
        categories = text_categorization(domain, source_lang, text)
        text_preprocessed = preprocess_text(text)
        terms_ner = extract_ner_terms(text, nlp)
        terms_pattern = extract_specialist_terms_with_patterns(text_preprocessed, nlp)
        terms_pattern = post_process_terms(terms_pattern)
        final_terms = combine_term_lists(terms_pattern, terms_ner)

        nlp_2 = load_spacy_model(target_lang)
        text2 = read_text_from_file(file_path_2)
        text_preprocessed_2 = preprocess_text(text2)
        terms_ner_2 = extract_ner_terms(text2, nlp_2)
        terms_pattern_2 = extract_specialist_terms_with_patterns(text_preprocessed_2, nlp_2)
        terms_pattern_2 = post_process_terms(terms_pattern_2)
        final_terms_2 = combine_term_lists(terms_pattern_2, terms_ner_2)

        alignment = align(final_terms, final_terms_2)

        terms_dict = {
            'alignment': alignment,
            'categories': categories
        }

        return terms_dict, 200

    glossary_files = get_glossary_names()

    return render_template('upload.html', glossary_files=glossary_files)


@app.route('/tables', methods=['GET'])
def get_tables():
    conn = sqlite3.connect(os.path.join(basedir, 'glossary.db'))
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    conn.close()
    return jsonify([table[0] for table in tables])


@app.route('/categorize', methods=['POST'])
def categorize_text():
    data = request.json
    category = data.get('category')
    language = data.get('language')
    text = data.get('text')

    if not category or not language or not text:
        return jsonify({'error': 'Invalid input'}), 400

    categories = text_categorization(category, language, text)
    return jsonify({'categories': categories})

@app.route('/glossary')
def glossary():
    table_name = request.args.get('table', 'medicine')
    records = db.session.execute(text(f'SELECT * FROM {table_name}')).fetchall()
    return render_template('glossary.html', records=records, table=table_name)


@app.route('/add', methods=['POST'])
def add_record():
    table_name = request.form['table']
    english = request.form['english']
    spanish = request.form.get('spanish')
    polish = request.form.get('polish')
    categories = request.form.get('categories')

    existing_record = db.session.execute(text(f'SELECT * FROM {table_name} WHERE english = :english'), {'english': english}).fetchone()
    if existing_record:
        return jsonify({'result': 'error', 'message': 'The English word already exists in the table.'})

    db.session.execute(
        text(f'INSERT INTO {table_name} (english, spanish, polish, categories) VALUES (:english, :spanish, :polish, :categories)'),
        {'english': english, 'spanish': spanish, 'polish': polish, 'categories': categories})
    db.session.commit()
    return jsonify({'result': 'success'})


@app.route('/edit/<string:english>', methods=['POST'])
def edit_record(english):
    table_name = request.form['table']
    new_english = request.form['new_english']
    spanish = request.form['spanish']
    polish = request.form['polish']
    categories = request.form['categories']

    if new_english != english:
        existing_record = db.session.execute(text(f'SELECT * FROM {table_name} WHERE english = :new_english'), {'new_english': new_english}).fetchone()
        if existing_record:
            return jsonify({'result': 'error', 'message': 'The new English word already exists in the table.'})

    db.session.execute(
        text(f'UPDATE {table_name} SET english = :new_english, spanish = :spanish, polish = :polish, categories = :categories WHERE english = :english'),
        {'new_english': new_english, 'spanish': spanish, 'polish': polish, 'categories': categories, 'english': english})
    db.session.commit()
    return jsonify({'result': 'success'})


@app.route('/delete/<string:english>', methods=['POST'])
def delete_record(english):
    table_name = request.form['table']
    db.session.execute(text(f'DELETE FROM {table_name} WHERE english = :english'), {'english': english})
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
