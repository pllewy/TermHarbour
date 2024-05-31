import os

def save_file(source_file):
    """
    Saves the provided file to the 'input_files' directory.

    Args:
        source_file (werkzeug.datastructures.FileStorage): The file to be saved.

    Returns:
        str: The path where the file was saved.
        int: HTTP status code 400 if no file was selected.
    """
    if source_file.filename == '':
        return 'No selected file', 400

    save_path = os.path.join('input_files', source_file.filename)
    source_file.save(save_path)

    return save_path


def get_glossary_names():
    """
    Retrieves the names of all glossary files in the 'glossaries' directory.

    Returns:
        list: A list of glossary file names.
    """
    glossary_files = []
    database_dir = './glossaries'

    for filename in os.listdir(database_dir):
        if os.path.isfile(os.path.join(database_dir, filename)):
            glossary_files.append(filename)

    return glossary_files