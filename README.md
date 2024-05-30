# Term Harbour

This is a Flask application that provides several functionalities including text extraction, translation, and term processing.

## Features

- Main Page: A page where users can input text, source language, and target language for processing.
- Glossary: A page that displays the contents of glossary files found in the `./glossaries` directory.
- Upload: A page where users can upload a file for text extraction and translation. The extracted terms are then post-processed.
- Test: A page for testing the extraction and translation of terms from a specific file.

## Setup

1. Clone the repository.
2. Install the required Python packages using setuptools. Run the following command in the terminal.\
WARNING: This will install big models for spaCy (~2 Gb).

   ```
   ./setup.sh
    ```
    or
    ```
    pip install -r requirements.txt
   python -m spacy download en_core_web_lg
   python -m spacy download es_core_news_lg
   python -m spacy download pl_core_news_lg
   ```

3. Run the Flask application:
    ```
    python app.py
    ```

## Usage

Navigate to the main page at `http://localhost:5000/`. From there, you can access the other features of the application.

In ./input_files there are sample files that can be used for testing the application.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

[MIT](https://choosealicense.com/licenses/mit/)

## Acknowledgements

- Masoud Jalili Sabet, Philipp Dufter, François Yvon, and Hinrich Schütze. 2020. SimAlign: High Quality Word Alignments Without Parallel Training Data Using Static and Contextualized Embeddings. In Findings of the Association for Computational Linguistics: EMNLP 2020, pages 1627–1643, Online. Association for Computational Linguistics.
- Honnibal, M. & Montani, I., 2017. spaCy 2: Natural language understanding with Bloom embeddings, convolutional neural networks and incremental parsing.
- 