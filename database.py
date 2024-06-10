
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
