![Nie działa](/images/sajad-nori-s1puI2BWQzQ-unsplash.jpg "Optional title")

["Obrazek?"](/images/ai-generative-cute-cat-isolated-on-solid-background-photo.jpg "xD")

!["blabla"](/images/translation.png)

![Settings Window](hhttps://github.com/pllewy/TermHarbour/master/images/translation.png)

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

## Application modules

## Glossary

## File upload

## Live translation