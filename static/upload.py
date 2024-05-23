import os


def save_file(source_file):
    if source_file.filename == '':
        return 'No selected file', 400

    save_path = os.path.join('.', 'input_files', source_file.filename)
    source_file.save(save_path)

    return save_path


def get_glossary_names():
    glossary_files = []
    database_dir = './glossaries'

    for filename in os.listdir(database_dir):
        if os.path.isfile(os.path.join(database_dir, filename)):
            with open(os.path.join(database_dir, filename), 'r') as file:
                # Append the file contents to the list
                glossary_files.append(filename)

    return glossary_files
