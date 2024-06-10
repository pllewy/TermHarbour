import sqlite3

from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text

from static.AI_modules.alignment import align, align_sentences
from static.text_batches import create_text_batches
from static.timer import measure_time
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


def tag_terms(terms, input_text):
    for word in terms:
        if f'<span style="color: green;">{word}</span>' not in input_text:
            input_text.append(f'<span style="color: red;">{word}</span>')
    input_text.append('<br>')


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

        # Read text from files
        source_text = read_text_from_file(source_file_path)
        target_text = read_text_from_file(target_file_path)

        # Extract GLOBAL terms from text
        source_terms = extract_terms(source_text, source_lang)
        target_terms = extract_terms(target_text, target_lang)

        print("SOURCE TERMS:", len(source_terms))
        print("TARGET TERMS:", len(target_terms))

        result_term_list = []

        source_batches = []
        target_batches = []
        if batching_method == 'PARAGRAPH':
            # Create text batches for faster simalign
            # returns list of words (for closer paragraph matching)
            source_batches, target_batches = create_text_batches(source_text, target_text)

            no_batches_diff = abs(len(source_batches) - len(target_batches))

            iterator = min(len(source_batches), len(target_batches))
        else:
            iterator = 1

        for i in range(iterator):

            if batching_method == 'PARAGRAPH':
                curr_src_batch = source_batches[i]
                curr_tgt_batch = target_batches[i]
            else:
                curr_src_batch = preprocess_text(source_text).split(' ')
                curr_tgt_batch = preprocess_text(target_text).split(' ')

            print("\nLIST LENGTHS: ", len(curr_src_batch), len(curr_tgt_batch))
            alignment = align(curr_src_batch, curr_tgt_batch)

            source_batch_terms = extract_terms(' '.join(curr_src_batch), source_lang, preprocessing=False)
            target_batch_terms = extract_terms(' '.join(curr_tgt_batch), target_lang, preprocessing=False)

            print("SOURCE BATCH TERMS BY SEBA: ", len(source_batch_terms), source_batch_terms)
            print("TARGET BATCH TERMS BY SEBA: ", len(target_batch_terms), target_batch_terms)

            print("ALIGNMENT: ", len(alignment), alignment)

            tgt_little_terms = []
            # For each multi-word term in target batch
            for term in target_batch_terms:
                # Split it into words
                tgt_little_terms.append(term.split('_'))

            print("\nTARGET LITTLE TERMS: ", tgt_little_terms)

            # For each multi-word term in source batch
            for term in source_batch_terms:
                # Split it into words
                src_little_terms = term.split('_')

                print("\nSOURCE LITTLE TERMS: ", src_little_terms)
                match_result = []
                for l in range(len(tgt_little_terms)):
                    match_result.append(0)

                # For each word in source term
                for little_term in src_little_terms:
                    # Get all alignments of this word
                    matching_tuples = [t[1] for t in alignment if t[0].lower() == little_term.lower()]
                    # Remove duplicates
                    matching_tuples = list(set(matching_tuples))
                    print("MATCHING TUPLES: ", little_term, " ", matching_tuples)

                    # Count matching words in tgt_little_terms
                    match_scores = []

                    for tgt_term in tgt_little_terms:
                        match_count = sum(1 for word in tgt_term if word in matching_tuples)
                        match_scores.append(match_count)
                    print("MATCH SCORES: ", little_term, " ", match_scores)

                    for i in range(len(match_scores)):
                        if match_scores[i] > 0:
                            match_scores[i] = 1
                    match_result = [x + y for x, y in zip(match_result, match_scores)]

                terms_result = []
                # Take each target term that has more than half of the words matched
                for k in range(len(tgt_little_terms)):
                    # Another possible condition <= len(tgt_little_terms[k])
                    if match_result[k] > len(tgt_little_terms[k]) // 2:
                        terms_result.append(tgt_little_terms[k])

                if len(terms_result) > 0:
                    result_term_list.append([term, terms_result])
                print("MATCH RESULT: ", term, " ", match_result, " ", terms_result)

                print("RESULT TERM LIST: ", len(result_term_list))

        print("RESULT TERM LIST with duplicates: ", len(result_term_list))

        for i in range(len(result_term_list)):
            for j in range(i + 1, len(result_term_list)):
                if result_term_list[i][0] == result_term_list[j][0]:
                    result_term_list[i][1] += result_term_list[j][1]
                    result_term_list[j][1] = []

        result_term_list = [term for term in result_term_list if term[1]]

        for line in range(len(result_term_list)):
            result_set = []
            for sublist_index in range(len(result_term_list[line][1])):
                term = ""
                for word in range(len(result_term_list[line][1][sublist_index])):
                    term = term + result_term_list[line][1][sublist_index][word] + " "
                result_set.append(term)
            result_term_list[line] = [result_term_list[line][0], list(set(result_set))]

        print("RESULT TERM LIST without duplicates: ", len(result_term_list))

        print("\n\nRESULT TERM LIST: ", result_term_list)

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


@measure_time
def extract_terms(input_text, lang, preprocessing=True):
    nlp = load_spacy_model(lang)
    if preprocessing:
        text_preprocessed = preprocess_text(input_text)
    else:
        text_preprocessed = input_text
    terms_ner = extract_ner_terms(input_text, nlp)
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
