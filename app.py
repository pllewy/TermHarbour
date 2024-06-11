import sqlite3

from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text

from static.AI_modules.alignment import align, full_alignment_process

from static.upload.upload import save_file
from static.AI_modules.extraction_01 import (read_text_from_file, post_process_terms, preprocess_text, load_spacy_model,
                                             extract_specialist_terms_with_patterns, combine_term_lists,
                                             extract_ner_terms)
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
        source_text = request.form['source_text']
        target_text = request.form['target_text']
        source_language = request.form['source_language']
        target_language = request.form['target_language']

        source_text_words = preprocess_text(source_text).split(' ')
        target_text_words = preprocess_text(target_text).split(' ')

        print(source_text_words)
        print(source_text_words)

        result_term_list, source_terms, target_terms = full_alignment_process(source_text, target_text, source_language, target_language)

        for term in result_term_list:
            for i in range(len(term[1])):
                if term[1][i][-1] == ' ':
                    term[1][i] = term[1][i][:-1]

        # words_set is in form [english, [target1, target2, ...]]

        for i in range(len(source_text_words)):
            if source_text_words[i] in source_terms:
                print("FOUND A TERM IN SOURCE TEXT", source_text_words[i])
                term_flag = False
                for term in result_term_list:
                    if term[0] == source_text_words[i]:
                        # blue
                        source_text_words[i] = f'<span style="color: #0353A4;">{source_text_words[i]}</span>'
                        term_flag = True
                        break
                if not term_flag:
                    # red 96031A
                    source_text_words[i] = f'<span style="color: #BF0603; font-size: 20px;">{source_text_words[i]}</span>'

        for i in range(len(target_text_words)):
            if target_text_words[i] in target_terms:
                print("FOUND A TERM IN TARGET TEXT", target_text_words[i])
                term_flag = False
                for term in result_term_list:
                    if target_text_words[i] in term[1]:
                        # blue
                        target_text_words[i] = f'<span style="color: #0353A4;">{target_text_words[i]}</span>'
                        term_flag = True
                        break
                if not term_flag:
                    # gold E8C547
                    target_text_words[i] = f'<span style="color: #FAA916; font-size: 20px;">{target_text_words[i]}</span>'


        print("\n\n", result_term_list)
        print("SOURCE TEXT: ", source_text_words)
        print("TARGET TEXT: ", target_text_words)

        response_dict = {
            'source_language': source_language,
            'source_text': source_text_words,
            'target_language': target_language,
            'target_text': target_text_words,
        }

        print("DONE")
        return response_dict, 200
    else:
        return render_template('main_page.html',
                               source_text="", source_language="en",
                               target_text="", target_language="pl")


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    # batching_method - TEXT or PARAGRAPH
    batching_method = 'TEXT'

    # Get files from web form
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

        # Save files
        source_file_path = save_file(source_file)
        target_file_path = save_file(target_file)

        try:
            source_text = read_text_from_file(source_file_path)
        except ValueError as e:
            return jsonify({'error': f'Error reading source file: {str(e)}'}), 400

        try:
            target_text = read_text_from_file(target_file_path)
        except ValueError as e:
            return jsonify({'error': f'Error reading target file: {str(e)}'}), 400

        result_term_list, source_terms, target_terms = full_alignment_process(source_text, target_text, source_lang, target_lang, batching_method)

        terms_dict = {
            'alignment': result_term_list,
            'categories': text_categorization(domain, source_lang, source_text)
        }

        return terms_dict, 200

    return render_template('upload.html')


@app.route('/add_to_glossary', methods=['POST'])
def add_to_glossary():
    data = request.json
    category = data['category']
    translations = data['translations']

    # Ensure the table exists
    table_exists = db.session.execute(text(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{category}'")).fetchone()
    if not table_exists:
        # Create the table dynamically if it does not exist
        db.session.execute(text(f"""
            CREATE TABLE {category} (
                english TEXT PRIMARY KEY,
                spanish TEXT,
                polish TEXT,
                categories TEXT
            )
        """))

    for translation in translations:
        english = translation['english']
        spanish = translation['spanish']
        polish = translation['polish']
        categories = translation['categories']

        existing_record = db.session.execute(text(f"SELECT * FROM {category} WHERE english = :english"), {'english': english}).fetchone()
        if existing_record:
            if spanish and (not existing_record[1] or existing_record[1] != spanish):
                updated_spanish = f"{existing_record[1]}, {spanish}" if existing_record[1] else spanish
                db.session.execute(text(f"UPDATE {category} SET spanish = :spanish WHERE english = :english"), {'spanish': updated_spanish, 'english': english})
            if polish and (not existing_record[2] or existing_record[2] != polish):
                updated_polish = f"{existing_record[2]}, {polish}" if existing_record[2] else polish
                db.session.execute(text(f"UPDATE {category} SET polish = :polish WHERE english = :english"), {'polish': updated_polish, 'english': english})
            if categories and (not existing_record[3] or existing_record[3] != categories):
                updated_categories = f"{existing_record[3]}, {categories}" if existing_record[3] else categories
                db.session.execute(text(f"UPDATE {category} SET categories = :categories WHERE english = :english"), {'categories': updated_categories, 'english': english})
        else:
            db.session.execute(text(f"""
                INSERT INTO {category} (english, spanish, polish, categories)
                VALUES (:english, :spanish, :polish, :categories)
            """), {'english': english, 'spanish': spanish, 'polish': polish, 'categories': categories})

    db.session.commit()
    return jsonify({'message': 'Translations added successfully'}), 200




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

    existing_record = db.session.execute(text(f'SELECT * FROM {table_name} WHERE english = :english'),
                                         {'english': english}).fetchone()
    if existing_record:
        return jsonify({'result': 'error', 'message': 'The English word already exists in the table.'})

    db.session.execute(
        text(
            f'INSERT INTO {table_name} (english, spanish, polish, categories) VALUES (:english, :spanish, :polish, :categories)'),
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
        existing_record = db.session.execute(text(f'SELECT * FROM {table_name} WHERE english = :new_english'),
                                             {'new_english': new_english}).fetchone()
        if existing_record:
            return jsonify({'result': 'error', 'message': 'The new English word already exists in the table.'})

    db.session.execute(
        text(
            f'UPDATE {table_name} SET english = :new_english, spanish = :spanish, polish = :polish, categories = :categories WHERE english = :english'),
        {'new_english': new_english, 'spanish': spanish, 'polish': polish, 'categories': categories,
         'english': english})
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
