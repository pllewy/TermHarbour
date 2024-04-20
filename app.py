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


@app.route('/translate', methods=['POST'])
def translate():
    if request.method == 'POST':
        # Access form data
        text = request.form['text']
        source_language = request.form['source']
        target_language = request.form['target']

        # Process the form data (e.g., perform translation)
        # Replace this with your translation logic

        # For demonstration, let's just return the form data
        return f'Text: {text}, Source Language: {source_language}, Target Language: {target_language}'
    else:
        # Handle other request methods (e.g., GET)
        return 'Method Not Allowed', 405


if __name__ == '__main__':
    app.run(debug=True)
