
# Term Harbour

Welcome to Term Harbour, your AI-powered translation assistant. This guide will walk you through the features and functionalities of our  specialised term extraction, categorisation and verification tool, ensuring you can use it effectively to load and verify your texts.

## Features

- Main Page: A page where you can input text, source language, and target language for recoginition, whether all terms have been accurately translated.
- Glossary: A page that displays already translated and categorised terms from a chosen domain
- Upload: A page where users can upload a file for text extraction. The given list of terms can be further loaded into glossary database under given domain.

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

Check documentation folder in ./documentation for more information.
## Usage

Navigate to the main page at `http://localhost:5000/`. From there, you can access the other features of the application.

In ./test_files there are sample files that can be used for testing the application.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## Authors
Maurycy Oprus - maurycyoprus@gmail.com \
Sebastian Piotrowski - sebpiot13@gmail.com \
Paweł Lewicki - https://www.linkedin.com/in/pllewicki/ \
Adam Mickiewicz University, Poznań, Poland 2023-2024

## License

[MIT](https://choosealicense.com/licenses/mit/)

## Acknowledgements

- Masoud Jalili Sabet, Philipp Dufter, François Yvon, and Hinrich Schütze. 2020. SimAlign: High Quality Word Alignments Without Parallel Training Data Using Static and Contextualized Embeddings. In Findings of the Association for Computational Linguistics: EMNLP 2020, pages 1627–1643, Online. Association for Computational Linguistics.
- Honnibal, M. & Montani, I., 2017. spaCy 2: Natural language understanding with Bloom embeddings, convolutional neural networks and incremental parsing.
