# Description: Script to setup the environment for the project
pip install -r requirements.txt

# Downloading spaCy models - Those are large files (~1.5 Gb), so it may take a while
python -m spacy download en_core_web_lg
python -m spacy download pl_core_news_lg
python -m spacy download es_core_news_lg
