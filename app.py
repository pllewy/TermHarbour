from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def main_page():
    x = [1, 2, 3, 4]
    return render_template('main_page.html', x=x)


@app.route('/dictionary')
def dictionary():
    return ('<div>Dictionary tab.</div>'
            '<a href="/" >Press here to go back to main menu</>')


@app.route('/glossary')
def glossary():
    with open('./database/basefile1.txt', 'r') as file:
        # Read the file line by line
        lines = file.readlines()

        # Split the lines and remove any leading or trailing whitespace
        lines = [line.strip() for line in lines]
    return render_template('glossaries.html', file_contents=lines)

@app.route('/upload')
def upload_file():
    return render_template('upload.html')

    # return ('<div>Dictionary tab.</div>'
            # '<a href="/" >Press here to go back to main menu</>')

@app.route('/', methods=['POST'])
def translate():
    if request.method == 'POST':
        # Access form data
        text = request.form['text']
        source_language = request.form['source']
        target_language = request.form['target']

        # Process the form data (e.g., perform translation)
        # Replace this with your translation logic

        # For demonstration, let's just return the form data
        # return f'Text: {text}, Source Language: {source_language}, Target Language: {target_language}'
        return render_template('main_page.html',
                               source_language=source_language,
                               target_language=target_language,
                               text=text)
    else:
        return render_template('main_page.html',
                               source_language="source_language",
                               target_language="target_language",
                               text="text")


if __name__ == '__main__':
    app.run(debug=True)
