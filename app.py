import sqlite3

from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text

from static.AI_modules.alignment import align, align_sentences
from static.upload.upload import save_file
from static.AI_modules.extraction_01 import (read_text_from_file, post_process_terms, preprocess_text, load_spacy_model,
                                  extract_specialist_terms_with_patterns,  combine_term_lists, extract_ner_terms)
from static.AI_modules.classification import text_categorization
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
        source_text = request.form['source_text'].split()
        target_text = request.form['target_text'].split()
        source_language = request.form['source_language']
        target_language = request.form['target_language']

        aligned = align_sentences(source_text, target_text)

        for pair in aligned['mwmf']:
            source_text[pair[0]] = f'<span style="color: green;">{source_text[pair[0]]}</span>'
            target_text[pair[1]] = f'<span style="color: green;">{target_text[pair[1]]}</span>'

        source_terms = extract_terms(request.form['source_text'], source_language)
        target_terms = extract_terms(request.form['target_text'], target_language)

        tag_terms(source_terms, source_text)
        tag_terms(target_terms, target_text)

        response_dict = {
            'source_language': source_language,
            'source_text': source_text,
            'target_language': target_language,
            'target_text': target_text,
        }

        return response_dict, 200
    else:
        return render_template('main_page.html',
                               source_text="", source_language="en",
                               target_text="", target_language="es")

def tag_terms(terms, text):
    for word in terms:
        if f'<span style="color: green;">{word}</span>' not in text:
            text.append(f'<span style="color: red;">{word}</span>')
    text.append('<br>')


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        source_lang = 'english'
        target_lang = request.form.get('language')
        domain = request.form.get('domain')
        source_file = request.files['file']
        target_file = request.files.get('target_file')

        if not source_file or source_file.filename == '':
            return jsonify({'error': 'No source file selected'}), 400

        if not target_file or target_file.filename == '':
            return jsonify({'error': 'No target file selected'}), 400

        source_file_path = save_file(source_file)
        target_file_path = save_file(target_file)

        source_text = read_text_from_file(source_file_path)
        target_text = read_text_from_file(target_file_path)

        source_terms = extract_terms(source_text, source_lang)
        target_terms = extract_terms(target_text, target_lang)

        alignment = align(source_terms, target_terms)

        terms_dict = {
            'alignment': alignment,
            'categories': text_categorization(domain, source_lang, source_text)
        }

        return terms_dict, 200

    return render_template('upload.html')

def extract_terms(text, lang):
    nlp = load_spacy_model(lang)
    text_preprocessed = preprocess_text(text)
    terms_ner = extract_ner_terms(text, nlp)
    terms_pattern = extract_specialist_terms_with_patterns(text_preprocessed, nlp)
    terms_pattern = post_process_terms(terms_pattern)
    return combine_term_lists(terms_pattern, terms_ner)


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
