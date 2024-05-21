# Term Harbour

This is a Flask application that provides several functionalities including text extraction, translation, and term processing.

## Features

- Main Page: A page where users can input text, source language, and target language for processing.
- Dictionary: A simple dictionary tab.
- Glossary: A page that displays the contents of glossary files found in the `./glossaries` directory.
- Upload: A page where users can upload a file for text extraction and translation. The extracted terms are then post-processed.
- Test: A page for testing the extraction and translation of terms from a specific file.

## Setup

1. Clone the repository.
2. Install the required Python packages using pip:
    ```
    pip install -r requirements.txt
    ```
3. Run the Flask application:
    ```
    python app.py
    ```

## Usage

Navigate to the main page at `http://localhost:5000/`. From there, you can access the other features of the application.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

[MIT](https://choosealicense.com/licenses/mit/)