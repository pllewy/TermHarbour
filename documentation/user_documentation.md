

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

## Usage

Navigate to the main page at `http://localhost:5000/`. From there, you can access the other features of the application.

In ./input_files there are sample files that can be used for testing the application.

## Navigation

!["Navigation bar"](/images/navbar.png)

The navigatation in the app is via navbar. 

## Live translation - main page
!["Translation"](/images/translation.png)

Live translation page is a component which allows user to check, whether all technical terms that are in the original version of the document have been included in translated version.

The main interface is divided into two primary sections with following subparts:

**Source Text Section**:
   - **Source Language**: Select the language of the text you want to translate from list. The application supports english, polish and spanish as translation languages
   - **Text to Translate**: Input the text you want to translate here. This field is contenteditable, allowing you to type or paste text directly into it.

**Target Text Section**:
   - **Target Language**: Select the language you want your text to be translated into.The application supports english, polish and spanish as translation languages
   - **Translated Text**: The translated text will appear here after you initiate the translation. This field is also contenteditable, allowing you to make manual adjustments if necessary.


### Usage

### Source Language
   1. Locate the dropdown menu labeled "Source language".
   2. Click the dropdown and select the language of the text you want to translate. Options currently include English (en), Polish (pl), and Spanish (es).

### Target Language
   1. Locate the dropdown menu labeled "Target language".
   2. Click the dropdown and select the language you want to translate the text into. Options currently include English (en), Polish (pl), and Spanish (es).

### Entering Source Text
   1. Click inside the "Text to translate" field. This is a large text area designed to accommodate substantial amounts of text.
   2. Type or paste the text you wish to check.

### Entering Translation
   1. Click inside the "Translated text" field. This is a large text area designed to accommodate substantial amounts of text.
   2. Type or paste the text you wish to check.

### Checking Word alignment
   1. After entering the source text and target text ensure that both the source and target languages are correctly selected.
   2. Click the "Translate" button to start the process of verification if all the technical terms are included in both texts.
   3. All positively verified terms are highlighted in green while the terms that have not been found are highlighted red.

### Manual Adjustments
   1. Both text fields are contenteditable. After the verification is complete, you can click inside this field to make any necessary adjustments to the texts.

## Glossary
!["Glossary"](/images/glossary.png)

The Glossary tab in the application provides a user-friendly interface to interact with the glossary database. Here's how to use it:

### Viewing the Glossary
1. Navigate to the Glossary tab in the application.
2. By default, the glossary from the 'medicine' table is displayed. If you want to view a different table, use the dropdown menu to select the table you want to view.
3. The glossary is displayed in a table format with columns for English, Spanish, Polish, and Categories.

### Adding a New Record
1. To add a new record to the glossary, click on the 'Add term' button.
2. A form will appear where you can input the English term, its Spanish and Polish translations, and the categories it belongs to.
3. After filling out the form, click on the 'Confirm' button to add the record to the glossary.

### Editing an Existing Record
1. To edit an existing record, click on the 'Edit' button next to the record you want to edit.
2. A form will appear with the current details of the record. You can change the English term, its Spanish and Polish translations, and the categories it belongs to.
3. After making your changes, click on the 'Confirm' button to update the record in the glossary.


### Deleting a Record
1. To delete a record, click on the 'Delete' button next to the record you want to delete.

Remember, any changes you make in the Glossary tab will be reflected in the glossary database.

### File upload
!["Upload"](/images/upload.png)

The Upload tab in the application allows you to upload source and target files for text alignment and term extraction. Here's how to use it:
### Selecting Language and Domain
1. Before uploading the files, you can select the target language and domain from the dropdown menus.
2. The target language is the language of the target file. The available options are English, Spanish, and Polish.
3. The domain is the field of study or industry to which the text belongs. This helps in better categorization and identification of terms.

### Uploading Files
1. Navigate to the Upload tab in the application.
2. You will see two file input fields labeled 'Source File' and 'Target File'.
3. Click on the field to select the file from your device or drag and drop it to the chosen field.
4. Repeat the third step for the second file.
5. After selecting both files, click on the 'Get terms' button to upload the files to the server and start the extraction process.


The application will align the source and target texts, extract terms, and display the results. You can then view the alignment and extracted terms in the table below.
## Additional Notes

- **Responsive Design**: The layout is designed to be responsive, meaning it should work well on various screen sizes, from desktop monitors to mobile devices.
- **Form Controls**: The text areas for both source and translated text are designed to be user-friendly, with adequate space and scrollable content areas to manage longer texts.
