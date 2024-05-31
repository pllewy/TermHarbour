from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Importing necessary modules and functions from the static directory
import os
import warnings
warnings.filterwarnings("ignore", category=FutureWarning, module='huggingface_hub')

# Initializing Flask app and SQLAlchemy
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'glossary.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Defining the Glossary model for SQLAlchemy
class Glossary(db.Model):
    __tablename__ = 'medicine'
    english = db.Column(db.String(80), primary_key=True)
    spanish = db.Column(db.String(80), nullable=True)
    polish = db.Column(db.String(80), nullable=True)
    categories = db.Column(db.String(255), nullable=True)

@app.route('/', methods=['GET', 'POST'])
def main_page():
    """
    Route for the main_page. Handles both GET and POST requests.
    For POST requests, it takes source and target texts and languages from the form,
    aligns the sentences, tags technical terms, and returns the response.
    For GET requests, it simply renders the main_page.
    """
    # Code omitted for brevity

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    """
    Route for uploading files. Handles both GET and POST requests.
    For POST requests, it takes source and target files, language, and domain from the form,
    saves the files, extracts terms, aligns them, and returns the response.
    For GET requests, it renders the upload page.
    """
    # Code omitted for brevity

@app.route('/tables', methods=['GET'])
def get_tables():
    """
    Route for getting the names of all tables in the database.
    Returns a JSON response with the table names.
    """
    # Code omitted for brevity

@app.route('/categorize', methods=['POST'])
def categorize_text():
    """
    Route for categorizing text. Takes category, language, and text from the JSON request,
    categorizes the text, and returns the categories.
    """
    # Code omitted for brevity

@app.route('/glossary')
def glossary():
    """
    Route for the glossary page. Takes the table name from the query parameters,
    fetches the records from the table, and renders the glossary page with the records.
    """
    # Code omitted for brevity

@app.route('/add', methods=['POST'])
def add_record():
    """
    Route for adding a record to a table. Takes table name, English, Spanish, Polish words, and categories from the form,
    adds the record to the table, and returns the result.
    """
    # Code omitted for brevity

@app.route('/edit/<string:english>', methods=['POST'])
def edit_record(english):
    """
    Route for editing a record in a table. Takes the English word from the URL,
    and new English, Spanish, Polish words, and categories from the form,
    updates the record in the table, and returns the result.
    """
    # Code omitted for brevity

@app.route('/delete/<string:english>', methods=['POST'])
def delete_record(english):
    """
    Route for deleting a record from a table. Takes the English word from the URL and table name from the form,
    deletes the record from the table, and returns the result.
    """
    # Code omitted for brevity

@app.route('/initialize')
def initialize():
    """
    Route for initializing the database. Creates all tables and commits the changes.
    Returns a success message.
    """
    # Code omitted for brevity

if __name__ == '__main__':
    app.run(debug=True)